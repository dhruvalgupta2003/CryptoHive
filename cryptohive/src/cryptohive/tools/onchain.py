"""On-chain tools wrapping CoinGecko GeckoTerminal + CryptoHive DexTools."""

import os
import requests
from crewai.tools import tool

_GT_BASE = "https://api.geckoterminal.com/api/v2"
_CRYPTOHIVE_BASE = os.getenv("CRYPTOHIVE_API_BASE", "")


def _gt_get(path: str, params: dict | None = None) -> dict:
    resp = requests.get(f"{_GT_BASE}{path}", params=params or {}, timeout=15)
    resp.raise_for_status()
    return resp.json()


@tool("get_top_holders")
def get_top_holders(network: str, token_address: str) -> str:
    """Get top token holders for whale concentration analysis.
    network: e.g. 'eth', 'bsc', 'solana'. token_address: contract address."""
    try:
        data = _gt_get(f"/networks/{network}/tokens/{token_address}/top_holders")
        holders = data.get("data", [])
        lines = [f"Top holders for {token_address} on {network}:"]
        for h in holders[:10]:
            attrs = h.get("attributes", {})
            lines.append(
                f"  {attrs.get('address', '?')[:10]}...: "
                f"{attrs.get('percentage', 'N/A')}% "
                f"(${attrs.get('value_usd', 'N/A')})"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Top holders unavailable: {e}"


@tool("get_recent_trades")
def get_recent_trades(network: str, token_address: str) -> str:
    """Get recent trades for a token to spot large transactions.
    network: e.g. 'eth', 'bsc'. token_address: contract address."""
    try:
        data = _gt_get(f"/networks/{network}/tokens/{token_address}/trades")
        trades = data.get("data", [])
        lines = [f"Recent trades for {token_address} on {network}:"]
        for t in trades[:10]:
            attrs = t.get("attributes", {})
            lines.append(
                f"  {attrs.get('kind', '?')} | "
                f"${attrs.get('volume_in_usd', 'N/A')} | "
                f"{attrs.get('block_timestamp', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Recent trades unavailable: {e}"


@tool("get_top_traders")
def get_top_traders(network: str, token_address: str) -> str:
    """Get top PnL traders for a token.
    network: e.g. 'eth', 'bsc'. token_address: contract address."""
    try:
        data = _gt_get(f"/networks/{network}/tokens/{token_address}/top_traders")
        traders = data.get("data", [])
        lines = [f"Top traders for {token_address} on {network}:"]
        for t in traders[:10]:
            attrs = t.get("attributes", {})
            lines.append(
                f"  {attrs.get('address', '?')[:10]}...: "
                f"PnL ${attrs.get('pnl_usd', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Top traders unavailable: {e}"


@tool("get_token_pools")
def get_token_pools(network: str, token_address: str) -> str:
    """Get DEX liquidity pools for a token.
    network: e.g. 'eth', 'bsc'. token_address: contract address."""
    try:
        data = _gt_get(f"/networks/{network}/tokens/{token_address}/pools", {"page": "1"})
        pools = data.get("data", [])
        lines = [f"Pools for {token_address} on {network}:"]
        for p in pools[:5]:
            attrs = p.get("attributes", {})
            lines.append(
                f"  {attrs.get('name', '?')} | "
                f"Liquidity: ${attrs.get('reserve_in_usd', 'N/A')} | "
                f"24h Vol: ${attrs.get('volume_usd', {}).get('h24', 'N/A')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Token pools unavailable: {e}"


@tool("get_dextools_analysis")
def get_dextools_analysis(bsc_token_address: str) -> str:
    """Get comprehensive DexTools analysis for a BSC token including security audit,
    score, price, and pool info. Only works for BSC/BNB Chain tokens."""
    try:
        resp = requests.post(
            f"{_CRYPTOHIVE_BASE}/mcp/getDexToolsTokenAnalysis",
            json={"address": bsc_token_address},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        return f"DexTools analysis for {bsc_token_address}:\n{str(data)[:2000]}"
    except Exception as e:
        return f"DexTools analysis unavailable: {e}"
