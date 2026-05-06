from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.errors import StudentTodoError


class SupervisorAgent(BaseAgent):
    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        # ✅ TEST MODE (default): raise error so pytest passes
        # if not getattr(state, "_production", False):
        #     raise StudentTodoError("TODO(student): implement SupervisorAgent.run")

        # ✅ REAL IMPLEMENTATION
        settings = get_settings()

        if state.iteration >= settings.max_iterations:
            state.record_route("done")
            return state

        if not state.research_notes:
            route = "researcher"
        elif not state.analysis_notes:
            route = "analyst"
        elif not state.final_answer:
            route = "writer"
        else:
            route = "done"

        state.record_route(route)
        state.add_trace_event("route", {"next": route})

        return state