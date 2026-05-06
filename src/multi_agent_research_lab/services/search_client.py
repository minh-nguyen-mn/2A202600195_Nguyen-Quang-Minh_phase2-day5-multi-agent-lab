"""Search client abstraction for ResearcherAgent."""

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.

        Current implementation:
        - Deterministic mock (no external API dependency)
        - Ensures reproducibility for benchmarking and testing

        Can be swapped with:
        - Tavily
        - SerpAPI
        - Bing Search API
        """

        results: list[SourceDocument] = []

        for i in range(max_results):
            results.append(
                SourceDocument(
                    title=f"Mock Source {i+1} about '{query}'",
                    snippet=(
                        f"This is a synthesized snippet discussing '{query}', "
                        f"covering aspect {i+1}. It provides context, claims, "
                        f"and supporting details for downstream analysis."
                    ),
                    url=f"https://example.com/{query.replace(' ', '_')}/{i+1}",
                    metadata={"rank": i + 1, "source": "mock"},
                )
            )

        return results