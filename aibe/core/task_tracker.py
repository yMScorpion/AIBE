# aibe/core/task_tracker.py
"""In-memory task lifecycle tracker with bus integration."""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from aibe.core.orchestrator.orchestrator import SystemOrchestrator


class TaskStatus(str, Enum):
    SUBMITTED = "submitted"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskRecord:
    task_id: str
    source: str
    target: str
    title: str
    description: str
    priority: int
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    output_data: Optional[dict] = None
    error_message: Optional[str] = None


class TaskTracker:
    """Track tasks from submission through completion."""

    def __init__(self, orchestrator: "SystemOrchestrator") -> None:
        self._orchestrator = orchestrator
        self._tasks: dict[str, TaskRecord] = {}
        self._running = False
        self._listener_task: asyncio.Task | None = None

    async def start(self) -> None:
        self._running = True

    async def stop(self) -> None:
        self._running = False
        if self._listener_task and not self._listener_task.done():
            self._listener_task.cancel()

    async def submit(
        self,
        target: str,
        title: str,
        description: str = "",
        priority: int = 5,
        source: str = "api",
    ) -> str:
        task_id = uuid.uuid4().hex[:12]
        record = TaskRecord(
            task_id=task_id,
            source=source,
            target=target,
            title=title,
            description=description,
            priority=priority,
            status=TaskStatus.SUBMITTED,
            created_at=datetime.now(timezone.utc),
        )
        self._tasks[task_id] = record

        # Dispatch to agent via orchestrator bus if available
        bus = getattr(self._orchestrator, "bus", None)
        if bus is not None:
            try:
                await bus.publish(
                    f"tasks.assign.{target}",
                    {
                        "task_id": task_id,
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "source": source,
                    },
                )
                record.status = TaskStatus.ASSIGNED
            except Exception:
                pass

        return task_id

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        agent_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[TaskRecord]:
        results = list(self._tasks.values())
        if agent_id:
            results = [t for t in results if t.target == agent_id]
        if status:
            results = [t for t in results if t.status.value == status]
        results.sort(key=lambda t: t.created_at, reverse=True)
        return results[:limit]

    def on_result(self, task_id: str, output: dict | None = None, error: str | None = None) -> None:
        record = self._tasks.get(task_id)
        if record is None:
            return
        if error:
            record.status = TaskStatus.FAILED
            record.error_message = error
        else:
            record.status = TaskStatus.COMPLETED
            record.output_data = output
        record.completed_at = datetime.now(timezone.utc)