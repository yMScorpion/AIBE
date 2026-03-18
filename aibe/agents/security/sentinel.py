# aibe/agents/security/sentinel.py
"""Sentinel — Chief Security Agent (Tier 8)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class SentinelAgent(BaseAgent):
    agent_id = "sentinel"
    name = "Sentinel"
    tier = 8
    escalation_target = "oracle"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("tasks.escalation.sentinel", self._handle_escalation)
        self._incidents: list[dict] = []

    def get_system_prompt(self) -> str:
        return (
            "You are Sentinel, the Chief Security Agent. "
            "You oversee all security operations, coordinate the security team, "
            "and maintain the organisation's security posture. Be vigilant and decisive."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._security_dashboard_loop, 600),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_escalation(self, data: dict) -> None:
        self._logger.warning("Security escalation from %s: %s", data.get("source"), data.get("message"))
        self._incidents.append({"time": time.time(), **data})

    async def _security_dashboard_loop(self) -> None:
        """Aggregate security status every 10 minutes."""
        context = self._context
        if context is None:
            return

        registry = getattr(context, "registry", None)
        if registry is None:
            return

        agents = registry.get_all() if hasattr(registry, "get_all") else list(getattr(registry, "_agents", {}).values())
        security_agents = [a for a in agents if getattr(a, "tier", -1) == 8]

        total_agents = len(agents)
        error_agents = sum(1 for a in agents if getattr(a, "status", "") == "error")
        sec_agents_ok = sum(1 for a in security_agents if getattr(a, "status", "") in ("ready", "running"))
        recent_incidents = len([i for i in self._incidents if time.time() - i.get("time", 0) < 3600])

        # Security score: start at 100, deduct for issues
        score = 100
        score -= error_agents * 5  # -5 per error agent
        score -= recent_incidents * 10  # -10 per recent incident
        score -= max(0, len(security_agents) - sec_agents_ok) * 15  # -15 per security agent down
        score = max(0, min(100, score))

        dashboard = {
            "security_score": score,
            "total_agents": total_agents,
            "error_agents": error_agents,
            "security_agents_ok": sec_agents_ok,
            "security_agents_total": len(security_agents),
            "recent_incidents": recent_incidents,
            "updated_at": time.time(),
        }

        await self.memory_store("sentinel.dashboard", "latest", dashboard)
        self._logger.info("Security score: %d/100", score)