"""Pydantic v2 message types for inter-agent communication via NATS."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


class MessageBase(BaseModel):
    """Base for all bus messages."""

    message_id: str = Field(default_factory=_new_id)
    timestamp: datetime = Field(default_factory=_utc_now)
    source_agent: str = ""
    target_agent: str = ""
    trace_id: str = Field(default_factory=_new_id)
    signature: str = ""  # HMAC-SHA256, filled by signing middleware


# ── Task messages ─────────────────────────────────────────────


class TaskAssignMessage(MessageBase):
    """Assign a task to an agent."""

    task_id: str = Field(default_factory=_new_id)
    title: str
    description: str = ""
    priority: int = 2
    task_type: str = "standard_reasoning"
    input_data: dict[str, Any] = Field(default_factory=dict)
    success_criteria: list[str] = Field(default_factory=list)
    model_routing_hint: str = ""
    escalation_path: str = ""
    deadline_minutes: Optional[int] = None


class TaskResultMessage(MessageBase):
    """Report task completion or failure."""

    task_id: str
    status: str = "completed"  # completed | failed
    output_data: dict[str, Any] = Field(default_factory=dict)
    error_message: str = ""
    tokens_used: int = 0
    cost_usd: float = 0.0
    duration_seconds: float = 0.0


# ── Security messages ─────────────────────────────────────────


class SecurityReportMessage(MessageBase):
    """Security scan results report."""

    scan_id: str = Field(default_factory=_new_id)
    scan_type: str = ""
    findings_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    blocks_deployment: bool = False
    findings_summary: list[dict[str, Any]] = Field(default_factory=list)


class DeploymentGateMessage(MessageBase):
    """Deployment gate decision."""

    class Decision(str, Enum):
        APPROVED = "approved"
        BLOCKED = "blocked"

    deployment_id: str = Field(default_factory=_new_id)
    decision: Decision = Decision.BLOCKED
    reason: str = ""
    blocking_findings: list[str] = Field(default_factory=list)


# ── Contractor messages ───────────────────────────────────────


class ContractorRequestMessage(MessageBase):
    """Request a contractor engagement."""

    request_id: str = Field(default_factory=_new_id)
    justification: str = ""
    required_skills: list[str] = Field(default_factory=list)
    estimated_budget_usd: float = 0.0
    estimated_duration_days: int = 0
    deliverables: list[str] = Field(default_factory=list)
    ai_capability_check: str = ""


# ── ML messages ───────────────────────────────────────────────


class MLProposalMessage(MessageBase):
    """ML opportunity proposal from Cipher."""

    proposal_id: str = Field(default_factory=_new_id)
    opportunity_type: str = ""
    description: str = ""
    estimated_impact: dict[str, Any] = Field(default_factory=dict)
    required_data_sources: list[str] = Field(default_factory=list)
    estimated_training_hours: float = 0.0
    risk_level: int = 5


# ── Sales messages ────────────────────────────────────────────


class SalesHandoffMessage(MessageBase):
    """Handoff between sales agents or to human."""

    handoff_id: str = Field(default_factory=_new_id)
    handoff_type: str = ""  # qualification | escalation | human_handoff
    customer_context: dict[str, Any] = Field(default_factory=dict)
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)
    sentiment_score: float = 0.0
    recommended_actions: list[str] = Field(default_factory=list)


# ── Escalation messages ──────────────────────────────────────


class EscalationMessage(MessageBase):
    """Escalate an issue to a higher-tier agent."""

    escalation_id: str = Field(default_factory=_new_id)
    severity: str = "medium"
    reason: str = ""
    context: dict[str, Any] = Field(default_factory=dict)
    attempts_made: int = 0


# ── Meeting messages ──────────────────────────────────────────


class MeetingRequestMessage(MessageBase):
    """Request to convene a multi-agent meeting."""

    meeting_id: str = Field(default_factory=_new_id)
    meeting_type: str = ""
    title: str = ""
    agenda_items: list[str] = Field(default_factory=list)
    required_participants: list[str] = Field(default_factory=list)
    optional_participants: list[str] = Field(default_factory=list)
    urgency: str = "normal"


class MeetingContributionMessage(MessageBase):
    """Agent contribution during a meeting."""

    meeting_id: str
    contribution_type: str = "position"  # position | rebuttal | consensus
    content: str = ""
    data_references: list[str] = Field(default_factory=list)
    confidence: float = 0.8


# ── Agent lifecycle messages ──────────────────────────────────


class HeartbeatMessage(MessageBase):
    """Agent heartbeat for liveness tracking."""

    agent_status: str = "running"
    current_task_id: Optional[str] = None
    uptime_seconds: float = 0.0
    tasks_completed: int = 0
    error_count: int = 0


class AgentStatusChangedMessage(MessageBase):
    """Agent status transition event."""

    old_status: str = ""
    new_status: str = ""
    reason: str = ""


__all__ = [
    "AgentStatusChangedMessage",
    "ContractorRequestMessage",
    "DeploymentGateMessage",
    "EscalationMessage",
    "HeartbeatMessage",
    "MLProposalMessage",
    "MeetingContributionMessage",
    "MeetingRequestMessage",
    "MessageBase",
    "SecurityReportMessage",
    "SalesHandoffMessage",
    "TaskAssignMessage",
    "TaskResultMessage",
]
