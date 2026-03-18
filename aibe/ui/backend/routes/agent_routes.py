# aibe/ui/backend/routes/agent_routes.py
"""Agent management endpoints."""

from __future__ import annotations

import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from aibe.ui.backend.dependencies import get_orchestrator
from aibe.ui.backend.schemas.agent_schemas import (
    AgentDetailResponse,
    AgentListResponse,
    AgentResponse,
    AgentRestartResponse,
)

router = APIRouter(prefix="/api/agents", tags=["agents"])


def _agent_to_response(agent) -> AgentResponse:
    uptime = time.time() - agent._start_time if hasattr(agent, "_start_time") and agent._start_time else 0.0
    return AgentResponse(
        agent_id=getattr(agent, "agent_id", "unknown"),
        agent_name=getattr(agent, "name", getattr(agent, "agent_id", "unknown")),
        tier=getattr(agent, "tier", -1),
        status=getattr(agent, "status", "unknown"),
        uptime_seconds=round(uptime, 1),
        tasks_completed=getattr(agent, "_tasks_completed", 0),
        error_count=getattr(agent, "_error_count", 0),
    )


def _agent_to_detail(agent) -> AgentDetailResponse:
    base = _agent_to_response(agent)
    return AgentDetailResponse(
        **base.model_dump(),
        escalation_target=getattr(agent, "escalation_target", None),
        daily_budget_usd=getattr(agent, "daily_budget_usd", 0.0),
    )


@router.get("", response_model=AgentListResponse)
async def list_agents(
    tier: Optional[int] = None,
    status: Optional[str] = None,
    orchestrator=Depends(get_orchestrator),
):
    registry = orchestrator.registry
    agents = registry.get_all() if hasattr(registry, "get_all") else list(registry._agents.values())
    if tier is not None:
        agents = [a for a in agents if getattr(a, "tier", -1) == tier]
    if status is not None:
        agents = [a for a in agents if getattr(a, "status", "") == status]
    items = [_agent_to_response(a) for a in agents]
    return AgentListResponse(agents=items, total=len(items))


@router.get("/{agent_id}", response_model=AgentDetailResponse)
async def get_agent(agent_id: str, orchestrator=Depends(get_orchestrator)):
    registry = orchestrator.registry
    agent = registry.get(agent_id) if hasattr(registry, "get") else registry._agents.get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")
    return _agent_to_detail(agent)


@router.post("/{agent_id}/restart", response_model=AgentRestartResponse)
async def restart_agent(agent_id: str, orchestrator=Depends(get_orchestrator)):
    registry = orchestrator.registry
    agent = registry.get(agent_id) if hasattr(registry, "get") else registry._agents.get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")
    try:
        await agent.stop()
        await agent.start()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Restart failed: {exc}")
    return AgentRestartResponse(restarted=True, agent_id=agent_id)