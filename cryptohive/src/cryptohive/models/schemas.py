"""Pydantic models for state management and output formatting."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MarketSnapshot(BaseModel):
    asset: str = ""
    price: float | None = None
    volume_24h: float | None = None
    market_cap: float | None = None
    price_change_24h: float | None = None
    volatility_note: str = ""
    top_gainers: str = ""
    top_losers: str = ""
    ohlcv_summary: str = ""
    raw: str = ""


class OnChainSignals(BaseModel):
    whale_activity: str = ""
    top_holders_concentration: str = ""
    recent_large_trades: str = ""
    pool_liquidity: str = ""
    dextools_analysis: str = ""
    raw: str = ""


class SentimentData(BaseModel):
    overall_bias: str = ""
    dominant_narrative: str = ""
    momentum_shift: str = ""
    fear_greed_index: str = ""
    trending_coins: str = ""
    news_summary: str = ""
    raw: str = ""


class MacroContext(BaseModel):
    total_market_cap: str = ""
    btc_dominance: str = ""
    market_cap_change_24h: str = ""
    risk_regime: str = ""
    correlations: str = ""
    raw: str = ""


class AnalysisState(BaseModel):
    """Flow state passed between agents."""
    query: str = ""
    market: MarketSnapshot = Field(default_factory=MarketSnapshot)
    onchain: OnChainSignals = Field(default_factory=OnChainSignals)
    sentiment: SentimentData = Field(default_factory=SentimentData)
    macro: MacroContext = Field(default_factory=MacroContext)
    synthesis: str = ""
    confidence_score: int = 0
    data_sources: list[str] = Field(default_factory=list)


class FinalReport(BaseModel):
    market_snapshot: str = ""
    onchain_signals: str = ""
    sentiment: str = ""
    macro_context: str = ""
    synthesis: str = ""
    confidence_score: int = 0
    data_sources: list[str] = Field(default_factory=list)

    def format(self) -> str:
        sources = ", ".join(self.data_sources) if self.data_sources else "N/A"
        return (
            f"🔹 MARKET SNAPSHOT\n{self.market_snapshot}\n\n"
            f"🔹 ON-CHAIN SIGNALS\n{self.onchain_signals}\n\n"
            f"🔹 SENTIMENT\n{self.sentiment}\n\n"
            f"🔹 MACRO CONTEXT\n{self.macro_context}\n\n"
            f"🔹 SYNTHESIS\n{self.synthesis}\n\n"
            f"🔹 CONFIDENCE SCORE: {self.confidence_score} / 10\n\n"
            f"🔹 DATA SOURCES USED: [{sources}]"
        )
