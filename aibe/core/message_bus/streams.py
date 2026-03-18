"""NATS JetStream stream and consumer configuration."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class StreamConfig:
    """JetStream stream configuration."""

    name: str
    subjects: list[str] = field(default_factory=list)
    max_bytes: int = 1_073_741_824  # 1 GB
    max_age_hours: int = 168  # 7 days
    storage: str = "file"
    retention: str = "limits"  # limits | interest | workqueue
    num_replicas: int = 1
    duplicate_window_seconds: int = 120


# ═══════════════════════════════════════════════════════════════
# STREAM DEFINITIONS
# ═══════════════════════════════════════════════════════════════

STREAM_TASKS = StreamConfig(
    name="TASKS",
    subjects=["tasks.>"],
    max_age_hours=72,
    retention="workqueue",
)

STREAM_EVENTS = StreamConfig(
    name="EVENTS",
    subjects=["events.>"],
    max_age_hours=168,
    retention="limits",
)

STREAM_SECURITY = StreamConfig(
    name="SECURITY",
    subjects=["security.>"],
    max_age_hours=720,  # 30 days
    retention="limits",
)

STREAM_MEETINGS = StreamConfig(
    name="MEETINGS",
    subjects=["meetings.>"],
    max_age_hours=720,
    retention="limits",
)

STREAM_HEARTBEATS = StreamConfig(
    name="HEARTBEATS",
    subjects=["heartbeats.>"],
    max_age_hours=1,
    retention="limits",
    storage="memory",  # In-memory for speed, OK to lose on restart
)

ALL_STREAMS = [
    STREAM_TASKS,
    STREAM_EVENTS,
    STREAM_SECURITY,
    STREAM_MEETINGS,
    STREAM_HEARTBEATS,
]

# ═══════════════════════════════════════════════════════════════
# SUBJECT PATTERNS
# ═══════════════════════════════════════════════════════════════

# Tasks
SUBJECT_TASK_ASSIGN = "tasks.assign.{agent_id}"
SUBJECT_TASK_RESULT = "tasks.result.{agent_id}"
SUBJECT_TASK_ESCALATION = "tasks.escalation.{agent_id}"

# Events
SUBJECT_AGENT_STATUS = "events.agent.status.{agent_id}"
SUBJECT_SYSTEM_EVENT = "events.system.{event_type}"

# Security
SUBJECT_SECURITY_REPORT = "security.report"
SUBJECT_SECURITY_GATE = "security.gate.{deployment_id}"
SUBJECT_SECURITY_INCIDENT = "security.incident"

# Meetings
SUBJECT_MEETING_REQUEST = "meetings.request"
SUBJECT_MEETING_CONTRIBUTION = "meetings.contribution.{meeting_id}"

# Heartbeats
SUBJECT_HEARTBEAT = "heartbeats.{agent_id}"


__all__ = [
    "ALL_STREAMS",
    "STREAM_EVENTS",
    "STREAM_HEARTBEATS",
    "STREAM_MEETINGS",
    "STREAM_SECURITY",
    "STREAM_TASKS",
    "SUBJECT_AGENT_STATUS",
    "SUBJECT_HEARTBEAT",
    "SUBJECT_MEETING_CONTRIBUTION",
    "SUBJECT_MEETING_REQUEST",
    "SUBJECT_SECURITY_GATE",
    "SUBJECT_SECURITY_INCIDENT",
    "SUBJECT_SECURITY_REPORT",
    "SUBJECT_SYSTEM_EVENT",
    "SUBJECT_TASK_ASSIGN",
    "SUBJECT_TASK_ESCALATION",
    "SUBJECT_TASK_RESULT",
    "StreamConfig",
]
