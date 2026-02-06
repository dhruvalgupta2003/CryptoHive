"""DeFi tools wrapping CoinGecko GeckoTerminal pool/category data."""

import requests
from crewai.tools import tool

_GT_BASE = "https://api.geckoterminal.com/api/v2"


def _gt_get(path: str, params: dict | None = None) -> dict:
    resp = requests.get(f"{_GT_BASE}{path}", params=params or {}, timeout=15)
    resp.raise_for_status()
    return resp.json()


@tool("get_trending_pools")
def get_trending_pools(network: str = "eth") -> str:
    """Get trending DEX pools on a network. network: eth, bsc, solana, etc."""
    try:
        data = _gt_get(f"/networks/{network}/trending_pools")
        pools = data.get("data", [])
        lines = [f"Trending pools on {network}:"]
        for p in pools[:10]:
            attrs = p.get("attributes", {})
            lines.append(
                f"  {attrs.get('name', '?')} | "
                f"24h Vol: ${attrs.get('volume_usd', {}).get('h24', 'N/A')} | "
                f"Liquidity: ${attrs.get('reserve_in_usd', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Trending pools unavailable: {e}"


@tool("get_new_pools")
def get_new_pools(network: str = "eth") -> str:
    """Get newly created pools on a network for early opportunity detection."""
    try:
        data = _gt_get(f"/networks/{network}/new_pools")
        pools = data.get("data", [])
        lines = [f"New pools on {network}:"]
        for p in pools[:10]:
            attrs = p.get("attributes", {})
            lines.append(
                f"  {attrs.get('name', '?')} | "
                f"Created: {attrs.get('pool_created_at', 'N/A')} | "
                f"Liquidity: ${attrs.get('reserve_in_usd', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"New pools unavailable: {e}"


@tool("search_pools")
def search_pools(query: str) -> str:
    """Search for DEX pools by token name or symbol."""
    try:
        data = _gt_get("/search/pools", {"query": query, "page": "1"})
        pools = data.get("data", [])
        lines = [f"Pool search results for '{query}':"]
        for p in pools[:10]:
            attrs = p.get("attributes", {})
            lines.append(
                f"  {attrs.get('name', '?')} on {attrs.get('network', {}).get('name', '?')} | "
                f"Liquidity: ${attrs.get('reserve_in_usd', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Pool search failed: {e}"
