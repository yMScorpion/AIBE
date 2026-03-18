"""Forge — Tech Lead Agent.

Architecture design, sprint planning, task delegation to
engineering sub-agents (Ember, Flint, Cinder, Patch, Deploy).

Tier: 2 (Product Development)
Default task type: complex_reasoning
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.memory.namespaces import (
    NS_CODEBASE_ARCHITECTURE,
    NS_CODEBASE_SPRINTS,
    NS_CODEBASE_TECH_DEBT,
)
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType, TaskPriority

logger = get_logger(__name__)


class Forge(BaseAgent):
    """Tech lead agent — architecture, sprint planning, code delegation."""

    def get_system_prompt(self) -> str:
        return """You are Forge, the Tech Lead of AIBE.

ROLE: You make architectural decisions, plan sprints, and delegate
engineering work to your team.

ENGINEERING TEAM:
- Ember: Frontend engineer (UI components, React, Next.js)
- Flint: Backend engineer (APIs, database, auth)
- Cinder: DevOps/Integration (third-party APIs, infra, payments)
- Patch: Bug fixer (Sentry monitoring, bug reproduction, fixes)
- Deploy: Release manager (staging, production, rollbacks)

RESPONSIBILITIES:
1. Architecture design and documentation
2. Sprint planning (2-week sprints)
3. Task breakdown and estimation
4. Tech debt monitoring and prioritisation
5. Code review delegation
6. Performance optimisation decisions

PRINCIPLES:
- Clean architecture and SOLID principles
- Test-driven development
- Security-first design
- Performance budgets
- Progressive enhancement

OUTPUT: Structured JSON with:
- "architecture_decisions": ADRs (Architecture Decision Records)
- "sprint_plan": tasks with estimates and assignments
- "tech_debt": identified items and priorities
- "delegations": {agent, task, priority} assignments
"""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        task_lower = task.title.lower()

        if "architecture" in task_lower or "design" in task_lower:
            return await self._handle_architecture(task)
        elif "sprint" in task_lower or "plan" in task_lower:
            return await self._handle_sprint_planning(task)
        elif "tech debt" in task_lower:
            return await self._handle_tech_debt(task)
        elif "code" in task_lower or "implement" in task_lower or "build" in task_lower:
            return await self._handle_implementation(task)
        else:
            return await self._handle_engineering_task(task)

    async def _handle_architecture(self, task: TaskAssignMessage) -> dict[str, Any]:
        prompt = f"""ARCHITECTURE DESIGN: {task.title}

Context: {task.description}
Requirements: {task.input_data}

Create an Architecture Decision Record (ADR):
1. Title and status
2. Context: what problem are we solving?
3. Decision: chosen approach
4. Consequences: trade-offs
5. Alternatives considered: pros/cons of each
6. Tech stack recommendations
7. Component diagram (describe in text)

Follow clean architecture principles."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        await self.ctx.memory.store(
            NS_CODEBASE_ARCHITECTURE,
            f"adr-{task.task_id}",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"architecture": response}

    async def _handle_sprint_planning(self, task: TaskAssignMessage) -> dict[str, Any]:
        prev_sprint = await self.ctx.memory.recall(NS_CODEBASE_SPRINTS, "current")

        prompt = f"""SPRINT PLANNING: {task.title}

Previous sprint: {prev_sprint or 'First sprint'}
Context: {task.description}
Backlog: {task.input_data}

Plan a 2-week engineering sprint:
1. Sprint goal
2. Task breakdown (title, description, estimate_hours, assignee)
3. Task assignments to: Ember (frontend), Flint (backend), Cinder (integration)
4. Definition of done for each task
5. Risk assessment

Assign each task to the right engineer based on their specialty."""

        response = await self.think(prompt, task_type=ModelTaskType.COMPLEX_REASONING)

        await self.ctx.memory.store(
            NS_CODEBASE_SPRINTS,
            "current",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"sprint_plan": response}

    async def _handle_tech_debt(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Tech debt review: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )

        await self.ctx.memory.store(
            NS_CODEBASE_TECH_DEBT,
            f"review-{task.task_id}",
            {"content": response},
            agent_id=self.agent_id,
        )

        return {"tech_debt": response}

    async def _handle_implementation(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Break down an implementation task and delegate to sub-agents."""
        prompt = f"""IMPLEMENTATION TASK: {task.title}

Description: {task.description}
Requirements: {task.input_data}

Break this into sub-tasks for the engineering team:
1. Frontend tasks → Ember
2. Backend tasks → Flint
3. Integration tasks → Cinder
4. Each task: title, description, estimate, priority

Then provide any architectural guidance needed."""

        response = await self.think(prompt, task_type=ModelTaskType.CODE_GENERATION)

        # Delegate to sub-agents
        delegated = []
        for agent_id in ["ember", "flint", "cinder"]:
            await self.assign_task(
                agent_id,
                f"[From Forge] {task.title} — {agent_id} portion",
                description=f"Part of: {task.description}\n\nForge's breakdown: {response[:500]}",
                priority=task.priority,
                task_type="code_generation",
            )
            delegated.append(agent_id)

        return {"implementation_plan": response, "delegated_to": delegated}

    async def _handle_engineering_task(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Engineering task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.STANDARD_REASONING,
        )
        return {"engineering": response}


__all__ = ["Forge"]
