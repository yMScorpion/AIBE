"""Task delegation models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _new_id() -> str:
    return str(uuid4())


class TaskSpec(BaseModel):
    """Full specification for a delegated task."""

    task_id: str = Field(default_factory=_new_id)
    title: str
    description: str = ""
    source_agent: str = ""
    target_agent: str = ""
    priority: int = 2
    task_type: str = "standard_reasoning"
    input_data: dict[str, Any] = Field(default_factory=dict)
    success_criteria: list[str] = Field(default_factory=list)
    deadline_minutes: Optional[int] = None
    escalation_path: str = ""
    max_retries: int = 1
    created_at: datetime = Field(default_factory=_utc_now)


class TaskResult(BaseModel):
    """Result of a completed task."""

    task_id: str
    status: str = "completed"  # completed | failed
    output_data: dict[str, Any] = Field(default_factory=dict)
    error_message: str = ""
    tokens_used: int = 0
    cost_usd: float = 0.0
    duration_seconds: float = 0.0
    completed_at: datetime = Field(default_factory=_utc_now)


class DelegationRule(BaseModel):
    """Rule for automatic task routing."""

    task_type: str
    preferred_agents: list[str] = Field(default_factory=list)
    fallback_agents: list[str] = Field(default_factory=list)
    min_tier: int = 0
    max_tier: int = 9
    requires_budget_check: bool = True


__all__ = [
    "DelegationRule",
    "TaskResult",
    "TaskSpec",
]
