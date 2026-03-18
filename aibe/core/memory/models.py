"""Memory record Pydantic models for OpenViking storage."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class MemoryRecord(BaseModel):
    """Base memory record stored in OpenViking."""

    namespace: str
    key: str
    value: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=_utc_now)
    version: int = 1
    agent_id: str = ""


class BusinessStateMemory(MemoryRecord):
    """Business state snapshot."""

    namespace: str = "/business/strategy"
    business_model: str = ""
    target_market: str = ""
    value_proposition: str = ""
    revenue_model: str = ""
    current_stage: str = "discovery"


class AgentEpisodicMemory(MemoryRecord):
    """Agent episodic memory — records of past actions and outcomes."""

    namespace: str = "/agents/{agent_id}/episodic"
    action: str = ""
    outcome: str = ""
    lessons_learned: list[str] = Field(default_factory=list)
    confidence: float = 0.8


class MeetingTranscript(MemoryRecord):
    """Meeting transcript and decisions."""

    namespace: str = "/meetings/transcripts"
    meeting_type: str = ""
    participants: list[str] = Field(default_factory=list)
    contributions: list[dict[str, Any]] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    action_items: list[dict[str, Any]] = Field(default_factory=list)
    consensus_score: float = 0.0


class SecurityVulnerabilityRecord(MemoryRecord):
    """Security vulnerability finding."""

    namespace: str = "/security/findings"
    severity: str = "medium"
    title: str = ""
    description: str = ""
    file_path: str = ""
    remediation: str = ""
    status: str = "open"
    cwe_id: str = ""


class MLModelRecord(MemoryRecord):
    """ML model registry entry in memory."""

    namespace: str = "/ml/models"
    model_name: str = ""
    model_type: str = ""
    model_version: str = ""
    metrics: dict[str, float] = Field(default_factory=dict)
    status: str = "staged"
    artifact_path: str = ""


class SalesLeadRecord(MemoryRecord):
    """Sales lead tracking record."""

    namespace: str = "/sales/leads"
    company_name: str = ""
    contact_name: str = ""
    contact_email: str = ""
    lead_score: float = 0.0
    stage: str = "prospecting"
    last_touchpoint: str = ""
    notes: list[str] = Field(default_factory=list)


class ContractorEngagementRecord(MemoryRecord):
    """Contractor engagement record."""

    namespace: str = "/contractor/engagements"
    contractor_name: str = ""
    platform: str = ""
    status: str = "requested"
    budget_usd: float = 0.0
    deliverables: list[str] = Field(default_factory=list)
    performance_rating: Optional[float] = None


__all__ = [
    "AgentEpisodicMemory",
    "BusinessStateMemory",
    "ContractorEngagementRecord",
    "MLModelRecord",
    "MeetingTranscript",
    "MemoryRecord",
    "SalesLeadRecord",
    "SecurityVulnerabilityRecord",
]
