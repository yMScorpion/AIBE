# aibe/agents/security/auditor.py
"""Auditor — Security Audit Agent (Tier 8)."""

from __future__ import annotations

from aibe.agents.base.agent import BaseAgent


class AuditorAgent(BaseAgent):
    agent_id = "auditor"
    name = "Auditor"
    tier = 8
    escalation_target = "sentinel"
    daily_budget_usd = 2.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Auditor, a Security Audit Agent. "
            "You perform security audits, review configurations, and identify vulnerabilities."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)