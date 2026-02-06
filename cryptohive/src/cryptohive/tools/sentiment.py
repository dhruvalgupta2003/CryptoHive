"""Sentiment tools using SerperDev search, CoinGecko trending, and Fear & Greed."""

import os
import requests
from crewai.tools import tool

_CG_BASE = "https://api.coingecko.com/api/v3"
_CG_PRO_BASE = "https://pro-api.coingecko.com/api/v3"


def _cg_base() -> str:
    return _CG_PRO_BASE if os.getenv("COINGECKO_API_KEY") else _CG_BASE


def _cg_headers() -> dict:
    key = os.getenv("COINGECKO_API_KEY", "")
    return {"x-cg-pro-api-key": key} if key else {}


@tool("search_crypto_news")
def search_crypto_news(query: str) -> str:
    """Search the web for crypto news and sentiment using SerperDev.
    query: search query like 'Bitcoin sentiment Twitter today'."""
    api_key = os.getenv("SERPER_API_KEY", "")
    if not api_key:
        return "SERPER_API_KEY not set — cannot search web."
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": 8},
            timeout=15,
        )
        resp.raise_for_status()
        results = resp.json()
        lines = []
        for item in results.get("organic", [])[:8]:
            lines.append(f"• {item.get('title', '')} — {item.get('snippet', '')}")
        return "\n".join(lines) if lines else "No results found."
    except Exception as e:
        return f"Web search failed: {e}"


@tool("get_trending")
def get_trending() -> str:
    """Get trending coins, NFTs, and categories from CoinGecko."""
    try:
        resp = requests.get(
            f"{_cg_base()}/search/trending",
            headers=_cg_headers(),
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        lines = ["TRENDING COINS:"]
        for c in data.get("coins", [])[:10]:
            item = c.get("item", {})
            lines.append(
                f"  #{item.get('market_cap_rank', '?')} {item.get('name', '?')} "
                f"({item.get('symbol', '?')}) — score: {item.get('score', 'N/A')}"
            )
        lines.append("TRENDING CATEGORIES:")
        for cat in data.get("categories", [])[:5]:
            lines.append(f"  {cat.get('name', '?')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Trending data unavailable: {e}"


@tool("get_fear_greed")
def get_fear_greed() -> str:
    """Get the current Crypto Fear & Greed Index from Alternative.me."""
    try:
        resp = requests.get(
            "https://api.alternative.me/fng/?limit=1&format=json",
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        entry = data.get("data", [{}])[0]
        return (
            f"Fear & Greed Index: {entry.get('value', 'N/A')} "
            f"({entry.get('value_classification', 'N/A')}) "
            f"— updated {entry.get('timestamp', 'N/A')}"
        )
    except Exception as e:
        return f"Fear & Greed unavailable: {e}"
