"""Tests for the FastAPI application and routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from aibe.ui.backend.app import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


class TestHealthRoutes:
    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "2.0.0"

    def test_readiness_check(self, client: TestClient) -> None:
        response = client.get("/api/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


class TestAgentRoutes:
    def test_list_agents(self, client: TestClient) -> None:
        response = client.get("/api/agents/")
        assert response.status_code == 200
        assert "agents" in response.json()

    def test_get_agent(self, client: TestClient) -> None:
        response = client.get("/api/agents/oracle")
        assert response.status_code == 200
        assert response.json()["agent_id"] == "oracle"

    def test_get_agent_status(self, client: TestClient) -> None:
        response = client.get("/api/agents/oracle/status")
        assert response.status_code == 200
        assert "uptime_seconds" in response.json()


class TestTaskRoutes:
    def test_create_task(self, client: TestClient) -> None:
        response = client.post("/api/tasks/", json={
            "title": "Research competitors",
            "target_agent": "scout",
        })
        assert response.status_code == 200
        assert response.json()["title"] == "Research competitors"

    def test_list_tasks(self, client: TestClient) -> None:
        response = client.get("/api/tasks/")
        assert response.status_code == 200
        assert "tasks" in response.json()


class TestMeetingRoutes:
    def test_list_meeting_types(self, client: TestClient) -> None:
        response = client.get("/api/meetings/types")
        assert response.status_code == 200
        types = response.json()["types"]
        assert len(types) == 8
        type_names = [t["meeting_type"] for t in types]
        assert "strategy_summit" in type_names
        assert "sprint_planning" in type_names

    def test_convene_meeting(self, client: TestClient) -> None:
        response = client.post("/api/meetings/convene", json={
            "meeting_type": "strategy_summit",
            "title_vars": {"topic": "Q1"},
        })
        assert response.status_code == 200


class TestCostRoutes:
    def test_cost_summary(self, client: TestClient) -> None:
        response = client.get("/api/costs/summary")
        assert response.status_code == 200
        data = response.json()
        assert "llm_spend_usd" in data
        assert "llm_budget_usd" in data

    def test_agent_costs(self, client: TestClient) -> None:
        response = client.get("/api/costs/agents")
        assert response.status_code == 200
