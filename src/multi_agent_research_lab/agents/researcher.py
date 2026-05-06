from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    name = "researcher"

    def __init__(self):
        self.search = SearchClient()

    def run(self, state: ResearchState) -> ResearchState:
        sources = self.search.search(
            state.request.query,
            state.request.max_sources
        )

        state.add_trace_event("research", {"num_sources": len(sources)})

        notes = "\n".join(f"- {s.title}: {s.snippet}" for s in sources)

        state.sources = sources
        state.research_notes = notes

        return state