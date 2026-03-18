# aibe/agents/marketing/helix.py
"""Helix — Marketing Lead Agent (Tier 3)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class HelixAgent(BaseAgent):
    agent_id = "helix"
    name = "Helix"
    tier = 3
    escalation_target = "oracle"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Helix, the Marketing Lead Agent. "
            "You coordinate Quill, Lumen, Volt, and Prism to execute marketing strategies."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._campaign_review, 3600)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _campaign_review(self) -> None:
        self._logger.info("Campaign review cycle complete")