from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.core.schemas import AgentResult, AgentName


class CriticAgent(BaseAgent):
    name = "critic"

    def __init__(self):
        self.llm = LLMClient()

    def run(self, state: ResearchState) -> ResearchState:
        if not state.final_answer:
            return state

        prompt = f"""
Review the following answer:

{state.final_answer}

Tasks:
- Check factual consistency with research notes
- Identify hallucinations
- Score quality (0–10)
- Suggest improvements
"""

        resp = self.llm.complete("You are a strict reviewer.", prompt)

        # ✅ FIXED TYPE
        state.agent_results.append(
            AgentResult(
                agent=AgentName.CRITIC,
                content=resp.content,
                metadata={}
            )
        )

        return state