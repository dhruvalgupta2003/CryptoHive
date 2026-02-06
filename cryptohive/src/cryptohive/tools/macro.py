"""Macro tools wrapping CoinGecko global and market data."""

import os
import requests
from crewai.tools import tool

_CG_BASE = "https://api.coingecko.com/api/v3"
_CG_PRO_BASE = "https://pro-api.coingecko.com/api/v3"


def _base() -> str:
    return _CG_PRO_BASE if os.getenv("COINGECKO_API_KEY") else _CG_BASE


def _headers() -> dict:
    key = os.getenv("COINGECKO_API_KEY", "")
    return {"x-cg-pro-api-key": key} if key else {}


def _get(path: str, params: dict | None = None) -> dict | list:
    resp = requests.get(f"{_base()}{path}", headers=_headers(), params=params or {}, timeout=15)
    resp.raise_for_status()
    return resp.json()


@tool("get_global_data")
def get_global_data() -> str:
    """Get global crypto market data: total market cap, BTC dominance, 24h volume, active coins."""
    data = _get("/global")
    d = data.get("data", {})
    mcap = d.get("total_market_cap", {}).get("usd", "N/A")
    vol = d.get("total_volume", {}).get("usd", "N/A")
    btc_dom = d.get("market_cap_percentage", {}).get("btc", "N/A")
    eth_dom = d.get("market_cap_percentage", {}).get("eth", "N/A")
    mcap_change = d.get("market_cap_change_percentage_24h_usd", "N/A")
    return (
        f"Global Crypto Market:\n"
        f"  Total Market Cap: ${mcap}\n"
        f"  24h Volume: ${vol}\n"
        f"  BTC Dominance: {btc_dom}%\n"
        f"  ETH Dominance: {eth_dom}%\n"
        f"  Market Cap 24h Change: {mcap_change}%\n"
        f"  Active Cryptocurrencies: {d.get('active_cryptocurrencies', 'N/A')}"
    )


@tool("get_market_overview")
def get_market_overview() -> str:
    """Get market overview of BTC, ETH, and top 10 coins by market cap."""
    data = _get("/coins/markets", {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false",
    })
    lines = ["Market Overview (Top 10):"]
    for c in data:
        lines.append(
            f"  {c['symbol'].upper()}: ${c.get('current_price', 'N/A')} | "
            f"24h: {c.get('price_change_percentage_24h', 'N/A')}% | "
            f"MCap: ${c.get('market_cap', 'N/A')}"
        )
    return "\n".join(lines)
