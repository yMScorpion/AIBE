"""Tests for aibe.core.message_bus — message models and signing."""

from __future__ import annotations

from aibe.core.message_bus.models import (
    HeartbeatMessage,
    MeetingRequestMessage,
    TaskAssignMessage,
    TaskResultMessage,
    SecurityReportMessage,
)
from aibe.core.message_bus.signing import sign_message, verify_message
from aibe.core.message_bus.streams import ALL_STREAMS, STREAM_TASKS


class TestMessageModels:
    def test_task_assign_defaults(self) -> None:
        msg = TaskAssignMessage(title="Test task")
        assert msg.title == "Test task"
        assert msg.priority == 2
        assert msg.task_type == "standard_reasoning"
        assert msg.message_id  # auto-generated
        assert msg.timestamp  # auto-generated

    def test_task_result_serialization(self) -> None:
        msg = TaskResultMessage(
            task_id="abc-123",
            status="completed",
            output_data={"result": "success"},
            tokens_used=500,
            cost_usd=0.05,
        )
        data = msg.model_dump()
        assert data["task_id"] == "abc-123"
        assert data["cost_usd"] == 0.05

    def test_security_report(self) -> None:
        msg = SecurityReportMessage(
            scan_type="commit_scan",
            findings_count=3,
            critical_count=1,
            blocks_deployment=True,
        )
        assert msg.blocks_deployment
        assert msg.critical_count == 1

    def test_heartbeat_message(self) -> None:
        msg = HeartbeatMessage(
            source_agent="oracle",
            agent_status="running",
            uptime_seconds=3600.0,
        )
        assert msg.source_agent == "oracle"
        assert msg.agent_status == "running"

    def test_meeting_request(self) -> None:
        msg = MeetingRequestMessage(
            meeting_type="strategy_summit",
            title="Q1 strategy review",
            required_participants=["oracle", "minerva", "forge"],
        )
        assert len(msg.required_participants) == 3

    def test_json_roundtrip(self) -> None:
        msg = TaskAssignMessage(title="Roundtrip test", description="Testing JSON")
        json_str = msg.model_dump_json()
        reconstructed = TaskAssignMessage.model_validate_json(json_str)
        assert reconstructed.title == msg.title
        assert reconstructed.message_id == msg.message_id


class TestMessageSigning:
    def test_sign_and_verify(self) -> None:
        msg = TaskAssignMessage(title="Signed task", source_agent="oracle")
        msg.signature = sign_message(msg)
        assert msg.signature  # non-empty
        assert verify_message(msg)

    def test_verify_fails_on_tampered_message(self) -> None:
        msg = TaskAssignMessage(title="Original", source_agent="oracle")
        msg.signature = sign_message(msg)
        # Tamper with the message
        msg.source_agent = "attacker"
        assert not verify_message(msg)

    def test_verify_fails_without_signature(self) -> None:
        msg = TaskAssignMessage(title="No sig")
        assert not verify_message(msg)


class TestStreamConfig:
    def test_all_streams_defined(self) -> None:
        assert len(ALL_STREAMS) == 5
        stream_names = {s.name for s in ALL_STREAMS}
        assert "TASKS" in stream_names
        assert "EVENTS" in stream_names
        assert "SECURITY" in stream_names
        assert "HEARTBEATS" in stream_names

    def test_tasks_stream_config(self) -> None:
        assert STREAM_TASKS.retention == "workqueue"
        assert STREAM_TASKS.subjects == ["tasks.>"]
