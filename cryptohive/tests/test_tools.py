"""Smoke tests for CryptoHive tools."""

import os
import pytest


def test_imports():
    """All tool modules import without error."""
    from cryptohive.tools import market_data, onchain, sentiment, macro, defi


def test_schemas():
    """Pydantic models instantiate correctly."""
    from cryptohive.models.schemas import AnalysisState, FinalReport

    state = AnalysisState(query="test")
    assert state.query == "test"
    assert state.confidence_score == 0

    report = FinalReport(
        market_snapshot="test",
        confidence_score=7,
        data_sources=["CoinGecko"],
    )
    formatted = report.format()
    assert "MARKET SNAPSHOT" in formatted
    assert "7 / 10" in formatted
    assert "CoinGecko" in formatted


def test_crew_imports():
    """Crew module imports and loads config."""
    from cryptohive.crew import build_agents
    # Just test that config loads (don't build agents as it needs LLM)


def test_flow_import():
    """Flow module imports."""
    from cryptohive.flow import run_analysis


@pytest.mark.skipif(
    not os.getenv("COINGECKO_API_KEY"),
    reason="COINGECKO_API_KEY not set",
)
def test_fear_greed_live():
    """Live test: Fear & Greed index (free API, no key needed)."""
    from cryptohive.tools.sentiment import get_fear_greed
    result = get_fear_greed.run()
    assert "Fear & Greed" in result


@pytest.mark.skipif(
    not os.getenv("COINGECKO_API_KEY"),
    reason="Requires API key for reliable access",
)
def test_get_crypto_price_live():
    """Live test: get BTC price."""
    from cryptohive.tools.market_data import get_crypto_price
    result = get_crypto_price.run(coin_ids="bitcoin")
    assert "bitcoin" in result.lower()
