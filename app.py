"""Stock Screener — Streamlit + yfinance.

Page layout:
  1. Ticker search  — bypass screening; show full profile for any single symbol.
  2. Screen Setup   — Sector → Universe → Market Cap → Trend → Momentum → Valuation.
  3. Market Overview— Finviz-style treemap: individual S&P 500 stocks grouped by
                      sector, sized by market-cap, colored by daily % change.
                      Clicking a sector label zooms into it (Plotly native drill-down).
                      Clicking a stock tile opens a detail panel below.
  4. Biggest Movers — top gainers / losers for the selected universe with a
                      1D / 1W / 1M / 3M / YTD period toggle.
  5. Results        — screener funnel, results table (with full ratio columns),
                      sector heatmap, and row-click detail panel.
"""

from __future__ import annotations

import concurrent.futures
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

import universe

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

PRICE_BATCH = 200

_ALL_SECTORS = [
    "Basic Materials", "Communication Services", "Consumer Cyclical",
    "Consumer Defensive", "Energy", "Financial Services", "Healthcare",
    "Industrials", "Real Estate", "Technology", "Utilities",
]

# Diverging red → dark neutral → green; deep saturated for Bloomberg aesthetic.
_HEATMAP_SCALE = [
    [0.00, "#7B0000"],
    [0.20, "#DD1111"],
    [0.50, "#1C2535"],
    [0.80, "#00AA44"],
    [1.00, "#005522"],
]

INDEX_GROUPS = {
    "Large Cap": ["S&P 500", "NASDAQ-100"],
    "Mid Cap":   ["S&P MidCap 400", "Russell Midcap"],
    "Small Cap": ["Russell 2000"],
}

# Hardcoded sector-median benchmarks (yfinance sector name → ratio dict).
# Percent-based ratios (roe, roa, margins, eps_growth) stored as decimals (0.22 = 22%).
_SECTOR_BENCHMARKS: dict[str, dict[str, float | None]] = {
    "Technology": {
        "pe": 28.0, "pb": 7.5, "ev_ebitda": 20.0, "de": 0.40,
        "current_ratio": 1.8, "quick_ratio": 1.6,
        "roe": 0.22, "roa": 0.12,
        "gross_margin": 0.55, "op_margin": 0.20, "net_margin": 0.17,
        "fwd_pe": 24.0, "peg": 1.8, "ps": 7.0, "eps_growth": 0.12,
    },
    "Financial Services": {
        "pe": 14.0, "pb": 1.6, "ev_ebitda": 12.0, "de": 2.50,
        "current_ratio": None, "quick_ratio": None,
        "roe": 0.12, "roa": 0.012,
        "gross_margin": None, "op_margin": 0.30, "net_margin": 0.24,
        "fwd_pe": 12.0, "peg": 1.5, "ps": 2.5, "eps_growth": 0.08,
    },
    "Healthcare": {
        "pe": 22.0, "pb": 3.8, "ev_ebitda": 14.0, "de": 0.50,
        "current_ratio": 2.0, "quick_ratio": 1.6,
        "roe": 0.16, "roa": 0.08,
        "gross_margin": 0.55, "op_margin": 0.15, "net_margin": 0.11,
        "fwd_pe": 18.0, "peg": 1.6, "ps": 2.5, "eps_growth": 0.10,
    },
    "Consumer Cyclical": {
        "pe": 20.0, "pb": 4.0, "ev_ebitda": 12.0, "de": 0.80,
        "current_ratio": 1.2, "quick_ratio": 0.7,
        "roe": 0.18, "roa": 0.07,
        "gross_margin": 0.32, "op_margin": 0.09, "net_margin": 0.06,
        "fwd_pe": 17.0, "peg": 1.5, "ps": 1.2, "eps_growth": 0.08,
    },
    "Consumer Defensive": {
        "pe": 20.0, "pb": 4.5, "ev_ebitda": 13.5, "de": 0.70,
        "current_ratio": 0.9, "quick_ratio": 0.5,
        "roe": 0.20, "roa": 0.08,
        "gross_margin": 0.30, "op_margin": 0.11, "net_margin": 0.08,
        "fwd_pe": 18.0, "peg": 2.2, "ps": 0.9, "eps_growth": 0.06,
    },
    "Industrials": {
        "pe": 19.0, "pb": 3.5, "ev_ebitda": 13.0, "de": 0.70,
        "current_ratio": 1.4, "quick_ratio": 1.0,
        "roe": 0.15, "roa": 0.06,
        "gross_margin": 0.32, "op_margin": 0.11, "net_margin": 0.08,
        "fwd_pe": 17.0, "peg": 1.8, "ps": 1.8, "eps_growth": 0.09,
    },
    "Communication Services": {
        "pe": 17.0, "pb": 2.5, "ev_ebitda": 10.0, "de": 0.60,
        "current_ratio": 1.2, "quick_ratio": 1.1,
        "roe": 0.12, "roa": 0.05,
        "gross_margin": 0.50, "op_margin": 0.16, "net_margin": 0.12,
        "fwd_pe": 15.0, "peg": 1.3, "ps": 2.5, "eps_growth": 0.09,
    },
    "Energy": {
        "pe": 12.0, "pb": 1.5, "ev_ebitda": 6.0, "de": 0.40,
        "current_ratio": 1.2, "quick_ratio": 0.9,
        "roe": 0.14, "roa": 0.07,
        "gross_margin": 0.35, "op_margin": 0.17, "net_margin": 0.12,
        "fwd_pe": 11.0, "peg": 0.9, "ps": 1.2, "eps_growth": 0.07,
    },
    "Basic Materials": {
        "pe": 14.0, "pb": 2.0, "ev_ebitda": 8.0, "de": 0.50,
        "current_ratio": 1.5, "quick_ratio": 1.0,
        "roe": 0.12, "roa": 0.06,
        "gross_margin": 0.28, "op_margin": 0.12, "net_margin": 0.09,
        "fwd_pe": 12.0, "peg": 1.2, "ps": 1.5, "eps_growth": 0.07,
    },
    "Real Estate": {
        "pe": 30.0, "pb": 1.8, "ev_ebitda": 20.0, "de": 1.50,
        "current_ratio": 0.9, "quick_ratio": 0.9,
        "roe": 0.08, "roa": 0.03,
        "gross_margin": 0.60, "op_margin": 0.35, "net_margin": 0.22,
        "fwd_pe": 22.0, "peg": 3.0, "ps": 5.0, "eps_growth": 0.05,
    },
    "Utilities": {
        "pe": 16.0, "pb": 1.8, "ev_ebitda": 11.0, "de": 1.20,
        "current_ratio": 0.8, "quick_ratio": 0.7,
        "roe": 0.09, "roa": 0.03,
        "gross_margin": 0.40, "op_margin": 0.25, "net_margin": 0.15,
        "fwd_pe": 14.0, "peg": 2.5, "ps": 2.5, "eps_growth": 0.04,
    },
}

_COMMODITIES: dict[str, dict] = {
    "Gold":        {"ticker": "GC=F",  "unit": "$/oz",    "category": "Metals"},
    "Silver":      {"ticker": "SI=F",  "unit": "$/oz",    "category": "Metals"},
    "Platinum":    {"ticker": "PL=F",  "unit": "$/oz",    "category": "Metals"},
    "Palladium":   {"ticker": "PA=F",  "unit": "$/oz",    "category": "Metals"},
    "Copper":      {"ticker": "HG=F",  "unit": "$/lb",    "category": "Metals"},
    "WTI Oil":     {"ticker": "CL=F",  "unit": "$/bbl",   "category": "Energy"},
    "Brent Oil":   {"ticker": "BZ=F",  "unit": "$/bbl",   "category": "Energy"},
    "Natural Gas": {"ticker": "NG=F",  "unit": "$/MMBtu", "category": "Energy"},
    "Wheat":       {"ticker": "ZW=F",  "unit": "¢/bu",    "category": "Grains"},
    "Corn":        {"ticker": "ZC=F",  "unit": "¢/bu",    "category": "Grains"},
    "Soybeans":    {"ticker": "ZS=F",  "unit": "¢/bu",    "category": "Grains"},
}

_CRYPTO_TICKERS: dict[str, str] = {
    "Bitcoin":      "BTC-USD",
    "Ethereum":     "ETH-USD",
    "Solana":       "SOL-USD",
    "XRP":          "XRP-USD",
    "Cardano":      "ADA-USD",
    "Dogecoin":     "DOGE-USD",
    "Polkadot":     "DOT-USD",
    "Avalanche":    "AVAX-USD",
    "Chainlink":    "LINK-USD",
    "Litecoin":     "LTC-USD",
    "Bitcoin Cash": "BCH-USD",
    "Stellar":      "XLM-USD",
}

_CRYPTO_ETFS: dict[str, str] = {
    "IBIT": "BlackRock Bitcoin ETF",
    "FBTC": "Fidelity Bitcoin ETF",
    "ARKB": "ARK Bitcoin ETF",
    "ETHA": "BlackRock Ethereum ETF",
    "BITB": "Bitwise Bitcoin ETF",
}

_ETF_CATEGORIES: dict[str, list[str]] = {
    "Broad Market":       ["SPY", "QQQ", "IWM", "DIA", "VTI", "VOO", "IVV"],
    "Sector":             ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"],
    "Bonds/Fixed Income": ["TLT", "AGG", "HYG", "LQD", "BND", "SHY", "IEF"],
    "International":      ["EEM", "VEA", "VWO", "EFA", "FXI"],
    "Thematic/Other":     ["ARKK", "GLD", "SLV", "USO", "PDBC"],
    "Crypto ETFs":        ["IBIT", "FBTC", "ARKB", "ETHA", "BITB"],
}

_ETF_NAMES: dict[str, str] = {
    "SPY":  "S&P 500 ETF (SPDR)",               "QQQ":  "NASDAQ-100 ETF (Invesco)",
    "IWM":  "Russell 2000 ETF (iShares)",        "DIA":  "Dow Jones ETF (SPDR)",
    "VTI":  "Total Stock Market ETF (Vanguard)", "VOO":  "S&P 500 ETF (Vanguard)",
    "IVV":  "S&P 500 ETF (iShares)",
    "XLK":  "Technology Select Sector ETF",      "XLF":  "Financial Select Sector ETF",
    "XLE":  "Energy Select Sector ETF",          "XLV":  "Health Care Select Sector ETF",
    "XLI":  "Industrial Select Sector ETF",      "XLY":  "Consumer Discr. Select Sector ETF",
    "XLP":  "Consumer Staples Select Sector ETF","XLU":  "Utilities Select Sector ETF",
    "XLB":  "Materials Select Sector ETF",       "XLRE": "Real Estate Select Sector ETF",
    "XLC":  "Comm. Services Select Sector ETF",
    "TLT":  "20+ Year Treasury Bond ETF (iShares)",
    "AGG":  "Core US Aggregate Bond ETF (iShares)",
    "HYG":  "High Yield Corporate Bond ETF (iShares)",
    "LQD":  "Investment Grade Corp Bond ETF (iShares)",
    "BND":  "Total Bond Market ETF (Vanguard)",  "SHY":  "1-3 Year Treasury Bond ETF (iShares)",
    "IEF":  "7-10 Year Treasury Bond ETF (iShares)",
    "EEM":  "Emerging Markets ETF (iShares)",    "VEA":  "Developed Markets ETF (Vanguard)",
    "VWO":  "Emerging Markets ETF (Vanguard)",   "EFA":  "MSCI EAFE ETF (iShares)",
    "FXI":  "China Large-Cap ETF (iShares)",
    "ARKK": "ARK Innovation ETF",               "GLD":  "Gold ETF (SPDR)",
    "SLV":  "Silver ETF (iShares)",             "USO":  "US Oil Fund ETF",
    "PDBC": "Optimum Yield Diversified Commodity ETF",
    "IBIT": "BlackRock Bitcoin ETF",            "FBTC": "Fidelity Bitcoin ETF",
    "ARKB": "ARK Bitcoin ETF",                  "ETHA": "BlackRock Ethereum ETF",
    "BITB": "Bitwise Bitcoin ETF",
}

# All session-state keys that belong to user-adjustable widgets.
_WIDGET_KEYS = [
    "ticker_search",
    "sector_filter",
    "grp_Large Cap", "grp_Mid Cap", "grp_Small Cap",
    "idx_Large Cap", "idx_Mid Cap", "idx_Small Cap",
    "extra_tickers",
    "use_mktcap", "mc_min_b", "mc_max_b",
    "use_ma50", "use_ma200",
    "use_rsi", "min_rsi",
    "use_growth", "min_growth",
    "use_pe", "max_pe",
    "cap",
    "results",
    "heatmap_ticker",
    "movers_period",
    "movers_gainers",
    "movers_losers",
    "use_fwd_pe", "max_fwd_pe",
    "use_peg",    "max_peg",
    "use_ps",     "max_ps",
    "use_eps_growth", "min_eps_growth",
    "use_surprise",   "min_surprise",
    "use_52h", "max_52h_pct",
    "use_52l", "max_52l_pct",
    "use_rel_str", "min_rel_str",
    "use_fcf_yield", "min_fcf_yield",
    "use_short", "short_range",
    "use_div", "min_div",
    "use_payout", "max_payout",
    "crypto_etf_selected",
    "etf_selected",
    "etf_search",
]


def _reset_all() -> None:
    for k in _WIDGET_KEYS:
        st.session_state.pop(k, None)


# ──────────────────────────────────────────────────────────────────────────────
# Bloomberg Terminal CSS theme
# ──────────────────────────────────────────────────────────────────────────────

_CSS_COMMON = """
/* ── Skeleton shimmer animation ───────────────────────────────────────────── */
@keyframes _skshimmer {
    0%   { background-position: -400px 0; }
    100% { background-position:  400px 0; }
}
.sk-box {
    border-radius: 6px;
    height: 80px;
    margin: 4px 0;
    animation: _skshimmer 1.4s infinite linear;
}
.sk-line {
    border-radius: 4px;
    height: 14px;
    width: 60%;
    margin: 6px 0;
    animation: _skshimmer 1.4s infinite linear;
}

/* ── Ratio cards ───────────────────────────────────────────────────────────── */
.r-card {
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.r-card-title {
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
    padding-bottom: 7px;
}
.r-row { display: flex; flex-wrap: wrap; gap: 10px 16px; }
.r-item { flex: 1; min-width: 72px; }
.r-label { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 3px; }
.r-value { font-size: 1.05rem; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1.1; }
.r-bench { font-size: 0.62rem; margin-top: 3px; }

/* ── Ticker hero ────────────────────────────────────────────────────────────── */
.t-hero { padding: 10px 0 16px; margin-bottom: 12px; }
.t-hero-top { display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 8px; }
.t-sym { font-size: 2rem; font-weight: 900; letter-spacing: -0.03em; line-height: 1; }
.t-name { font-size: 0.9rem; font-weight: 400; margin-top: 2px; opacity: 0.7; }
.t-price { font-size: 2.2rem; font-weight: 900; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.t-chg { font-size: 1.05rem; font-weight: 700; margin-left: 10px; }
.t-pos { color: #00CC66; }
.t-neg { color: #FF3344; }
"""

_CSS_DARK = """
<style>
""" + _CSS_COMMON + """
/* ── Color tokens ────────────────────────────────────────────────────────── */
:root {
    --bg:      #0B0E1A;
    --bg2:     #141927;
    --bg3:     #1A2235;
    --border:  #1E2C42;
    --txt:     #E2E8F0;
    --txt2:    #7A8EA8;
    --green:   #00CC66;
    --red:     #FF3344;
    --gold:    #FFA500;
    --blue:    #1A6DFF;
    --blue2:   #4D94FF;
}

/* ── App shell ───────────────────────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"],
section[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--txt) !important;
}
.block-container { background: var(--bg) !important; padding-top: 0.75rem !important; }

/* ── Typography ──────────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: var(--txt) !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
}
h1 { font-size: 1.75rem !important; }
h3 { font-size: 1.25rem !important; }
p, span, label, div { color: var(--txt); }

/* ── Navigation radio bar ────────────────────────────────────────────────── */
[data-testid="stRadio"] > div {
    gap: 4px !important;
    background: transparent !important;
}
[data-testid="stRadio"] label {
    color: var(--txt2) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 6px 16px !important;
    border-radius: 6px !important;
    border: 1px solid transparent !important;
    transition: all 0.15s !important;
    cursor: pointer !important;
}
[data-testid="stRadio"] label:hover {
    background: var(--bg3) !important;
    color: var(--txt) !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: var(--bg3) !important;
    color: #fff !important;
    border-color: var(--blue) !important;
}
[data-testid="stRadio"] input { display: none !important; }

/* ── Sticky nav ──────────────────────────────────────────────────────────── */
div[data-testid="element-container"]:has(> div > [data-testid="stRadio"]) {
    position: sticky !important;
    top: 0 !important;
    z-index: 999 !important;
    background: var(--bg) !important;
    padding: 8px 0 6px !important;
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 2px !important;
}

/* ── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] p {
    color: var(--txt2) !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}
[data-testid="stMetricValue"] {
    color: var(--txt) !important;
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    font-variant-numeric: tabular-nums !important;
}

/* ── Divider ─────────────────────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 0.6rem 0 !important; }

/* ── Expanders ───────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span {
    color: var(--txt) !important;
    font-weight: 600 !important;
}

/* ── Bordered containers ─────────────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"][style*="border"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-bottom: 1px solid var(--border) !important;
    border-radius: 8px 8px 0 0 !important;
    gap: 2px !important;
}
[data-baseweb="tab"] {
    color: var(--txt2) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    background: transparent !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: var(--txt) !important;
    border-bottom: 2px solid var(--blue) !important;
}
[data-baseweb="tab-panel"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 16px !important;
}

/* ── DataFrame ───────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── Inputs ──────────────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: var(--bg3) !important;
    color: var(--txt) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 2px rgba(26,109,255,0.25) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
[data-testid="stButton"] button {
    background: var(--bg3) !important;
    color: var(--txt) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.15s !important;
}
[data-testid="stButton"] button:hover {
    border-color: var(--blue2) !important;
    color: #fff !important;
}
[data-testid="stButton"] button[kind="primary"] {
    background: var(--blue) !important;
    border-color: var(--blue) !important;
    color: #fff !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    background: var(--blue2) !important;
    border-color: var(--blue2) !important;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--blue), var(--blue2)) !important;
}

/* ── Info/warning banners ────────────────────────────────────────────────── */
[data-testid="stInfo"] {
    background: rgba(26,109,255,0.12) !important;
    border-left: 3px solid var(--blue) !important;
    border-radius: 0 6px 6px 0 !important;
    color: var(--txt) !important;
}
[data-testid="stWarning"] {
    background: rgba(255,165,0,0.12) !important;
    border-left: 3px solid var(--gold) !important;
    border-radius: 0 6px 6px 0 !important;
    color: var(--txt) !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Caption ─────────────────────────────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span {
    color: var(--txt2) !important;
    font-size: 0.78rem !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--txt2); }

/* ── Hide default Streamlit chrome ───────────────────────────────────────── */
#MainMenu, footer, [data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Skeleton colors ─────────────────────────────────────────────────────── */
.sk-box, .sk-line {
    background: linear-gradient(90deg, var(--bg2) 25%, var(--bg3) 50%, var(--bg2) 75%);
    background-size: 400px 100%;
}

/* ── Ratio card colors ───────────────────────────────────────────────────── */
.r-card { background: var(--bg2); border: 1px solid var(--border); }
.r-card-title { color: var(--txt2); border-bottom: 1px solid var(--border); }
.r-label { color: var(--txt2); }
.r-value { color: var(--txt); }
.r-bench { color: var(--txt2); }

/* ── Ticker hero colors ──────────────────────────────────────────────────── */
.t-hero { border-bottom: 1px solid var(--border); }
.t-sym { color: #fff; }
.t-name { color: var(--txt2); }
.t-price { color: #fff; }

/* ── Toggle ──────────────────────────────────────────────────────────────── */
[data-testid="stToggle"] span { font-size: 0.8rem !important; color: var(--txt2) !important; }
</style>
"""

_CSS_LIGHT = """
<style>
""" + _CSS_COMMON + """
:root {
    --bg:      #F2F5FA;
    --bg2:     #FFFFFF;
    --bg3:     #E8EDF5;
    --border:  #CDD5E0;
    --txt:     #0B1628;
    --txt2:    #4A5B75;
    --green:   #00883D;
    --red:     #CC1122;
    --gold:    #B85C00;
    --blue:    #1A5FCC;
    --blue2:   #2E7AFF;
}
.stApp, [data-testid="stAppViewContainer"],
section[data-testid="stMain"] { background: var(--bg) !important; color: var(--txt) !important; }
.block-container { background: var(--bg) !important; padding-top: 0.75rem !important; }
h1, h2, h3, h4, h5, h6 { color: var(--txt) !important; font-weight: 800 !important; }
[data-testid="stRadio"] > div { gap: 4px !important; }
[data-testid="stRadio"] label { color: var(--txt2) !important; font-weight: 600 !important; padding: 6px 16px !important; border-radius: 6px !important; border: 1px solid transparent !important; }
[data-testid="stRadio"] label:has(input:checked) { background: var(--bg3) !important; color: var(--txt) !important; border-color: var(--blue) !important; }
[data-testid="stRadio"] input { display: none !important; }
div[data-testid="element-container"]:has(> div > [data-testid="stRadio"]) { position: sticky !important; top: 0 !important; z-index: 999 !important; background: var(--bg) !important; padding: 8px 0 6px !important; border-bottom: 1px solid var(--border) !important; }
[data-testid="stMetric"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 12px 14px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; }
[data-testid="stMetricLabel"] p { color: var(--txt2) !important; font-size: 0.7rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.09em !important; }
[data-testid="stMetricValue"] { color: var(--txt) !important; font-size: 1.35rem !important; font-weight: 800 !important; }
hr { border-color: var(--border) !important; }
[data-testid="stExpander"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; }
[data-testid="stButton"] button { border-radius: 6px !important; font-weight: 600 !important; }
[data-testid="stButton"] button[kind="primary"] { background: var(--blue) !important; color: #fff !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
#MainMenu, footer, [data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
[data-testid="stToolbar"] { display: none !important; }
.sk-box, .sk-line { background: linear-gradient(90deg, var(--bg2) 25%, var(--bg3) 50%, var(--bg2) 75%); background-size: 400px 100%; }
.r-card { background: var(--bg2); border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.r-card-title { color: var(--txt2); border-bottom: 1px solid var(--border); }
.r-label { color: var(--txt2); }
.r-value { color: var(--txt); }
.r-bench { color: var(--txt2); }
.t-hero { border-bottom: 1px solid var(--border); }
.t-sym { color: var(--txt); }
.t-name { color: var(--txt2); }
.t-price { color: var(--txt); }
.t-pos { color: var(--green); }
.t-neg { color: var(--red); }
</style>
"""


def _inject_css() -> None:
    dark = st.session_state.get("dark_mode", True)
    st.markdown(_CSS_DARK if dark else _CSS_LIGHT, unsafe_allow_html=True)


def _skeleton(n_cols: int = 5, height: int = 80) -> None:
    cols = st.columns(n_cols)
    for col in cols:
        col.markdown(
            f'<div class="sk-box" style="height:{height}px"></div>',
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────────────────────────────────────
# Price data
# ──────────────────────────────────────────────────────────────────────────────

def _compute_rsi(close: pd.Series, period: int = 14) -> float | None:
    if isinstance(close, pd.DataFrame):
        close = close.squeeze()
    if len(close) < period + 1:
        return None
    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_gain = float(gain.ewm(com=period - 1, min_periods=period).mean().iloc[-1])
    avg_loss = float(loss.ewm(com=period - 1, min_periods=period).mean().iloc[-1])
    if avg_loss == 0:
        return 100.0
    return round(100.0 - 100.0 / (1.0 + avg_gain / avg_loss), 2)


def _pct(close: pd.Series, n: int) -> float | None:
    """Return % change from n bars ago to now, or None if not enough data."""
    if len(close) > n:
        ref = float(close.iloc[-(n + 1)])
        if ref > 0:
            return round((float(close.iloc[-1]) / ref - 1) * 100, 2)
    return None


@st.cache_data(show_spinner=False, ttl=60 * 30)
def fetch_price_batch(tickers: tuple[str, ...]) -> dict[str, dict]:
    data = yf.download(
        list(tickers), period="1y", interval="1d",
        group_by="ticker", auto_adjust=True, threads=True, progress=False,
    )
    out: dict[str, dict] = {}
    multi = isinstance(data.columns, pd.MultiIndex)
    for t in tickers:
        try:
            series = data[t]["Close"] if multi else data["Close"]
            close  = series.dropna()
            if close.empty:
                continue
            cur  = float(close.iloc[-1])
            prev = float(close.iloc[-2]) if len(close) >= 2 else None

            # YTD: first trading day of the current calendar year.
            cur_year   = close.index[-1].year
            ytd_slice  = close[close.index.year == cur_year]
            ytd_chg    = _pct(ytd_slice, len(ytd_slice) - 1) if len(ytd_slice) >= 2 else None

            out[t] = {
                "price":        cur,
                "ma50":         float(close.tail(50).mean())  if len(close) >= 50  else None,
                "ma200":        float(close.tail(200).mean()) if len(close) >= 200 else None,
                "rsi":          _compute_rsi(close),
                "daily_change": round((cur / prev - 1) * 100, 2) if prev else None,
                "chg_1w":       _pct(close, 5),
                "chg_1m":       _pct(close, 21),
                "chg_3m":       _pct(close, 63),
                "chg_ytd":      ytd_chg,
                "chg_1y":       _pct(close, min(len(close) - 1, 252)),
            }
        except (KeyError, IndexError, ValueError):
            continue
    return out


def fetch_prices(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    chunks = [tickers[i : i + PRICE_BATCH] for i in range(0, len(tickers), PRICE_BATCH)]
    bar = st.progress(0.0, text="Downloading price history…")
    for i, chunk in enumerate(chunks, start=1):
        out.update(fetch_price_batch(tuple(chunk)))
        bar.progress(i / len(chunks), text=f"Downloading price history… ({i}/{len(chunks)})")
    bar.empty()
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Fundamentals
# ──────────────────────────────────────────────────────────────────────────────

def _to_float(value):
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return f if f == f and f not in (float("inf"), float("-inf")) else None


@st.cache_data(show_spinner=False, ttl=60 * 30)
def fetch_fundamentals(ticker: str) -> dict:
    try:
        t_obj = yf.Ticker(ticker)
        info  = t_obj.info or {}

        def _g(*keys):
            """Return the first non-null float found across several yfinance key aliases."""
            for k in keys:
                v = _to_float(info.get(k))
                if v is not None:
                    return v
            return None

        # yfinance returns debtToEquity as a percentage (e.g. 79.5 ≡ 0.795× ratio).
        de_pct = _g("debtToEquity")
        de = round(de_pct / 100, 3) if de_pct is not None else None

        # Earnings surprise from earnings_history DataFrame (most recent quarter).
        surprise_pct: float | None = None
        try:
            eh = t_obj.earnings_history
            if eh is not None and not eh.empty:
                last = eh.sort_index().iloc[-1]
                # Try explicit surprise column first (various yfinance column spellings).
                for col in ("Surprise(%)", "surprisePercent", "Surprise (%)", "surprise_pct"):
                    sv = _to_float(last.get(col))
                    if sv is not None:
                        # Some versions return a fraction (0.05), others a percent (5.0).
                        surprise_pct = sv / 100 if abs(sv) > 2 else sv
                        break
                else:
                    # Compute from actual vs. estimate columns.
                    act = _to_float(
                        last.get("Reported EPS") or last.get("epsActual") or last.get("EPS Actual")
                    )
                    est = _to_float(
                        last.get("Consensus EPS") or last.get("epsEstimate")
                        or last.get("EPS Estimate") or last.get("Estimate")
                    )
                    if act is not None and est and est != 0:
                        surprise_pct = (act - est) / abs(est)
        except Exception:
            pass

        price    = _g("currentPrice", "regularMarketPrice")
        mktcap   = _g("marketCap")
        high52   = _g("fiftyTwoWeekHigh")
        low52    = _g("fiftyTwoWeekLow")
        fcf_raw  = _g("freeCashflow")
        prox_high = round((high52 - price) / high52, 4) if (high52 and price) else None
        prox_low  = round((price - low52) / low52, 4)  if (low52 and price)  else None
        fcf_yield = round(fcf_raw / mktcap, 4)         if (fcf_raw and mktcap) else None

        return {
            "name":          info.get("shortName") or info.get("longName") or ticker,
            "pe":            _g("trailingPE", "forwardPE"),
            "fwd_pe":        _g("forwardPE"),
            "peg":           _g("pegRatio", "trailingPegRatio"),
            "ps":            _g("priceToSalesTrailing12Months"),
            "eps_growth":    _g("earningsGrowth", "earningsQuarterlyGrowth"),
            "surprise_pct":  surprise_pct,
            "rev":           _g("revenueGrowth"),
            "mktcap":        mktcap,
            "sector":        info.get("sector"),
            "pb":            _g("priceToBook"),
            "de":            de,
            "current_ratio": _g("currentRatio"),
            "quick_ratio":   _g("quickRatio"),
            "gross_margin":  _g("grossMargins"),
            "op_margin":     _g("operatingMargins"),
            "net_margin":    _g("profitMargins", "netMargins"),
            "ev_ebitda":     _g("enterpriseToEbitda"),
            "roe":           _g("returnOnEquity"),
            "roa":           _g("returnOnAssets"),
            "high52":        high52,
            "low52":         low52,
            "prox_high":     prox_high,
            "prox_low":      prox_low,
            "fcf_yield":     fcf_yield,
            "short_pct":     _g("shortPercentOfFloat"),
            "div_yield":     _g("dividendYield"),
            "payout":        _g("payoutRatio"),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "name": ticker, "pe": None, "fwd_pe": None, "peg": None, "ps": None,
            "eps_growth": None, "surprise_pct": None,
            "rev": None, "mktcap": None, "sector": None,
            "pb": None, "de": None, "current_ratio": None, "quick_ratio": None,
            "gross_margin": None, "op_margin": None, "net_margin": None,
            "ev_ebitda": None, "roe": None, "roa": None,
            "high52": None, "low52": None, "prox_high": None, "prox_low": None,
            "fcf_yield": None, "short_pct": None, "div_yield": None, "payout": None,
            "error": str(exc),
        }


def fetch_fundamentals_many(tickers: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if not tickers:
        return out
    bar = st.progress(0.0, text="Fetching fundamentals…")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(fetch_fundamentals, t): t for t in tickers}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), start=1):
            out[futures[fut]] = fut.result()
            bar.progress(i / len(tickers), text=f"Fetching fundamentals… ({i}/{len(tickers)})")
    bar.empty()
    return out


@st.cache_data(show_spinner=False, ttl=60 * 30)
def fetch_benchmark_returns() -> dict:
    """SPY 1-year return for relative-strength comparison."""
    return fetch_price_batch(("SPY",)).get("SPY", {})


# ──────────────────────────────────────────────────────────────────────────────
# S&P 500 constituent meta — sector + mktcap; used by heatmap & movers.
# Expensive on first load (~500 API calls, 15-25 s). Cached 12 h.
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False, ttl=60 * 60 * 12)
def fetch_sp500_meta() -> pd.DataFrame:
    try:
        tickers = universe.get_sp500()
    except Exception:
        return pd.DataFrame(columns=["Ticker", "Name", "Sector", "Mkt Cap"])

    def _one(t: str) -> dict:
        try:
            info = yf.Ticker(t).info or {}
            return {
                "Ticker":  t,
                "Name":    info.get("shortName") or t,
                "Sector":  info.get("sector") or "Unknown",
                "Mkt Cap": _to_float(info.get("marketCap")),
            }
        except Exception:
            return {"Ticker": t, "Name": t, "Sector": "Unknown", "Mkt Cap": None}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        rows = list(pool.map(_one, tickers))
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Commodity + Crypto price data
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False, ttl=60 * 15)
def fetch_commodity_data() -> pd.DataFrame:
    tickers = [v["ticker"] for v in _COMMODITIES.values()]
    try:
        raw = yf.download(
            tickers, period="1y", interval="1d",
            group_by="ticker", auto_adjust=True, threads=True, progress=False,
        )
    except Exception:
        return pd.DataFrame()
    multi = isinstance(raw.columns, pd.MultiIndex)
    rows = []
    for name, meta in _COMMODITIES.items():
        t = meta["ticker"]
        try:
            close = (raw[t]["Close"] if multi else raw["Close"]).dropna()
            if close.empty:
                continue
            cur  = float(close.iloc[-1])
            prev = float(close.iloc[-2]) if len(close) >= 2 else None
            chg  = round((cur / prev - 1) * 100, 2) if prev else None
            ytd  = close[close.index.year == close.index[-1].year]
            rows.append({
                "Name":     name,
                "Ticker":   t,
                "Category": meta["category"],
                "Unit":     meta["unit"],
                "Price":    cur,
                "Change %": chg,
                "Chg 1W":   _pct(close, 5),
                "Chg 1M":   _pct(close, 21),
                "Chg 3M":   _pct(close, 63),
                "Chg YTD":  _pct(ytd, len(ytd) - 1) if len(ytd) >= 2 else None,
            })
        except Exception:
            continue
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False, ttl=60 * 15)
def fetch_crypto_data() -> pd.DataFrame:
    tickers = list(_CRYPTO_TICKERS.values())
    try:
        raw = yf.download(
            tickers, period="1y", interval="1d",
            group_by="ticker", auto_adjust=True, threads=True, progress=False,
        )
    except Exception:
        raw = pd.DataFrame()

    def _get_meta(ticker: str) -> dict:
        try:
            info = yf.Ticker(ticker).info or {}
            return {
                "market_cap": _to_float(info.get("marketCap")),
                "volume_24h": _to_float(
                    info.get("volume24Hr") or info.get("totalAssets") or info.get("volume")
                ),
            }
        except Exception:
            return {"market_cap": None, "volume_24h": None}

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futs = {pool.submit(_get_meta, t): t for t in tickers}
        meta_map = {futs[f]: f.result() for f in concurrent.futures.as_completed(futs)}

    multi = isinstance(raw.columns, pd.MultiIndex) if not raw.empty else False
    rows = []
    for name, t in _CRYPTO_TICKERS.items():
        try:
            if raw.empty:
                continue
            close = (raw[t]["Close"] if multi else raw["Close"]).dropna()
            if close.empty:
                continue
            cur  = float(close.iloc[-1])
            prev = float(close.iloc[-2]) if len(close) >= 2 else None
            chg  = round((cur / prev - 1) * 100, 2) if prev else None
            meta = meta_map.get(t, {})
            ytd  = close[close.index.year == close.index[-1].year]
            rows.append({
                "Name":       name,
                "Ticker":     t,
                "Price":      cur,
                "Change %":   chg,
                "Market Cap": meta.get("market_cap"),
                "24h Vol":    meta.get("volume_24h"),
                "Chg 1W":     _pct(close, 5),
                "Chg 1M":     _pct(close, 21),
                "Chg 3M":     _pct(close, 63),
                "Chg YTD":    _pct(ytd, len(ytd) - 1) if len(ytd) >= 2 else None,
            })
        except Exception:
            continue
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False, ttl=60 * 60)
def fetch_etf_data() -> pd.DataFrame:
    """Batch-download all curated ETF tickers in one yf.download call (1-hour cache)."""
    all_tickers = [t for tickers in _ETF_CATEGORIES.values() for t in tickers]
    try:
        raw = yf.download(
            all_tickers, period="1y", interval="1d",
            group_by="ticker", auto_adjust=True, threads=True, progress=False,
        )
    except Exception:
        return pd.DataFrame()
    multi = isinstance(raw.columns, pd.MultiIndex)
    rows = []
    for category, tickers in _ETF_CATEGORIES.items():
        for sym in tickers:
            try:
                close = (raw[sym]["Close"] if multi else raw["Close"]).dropna()
                if close.empty:
                    continue
                cur  = float(close.iloc[-1])
                prev = float(close.iloc[-2]) if len(close) >= 2 else None
                chg  = round((cur / prev - 1) * 100, 2) if prev else None
                ytd  = close[close.index.year == close.index[-1].year]
                rows.append({
                    "Category": category,
                    "Ticker":   sym,
                    "Name":     _ETF_NAMES.get(sym, sym),
                    "Price":    cur,
                    "Change %": chg,
                    "Chg 1W":   _pct(close, 5),
                    "Chg 1M":   _pct(close, 21),
                    "Chg 3M":   _pct(close, 63),
                    "Chg YTD":  _pct(ytd, len(ytd) - 1) if len(ytd) >= 2 else None,
                })
            except Exception:
                continue
    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Market Overview heatmap — Finviz-style individual S&P 500 stocks
# ──────────────────────────────────────────────────────────────────────────────

def _fmt_chg(v) -> str:
    return f"{v:+.2f}%" if v is not None and v == v else "—"


def render_market_heatmap(sector_filter: set[str] = frozenset()) -> str | None:
    """Render individual S&P 500 stock tiles grouped by sector.

    Returns the ticker that was clicked (if any), else None.
    Plotly's native treemap drill-down handles sector-click zoom automatically.
    """
    already_loaded = "sp500_meta_loaded" in st.session_state
    if not already_loaded:
        st.info(
            "⏳ **First load** — downloading sector & market-cap data for ~500 S&P 500 "
            "stocks. This takes roughly 20–30 seconds and is then cached for 12 hours."
        )
        _skeleton(5, 80)
        _skeleton(5, 80)

    with st.spinner("Loading S&P 500 constituent data…"):
        meta = fetch_sp500_meta()

    st.session_state["sp500_meta_loaded"] = True

    if meta.empty:
        st.caption("Market overview unavailable.")
        return None

    if sector_filter:
        meta = meta[meta["Sector"].isin(sector_filter)].copy()

    if meta.empty:
        st.caption("No S&P 500 stocks match the selected sector(s).")
        return None

    # Fetch prices for all stocks in view.
    tickers_list = meta["Ticker"].tolist()
    prices: dict[str, dict] = {}
    for i in range(0, len(tickers_list), PRICE_BATCH):
        prices.update(fetch_price_batch(tuple(tickers_list[i : i + PRICE_BATCH])))

    meta = meta.copy()
    meta["Daily Chg %"] = meta["Ticker"].map(lambda t: prices.get(t, {}).get("daily_change"))
    meta["Price"]       = meta["Ticker"].map(lambda t: prices.get(t, {}).get("price"))
    meta["_size"]       = meta["Mkt Cap"].fillna(1e9).clip(lower=1e6)
    meta["_chg_text"]   = meta["Daily Chg %"].apply(_fmt_chg)
    meta = meta.dropna(subset=["Price"])

    if meta.empty:
        st.caption("No price data available for S&P 500 constituents.")
        return None

    known_tickers = set(meta["Ticker"].tolist())

    fig = px.treemap(
        meta, path=["Sector", "Ticker"], values="_size",
        color="Daily Chg %", color_continuous_scale=_HEATMAP_SCALE,
        color_continuous_midpoint=0, range_color=[-3, 3],
        custom_data=["_chg_text", "Name", "Price"],
        hover_data={"_size": False, "_chg_text": False},
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textposition="middle center", textfont_size=11,
        hovertemplate=(
            "<b>%{label}</b> · %{customdata[1]}<br>"
            "Daily: %{customdata[0]}  ·  Price: $%{customdata[2]:.2f}<extra></extra>"
        ),
    )
    fig.update_layout(
        margin=dict(t=10, l=0, r=0, b=0), height=540,
        coloraxis_colorbar=dict(title="Daily %", tickformat="+.1f", len=0.6),
    )

    event = st.plotly_chart(
        fig, use_container_width=True, key="market_heatmap", on_select="rerun",
    )

    clicked: str | None = None
    if event and event.selection:
        for pt in event.selection.get("points", []):
            label = pt.get("label", "")
            if label in known_tickers:
                clicked = label
                break
    return clicked


# ──────────────────────────────────────────────────────────────────────────────
# Screened-results heatmap (also clickable)
# ──────────────────────────────────────────────────────────────────────────────

def render_results_heatmap(df: pd.DataFrame) -> str | None:
    """Render the screened-stock treemap. Returns clicked ticker or None."""
    hm = df.copy()
    hm["Sector"] = hm["Sector"].fillna("Unknown").replace("", "Unknown")
    median_mc = hm["Mkt Cap"].median()
    hm["_size"] = hm["Mkt Cap"].fillna(
        median_mc if pd.notna(median_mc) else 1e9
    ).clip(lower=1e6)
    hm["_chg_text"] = hm["Daily Chg %"].apply(_fmt_chg)

    if hm["Daily Chg %"].isna().all():
        st.caption("Daily change data unavailable — heatmap skipped.")
        return None

    known_tickers = set(hm["Ticker"].tolist())

    fig = px.treemap(
        hm, path=["Sector", "Ticker"], values="_size",
        color="Daily Chg %", color_continuous_scale=_HEATMAP_SCALE,
        color_continuous_midpoint=0, range_color=[-3, 3],
        custom_data=["_chg_text", "Name", "Price", "RSI", "P/E"],
        hover_data={"_size": False, "_chg_text": False},
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textposition="middle center", textfont_size=12,
        hovertemplate=(
            "<b>%{label}</b><br>%{customdata[1]}<br>"
            "Daily: %{customdata[0]}<br>Price: $%{customdata[2]:.2f}<br>"
            "RSI: %{customdata[3]:.1f}<br>P/E: %{customdata[4]:.1f}<extra></extra>"
        ),
    )
    fig.update_layout(
        margin=dict(t=10, l=0, r=0, b=0), height=480,
        coloraxis_colorbar=dict(title="Daily %", tickformat="+.1f", len=0.7),
    )

    event = st.plotly_chart(
        fig, use_container_width=True, key="results_heatmap", on_select="rerun",
    )

    if event and event.selection:
        for pt in event.selection.get("points", []):
            label = pt.get("label", "")
            if label in known_tickers:
                return label
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Biggest Movers
# ──────────────────────────────────────────────────────────────────────────────

_PERIOD_KEY = {
    "1 Day":    "daily_change",
    "1 Week":   "chg_1w",
    "1 Month":  "chg_1m",
    "3 Months": "chg_3m",
    "YTD":      "chg_ytd",
}


def render_biggest_movers(sector_filter: set[str]) -> str | None:
    period = st.radio(
        "Period", list(_PERIOD_KEY.keys()), horizontal=True, key="movers_period",
        index=0,
    )
    p_key = _PERIOD_KEY[period]

    with st.spinner("Loading…"):
        meta = fetch_sp500_meta()

    if meta.empty:
        st.caption("Market data unavailable.")
        return None

    if sector_filter:
        meta = meta[meta["Sector"].isin(sector_filter)]

    tickers_t = tuple(meta["Ticker"].tolist())
    prices: dict[str, dict] = {}
    for i in range(0, len(tickers_t), PRICE_BATCH):
        prices.update(fetch_price_batch(tickers_t[i : i + PRICE_BATCH]))

    rows = []
    for _, row in meta.iterrows():
        t = row["Ticker"]
        p = prices.get(t, {})
        chg = p.get(p_key)
        if chg is not None:
            rows.append({
                "Ticker":    t,
                "Name":      row["Name"],
                "Sector":    row["Sector"],
                "Price":     p.get("price"),
                "Change %":  chg,
            })

    if not rows:
        st.caption(f"No {period} return data available.")
        return None

    df_m = pd.DataFrame(rows).sort_values("Change %", ascending=False).reset_index(drop=True)
    gainers = df_m.head(10).reset_index(drop=True)
    losers  = df_m.tail(10).sort_values("Change %").reset_index(drop=True)
    col_g, col_l = st.columns(2)
    cfg = {
        "Change %": st.column_config.NumberColumn(format="%.2f%%"),
        "Price":    st.column_config.NumberColumn(format="$%.2f"),
    }
    with col_g:
        st.markdown("**🟢 Top Gainers** · click a row to view full profile")
        g_ev = st.dataframe(gainers, use_container_width=True, hide_index=True,
                            column_config=cfg, on_select="rerun",
                            selection_mode="single-row", key="movers_gainers")
    with col_l:
        st.markdown("**🔴 Top Losers** · click a row to view full profile")
        l_ev = st.dataframe(losers, use_container_width=True, hide_index=True,
                            column_config=cfg, on_select="rerun",
                            selection_mode="single-row", key="movers_losers")

    g_rows = (g_ev.selection or {}).get("rows", []) if g_ev else []
    l_rows = (l_ev.selection or {}).get("rows", []) if l_ev else []
    if g_rows and g_rows[0] < len(gainers):
        return gainers.iloc[g_rows[0]]["Ticker"]
    if l_rows and l_rows[0] < len(losers):
        return losers.iloc[l_rows[0]]["Ticker"]
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Analyst ratings + news
# ──────────────────────────────────────────────────────────────────────────────

def _news_date(value) -> str:
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc).strftime("%Y-%m-%d")
        except (ValueError, OverflowError, OSError):
            return ""
    if isinstance(value, str):
        return value[:10]
    return ""


@st.cache_data(show_spinner=False, ttl=60 * 30)
def fetch_detail(ticker: str) -> dict:
    out: dict = {"news": [], "breakdown": None, "error": None}
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}
        out.update({
            "rec_key":     info.get("recommendationKey"),
            "rec_mean":    _to_float(info.get("recommendationMean")),
            "n_analysts":  info.get("numberOfAnalystOpinions"),
            "target_mean": _to_float(info.get("targetMeanPrice")),
            "target_high": _to_float(info.get("targetHighPrice")),
            "target_low":  _to_float(info.get("targetLowPrice")),
            "current":     _to_float(info.get("currentPrice") or info.get("regularMarketPrice")),
        })
        try:
            rec = tk.recommendations
            if rec is not None and not rec.empty:
                r0 = rec.iloc[0]
                out["breakdown"] = {
                    "Strong Buy":  int(r0.get("strongBuy",  0) or 0),
                    "Buy":         int(r0.get("buy",        0) or 0),
                    "Hold":        int(r0.get("hold",       0) or 0),
                    "Sell":        int(r0.get("sell",       0) or 0),
                    "Strong Sell": int(r0.get("strongSell", 0) or 0),
                }
        except Exception:  # noqa: BLE001
            pass
        try:
            for item in (tk.news or [])[:8]:
                c = item.get("content") if isinstance(item, dict) else None
                if isinstance(c, dict):
                    title     = c.get("title")
                    publisher = (c.get("provider") or {}).get("displayName")
                    url       = ((c.get("canonicalUrl") or {}).get("url") or
                                 (c.get("clickThroughUrl") or {}).get("url"))
                    date      = c.get("pubDate")
                else:
                    title = item.get("title"); publisher = item.get("publisher")
                    url   = item.get("link");  date      = item.get("providerPublishTime")
                if title:
                    out["news"].append({
                        "title": title, "publisher": publisher,
                        "url": url, "date": _news_date(date),
                    })
        except Exception:  # noqa: BLE001
            pass
    except Exception as exc:  # noqa: BLE001
        out["error"] = str(exc)
    return out


def render_analyst(ticker: str) -> None:
    detail = fetch_detail(ticker)
    if detail.get("error"):
        st.warning(f"Couldn't load detail for {ticker}: {detail['error']}")
        return
    rec_key = detail.get("rec_key")
    mean    = detail.get("rec_mean")
    consensus = rec_key.replace("_", " ").title() if rec_key and rec_key != "none" else "—"
    tmean, cur, n = detail.get("target_mean"), detail.get("current"), detail.get("n_analysts")
    c1, c2, c3 = st.columns(3)
    c1.metric("Consensus", consensus,
              help=f"Mean {mean:.2f}/5 (1=Strong Buy)" if mean else None)
    if tmean:
        c2.metric("Avg price target", f"${tmean:,.2f}",
                  delta=f"{(tmean/cur-1)*100:+.1f}% vs current" if cur else None)
    else:
        c2.metric("Avg price target", "—")
    c3.metric("# Analysts", int(n) if n else "—")
    bd = detail.get("breakdown")
    if bd and sum(bd.values()) > 0:
        st.caption("Rating breakdown (current month)")
        for col, (label, val) in zip(st.columns(len(bd)), bd.items()):
            col.metric(label, val)
    if detail.get("target_low") and detail.get("target_high"):
        st.caption(f"Target range: ${detail['target_low']:,.2f} – ${detail['target_high']:,.2f}")
    st.markdown("**Recent news**")
    news = detail.get("news") or []
    if not news:
        st.caption("No recent headlines from Yahoo Finance.")
    else:
        for item in news:
            title, url = item["title"], item.get("url")
            meta_str = " · ".join(x for x in (item.get("publisher"), item.get("date")) if x)
            line = f"- [{title}]({url})" if url else f"- {title}"
            if meta_str:
                line += f"  \n  <small>{meta_str}</small>"
            st.markdown(line, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Financial ratios panel
# ──────────────────────────────────────────────────────────────────────────────

def render_financial_ratios(f: dict, sector: str | None = None) -> None:
    def _r(v):   return f"{v:.2f}"      if v is not None else "—"
    def _pct(v): return f"{v*100:.1f}%" if v is not None else "—"
    def _x(v):   return f"{v:.1f}×"    if v is not None else "—"

    bench = _SECTOR_BENCHMARKS.get(sector, {}) if sector else {}
    def _b_r(k):   bv = bench.get(k); return f"avg {_r(bv)}"   if bv is not None else ""
    def _b_pct(k): bv = bench.get(k); return f"avg {_pct(bv)}" if bv is not None else ""
    def _b_x(k):   bv = bench.get(k); return f"avg {_x(bv)}"   if bv is not None else ""

    def _item(label: str, value: str, bench_str: str = "") -> str:
        bench_html = f'<div class="r-bench">{bench_str}</div>' if bench_str else ""
        return (f'<div class="r-item">'
                f'<div class="r-label">{label}</div>'
                f'<div class="r-value">{value}</div>'
                f'{bench_html}</div>')

    def _card(title: str, items_html: str) -> str:
        return (f'<div class="r-card">'
                f'<div class="r-card-title">{title}</div>'
                f'<div class="r-row">{items_html}</div>'
                f'</div>')

    bench_note = f" · <small>sector benchmarks in gray</small>" if bench else ""
    st.markdown(f"**Key Ratios**{bench_note}", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    # ── Left column ───────────────────────────────────────────────────────────
    with col_l:
        # Valuation card
        items = (
            _item("P/E",       _r(f.get("pe")),        _b_r("pe")) +
            _item("P/B",       _r(f.get("pb")),        _b_r("pb")) +
            _item("EV/EBITDA", _x(f.get("ev_ebitda")), _b_x("ev_ebitda")) +
            _item("Fwd P/E",   _r(f.get("fwd_pe")),    _b_r("fwd_pe")) +
            _item("PEG",       _r(f.get("peg")),        _b_r("peg")) +
            _item("P/S",       _r(f.get("ps")),         _b_r("ps"))
        )
        st.markdown(_card("Valuation", items), unsafe_allow_html=True)

        # Balance sheet card
        items = (
            _item("D/E",           _r(f.get("de")),            _b_r("de")) +
            _item("Current Ratio", _r(f.get("current_ratio")), _b_r("current_ratio")) +
            _item("Quick Ratio",   _r(f.get("quick_ratio")),   _b_r("quick_ratio")) +
            _item("Mkt Cap",       f"${f['mktcap']/1e9:.1f}B" if f.get("mktcap") else "—") +
            _item("Rev Growth",    _pct(f.get("rev")))
        )
        st.markdown(_card("Balance Sheet & Liquidity", items), unsafe_allow_html=True)

    # ── Right column ──────────────────────────────────────────────────────────
    with col_r:
        # Profitability card
        items = (
            _item("Gross Margin", _pct(f.get("gross_margin")), _b_pct("gross_margin")) +
            _item("Oper. Margin", _pct(f.get("op_margin")),    _b_pct("op_margin")) +
            _item("Net Margin",   _pct(f.get("net_margin")),   _b_pct("net_margin")) +
            _item("ROE",          _pct(f.get("roe")),          _b_pct("roe")) +
            _item("ROA",          _pct(f.get("roa")),          _b_pct("roa"))
        )
        st.markdown(_card("Profitability", items), unsafe_allow_html=True)

        # Growth & earnings card
        items = (
            _item("EPS Growth",     _pct(f.get("eps_growth")),   _b_pct("eps_growth")) +
            _item("Earn. Surprise", _pct(f.get("surprise_pct"))) +
            _item("FCF Yield",      _pct(f.get("fcf_yield")))
        )
        st.markdown(_card("Growth & Earnings", items), unsafe_allow_html=True)

    # ── Income & short interest (full width) ──────────────────────────────────
    prox_h = f.get("prox_high")
    items = (
        _item("Div Yield",  _pct(f.get("div_yield"))) +
        _item("Payout",     _pct(f.get("payout"))) +
        _item("Short Int.", _pct(f.get("short_pct"))) +
        _item("52wH Prox.", f"{prox_h*100:.1f}% below" if prox_h is not None else "—") +
        _item("52wL Prox.", f"{f['prox_low']*100:.1f}% above" if f.get("prox_low") is not None else "—")
    )
    st.markdown(_card("Income & Short Interest", items), unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Single-ticker full detail (search + heatmap click)
# ──────────────────────────────────────────────────────────────────────────────

def render_single_ticker(ticker: str) -> None:
    ticker = ticker.upper().strip()
    f = fetch_fundamentals(ticker)
    if f.get("error") and not f.get("name"):
        st.error(f"Could not load data for **{ticker}**: {f['error']}")
        return
    name  = f.get("name", ticker)
    p     = fetch_price_batch((ticker,)).get(ticker, {})
    price = p.get("price")
    chg   = p.get("daily_change")

    # ── Hero header ───────────────────────────────────────────────────────────
    chg_class = "t-pos" if (chg or 0) >= 0 else "t-neg"
    price_str = f"${price:,.2f}" if price is not None else "—"
    chg_str   = f"{chg:+.2f}%" if chg is not None else ""
    st.markdown(f"""
    <div class="t-hero">
      <div class="t-hero-top">
        <div>
          <div class="t-sym">{ticker}</div>
          <div class="t-name">{name}</div>
        </div>
        <div style="text-align:right">
          <span class="t-price">{price_str}</span>
          <span class="t-chg {chg_class}">{chg_str}</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Quick stats strip ─────────────────────────────────────────────────────
    mc  = f.get("mktcap")
    rsi = p.get("rsi")
    chg_1m = p.get("chg_1m")
    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("Sector",    f.get("sector") or "—")
    q2.metric("Mkt Cap",   f"${mc/1e9:.1f}B" if mc else "—")
    q3.metric("P/E",       f"{f['pe']:.1f}"  if f.get("pe") else "—")
    q4.metric("RSI (14d)", f"{rsi:.1f}"      if rsi else "—")
    q5.metric("1-Month",   f"{chg_1m:+.1f}%" if chg_1m is not None else "—",
              delta=f"{chg_1m:+.2f}%" if chg_1m is not None else None)

    render_financial_ratios(f, f.get("sector"))
    tab_chart, tab_analyst = st.tabs(["📈 Price Chart", "🔎 Analyst & News"])
    with tab_chart:
        render_price_chart(ticker, name)
    with tab_analyst:
        render_analyst(ticker)


# ──────────────────────────────────────────────────────────────────────────────
# Price chart (2y download → 1y display so MA200 is fully populated)
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False, ttl=300)
def fetch_chart_data(ticker: str, chart_period: str = "1Y") -> pd.DataFrame | None:
    # (yf_period, interval, add_moving_averages)
    _CFG = {
        "1D":  ("1d",  "2m",  False),
        "1W":  ("5d",  "1h",  False),
        "1M":  ("1mo", "1d",  True),
        "3M":  ("3mo", "1d",  True),
        "YTD": ("ytd", "1d",  True),
        "1Y":  ("2y",  "1d",  True),   # download 2y to ensure MA200 is fully populated
        "3Y":  ("3y",  "1d",  True),
    }
    yf_period, interval, show_ma = _CFG.get(chart_period, ("2y", "1d", True))
    try:
        hist = yf.Ticker(ticker).history(period=yf_period, interval=interval, auto_adjust=True)
        if hist is None or hist.empty:
            return None
        if show_ma:
            hist["MA50"]  = hist["Close"].rolling(50).mean()
            hist["MA200"] = hist["Close"].rolling(200).mean()
            if chart_period == "1Y":
                cutoff = hist.index[-1] - pd.DateOffset(years=1)
                hist = hist[hist.index >= cutoff]
        return hist
    except Exception:
        return None


def render_price_chart(ticker: str, name: str) -> None:
    ctrl_l, ctrl_r = st.columns([3, 2])
    with ctrl_l:
        chart_period = st.radio(
            "Period", ["1D", "1W", "1M", "3M", "YTD", "1Y", "3Y"],
            index=5, horizontal=True, key=f"chart_period_{ticker}",
            label_visibility="collapsed",
        )
    with ctrl_r:
        chart_type = st.radio(
            "Chart type", ["Candlestick", "Line", "OHLC Bar"],
            horizontal=True, key=f"chart_type_{ticker}",
        )

    hist = fetch_chart_data(ticker, chart_period)
    if hist is None or hist.empty:
        st.warning(f"No price history available for {ticker}.")
        return

    fig = go.Figure()
    kw = dict(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"], name=ticker,
        increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
    )
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(**kw))
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=hist.index, y=hist["Close"], mode="lines", name="Close",
                                 line=dict(color="#2196F3", width=1.5)))
    else:
        fig.add_trace(go.Ohlc(**kw))
    if "MA50" in hist.columns and hist["MA50"].notna().any():
        fig.add_trace(go.Scatter(x=hist.index, y=hist["MA50"], mode="lines", name="50d MA",
                                 line=dict(color="#FF9800", width=1.5, dash="dot")))
    if "MA200" in hist.columns and hist["MA200"].notna().any():
        fig.add_trace(go.Scatter(x=hist.index, y=hist["MA200"], mode="lines", name="200d MA",
                                 line=dict(color="#CE93D8", width=1.5, dash="dash")))
    fig.update_layout(
        title=f"{ticker} — {name} · {chart_period}",
        xaxis_title=None, yaxis_title="Price ($)", height=450,
        xaxis_rangeslider_visible=False, template="plotly_dark",
        margin=dict(t=50, l=60, r=20, b=40),
        legend=dict(orientation="h", y=1.08),
    )
    st.plotly_chart(fig, use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────
# Commodity heatmap
# ──────────────────────────────────────────────────────────────────────────────

def render_commodity_heatmap(df: pd.DataFrame, period_col: str) -> str | None:
    if df.empty:
        st.warning("No commodity data available.")
        return None
    plot_df = df.copy()
    plot_df["_size"] = 1  # equal-sized tiles
    plot_df["_chg_fmt"] = plot_df[period_col].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A"
    )
    plot_df["_price_fmt"] = plot_df.apply(
        lambda r: f"{r['Price']:.2f} {r['Unit']}" if pd.notna(r.get("Price")) else "—", axis=1
    )
    fig = px.treemap(
        plot_df, path=["Category", "Name"], values="_size",
        color=period_col, color_continuous_scale=_HEATMAP_SCALE,
        color_continuous_midpoint=0, range_color=[-3, 3],
        custom_data=["_chg_fmt", "_price_fmt"],
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textposition="middle center",
        hovertemplate="<b>%{label}</b><br>Change: %{customdata[0]}<br>Price: %{customdata[1]}<extra></extra>",
    )
    fig.update_layout(
        height=380, margin=dict(t=30, l=5, r=5, b=5),
        coloraxis_showscale=False, template="plotly_dark",
    )
    known = set(df["Name"].tolist())
    event = st.plotly_chart(fig, use_container_width=True, key="commodity_heatmap", on_select="rerun")
    if event and event.selection:
        for pt in event.selection.get("points", []):
            label = pt.get("label", "")
            if label in known:
                return label
    return None


# ──────────────────────────────────────────────────────────────────────────────
# Crypto heatmap
# ──────────────────────────────────────────────────────────────────────────────

def render_crypto_heatmap(df: pd.DataFrame, period_col: str) -> str | None:
    if df.empty:
        st.warning("No crypto data available.")
        return None
    plot_df = df.copy()
    plot_df["_size"] = plot_df["Market Cap"].fillna(1e9).clip(lower=1e6)
    plot_df["_chg_fmt"] = plot_df[period_col].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A"
    )
    fig = px.treemap(
        plot_df, path=["Name"], values="_size",
        color=period_col, color_continuous_scale=_HEATMAP_SCALE,
        color_continuous_midpoint=0, range_color=[-5, 5],
        custom_data=["_chg_fmt", "Ticker"],
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textposition="middle center",
        hovertemplate="<b>%{label}</b> (%{customdata[1]})<br>Change: %{customdata[0]}<extra></extra>",
    )
    fig.update_layout(
        height=380, margin=dict(t=30, l=5, r=5, b=5),
        coloraxis_showscale=False, template="plotly_dark",
    )
    known = set(df["Name"].tolist())
    event = st.plotly_chart(fig, use_container_width=True, key="crypto_heatmap", on_select="rerun")
    if event and event.selection:
        for pt in event.selection.get("points", []):
            label = pt.get("label", "")
            if label in known:
                return label
    return None


# ──────────────────────────────────────────────────────────────────────────────
# ETF heatmap + page
# ──────────────────────────────────────────────────────────────────────────────

def render_etf_heatmap(df: pd.DataFrame, period_col: str) -> str | None:
    if df.empty:
        st.warning("No ETF data available.")
        return None
    plot_df = df.copy()
    plot_df["_size"] = 1  # equal-sized tiles within each category
    plot_df["_chg_fmt"] = plot_df[period_col].apply(
        lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A"
    )
    fig = px.treemap(
        plot_df, path=["Category", "Ticker"], values="_size",
        color=period_col, color_continuous_scale=_HEATMAP_SCALE,
        color_continuous_midpoint=0, range_color=[-3, 3],
        custom_data=["_chg_fmt", "Name"],
    )
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{customdata[0]}",
        textposition="middle center", textfont_size=11,
        hovertemplate=(
            "<b>%{label}</b> · %{customdata[1]}<br>"
            "Change: %{customdata[0]}<extra></extra>"
        ),
    )
    fig.update_layout(
        height=440, margin=dict(t=30, l=5, r=5, b=5),
        coloraxis_showscale=False, template="plotly_dark",
    )
    known = set(df["Ticker"].tolist())
    event = st.plotly_chart(fig, use_container_width=True, key="etf_heatmap", on_select="rerun")
    if event and event.selection:
        for pt in event.selection.get("points", []):
            label = pt.get("label", "")
            if label in known:
                return label
    return None


_ETF_PERIOD = {
    "1 Day": "Change %", "1 Week": "Chg 1W",
    "1 Month": "Chg 1M", "3 Months": "Chg 3M", "YTD": "Chg YTD",
}


def render_etf_page() -> None:
    st.title("📊 ETFs")
    st.caption("Curated ETF watchlist across major categories · Data via Yahoo Finance · For research only.")

    # ── Ticker search ─────────────────────────────────────────────────────────
    with st.container(border=True):
        sc, clr = st.columns([5, 1])
        with sc:
            etf_search_raw = st.text_input(
                "Search any ETF ticker",
                placeholder="Type any ETF ticker not in the list below (e.g. SCHD, VIG, JEPI…)",
                key="etf_search",
                label_visibility="collapsed",
            )
        with clr:
            st.write(" ")
            if st.button("Clear", key="etf_search_clear", use_container_width=True):
                st.session_state.pop("etf_search", None)
                st.rerun()

    if etf_search_raw and etf_search_raw.strip():
        with st.container(border=True):
            render_single_ticker(etf_search_raw.strip().upper())
        st.divider()

    # ── Load data ─────────────────────────────────────────────────────────────
    if not st.session_state.get("_etf_loaded"):
        _skeleton(6, 72)
    with st.spinner("Loading ETF data…"):
        df = fetch_etf_data()
    st.session_state["_etf_loaded"] = True

    if df.empty:
        st.error("ETF data unavailable — Yahoo Finance may be throttling. Refresh in a moment.")
        return

    period = st.radio("Period", list(_ETF_PERIOD.keys()), horizontal=True, key="etf_period")
    period_col = _ETF_PERIOD[period]

    # ── Heatmap ───────────────────────────────────────────────────────────────
    with st.expander("🗺 ETF Performance Heatmap", expanded=True):
        st.caption(
            "Click a category label to zoom in · click a tile to open its detail panel below"
        )
        clicked = render_etf_heatmap(df, period_col)
        if clicked:
            st.session_state["etf_selected"] = clicked

    # ── Full table ─────────────────────────────────────────────────────────────
    with st.expander("📋 All ETFs", expanded=True):
        st.caption("Click a row to open the full ETF detail panel below.")
        tbl = (
            df.sort_values(["Category", period_col], ascending=[True, False])
            .reset_index(drop=True)
        )
        etf_event = st.dataframe(
            tbl, use_container_width=True, hide_index=True,
            on_select="rerun", selection_mode="single-row", key="etf_table",
            column_config={
                "Price":    st.column_config.NumberColumn(format="$%.2f"),
                "Change %": st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 1W":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 1M":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 3M":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg YTD":  st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
        etf_sel_rows = (etf_event.selection or {}).get("rows", [])
        if etf_sel_rows and etf_sel_rows[0] < len(tbl):
            st.session_state["etf_selected"] = str(tbl.iloc[etf_sel_rows[0]]["Ticker"])

    # ── Detail panel ──────────────────────────────────────────────────────────
    etf_sel = st.session_state.get("etf_selected")
    if etf_sel:
        st.divider()
        hdr_c, clr_c = st.columns([6, 1])
        hdr_c.markdown(f"**Profile: {etf_sel} — {_ETF_NAMES.get(etf_sel, etf_sel)}**")
        with clr_c:
            if st.button("✕ Close", key="close_etf"):
                st.session_state.pop("etf_selected", None)
                st.rerun()
        with st.container(border=True):
            render_single_ticker(etf_sel)


# ──────────────────────────────────────────────────────────────────────────────
# Commodities page
# ──────────────────────────────────────────────────────────────────────────────

_COM_PERIOD = {"1 Day": "Change %", "1 Week": "Chg 1W", "1 Month": "Chg 1M", "3 Months": "Chg 3M", "YTD": "Chg YTD"}


def render_commodities_page() -> None:
    st.title("🛢 Commodities")
    st.caption("Major commodity futures · Data via Yahoo Finance · For research only.")

    if not st.session_state.get("_com_loaded"):
        _skeleton(5, 72)
    with st.spinner("Loading commodity data…"):
        df = fetch_commodity_data()
    st.session_state["_com_loaded"] = True

    if df.empty:
        st.error("Commodity data unavailable — Yahoo Finance may be throttling. Refresh in a moment.")
        return

    period = st.radio("Period", list(_COM_PERIOD.keys()), horizontal=True, key="com_period")
    period_col = _COM_PERIOD[period]

    # ── Heatmap ───────────────────────────────────────────────────────────────
    with st.expander("🗺 Commodity Performance Heatmap", expanded=True):
        st.caption("Click a category to zoom in · click a tile to view its price chart below")
        clicked = render_commodity_heatmap(df, period_col)
        if clicked:
            st.session_state["com_selected"] = clicked

    # ── Full table ─────────────────────────────────────────────────────────────
    with st.expander("📋 All Commodities", expanded=True):
        st.caption("Click a row to view its price chart below.")
        tbl = (
            df[["Name", "Category", "Price", "Unit", "Change %", "Chg 1W", "Chg 1M", "Chg 3M", "Chg YTD"]]
            .sort_values(period_col, ascending=False)
            .reset_index(drop=True)
        )
        com_event = st.dataframe(
            tbl, use_container_width=True, hide_index=True,
            on_select="rerun", selection_mode="single-row", key="com_table",
            column_config={
                "Price":    st.column_config.NumberColumn(format="%.2f"),
                "Change %": st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 1W":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 1M":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 3M":   st.column_config.NumberColumn(format="%.2f%%"),
                "Chg YTD":  st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
        c_rows = (com_event.selection or {}).get("rows", [])
        if c_rows and c_rows[0] < len(tbl):
            st.session_state["com_selected"] = tbl.iloc[c_rows[0]]["Name"]

    # ── Detail panel ──────────────────────────────────────────────────────────
    com_sel = st.session_state.get("com_selected")
    if com_sel and len(df) > 0 and com_sel in df["Name"].values:
        row = df[df["Name"] == com_sel].iloc[0]
        ticker = row["Ticker"]
        st.divider()
        with st.container(border=True):
            hdr, close_btn = st.columns([6, 1])
            hdr.markdown(f"### {com_sel}")
            with close_btn:
                if st.button("✕ Close", key="close_com"):
                    st.session_state.pop("com_selected", None)
                    st.rerun()
            s1, s2, s3, s4, s5 = st.columns(5)
            price = row.get("Price")
            chg   = row.get("Change %")
            s1.metric("Price", f"{price:.2f} {row.get('Unit', '')}" if price else "—",
                      delta=f"{chg:+.2f}%" if chg is not None else None)
            s2.metric("Category", row.get("Category", "—"))
            s3.metric("1-Week",  f"{row.get('Chg 1W', 0):+.2f}%" if row.get("Chg 1W") is not None else "—")
            s4.metric("1-Month", f"{row.get('Chg 1M', 0):+.2f}%" if row.get("Chg 1M") is not None else "—")
            s5.metric("YTD",     f"{row.get('Chg YTD', 0):+.2f}%" if row.get("Chg YTD") is not None else "—")
            render_price_chart(ticker, com_sel)


# ──────────────────────────────────────────────────────────────────────────────
# Crypto page
# ──────────────────────────────────────────────────────────────────────────────

_CRYPTO_PERIOD = {"1 Day": "Change %", "1 Week": "Chg 1W", "1 Month": "Chg 1M", "3 Months": "Chg 3M", "YTD": "Chg YTD"}


def render_crypto_page() -> None:
    st.title("₿ Crypto")
    st.caption("Major cryptocurrencies · Data via Yahoo Finance · For research only.")

    if not st.session_state.get("_crypto_loaded"):
        _skeleton(4, 72)
    with st.spinner("Loading crypto data…"):
        df = fetch_crypto_data()
    st.session_state["_crypto_loaded"] = True

    if df.empty:
        st.error("Crypto data unavailable — Yahoo Finance may be throttling. Refresh in a moment.")
        return

    period = st.radio("Period", list(_CRYPTO_PERIOD.keys()), horizontal=True, key="crypto_period")
    period_col = _CRYPTO_PERIOD[period]

    # ── Heatmap ───────────────────────────────────────────────────────────────
    with st.expander("🗺 Crypto Performance Heatmap", expanded=True):
        st.caption("Sized by market cap · colored ±5% · click a tile to view its price chart below")
        clicked = render_crypto_heatmap(df, period_col)
        if clicked:
            st.session_state["crypto_selected"] = clicked

    # ── Biggest Movers ────────────────────────────────────────────────────────
    with st.expander("📈 Biggest Movers", expanded=True):
        sorted_df = df.dropna(subset=[period_col]).sort_values(period_col, ascending=False).reset_index(drop=True)
        if sorted_df.empty:
            st.caption("No data available.")
        else:
            gainers = sorted_df[sorted_df[period_col] >= 0].reset_index(drop=True)
            losers  = sorted_df[sorted_df[period_col] < 0].sort_values(period_col).reset_index(drop=True)
            col_g, col_l = st.columns(2)
            mv_cfg = {
                "Price":    st.column_config.NumberColumn(format="$%.4f"),
                period_col: st.column_config.NumberColumn(format="%.2f%%"),
            }
            with col_g:
                st.markdown("**🟢 Gainers** · click a row to view chart")
                g_ev = st.dataframe(
                    gainers[["Name", "Ticker", "Price", period_col]], use_container_width=True,
                    hide_index=True, column_config=mv_cfg,
                    on_select="rerun", selection_mode="single-row", key="crypto_gainers",
                )
            with col_l:
                st.markdown("**🔴 Losers** · click a row to view chart")
                l_ev = st.dataframe(
                    losers[["Name", "Ticker", "Price", period_col]], use_container_width=True,
                    hide_index=True, column_config=mv_cfg,
                    on_select="rerun", selection_mode="single-row", key="crypto_losers",
                )
            g_rows = (g_ev.selection or {}).get("rows", [])
            l_rows = (l_ev.selection or {}).get("rows", [])
            if g_rows and g_rows[0] < len(gainers):
                st.session_state["crypto_selected"] = gainers.iloc[g_rows[0]]["Name"]
            elif l_rows and l_rows[0] < len(losers):
                st.session_state["crypto_selected"] = losers.iloc[l_rows[0]]["Name"]

    # ── Full table ─────────────────────────────────────────────────────────────
    with st.expander("📋 All Cryptocurrencies", expanded=True):
        st.caption("Click a row to view its price chart below.")
        avail = [c for c in ["Name", "Ticker", "Price", "Change %", "Market Cap", "24h Vol",
                              "Chg 1W", "Chg 1M", "Chg 3M", "Chg YTD"] if c in df.columns]
        tbl = df[avail].sort_values(period_col if period_col in avail else "Change %",
                                    ascending=False).reset_index(drop=True)
        crypto_event = st.dataframe(
            tbl, use_container_width=True, hide_index=True,
            on_select="rerun", selection_mode="single-row", key="crypto_table",
            column_config={
                "Price":      st.column_config.NumberColumn(format="$%.4f"),
                "Change %":   st.column_config.NumberColumn(format="%.2f%%"),
                "Market Cap": st.column_config.NumberColumn(format="compact"),
                "24h Vol":    st.column_config.NumberColumn(format="compact"),
                "Chg 1W":     st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 1M":     st.column_config.NumberColumn(format="%.2f%%"),
                "Chg 3M":     st.column_config.NumberColumn(format="%.2f%%"),
                "Chg YTD":    st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
        ct_rows = (crypto_event.selection or {}).get("rows", [])
        if ct_rows and ct_rows[0] < len(tbl):
            st.session_state["crypto_selected"] = tbl.iloc[ct_rows[0]]["Name"]

    # ── Crypto-Related ETFs ───────────────────────────────────────────────────
    with st.expander("🏦 Crypto-Related ETFs", expanded=True):
        st.caption("Bitcoin & Ethereum spot ETFs · click a row to open full detail panel")
        etf_tickers = tuple(_CRYPTO_ETFS.keys())
        etf_prices  = fetch_price_batch(etf_tickers)
        etf_rows = []
        for sym, full_name in _CRYPTO_ETFS.items():
            p = etf_prices.get(sym, {})
            etf_rows.append({
                "Ticker":     sym,
                "Name":       full_name,
                "Price":      p.get("price"),
                "Change %":   p.get("daily_change"),
                "1W %":       p.get("chg_1w"),
                "1M %":       p.get("chg_1m"),
                "3M %":       p.get("chg_3m"),
                "YTD %":      p.get("chg_ytd"),
            })
        etf_df = pd.DataFrame(etf_rows)
        etf_event = st.dataframe(
            etf_df, use_container_width=True, hide_index=True,
            on_select="rerun", selection_mode="single-row", key="crypto_etf_table",
            column_config={
                "Price":    st.column_config.NumberColumn(format="$%.2f"),
                "Change %": st.column_config.NumberColumn(format="%.2f%%"),
                "1W %":     st.column_config.NumberColumn(format="%.2f%%"),
                "1M %":     st.column_config.NumberColumn(format="%.2f%%"),
                "3M %":     st.column_config.NumberColumn(format="%.2f%%"),
                "YTD %":    st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
        etf_rows_sel = (etf_event.selection or {}).get("rows", [])
        if etf_rows_sel and etf_rows_sel[0] < len(etf_df):
            st.session_state["crypto_etf_selected"] = str(etf_df.iloc[etf_rows_sel[0]]["Ticker"])

    etf_sel = st.session_state.get("crypto_etf_selected")
    if etf_sel:
        st.divider()
        etf_hdr, etf_clr = st.columns([6, 1])
        etf_hdr.markdown(f"**ETF Profile: {etf_sel} — {_CRYPTO_ETFS.get(etf_sel, '')}**")
        with etf_clr:
            if st.button("✕ Close", key="close_crypto_etf"):
                st.session_state.pop("crypto_etf_selected", None)
                st.rerun()
        with st.container(border=True):
            render_single_ticker(etf_sel)

    # ── Detail panel ──────────────────────────────────────────────────────────
    crypto_sel = st.session_state.get("crypto_selected")
    if crypto_sel and len(df) > 0 and crypto_sel in df["Name"].values:
        row = df[df["Name"] == crypto_sel].iloc[0]
        ticker = row["Ticker"]
        st.divider()
        with st.container(border=True):
            hdr, close_btn = st.columns([6, 1])
            hdr.markdown(f"### {crypto_sel}  `{ticker}`")
            with close_btn:
                if st.button("✕ Close", key="close_crypto"):
                    st.session_state.pop("crypto_selected", None)
                    st.rerun()
            s1, s2, s3, s4, s5 = st.columns(5)
            price = row.get("Price")
            chg   = row.get("Change %")
            mc    = row.get("Market Cap")
            vol   = row.get("24h Vol")
            s1.metric("Price",    f"${price:,.4f}" if price else "—",
                      delta=f"{chg:+.2f}%" if chg is not None else None)
            s2.metric("Market Cap", f"${mc/1e9:.2f}B" if mc else "—")
            s3.metric("24h Vol",    f"${vol/1e9:.2f}B" if vol else "—")
            s4.metric("1-Month",  f"{row.get('Chg 1M', 0):+.2f}%" if row.get("Chg 1M") is not None else "—")
            s5.metric("YTD",      f"{row.get('Chg YTD', 0):+.2f}%" if row.get("Chg YTD") is not None else "—")
            render_price_chart(ticker, crypto_sel)


# ──────────────────────────────────────────────────────────────────────────────
# Universe loader
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading index constituents…", ttl=60 * 60 * 12)
def load_indexes(indexes: tuple[str, ...]):
    return universe.build_universe(list(indexes))


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def render_equities_page() -> None:
    st.caption(
        "Real-time screening across major US indexes · Data via Yahoo Finance · For research only."
    )

    # ── 1. Single-ticker search ───────────────────────────────────────────────
    search_col, clear_col = st.columns([5, 1])
    ticker_input = search_col.text_input(
        "🔍 Quick ticker lookup",
        placeholder="Type a ticker (e.g. AAPL) to view its full profile — bypasses the screener",
        key="ticker_search", label_visibility="collapsed",
    ).strip().upper()

    if ticker_input:
        with clear_col:
            st.write(" ")
            if st.button("✕ Clear", key="clear_search"):
                st.session_state.pop("ticker_search", None)
                st.rerun()
        with st.container(border=True):
            render_single_ticker(ticker_input)
        st.divider()

    # ── 2. Screen Setup card ──────────────────────────────────────────────────
    with st.container(border=True):

        r1a, r1b, r1c = st.columns([1, 2, 1])

        with r1a:
            st.markdown("**Sector**")
            sector_list = st.multiselect(
                "Sector", _ALL_SECTORS, default=[], key="sector_filter",
                placeholder="All sectors", label_visibility="collapsed",
            )
            st.caption(f"Filtering: {', '.join(sector_list)}" if sector_list else "All sectors.")

        with r1b:
            st.markdown("**Universe**")
            selected: list[str] = []
            for group, members in INDEX_GROUPS.items():
                enabled = st.checkbox(group, value=(group == "Large Cap"), key=f"grp_{group}")
                if enabled:
                    picked = st.multiselect(
                        group, members, default=members,
                        key=f"idx_{group}", label_visibility="collapsed",
                    )
                    selected.extend(picked)
            tickers: set[str] = set()
            if selected:
                names, counts, errors = load_indexes(tuple(sorted(selected)))
                tickers.update(names)
                if counts:
                    st.caption("Loaded: " + ", ".join(f"{k} ({v})" for k, v in counts.items()))
                for idx, msg in errors.items():
                    st.warning(f"**{idx}**: {msg}")
            with st.expander("Extra tickers (optional)", expanded=False):
                extra = st.text_area("", value="", height=55,
                                     label_visibility="collapsed", key="extra_tickers")
                for t in extra.replace("\n", ",").replace(" ", ",").split(","):
                    norm = universe._normalise(t)
                    if norm:
                        tickers.add(norm)
            tickers_list = sorted(tickers)

        with r1c:
            st.markdown("**Market Cap**")
            use_mktcap = st.checkbox("Filter by range", value=False, key="use_mktcap")
            mc_c1, mc_c2 = st.columns(2)
            mc_min_b = mc_c1.number_input("Min ($B)", min_value=0.0, value=5.0, step=0.5,
                                           key="mc_min_b")
            mc_max_b = mc_c2.number_input("Max ($B)", min_value=0.0, value=0.0, step=0.5,
                                           key="mc_max_b", help="0 = no upper limit")
            if use_mktcap:
                st.caption(f"≥ ${mc_min_b:g}B" +
                           (f" ≤ ${mc_max_b:g}B" if mc_max_b > 0 else " (no max)"))

        r2a, r2b, r2c = st.columns([1, 2, 1])

        with r2a:
            st.markdown("**Trend**")
            use_ma50  = st.checkbox("Above 50-day MA",  value=True, key="use_ma50")
            use_ma200 = st.checkbox("Above 200-day MA", value=True, key="use_ma200")
            tc1, ts1 = st.columns([1, 2])
            use_52h   = tc1.checkbox("≤ X% of 52wH", value=False, key="use_52h",
                                     help="Within X% below 52-week high (proximity)")
            max_52h_pct = ts1.slider("52wH %", 0, 50, 10, step=1, key="max_52h_pct",
                                     label_visibility="collapsed",
                                     help="Price is at most this % below its 52-week high")
            tc2, ts2 = st.columns([1, 2])
            use_52l   = tc2.checkbox("≥ X% of 52wL", value=False, key="use_52l",
                                     help="Within X% above 52-week low (proximity)")
            max_52l_pct = ts2.slider("52wL %", 0, 50, 10, step=1, key="max_52l_pct",
                                     label_visibility="collapsed",
                                     help="Price is at most this % above its 52-week low")

        with r2b:
            st.markdown("**Momentum & Growth**")
            cb1, sl1 = st.columns([1, 2])
            use_rsi    = cb1.checkbox("RSI ≥",       value=False, key="use_rsi")
            min_rsi    = sl1.slider("RSI",  1, 99, 50, step=1,  key="min_rsi",
                                    label_visibility="collapsed")
            cb2, sl2 = st.columns([1, 2])
            use_growth = cb2.checkbox("Rev growth ≥", value=True, key="use_growth")
            min_growth = sl2.slider("Growth %", 0, 100, 20, step=5, key="min_growth",
                                    label_visibility="collapsed") / 100.0
            cb3, sl3 = st.columns([1, 2])
            use_eps_growth = cb3.checkbox("EPS growth ≥", value=False, key="use_eps_growth")
            min_eps_growth = sl3.slider("EPS %", -100, 200, 10, step=5, key="min_eps_growth",
                                        label_visibility="collapsed",
                                        help="YoY quarterly EPS growth threshold (%)") / 100.0
            cb4, sl4 = st.columns([1, 2])
            use_surprise = cb4.checkbox("Earn. surprise ≥", value=False, key="use_surprise")
            min_surprise = sl4.slider("Surprise %", -50, 50, 0, step=1, key="min_surprise",
                                      label_visibility="collapsed",
                                      help="Last-quarter EPS actual vs. estimate (%)") / 100.0
            cb5, sl5 = st.columns([1, 2])
            use_rel_str = cb5.checkbox("RS vs SPY ≥", value=False, key="use_rel_str",
                                       help="1-year return minus SPY 1-year return (ppt)")
            min_rel_str = sl5.slider("RS ppt", -50, 100, 0, step=1, key="min_rel_str",
                                     label_visibility="collapsed",
                                     help="Stock 1Y return minus SPY 1Y return (percentage points)")

        with r2c:
            st.markdown("**Valuation**")
            vc1, vs1 = st.columns([1, 2])
            use_pe = vc1.checkbox("P/E ≤", value=True, key="use_pe")
            max_pe = vs1.slider("P/E", 1, 100, 30, step=1, key="max_pe",
                                label_visibility="collapsed")
            vc2, vs2 = st.columns([1, 2])
            use_fwd_pe = vc2.checkbox("Fwd P/E ≤", value=False, key="use_fwd_pe")
            max_fwd_pe = vs2.slider("Fwd P/E", 1, 100, 25, step=1, key="max_fwd_pe",
                                    label_visibility="collapsed",
                                    help="Forward P/E (consensus next-12-month estimate)")
            vc3, vs3 = st.columns([1, 2])
            use_peg = vc3.checkbox("PEG ≤", value=False, key="use_peg")
            max_peg = vs3.slider("PEG", 0.1, 10.0, 2.0, step=0.1, key="max_peg",
                                 label_visibility="collapsed",
                                 help="PEG Ratio — P/E divided by EPS growth rate")
            vc4, vs4 = st.columns([1, 2])
            use_ps = vc4.checkbox("P/S ≤", value=False, key="use_ps")
            max_ps = vs4.slider("P/S", 0.1, 50.0, 5.0, step=0.5, key="max_ps",
                                label_visibility="collapsed",
                                help="Price-to-Sales (trailing 12 months)")
            vc5, vs5 = st.columns([1, 2])
            use_fcf_yield = vc5.checkbox("FCF yield ≥", value=False, key="use_fcf_yield",
                                         help="Free Cash Flow yield (FCF / Market Cap)")
            min_fcf_yield = vs5.slider("FCF %", 0, 20, 3, step=1, key="min_fcf_yield",
                                       label_visibility="collapsed") / 100.0
            vc6, vs6 = st.columns([1, 2])
            use_short = vc6.checkbox("Short int.", value=False, key="use_short",
                                     help="Short interest as % of float (range)")
            short_range = vs6.slider("Short %", 0, 100, (0, 25), step=1, key="short_range",
                                     label_visibility="collapsed")
            vc7, vs7 = st.columns([1, 2])
            use_div = vc7.checkbox("Div yield ≥", value=False, key="use_div",
                                   help="Annual dividend yield (%)")
            min_div = vs7.slider("Div %", 0, 15, 1, step=1, key="min_div",
                                 label_visibility="collapsed") / 100.0
            vc8, vs8 = st.columns([1, 2])
            use_payout = vc8.checkbox("Payout ≤", value=False, key="use_payout",
                                      help="Dividend payout ratio (%)")
            max_payout = vs8.slider("Payout %", 0, 200, 75, step=5, key="max_payout",
                                    label_visibility="collapsed") / 100.0

        st.divider()
        rc1, rc2, rc3, rc4 = st.columns([3, 2, 1, 1])
        ticker_count  = len(tickers_list)
        sector_filter = set(sector_list)
        with rc1:
            sn = f" · {len(sector_filter)} sector(s)" if sector_filter else ""
            st.write(f"**{ticker_count} tickers** in universe{sn}.")
        cap = rc2.number_input(
            "Max tickers to screen", min_value=10, max_value=5000,
            value=min(500, max(10, ticker_count)) if ticker_count else 500,
            step=50, key="cap",
            help="Yahoo rate-limits heavy use — raise to screen more tickers.",
        )
        with rc3:
            st.write(" ")
            run = st.button("▶ Run screen", type="primary", use_container_width=True)
        with rc4:
            st.write(" ")
            st.button("↺ Reset", on_click=_reset_all, use_container_width=True)

    if ticker_count > cap:
        st.warning(
            f"Screening first {int(cap)} of {ticker_count} tickers. "
            "Raise *Max tickers to screen* to cover more."
        )
    if run and not tickers_list:
        st.warning("No tickers selected — enable at least one index group.")

    st.divider()

    # ── 3. Market Overview heatmap ────────────────────────────────────────────
    hmap_click = None
    with st.expander("📊 Market Overview — S&P 500", expanded=True):
        st.caption(
            "Individual stocks sized by market cap · grouped by sector · colored by daily % change "
            "· **click a sector label to zoom in · click a stock tile to open its profile**"
        )
        hmap_click = render_market_heatmap(sector_filter)
    if hmap_click:
        st.session_state["heatmap_ticker"] = hmap_click

    hmap_ticker = st.session_state.get("heatmap_ticker")
    if hmap_ticker:
        hd_col, hd_clr = st.columns([6, 1])
        hd_col.markdown(f"**Profile: {hmap_ticker}**")
        with hd_clr:
            if st.button("✕ Close", key="close_hmap"):
                st.session_state.pop("heatmap_ticker", None)
                st.rerun()
        with st.container(border=True):
            render_single_ticker(hmap_ticker)

    st.divider()

    # ── 4. Biggest Movers ─────────────────────────────────────────────────────
    movers_ticker = None
    with st.expander("📈 Biggest Movers — S&P 500", expanded=True):
        movers_ticker = render_biggest_movers(sector_filter)

    if movers_ticker:
        with st.container(border=True):
            st.caption(f"Click another row or close the panel below to dismiss.")
            render_single_ticker(movers_ticker)

    st.divider()

    # ── 5. Screener run logic ─────────────────────────────────────────────────
    if run and tickers_list:
        screen = tickers_list[: int(cap)]
        prices = fetch_prices(screen)

        spy_1y = fetch_benchmark_returns().get("chg_1y") if use_rel_str else None

        def above(p, ma):
            return p is not None and ma is not None and p > ma

        candidates = []
        for t in screen:
            d = prices.get(t)
            if d is None:
                continue
            if use_ma50  and not above(d["price"], d["ma50"]):
                continue
            if use_ma200 and not above(d["price"], d["ma200"]):
                continue
            if use_rsi   and (d.get("rsi") is None or d["rsi"] < min_rsi):
                continue
            candidates.append(t)

        funda = fetch_fundamentals_many(candidates)

        mc_lo = mc_min_b * 1e9
        mc_hi = float("inf") if mc_max_b <= 0 else mc_max_b * 1e9
        if mc_hi < mc_lo:
            mc_lo, mc_hi = mc_hi, mc_lo

        rows = []
        for t in candidates:
            d = prices[t]
            f = funda.get(t, {})
            pe         = f.get("pe")
            fwd_pe     = f.get("fwd_pe")
            peg        = f.get("peg")
            ps         = f.get("ps")
            eps_growth = f.get("eps_growth")
            surprise   = f.get("surprise_pct")
            rev        = f.get("rev")
            mc         = f.get("mktcap")
            sector     = f.get("sector")
            prox_high  = f.get("prox_high")
            prox_low   = f.get("prox_low")
            fcf_yield  = f.get("fcf_yield")
            short_pct  = f.get("short_pct")
            div_yield  = f.get("div_yield")
            payout     = f.get("payout")
            stock_1y   = d.get("chg_1y")
            if use_growth     and not (rev        is not None and rev        >= min_growth):
                continue
            if use_eps_growth and not (eps_growth is not None and eps_growth >= min_eps_growth):
                continue
            if use_surprise   and not (surprise   is not None and surprise   >= min_surprise):
                continue
            if use_pe         and not (pe         is not None and pe         <= max_pe):
                continue
            if use_fwd_pe     and not (fwd_pe     is not None and fwd_pe     <= max_fwd_pe):
                continue
            if use_peg        and not (peg        is not None and peg        <= max_peg):
                continue
            if use_ps         and not (ps         is not None and ps         <= max_ps):
                continue
            if use_mktcap     and not (mc         is not None and mc_lo <= mc <= mc_hi):
                continue
            if use_52h and not (prox_high is not None and prox_high * 100 <= max_52h_pct):
                continue
            if use_52l and not (prox_low  is not None and prox_low  * 100 <= max_52l_pct):
                continue
            if use_rel_str and spy_1y is not None:
                if not (stock_1y is not None and (stock_1y - spy_1y) >= min_rel_str):
                    continue
            if use_fcf_yield and not (fcf_yield is not None and fcf_yield >= min_fcf_yield):
                continue
            if use_short and short_pct is not None:
                lo_s, hi_s = short_range[0] / 100.0, short_range[1] / 100.0
                if not (lo_s <= short_pct <= hi_s):
                    continue
            if use_div    and not (div_yield is not None and div_yield >= min_div):
                continue
            if use_payout and not (payout   is not None and payout   <= max_payout):
                continue
            if sector_filter and sector not in sector_filter:
                continue
            vs_spy = round(stock_1y - spy_1y, 2) if (stock_1y is not None and spy_1y is not None) else None
            rows.append({
                "Ticker": t, "Name": f.get("name", t), "Sector": sector,
                "Price": d["price"], "Daily Chg %": d.get("daily_change"),
                "RSI":  d.get("rsi"), "Mkt Cap": mc, "P/E": pe,
                "Fwd P/E":      fwd_pe,
                "PEG":          peg,
                "P/S":          ps,
                "EPS Growth":   eps_growth,
                "Earn. Surpr.": surprise,
                "P/B":          f.get("pb"),
                "D/E":          f.get("de"),
                "Curr. Ratio":  f.get("current_ratio"),
                "Quick Ratio":  f.get("quick_ratio"),
                "Gross Margin": f.get("gross_margin"),
                "Oper. Margin": f.get("op_margin"),
                "Net Margin":   f.get("net_margin"),
                "EV/EBITDA":    f.get("ev_ebitda"),
                "ROE":          f.get("roe"),
                "ROA":          f.get("roa"),
                "Rev Growth":   rev, "50d MA": d["ma50"], "200d MA": d["ma200"],
                "Div Yield":    div_yield,
                "Payout":       payout,
                "FCF Yield":    fcf_yield,
                "Short Int.":   short_pct,
                "vs SPY 1Y":    vs_spy,
                "52wH %":       prox_high,
                "52wL %":       prox_low,
            })

        st.session_state["results"] = {
            "rows": rows, "screened": len(screen),
            "priced": len(prices), "candidates": len(candidates),
        }

    res = st.session_state.get("results")
    if res is None:
        st.info("Configure filters above and click **▶ Run screen** to see results.")
        return

    # ── Results ───────────────────────────────────────────────────────────────
    st.subheader("Screener Results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Screened",      res["screened"])
    c2.metric("Priced",        res["priced"])
    c3.metric("Passed MA/RSI", res["candidates"])
    c4.metric("Final matches", len(res["rows"]))

    if not res["rows"]:
        st.write("No stocks matched all criteria.")
        return

    df = (
        pd.DataFrame(res["rows"])
        .sort_values("Rev Growth", ascending=False, na_position="last")
        .reset_index(drop=True)
    )

    tbl_event = None
    with st.expander("📋 Results Table", expanded=True):
        st.caption("Click a row to open a full stock profile.")
        tbl_event = st.dataframe(
            df, use_container_width=True, hide_index=True,
            on_select="rerun", selection_mode="single-row", key="results_table",
            column_config={
                "Price":        st.column_config.NumberColumn(format="$%.2f"),
                "Daily Chg %":  st.column_config.NumberColumn(format="%.2f%%"),
                "RSI":          st.column_config.NumberColumn(format="%.1f"),
                "Mkt Cap":      st.column_config.NumberColumn(format="compact"),
                "50d MA":       st.column_config.NumberColumn(format="$%.2f"),
                "200d MA":      st.column_config.NumberColumn(format="$%.2f"),
                "P/E":          st.column_config.NumberColumn(format="%.1f"),
                "Fwd P/E":      st.column_config.NumberColumn(format="%.1f"),
                "PEG":          st.column_config.NumberColumn(format="%.2f"),
                "P/S":          st.column_config.NumberColumn(format="%.2f"),
                "EPS Growth":   st.column_config.NumberColumn(format="percent"),
                "Earn. Surpr.": st.column_config.NumberColumn(format="percent"),
                "P/B":          st.column_config.NumberColumn(format="%.2f"),
                "D/E":          st.column_config.NumberColumn(format="%.3f"),
                "Curr. Ratio":  st.column_config.NumberColumn(format="%.2f"),
                "Quick Ratio":  st.column_config.NumberColumn(format="%.2f"),
                "Gross Margin": st.column_config.NumberColumn(format="percent"),
                "Oper. Margin": st.column_config.NumberColumn(format="percent"),
                "Net Margin":   st.column_config.NumberColumn(format="percent"),
                "EV/EBITDA":    st.column_config.NumberColumn(format="%.1f"),
                "ROE":          st.column_config.NumberColumn(format="percent"),
                "ROA":          st.column_config.NumberColumn(format="percent"),
                "Rev Growth":   st.column_config.NumberColumn(format="percent"),
                "Div Yield":    st.column_config.NumberColumn(format="percent"),
                "Payout":       st.column_config.NumberColumn(format="percent"),
                "FCF Yield":    st.column_config.NumberColumn(format="percent"),
                "Short Int.":   st.column_config.NumberColumn(format="percent"),
                "vs SPY 1Y":    st.column_config.NumberColumn(format="%.2f%%",
                                    help="Stock 1Y return minus SPY 1Y return (ppt)"),
                "52wH %":       st.column_config.NumberColumn(format="percent",
                                    help="% below 52-week high"),
                "52wL %":       st.column_config.NumberColumn(format="percent",
                                    help="% above 52-week low"),
            },
        )
        st.download_button(
            "⬇ Download CSV", df.to_csv(index=False).encode(),
            file_name="screener_matches.csv", mime="text/csv",
        )

    heatmap_click = None
    with st.expander("🗺 Screened Results — Sector Heatmap", expanded=True):
        st.caption(
            "Sized by market cap · colored ±3% · "
            "click a sector label to zoom in · click a stock tile to open its profile."
        )
        heatmap_click = render_results_heatmap(df)

    # Determine which stock to show in detail (table row or heatmap tile).
    detail_ticker: str | None = None
    sel_rows = tbl_event.selection["rows"] if tbl_event and tbl_event.selection else []
    if sel_rows and sel_rows[0] < len(df):
        detail_ticker = str(df.iloc[sel_rows[0]]["Ticker"])
    if heatmap_click:
        detail_ticker = heatmap_click  # heatmap click takes precedence when fresh

    if detail_ticker:
        st.divider()
        with st.container(border=True):
            render_single_ticker(detail_ticker)


def main() -> None:
    st.set_page_config(
        page_title="Market Screener", page_icon="📈",
        layout="wide", initial_sidebar_state="collapsed",
    )

    # Default dark mode on first load.
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = True

    _inject_css()

    # ── Top navigation bar ────────────────────────────────────────────────────
    nav_col, toggle_col = st.columns([11, 1])
    with nav_col:
        nav_page = st.radio(
            "Page",
            ["📈 Equities", "🛢 Commodities", "₿ Crypto", "📊 ETFs"],
            horizontal=True,
            key="nav_page",
            label_visibility="collapsed",
        )
    with toggle_col:
        st.toggle(
            "🌙",
            value=st.session_state["dark_mode"],
            key="dark_mode",
            help="Toggle dark / light mode",
        )
    st.divider()

    if nav_page == "📈 Equities":
        st.title("📈 Equities Screener")
        render_equities_page()
    elif nav_page == "🛢 Commodities":
        render_commodities_page()
    elif nav_page == "₿ Crypto":
        render_crypto_page()
    else:
        render_etf_page()


if __name__ == "__main__":
    main()
