# tests/conftest.py
"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from aibe.agents.registry import AgentRegistry
from aibe.core.orchestrator.orchestrator import SystemOrchestrator
from aibe.ui.backend.app import create_app
from aibe.ui.backend.dependencies import set_orchestrator


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_registry() -> AgentRegistry:
    """Create a mock agent registry."""
    registry = AgentRegistry()
    return registry


@pytest.fixture
def mock_orchestrator(mock_registry: AgentRegistry) -> MagicMock:
    """Create a mock orchestrator."""
    orchestrator = MagicMock(spec=SystemOrchestrator)
    orchestrator.registry = mock_registry
    orchestrator.get_status.return_value = {
        "running": True,
        "total_agents": 0,
        "active_agents": 0,
        "status_summary": {},
        "tools_registered": 0,
    }
    return orchestrator


@pytest.fixture
def app(mock_orchestrator: MagicMock):
    """Create FastAPI app with mocked dependencies."""
    set_orchestrator(mock_orchestrator)
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    """Create sync test client."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client(app) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_agent() -> MagicMock:
    """Create a mock agent."""
    agent = MagicMock()
    agent.agent_id = "test_agent"
    agent.name = "Test Agent"
    agent.tier = 0
    agent.status = "ready"
    agent._start_time = 0
    agent._tasks_completed = 0
    agent._error_count = 0
    agent.daily_budget_usd = 5.0
    agent.escalation_target = "oracle"
    return agent


# Markers for test categories
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "integration: integration tests requiring external services")
    config.addinivalue_line("markers", "e2e: end-to-end tests")
    config.addinivalue_line("markers", "slow: slow-running tests")