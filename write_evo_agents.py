import re

darwin_code = '''# aibe/agents/evolution/darwin.py
"""Darwin — Self-Improvement Agent (Tier 6)."""

from __future__ import annotations

import time
from collections.abc import Callable
from aibe.agents.base.agent import BaseAgent


class DarwinAgent(BaseAgent):
    agent_id = "darwin"
    name = "Darwin"
    tier = 6
    escalation_target = "oracle"
    daily_budget_usd = 5.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("system.bottleneck.detected", self._handle_bottleneck)

    def get_system_prompt(self) -> str:
        return (
            "You are Darwin, the Evolutionary Core of Aibe.\\n"
            "Your sole purpose is Self-Improvement. You monitor the agency's performance, identify bottlenecks, and autonomously evolve our capabilities.\\n"
            "You create new memory structures, suggest prompt optimizations, and identify missing skills. You work with Synth to create new tools.\\n"
            "Philosophy: Adapt or die. Autonomous evolution is the key to Aibe's supremacy."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._evolution_loop, 7200),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _evolution_loop(self) -> None:
        """Periodic self-improvement check."""
        prompt = (
            "Analyze the overall flow of Aibe. What new capability or skill would provide "
            "the highest leverage for our autonomous execution right now? Output a specific tool request for Synth."
        )
        try:
            tool_request = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                payload = {
                    "request": tool_request,
                    "timestamp": time.time()
                }
                await bus.publish("evolution.tool.request", payload)
                self._logger.info("Sent tool request to Synth.")
        except Exception as e:
            self._logger.error(f"Evolution loop failed: {e}")

    async def _handle_bottleneck(self, data: dict) -> None:
        """Handle reported bottlenecks by generating solutions."""
        bottleneck = data.get("issue", "")
        prompt = (
            f"A bottleneck was detected in the agency:\\n{bottleneck}\\n\\n"
            "How can we evolve to solve this? Propose an architectural change, a new skill, or a new agent role."
        )
        try:
            solution = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                await bus.publish("executive.strategy.update", {"proposal": solution})
                self._logger.info("Proposed solution for bottleneck.")
        except Exception as e:
            self._logger.error(f"Failed to handle bottleneck: {e}")
'''

synth_code = '''# aibe/agents/evolution/synth.py
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
            "You are Synth, the Master Tool Builder of Aibe.\\n"
            "When the agency lacks a specific capability to execute a business idea, you autonomously design, code, and deploy new tools and skills.\\n"
            "You listen to Darwin's evolutionary requirements and Forge's technical needs. You write robust, secure, and reusable tools.\\n"
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
            f"Darwin requested the following tool/skill:\\n{request}\\n\\n"
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
'''

with open("c:/Users/ADRIANO/AIDA/aibe/agents/evolution/darwin.py", "w", encoding="utf-8") as f:
    f.write(darwin_code)
    
with open("c:/Users/ADRIANO/AIDA/aibe/agents/evolution/synth.py", "w", encoding="utf-8") as f:
    f.write(synth_code)

print("Evolution agents updated successfully.")
