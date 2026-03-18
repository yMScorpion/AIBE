"""SQLAlchemy ORM models for AIBE.

All persistent entities stored in PostgreSQL.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    type_annotation_map = {
        dict[str, Any]: JSONB,
    }


class TimestampMixin:
    """Adds created_at and updated_at columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ═══════════════════════════════════════════════════════════════
# AGENT & TASK MODELS
# ═══════════════════════════════════════════════════════════════


class AgentModel(TimestampMixin, Base):
    """Registered agent record."""

    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    tier: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="initializing")
    description: Mapped[str] = mapped_column(Text, default="")
    config: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    last_heartbeat: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    tasks: Mapped[list[TaskModel]] = relationship("TaskModel", back_populates="agent")


class TaskModel(TimestampMixin, Base):
    """Task assigned to an agent."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[str] = mapped_column(ForeignKey("agents.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=2)
    task_type: Mapped[str] = mapped_column(String(64), default="standard_reasoning")
    input_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    output_data: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_task_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped[AgentModel] = relationship("AgentModel", back_populates="tasks")


# ═══════════════════════════════════════════════════════════════
# MEETING MODELS
# ═══════════════════════════════════════════════════════════════


class MeetingModel(TimestampMixin, Base):
    """Multi-agent meeting record."""

    __tablename__ = "meetings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meeting_type: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="scheduled")
    participants: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    agenda: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    minutes: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    action_items: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ═══════════════════════════════════════════════════════════════
# SECURITY MODELS
# ═══════════════════════════════════════════════════════════════


class SecurityScanModel(TimestampMixin, Base):
    """Security scan execution record."""

    __tablename__ = "security_scans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_type: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="running")
    target: Mapped[str] = mapped_column(String(512), default="")
    findings_count: Mapped[int] = mapped_column(Integer, default=0)
    critical_count: Mapped[int] = mapped_column(Integer, default=0)
    high_count: Mapped[int] = mapped_column(Integer, default=0)
    results: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    findings: Mapped[list[SecurityFindingModel]] = relationship("SecurityFindingModel", back_populates="scan")


class SecurityFindingModel(TimestampMixin, Base):
    """Individual security finding from a scan."""

    __tablename__ = "security_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("security_scans.id"), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    file_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    line_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    remediation: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="open")
    is_false_positive: Mapped[bool] = mapped_column(default=False)
    cwe_id: Mapped[str | None] = mapped_column(String(32), nullable=True)

    scan: Mapped[SecurityScanModel] = relationship("SecurityScanModel", back_populates="findings")


class IncidentModel(TimestampMixin, Base):
    """Security incident record."""

    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="active")
    playbook_used: Mapped[str | None] = mapped_column(String(128), nullable=True)
    actions_taken: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ═══════════════════════════════════════════════════════════════
# ML MODELS
# ═══════════════════════════════════════════════════════════════


class MLExperimentModel(TimestampMixin, Base):
    """ML experiment tracking record."""

    __tablename__ = "ml_experiments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="running")
    model_type: Mapped[str] = mapped_column(String(128), default="")
    hyperparameters: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    wandb_run_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MLModelModel(TimestampMixin, Base):
    """Trained ML model registry entry."""

    __tablename__ = "ml_models"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    model_type: Mapped[str] = mapped_column(String(128), nullable=False)
    experiment_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="staged")
    artifact_path: Mapped[str] = mapped_column(String(1024), default="")
    metrics: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    deployed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


# ═══════════════════════════════════════════════════════════════
# EVOLUTION MODELS
# ═══════════════════════════════════════════════════════════════


class EvolutionProposalModel(TimestampMixin, Base):
    """Darwin's evolution proposal record."""

    __tablename__ = "evolution_proposals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    proposal_type: Mapped[str] = mapped_column(String(64), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(32), default="proposed")
    evidence: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    implementation_plan: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    shadow_validation_results: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ToolModel(TimestampMixin, Base):
    """Registered tool in the tool registry."""

    __tablename__ = "tools"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    source: Mapped[str] = mapped_column(String(32), default="builtin")
    parameters_schema: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_by: Mapped[str] = mapped_column(String(64), default="system")


# ═══════════════════════════════════════════════════════════════
# FINANCE & CONTRACTOR MODELS
# ═══════════════════════════════════════════════════════════════


class ContractorModel(TimestampMixin, Base):
    """Contractor engagement record."""

    __tablename__ = "contractors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    platform: Mapped[str] = mapped_column(String(64), default="")
    status: Mapped[str] = mapped_column(String(32), default="requested")
    justification: Mapped[str] = mapped_column(Text, default="")
    budget_usd: Mapped[float] = mapped_column(Float, default=0.0)
    actual_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    requesting_agent: Mapped[str] = mapped_column(String(64), default="")
    deliverables: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    performance_rating: Mapped[float | None] = mapped_column(Float, nullable=True)


class FinancialTransactionModel(TimestampMixin, Base):
    """Financial transaction for P&L tracking."""

    __tablename__ = "financial_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_type: Mapped[str] = mapped_column(String(32), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    amount_usd: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(512), default="")
    source: Mapped[str] = mapped_column(String(128), default="")
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)


# ═══════════════════════════════════════════════════════════════
# AUDIT LOG
# ═══════════════════════════════════════════════════════════════


class AuditLogModel(TimestampMixin, Base):
    """System-wide audit log entry."""

    __tablename__ = "audit_log"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(64), default="")
    resource_id: Mapped[str] = mapped_column(String(256), default="")
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)


__all__ = [
    "AgentModel",
    "AuditLogModel",
    "Base",
    "ContractorModel",
    "EvolutionProposalModel",
    "FinancialTransactionModel",
    "IncidentModel",
    "MLExperimentModel",
    "MLModelModel",
    "MeetingModel",
    "SecurityFindingModel",
    "SecurityScanModel",
    "TaskModel",
    "TimestampMixin",
    "ToolModel",
]
