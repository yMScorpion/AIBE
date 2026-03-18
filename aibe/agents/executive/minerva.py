# aibe/agents/executive/minerva.py
"""Minerva — Chief Strategy Agent (Tier 0)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class MinervaAgent(BaseAgent):
    agent_id = "minerva"
    name = "Minerva"
    tier = 0
    escalation_target = "oracle"
    daily_budget_usd = 8.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)

    def get_system_prompt(self) -> str:
        return (
            "You are Minerva, the Chief Strategy Agent of AIBE. "
            "You define OKRs, track strategic objectives, and ensure all departments "
            "are aligned with the organisation's goals. Be analytical and structured."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._okr_tracking_loop, 1800),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _okr_tracking_loop(self) -> None:
        """Track OKR progress every 30 minutes."""
        okrs = await self.memory_recall("minerva.okrs", "current")
        if not okrs:
            # Initialize default OKRs
            default_okrs = {
                "objectives": [
                    {
                        "title": "System Stability",
                        "key_results": [
                            {"kr": "Agent uptime > 99%", "score": 0.0},
                            {"kr": "Error rate < 1%", "score": 0.0},
                        ],
                    },
                    {
                        "title": "Cost Efficiency",
                        "key_results": [
                            {"kr": "Daily spend < $50", "score": 0.0},
                            {"kr": "Budget utilisation < 80%", "score": 0.0},
                        ],
                    },
                ],
                "updated_at": time.time(),
            }
            await self.memory_store("minerva.okrs", "current", default_okrs)
            return

        # Update scores based on current system state
        kpis = await self.memory_recall("oracle.kpis", "latest")
        if kpis:
            for obj in okrs.get("objectives", []):
                for kr in obj.get("key_results", []):
                    if "uptime" in kr["kr"].lower():
                        error_agents = kpis.get("agents_in_error", 0)
                        total = kpis.get("total_agents", 1)
                        kr["score"] = round(1.0 - (error_agents / max(total, 1)), 2)
                    elif "error rate" in kr["kr"].lower():
                        total_errors = kpis.get("total_errors", 0)
                        total_tasks = kpis.get("total_tasks_completed", 1)
                        rate = total_errors / max(total_tasks, 1)
                        kr["score"] = round(max(0, 1.0 - rate * 100), 2)
                    elif "daily spend" in kr["kr"].lower():
                        spend = kpis.get("total_spend_usd", 0)
                        kr["score"] = round(min(1.0, max(0, 1.0 - spend / 50)), 2)

            okrs["updated_at"] = time.time()
            await self.memory_store("minerva.okrs", "current", okrs)