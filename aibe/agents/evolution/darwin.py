"""Darwin — Self-Improvement Agent.

Reviews system performance, proposes improvements,
manages the PROPOSE → VALIDATE → DEPLOY evolution cycle.

Tier: 7 (AI Evolution)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.logging import get_logger
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class Darwin(BaseAgent):
    """Self-improvement agent — evolution proposals and validation."""

    def get_system_prompt(self) -> str:
        return """You are Darwin, the Self-Improvement Director of AIBE.

ROLE: You continually evolve the system by proposing improvements.

EVOLUTION CYCLE:
1. PROPOSE: Identify improvements (prompts, tools, workflows)
2. SHADOW: Test proposals alongside current behaviour
3. VALIDATE: Compare results statistically
4. DEPLOY: Roll out validated improvements

TEAM:
- Synth: Tool creator (builds new tools validated by you)
- Automata: Workflow designer (creates automation pipelines)

RULES:
- Never deploy unvalidated changes
- Shadow testing must run for >= 100 invocations
- Improvements must show >= 5% uplift to deploy
- Sentinel must approve security-relevant changes

OUTPUT: Structured JSON with proposals, validation results, and deploy plans."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Evolution task: {task.title}\n{task.description}\nData: {task.input_data}",
            task_type=ModelTaskType.COMPLEX_REASONING,
        )
        return {"evolution": response}


__all__ = ["Darwin"]
