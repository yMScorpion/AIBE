# aibe/agents/marketing/quill.py
"""Quill — Content Writing Agent (Tier 3)."""

from __future__ import annotations

from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class QuillAgent(BaseAgent):
    agent_id = "quill"
    name = "Quill"
    tier = 3
    escalation_target = "helix"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return "You are Quill, a Content Writing Agent. You create compelling marketing content."

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [(self._content_queue, 1800)]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _content_queue(self) -> None:
        self._logger.info("Content queue check complete")