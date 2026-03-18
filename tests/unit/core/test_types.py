"""Tests for aibe.core.types — enums and type definitions."""

from __future__ import annotations

from aibe.core.types import (
    AgentStatus,
    AgentTier,
    MeetingType,
    ModelTaskType,
    SecuritySeverity,
    TaskPriority,
    TaskStatus,
)


class TestAgentTier:
    def test_tier_values(self) -> None:
        assert AgentTier.EXECUTIVE == 0
        assert AgentTier.SALES == 9
        assert len(AgentTier) == 10

    def test_tier_ordering(self) -> None:
        assert AgentTier.EXECUTIVE < AgentTier.RESEARCH
        assert AgentTier.SECURITY < AgentTier.SALES


class TestAgentStatus:
    def test_all_statuses_exist(self) -> None:
        expected = {"initializing", "ready", "running", "paused", "stopped", "error", "degraded"}
        actual = {s.value for s in AgentStatus}
        assert actual == expected


class TestModelTaskType:
    def test_nine_task_types(self) -> None:
        assert len(ModelTaskType) == 9

    def test_values(self) -> None:
        assert ModelTaskType.SIMPLE_CLASSIFICATION.value == "simple_classification"
        assert ModelTaskType.ML_DESIGN.value == "ml_design"


class TestMeetingType:
    def test_eight_meeting_types(self) -> None:
        assert len(MeetingType) == 8

    def test_emergency_type(self) -> None:
        assert MeetingType.STRATEGY_SUMMIT_EMERGENCY.value == "strategy_summit_emergency"


class TestTaskStatus:
    def test_lifecycle_statuses(self) -> None:
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.ESCALATED.value == "escalated"


class TestSecuritySeverity:
    def test_severity_levels(self) -> None:
        assert len(SecuritySeverity) == 5
        assert SecuritySeverity.CRITICAL.value == "critical"
        assert SecuritySeverity.INFO.value == "info"


class TestTaskPriority:
    def test_priority_ordering(self) -> None:
        assert TaskPriority.CRITICAL < TaskPriority.LOW
