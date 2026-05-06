"""Tracing hooks.

This file intentionally avoids binding to one provider. Students can plug in LangSmith,
Langfuse, OpenTelemetry, or simple JSON traces.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any


@contextmanager
def trace_span(
    name: str,
    attributes: dict[str, Any] | None = None,
    trace_sink: list[dict[str, Any]] | None = None,
) -> Iterator[dict[str, Any]]:
    """Minimal span context used by the skeleton.

    Enhancements:
    - Records duration
    - Captures errors
    - Optionally pushes to shared trace list (ResearchState.trace)
    """

    started = perf_counter()
    span: dict[str, Any] = {
        "name": name,
        "attributes": attributes or {},
        "duration_seconds": None,
        "status": "ok",
        "error": None,
    }

    try:
        yield span

    except Exception as e:
        span["status"] = "error"
        span["error"] = str(e)
        raise

    finally:
        span["duration_seconds"] = perf_counter() - started

        # Push to shared trace if provided
        if trace_sink is not None:
            trace_sink.append(span)

        # Fallback: print (useful for CLI debugging)
        else:
            print(span)