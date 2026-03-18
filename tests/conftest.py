"""Shared test fixtures and factories for AIBE tests."""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture(autouse=True)
def _set_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set test environment variables for all tests."""
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-for-unit-tests-64chars-long-enough-for-hmac!!")
    monkeypatch.setenv("DATABASE__URL", "postgresql+asyncpg://test:test@localhost:5432/test")
    monkeypatch.setenv("REDIS__URL", "redis://localhost:6379/15")
    monkeypatch.setenv("NATS__URL", "nats://localhost:4222")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENVIKING__CONNECTION_STRING", "")
    monkeypatch.setenv("OPENVIKING__API_KEY", "")

    # Clear cached settings so the test environment takes effect
    from aibe.core.config import get_settings
    get_settings.cache_clear()


@pytest.fixture
def mock_nats_bus() -> AsyncMock:
    """Mock NATS bus client."""
    bus = AsyncMock()
    bus.is_connected = True
    bus.connect = AsyncMock()
    bus.disconnect = AsyncMock()
    bus.publish = AsyncMock()
    bus.subscribe = AsyncMock()
    bus.request = AsyncMock(return_value=b'{"status": "ok"}')
    return bus


@pytest.fixture
def mock_memory_client() -> AsyncMock:
    """Mock OpenViking memory client."""
    client = AsyncMock()
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.store = AsyncMock()
    client.recall = AsyncMock(return_value=None)
    client.semantic_search = AsyncMock(return_value=[])
    client.batch_write = AsyncMock()
    return client


@pytest.fixture
def mock_redis() -> AsyncMock:
    """Mock Redis client."""
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock()
    redis.incrbyfloat = AsyncMock(return_value="0.0")
    redis.ttl = AsyncMock(return_value=-1)
    redis.expire = AsyncMock()
    redis.scan = AsyncMock(return_value=(0, []))
    return redis
