# aibe/ui/backend/routes/meeting_routes.py
"""Meeting management endpoints."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from aibe.core.meeting_store import MeetingStatus
from aibe.ui.backend.dependencies import get_meeting_store, get_orchestrator
from aibe.ui.backend.schemas.meeting_schemas import (
    MeetingCreate,
    MeetingCreateResponse,
    MeetingListResponse,
    MeetingResponse,
)

logger = logging.getLogger("aibe.routes.meetings")
router = APIRouter(prefix="/api/meetings", tags=["meetings"])


def _record_to_response(r) -> MeetingResponse:
    return MeetingResponse(
        meeting_id=r.meeting_id,
        topic=r.topic,
        participants=r.participants,
        meeting_type=r.meeting_type,
        max_rounds=r.max_rounds,
        status=r.status.value,
        rounds_completed=r.rounds_completed,
        transcript=r.transcript,
        result=r.result,
        error_message=r.error_message,
        created_at=r.created_at,
        completed_at=r.completed_at,
    )


async def _run_meeting_background(
    meeting_id: str,
    orchestrator,
    meeting_store,
    topic: str,
    participants: list[str],
    max_rounds: int,
) -> None:
    """Execute meeting in background via MeetingEngine."""
    meeting_store.update_status(meeting_id, MeetingStatus.IN_PROGRESS)
    try:
        engine = getattr(orchestrator, "meeting_engine", None)
        if engine is None:
            # Fallback: simulate a basic round-robin meeting
            for round_num in range(1, max_rounds + 1):
                for pid in participants:
                    meeting_store.add_transcript_entry(
                        meeting_id,
                        {
                            "round": round_num,
                            "agent_id": pid,
                            "message": f"[{pid}] Contributing to '{topic}' (round {round_num})",
                        },
                    )
                    await asyncio.sleep(0.1)
                meeting_store.update_status(meeting_id, MeetingStatus.IN_PROGRESS, rounds_completed=round_num)
            meeting_store.update_status(
                meeting_id,
                MeetingStatus.COMPLETED,
                rounds_completed=max_rounds,
                result={"summary": f"Meeting on '{topic}' completed with {max_rounds} rounds."},
            )
        else:
            result = await engine.run_meeting(
                topic=topic,
                participants=participants,
                max_rounds=max_rounds,
            )
            meeting_store.update_status(
                meeting_id,
                MeetingStatus.COMPLETED,
                rounds_completed=max_rounds,
                result=result if isinstance(result, dict) else {"summary": str(result)},
            )
    except Exception as exc:
        logger.exception("Meeting %s failed", meeting_id)
        meeting_store.update_status(meeting_id, MeetingStatus.FAILED, error=str(exc))


@router.post("", response_model=MeetingCreateResponse)
async def create_meeting(
    body: MeetingCreate,
    orchestrator=Depends(get_orchestrator),
    meeting_store=Depends(get_meeting_store),
):
    # Validate participants exist
    registry = orchestrator.registry
    for pid in body.participants:
        agent = registry.get(pid) if hasattr(registry, "get") else registry._agents.get(pid)
        if agent is None:
            raise HTTPException(status_code=422, detail=f"Unknown participant: {pid}")

    meeting_id = meeting_store.create(
        topic=body.topic,
        participants=body.participants,
        meeting_type=body.meeting_type,
        max_rounds=body.max_rounds,
    )

    asyncio.create_task(
        _run_meeting_background(
            meeting_id=meeting_id,
            orchestrator=orchestrator,
            meeting_store=meeting_store,
            topic=body.topic,
            participants=body.participants,
            max_rounds=body.max_rounds,
        )
    )

    return MeetingCreateResponse(meeting_id=meeting_id, status="in_progress")


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(meeting_id: str, meeting_store=Depends(get_meeting_store)):
    record = meeting_store.get(meeting_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Meeting not found: {meeting_id}")
    return _record_to_response(record)


@router.get("", response_model=MeetingListResponse)
async def list_meetings(
    status: Optional[str] = None,
    limit: int = 50,
    meeting_store=Depends(get_meeting_store),
):
    records = meeting_store.list_meetings(status=status, limit=limit)
    items = [_record_to_response(r) for r in records]
    return MeetingListResponse(meetings=items, total=len(items))