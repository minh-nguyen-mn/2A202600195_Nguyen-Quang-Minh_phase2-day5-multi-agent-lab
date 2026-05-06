from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="local", validation_alias="APP_ENV")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")

    openai_api_key: str | None = Field(default=None, validation_alias="OPENROUTER_API_KEY")
    openai_model: str = Field(default="openai/gpt-4o-mini", validation_alias="OPENROUTER_MODEL")

    max_iterations: int = Field(default=6)
    timeout_seconds: int = Field(default=60)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()