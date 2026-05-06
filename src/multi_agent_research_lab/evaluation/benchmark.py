"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def _estimate_cost(state: ResearchState) -> float | None:
    """Aggregate token usage if available."""
    total_cost = 0.0
    found = False

    for r in state.agent_results:
        cost = r.metadata.get("cost_usd")
        if cost is not None:
            total_cost += cost
            found = True

    return total_cost if found else None


def _quality_score(state: ResearchState) -> float:
    """
    Simple heuristic scoring (0–10):
    - Has final answer
    - Has research + analysis
    - Length / completeness
    """

    if not state.final_answer:
        return 0.0

    score = 5.0

    if state.research_notes:
        score += 1.5
    if state.analysis_notes:
        score += 1.5

    length = len(state.final_answer.split())
    if length > 200:
        score += 1.0
    elif length < 50:
        score -= 1.0

    return max(0.0, min(10.0, score))


def _citation_coverage(state: ResearchState) -> float | None:
    """
    Approximate citation coverage:
    (# sources referenced) / (# sources collected)
    """

    if not state.sources or not state.final_answer:
        return None

    used = 0
    for src in state.sources:
        if src.title.lower() in state.final_answer.lower():
            used += 1

    return used / len(state.sources)


def _failure_rate(state: ResearchState) -> float:
    """Basic failure proxy."""
    if not state.final_answer:
        return 1.0
    return 0.0


def run_benchmark(
    run_name: str,
    query: str,
    runner: Runner,
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and compute richer evaluation metrics."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started

    cost = _estimate_cost(state)
    quality = _quality_score(state)
    citation = _citation_coverage(state)
    failure = _failure_rate(state)

    notes = (
        f"iterations={state.iteration}, "
        f"sources={len(state.sources)}, "
        f"citation_coverage={citation if citation is not None else 'N/A'}, "
        f"errors={len(state.errors)}"
    )

    metrics = BenchmarkMetrics(
        run_name=run_name,
        latency_seconds=latency,
        estimated_cost_usd=cost,
        quality_score=quality,
        notes=notes,
    )

    return state, metrics