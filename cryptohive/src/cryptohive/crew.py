"""Crew definitions for CryptoHive."""

import os
from pathlib import Path

import yaml
from crewai import Agent, Crew, Task, Process, LLM

from cryptohive.tools.market_data import (
    get_crypto_price, get_market_data, get_top_movers, get_ohlcv, get_coin_details,
)
from cryptohive.tools.onchain import (
    get_top_holders, get_recent_trades, get_top_traders, get_token_pools, get_dextools_analysis,
)
from cryptohive.tools.sentiment import (
    search_crypto_news, get_trending, get_fear_greed,
)
from cryptohive.tools.macro import get_global_data, get_market_overview
from cryptohive.tools.defi import get_trending_pools, get_new_pools, search_pools

_CONFIG = Path(__file__).parent / "config"


def _load_yaml(name: str) -> dict:
    with open(_CONFIG / name) as f:
        return yaml.safe_load(f)


def _get_llm() -> LLM:
    """Build the LLM from environment. Supports ANTHROPIC_API_KEY or OPENAI_API_KEY."""
    if os.getenv("ANTHROPIC_API_KEY"):
        model = os.getenv("CREWAI_MODEL", "anthropic/claude-sonnet-4-5-20250929")
        return LLM(model=model, api_key=os.getenv("ANTHROPIC_API_KEY"))
    if os.getenv("OPENAI_API_KEY"):
        model = os.getenv("CREWAI_MODEL", "gpt-4o")
        return LLM(model=model, api_key=os.getenv("OPENAI_API_KEY"))
    raise RuntimeError("Set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env")


def build_agents() -> dict[str, Agent]:
    cfg = _load_yaml("agents.yaml")
    llm = _get_llm()

    market_data_agent = Agent(
        **cfg["market_data_agent"],
        tools=[get_crypto_price, get_market_data, get_top_movers, get_ohlcv, get_coin_details],
        llm=llm,
        verbose=True,
    )
    onchain_agent = Agent(
        **cfg["onchain_agent"],
        tools=[get_top_holders, get_recent_trades, get_top_traders, get_token_pools, get_dextools_analysis],
        llm=llm,
        verbose=True,
    )
    sentiment_agent = Agent(
        **cfg["sentiment_agent"],
        tools=[search_crypto_news, get_trending, get_fear_greed],
        llm=llm,
        verbose=True,
    )
    macro_agent = Agent(
        **cfg["macro_agent"],
        tools=[get_global_data, get_market_overview],
        llm=llm,
        verbose=True,
    )
    strategy_agent = Agent(
        **cfg["strategy_agent"],
        tools=[],
        llm=llm,
        verbose=True,
    )
    orchestrator = Agent(
        **cfg["orchestrator"],
        tools=[],
        llm=llm,
        verbose=True,
    )

    return {
        "orchestrator": orchestrator,
        "market_data": market_data_agent,
        "onchain": onchain_agent,
        "sentiment": sentiment_agent,
        "macro": macro_agent,
        "strategy": strategy_agent,
    }


def build_data_crew(query: str, agents: dict[str, Agent]) -> Crew:
    """Build the parallel data-gathering crew (market, onchain, sentiment, macro)."""
    cfg = _load_yaml("tasks.yaml")

    tasks = [
        Task(
            description=cfg["market_data_task"]["description"].format(query=query),
            expected_output=cfg["market_data_task"]["expected_output"],
            agent=agents["market_data"],
        ),
        Task(
            description=cfg["onchain_task"]["description"].format(query=query),
            expected_output=cfg["onchain_task"]["expected_output"],
            agent=agents["onchain"],
        ),
        Task(
            description=cfg["sentiment_task"]["description"].format(query=query),
            expected_output=cfg["sentiment_task"]["expected_output"],
            agent=agents["sentiment"],
        ),
        Task(
            description=cfg["macro_task"]["description"].format(query=query),
            expected_output=cfg["macro_task"]["expected_output"],
            agent=agents["macro"],
        ),
    ]

    return Crew(
        agents=[agents["market_data"], agents["onchain"], agents["sentiment"], agents["macro"]],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


def build_strategy_crew(
    query: str,
    agents: dict[str, Agent],
    market_data: str,
    onchain_data: str,
    sentiment_data: str,
    macro_data: str,
) -> Crew:
    """Build the strategy synthesis crew."""
    cfg = _load_yaml("tasks.yaml")

    task = Task(
        description=cfg["strategy_task"]["description"].format(
            query=query,
            market_data=market_data,
            onchain_data=onchain_data,
            sentiment_data=sentiment_data,
            macro_data=macro_data,
        ),
        expected_output=cfg["strategy_task"]["expected_output"],
        agent=agents["strategy"],
    )

    return Crew(
        agents=[agents["strategy"]],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )
