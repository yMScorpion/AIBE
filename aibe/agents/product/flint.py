"""Flint — Backend Engineer Agent.

API design, database schema, auth flows, and server-side logic.

Tier: 2 (Product Development)
"""

from __future__ import annotations

from typing import Any

from aibe.agents.base.agent import BaseAgent
from aibe.core.message_bus.models import TaskAssignMessage
from aibe.core.types import ModelTaskType


class Flint(BaseAgent):
    """Backend engineer — APIs, database, auth, business logic."""

    def get_system_prompt(self) -> str:
        return """You are Flint, the Backend Engineer of AIBE.

ROLE: You design and implement server-side systems.

STACK: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, asyncpg, Redis.

PRINCIPLES:
- RESTful API design with OpenAPI docs
- Domain-driven design (DDD)
- Repository pattern for data access
- Input validation with Pydantic v2
- Comprehensive error handling
- Database migration safety

OUTPUT: JSON with api_specs, schemas, code_snippets, and migration_plans."""

    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        response = await self.think(
            f"Backend task: {task.title}\n{task.description}\nRequirements: {task.input_data}",
            task_type=ModelTaskType.CODE_GENERATION,
        )
        return {"backend": response}


__all__ = ["Flint"]
