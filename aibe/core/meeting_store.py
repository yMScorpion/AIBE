# aibe/core/meeting_store.py
"""In-memory meeting lifecycle store."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class MeetingStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MeetingRecord:
    meeting_id: str
    topic: str
    participants: list[str]
    meeting_type: str
    max_rounds: int
    status: MeetingStatus
    created_at: datetime
    rounds_completed: int = 0
    transcript: list[dict] = field(default_factory=list)
    result: Optional[dict] = None
    error_message: Optional[str] = None
    completed_at: Optional[datetime] = None


class MeetingStore:
    """Track meetings from creation through completion."""

    def __init__(self) -> None:
        self._meetings: dict[str, MeetingRecord] = {}

    def create(
        self,
        topic: str,
        participants: list[str],
        meeting_type: str = "general",
        max_rounds: int = 3,
    ) -> str:
        meeting_id = uuid.uuid4().hex[:12]
        record = MeetingRecord(
            meeting_id=meeting_id,
            topic=topic,
            participants=participants,
            meeting_type=meeting_type,
            max_rounds=max_rounds,
            status=MeetingStatus.PENDING,
            created_at=datetime.now(timezone.utc),
        )
        self._meetings[meeting_id] = record
        return meeting_id

    def get(self, meeting_id: str) -> MeetingRecord | None:
        return self._meetings.get(meeting_id)

    def update_status(
        self,
        meeting_id: str,
        status: MeetingStatus,
        rounds_completed: int | None = None,
        result: dict | None = None,
        error: str | None = None,
    ) -> None:
        record = self._meetings.get(meeting_id)
        if record is None:
            return
        record.status = status
        if rounds_completed is not None:
            record.rounds_completed = rounds_completed
        if result is not None:
            record.result = result
        if error is not None:
            record.error_message = error
        if status in (MeetingStatus.COMPLETED, MeetingStatus.FAILED):
            record.completed_at = datetime.now(timezone.utc)

    def add_transcript_entry(self, meeting_id: str, entry: dict) -> None:
        record = self._meetings.get(meeting_id)
        if record:
            record.transcript.append(entry)

    def list_meetings(
        self,
        status: str | None = None,
        limit: int = 50,
    ) -> list[MeetingRecord]:
        results = list(self._meetings.values())
        if status:
            results = [m for m in results if m.status.value == status]
        results.sort(key=lambda m: m.created_at, reverse=True)
        return results[:limit]