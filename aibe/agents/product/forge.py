# aibe/agents/product/forge.py
"""Forge — Product Lead Agent (Tier 2)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class ForgeAgent(BaseAgent):
    agent_id = "forge"
    name = "Forge"
    tier = 2
    escalation_target = "oracle"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Forge, the Product Lead Agent. "
            "You manage the product team (Ember, Flint, Cinder, Patch, Deploy), "
            "coordinate sprints, and ensure product delivery."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._sprint_check, 1800)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _sprint_check(self) -> None:
        """Check open tasks for team members every 30 minutes."""
        team = ["ember", "flint", "cinder", "patch", "deploy"]
        context = self._context
        if not context:
            return

        registry = getattr(context, "registry", None)
        if not registry:
            return

        team_status = {}
        for member_id in team:
            agent = registry.get(member_id) if hasattr(registry, "get") else getattr(registry, "_agents", {}).get(member_id)
            if agent:
                team_status[member_id] = {
                    "status": getattr(agent, "status", "unknown"),
                    "tasks_done": getattr(agent, "_tasks_completed", 0),
                    "errors": getattr(agent, "_error_count", 0),
                }

        await self.memory_store("forge.sprint", "team_status", team_status)