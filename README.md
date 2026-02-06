# CryptoHive - Multi-Agent Web3 Intelligence Swarm

A multi-agent swarm powered by [CrewAI](https://crewai.com) that generates trading signals, strategies, and market intelligence from real-time blockchain data and market insights.

## Overview

CryptoHive deploys a swarm of specialized AI agents that work together to analyze cryptocurrency markets from multiple angles:

| Agent | Role |
|-------|------|
| **Market Data Analyst** | Price, volume, OHLCV, market cap, top movers |
| **On-Chain Analyst** | Whale tracking, large trades, liquidity pools, token security |
| **Sentiment Analyst** | News, social sentiment, Fear & Greed Index, trending narratives |
| **Macro Analyst** | Total market cap, BTC dominance, risk regime assessment |
| **Strategy Synthesizer** | Aggregates all signals into a unified thesis with confidence score |
| **Orchestrator** | Decomposes queries, delegates to specialists, formats final report |

### How It Works

```
User Query
    |
    v
[Orchestrator] ──> [Market Data Agent] ──> CoinGecko API
                ──> [On-Chain Agent]    ──> GeckoTerminal / DexTools
                ──> [Sentiment Agent]   ──> SerperDev / Alternative.me
                ──> [Macro Agent]       ──> CoinGecko Global
    |
    v
[Strategy Synthesizer]
    |
    v
Final Report (bias, key drivers, invalidation conditions, confidence 1-10)
```

## Quick Start

### Prerequisites

- Python 3.11+
- API keys (see [Configuration](#configuration))

### Installation

```bash
git clone https://github.com/dhruvalgupta2003/CryptoHive.git
cd CryptoHive/cryptohive

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install
pip install -e .
```

### Configuration

Copy the example env file and add your API keys:

```bash
cp .env.example .env
```

**Required:**
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` — LLM provider (Anthropic recommended)

**Optional but recommended:**
- `COINGECKO_API_KEY` — Unlocks pro endpoints (free tier works with rate limits)
- `SERPER_API_KEY` — Enables web search for news and sentiment

### Usage

```bash
# Via CLI
cryptohive "Analyze BTC outlook for this week"

# Or run directly
python -m cryptohive.main "What's the sentiment around ETH?"

# More examples
cryptohive "Should I be bullish or bearish on SOL?"
cryptohive "Analyze on-chain activity for PEPE on BSC"
cryptohive "Give me a full market report for the top 10 coins"
```

## Project Structure

```
cryptohive/
├── src/cryptohive/
│   ├── config/
│   │   ├── agents.yaml          # Agent role definitions
│   │   └── tasks.yaml           # Task templates
│   ├── models/
│   │   └── schemas.py           # Pydantic state models
│   ├── tools/
│   │   ├── market_data.py       # CoinGecko price/market tools
│   │   ├── onchain.py           # GeckoTerminal + DexTools tools
│   │   ├── sentiment.py         # News search, Fear & Greed, trending
│   │   ├── macro.py             # Global market data tools
│   │   └── defi.py              # DEX pool discovery tools
│   ├── crew.py                  # Agent & crew construction
│   ├── flow.py                  # CrewAI Flow orchestration
│   └── main.py                  # CLI entry point
├── tests/
│   └── test_tools.py
├── pyproject.toml
└── .env.example
```

## Data Sources

| Source | Data | Auth Required |
|--------|------|---------------|
| [CoinGecko](https://www.coingecko.com/en/api) | Prices, market data, OHLCV, trending, global stats | Optional (free tier available) |
| [GeckoTerminal](https://www.geckoterminal.com/) | On-chain pools, trades, top holders/traders | No |
| [DexTools](https://www.dextools.io/) | BSC token analysis, security audits, scores | No (via CryptoHive API) |
| [SerperDev](https://serper.dev/) | Web search for news and sentiment | Yes |
| [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) | Crypto Fear & Greed Index | No |

## Roadmap

- [ ] Add technical analysis agent (RSI, MACD, Bollinger Bands)
- [ ] Support more chains (Solana, Arbitrum, Base)
- [ ] Telegram/Discord bot integration
- [ ] Historical report storage and backtesting
- [ ] Portfolio-level multi-asset analysis
- [ ] Streaming real-time alerts
- [ ] Custom strategy plugins

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [CrewAI](https://crewai.com) multi-agent framework
- Market data from [CoinGecko](https://www.coingecko.com/)
- On-chain data from [GeckoTerminal](https://www.geckoterminal.com/)

---

Created by [Dhruval Gupta](https://github.com/dhruvalgupta2003)
