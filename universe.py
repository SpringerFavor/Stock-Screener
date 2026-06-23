"""Index-constituent loaders for the stock screener.

Every index loads automatically from a reputable primary source — ETF-issuer
holdings files (State Street SPDR, Vanguard) or the index owner's own API — with
an independent fallback issuer so a single provider outage can't break a load.
No Wikipedia, no manual uploads.

  * S&P 500          — SPDR SPY (State Street)  → Vanguard VOO
  * S&P MidCap 400   — SPDR MDY (State Street)  → Vanguard IVOO
  * Russell Midcap   — iShares IWR
  * NASDAQ-100       — Nasdaq official API (api.nasdaq.com) → Invesco QQQ
  * Russell 2000     — Vanguard VTWO            → iShares IWM

Each loader returns a sorted list of yfinance-style tickers (dots normalised to
dashes, e.g. ``BRK.B`` -> ``BRK-B``). Loaders raise :class:`UniverseError`
with an actionable message when every source for an index is unreachable, so
the UI can surface the problem instead of silently returning an empty list.
"""

from __future__ import annotations

import io

import pandas as pd
import requests

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "*/*",
}

# State Street SPDR daily-holdings files (.xlsx). Same URL pattern for any SPDR.
_SSGA_HOLDINGS = (
    "https://www.ssga.com/us/en/intermediary/etfs/library-content/products/"
    "fund-data/etfs/us/holdings-daily-us-en-{etf}.xlsx"
)
# Vanguard investor-site holdings proxy (paginated JSON, 500 rows/page).
_VANGUARD_HOLDINGS = (
    "https://investor.vanguard.com/investment-products/etfs/profile/api/"
    "{etf}/portfolio-holding/stock"
)
# Nasdaq's own index-membership API.
_NASDAQ_LIST = "https://api.nasdaq.com/api/quote/list-type/{list_type}"
# Invesco ETF daily holdings CSV (QQQ = NASDAQ-100) — NASDAQ-100 fallback.
_INVESCO_HOLDINGS = (
    "https://www.invesco.com/us/financial-products/etfs/holdings/main/holdings/0"
    "?audienceType=Investor&action=download&ticker={etf}"
)
# iShares full-holdings CSVs, keyed by ETF ticker -> (product id, URL slug).
# IWM = Russell 2000, IWR = Russell Mid-Cap. The numeric download token after
# the slug is shared across iShares products.
_ISHARES_PRODUCTS = {
    "IWM": ("239710", "ishares-russell-2000-etf"),
    "IWR": ("239717", "ishares-russell-mid-cap-etf"),
}


class UniverseError(RuntimeError):
    """Raised when an index's constituents cannot be fetched from any source."""


def _normalise(symbol) -> str | None:
    """Convert a raw symbol to a yfinance ticker, or None if not equity-like."""
    if symbol is None:
        return None
    sym = str(symbol).strip().upper()
    if not sym or sym in {"--", "-", "N/A", "NAN", "CASH", "USD"}:
        return None
    sym = sym.replace(".", "-")
    if not all(c.isalnum() or c == "-" for c in sym):
        return None
    return sym


def _clean(symbols) -> list[str]:
    return sorted({s for s in (_normalise(x) for x in symbols) if s})


def _get(url: str, *, timeout: int = 40, headers: dict | None = None) -> requests.Response:
    resp = requests.get(url, headers=headers or _HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp


# --------------------------------------------------------------------------
# Reusable per-issuer fetchers
# --------------------------------------------------------------------------

def _ssga_holdings(etf: str) -> list[str]:
    """Parse a State Street SPDR daily-holdings .xlsx into a ticker list."""
    resp = _get(_SSGA_HOLDINGS.format(etf=etf.lower()))
    if not resp.content[:2] == b"PK":  # .xlsx is a zip; HTML error page is not
        raise UniverseError(f"SPDR {etf.upper()}: expected an .xlsx file, got something else.")
    raw = pd.read_excel(io.BytesIO(resp.content), header=None)
    # The holdings table starts at the row whose first cell is "Name".
    header_rows = raw.index[raw.iloc[:, 0].astype(str).str.strip() == "Name"]
    if len(header_rows) == 0:
        raise UniverseError(f"SPDR {etf.upper()}: unexpected file layout (no 'Name' header).")
    h = header_rows[0]
    table = raw.iloc[h + 1 :].copy()
    table.columns = raw.iloc[h]
    if "Ticker" not in table.columns:
        raise UniverseError(f"SPDR {etf.upper()}: no 'Ticker' column found.")
    tickers = _clean(table["Ticker"])
    if not tickers:
        raise UniverseError(f"SPDR {etf.upper()}: parsed file but found no tickers.")
    return tickers


def _vanguard_holdings(etf: str) -> list[str]:
    """Page through Vanguard's holdings API for an ETF and return its tickers."""
    headers = {**_HEADERS, "Accept": "application/json", "Referer": "https://investor.vanguard.com/"}
    base = _VANGUARD_HOLDINGS.format(etf=etf.upper())
    out: set[str] = set()
    start, size, guard = 1, None, 0
    while guard < 50:  # hard stop; ~4 pages for the Russell 2000
        guard += 1
        data = _get(f"{base}?start={start}&count=500", headers=headers).json()
        size = data.get("size") or size
        entities = (data.get("fund") or {}).get("entity") or []
        if not entities:
            break
        for e in entities:
            norm = _normalise(e.get("ticker"))
            if norm:
                out.add(norm)
        start += 500
        if size and start > size:
            break
    if not out:
        raise UniverseError(f"Vanguard {etf.upper()}: holdings API returned no tickers.")
    return sorted(out)


def _nasdaq_index(list_type: str) -> list[str]:
    """Fetch an index's membership from Nasdaq's official API."""
    headers = {**_HEADERS, "Accept": "application/json", "Referer": "https://www.nasdaq.com/"}
    data = _get(_NASDAQ_LIST.format(list_type=list_type), headers=headers).json()
    rows = ((data.get("data") or {}).get("data") or {}).get("rows") or []
    tickers = _clean(r.get("symbol") for r in rows)
    if not tickers:
        raise UniverseError(f"Nasdaq API ({list_type}): returned no tickers.")
    return tickers


def _invesco_holdings(etf: str) -> list[str]:
    """Parse an Invesco ETF daily-holdings CSV (e.g. QQQ for the NASDAQ-100).

    Invesco bot-blocks some networks (notably datacenter/VPN IPs), serving an
    HTML page instead of the CSV; we detect that and raise so the caller can
    fall back. Works from a normal connection.
    """
    resp = _get(
        _INVESCO_HOLDINGS.format(etf=etf.upper()),
        headers={**_HEADERS, "Referer": "https://www.invesco.com/", "Accept": "text/csv,*/*"},
    )
    text = resp.text
    if text.lstrip()[:1] in ("<",) or "<!doctype" in text[:200].lower():
        raise UniverseError(f"Invesco {etf.upper()}: bot-protection page instead of CSV.")
    df = pd.read_csv(io.StringIO(text))
    # Invesco labels the constituent symbol "Holding Ticker"; be tolerant of
    # minor header variations.
    col = next(
        (c for c in df.columns if str(c).strip().lower() in ("holding ticker", "ticker", "holdingticker")),
        None,
    )
    if col is None:
        raise UniverseError(f"Invesco {etf.upper()}: no ticker column found.")
    tickers = _clean(df[col])
    if not tickers:
        raise UniverseError(f"Invesco {etf.upper()}: parsed CSV but found no tickers.")
    return tickers


def _ishares_holdings(etf: str) -> list[str]:
    """Parse an iShares ETF full-holdings CSV (e.g. IWM, IWR) into tickers.

    iShares bot-blocks some networks (notably datacenter/VPN IPs), serving an
    HTML page instead of the CSV; we detect that and raise. Loads from a normal
    (residential) connection.
    """
    product_id, slug = _ISHARES_PRODUCTS[etf.upper()]
    url = (
        f"https://www.ishares.com/us/products/{product_id}/{slug}/"
        f"1467271812596.ajax?fileType=csv&fileName={etf.upper()}_holdings&dataType=fund"
    )
    text = _get(url).text
    if text.lstrip().lower().startswith(("<!doctype", "<html")):
        raise UniverseError(
            f"iShares returned a bot-protection page instead of the {etf.upper()} "
            "holdings CSV (happens on datacenter/VPN IPs; loads on a normal connection)."
        )
    lines = text.splitlines()
    header_idx = next(
        (i for i, ln in enumerate(lines) if ln.replace('"', "").strip().startswith("Ticker,")),
        None,
    )
    if header_idx is None:
        raise UniverseError(f"iShares {etf.upper()} CSV: no 'Ticker' header row found.")
    df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])))
    if "Asset Class" in df.columns:
        df = df[df["Asset Class"].astype(str).str.strip().str.lower() == "equity"]
    tickers = _clean(df["Ticker"])
    if not tickers:
        raise UniverseError(f"iShares {etf.upper()} CSV parsed but contained no equity tickers.")
    return tickers


def _first_working(index_name: str, sources: list) -> list[str]:
    """Try each ``(label, fn)`` source in order; return the first that succeeds."""
    problems = []
    for label, fn in sources:
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 — try the next source
            problems.append(f"{label}: {exc}")
    raise UniverseError(
        f"{index_name} could not be loaded from any source — " + " | ".join(problems)
    )


# --------------------------------------------------------------------------
# Per-index loaders (primary issuer → independent fallback)
# --------------------------------------------------------------------------

def get_sp500() -> list[str]:
    return _first_working(
        "S&P 500",
        [("SPDR SPY", lambda: _ssga_holdings("SPY")),
         ("Vanguard VOO", lambda: _vanguard_holdings("VOO"))],
    )


def get_sp400() -> list[str]:
    return _first_working(
        "S&P MidCap 400",
        [("SPDR MDY", lambda: _ssga_holdings("MDY")),
         ("Vanguard IVOO", lambda: _vanguard_holdings("IVOO"))],
    )


def get_nasdaq100() -> list[str]:
    return _first_working(
        "NASDAQ-100",
        [("Nasdaq API", lambda: _nasdaq_index("nasdaq100")),
         ("Invesco QQQ", lambda: _invesco_holdings("QQQ"))],
    )


def get_russell_midcap() -> list[str]:
    return _first_working(
        "Russell Midcap",
        [("iShares IWR", lambda: _ishares_holdings("IWR"))],
    )


def get_russell2000() -> list[str]:
    return _first_working(
        "Russell 2000",
        [("Vanguard VTWO", lambda: _vanguard_holdings("VTWO")),
         ("iShares IWM", lambda: _ishares_holdings("IWM"))],
    )


# --------------------------------------------------------------------------
# Combined universe
# --------------------------------------------------------------------------

_LOADERS = {
    "S&P 500": get_sp500,
    "S&P MidCap 400": get_sp400,
    "Russell Midcap": get_russell_midcap,
    "NASDAQ-100": get_nasdaq100,
    "Russell 2000": get_russell2000,
}

INDEX_NAMES = list(_LOADERS)


def build_universe(indexes: list[str]) -> tuple[list[str], dict[str, int], dict[str, str]]:
    """Load and union the requested indexes.

    Returns ``(tickers, counts, errors)`` where ``counts`` maps each index that
    loaded to its ticker count and ``errors`` maps each index that failed to its
    error message. The combined ``tickers`` list is de-duplicated and sorted.
    """
    union: set[str] = set()
    counts: dict[str, int] = {}
    errors: dict[str, str] = {}
    for name in indexes:
        loader = _LOADERS.get(name)
        if loader is None:
            errors[name] = "unknown index"
            continue
        try:
            syms = loader()
            counts[name] = len(syms)
            union.update(syms)
        except Exception as exc:  # noqa: BLE001 — report per-index, keep going
            errors[name] = str(exc)
    return sorted(union), counts, errors
