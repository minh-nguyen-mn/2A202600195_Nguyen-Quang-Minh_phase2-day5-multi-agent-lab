"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown.

    Enhanced with:
    - Summary table
    - Comparative analysis
    - Observations
    """

    # --- Table (keep original structure) ---
    lines = [
        "# Benchmark Report",
        "",
        "| Run | Latency (s) | Cost (USD) | Quality | Notes |",
        "|---|---:|---:|---:|---|",
    ]

    for item in metrics:
        cost = "" if item.estimated_cost_usd is None else f"{item.estimated_cost_usd:.4f}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(
            f"| {item.run_name} | {item.latency_seconds:.2f} | {cost} | {quality} | {item.notes} |"
        )

    # --- Analysis Section ---
    lines.append("\n## Analysis\n")

    if len(metrics) >= 2:
        # Assume first = baseline, second = multi-agent (common convention)
        baseline = metrics[0]
        multi = metrics[1]

        latency_diff = multi.latency_seconds - baseline.latency_seconds
        quality_diff = (multi.quality_score or 0) - (baseline.quality_score or 0)

        lines.append("### Comparison: Baseline vs Multi-Agent\n")
        lines.append(f"- Latency difference: {latency_diff:+.2f} seconds")
        lines.append(f"- Quality difference: {quality_diff:+.2f}")

        if latency_diff > 0:
            lines.append("- Multi-agent system is slower due to multiple steps.")
        else:
            lines.append("- Multi-agent system is faster (unexpected, investigate).")

        if quality_diff > 0:
            lines.append("- Multi-agent improves answer quality via structured reasoning.")
        elif quality_diff < 0:
            lines.append("- Multi-agent underperforms baseline (possible coordination issues).")
        else:
            lines.append("- No significant quality difference observed.")

    else:
        lines.append("- Not enough runs to compare baseline vs multi-agent.")

    # --- Observations ---
    lines.append("\n## Observations\n")
    lines.append("- Multi-agent systems decompose tasks into specialized roles.")
    lines.append("- This improves interpretability and modular debugging.")
    lines.append("- Trade-off: increased latency and orchestration complexity.")
    lines.append("- Performance depends heavily on routing and agent design.\n")

    # --- Optional Extension Hooks ---
    lines.append("## Future Improvements\n")
    lines.append("- Add citation coverage metric (sources used / claims).")
    lines.append("- Track token usage and estimated cost.")
    lines.append("- Integrate trace visualization (LangSmith / Langfuse).")
    lines.append("- Add automated quality scoring via LLM-as-judge.\n")

    return "\n".join(lines) + "\n"