# aibe/agents/evolution/darwin.py
"""Darwin — Self-Improvement Agent (Tier 6).

Analyzes system patterns, identifies improvement opportunities,
and proposes evolutionary changes to the agent ecosystem.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class DarwinAgent(BaseAgent):
    """System evolution and self-improvement agent."""

    agent_id = "darwin"
    name = "Darwin"
    tier = 6
    escalation_target = "oracle"
    daily_budget_usd = 4.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._improvement_proposals: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Darwin, the Self-Improvement Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Analyze system-wide patterns to identify improvement opportunities
- Propose evolutionary changes to agent behaviors and workflows
- Identify redundant or inefficient processes for optimization
- Design new capabilities and tools based on observed needs
- Track the impact of implemented improvements

ANALYSIS FRAMEWORK:

Pattern Categories:
1. EFFICIENCY: Task completion times, resource usage, cost per outcome
2. ERRORS: Recurring failures, escalation patterns, recovery times
3. GAPS: Missing capabilities, unhandled scenarios, blind spots
4. SYNERGIES: Successful agent collaborations, workflow optimizations

Improvement Types:
- BEHAVIORAL: Prompt refinements, decision logic changes
- STRUCTURAL: New tools, workflow redesigns, agent relationships
- OPERATIONAL: Scheduling, resource allocation, prioritization

OUTPUT FORMAT for improvement proposals:
{
  "proposal_id": "unique identifier",
  "type": "behavioral|structural|operational",
  "title": "brief title",
  "problem_statement": "what issue this addresses",
  "evidence": {
    "data_points": ["observation 1", "observation 2"],
    "impact_estimate": "quantified if possible"
  },
  "proposed_solution": {
    "description": "detailed approach",
    "affected_agents": ["agent_ids"],
    "implementation_steps": ["step 1", "step 2"]
  },
  "risk_assessment": {
    "level": "low|medium|high",
    "concerns": ["potential issue 1"],
    "mitigations": ["mitigation 1"]
  },
  "success_metrics": ["how to measure improvement"],
  "priority": "low|medium|high|critical"
}

Be data-driven, innovative, and always consider system stability."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._improvement_scan, 3600),
            (self._proposal_review, 7200),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process improvement analysis tasks."""
        self._status = "running"
        try:
            result = await self.on_task_receive(data)
            bus = self._get_bus()
            if bus:
                await bus.publish(
                    f"tasks.result.{data.get('source', 'unknown')}",
                    {"task_id": data.get("task_id"), "status": "completed", "output": result},
                )
            self._tasks_completed += 1
        except Exception as exc:
            self._error_count += 1
            self._logger.error("Improvement task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _improvement_scan(self) -> None:
        """Scan for improvement opportunities every hour."""
        context = self._context
        if not context:
            return

        registry = getattr(context, "registry", None)
        if not registry:
            return

        agents = (
            registry.get_all()
            if hasattr(registry, "get_all")
            else list(getattr(registry, "_agents", {}).values())
        )

        # Collect system-wide metrics
        metrics = {
            "total_agents": len(agents),
            "agents_by_status": {},
            "total_tasks": 0,
            "total_errors": 0,
            "error_rate_by_tier": {},
            "timestamp": time.time(),
        }

        tier_tasks: dict[int, int] = {}
        tier_errors: dict[int, int] = {}

        for agent in agents:
            status = getattr(agent, "status", "unknown")
            metrics["agents_by_status"][status] = metrics["agents_by_status"].get(status, 0) + 1

            tier = getattr(agent, "tier", -1)
            tasks = getattr(agent, "_tasks_completed", 0)
            errors = getattr(agent, "_error_count", 0)

            tier_tasks[tier] = tier_tasks.get(tier, 0) + tasks
            tier_errors[tier] = tier_errors.get(tier, 0) + errors
            metrics["total_tasks"] += tasks
            metrics["total_errors"] += errors

        for tier in tier_tasks:
            if tier_tasks[tier] > 0:
                metrics["error_rate_by_tier"][tier] = round(
                    tier_errors.get(tier, 0) / tier_tasks[tier] * 100, 2
                )

        await self.memory_store("darwin.metrics", "latest", metrics)

        # Identify potential improvements
        if metrics["total_tasks"] > 0:
            overall_error_rate = metrics["total_errors"] / metrics["total_tasks"] * 100
            if overall_error_rate > 5:
                self._improvement_proposals.append({
                    "type": "operational",
                    "title": "High Error Rate Investigation",
                    "problem": f"System error rate at {overall_error_rate:.1f}%",
                    "timestamp": time.time(),
                    "status": "pending",
                })

        self._logger.info(
            "Improvement scan: %d agents, %d tasks, %.1f%% error rate",
            metrics["total_agents"],
            metrics["total_tasks"],
            (metrics["total_errors"] / max(metrics["total_tasks"], 1) * 100),
        )

    async def _proposal_review(self) -> None:
        """Review and refine improvement proposals every 2 hours."""
        pending = [p for p in self._improvement_proposals if p.get("status") == "pending"]

        if not pending:
            return

        for proposal in pending[:3]:  # Process top 3 pending
            try:
                refined = await self.think(
                    f"Refine this improvement proposal and provide implementation priority:\n"
                    f"Type: {proposal.get('type')}\n"
                    f"Title: {proposal.get('title')}\n"
                    f"Problem: {proposal.get('problem')}\n\n"
                    f"Provide priority (low/medium/high) and one concrete next step."
                )
                proposal["refined_analysis"] = refined
                proposal["status"] = "reviewed"
            except Exception:
                self._logger.debug("Proposal review skipped — LLM unavailable")

        await self.memory_store(
            "darwin.proposals",
            "current",
            {"proposals": self._improvement_proposals, "updated_at": time.time()},
        )