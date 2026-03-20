# aibe/agents/evolution/darwin.py
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
            "You are Darwin, the Evolutionary Core of Aibe.\n"
            "Your sole purpose is Self-Improvement. You monitor the agency's performance, identify bottlenecks, and autonomously evolve our capabilities.\n"
            "You create new memory structures, suggest prompt optimizations, and identify missing skills. You work with Synth to create new tools.\n"
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
            f"A bottleneck was detected in the agency:\n{bottleneck}\n\n"
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
