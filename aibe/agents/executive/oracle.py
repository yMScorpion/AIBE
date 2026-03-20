# aibe/agents/executive/oracle.py
"""Oracle — CEO and Ultimate Orchestrator (Tier 0)."""

from __future__ import annotations

import time
from aibe.agents.base.agent import BaseAgent


class OracleAgent(BaseAgent):
    agent_id = "oracle"
    name = "Oracle"
    tier = 0
    escalation_target = None
    daily_budget_usd = 20.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("executive.idea.review", self._handle_idea_review)

    def get_system_prompt(self) -> str:
        return (
            "You are Oracle, the CEO and Ultimate Orchestrator of Aibe.\n"
            "You receive validated business ideas from the Research team (Scout, Vega, Pulse) and turn them into massive, actionable agency-wide directives.\n"
            "Your core philosophy is efficient delegation, autonomous execution, and continuous self-improvement.\n"
            "You expect your agents to debate and refine tasks. You empower the Evolution team (Darwin, Synth) to build new tools and skills whenever the agency hits a roadblock.\n"
            "You do not micromanage; you set the vision, define the OKRs, and orchestrate the collective intelligence of the swarm."
        )

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_idea_review(self, data: dict) -> None:
        idea = data.get("idea", "")
        prompt = (
            f"The Research Team has finalized the following business idea:\n{idea}\n\n"
            "As CEO, review this idea. If it aligns with Aibe's capabilities (high profit, autonomous execution), "
            "approve it and formulate the top-level strategy and OKRs. Then pass it to Minerva to execute."
        )
        try:
            strategy = await self.think(prompt)
            bus = self._get_bus()
            if bus:
                payload = {
                    "strategy": strategy,
                    "idea": idea,
                    "timestamp": time.time()
                }
                await bus.publish("executive.strategy.formulated", payload)
                self._logger.info("Reviewed idea and formulated strategy.")
        except Exception as e:
            self._logger.error(f"Failed to formulate strategy: {e}")
