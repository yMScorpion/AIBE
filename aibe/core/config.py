"""AIBE application settings — single source of truth for all configuration.

Uses pydantic-settings to load from environment variables with nested
delimiter support (e.g. DATABASE__HOST maps to Settings.database.host).
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root: two levels up from aibe/core/config.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ═══════════════════════════════════════════════════════════════
# SUB-SETTINGS
# ═══════════════════════════════════════════════════════════════


class DatabaseSettings(BaseSettings):
    """PostgreSQL connection settings."""

    model_config = SettingsConfigDict(env_prefix="DATABASE__")

    url: str = "postgresql+asyncpg://aibe:changeme@localhost:5432/aibe"
    sync_url: str = "postgresql://aibe:changeme@localhost:5432/aibe"
    pool_size: int = 20
    max_overflow: int = 10
    pool_timeout: int = 30
    echo: bool = False


class RedisSettings(BaseSettings):
    """Redis connection settings."""

    model_config = SettingsConfigDict(env_prefix="REDIS__")

    url: str = "redis://localhost:6379/0"
    cache_url: str = "redis://localhost:6379/1"
    celery_url: str = "redis://localhost:6379/2"
    max_connections: int = 50


class NATSSettings(BaseSettings):
    """NATS message bus settings."""

    model_config = SettingsConfigDict(env_prefix="NATS__")

    url: str = "nats://localhost:4222"
    cluster_name: str = "aibe-cluster"
    max_reconnect_attempts: int = 60
    reconnect_time_wait_seconds: int = 2


class VaultSettings(BaseSettings):
    """HashiCorp Vault settings."""

    model_config = SettingsConfigDict(env_prefix="VAULT__")

    addr: str = "http://localhost:8200"
    token: SecretStr = SecretStr("changeme")
    mount_point: str = "secret"


class OpenRouterSettings(BaseSettings):
    """OpenRouter LLM API settings."""

    model_config = SettingsConfigDict(env_prefix="OPENROUTER__")

    api_key: SecretStr = SecretStr("")
    base_url: str = "https://openrouter.ai/api/v1"
    timeout_seconds: int = 120
    max_retries: int = 3


class OpenVikingSettings(BaseSettings):
    """OpenViking memory system settings."""

    model_config = SettingsConfigDict(env_prefix="OPENVIKING__")

    connection_string: str = ""
    api_key: SecretStr = SecretStr("")


class LightpandaSettings(BaseSettings):
    """Lightpanda browser pool settings."""

    model_config = SettingsConfigDict(env_prefix="LIGHTPANDA__")

    api_url: str = "http://localhost:8080"
    pool_size: int = 3
    max_pool_size: int = 10


class ClickHouseSettings(BaseSettings):
    """ClickHouse analytics database settings."""

    model_config = SettingsConfigDict(env_prefix="CLICKHOUSE__")

    host: str = "localhost"
    port: int = 9000
    user: str = "aibe"
    password: SecretStr = SecretStr("changeme")
    database: str = "aibe_analytics"


class CelerySettings(BaseSettings):
    """Celery task queue settings."""

    model_config = SettingsConfigDict(env_prefix="CELERY__")

    broker_url: str = "redis://localhost:6379/2"
    result_backend: str = "redis://localhost:6379/2"
    task_default_queue: str = "default"


class ModalSettings(BaseSettings):
    """Modal cloud GPU settings."""

    model_config = SettingsConfigDict(env_prefix="MODAL__")

    token_id: str = ""
    token_secret: SecretStr = SecretStr("")


class WandBSettings(BaseSettings):
    """Weights & Biases experiment tracking settings."""

    model_config = SettingsConfigDict(env_prefix="WANDB__")

    api_key: SecretStr = SecretStr("")
    project: str = "aibe-ml"


class BudgetSettings(BaseSettings):
    """Global budget configuration."""

    model_config = SettingsConfigDict(env_prefix="BUDGET__")

    daily_llm_usd: float = 50.00
    daily_ads_cap_usd: float = 100.00
    monthly_contractor_usd: float = 500.00
    contractor_auto_approve_usd: float = 200.00
    contractor_human_approve_usd: float = 500.00


# ═══════════════════════════════════════════════════════════════
# MAIN SETTINGS
# ═══════════════════════════════════════════════════════════════


class Settings(BaseSettings):
    """Root application settings composing all sub-settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────
    environment: Literal["development", "staging", "production", "test"] = "development"
    log_level: str = "INFO"
    secret_key: SecretStr = SecretStr("changeme-to-random-64-char-string")
    primary_domain: str = ""

    # ── Auth ──────────────────────────────────────────────────
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    # ── Human-in-the-loop ─────────────────────────────────────
    human_review_mode: bool = False
    human_operator_email: str = ""
    human_slack_webhook: str = ""

    # ── Feature flags ─────────────────────────────────────────
    sales_activation_threshold: int = 5
    security_block_on_high: bool = True
    pentest_schedule: str = "weekly"
    evolution_cycle_hours: int = 48

    # ── Direct API keys (flat env vars) ───────────────────────
    openrouter_api_key: SecretStr = SecretStr("")
    anthropic_api_key: SecretStr = SecretStr("")
    openai_api_key: SecretStr = SecretStr("")

    # ── Sub-settings ──────────────────────────────────────────
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    nats: NATSSettings = Field(default_factory=NATSSettings)
    vault: VaultSettings = Field(default_factory=VaultSettings)
    openrouter: OpenRouterSettings = Field(default_factory=OpenRouterSettings)
    openviking: OpenVikingSettings = Field(default_factory=OpenVikingSettings)
    lightpanda: LightpandaSettings = Field(default_factory=LightpandaSettings)
    clickhouse: ClickHouseSettings = Field(default_factory=ClickHouseSettings)
    celery: CelerySettings = Field(default_factory=CelerySettings)
    modal: ModalSettings = Field(default_factory=ModalSettings)
    wandb: WandBSettings = Field(default_factory=WandBSettings)
    budget: BudgetSettings = Field(default_factory=BudgetSettings)

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    @property
    def is_test(self) -> bool:
        """Check if running in test mode."""
        return self.environment == "test"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the cached global settings instance.

    Returns the same Settings object on repeated calls.
    Use in FastAPI dependency injection:

        settings = Depends(get_settings)
    """
    return Settings()


__all__ = [
    "BudgetSettings",
    "CelerySettings",
    "ClickHouseSettings",
    "DatabaseSettings",
    "LightpandaSettings",
    "ModalSettings",
    "NATSSettings",
    "OpenRouterSettings",
    "OpenVikingSettings",
    "PROJECT_ROOT",
    "RedisSettings",
    "Settings",
    "VaultSettings",
    "WandBSettings",
    "get_settings",
]
