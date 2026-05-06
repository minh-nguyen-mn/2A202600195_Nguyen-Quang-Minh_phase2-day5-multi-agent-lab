"""LangGraph workflow implementation."""

from typing import Literal

from langgraph.graph import END, StateGraph

from multi_agent_research_lab.agents import (
    AnalystAgent,
    ResearcherAgent,
    SupervisorAgent,
    WriterAgent,
)
from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(self) -> None:
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

    # -----------------------------
    # Node wrappers (LangGraph nodes must be callables)
    # -----------------------------

    def supervisor_node(self, state: ResearchState) -> ResearchState:
        return self.supervisor.run(state)

    def researcher_node(self, state: ResearchState) -> ResearchState:
        return self.researcher.run(state)

    def analyst_node(self, state: ResearchState) -> ResearchState:
        return self.analyst.run(state)

    def writer_node(self, state: ResearchState) -> ResearchState:
        return self.writer.run(state)

    # -----------------------------
    # Routing logic (critical part)
    # -----------------------------

    def route(self, state: ResearchState) -> Literal[
        "researcher", "analyst", "writer", "end"
    ]:
        """Read last decision from supervisor and route graph."""

        last_route = state.route_history[-1]

        if last_route == "done":
            return "end"

        return last_route  # researcher / analyst / writer

    # -----------------------------
    # Build graph
    # -----------------------------

    def build(self):
        graph = StateGraph(ResearchState)

        # Add nodes
        graph.add_node("supervisor", self.supervisor_node)
        graph.add_node("researcher", self.researcher_node)
        graph.add_node("analyst", self.analyst_node)
        graph.add_node("writer", self.writer_node)

        # Entry point
        graph.set_entry_point("supervisor")

        # Conditional routing from supervisor
        graph.add_conditional_edges(
            "supervisor",
            self.route,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "end": END,
            },
        )

        # After each worker → go back to supervisor
        graph.add_edge("researcher", "supervisor")
        graph.add_edge("analyst", "supervisor")
        graph.add_edge("writer", "supervisor")

        return graph.compile()

    # -----------------------------
    # Run graph
    # -----------------------------

    def run(self, state: ResearchState) -> ResearchState:
        app = self.build()

        # LangGraph returns updated state
        result = app.invoke(state)

        return result