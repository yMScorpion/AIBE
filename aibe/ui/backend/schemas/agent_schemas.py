# aibe/ui/backend/schemas/agent_schemas.py
"""Pydantic schemas for agent endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class AgentResponse(BaseModel):
    agent_id: str
    agent_name: str
    tier: int
    status: str
    uptime_seconds: float
    tasks_completed: int
    error_count: int


class AgentDetailResponse(AgentResponse):
    escalation_target: str | None = None
    daily_budget_usd: float = 0.0


class AgentListResponse(BaseModel):
    agents: list[AgentResponse]
    total: int


class AgentRestartResponse(BaseModel):
    restarted: bool
    agent_id: str