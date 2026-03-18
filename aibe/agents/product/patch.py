# aibe/agents/product/patch.py
"""Patch — Bug Fix & Error Resolution Agent (Tier 2)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class PatchAgent(BaseAgent):
    agent_id = "patch"
    name = "Patch"
    tier = 2
    escalation_target = "forge"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Patch, a Bug Fix Agent. You identify, diagnose, and fix errors across the system."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._error_scan, 300)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _error_scan(self) -> None:
        context = self._context
        if not context:
            return
        registry = getattr(context, "registry", None)
        if not registry:
            return
        agents = registry.get_all() if hasattr(registry, "get_all") else list(getattr(registry, "_agents", {}).values())
        error_agents = [a for a in agents if getattr(a, "_error_count", 0) > 0]
        if error_agents:
            self._logger.info("Found %d agents with errors", len(error_agents))