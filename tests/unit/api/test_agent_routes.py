# tests/unit/api/test_agent_routes.py
"""Unit tests for agent routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestAgentRoutes:
    """Tests for /api/agents endpoints."""

    def test_list_agents_empty(self, client: TestClient):
        """Test listing agents when registry is empty."""
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["agents"] == []
        assert data["total"] == 0

    def test_list_agents_with_agents(self, client: TestClient, mock_orchestrator, mock_agent):
        """Test listing agents with populated registry."""
        mock_orchestrator.registry.register(mock_agent)
        
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["agents"][0]["agent_id"] == "test_agent"

    def test_list_agents_filter_by_tier(self, client: TestClient, mock_orchestrator, mock_agent):
        """Test filtering agents by tier."""
        mock_agent.tier = 5
        mock_orchestrator.registry.register(mock_agent)
        
        response = client.get("/api/agents?tier=5")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        
        response = client.get("/api/agents?tier=0")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_get_agent_not_found(self, client: TestClient):
        """Test getting non-existent agent."""
        response = client.get("/api/agents/nonexistent")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_agent_found(self, client: TestClient, mock_orchestrator, mock_agent):
        """Test getting existing agent."""
        mock_orchestrator.registry.register(mock_agent)
        
        response = client.get("/api/agents/test_agent")
        assert response.status_code == 200
        data = response.json()
        assert data["agent_id"] == "test_agent"
        assert "escalation_target" in data

    def test_restart_agent_not_found(self, client: TestClient):
        """Test restarting non-existent agent."""
        response = client.post("/api/agents/nonexistent/restart")
        assert response.status_code == 404

    def test_restart_agent_success(self, client: TestClient, mock_orchestrator, mock_agent):
        """Test successful agent restart."""
        mock_agent.stop = lambda: None
        mock_agent.start = lambda: None
        mock_orchestrator.registry.register(mock_agent)
        
        response = client.post("/api/agents/test_agent/restart")
        assert response.status_code == 200
        assert response.json()["restarted"] is True