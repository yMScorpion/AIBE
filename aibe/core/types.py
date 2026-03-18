"""AIBE core type definitions — enums, type aliases, and constants.

All shared types used across the system are defined here to avoid
circular imports and ensure a single source of truth.
"""

from __future__ import annotations

import enum
from typing import NewType
from uuid import UUID

# ═══════════════════════════════════════════════════════════════
# TYPE ALIASES
# ═══════════════════════════════════════════════════════════════

AgentId = NewType("AgentId", str)
TaskId = NewType("TaskId", UUID)
TraceId = NewType("TraceId", UUID)
MeetingId = NewType("MeetingId", UUID)
Namespace = NewType("Namespace", str)


# ═══════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════


class AgentTier(int, enum.Enum):
    """Agent tier hierarchy (0 = highest authority)."""

    EXECUTIVE = 0
    RESEARCH = 1
    PRODUCT = 2
    MARKETING = 3
    SOCIAL = 4
    FINANCE = 5
    EVOLUTION = 6
    AI_ML = 7
    SECURITY = 8
    SALES = 9


class AgentStatus(str, enum.Enum):
    """Runtime status of an agent."""

    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    DEGRADED = "degraded"


class TaskPriority(int, enum.Enum):
    """Task priority levels."""

    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class TaskStatus(str, enum.Enum):
    """Lifecycle status of a task."""

    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ESCALATED = "escalated"


class MeetingType(str, enum.Enum):
    """Types of multi-agent meetings."""

    STRATEGY_SUMMIT = "strategy_summit"
    SPRINT_PLANNING = "sprint_planning"
    SECURITY_REVIEW = "security_review"
    ML_ROADMAP = "ml_roadmap"
    SALES_PIPELINE_REVIEW = "sales_pipeline_review"
    INCIDENT_POSTMORTEM = "incident_postmortem"
    EVOLUTION_REVIEW = "evolution_review"
    STRATEGY_SUMMIT_EMERGENCY = "strategy_summit_emergency"


class ModelTaskType(str, enum.Enum):
    """LLM task type for model routing."""

    SIMPLE_CLASSIFICATION = "simple_classification"
    SIMPLE_EXTRACTION = "simple_extraction"
    STANDARD_GENERATION = "standard_generation"
    STANDARD_REASONING = "standard_reasoning"
    CODE_GENERATION = "code_generation"
    COMPLEX_REASONING = "complex_reasoning"
    DEEP_RESEARCH = "deep_research"
    SECURITY_ANALYSIS = "security_analysis"
    ML_DESIGN = "ml_design"


class SecuritySeverity(str, enum.Enum):
    """Security finding severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IncidentType(str, enum.Enum):
    """Security incident types triggering playbooks."""

    API_KEY_LEAKED = "api_key_leaked"
    CRITICAL_VULNERABILITY = "critical_vulnerability_found"
    SITE_UNDER_ATTACK = "site_under_attack"
    DATA_BREACH_SUSPECTED = "data_breach_suspected"


class SocialInteractionType(str, enum.Enum):
    """Classification of inbound social media interactions."""

    QUESTION = "question"
    COMPLIMENT = "compliment"
    COMPLAINT = "complaint"
    SPAM = "spam"
    PARTNERSHIP = "partnership"
    SALES_INQUIRY = "sales_inquiry"


class ContractorStatus(str, enum.Enum):
    """Status of a contractor engagement."""

    REQUESTED = "requested"
    VALIDATED = "validated"
    BUDGET_APPROVED = "budget_approved"
    HUMAN_APPROVED = "human_approved"
    SOURCING = "sourcing"
    ENGAGED = "engaged"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class EvolutionProposalRisk(int, enum.Enum):
    """Risk score for evolution proposals (1-10)."""

    TRIVIAL = 1
    LOW = 3
    MODERATE = 5
    HIGH = 7
    CRITICAL = 10


# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

HEARTBEAT_INTERVAL_SECONDS = 30
MAX_AGENT_RESTARTS = 5
RESTART_WINDOW_SECONDS = 60
DEGRADED_AGENT_THRESHOLD_PCT = 30
BUDGET_WARNING_PCT = 80
BUDGET_SUSPEND_PCT = 100

# Auto-approve evolution proposals with risk <= this value
EVOLUTION_AUTO_APPROVE_MAX_RISK = 5
EVOLUTION_SHADOW_VALIDATION_HOURS = 48


__all__ = [
    "AgentId",
    "AgentStatus",
    "AgentTier",
    "BUDGET_SUSPEND_PCT",
    "BUDGET_WARNING_PCT",
    "ContractorStatus",
    "DEGRADED_AGENT_THRESHOLD_PCT",
    "EVOLUTION_AUTO_APPROVE_MAX_RISK",
    "EVOLUTION_SHADOW_VALIDATION_HOURS",
    "EvolutionProposalRisk",
    "HEARTBEAT_INTERVAL_SECONDS",
    "IncidentType",
    "MAX_AGENT_RESTARTS",
    "MeetingId",
    "MeetingType",
    "ModelTaskType",
    "Namespace",
    "RESTART_WINDOW_SECONDS",
    "SecuritySeverity",
    "SocialInteractionType",
    "TaskId",
    "TaskPriority",
    "TaskStatus",
    "TraceId",
]
