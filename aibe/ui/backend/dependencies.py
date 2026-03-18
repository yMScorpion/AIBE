# aibe/ui/backend/dependencies.py
"""Dependency injection for FastAPI routes."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aibe.core.orchestrator.orchestrator import SystemOrchestrator
    from aibe.core.task_tracker import TaskTracker
    from aibe.core.meeting_store import MeetingStore

_orchestrator: "SystemOrchestrator | None" = None
_task_tracker: "TaskTracker | None" = None
_meeting_store: "MeetingStore | None" = None


def set_orchestrator(o: "SystemOrchestrator") -> None:
    global _orchestrator
    _orchestrator = o


def set_task_tracker(t: "TaskTracker") -> None:
    global _task_tracker
    _task_tracker = t


def set_meeting_store(m: "MeetingStore") -> None:
    global _meeting_store
    _meeting_store = m


async def get_orchestrator() -> "SystemOrchestrator":
    assert _orchestrator is not None, "Orchestrator not booted"
    return _orchestrator


async def get_task_tracker() -> "TaskTracker":
    assert _task_tracker is not None, "TaskTracker not initialised"
    return _task_tracker


async def get_meeting_store() -> "MeetingStore":
    assert _meeting_store is not None, "MeetingStore not initialised"
    return _meeting_store