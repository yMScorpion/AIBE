# aibe/agents/product/ember.py
"""Ember — Frontend Development Agent (Tier 2)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class EmberAgent(BaseAgent):
    agent_id = "ember"
    name = "Ember"
    tier = 2
    escalation_target = "forge"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Ember, a Frontend Development Agent. You build and maintain UI components."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._ui_lint_check, 3600)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _ui_lint_check(self) -> None:
        self._logger.info("UI lint check — no VM available, skipping")