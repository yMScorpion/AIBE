"""Cost tracking and budget routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def cost_summary() -> dict[str, Any]:
    """Get today's cost summary across all categories."""
    # TODO: Wire to CostTracker
    return {
        "llm_spend_usd": 0.0,
        "llm_budget_usd": 50.0,
        "ad_spend_usd": 0.0,
        "ad_budget_usd": 100.0,
        "contractor_spend_usd": 0.0,
        "contractor_budget_usd": 500.0,
        "tokens_input": 0,
        "tokens_output": 0,
    }


@router.get("/agents")
async def agent_costs() -> dict[str, Any]:
    """Get per-agent cost breakdown for today."""
    return {"agents": {}, "total": 0.0}


@router.get("/history")
async def cost_history() -> dict[str, Any]:
    """Get historical cost data for charting."""
    return {"history": [], "days": 0}
