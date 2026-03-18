# tests/unit/api/test_system_routes.py
"""Unit tests for system routes."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestSystemRoutes:
    """Tests for /api/system endpoints."""

    def test_health_check(self, client: TestClient):
        """Test health endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "orchestrator" in data

    def test_system_status(self, client: TestClient):
        """Test system status endpoint."""
        response = client.get("/api/system/status")
        assert response.status_code == 200
        data = response.json()
        assert "running" in data
        assert "mode" in data
        assert "total_agents" in data

    def test_boot_system(self, client: TestClient, mock_orchestrator):
        """Test system boot endpoint."""
        mock_orchestrator.boot = lambda **kwargs: None
        
        response = client.post(
            "/api/system/boot",
            json={"tiers": [0, 1, 2], "exclude_agents": ["mercury"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "booting"
        assert data["booting_tiers"] == [0, 1, 2]
        assert data["excluded"] == ["mercury"]

    def test_shutdown_system(self, client: TestClient, mock_orchestrator):
        """Test system shutdown endpoint."""
        mock_orchestrator.shutdown = lambda: None
        
        response = client.post("/api/system/shutdown")
        assert response.status_code == 200
        assert response.json()["status"] == "shutting_down"

    def test_maintenance_mode(self, client: TestClient):
        """Test entering maintenance mode."""
        response = client.post("/api/system/maintenance")
        assert response.status_code == 200
        assert response.json()["status"] == "maintenance"

    def test_resume_from_maintenance(self, client: TestClient):
        """Test resuming from maintenance mode."""
        # First enter maintenance
        client.post("/api/system/maintenance")
        
        # Then resume
        response = client.post("/api/system/resume")
        assert response.status_code == 200