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

import math

import networkx as nx
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


# ──────────────────────────────────────────────────────────────────────────────
# Corporate Network page
# ──────────────────────────────────────────────────────────────────────────────

# Curated corporate relationship dataset
_NETWORK_COMPANIES: dict[str, dict] = {
    # Ticker: {name, sector, mktcap_b (billions)}
    "AAPL":  {"name": "Apple",              "sector": "Technology",              "mktcap_b": 3000},
    "MSFT":  {"name": "Microsoft",          "sector": "Technology",              "mktcap_b": 3200},
    "GOOGL": {"name": "Alphabet",           "sector": "Communication Services",  "mktcap_b": 2200},
    "META":  {"name": "Meta Platforms",     "sector": "Communication Services",  "mktcap_b": 1400},
    "AMZN":  {"name": "Amazon",             "sector": "Consumer Cyclical",       "mktcap_b": 1900},
    "NVDA":  {"name": "NVIDIA",             "sector": "Technology",              "mktcap_b": 3000},
    "AMD":   {"name": "Advanced Micro Devices","sector": "Technology",           "mktcap_b": 250},
    "QCOM":  {"name": "Qualcomm",           "sector": "Technology",              "mktcap_b": 170},
    "AVGO":  {"name": "Broadcom",           "sector": "Technology",              "mktcap_b": 600},
    "TSM":   {"name": "TSMC",               "sector": "Technology",              "mktcap_b": 900},
    "SWKS":  {"name": "Skyworks Solutions", "sector": "Technology",              "mktcap_b": 15},
    "INTC":  {"name": "Intel",              "sector": "Technology",              "mktcap_b": 130},
    "CRM":   {"name": "Salesforce",         "sector": "Technology",              "mktcap_b": 280},
    "ORCL":  {"name": "Oracle",             "sector": "Technology",              "mktcap_b": 350},
    "ADBE":  {"name": "Adobe",              "sector": "Technology",              "mktcap_b": 240},
    "TSLA":  {"name": "Tesla",              "sector": "Consumer Cyclical",       "mktcap_b": 700},
    "RIVN":  {"name": "Rivian",             "sector": "Consumer Cyclical",       "mktcap_b": 15},
    "GM":    {"name": "General Motors",     "sector": "Consumer Cyclical",       "mktcap_b": 50},
    "F":     {"name": "Ford Motor",         "sector": "Consumer Cyclical",       "mktcap_b": 50},
    "UBER":  {"name": "Uber Technologies",  "sector": "Technology",              "mktcap_b": 155},
    "SPOT":  {"name": "Spotify",            "sector": "Communication Services",  "mktcap_b": 80},
    "JPM":   {"name": "JPMorgan Chase",     "sector": "Financial Services",      "mktcap_b": 580},
    "BAC":   {"name": "Bank of America",    "sector": "Financial Services",      "mktcap_b": 320},
    "WFC":   {"name": "Wells Fargo",        "sector": "Financial Services",      "mktcap_b": 220},
    "GS":    {"name": "Goldman Sachs",      "sector": "Financial Services",      "mktcap_b": 160},
    "BRK-B": {"name": "Berkshire Hathaway", "sector": "Financial Services",      "mktcap_b": 900},
    "V":     {"name": "Visa",               "sector": "Financial Services",      "mktcap_b": 560},
    "MA":    {"name": "Mastercard",         "sector": "Financial Services",      "mktcap_b": 450},
    "AXP":   {"name": "American Express",   "sector": "Financial Services",      "mktcap_b": 200},
    "PYPL":  {"name": "PayPal",             "sector": "Financial Services",      "mktcap_b": 65},
    "MCO":   {"name": "Moody's",            "sector": "Financial Services",      "mktcap_b": 80},
    "OXY":   {"name": "Occidental Petroleum","sector": "Energy",                 "mktcap_b": 55},
    "XOM":   {"name": "ExxonMobil",         "sector": "Energy",                  "mktcap_b": 490},
    "CVX":   {"name": "Chevron",            "sector": "Energy",                  "mktcap_b": 290},
    "SLB":   {"name": "SLB (Schlumberger)", "sector": "Energy",                  "mktcap_b": 60},
    "HAL":   {"name": "Halliburton",        "sector": "Energy",                  "mktcap_b": 30},
    "JNJ":   {"name": "Johnson & Johnson",  "sector": "Healthcare",              "mktcap_b": 380},
    "PFE":   {"name": "Pfizer",             "sector": "Healthcare",              "mktcap_b": 180},
    "MRK":   {"name": "Merck",              "sector": "Healthcare",              "mktcap_b": 270},
    "LLY":   {"name": "Eli Lilly",          "sector": "Healthcare",              "mktcap_b": 750},
    "ABBV":  {"name": "AbbVie",             "sector": "Healthcare",              "mktcap_b": 300},
    "UNH":   {"name": "UnitedHealth",       "sector": "Healthcare",              "mktcap_b": 490},
    "BNTX":  {"name": "BioNTech",           "sector": "Healthcare",              "mktcap_b": 25},
    "GILD":  {"name": "Gilead Sciences",    "sector": "Healthcare",              "mktcap_b": 100},
    "MCD":   {"name": "McDonald's",         "sector": "Consumer Defensive",      "mktcap_b": 220},
    "WMT":   {"name": "Walmart",            "sector": "Consumer Defensive",      "mktcap_b": 700},
    "TGT":   {"name": "Target",             "sector": "Consumer Defensive",      "mktcap_b": 70},
    "KO":    {"name": "Coca-Cola",          "sector": "Consumer Defensive",      "mktcap_b": 260},
    "PEP":   {"name": "PepsiCo",            "sector": "Consumer Defensive",      "mktcap_b": 220},
    "SBUX":  {"name": "Starbucks",          "sector": "Consumer Defensive",      "mktcap_b": 90},
    "PG":    {"name": "Procter & Gamble",   "sector": "Consumer Defensive",      "mktcap_b": 380},
    "YUM":   {"name": "Yum! Brands",        "sector": "Consumer Defensive",      "mktcap_b": 40},
    "BA":    {"name": "Boeing",             "sector": "Industrials",             "mktcap_b": 140},
    "GE":    {"name": "GE Aerospace",       "sector": "Industrials",             "mktcap_b": 200},
    "RTX":   {"name": "RTX Corporation",    "sector": "Industrials",             "mktcap_b": 150},
    "LMT":   {"name": "Lockheed Martin",    "sector": "Industrials",             "mktcap_b": 120},
    "HON":   {"name": "Honeywell",          "sector": "Industrials",             "mktcap_b": 140},
    "UPS":   {"name": "United Parcel Service","sector": "Industrials",           "mktcap_b": 130},
    "FDX":   {"name": "FedEx",              "sector": "Industrials",             "mktcap_b": 70},
    "PLUG":  {"name": "Plug Power",         "sector": "Industrials",             "mktcap_b": 2},
    "SAP":   {"name": "SAP SE",             "sector": "Technology",              "mktcap_b": 250},
}

# Edge list — each entry is a dict with full deal metadata
_NETWORK_EDGES: list[dict] = [
    # ── Supply Chain ──────────────────────────────────────────────────────────
    {"src":"AAPL","dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC manufactures Apple A-series and M-series chips",
     "value":"~$20B+ annually","year":"2010",
     "details":"TSMC is Apple's exclusive chip foundry for A-series (iPhone) and M-series (Mac) silicon. Apple represents ~25% of TSMC's total revenue. The relationship began with the A4 chip in 2010, replacing Samsung after IP disputes."},
    {"src":"AAPL","dst":"QCOM", "type":"Supply Chain",
     "desc":"Qualcomm 5G modems and RF chips power every iPhone",
     "value":"~$15B+ annually","year":"2011",
     "details":"Qualcomm supplies 5G modems and RF front-end chips for iPhones. Despite a bitter patent war (2017-2019) settled for ~$4.5B, the companies renewed their supply agreement. Qualcomm chips handle virtually all iPhone cellular connectivity."},
    {"src":"AAPL","dst":"AVGO", "type":"Supply Chain",
     "desc":"Broadcom wireless, Wi-Fi, and Bluetooth chips for Apple devices",
     "value":"~$15B annually (2022 deal)","year":"2020",
     "details":"Apple signed a multi-year agreement with Broadcom in 2020 for wireless components, extended in 2022 to cover Wi-Fi 6E, Bluetooth, and other chips. Broadcom's CEO described Apple as their largest customer, representing ~20% of Broadcom's revenue."},
    {"src":"AAPL","dst":"SWKS", "type":"Supply Chain",
     "desc":"Skyworks RF front-end modules handle cellular signals in iPhone",
     "value":"~$2-3B annually","year":"2011",
     "details":"Skyworks Solutions supplies radio frequency chips and power amplifiers used in iPhones. Apple accounts for roughly 50% of Skyworks' annual revenue. Skyworks chips handle cellular signal amplification across multiple frequency bands for 4G/5G."},
    {"src":"NVDA","dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC manufactures all NVIDIA GPUs on leading-edge nodes",
     "value":"~$10-15B+ annually","year":"1998",
     "details":"TSMC has manufactured NVIDIA's GPUs since the company's early days. Modern NVIDIA GPUs (H100, H200, Blackwell) are produced on TSMC's most advanced 4nm and 3nm processes. NVIDIA's AI-driven growth has made it one of TSMC's top-3 customers."},
    {"src":"AMD", "dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC manufactures AMD Ryzen CPUs and RDNA GPUs",
     "value":"~$8-12B annually","year":"2009",
     "details":"AMD moved exclusively to TSMC after spinning off its fab operations (GlobalFoundries) in 2009. AMD's Ryzen and EPYC CPUs are built on TSMC 5nm/4nm. The AMD-TSMC relationship underpins AMD's competitive comeback against Intel."},
    {"src":"QCOM","dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC manufactures Qualcomm Snapdragon SoCs for premium smartphones",
     "value":"~$6B+ annually","year":"2015",
     "details":"Qualcomm's flagship Snapdragon SoCs are made by TSMC on 4nm and 3nm. After splitting orders with Samsung, Qualcomm shifted more volume to TSMC following Samsung's yield issues in 2022-23. TSMC is now Qualcomm's primary foundry."},
    {"src":"AVGO","dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC manufactures Broadcom networking chips and AI ASICs",
     "value":"~$5B+ annually","year":"2012",
     "details":"Broadcom uses TSMC's advanced nodes for networking chips and custom AI accelerators, including Google's TPUs (made by TSMC under Broadcom design). Broadcom's AI ASIC business is growing rapidly, serving major hyperscalers."},
    {"src":"INTC","dst":"TSM",  "type":"Supply Chain",
     "desc":"TSMC produces Intel Arc GPUs and certain Xeon mobile chips",
     "value":"~$2B+ annually","year":"2021",
     "details":"Intel began outsourcing to TSMC in 2021 as part of its IDM 2.0 strategy. TSMC produces Intel's Arc GPU line and Xeon mobile processors. Intel targets ~40% internal manufacturing while leveraging TSMC for leading-edge designs it cannot produce internally."},
    {"src":"MCD", "dst":"KO",   "type":"Supply Chain",
     "desc":"Coca-Cola is McDonald's exclusive fountain beverage supplier since 1955",
     "value":"~$1.5B annually","year":"1955",
     "details":"Coca-Cola has supplied McDonald's exclusively since Ray Kroc and Robert Woodruff sealed the deal. McDonald's accounts for ~5% of Coca-Cola's global volume across 40,000+ locations. McDonald's fountains use a proprietary chilled delivery system designed with Coke."},
    {"src":"YUM", "dst":"PEP",  "type":"Supply Chain",
     "desc":"PepsiCo exclusive beverage partner for KFC, Pizza Hut, and Taco Bell",
     "value":"~$1B annually","year":"1997",
     "details":"Yum! Brands was spun from PepsiCo in 1997 and retained PepsiCo as its beverage partner. KFC, Pizza Hut, Taco Bell, and Habit Burger serve Pepsi products at 55,000+ global locations, making Yum! one of PepsiCo's largest on-premise accounts."},
    {"src":"WMT", "dst":"PG",   "type":"Supply Chain",
     "desc":"P&G's largest retail partner — ~16% of P&G total revenue flows through Walmart",
     "value":"~$11B annually","year":"1985",
     "details":"Walmart accounts for approximately 16% of P&G's total revenue. The relationship pioneered 'everyday low prices' collaboration and RFID supply-chain tracking in the 1980s-90s. P&G has dedicated account teams embedded at Walmart's Bentonville HQ."},
    {"src":"TGT", "dst":"PG",   "type":"Supply Chain",
     "desc":"P&G second-largest US retail customer through Target stores",
     "value":"~$3-4B annually","year":"1960s",
     "details":"Target is P&G's second-largest US retail customer. P&G brands (Tide, Pampers, Gillette, Oral-B) are among Target's top consumer staples. P&G co-develops Target-exclusive product variants and participates in Target's promotional programs."},
    {"src":"AMZN","dst":"UPS",  "type":"Supply Chain",
     "desc":"UPS handles overflow and international Amazon packages",
     "value":"~$12B (peak, declining)","year":"2001",
     "details":"UPS was Amazon's dominant carrier in the early 2000s. Amazon now handles ~76% of its own volume via Amazon Logistics, but UPS still handles overflow and international shipments. Amazon represented ~11% of UPS 2022 revenue; the relationship is scaling back as Amazon's internal network grows."},
    {"src":"AMZN","dst":"FDX",  "type":"Supply Chain",
     "desc":"FedEx international air freight partner for Amazon sellers",
     "value":"~$8B historically","year":"2001",
     "details":"FedEx ended its U.S. domestic ground contract with Amazon in 2019 as Amazon built its own delivery network. FedEx still handles some international air shipments for Amazon marketplace sellers. FedEx CEO publicly stated they're not pursuing Amazon's business."},
    {"src":"BA",  "dst":"GE",   "type":"Supply Chain",
     "desc":"GE Aviation engines power Boeing 737 MAX (LEAP-1B) and 777X (GE9X)",
     "value":"~$20B+ (lifetime contracts)","year":"1956",
     "details":"GE Aerospace is the sole-source engine supplier for Boeing's 737 MAX (LEAP-1B) and 777X (GE9X). The 787 uses GEnx engines. These programs represent hundreds of billions in lifetime value. Boeing's 737 MAX grounding crisis made GE and Boeing's commercial fortunes closely linked."},
    {"src":"BA",  "dst":"RTX",  "type":"Supply Chain",
     "desc":"Pratt & Whitney engines on Boeing 757, 767, and older 737 models",
     "value":"~$5B+ (aftermarket ongoing)","year":"1970s",
     "details":"Pratt & Whitney (RTX subsidiary) supplies engines for several Boeing aircraft including the 757 (PW2000) and older 767/737 variants. While GE dominates newer Boeing programs, RTX/PW maintains aftermarket services for thousands of P&W-powered Boeing jets globally."},
    {"src":"LMT", "dst":"RTX",  "type":"Supply Chain",
     "desc":"Pratt & Whitney F135 is the sole engine for the F-35 Lightning II",
     "value":"~$50B+ (lifetime program)","year":"2001",
     "details":"P&W (RTX) was selected in 2001 as sole-source engine supplier for the F-35 program — the largest defense procurement in history (~$400B+ lifetime). P&W has exclusive rights to F135 production and maintenance. Congressional debates about an alternative engine have not displaced P&W."},
    {"src":"LMT", "dst":"GE",   "type":"Supply Chain",
     "desc":"GE F110 turbofan engines power F-16 Fighting Falcons sold by Lockheed",
     "value":"~$2B+ (ongoing)","year":"1984",
     "details":"GE Aerospace's F110 powers a large share of F-16s, competing with Pratt & Whitney's F100. For F-16 Block 70/72 export sales, buyers can choose GE F110 or P&W F100. This competitive engine environment has persisted across 50+ years of F-16 production."},
    {"src":"XOM", "dst":"SLB",  "type":"Supply Chain",
     "desc":"SLB provides oilfield services, well-logging, and digital tools to ExxonMobil",
     "value":"~$2-5B annually","year":"1970s",
     "details":"SLB (formerly Schlumberger) is ExxonMobil's largest third-party oilfield services provider. SLB supplies drilling fluids, well logging, completion services, and digital reservoir management for Exxon's Permian, Guyana, and deepwater Gulf of Mexico operations."},
    {"src":"CVX", "dst":"SLB",  "type":"Supply Chain",
     "desc":"SLB oilfield services for Chevron's global upstream operations",
     "value":"~$1.5-3B annually","year":"1970s",
     "details":"SLB provides Chevron with directional drilling, formation evaluation, and stimulation services. Key Chevron projects supported by SLB include Tengiz expansion in Kazakhstan, deepwater Gulf of Mexico, and Permian Basin unconventional operations."},
    {"src":"XOM", "dst":"HAL",  "type":"Supply Chain",
     "desc":"Halliburton drilling and hydraulic fracturing services for ExxonMobil",
     "value":"~$1-3B annually","year":"1980s",
     "details":"Halliburton provides ExxonMobil with hydraulic fracturing, cementing, and completion services, especially in the Permian Basin. HAL's Sperry Drilling and Baroid brands support Exxon's North American unconventional operations, typically awarded in competitive bids with SLB."},
    {"src":"CVX", "dst":"HAL",  "type":"Supply Chain",
     "desc":"Halliburton well completion and drilling services for Chevron",
     "value":"~$1-2B annually","year":"1980s",
     "details":"Halliburton supports Chevron's upstream operations with well completion, production chemicals, and drilling services across the Permian Basin, deepwater Gulf, and international projects including Kazakhstan's Tengiz field."},
    {"src":"META","dst":"QCOM", "type":"Supply Chain",
     "desc":"Qualcomm Snapdragon XR chips are the sole processor in Meta Quest headsets",
     "value":"~$1.5B annually","year":"2022",
     "details":"Qualcomm's Snapdragon XR2 Gen 2 and XR2+ Gen 2 chips are the exclusive processor in Meta Quest 3 and Quest Pro. Qualcomm and Meta announced a multi-year, multi-generation supply agreement in 2022. Meta's AR/VR ambitions make this a strategically growing relationship."},

    # ── Partnership ───────────────────────────────────────────────────────────
    {"src":"GOOGL","dst":"AAPL","type":"Partnership",
     "desc":"Google pays Apple for default search engine placement on Safari/iOS",
     "value":"~$18-20B annually","year":"2007",
     "details":"Google's payment to Apple for default search status on Safari is the largest known revenue-sharing deal in tech. A 2023 DOJ antitrust trial revealed Google paid Apple $18B in 2021 alone. This deal represents ~15-18% of Apple Services revenue and is Google's single largest traffic acquisition cost."},
    {"src":"MSFT","dst":"NVDA", "type":"Partnership",
     "desc":"Microsoft Azure built its AI supercomputing infrastructure on NVIDIA GPUs",
     "value":"~$10B+ (multi-year)","year":"2016",
     "details":"Microsoft Azure hosts tens of thousands of NVIDIA H100 GPUs powering Azure OpenAI Service (ChatGPT, Copilot). NVIDIA CEO Jensen Huang and Microsoft CEO Satya Nadella appear frequently together at product launches. The relationship deepened dramatically in 2023 with Microsoft's $10B+ OpenAI investment requiring massive NVIDIA GPU clusters."},
    {"src":"GOOGL","dst":"NVDA","type":"Partnership",
     "desc":"Google Cloud deploys NVIDIA H100/H200 clusters for enterprise AI",
     "value":"~$5B+ (multi-year)","year":"2023",
     "details":"Google Cloud deployed large clusters of NVIDIA H100 and H200 GPUs to serve enterprise AI demand alongside its proprietary TPU chips. The partnership includes co-selling commitments on Google Cloud Marketplace for NVIDIA-powered AI workloads."},
    {"src":"META","dst":"NVDA", "type":"Partnership",
     "desc":"Meta ordered 350,000+ NVIDIA H100 GPUs — one of the world's largest AI clusters",
     "value":"~$10-15B (2023-24 orders)","year":"2023",
     "details":"Meta CEO Mark Zuckerberg announced in 2024 that Meta was deploying 350,000 H100 GPUs for AI training — one of the largest GPU clusters in existence. Meta uses NVIDIA GPUs to train LLaMA language models and develop AI for its 3B+ user platforms, making Meta one of NVIDIA's largest customers by unit volume."},
    {"src":"AMZN","dst":"NVDA", "type":"Partnership",
     "desc":"AWS P5/P4 instances powered by NVIDIA H100/A100 GPUs for cloud AI",
     "value":"~$5-10B annually","year":"2023",
     "details":"AWS's P5 instances use NVIDIA H100 SXM5 GPUs with 192GB HBM3 memory per GPU. Amazon also develops its own Trainium and Inferentia chips but NVIDIA partnerships ensure Amazon can serve customers who depend on NVIDIA's CUDA ecosystem. AWS and NVIDIA co-market AI training services."},
    {"src":"ORCL","dst":"NVDA", "type":"Partnership",
     "desc":"Oracle Cloud built a 131,000-GPU NVIDIA H100 supercluster",
     "value":"~$4B+ (2023-24)","year":"2023",
     "details":"Oracle Cloud Infrastructure (OCI) built one of the largest H100 GPU clusters globally — 131,072 NVIDIA H100s interconnected via high-bandwidth fabric. NVIDIA CEO Jensen Huang featured Oracle CEO Larry Ellison at the 2024 GTC keynote. Oracle positioned this as its leap to compete with AWS and Azure on AI infrastructure."},
    {"src":"TSLA","dst":"NVDA", "type":"Partnership",
     "desc":"Tesla used NVIDIA GPUs to train Full Self-Driving AI before building Dojo",
     "value":"~$500M-1B historically","year":"2019",
     "details":"Tesla relied heavily on NVIDIA A100 and H100 GPUs for training its FSD neural networks before transitioning to its proprietary Dojo supercomputer in 2023. Elon Musk noted Tesla was among the largest buyers of NVIDIA GPUs. Some NVIDIA GPU usage for AI inference continues alongside Dojo."},
    {"src":"V",   "dst":"PYPL", "type":"Partnership",
     "desc":"Visa-PayPal strategic deal: Visa promoted as 'first choice' in PayPal wallet",
     "value":"Revenue sharing (undisclosed)","year":"2016",
     "details":"In 2016, Visa and PayPal ended years of adversarial positioning with a landmark strategic partnership. PayPal agreed to promote Visa as a first-choice funding option and enable tap-to-pay, while Visa gained access to PayPal's 400M+ users. Venmo integrates with Visa Direct for instant payouts."},
    {"src":"MA",  "dst":"PYPL", "type":"Partnership",
     "desc":"Mastercard-PayPal strategic deal for digital wallet and Click to Pay integration",
     "value":"Revenue sharing (undisclosed)","year":"2016",
     "details":"Mastercard and PayPal signed a mirror strategic agreement in 2016. Mastercard is promoted as a preferred payment option in PayPal's wallet, while PayPal benefits from Mastercard's merchant network and Mastercard Send for money transfers."},
    {"src":"AAPL","dst":"V",    "type":"Partnership",
     "desc":"Apple Pay operates on Visa network — Visa was a founding partner at 2014 launch",
     "value":"~$0.15% per transaction","year":"2014",
     "details":"Visa was one of three founding payment network partners when Apple Pay launched in October 2014. Visa provides tokenization infrastructure for Apple Pay contactless transactions. Apple Pay is accepted at 85%+ of US retailers. Apple earns approximately 0.15% on each Visa transaction made via Apple Pay."},
    {"src":"AAPL","dst":"MA",   "type":"Partnership",
     "desc":"Apple Card runs on Mastercard network; Apple Pay on MA since 2014",
     "value":"Transaction fee share (undisclosed)","year":"2014",
     "details":"The Apple Card (launched 2019 with Goldman Sachs) runs on the Mastercard payment network. Apple Pay also launched with Mastercard in 2014. Apple negotiated competitive interchange rates and revenue-sharing. Goldman Sachs withdrew from Apple Card in 2024, with a new issuer expected to continue the Mastercard arrangement."},
    {"src":"MSFT","dst":"CRM",  "type":"Partnership",
     "desc":"Salesforce and Microsoft 365 deep AI integration — Copilot, Teams, Azure",
     "value":"~$100M+ annually","year":"2014",
     "details":"After years of rivalry, Salesforce and Microsoft formed a partnership in 2014 that has deepened dramatically. Salesforce Data Cloud integrates with Azure OpenAI; Slack connects to Teams. In 2023 they deepened the AI partnership. Notable because Salesforce CEO Marc Benioff was a vocal Microsoft critic for years."},
    {"src":"GOOGL","dst":"CRM", "type":"Partnership",
     "desc":"Salesforce + Google Cloud partnership for CRM and AI workloads",
     "value":"~$50M+ annually","year":"2017",
     "details":"Salesforce and Google Cloud signed a partnership in 2017 to integrate Google Workspace with Salesforce CRM. The partnership expanded in 2023 with Google Vertex AI integrating into Salesforce Einstein AI. Google Workspace (Gmail, Calendar, Drive) has native Salesforce connectors."},
    {"src":"WMT", "dst":"MSFT", "type":"Partnership",
     "desc":"Walmart signed a 5-year Azure cloud deal, deliberately avoiding AWS competitor",
     "value":"~$400M+ (5-year)","year":"2018",
     "details":"Walmart signed a 5-year cloud deal with Microsoft Azure in 2018, a calculated move to avoid enriching competitor Amazon (AWS). Walmart uses Azure for supply chain optimization, inventory management, and customer analytics. The deal was extended in 2022 and has become a template for retailers avoiding Amazon cloud services."},
    {"src":"MSFT","dst":"SAP",  "type":"Partnership",
     "desc":"SAP enterprise apps run on Microsoft Azure — RISE with SAP program",
     "value":"~$1B+ annually","year":"2016",
     "details":"SAP and Microsoft have partnered since 2016 on running SAP S/4HANA and enterprise workloads on Azure. The 'RISE with SAP on Azure' program helps enterprises migrate SAP systems to the cloud. Microsoft Teams integrates natively with SAP apps. The partnership expanded in 2023 with Azure OpenAI powering SAP Joule AI assistant."},
    {"src":"META","dst":"MSFT", "type":"Partnership",
     "desc":"Meta's Llama open-source AI models available on Microsoft Azure Marketplace",
     "value":"Revenue sharing (undisclosed)","year":"2023",
     "details":"Meta made its Llama 2 and Llama 3 models available through Microsoft Azure AI Studio in 2023. Azure enterprise customers can fine-tune and deploy Llama models with Azure's security and compliance controls. The partnership gives Meta's Llama commercial reach while helping Azure compete with AWS Bedrock."},
    {"src":"JPM", "dst":"V",    "type":"Partnership",
     "desc":"JPMorgan Chase issues the world's largest Visa credit card portfolio",
     "value":"Interchange revenue sharing","year":"1958",
     "details":"JPMorgan Chase's Sapphire, Freedom, Ink, and co-brand cards (United, Marriott) run on Visa's network. Chase is Visa's largest card-issuing partner by purchase volume (~$800B+/yr). Chase Sapphire Reserve, launched 2016, became one of the most successful premium card launches in history."},
    {"src":"BAC", "dst":"MA",   "type":"Partnership",
     "desc":"Bank of America Mastercard consumer and co-brand card partnership",
     "value":"Interchange revenue sharing","year":"1966",
     "details":"Bank of America is one of Mastercard's largest card-issuing partners. BofA's cash rewards, travel rewards, and co-brand cards (Alaska Airlines, Allegiant) operate on Mastercard's network. BofA also participates in Mastercard's Click to Pay digital initiative."},
    {"src":"WFC", "dst":"V",    "type":"Partnership",
     "desc":"Wells Fargo Visa consumer card and debit card partnership",
     "value":"Interchange revenue sharing","year":"1970s",
     "details":"Wells Fargo issues Visa consumer and business credit cards, and all Wells Fargo debit cards run on Visa's network. Signature cards include the Active Cash (2% cash back) and Autograph. Wells Fargo has ~$500B in Visa purchase volume annually, making it a top-5 Visa issuer globally."},
    {"src":"AMZN","dst":"SBUX", "type":"Partnership",
     "desc":"Starbucks Alexa voice ordering; Starbucks operates cafes on Amazon campus",
     "value":"Nominal (strategic)","year":"2017",
     "details":"Starbucks launched an Alexa skill in 2017 for voice ordering. Starbucks cafes operate inside Amazon's Seattle HQ. Both companies are Seattle-based with overlapping leadership relationships. Amazon Fresh stores sell Starbucks ready-to-drink products, extending the commercial relationship into grocery."},
    {"src":"TSLA","dst":"F",    "type":"Partnership",
     "desc":"Ford adopts Tesla NACS connector — F-150 Lightning and Mach-E gain Supercharger access",
     "value":"Royalty and charging fee savings","year":"2023",
     "details":"In May 2023, Ford became the first legacy automaker to adopt Tesla's NACS charging standard. Ford EV drivers gained access to Tesla's 12,000+ North American Supercharger network. Adapters shipped for Mustang Mach-E and F-150 Lightning owners in 2023; NACS native ports roll out in 2025 model years."},
    {"src":"TSLA","dst":"GM",   "type":"Partnership",
     "desc":"GM adopts Tesla NACS standard — Silverado EV, Equinox EV get Supercharger access",
     "value":"Royalty and charging fee savings","year":"2023",
     "details":"In June 2023, GM CEO Mary Barra joined Elon Musk to announce GM's NACS adoption — a major industry validation of Tesla's connector. GM's Ultium-based EVs gain access to Tesla Superchargers via adapter initially, then native NACS ports in 2025. GM was the second major OEM to adopt NACS, accelerating it becoming the US standard."},
    {"src":"MSFT","dst":"AAPL", "type":"Partnership",
     "desc":"Microsoft 365 on iOS/Mac — relationship rooted in 1997 rescue investment",
     "value":"~$5B+ annually (App Store share)","year":"1997",
     "details":"In 1997, Microsoft invested $150M in near-bankrupt Apple and committed to develop Office for Mac for 5 years. Today, Microsoft 365 (Word, Excel, Teams) is among the top paid apps on the App Store. Microsoft pays Apple's App Store commission. A 2023 update brought Microsoft Copilot to iPhone."},
    {"src":"GOOGL","dst":"SPOT","type":"Partnership",
     "desc":"Spotify preferred music partner for Google Assistant; Google Cloud hosting deal",
     "value":"~$100M+ (cloud contract)","year":"2019",
     "details":"Spotify and Google announced a partnership in 2019: Spotify became the preferred music streaming partner for Google Assistant, and signed a multi-year commitment to migrate infrastructure to Google Cloud. Spotify is preinstalled on Pixel phones and featured in Google Home devices."},
    {"src":"ADBE","dst":"MSFT", "type":"Partnership",
     "desc":"Adobe Firefly AI embedded in Microsoft 365; Adobe Express integrates with Teams",
     "value":"Revenue sharing (undisclosed)","year":"2023",
     "details":"Adobe and Microsoft announced a deep AI integration in 2023: Adobe Firefly generative AI is embedded into Microsoft 365 apps (Word, PowerPoint), and Adobe Express integrates with Teams. Users can create design assets without leaving Microsoft apps. The partnership also includes joint enterprise sales motions."},
    {"src":"GOOGL","dst":"UBER","type":"Partnership",
     "desc":"Google Maps powers all Uber routing, ETA, and navigation globally",
     "value":"~$50-100M annually (estimated)","year":"2012",
     "details":"Google Maps has been the core mapping infrastructure in Uber's app since its early days, providing routing, ETA calculations, and street-level navigation. Uber is one of Google Maps' largest commercial API customers. Uber has evaluated alternatives (HERE Maps, Mapbox) for parts of its stack, but Google Maps remains the primary rider-experience mapping layer."},
    {"src":"MSFT","dst":"GILD", "type":"Partnership",
     "desc":"Gilead Sciences uses Microsoft Azure AI for antiviral drug discovery",
     "value":"~$50M+ (estimated)","year":"2020",
     "details":"Gilead Sciences and Microsoft partnered in 2020 to apply AI to antiviral drug discovery and COVID-19 research. Gilead uses Azure Machine Learning and Microsoft AI tools to analyze large molecular datasets and run protein-folding simulations. The partnership accelerated Gilead's computational chemistry capabilities."},

    # ── Ownership ─────────────────────────────────────────────────────────────
    {"src":"BRK-B","dst":"AAPL","type":"Ownership",
     "desc":"Berkshire Hathaway ~5.5% stake in Apple — was Berkshire's single largest holding",
     "value":"~$155-177B (peak 2023)","year":"2016",
     "details":"Berkshire began buying Apple in Q1 2016, initially driven by investment managers Ted Weschler and Todd Combs. Warren Buffett later called it Berkshire's best investment. At peak in mid-2023, Berkshire held 915M shares (~$177B). Berkshire sold ~50% of the position in 2023-24, retaining 400M+ shares. Apple paid Berkshire ~$900M+ annually in dividends."},
    {"src":"BRK-B","dst":"BAC", "type":"Ownership",
     "desc":"Berkshire holds ~13% of Bank of America — second-largest equity position",
     "value":"~$34B (2024)","year":"2011",
     "details":"Berkshire acquired $5B in Bank of America warrants in 2011 during BofA's post-crisis capital raise. Buffett called then-CEO Brian Moynihan from his bathtub to propose the deal. Berkshire converted warrants to 700M shares in 2017. Berkshire began selling shares in 2024, reducing from 13% toward 10%+."},
    {"src":"BRK-B","dst":"KO",  "type":"Ownership",
     "desc":"Berkshire holds ~9.3% of Coca-Cola — held for 35+ years without selling a share",
     "value":"~$24B (2024)","year":"1988",
     "details":"Berkshire bought 6.2% of Coca-Cola in 1988-89 for ~$1.3B after the 1987 stock crash. This grew to 400M shares worth ~$24B — an 18x+ return. Berkshire has never sold a single share in 35+ years. KO pays Berkshire ~$776M in annual dividends, a 60% yield on Berkshire's original cost basis."},
    {"src":"BRK-B","dst":"AXP", "type":"Ownership",
     "desc":"Berkshire holds ~21% of American Express — relationship dating to the 1960s",
     "value":"~$38B (2024)","year":"1964",
     "details":"Buffett first invested in American Express during the 1963 'Salad Oil Scandal' when Amex stock fell 50%. Berkshire built its current position from 1994-1998 averaging ~$8.50/share. The 151.6M-share position was worth $38B in 2024. Buffett frequently praises Amex's customer loyalty and premium-card competitive moat."},
    {"src":"BRK-B","dst":"OXY", "type":"Ownership",
     "desc":"Berkshire holds ~28% of Occidental Petroleum — has SEC approval to buy up to 50%",
     "value":"~$14B (2024)","year":"2019",
     "details":"Berkshire first invested during OXY's 2019 bid for Anadarko, providing $10B in preferred stock financing. Berkshire then accumulated common shares on the open market. By 2024, Berkshire held 27.8% of OXY common stock with SEC approval to buy up to 50%. Buffett has called OXY a potential full acquisition target, attracted by its Permian Basin assets and direct-air carbon capture technology."},
    {"src":"BRK-B","dst":"MCO", "type":"Ownership",
     "desc":"Berkshire holds ~13% of Moody's — received shares at Dun & Bradstreet spinoff",
     "value":"~$11B (2024)","year":"2000",
     "details":"Berkshire received Moody's shares when Dun & Bradstreet split in 2000. Berkshire's ~24.6M-share position has never been sold. Buffett considers Moody's a business with significant pricing power and high barriers to entry — rating agencies Moody's and S&P control ~80% of the global credit-rating market."},
    {"src":"BRK-B","dst":"CVX", "type":"Ownership",
     "desc":"Berkshire holds ~9% of Chevron — major energy sector position since 2020",
     "value":"~$18B (2024)","year":"2020",
     "details":"Berkshire began buying Chevron during COVID's oil price collapse in 2020. By Q4 2021 it was Berkshire's fourth-largest position at $4.5B, expanding to ~$26B by 2022 during the oil surge. Berkshire has since reduced the position but remains a ~9% owner, reflecting Buffett's view that oil will remain essential for decades."},
    {"src":"AMZN","dst":"RIVN", "type":"Ownership",
     "desc":"Amazon owns ~16% of Rivian + 100,000-van EV delivery purchase order",
     "value":"~$4.4B investment + $10B van contract","year":"2019",
     "details":"Amazon led a $700M Series E funding round for Rivian in 2019. Amazon also committed to purchase 100,000 electric delivery vans by 2030 as part of its Climate Pledge. At Rivian's November 2021 IPO, Amazon's stake was worth ~$17B. The first R1 vans began Amazon deliveries in 2022. Amazon has since reduced its stake as Rivian's share price fell."},
    {"src":"GOOGL","dst":"UBER","type":"Ownership",
     "desc":"Alphabet (GV) early investor in Uber — holds equity since Series B in 2013",
     "value":"~$250M initial (2013); ~$3B+ unrealized","year":"2013",
     "details":"Google Ventures (now GV) led Uber's $258M Series B in 2013, valuing Uber at $3.76B. Alphabet retained a significant equity stake through Uber's 2019 IPO, generating multi-billion dollar returns. Despite building Waymo to compete in autonomous ride-hailing, Alphabet maintains its Uber equity position."},

    # ── Joint Venture ─────────────────────────────────────────────────────────
    {"src":"PFE", "dst":"BNTX", "type":"Joint Venture",
     "desc":"Pfizer-BioNTech co-developed Comirnaty, the world's first authorized mRNA COVID vaccine",
     "value":"~$37B+ combined revenue (2021-22)","year":"2020",
     "details":"In March 2020, Pfizer and BioNTech signed a co-development and commercialization agreement for a COVID-19 mRNA vaccine. BioNTech provided the mRNA technology; Pfizer provided manufacturing scale and commercial infrastructure. The vaccine (BNT162b2/Comirnaty) received emergency authorization in December 2020. The partnership generated over $37B combined in 2021. BioNTech received 50% of profits; Pfizer handled manufacturing and non-German sales."},
    {"src":"JNJ", "dst":"ABBV", "type":"Joint Venture",
     "desc":"Imbruvica co-development: Janssen/Pharmacyclics partnership acquired by AbbVie in 2015",
     "value":"~$2B annually in royalties to JNJ","year":"2015",
     "details":"J&J's Janssen subsidiary co-developed Imbruvica with Pharmacyclics for blood cancers (CLL, MCL). When AbbVie acquired Pharmacyclics in 2015 for $21B, AbbVie inherited the Imbruvica partnership with J&J. AbbVie commercializes Imbruvica globally while paying J&J substantial royalties (~$2B/yr). Imbruvica peaked at ~$9B in annual sales before next-generation BTK inhibitors eroded market share."},
    {"src":"BA",  "dst":"LMT",  "type":"Joint Venture",
     "desc":"United Launch Alliance (ULA) — 50/50 rocket launch JV for government payloads",
     "value":"~$2-3B annually (gov. launches)","year":"2006",
     "details":"Boeing and Lockheed Martin formed United Launch Alliance in 2006 by merging their respective government launch businesses (Delta and Atlas rockets). ULA has an exceptional track record with 100% mission success for national security satellites. SpaceX's competition from 2016 onward pressured ULA, leading both partners to explore strategic alternatives including a potential sale."},
    {"src":"XOM", "dst":"CVX",  "type":"Joint Venture",
     "desc":"Tengizchevroil (TCO) — $45B+ Kazakhstan upstream oil production JV since 1993",
     "value":"~$6B+ annually (combined)","year":"1993",
     "details":"Tengizchevroil is a production-sharing JV in Kazakhstan's Tengiz oil field: Chevron 50%, ExxonMobil 25%, KazMunayGas 20%, Lukoil 5%. The JV was formed in 1993 post-Soviet Union dissolution. TCO's Future Growth Project ($45B+) is one of the largest oil developments in history, producing ~700,000 barrels/day in 2023. Both XOM and CVX count TCO among their top-10 production assets."},
    {"src":"GM",  "dst":"PLUG", "type":"Joint Venture",
     "desc":"GM-Plug Power hydrogen fuel cell JV (Hydrotec) for commercial trucks and aviation",
     "value":"$300M equity investment (2021)","year":"2021",
     "details":"General Motors and Plug Power formed a strategic partnership in 2021. GM licensed its Hydrotec hydrogen fuel cell technology to Plug Power for manufacturing and integration into commercial vehicles, aviation, and locomotives. GM received a $300M equity stake in Plug Power. The collaboration targets clean hydrogen for heavy transport as hydrogen infrastructure expands."},
    {"src":"MRK", "dst":"BNTX", "type":"Joint Venture",
     "desc":"Merck-BioNTech personalized mRNA cancer vaccine co-development (V940/mRNA-4157)",
     "value":"$250M upfront + ~$4B+ milestone potential","year":"2022",
     "details":"In 2022, Merck exercised its option to co-develop BioNTech's personalized mRNA cancer vaccine (mRNA-4157/V940) with Keytruda (pembrolizumab). The Phase 2b KEYNOTE-942 trial showed a 44% reduction in melanoma recurrence. Merck paid $250M upfront with $4B+ in potential milestones. This partnership targets individualized mRNA vaccines tailored to each patient's tumor mutations."},
    {"src":"F",   "dst":"RIVN", "type":"Joint Venture",
     "desc":"Ford invested $1.2B in Rivian at IPO; planned EV platform JV was cancelled April 2022",
     "value":"$1.2B investment (2021 IPO)","year":"2021",
     "details":"Ford invested $500M in Rivian in 2019 and held ~12% at IPO (November 2021, peak value ~$100B+). Ford and Rivian planned to co-develop a Lincoln EV on Rivian's platform. Ford cancelled the JV in April 2022, citing platform differences. Ford retained ~11M Rivian shares, selling gradually at a loss from the peak. The investment peaked at ~$12B in value."},
    {"src":"GOOGL","dst":"MSFT","type":"Joint Venture",
     "desc":"Co-signed White House AI safety pledge; joint Partnership on AI founding members",
     "value":"Regulatory goodwill investment","year":"2023",
     "details":"Google and Microsoft both signed the White House voluntary AI safety commitments in 2023 alongside Anthropic, Meta, Amazon, and others, pledging pre-deployment safety testing and information sharing. Both are founding members of the Partnership on AI (2016). Despite fierce cloud AI competition, they cooperate on safety watermarking (SynthID), red-teaming coordination, and AI interoperability standards."},
]

# Fast lookup: (src, dst) → edge dict, also keyed (dst, src) for undirected access
_EDGE_LOOKUP: dict[tuple[str, str], dict] = {}
for _e in _NETWORK_EDGES:
    _EDGE_LOOKUP[(_e["src"], _e["dst"])] = _e
    _EDGE_LOOKUP[(_e["dst"], _e["src"])] = _e

_SECTOR_COLORS: dict[str, str] = {
    "Technology":             "#1A6DFF",
    "Communication Services": "#9C27B0",
    "Consumer Cyclical":      "#FF9800",
    "Consumer Defensive":     "#4CAF50",
    "Financial Services":     "#26C6DA",
    "Energy":                 "#FF5722",
    "Healthcare":             "#E91E63",
    "Industrials":            "#78909C",
    "Real Estate":            "#8D6E63",
    "Utilities":              "#FFEE58",
    "Basic Materials":        "#66BB6A",
}

_REL_COLORS: dict[str, str] = {
    "Supply Chain": "#FF9800",
    "Partnership":  "#1A6DFF",
    "Ownership":    "#00CC66",
    "Joint Venture":"#E91E63",
}


@st.cache_data(show_spinner=False)
def _build_network_layout() -> dict[str, tuple[float, float]]:
    G = nx.Graph()
    for ticker in _NETWORK_COMPANIES:
        G.add_node(ticker)
    for e in _NETWORK_EDGES:
        if e["src"] in _NETWORK_COMPANIES and e["dst"] in _NETWORK_COMPANIES:
            G.add_edge(e["src"], e["dst"])
    return nx.spring_layout(G, seed=42, k=2.2, iterations=80)


def _build_network_figure(
    pos: dict[str, tuple[float, float]],
    highlighted_nodes: set[str] | None,  # None = all full opacity
    highlighted_edge: tuple[str, str] | None,  # (src, dst) of selected edge
    rel_types: set[str],
    sector_filter: set[str],
) -> go.Figure:
    fig = go.Figure()

    # Active edges after type + sector filters
    active_edges = [
        e for e in _NETWORK_EDGES
        if e["type"] in rel_types
    ]
    if sector_filter and "All" not in sector_filter:
        active_edges = [
            e for e in active_edges
            if (_NETWORK_COMPANIES.get(e["src"], {}).get("sector", "") in sector_filter
                or _NETWORK_COMPANIES.get(e["dst"], {}).get("sector", "") in sector_filter)
        ]

    # ── Edge lines + midpoint hit-area markers ────────────────────────────────
    for rel_type, color in _REL_COLORS.items():
        if rel_type not in rel_types:
            continue
        edges_of_type = [e for e in active_edges if e["type"] == rel_type]
        if not edges_of_type:
            continue

        mid_x_list, mid_y_list, mid_cd = [], [], []

        for e in edges_of_type:
            s, d = e["src"], e["dst"]
            if s not in pos or d not in pos:
                continue
            x0, y0 = pos[s]
            x1, y1 = pos[d]
            mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2

            is_this_edge_sel = highlighted_edge and (
                (s == highlighted_edge[0] and d == highlighted_edge[1]) or
                (d == highlighted_edge[0] and s == highlighted_edge[1])
            )
            involves_highlighted = (highlighted_nodes is None or
                                    s in (highlighted_nodes or set()) or
                                    d in (highlighted_nodes or set()))

            if highlighted_nodes is not None and not involves_highlighted and not is_this_edge_sel:
                line_opacity = 0.05
            elif is_this_edge_sel:
                line_opacity = 1.0
            else:
                line_opacity = 0.75

            lw = 3 if is_this_edge_sel else 2

            fig.add_trace(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                mode="lines",
                line=dict(color=color, width=lw),
                opacity=line_opacity,
                hoverinfo="skip",
                showlegend=False,
            ))

            # Midpoint marker — clickable hit area
            mid_x_list.append(mid_x)
            mid_y_list.append(mid_y)
            mid_cd.append(["edge", s, d, rel_type, e["desc"]])

        if mid_x_list:
            fig.add_trace(go.Scatter(
                x=mid_x_list, y=mid_y_list,
                mode="markers",
                marker=dict(
                    symbol="diamond",
                    size=9,
                    color=color,
                    opacity=0.55,
                    line=dict(color="#fff", width=0.5),
                ),
                customdata=mid_cd,
                hovertemplate=(
                    "<b>%{customdata[1]} ↔ %{customdata[2]}</b><br>"
                    "%{customdata[3]}<br>"
                    "<i>%{customdata[4]}</i><br>"
                    "<span style='color:#aaa'>Click for deal details</span>"
                    "<extra></extra>"
                ),
                showlegend=False,
            ))

    # ── Nodes per sector ──────────────────────────────────────────────────────
    visible_nodes = set(_NETWORK_COMPANIES.keys())
    for sector in sorted({_NETWORK_COMPANIES[t]["sector"] for t in visible_nodes if t in pos}):
        tickers_in_sector = [
            t for t in visible_nodes
            if _NETWORK_COMPANIES.get(t, {}).get("sector") == sector and t in pos
        ]
        if not tickers_in_sector:
            continue

        node_x, node_y, node_text, customdata, sizes, opacities, borders = [], [], [], [], [], [], []
        for t in tickers_in_sector:
            x, y = pos[t]
            node_x.append(x); node_y.append(y)
            info = _NETWORK_COMPANIES[t]
            mc = info["mktcap_b"]
            sizes.append(max(10, min(40, 8 + 12 * math.log10(max(mc, 1) + 1))))
            node_text.append(t)
            customdata.append(["node", t, info["name"], info["sector"], mc])

            if highlighted_nodes is not None:
                op = 1.0 if t in highlighted_nodes else 0.12
            elif sector_filter and "All" not in sector_filter:
                op = 1.0 if info["sector"] in sector_filter else 0.25
            else:
                op = 1.0
            opacities.append(op)

            is_edge_endpoint = (highlighted_edge and
                                (t == highlighted_edge[0] or t == highlighted_edge[1]))
            borders.append(
                "#FFD700" if (highlighted_nodes and t == next(iter(highlighted_nodes), None)
                              and len(highlighted_nodes) == 1) else
                "#FFD700" if is_edge_endpoint else
                "#FFFFFF" if (highlighted_nodes and t in highlighted_nodes) else
                "#2a2a2a"
            )

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode="markers+text",
            name=sector,
            marker=dict(
                color=[_SECTOR_COLORS.get(sector, "#888")] * len(node_x),
                size=sizes,
                line=dict(color=borders, width=[2 if b != "#2a2a2a" else 0.5 for b in borders]),
                opacity=opacities,
            ),
            text=node_text,
            textposition="top center",
            textfont=dict(size=9, color="#E2E8F0"),
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[1]}</b> · %{customdata[2]}<br>"
                "Sector: %{customdata[3]}<br>"
                "Market Cap: ~$%{customdata[4]:.0f}B<br>"
                "<span style='color:#aaa'>Click for all relationships</span>"
                "<extra></extra>"
            ),
            showlegend=True,
            legendgroup=sector,
        ))

    # Legend entries for relationship types
    for rel_type, color in _REL_COLORS.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines",
            name=rel_type,
            line=dict(color=color, width=3),
            showlegend=True, legendgroup=rel_type,
        ))

    dark = st.session_state.get("dark_mode", True)
    fig.update_layout(
        height=680,
        margin=dict(t=10, l=5, r=5, b=5),
        paper_bgcolor="#141927" if dark else "#FFFFFF",
        plot_bgcolor="#0B0E1A" if dark else "#F2F5FA",
        font=dict(color="#E2E8F0" if dark else "#0B1628", family="sans-serif"),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode="closest",
        legend=dict(
            orientation="v", x=1.01, y=0.99,
            bgcolor="rgba(20,25,39,0.9)" if dark else "rgba(255,255,255,0.9)",
            bordercolor="#1E2C42" if dark else "#CDD5E0",
            borderwidth=1, font=dict(size=10), tracegroupgap=4,
        ),
        dragmode="pan",
    )
    return fig


def _render_node_panel(ticker: str, rel_types: set[str]) -> None:
    """Structured panel for a clicked company node — shows all its relationships."""
    info = _NETWORK_COMPANIES[ticker]
    dark = st.session_state.get("dark_mode", True)
    badge_bg  = "rgba(26,109,255,0.15)"
    badge_txt = "#4D94FF"

    # ── Header ────────────────────────────────────────────────────────────────
    hcol, vcol = st.columns([5, 2])
    with hcol:
        sector_color = _SECTOR_COLORS.get(info["sector"], "#888")
        st.markdown(
            f"<h3 style='margin:0'>{ticker} &nbsp;"
            f"<span style='font-size:1rem;font-weight:400;color:var(--txt2)'>{info['name']}</span>"
            f"</h3>"
            f"<span style='font-size:0.78rem;background:{sector_color}22;color:{sector_color};"
            f"border:1px solid {sector_color}44;border-radius:4px;padding:2px 8px;"
            f"margin-right:8px'>{info['sector']}</span>"
            f"<span style='font-size:0.78rem;color:var(--txt2)'>~${info['mktcap_b']:,}B market cap</span>",
            unsafe_allow_html=True,
        )
    with vcol:
        st.write(" ")
        if st.button(f"📈 View {ticker} Stock Profile", key="net_view_stock",
                     use_container_width=True):
            st.session_state["net_detail_ticker"] = ticker
            st.rerun()

    # ── Relationship cards ────────────────────────────────────────────────────
    node_edges = [
        e for e in _NETWORK_EDGES
        if (e["src"] == ticker or e["dst"] == ticker) and e["type"] in rel_types
    ]
    if not node_edges:
        st.caption("No relationships match the current filter.")
        return

    st.markdown(f"**{len(node_edges)} relationship{'s' if len(node_edges) != 1 else ''} found**")

    # Group by relationship type for visual organisation
    by_type: dict[str, list[dict]] = {}
    for e in node_edges:
        by_type.setdefault(e["type"], []).append(e)

    for rel_type in _REL_COLORS:
        edges_of_type = by_type.get(rel_type, [])
        if not edges_of_type:
            continue
        color = _REL_COLORS[rel_type]
        st.markdown(
            f"<div style='font-size:0.7rem;font-weight:800;text-transform:uppercase;"
            f"letter-spacing:0.1em;color:{color};margin:14px 0 6px'>"
            f"● {rel_type} ({len(edges_of_type)})</div>",
            unsafe_allow_html=True,
        )

        cols_per_row = 2
        for row_start in range(0, len(edges_of_type), cols_per_row):
            row_edges = edges_of_type[row_start:row_start + cols_per_row]
            cols = st.columns(len(row_edges))
            for col, e in zip(cols, row_edges):
                other = e["dst"] if e["src"] == ticker else e["src"]
                direction = "→" if e["src"] == ticker else "←"
                other_info = _NETWORK_COMPANIES.get(other, {})
                other_sector = other_info.get("sector", "")
                other_color  = _SECTOR_COLORS.get(other_sector, "#888")
                with col:
                    with st.container(border=True):
                        st.markdown(
                            f"<div style='font-size:1rem;font-weight:800;margin-bottom:2px'>"
                            f"{ticker} {direction} {other}</div>"
                            f"<div style='font-size:0.78rem;color:var(--txt2);margin-bottom:8px'>"
                            f"{other_info.get('name', other)} &nbsp;"
                            f"<span style='font-size:0.7rem;background:{other_color}22;"
                            f"color:{other_color};border:1px solid {other_color}44;"
                            f"border-radius:3px;padding:1px 5px'>{other_sector}</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(f"**{e['desc']}**")
                        m1c, m2c = st.columns(2)
                        m1c.metric("Deal Value", e.get("value", "N/A"))
                        m2c.metric("Established", e.get("year", "—"))
                        with st.expander("Full Details", expanded=False):
                            st.markdown(e.get("details", "No additional details."))
                        if st.button(f"View {other}", key=f"net_goto_{other}_{e['src']}_{e['dst']}",
                                     use_container_width=True):
                            st.session_state["net_click_type"] = "node"
                            st.session_state["net_selected"] = other
                            st.rerun()


def _render_edge_panel(src: str, dst: str) -> None:
    """Structured panel for a clicked edge — shows the specific deal between two companies."""
    e = _EDGE_LOOKUP.get((src, dst)) or _EDGE_LOOKUP.get((dst, src))
    if not e:
        st.warning(f"No deal data found for {src} ↔ {dst}.")
        return

    src_info = _NETWORK_COMPANIES.get(e["src"], {})
    dst_info = _NETWORK_COMPANIES.get(e["dst"], {})
    rel_color = _REL_COLORS.get(e["type"], "#888")
    src_color = _SECTOR_COLORS.get(src_info.get("sector", ""), "#888")
    dst_color = _SECTOR_COLORS.get(dst_info.get("sector", ""), "#888")

    with st.container(border=True):
        # Header row
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:12px;margin-bottom:10px'>"
            f"<span style='font-size:1.4rem;font-weight:900'>{e['src']}</span>"
            f"<span style='font-size:1rem;color:{rel_color};font-weight:700'>↔</span>"
            f"<span style='font-size:1.4rem;font-weight:900'>{e['dst']}</span>"
            f"<span style='font-size:0.72rem;font-weight:800;text-transform:uppercase;"
            f"letter-spacing:0.1em;background:{rel_color}22;color:{rel_color};"
            f"border:1px solid {rel_color}55;border-radius:4px;padding:2px 10px'>"
            f"{e['type']}</span>"
            f"</div>"
            f"<div style='font-size:0.82rem;color:var(--txt2);margin-bottom:6px'>"
            f"<span style='background:{src_color}22;color:{src_color};"
            f"border:1px solid {src_color}44;border-radius:3px;padding:1px 6px;margin-right:6px'>"
            f"{src_info.get('name', e['src'])} · {src_info.get('sector','')}</span>"
            f"<span style='background:{dst_color}22;color:{dst_color};"
            f"border:1px solid {dst_color}44;border-radius:3px;padding:1px 6px'>"
            f"{dst_info.get('name', e['dst'])} · {dst_info.get('sector','')}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(f"### {e['desc']}")

        c1, c2 = st.columns(2)
        c1.metric("Deal Value", e.get("value", "N/A"))
        c2.metric("Established", e.get("year", "—"))

        st.markdown("**Deal Details**")
        st.markdown(e.get("details", "No additional details available."))

        st.divider()
        b1, b2, b3 = st.columns([2, 2, 1])
        with b1:
            if st.button(f"📈 View {e['src']} Stock Profile", key="net_edge_view_src",
                         use_container_width=True):
                st.session_state["net_detail_ticker"] = e["src"]
                st.rerun()
        with b2:
            if st.button(f"📈 View {e['dst']} Stock Profile", key="net_edge_view_dst",
                         use_container_width=True):
                st.session_state["net_detail_ticker"] = e["dst"]
                st.rerun()
        with b3:
            if st.button("✕ Close", key="net_edge_close", use_container_width=True):
                st.session_state.pop("net_click_type", None)
                st.session_state.pop("net_edge_sel", None)
                st.rerun()


def render_network_page() -> None:
    st.title("🕸 Corporate Network")
    st.caption(
        "Interactive corporate relationship graph · nodes sized by market cap · colored by sector · "
        "**click a node** to see all its relationships · "
        "**click a diamond ◆ on an edge** to see that specific deal"
    )

    # ── Controls ──────────────────────────────────────────────────────────────
    ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 1])
    all_rel_types = list(_REL_COLORS.keys())
    all_sectors   = sorted({v["sector"] for v in _NETWORK_COMPANIES.values()})

    with ctrl1:
        rel_filter = st.multiselect(
            "Relationship types", all_rel_types, default=all_rel_types, key="net_rel_filter",
        )
    with ctrl2:
        sector_filter_list = st.multiselect(
            "Sectors", all_sectors, default=[], key="net_sector_filter",
            placeholder="All sectors",
        )
    with ctrl3:
        st.write(" ")
        if st.button("✕ Clear", key="net_clear", use_container_width=True):
            for k in ("net_click_type", "net_selected", "net_edge_sel", "net_detail_ticker"):
                st.session_state.pop(k, None)
            st.rerun()

    # Company dropdown
    ticker_opts = ["— (none)"] + sorted(_NETWORK_COMPANIES.keys())
    current_sel = st.session_state.get("net_selected") \
                  if st.session_state.get("net_click_type") == "node" else None
    dropdown_idx = ticker_opts.index(current_sel) if current_sel in ticker_opts else 0
    chosen = st.selectbox(
        "Jump to company",
        ticker_opts, index=dropdown_idx, key="net_company_dropdown",
        format_func=lambda t: (
            f"{t} — {_NETWORK_COMPANIES[t]['name']}" if t in _NETWORK_COMPANIES else t
        ),
    )
    if chosen and chosen != "— (none)":
        if chosen != st.session_state.get("net_selected") or \
                st.session_state.get("net_click_type") != "node":
            st.session_state["net_click_type"] = "node"
            st.session_state["net_selected"] = chosen
            st.session_state.pop("net_edge_sel", None)
            st.rerun()

    rel_types     = set(rel_filter) if rel_filter else set(all_rel_types)
    sector_filter = set(sector_filter_list) if sector_filter_list else {"All"}
    click_type    = st.session_state.get("net_click_type")
    net_selected  = st.session_state.get("net_selected")
    net_edge_sel  = st.session_state.get("net_edge_sel")  # (src, dst)

    # Compute highlighted nodes for dimming
    highlighted_nodes: set[str] | None = None
    highlighted_edge: tuple[str, str] | None = None
    if click_type == "node" and net_selected:
        neighbors = {
            (e["dst"] if e["src"] == net_selected else e["src"])
            for e in _NETWORK_EDGES
            if (e["src"] == net_selected or e["dst"] == net_selected)
            and e["type"] in rel_types
        }
        highlighted_nodes = neighbors | {net_selected}
    elif click_type == "edge" and net_edge_sel:
        highlighted_edge = net_edge_sel
        highlighted_nodes = set(net_edge_sel)

    # ── Graph ─────────────────────────────────────────────────────────────────
    pos = _build_network_layout()
    fig = _build_network_figure(pos, highlighted_nodes, highlighted_edge, rel_types, sector_filter)

    event = st.plotly_chart(
        fig, use_container_width=True, key="network_graph", on_select="rerun",
        config=dict(scrollZoom=True, displayModeBar=True,
                    modeBarButtonsToRemove=["lasso2d", "select2d"]),
    )

    # Handle clicks
    if event and event.selection:
        for pt in event.selection.get("points", []):
            cd = pt.get("customdata")
            if not cd or len(cd) < 2:
                continue
            if cd[0] == "node" and str(cd[1]) in _NETWORK_COMPANIES:
                st.session_state["net_click_type"] = "node"
                st.session_state["net_selected"] = str(cd[1])
                st.session_state.pop("net_edge_sel", None)
                st.rerun()
            elif cd[0] == "edge" and len(cd) >= 3:
                st.session_state["net_click_type"] = "edge"
                st.session_state["net_edge_sel"] = (str(cd[1]), str(cd[2]))
                st.session_state.pop("net_selected", None)
                st.rerun()

    # ── Stats strip ───────────────────────────────────────────────────────────
    active_edge_count = sum(
        1 for e in _NETWORK_EDGES
        if e["type"] in rel_types and (
            "All" in sector_filter or
            _NETWORK_COMPANIES.get(e["src"], {}).get("sector", "") in sector_filter or
            _NETWORK_COMPANIES.get(e["dst"], {}).get("sector", "") in sector_filter
        )
    )
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Companies", len(_NETWORK_COMPANIES))
    m2.metric("Connections", active_edge_count)
    m3.metric("Rel. types shown", len(rel_types))
    if click_type == "node" and net_selected and net_selected in _NETWORK_COMPANIES:
        cnt = sum(1 for e in _NETWORK_EDGES
                  if (e["src"] == net_selected or e["dst"] == net_selected)
                  and e["type"] in rel_types)
        m4.metric(f"{net_selected} relationships", cnt)
    elif click_type == "edge" and net_edge_sel:
        m4.metric("Selected edge", f"{net_edge_sel[0]} ↔ {net_edge_sel[1]}")
    else:
        m4.metric("Click a node or ◆", "to see details")

    st.divider()

    # ── Detail panel ──────────────────────────────────────────────────────────
    if click_type == "node" and net_selected and net_selected in _NETWORK_COMPANIES:
        _render_node_panel(net_selected, rel_types)
    elif click_type == "edge" and net_edge_sel:
        _render_edge_panel(net_edge_sel[0], net_edge_sel[1])

    # ── Stock profile panel (opened via button inside node/edge panels) ────────
    detail_ticker = st.session_state.get("net_detail_ticker")
    if detail_ticker:
        st.divider()
        hdr_c, clr_c = st.columns([6, 1])
        hdr_c.markdown(f"**Stock Profile: {detail_ticker}**")
        with clr_c:
            if st.button("✕ Close", key="net_close_stock"):
                st.session_state.pop("net_detail_ticker", None)
                st.rerun()
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
            ["📈 Equities", "🛢 Commodities", "₿ Crypto", "📊 ETFs", "🕸 Network"],
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
    elif nav_page == "📊 ETFs":
        render_etf_page()
    else:
        render_network_page()


if __name__ == "__main__":
    main()
