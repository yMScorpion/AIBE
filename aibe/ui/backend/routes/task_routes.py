# aibe/ui/backend/routes/task_routes.py
"""Task management endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from aibe.ui.backend.dependencies import get_task_tracker
from aibe.ui.backend.schemas.task_schemas import (
    TaskListResponse,
    TaskResponse,
    TaskSubmit,
    TaskSubmitResponse,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


def _record_to_response(r) -> TaskResponse:
    return TaskResponse(
        task_id=r.task_id,
        source=r.source,
        target=r.target,
        title=r.title,
        description=r.description,
        priority=r.priority,
        status=r.status.value if hasattr(r.status, "value") else str(r.status),
        created_at=r.created_at,
        completed_at=r.completed_at,
        output_data=r.output_data,
        error_message=r.error_message,
    )


@router.post("", response_model=TaskSubmitResponse)
async def submit_task(body: TaskSubmit, tracker=Depends(get_task_tracker)):
    task_id = await tracker.submit(
        target=body.target_agent,
        title=body.title,
        description=body.description,
        priority=body.priority,
    )
    record = tracker.get(task_id)
    status = record.status.value if record else "submitted"
    return TaskSubmitResponse(task_id=task_id, status=status)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, tracker=Depends(get_task_tracker)):
    record = tracker.get(task_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return _record_to_response(record)


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    tracker=Depends(get_task_tracker),
):
    records = tracker.list_tasks(agent_id=agent_id, status=status, limit=limit)
    items = [_record_to_response(r) for r in records]
    return TaskListResponse(tasks=items, total=len(items))