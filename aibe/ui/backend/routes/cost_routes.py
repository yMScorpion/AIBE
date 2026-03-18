# aibe/ui/backend/routes/cost_routes.py
"""Cost tracking endpoints."""

from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException

from aibe.ui.backend.dependencies import get_orchestrator
from aibe.ui.backend.schemas.cost_schemas import (
    AgentCostDetailResponse,
    AgentCostEntry,
    CostHistoryResponse,
    CostSummaryResponse,
    DailyCostEntry,
    ModelCostEntry,
    TierCostEntry,
)

TIER_NAMES = {
    0: "Executive",
    1: "Research",
    2: "Product",
    3: "Marketing",
    4: "Social",
    5: "Finance",
    6: "Evolution",
    7: "AI/ML",
    8: "Security",
    9: "Sales",
}

router = APIRouter(prefix="/api/costs", tags=["costs"])


def _get_cost_tracker(orchestrator):
    return getattr(orchestrator, "cost_tracker", None)


@router.get("/summary", response_model=CostSummaryResponse)
async def cost_summary(orchestrator=Depends(get_orchestrator)):
    ct = _get_cost_tracker(orchestrator)
    registry = orchestrator.registry
    agents = registry.get_all() if hasattr(registry, "get_all") else list(registry._agents.values())

    by_agent: list[AgentCostEntry] = []
    tier_map: dict[int, dict] = {}
    total_spent = 0.0
    total_budget = 0.0

    for agent in agents:
        aid = getattr(agent, "agent_id", "unknown")
        tier = getattr(agent, "tier", -1)
        budget = getattr(agent, "daily_budget_usd", 1.0)
        spent = 0.0
        if ct is not None and hasattr(ct, "get_agent_spend"):
            try:
                spent = ct.get_agent_spend(aid)
            except Exception:
                spent = 0.0

        utilization = min(round((spent / budget) * 100, 2), 100.0) if budget > 0 else 0.0
        by_agent.append(
            AgentCostEntry(
                agent_id=aid,
                spent_usd=round(spent, 4),
                budget_usd=round(budget, 4),
                utilization_pct=utilization,
            )
        )
        total_spent += spent
        total_budget += budget

        if tier not in tier_map:
            tier_map[tier] = {"spent": 0.0, "count": 0}
        tier_map[tier]["spent"] += spent
        tier_map[tier]["count"] += 1

    by_tier = [
        TierCostEntry(
            tier=t,
            tier_name=TIER_NAMES.get(t, f"Tier {t}"),
            spent_usd=round(info["spent"], 4),
            agent_count=info["count"],
        )
        for t, info in sorted(tier_map.items())
    ]

    return CostSummaryResponse(
        total_spent_usd=round(total_spent, 4),
        total_budget_usd=round(total_budget, 4),
        period="daily",
        by_agent=by_agent,
        by_tier=by_tier,
    )


@router.get("/history", response_model=CostHistoryResponse)
async def cost_history(days: int = 7, orchestrator=Depends(get_orchestrator)):
    ct = _get_cost_tracker(orchestrator)
    history: list[DailyCostEntry] = []
    today = date.today()

    if ct and hasattr(ct, "get_daily_history"):
        raw = ct.get_daily_history(days)
        for entry in raw:
            history.append(DailyCostEntry(date=entry["date"], spent_usd=round(entry["spent_usd"], 4)))
    else:
        for i in range(days):
            d = today - timedelta(days=days - 1 - i)
            history.append(DailyCostEntry(date=d.isoformat(), spent_usd=0.0))

    return CostHistoryResponse(days=days, history=history)


@router.get("/agent/{agent_id}", response_model=AgentCostDetailResponse)
async def cost_agent_detail(agent_id: str, orchestrator=Depends(get_orchestrator)):
    registry = orchestrator.registry
    agent = registry.get(agent_id) if hasattr(registry, "get") else registry._agents.get(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

    ct = _get_cost_tracker(orchestrator)
    budget = getattr(agent, "daily_budget_usd", 1.0)
    total = 0.0
    by_model: list[ModelCostEntry] = []

    if ct and hasattr(ct, "get_agent_detail"):
        detail = ct.get_agent_detail(agent_id)
        total = detail.get("total", 0.0)
        for m in detail.get("models", []):
            by_model.append(
                ModelCostEntry(
                    model=m["model"],
                    calls=m["calls"],
                    tokens_in=m["tokens_in"],
                    tokens_out=m["tokens_out"],
                    cost_usd=round(m["cost_usd"], 4),
                )
            )
    elif ct and hasattr(ct, "get_agent_spend"):
        total = ct.get_agent_spend(agent_id)

    return AgentCostDetailResponse(
        agent_id=agent_id,
        total_spent_usd=round(total, 4),
        budget_usd=round(budget, 4),
        by_model=by_model,
    )