# aibe/ui/backend/routes/metrics_routes.py
"""Prometheus metrics endpoint."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, Response

from aibe.ui.backend.dependencies import get_orchestrator

router = APIRouter(tags=["metrics"])


def _generate_metrics(orchestrator) -> str:
    """Generate Prometheus-format metrics."""
    lines: list[str] = []
    
    # Metric help and type declarations
    lines.append("# HELP aibe_agents_total Total number of agents")
    lines.append("# TYPE aibe_agents_total gauge")
    
    lines.append("# HELP aibe_agent_status Agent status (1=active)")
    lines.append("# TYPE aibe_agent_status gauge")
    
    lines.append("# HELP aibe_agent_tasks_completed Total tasks completed by agent")
    lines.append("# TYPE aibe_agent_tasks_completed counter")
    
    lines.append("# HELP aibe_agent_errors_total Total errors by agent")
    lines.append("# TYPE aibe_agent_errors_total counter")
    
    lines.append("# HELP aibe_agent_uptime_seconds Agent uptime in seconds")
    lines.append("# TYPE aibe_agent_uptime_seconds gauge")
    
    lines.append("# HELP aibe_budget_utilization_percent Budget utilization percentage")
    lines.append("# TYPE aibe_budget_utilization_percent gauge")

    # Collect agent metrics
    registry = orchestrator.registry
    agents = (
        registry.get_all()
        if hasattr(registry, "get_all")
        else list(getattr(registry, "_agents", {}).values())
    )

    lines.append(f"aibe_agents_total {len(agents)}")

    for agent in agents:
        agent_id = getattr(agent, "agent_id", "unknown")
        tier = getattr(agent, "tier", -1)
        status = getattr(agent, "status", "unknown")
        tasks = getattr(agent, "_tasks_completed", 0)
        errors = getattr(agent, "_error_count", 0)
        start_time = getattr(agent, "_start_time", 0)
        budget = getattr(agent, "daily_budget_usd", 1.0)

        # Labels for this agent
        labels = f'agent_id="{agent_id}",tier="{tier}"'

        # Status (1 if running/ready, 0 otherwise)
        is_active = 1 if status in ("running", "ready") else 0
        lines.append(f'aibe_agent_status{{{labels},status="{status}"}} {is_active}')

        # Tasks completed
        lines.append(f"aibe_agent_tasks_completed{{{labels}}} {tasks}")

        # Errors
        lines.append(f"aibe_agent_errors_total{{{labels}}} {errors}")

        # Uptime
        uptime = time.time() - start_time if start_time > 0 else 0
        lines.append(f"aibe_agent_uptime_seconds{{{labels}}} {uptime:.1f}")

        # Budget utilization (would need cost tracker integration)
        # For now, estimate based on task count
        estimated_spend = tasks * 0.01  # Rough estimate
        utilization = min(100, (estimated_spend / budget * 100)) if budget > 0 else 0
        lines.append(f"aibe_budget_utilization_percent{{{labels}}} {utilization:.2f}")

    return "\n".join(lines) + "\n"


@router.get("/metrics")
async def metrics(orchestrator=Depends(get_orchestrator)):
    """Prometheus metrics endpoint."""
    content = _generate_metrics(orchestrator)
    return Response(
        content=content,
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )