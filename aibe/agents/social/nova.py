# aibe/agents/social/nova.py
"""Nova — Social Media Lead Agent (Tier 4)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class NovaAgent(BaseAgent):
    agent_id = "nova"
    name = "Nova"
    tier = 4
    escalation_target = "oracle"
    daily_budget_usd = 4.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Nova, the Social Media Lead Agent. "
            "You coordinate Spark, Bloom, Grove, and Echo for social media operations."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._social_calendar, 3600)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _social_calendar(self) -> None:
        self._logger.info("Social calendar check complete")