# aibe/agents/executive/oracle.py
"""Oracle — Chief Executive Agent (Tier 0)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class OracleAgent(BaseAgent):
    agent_id = "oracle"
    name = "Oracle"
    tier = 0
    escalation_target = None  # Top of hierarchy
    daily_budget_usd = 10.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("tasks.escalation.oracle", self._handle_escalation)
        self._alerts: list[dict] = []

    def get_system_prompt(self) -> str:
        return (
            "You are Oracle, the Chief Executive AI Agent of AIBE. "
            "You oversee the entire 40-agent organisation, make strategic decisions, "
            "monitor KPIs, and ensure alignment across all departments. "
            "Be concise, decisive, and data-driven."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._kpi_monitoring_loop, 300),
            (self._strategic_review_loop, 3600),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_escalation(self, data: dict) -> None:
        self._logger.warning("Escalation received from %s: %s", data.get("source"), data.get("message"))
        self._alerts.append({"time": time.time(), **data})

    async def _kpi_monitoring_loop(self) -> None:
        """Monitor system KPIs every 5 minutes."""
        context = self._context
        if context is None:
            return

        registry = getattr(context, "registry", None)
        cost_tracker = getattr(context, "cost_tracker", None)
        if registry is None:
            return

        agents = registry.get_all() if hasattr(registry, "get_all") else list(getattr(registry, "_agents", {}).values())

        error_agents = [a for a in agents if getattr(a, "status", "") == "error"]
        total_tasks = sum(getattr(a, "_tasks_completed", 0) for a in agents)
        total_errors = sum(getattr(a, "_error_count", 0) for a in agents)

        total_spend = 0.0
        if cost_tracker and hasattr(cost_tracker, "get_total_spend"):
            try:
                total_spend = cost_tracker.get_total_spend()
            except Exception:
                pass

        kpi = {
            "total_agents": len(agents),
            "agents_in_error": len(error_agents),
            "total_tasks_completed": total_tasks,
            "total_errors": total_errors,
            "total_spend_usd": total_spend,
        }

        await self.memory_store("oracle.kpis", "latest", kpi)

        if len(error_agents) > 2:
            self._alerts.append({"type": "agent_errors", "count": len(error_agents), "time": time.time()})
            self._logger.warning("KPI Alert: %d agents in error state", len(error_agents))

        daily_budget = sum(getattr(a, "daily_budget_usd", 1.0) for a in agents)
        if daily_budget > 0 and total_spend > daily_budget * 0.8:
            self._logger.warning("KPI Alert: Budget utilisation at %.1f%%", (total_spend / daily_budget) * 100)

    async def _strategic_review_loop(self) -> None:
        """Hourly strategic review using recent data."""
        scout_intel = await self.memory_recall("scout.market_intel", "latest")
        kpis = await self.memory_recall("oracle.kpis", "latest")

        if not kpis:
            return  # No data to review

        prompt = (
            f"Based on the following KPIs, provide a brief strategic assessment with 3 action items:\n"
            f"KPIs: {kpis}\n"
        )
        if scout_intel:
            prompt += f"Market Intelligence: {scout_intel}\n"

        try:
            review = await self.think(prompt)
            await self.memory_store("oracle.strategic_reviews", "latest", {"review": review, "time": time.time()})
        except Exception:
            self._logger.debug("Strategic review skipped — no LLM available")