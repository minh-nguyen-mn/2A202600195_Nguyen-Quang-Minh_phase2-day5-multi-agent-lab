from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult, AgentName  


class WriterAgent(BaseAgent):
    name = "writer"

    def __init__(self):
        self.llm = LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        prompt = f"""
Question: {state.request.query}

Research:
{state.research_notes}

Analysis:
{state.analysis_notes}

Write final answer.
"""
        resp = self.llm.complete("You are a writer.", prompt)

        state.final_answer = resp.content

        state.agent_results.append(
            AgentResult(
                agent=AgentName.WRITER,
                content=resp.content,
                metadata={
                    "cost_usd": resp.cost_usd,
                    "input_tokens": resp.input_tokens,
                    "output_tokens": resp.output_tokens,
                },
            )
        )

        return state