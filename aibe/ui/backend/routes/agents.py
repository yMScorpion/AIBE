"""Agent management routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_agents() -> dict[str, Any]:
    """List all registered agents with their current status."""
    # TODO: Connect to AgentRegistry
    return {
        "agents": [],
        "total": 0,
        "active": 0,
    }


@router.get("/{agent_id}")
async def get_agent(agent_id: str) -> dict[str, Any]:
    """Get details of a specific agent."""
    return {
        "agent_id": agent_id,
        "status": "not_initialized",
        "detail": "Agent registry not connected yet",
    }


@router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str) -> dict[str, Any]:
    """Get current status and metrics for an agent."""
    return {
        "agent_id": agent_id,
        "status": "not_initialized",
        "uptime_seconds": 0,
        "tasks_completed": 0,
        "error_count": 0,
    }


@router.post("/{agent_id}/start")
async def start_agent(agent_id: str) -> dict[str, str]:
    """Start a specific agent."""
    return {"status": "pending", "detail": "Agent startup not implemented yet"}


@router.post("/{agent_id}/stop")
async def stop_agent(agent_id: str) -> dict[str, str]:
    """Stop a specific agent."""
    return {"status": "pending", "detail": "Agent shutdown not implemented yet"}
