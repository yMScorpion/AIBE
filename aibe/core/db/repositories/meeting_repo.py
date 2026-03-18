# aibe/core/db/repositories/meeting_repo.py
"""Meeting CRUD repository."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aibe.core.db.models import MeetingModel


class MeetingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        topic: str,
        participants: list[str],
        meeting_type: str = "general",
        max_rounds: int = 3,
    ) -> MeetingModel:
        meeting = MeetingModel(
            id=uuid.uuid4().hex[:12],
            topic=topic,
            participants=participants,
            meeting_type=meeting_type,
            max_rounds=max_rounds,
            status="pending",
        )
        self._session.add(meeting)
        await self._session.commit()
        await self._session.refresh(meeting)
        return meeting

    async def get(self, meeting_id: str) -> MeetingModel | None:
        return await self._session.get(MeetingModel, meeting_id)

    async def list(
        self,
        *,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> list[MeetingModel]:
        stmt = select(MeetingModel).order_by(MeetingModel.created_at.desc()).limit(limit)
        if status:
            stmt = stmt.where(MeetingModel.status == status)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self,
        meeting_id: str,
        *,
        status: str | None = None,
        rounds_completed: int | None = None,
        transcript: list | None = None,
        result: dict | None = None,
        error: str | None = None,
    ) -> MeetingModel | None:
        meeting = await self.get(meeting_id)
        if meeting is None:
            return None
        if status:
            meeting.status = status
        if rounds_completed is not None:
            meeting.rounds_completed = rounds_completed
        if transcript is not None:
            meeting.transcript = transcript
        if result is not None:
            meeting.result = result
        if error is not None:
            meeting.error_message = error
        if status in ("completed", "failed"):
            meeting.completed_at = datetime.now(timezone.utc)
        await self._session.commit()
        await self._session.refresh(meeting)
        return meeting