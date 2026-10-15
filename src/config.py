"""TalentFlow-AI configuration module powered by pydantic-settings."""

import json
from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable loading and test-safe defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Primary LLM Configuration
    primary_llm_api_key: str = Field(
        default="mock-primary-key",
        validation_alias="PRIMARY_LLM_API_KEY",
        description="API key for the primary LLM provider",
    )
    primary_llm_base_url: str = Field(
        default="https://api.deepseek.com/v1",
        validation_alias="PRIMARY_LLM_BASE_URL",
        description="Base URL for the primary LLM endpoint",
    )
    primary_llm_model: str = Field(
        default="deepseek-chat",
        validation_alias="PRIMARY_LLM_MODEL",
        description="Primary LLM model identifier",
    )

    # Fallback LLM Configuration (Google Gemini)
    gemini_api_key: str = Field(
        default="mock-gemini-key",
        validation_alias="GEMINI_API_KEY",
        description="API key for Google Gemini fallback model",
    )
    gemini_model: str = Field(
        default="gemini/gemini-2.5-flash",
        validation_alias="GEMINI_MODEL",
        description="Gemini fallback model identifier",
    )

    # Observability & Tracing (Langfuse)
    langfuse_public_key: str = Field(
        default="pk-lf-mock",
        validation_alias="LANGFUSE_PUBLIC_KEY",
        description="Langfuse public key for client-side tracing",
    )
    langfuse_secret_key: str = Field(
        default="sk-lf-mock",
        validation_alias="LANGFUSE_SECRET_KEY",
        description="Langfuse secret key for server-side tracing",
    )
    langfuse_host: str = Field(
        default="https://cloud.langfuse.com",
        validation_alias="LANGFUSE_HOST",
        description="Langfuse host URL",
    )

    # Google Sheets Storage
    google_sheet_id: str = Field(
        default="mock-sheet-id",
        validation_alias="GOOGLE_SHEET_ID",
        description="Target Google Sheet identifier for job persistence",
    )
    google_service_account_json: str = Field(
        default="{}",
        validation_alias="GOOGLE_SERVICE_ACCOUNT_JSON",
        description="Raw JSON string or file path for Google Service Account credentials",
    )

    # GitHub Actions Integration
    github_pat_token: str = Field(
        default="mock-github-pat",
        validation_alias="GITHUB_PAT_TOKEN",
        description="GitHub Personal Access Token for triggering workflows",
    )
    github_repository: str = Field(
        default="username/talentflow-ai",
        validation_alias="GITHUB_REPOSITORY",
        description="GitHub repository in owner/repo format",
    )

    # Application Runtime
    environment: str = Field(
        default="development",
        validation_alias="ENVIRONMENT",
        description="Application environment (development, staging, production)",
    )
    dry_run: bool = Field(
        default=True,
        validation_alias="DRY_RUN",
        description="When True, browser automation will not execute final form submissions",
    )
    headless: bool = Field(
        default=True,
        validation_alias="HEADLESS",
        description="Whether to run Playwright in headless mode",
    )
    max_jobs_per_run: int = Field(
        default=10,
        validation_alias="MAX_JOBS_PER_RUN",
        description="Maximum number of jobs to process per execution run",
    )
    log_level: str = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    @property
    def is_production(self) -> bool:
        """Return True if running in production environment."""
        return self.environment.lower() == "production"

    def get_service_account_info(self) -> dict[str, Any]:
        """Safely parse service account JSON string into dictionary."""
        try:
            parsed = json.loads(self.google_service_account_json)
            if isinstance(parsed, dict):
                return parsed
            return {}
        except (json.JSONDecodeError, TypeError):
            return {}


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
