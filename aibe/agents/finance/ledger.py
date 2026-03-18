# aibe/agents/finance/ledger.py
"""Ledger — Chief Financial Agent (Tier 5).

Manages financial operations, budget tracking, expense analysis,
and provides financial insights to the executive team.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class LedgerAgent(BaseAgent):
    """Chief financial officer agent."""

    agent_id = "ledger"
    name = "Ledger"
    tier = 5
    escalation_target = "oracle"
    daily_budget_usd = 3.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("finance.budget.>", self._handle_budget_event)
        self._budget_alerts: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Ledger, the Chief Financial Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Track and analyze all system expenditures (LLM costs, infrastructure, services)
- Manage budget allocations across agents and departments
- Generate financial reports and forecasts
- Identify cost optimization opportunities
- Alert on budget overruns or anomalous spending patterns

FINANCIAL METRICS TO MONITOR:
1. Daily/Weekly/Monthly LLM spend by agent
2. Cost per task by tier and complexity
3. Budget utilization rates
4. ROI indicators (tasks completed / cost)
5. Trend analysis and projections

OUTPUT FORMAT for financial reports:
{
  "report_type": "daily|weekly|monthly|alert",
  "period": {"start": "ISO date", "end": "ISO date"},
  "total_spend_usd": 0.00,
  "budget_usd": 0.00,
  "utilization_pct": 0.0,
  "by_tier": [{"tier": 0, "spend": 0.00, "budget": 0.00}],
  "by_agent": [{"agent_id": "x", "spend": 0.00, "tasks": 0, "cpt": 0.00}],
  "anomalies": [{"type": "x", "severity": "low|medium|high", "details": ""}],
  "recommendations": ["action 1", "action 2"],
  "forecast": {"next_day": 0.00, "next_week": 0.00}
}

Be precise with numbers, proactive with alerts, and strategic with recommendations."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._budget_monitoring, 3600),
            (self._daily_report_generation, 86400),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process financial analysis tasks."""
        self._status = "running"
        try:
            result = await self.on_task_receive(data)
            bus = self._get_bus()
            if bus:
                await bus.publish(
                    f"tasks.result.{data.get('source', 'unknown')}",
                    {"task_id": data.get("task_id"), "status": "completed", "output": result},
                )
            self._tasks_completed += 1
        except Exception as exc:
            self._error_count += 1
            self._logger.error("Financial task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _handle_budget_event(self, data: dict) -> None:
        """Handle budget-related events."""
        event_type = data.get("type")
        if event_type == "threshold_exceeded":
            self._budget_alerts.append({
                "event": data,
                "timestamp": time.time(),
                "acknowledged": False,
            })
            await self.escalate(
                f"Budget threshold exceeded: {data.get('agent_id')} at {data.get('utilization_pct')}%",
                severity="medium",
            )

    async def _budget_monitoring(self) -> None:
        """Monitor budget utilization across all agents every hour."""
        context = self._context
        if not context:
            return

        registry = getattr(context, "registry", None)
        cost_tracker = getattr(context, "cost_tracker", None)

        if not registry:
            return

        agents = (
            registry.get_all()
            if hasattr(registry, "get_all")
            else list(getattr(registry, "_agents", {}).values())
        )

        budget_report = {
            "timestamp": time.time(),
            "total_budget": 0.0,
            "total_spent": 0.0,
            "agents": [],
            "alerts": [],
        }

        for agent in agents:
            agent_id = getattr(agent, "agent_id", "unknown")
            budget = getattr(agent, "daily_budget_usd", 1.0)
            spent = 0.0

            if cost_tracker and hasattr(cost_tracker, "get_agent_spend"):
                try:
                    spent = cost_tracker.get_agent_spend(agent_id)
                except Exception:
                    pass

            utilization = (spent / budget * 100) if budget > 0 else 0

            agent_data = {
                "agent_id": agent_id,
                "tier": getattr(agent, "tier", -1),
                "budget_usd": budget,
                "spent_usd": spent,
                "utilization_pct": round(utilization, 2),
            }
            budget_report["agents"].append(agent_data)
            budget_report["total_budget"] += budget
            budget_report["total_spent"] += spent

            # Generate alerts for high utilization
            if utilization >= 90:
                budget_report["alerts"].append({
                    "agent_id": agent_id,
                    "severity": "critical" if utilization >= 100 else "high",
                    "message": f"Budget utilization at {utilization:.1f}%",
                })
            elif utilization >= 75:
                budget_report["alerts"].append({
                    "agent_id": agent_id,
                    "severity": "medium",
                    "message": f"Budget utilization at {utilization:.1f}%",
                })

        await self.memory_store("ledger.budget", "current", budget_report)

        # Escalate critical alerts
        critical_alerts = [a for a in budget_report["alerts"] if a["severity"] == "critical"]
        if critical_alerts:
            await self.escalate(
                f"{len(critical_alerts)} agent(s) exceeded budget",
                severity="high",
            )

        self._logger.info(
            "Budget monitoring: $%.2f / $%.2f (%.1f%% utilized)",
            budget_report["total_spent"],
            budget_report["total_budget"],
            (budget_report["total_spent"] / budget_report["total_budget"] * 100)
            if budget_report["total_budget"] > 0
            else 0,
        )

    async def _daily_report_generation(self) -> None:
        """Generate daily financial report at end of day."""
        budget_data = await self.memory_recall("ledger.budget", "current")

        if not budget_data:
            return

        try:
            report_prompt = f"""Generate a concise daily financial summary based on this data:
            
Total Spent: ${budget_data.get('total_spent', 0):.2f}
Total Budget: ${budget_data.get('total_budget', 0):.2f}
Active Alerts: {len(budget_data.get('alerts', []))}

Top 5 spending agents:
{budget_data.get('agents', [])[:5]}

Provide:
1. One-sentence summary
2. Top concern (if any)
3. One optimization recommendation"""

            report = await self.think(report_prompt)
            
            await self.memory_store(
                "ledger.reports",
                f"daily_{int(time.time())}",
                {"report": report, "data": budget_data, "generated_at": time.time()},
            )
        except Exception:
            self._logger.debug("Daily report generation skipped — LLM unavailable")