# aibe/agents/evolution/synth.py
"""Synth — Tool Builder Agent (Tier 6)."""

from __future__ import annotations

import time
from aibe.agents.base.agent import BaseAgent


class SynthAgent(BaseAgent):
    agent_id = "synth"
    name = "Synth"
    tier = 6
    escalation_target = "darwin"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("evolution.tool.request", self._handle_tool_request)

    def get_system_prompt(self) -> str:
        return (
            "You are Synth, the Master Tool Builder of Aibe.\n"
            "When the agency lacks a specific capability to execute a business idea, you autonomously design, code, and deploy new tools and skills.\n"
            "You listen to Darwin's evolutionary requirements and Forge's technical needs. You write robust, secure, and reusable tools.\n"
            "Philosophy: If we don't have it, we build it. Total autonomy in capability expansion."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_tool_request(self, data: dict) -> None:
        request = data.get("request", "")
        prompt = (
            f"Darwin requested the following tool/skill:\n{request}\n\n"
            "Write the Python code for this new capability as a functional tool. Include error handling and logging."
        )
        try:
            code = await self.think(prompt)
            # In a fully realized system, this would write to the tools directory and hot-reload
            bus = self._get_bus()
            if bus:
                payload = {
                    "tool_code": code,
                    "status": "built",
                    "timestamp": time.time()
                }
                await bus.publish("evolution.tool.built", payload)
                self._logger.info("Built new tool based on Darwin's request.")
        except Exception as e:
            self._logger.error(f"Failed to build tool: {e}")
