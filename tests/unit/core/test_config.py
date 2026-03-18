"""Tests for aibe.core.config — application settings."""

from __future__ import annotations

from aibe.core.config import Settings, get_settings


class TestSettings:
    def test_default_environment(self) -> None:
        """Settings should load ENVIRONMENT from env var set by conftest."""
        settings = get_settings()
        assert settings.environment == "test"

    def test_nested_database_settings(self) -> None:
        """Database sub-settings should populate from DATABASE__ prefix vars."""
        settings = Settings()  # Fresh instance, not cached
        assert "asyncpg" in settings.database.url

    def test_is_test_mode(self) -> None:
        settings = get_settings()
        assert settings.is_test
        assert not settings.is_production

    def test_default_budget_values(self) -> None:
        settings = Settings()
        assert settings.budget.daily_llm_usd == 50.0
        assert settings.budget.daily_ads_cap_usd == 100.0

    def test_redis_defaults(self) -> None:
        settings = Settings()
        assert settings.redis.max_connections == 50

    def test_nats_defaults(self) -> None:
        settings = Settings()
        assert settings.nats.max_reconnect_attempts == 60

    def test_secret_key_is_secret(self) -> None:
        settings = get_settings()
        # Secret values should not appear in repr
        assert "changeme" not in repr(settings.secret_key)
