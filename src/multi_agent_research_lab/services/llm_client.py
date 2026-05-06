"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.errors import AgentExecutionError


# Ensure .env overrides system env (important for lab reproducibility)
load_dotenv(override=True)


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def __init__(self) -> None:
        settings = get_settings()

        if not settings.openai_api_key:
            raise AgentExecutionError("Missing OPENROUTER_API_KEY")

        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self.model = settings.openai_model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion.

        - Uses OpenRouter via OpenAI SDK
        - Includes retry logic
        - Captures token usage
        """

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                extra_headers={
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "multi-agent-research-lab",
                },
            )

            usage = resp.usage

            return LLMResponse(
                content=resp.choices[0].message.content,
                input_tokens=usage.prompt_tokens if usage else None,
                output_tokens=usage.completion_tokens if usage else None,
                cost_usd=None,  # OpenRouter may not return cost
            )

        except Exception as e:
            raise AgentExecutionError(f"LLM call failed: {e}") from e