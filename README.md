# 📈 Stock Screener

A Streamlit stock screener built on `yfinance`. It pulls index constituents **automatically** and screens them against four adjustable criteria:

- Price **above its 50-day** moving average
- Price **above its 200-day** moving average
- **Revenue growth ≥ 20%** (adjustable)
- **P/E ratio < 30** (adjustable)

Each filter can be toggled on/off and its threshold tuned from the sidebar.

## Universe

Pick any combination of four indexes in the sidebar — tickers are fetched live, deduplicated, and unioned (`universe.py`). **Every index loads automatically from a reputable issuer/index-owner source, with an independent fallback. No Wikipedia, no manual uploads.**

| Index | Primary source | Fallback | Status |
|-------|----------------|----------|--------|
| **S&P 500** | State Street **SPDR SPY** holdings (.xlsx) | Vanguard **VOO** | ✅ ~504 |
| **S&P MidCap 400** | State Street **SPDR MDY** holdings (.xlsx) | Vanguard **IVOO** | ✅ ~400 |
| **Russell Midcap** | iShares **IWR** holdings CSV | — | ✅ auto¹ |
| **NASDAQ-100** | **Nasdaq** official API (`api.nasdaq.com`) | Invesco **QQQ** | ✅ ~101 |
| **Russell 2000** | Vanguard **VTWO** holdings API | iShares **IWM** | ✅ ~1,940 |

Sources are the actual fund issuers (State Street, Vanguard, BlackRock/iShares) and the index owner (Nasdaq) — authoritative primary data, refreshed daily by the providers.

¹ The Russell Midcap loads from the iShares IWR holdings file. Like iShares IWM (Russell 2000 fallback), this endpoint is bot-protected on datacenter/VPN IPs but loads automatically on a normal residential connection. There is no second issuer tracking the Russell Midcap, so it has no fallback; if blocked it shows a warning and the other indexes continue.

### Russell 2000 — bulletproofing

The Russell 2000 has ~2,000 members and reconstitutes annually, so there's no static list worth shipping. It now loads from **two independent issuers**: Vanguard's VTWO holdings API (primary) and the iShares IWM holdings CSV (fallback). Vanguard's endpoint is reachable from essentially any network (including datacenter/VPN IPs that bot-block iShares), so the load succeeds wherever you run it; if Vanguard ever hiccups, iShares covers it.

## Run

```bash
cd stock-screener
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501.

## How it works

The screen runs as a **funnel** so it scales to thousands of tickers without hammering Yahoo:

1. **Prices (batched).** Downloads 1y of daily closes in chunks of 150 via `yf.download` and computes the 50/200-day moving averages.
2. **MA prefilter.** Keeps only tickers passing the (enabled) moving-average filters.
3. **Fundamentals (survivors only).** Fetches `trailingPE` and `revenueGrowth` per surviving ticker, concurrently. This is the slow, rate-limited step — limiting it to MA survivors keeps runs fast.
4. **Valuation/growth filters** → final table, sortable, with CSV download.

A funnel summary (Screened → Priced → Passed MA → Final matches) shows where names dropped out.

### Scale & rate limits

The combined S&P 500 + S&P MidCap 400 + NASDAQ-100 + Russell 2000 universe is ~2,800 names. Yahoo throttles heavy use, so:

- A **Max tickers to screen** cap (default 500) bounds each run. Raise it to cover more.
- Index lists are cached 12h; prices and fundamentals are cached 30 min, so re-running with different thresholds is fast and avoids re-hitting the network.

## Notes

- Yahoo Finance is an unofficial, best-effort source. Tickers missing `P/E` or `revenueGrowth` fail any active filter that needs them.
- For research/education only — not investment advice.
