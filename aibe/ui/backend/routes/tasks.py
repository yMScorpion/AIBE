"""Task management routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class TaskCreateRequest(BaseModel):
    """Request body for creating a new task."""

    title: str
    description: str = ""
    target_agent: str = ""
    priority: int = 2
    task_type: str = "standard_reasoning"
    input_data: dict[str, Any] = Field(default_factory=dict)


@router.post("/")
async def create_task(request: TaskCreateRequest) -> dict[str, Any]:
    """Create and dispatch a new task to an agent."""
    # TODO: Wire to TaskRouter and message bus
    return {
        "task_id": "pending",
        "status": "queued",
        "target_agent": request.target_agent or "auto-routed",
        "title": request.title,
    }


@router.get("/")
async def list_tasks() -> dict[str, Any]:
    """List recent tasks with their status."""
    return {"tasks": [], "total": 0}


@router.get("/{task_id}")
async def get_task(task_id: str) -> dict[str, Any]:
    """Get details of a specific task."""
    return {"task_id": task_id, "status": "unknown"}
