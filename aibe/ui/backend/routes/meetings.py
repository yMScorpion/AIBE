"""Meeting management routes."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class MeetingConveneRequest(BaseModel):
    """Request to convene a meeting."""

    meeting_type: str
    title_vars: dict[str, str] = Field(default_factory=dict)
    extra_agenda: list[str] = Field(default_factory=list)
    extra_participants: list[str] = Field(default_factory=list)


@router.post("/convene")
async def convene_meeting(request: MeetingConveneRequest) -> dict[str, Any]:
    """Convene a new meeting of the specified type."""
    # TODO: Wire to MeetingEngine
    return {
        "meeting_id": "pending",
        "meeting_type": request.meeting_type,
        "status": "scheduled",
    }


@router.get("/")
async def list_meetings() -> dict[str, Any]:
    """List recent and active meetings."""
    return {"meetings": [], "total": 0}


@router.get("/types")
async def list_meeting_types() -> dict[str, Any]:
    """List all available meeting types."""
    from aibe.agents.meetings.types import ALL_MEETING_TEMPLATES

    return {
        "types": [
            {
                "meeting_type": t.meeting_type,
                "description": t.description,
                "required_participants": t.required_participants,
                "max_rounds": t.max_rounds,
                "min_quorum": t.min_quorum,
            }
            for t in ALL_MEETING_TEMPLATES.values()
        ]
    }


@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str) -> dict[str, Any]:
    """Get details and transcript of a meeting."""
    return {"meeting_id": meeting_id, "status": "unknown"}
