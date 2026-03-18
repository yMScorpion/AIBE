# aibe/ui/backend/schemas/task_schemas.py
"""Pydantic schemas for task endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskSubmit(BaseModel):
    target_agent: str
    title: str
    description: str = ""
    priority: int = Field(default=5, ge=1, le=10)


class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str


class TaskResponse(BaseModel):
    task_id: str
    source: str
    target: str
    title: str
    description: str
    priority: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    output_data: Optional[dict] = None
    error_message: Optional[str] = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int