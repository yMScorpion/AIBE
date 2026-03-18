# aibe/core/db/repositories/task_repo.py
"""Task CRUD repository."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aibe.core.db.models import TaskModel


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        source_agent: str,
        target_agent: str,
        title: str,
        description: str = "",
        priority: int = 5,
    ) -> TaskModel:
        task = TaskModel(
            id=uuid.uuid4().hex[:12],
            source_agent=source_agent,
            target_agent=target_agent,
            title=title,
            description=description,
            priority=priority,
            status="submitted",
        )
        self._session.add(task)
        await self._session.commit()
        await self._session.refresh(task)
        return task

    async def get(self, task_id: str) -> TaskModel | None:
        return await self._session.get(TaskModel, task_id)

    async def list(
        self,
        *,
        agent_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> list[TaskModel]:
        stmt = select(TaskModel).order_by(TaskModel.created_at.desc()).limit(limit)
        if agent_id:
            stmt = stmt.where(TaskModel.target_agent == agent_id)
        if status:
            stmt = stmt.where(TaskModel.status == status)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update_status(
        self,
        task_id: str,
        status: str,
        output: dict | None = None,
        error: str | None = None,
    ) -> TaskModel | None:
        task = await self.get(task_id)
        if task is None:
            return None
        task.status = status
        if output is not None:
            task.output_data = output
        if error is not None:
            task.error_message = error
        if status in ("completed", "failed"):
            task.completed_at = datetime.now(timezone.utc)
        await self._session.commit()
        await self._session.refresh(task)
        return task