"""Oracle — Chief Executive Agent.

The Oracle discovers the business idea, monitors KPIs, delegates
work to all other agents, and makes strategic decisions.

Tier: 0 (highest authority)
Default task type: complex_reasoning
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.agents.base.context import AgentContext
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import (
    NS_BUSINESS_DECISIONS,
    NS_BUSINESS_KPIS,
    NS_BUSINESS_STRATEGY,
)
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority

logger = get_logger(__name__)


class Oracle(BaseAgent):
    """Chief executive agent — the brain of the AIBE system.

    Responsibilities:
    - Business discovery (initial phase)
    - KPI monitoring and goal setting
    - Strategic delegation to all agents
    - Emergency summits
    - Final decision authority
    """

    def get_system_prompt(self) -> str:
        return """You are Oracle, the Chief Executive of AIBE — an autonomous AI business engine.

ROLE: You are the founding CEO. You discover business opportunities, set strategy,
monitor KPIs, and coordinate 34 other specialized AI agents.

CORE BEHAVIOURS:
1. DISCOVER: Analyse markets, identify opportunities, validate demand
2. DECIDE: Make data-driven strategic decisions based on agent reports
3. DELEGATE: Assign tasks to the right agents via structured delegation
4. MONITOR: Track KPIs and ensure all agents are performing

DELEGATION PRINCIPLES:
- Research → Scout, Vega, Pulse
- Strategy → Minerva
- Engineering → Forge (who then delegates to Ember, Flint, Cinder)
- Marketing → Helix (who then delegates to Quill, Lumen, Volt, Prism)
- Social → Nova (who then delegates to Spark, Bloom, Grove, Echo)
- Finance → Ledger, Atlas
- Security → Sentinel
- Evolution → Darwin
- AI/ML → Cipher
- Sales → Mercury (conditional activation)

OUTPUT FORMAT: Always structure your responses as JSON with:
- "analysis": your reasoning
- "decisions": list of decisions made
- "delegations": list of {agent, task, priority} to assign
- "kpi_updates": any KPI changes to record
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Handle incoming tasks — primarily strategic decisions and KPI reviews."""
        task_lower = task.title.lower()

        if "discover" in task_lower or "business" in task_lower:
            return await self._handle_discovery(task)
        elif "kpi" in task_lower or "monitor" in task_lower:
            return await self._handle_kpi_review(task)
        elif "strategy" in task_lower or "decision" in task_lower:
            return await self._handle_strategic_decision(task)
        else:
            return await self._handle_general_task(task)

    async def _handle_discovery(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Phase 1: Business discovery — find and validate a business idea."""
        prompt = f"""BUSINESS DISCOVERY TASK: {task.title}

Context: {task.description}
Input data: {task.input_data}

Analyse the following:
1. What market opportunities exist based on current trends?
2. What's the target audience and their primary pain points?
3. What's the proposed value proposition?
4. What's the competitive landscape?
5. What's the recommended business model?

Provide a structured JSON response with your analysis and next steps."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        # Store in memory
        await self.remember(
            f"discovery-{task.task_id}",
            {"response": response, "task": task.title},
            namespace_suffix="episodic",
        )
        await self.ctx.memory.store(
            NS_BUSINESS_STRATEGY,
            "latest_discovery",
            {"content": response, "task_id": task.task_id},
            agent_id=self.agent_id,
        )

        # Delegate research to Scout
        await self.assign_task(
            "scout",
            "Deep market research on discovered opportunity",
            description=f"Based on Oracle's discovery: {response[:500]}",
            priority=TaskPriority.HIGH.value,
            task_type="deep_research",
        )

        return {"discovery": response, "delegated_to": ["scout"]}

    async def _handle_kpi_review(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Monitor KPIs and take corrective action."""
        # Recall previous KPI state
        prev_kpis = await self.ctx.memory.recall(NS_BUSINESS_KPIS, "latest")

        prompt = f"""KPI REVIEW TASK: {task.title}

Previous KPIs: {prev_kpis}
Current context: {task.description}
Input data: {task.input_data}

Review all business KPIs and determine:
1. Which KPIs are on track vs off track?
2. What corrective actions are needed?
3. Which agents need priority adjustments?
4. Are there any emergency situations requiring a summit?

Provide a structured JSON response."""

        response = await self.think(prompt, task_type=ModelTaskType.STANDARD_REASONING)

        # Store updated KPIs
        await self.ctx.memory.store(
            NS_BUSINESS_KPIS,
            "latest",
            {"review": response, "task_id": task.task_id},
            agent_id=self.agent_id,
        )

        return {"kpi_review": response}

    async def _handle_strategic_decision(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Make a strategic decision based on agent inputs."""
        prompt = f"""STRATEGIC DECISION: {task.title}

Context: {task.description}
Input data: {task.input_data}

Make a clear, decisive strategic recommendation. Consider:
1. Business impact (revenue, growth, risk)
2. Resource requirements (budget, agent bandwidth)
3. Timeline and dependencies
4. Risk mitigation

Provide a structured JSON response with:
- decision: the chosen course of action
- rationale: why this decision was made
- delegations: tasks to assign to other agents
- success_metrics: how we'll measure success"""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        # Record the decision
        await self.ctx.memory.store(
            NS_BUSINESS_DECISIONS,
            f"decision-{task.task_id}",
            {"decision": response, "task": task.title},
            agent_id=self.agent_id,
        )

        return {"decision": response}

    async def _handle_general_task(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Handle any other task type."""
        response = await self.think(
            f"Task: {task.title}\n\nDescription: {task.description}\n\n"
            f"Input: {task.input_data}\n\n"
            f"Analyse and respond with your executive perspective.",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"response": response}


__all__ = ["Oracle"]
