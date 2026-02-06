"""Market data tools wrapping CoinGecko API."""

import os
import requests
from crewai.tools import tool

_BASE = "https://api.coingecko.com/api/v3"
_PRO_BASE = "https://pro-api.coingecko.com/api/v3"


def _headers() -> dict:
    key = os.getenv("COINGECKO_API_KEY", "")
    if key:
        return {"x-cg-pro-api-key": key}
    return {}


def _base() -> str:
    return _PRO_BASE if os.getenv("COINGECKO_API_KEY") else _BASE


def _get(path: str, params: dict | None = None) -> dict | list:
    resp = requests.get(f"{_base()}{path}", headers=_headers(), params=params or {}, timeout=15)
    resp.raise_for_status()
    return resp.json()


@tool("get_crypto_price")
def get_crypto_price(coin_ids: str, vs_currencies: str = "usd") -> str:
    """Get spot price, 24h change, market cap, and volume for one or more coins.
    coin_ids: comma-separated CoinGecko IDs (e.g. 'bitcoin,ethereum').
    vs_currencies: comma-separated fiat (default 'usd')."""
    data = _get("/simple/price", {
        "ids": coin_ids,
        "vs_currencies": vs_currencies,
        "include_24hr_change": "true",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
    })
    lines = []
    for cid, info in data.items():
        for cur in vs_currencies.split(","):
            cur = cur.strip()
            lines.append(
                f"{cid}: price=${info.get(cur, 'N/A')}, "
                f"24h_change={info.get(f'{cur}_24h_change', 'N/A')}%, "
                f"market_cap=${info.get(f'{cur}_market_cap', 'N/A')}, "
                f"volume=${info.get(f'{cur}_24h_vol', 'N/A')}"
            )
    return "\n".join(lines) if lines else str(data)


@tool("get_market_data")
def get_market_data(vs_currency: str = "usd", per_page: int = 10, order: str = "market_cap_desc") -> str:
    """Get full market data for top coins sorted by market cap, volume, etc.
    order options: market_cap_desc, volume_desc, id_asc."""
    data = _get("/coins/markets", {
        "vs_currency": vs_currency,
        "order": order,
        "per_page": per_page,
        "page": 1,
        "sparkline": "false",
    })
    lines = []
    for c in data:
        lines.append(
            f"{c['symbol'].upper()}: ${c.get('current_price', 'N/A')} | "
            f"MCap: ${c.get('market_cap', 'N/A')} | "
            f"Vol: ${c.get('total_volume', 'N/A')} | "
            f"24h: {c.get('price_change_percentage_24h', 'N/A')}%"
        )
    return "\n".join(lines) if lines else str(data)


@tool("get_top_movers")
def get_top_movers(vs_currency: str = "usd") -> str:
    """Get top gainers and losers in the last 24h."""
    try:
        data = _get("/coins/top_gainers_losers", {"vs_currency": vs_currency})
        lines = ["TOP GAINERS:"]
        for c in data.get("top_gainers", [])[:5]:
            lines.append(f"  {c.get('symbol', '?').upper()}: {c.get('usd_24h_change', 'N/A')}%")
        lines.append("TOP LOSERS:")
        for c in data.get("top_losers", [])[:5]:
            lines.append(f"  {c.get('symbol', '?').upper()}: {c.get('usd_24h_change', 'N/A')}%")
        return "\n".join(lines)
    except Exception as e:
        return f"Top movers endpoint unavailable (may require paid plan): {e}"


@tool("get_ohlcv")
def get_ohlcv(coin_id: str, vs_currency: str = "usd", days: str = "7") -> str:
    """Get OHLCV candlestick data for a coin. days: 1, 7, 14, 30, 90, 180, 365."""
    data = _get(f"/coins/{coin_id}/ohlc", {
        "vs_currency": vs_currency,
        "days": days,
    })
    if not data:
        return "No OHLCV data available."
    first = data[0]
    last = data[-1]
    highs = [c[2] for c in data]
    lows = [c[3] for c in data]
    return (
        f"OHLCV for {coin_id} ({days}d):\n"
        f"  Period high: ${max(highs)}\n"
        f"  Period low: ${min(lows)}\n"
        f"  Open: ${first[1]} → Close: ${last[4]}\n"
        f"  Data points: {len(data)}"
    )


@tool("get_coin_details")
def get_coin_details(coin_id: str) -> str:
    """Get full metadata and market data for a single coin by CoinGecko ID."""
    data = _get(f"/coins/{coin_id}", {
        "localization": "false",
        "tickers": "false",
        "community_data": "true",
        "developer_data": "false",
    })
    md = data.get("market_data", {})
    return (
        f"Name: {data.get('name')} ({data.get('symbol', '').upper()})\n"
        f"Price: ${md.get('current_price', {}).get('usd', 'N/A')}\n"
        f"ATH: ${md.get('ath', {}).get('usd', 'N/A')}\n"
        f"ATL: ${md.get('atl', {}).get('usd', 'N/A')}\n"
        f"Market Cap Rank: {data.get('market_cap_rank', 'N/A')}\n"
        f"24h Change: {md.get('price_change_percentage_24h', 'N/A')}%\n"
        f"7d Change: {md.get('price_change_percentage_7d', 'N/A')}%\n"
        f"30d Change: {md.get('price_change_percentage_30d', 'N/A')}%\n"
        f"Total Supply: {md.get('total_supply', 'N/A')}\n"
        f"Circulating Supply: {md.get('circulating_supply', 'N/A')}\n"
        f"Description: {(data.get('description', {}).get('en', '') or '')[:300]}"
    )
