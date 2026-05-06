from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult, AgentName 


class AnalystAgent(BaseAgent):
    name = "analyst"

    def __init__(self):
        self.llm = LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        prompt = f"""
Analyze:
{state.research_notes}

- Key claims
- Comparisons
- Weak evidence
"""
        resp = self.llm.complete("You are an analyst.", prompt)

        state.analysis_notes = resp.content

        state.agent_results.append(
            AgentResult(
                agent=AgentName.ANALYST,
                content=resp.content,
                metadata={
                    "cost_usd": resp.cost_usd,
                    "input_tokens": resp.input_tokens,
                    "output_tokens": resp.output_tokens,
                },
            )
        )

        return state