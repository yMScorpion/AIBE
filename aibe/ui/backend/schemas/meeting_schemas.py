# aibe/ui/backend/schemas/meeting_schemas.py
"""Pydantic schemas for meeting endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MeetingCreate(BaseModel):
    topic: str
    participants: list[str] = Field(min_length=2)
    max_rounds: int = Field(default=3, ge=1, le=10)
    meeting_type: str = "general"


class MeetingCreateResponse(BaseModel):
    meeting_id: str
    status: str


class MeetingResponse(BaseModel):
    meeting_id: str
    topic: str
    participants: list[str]
    meeting_type: str
    max_rounds: int
    status: str
    rounds_completed: int
    transcript: list[dict]
    result: Optional[dict] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None


class MeetingListResponse(BaseModel):
    meetings: list[MeetingResponse]
    total: int