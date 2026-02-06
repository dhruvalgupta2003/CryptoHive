# Contributing to CryptoHive

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/CryptoHive.git
   cd CryptoHive
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Set up the dev environment:
   ```bash
   cd cryptohive
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   cp .env.example .env
   # Add your API keys to .env
   ```

## What to Work On

Check the [GitHub Issues](https://github.com/dhruvalgupta2003/CryptoHive/issues) for open tasks. Good areas to contribute:

- **New tools** — Add data sources (e.g., Etherscan, Dune Analytics, Santiment)
- **New agents** — Add specialist agents (e.g., technical analysis, NFT analysis)
- **Chain support** — Extend on-chain tools to more networks
- **Integrations** — Telegram bots, Discord bots, webhooks
- **Tests** — Improve test coverage for tools and flows
- **Docs** — Improve documentation and examples

## Adding a New Tool

1. Create or edit a file in `src/cryptohive/tools/`
2. Use the `@tool` decorator from CrewAI:
   ```python
   from crewai.tools import tool

   @tool("my_new_tool")
   def my_new_tool(param: str) -> str:
       """Docstring becomes the tool description for the agent."""
       # Your implementation
       return "result"
   ```
3. Register the tool with the appropriate agent in `crew.py`
4. Add tests in `tests/`

## Adding a New Agent

1. Define the agent in `config/agents.yaml`:
   ```yaml
   my_agent:
     role: "My Specialist"
     goal: "What this agent does"
     backstory: >
       Background context for the agent.
   ```
2. Define its task in `config/tasks.yaml`
3. Wire it up in `crew.py` — add to `build_agents()` and the appropriate crew

## Code Style

- Follow existing patterns in the codebase
- Use type hints
- Keep tools focused — one API call per tool where possible
- Handle API errors gracefully (return error strings, don't crash)
- Don't commit `.env` or API keys

## Pull Requests

1. Keep PRs focused on a single change
2. Write a clear description of what and why
3. Make sure existing tests pass: `pytest tests/`
4. Add tests for new functionality
5. Update the README if you add new features or data sources

## Commit Messages

Use clear, descriptive commit messages:
```
Add Etherscan tool for contract verification status
Fix OHLCV tool handling empty response
Update agents.yaml with technical analysis agent
```

## Reporting Issues

When filing a bug report, include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Relevant error messages or logs

## Code of Conduct

Be respectful and constructive. We're all here to build something useful.

## Questions?

Open a [GitHub Discussion](https://github.com/dhruvalgupta2003/CryptoHive/discussions) or file an issue.
