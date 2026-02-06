"""CrewAI Flow orchestrator for the CryptoHive pipeline."""

from crewai.flow.flow import Flow, listen, start

from cryptohive.crew import build_agents, build_data_crew, build_strategy_crew
from cryptohive.models.schemas import AnalysisState


class CryptoIntelligenceFlow(Flow[AnalysisState]):
    """Orchestrates the multi-agent analysis pipeline."""

    def __init__(self, query: str):
        super().__init__()
        self.query = query
        self.agents = build_agents()

    @start()
    def gather_data(self) -> str:
        """Run all data-gathering agents."""
        self.state.query = self.query
        crew = build_data_crew(self.query, self.agents)
        result = crew.kickoff()

        # Extract individual task outputs
        task_outputs = result.tasks_output if hasattr(result, "tasks_output") else []

        if len(task_outputs) >= 4:
            self.state.market.raw = str(task_outputs[0])
            self.state.onchain.raw = str(task_outputs[1])
            self.state.sentiment.raw = str(task_outputs[2])
            self.state.macro.raw = str(task_outputs[3])
        else:
            # Fallback: store entire result
            self.state.market.raw = str(result)

        self.state.data_sources.extend([
            "CoinGecko", "GeckoTerminal", "SerperDev", "Alternative.me"
        ])

        return str(result)

    @listen(gather_data)
    def synthesize(self, data_result: str) -> str:
        """Run strategy agent to synthesize all findings."""
        market = self.state.market.raw or data_result
        onchain = self.state.onchain.raw or "No on-chain data gathered."
        sentiment = self.state.sentiment.raw or "No sentiment data gathered."
        macro = self.state.macro.raw or "No macro data gathered."

        crew = build_strategy_crew(
            self.query, self.agents, market, onchain, sentiment, macro,
        )
        result = crew.kickoff()
        self.state.synthesis = str(result)
        return str(result)


def run_analysis(query: str) -> str:
    """Run the full CryptoHive analysis pipeline."""
    flow = CryptoIntelligenceFlow(query)
    result = flow.kickoff()
    return str(result)
