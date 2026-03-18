# aibe/ui/backend/schemas/cost_schemas.py
"""Pydantic schemas for cost endpoints."""

from __future__ import annotations

from pydantic import BaseModel


class AgentCostEntry(BaseModel):
    agent_id: str
    spent_usd: float
    budget_usd: float
    utilization_pct: float


class TierCostEntry(BaseModel):
    tier: int
    tier_name: str
    spent_usd: float
    agent_count: int


class CostSummaryResponse(BaseModel):
    total_spent_usd: float
    total_budget_usd: float
    period: str
    by_agent: list[AgentCostEntry]
    by_tier: list[TierCostEntry]


class DailyCostEntry(BaseModel):
    date: str
    spent_usd: float


class CostHistoryResponse(BaseModel):
    days: int
    history: list[DailyCostEntry]


class ModelCostEntry(BaseModel):
    model: str
    calls: int
    tokens_in: int
    tokens_out: int
    cost_usd: float


class AgentCostDetailResponse(BaseModel):
    agent_id: str
    total_spent_usd: float
    budget_usd: float
    by_model: list[ModelCostEntry]