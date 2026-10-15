"""Unit tests for application configuration and settings loading."""

import os
from unittest.mock import patch

from src.config import Settings, get_settings


def test_default_settings():
    """Verify that Settings instantiates with test-safe defaults without external env."""
    with patch.dict(os.environ, {}, clear=True):
        settings = Settings()
        assert settings.primary_llm_api_key == "mock-primary-key"
        assert settings.primary_llm_base_url == "https://api.deepseek.com/v1"
        assert settings.primary_llm_model == "deepseek-chat"
        assert settings.gemini_api_key == "mock-gemini-key"
        assert settings.gemini_model == "gemini/gemini-2.5-flash"
        assert settings.langfuse_public_key == "pk-lf-mock"
        assert settings.langfuse_secret_key == "sk-lf-mock"
        assert settings.google_sheet_id == "mock-sheet-id"
        assert settings.dry_run is True
        assert settings.headless is True
        assert settings.max_jobs_per_run == 10
        assert settings.environment == "development"
        assert settings.is_production is False


def test_environment_override():
    """Verify environment variables correctly override default settings."""
    test_env = {
        "PRIMARY_LLM_API_KEY": "test-custom-key",
        "PRIMARY_LLM_BASE_URL": "https://api.custom.ai/v1",
        "PRIMARY_LLM_MODEL": "custom-gpt-4",
        "GEMINI_API_KEY": "test-gemini-custom",
        "ENVIRONMENT": "production",
        "DRY_RUN": "false",
        "MAX_JOBS_PER_RUN": "25",
        "GOOGLE_SHEET_ID": "custom-sheet-xyz",
    }
    with patch.dict(os.environ, test_env, clear=True):
        settings = Settings()
        assert settings.primary_llm_api_key == "test-custom-key"
        assert settings.primary_llm_base_url == "https://api.custom.ai/v1"
        assert settings.primary_llm_model == "custom-gpt-4"
        assert settings.gemini_api_key == "test-gemini-custom"
        assert settings.environment == "production"
        assert settings.is_production is True
        assert settings.dry_run is False
        assert settings.max_jobs_per_run == 25
        assert settings.google_sheet_id == "custom-sheet-xyz"


def test_get_settings_singleton():
    """Verify get_settings returns a cached instance."""
    get_settings.cache_clear()
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2


def test_service_account_info_parsing():
    """Verify parsing valid and invalid service account JSON."""
    valid_json = '{"project_id": "test-proj", "private_key": "-----BEGIN KEY-----"}'
    s_valid = Settings(GOOGLE_SERVICE_ACCOUNT_JSON=valid_json)
    info = s_valid.get_service_account_info()
    assert info.get("project_id") == "test-proj"

    s_invalid = Settings(GOOGLE_SERVICE_ACCOUNT_JSON="invalid-json-string")
    assert s_invalid.get_service_account_info() == {}
