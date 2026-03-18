"""Tests for task delegation — builder, router, and models."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, PropertyMock

import pytest

from aibe.agents.delegation.builder import TaskBuilder
from aibe.agents.delegation.models import DelegationRule, TaskResult, TaskSpec
from aibe.agents.delegation.router import DEFAULT_RULES, TaskRouter
from aibe.core.types import TaskPriority


class TestTaskSpec:
    def test_auto_generates_id(self) -> None:
        spec = TaskSpec(title="Test task")
        assert spec.task_id  # non-empty UUID

    def test_defaults(self) -> None:
        spec = TaskSpec(title="Test")
        assert spec.priority == 2
        assert spec.task_type == "standard_reasoning"
        assert spec.max_retries == 1


class TestTaskBuilder:
    def test_basic_build(self) -> None:
        task = (
            TaskBuilder("Research market")
            .to_agent("scout")
            .from_agent("oracle")
            .build()
        )
        assert task.title == "Research market"
        assert task.target_agent == "scout"
        assert task.source_agent == "oracle"

    def test_full_builder_chain(self) -> None:
        task = (
            TaskBuilder("Analyse competitors")
            .described_as("Deep competitive analysis")
            .from_agent("oracle")
            .to_agent("vega")
            .with_priority(TaskPriority.HIGH)
            .with_task_type("deep_research")
            .with_input({"industry": "fintech"})
            .with_success_criteria(["5+ competitors"])
            .with_deadline(30)
            .with_escalation("oracle")
            .with_retries(3)
            .build()
        )
        assert task.priority == 1
        assert task.task_type == "deep_research"
        assert task.deadline_minutes == 30
        assert task.max_retries == 3
        assert "fintech" in task.input_data["industry"]

    def test_missing_target_raises(self) -> None:
        with pytest.raises(ValueError, match="Target agent"):
            TaskBuilder("No target").build()

    def test_missing_title_raises(self) -> None:
        with pytest.raises(ValueError, match="title"):
            TaskBuilder("").to_agent("scout").build()


class TestTaskRouter:
    def test_direct_routing(self) -> None:
        router = TaskRouter()
        task = TaskSpec(title="Test", target_agent="forge")
        assert router.route(task) == "forge"

    def test_rule_based_routing(self) -> None:
        router = TaskRouter()
        task = TaskSpec(title="Research", task_type="deep_research")
        result = router.route(task)
        assert result in ["scout", "vega", "pulse", "lumen"]

    def test_unknown_type_raises(self) -> None:
        router = TaskRouter()
        task = TaskSpec(title="Test", task_type="nonexistent")
        with pytest.raises(Exception):
            router.route(task)

    def test_default_rules_cover_all_types(self) -> None:
        rule_types = {r.task_type for r in DEFAULT_RULES}
        expected = {
            "deep_research", "code_generation", "standard_generation",
            "complex_reasoning", "security_analysis", "ml_design",
            "simple_classification", "simple_extraction", "standard_reasoning",
        }
        assert rule_types == expected

    def test_custom_rule(self) -> None:
        router = TaskRouter()
        router.add_rule(DelegationRule(
            task_type="custom_task",
            preferred_agents=["forge"],
        ))
        task = TaskSpec(title="Custom", task_type="custom_task")
        assert router.route(task) == "forge"


class TestTaskResult:
    def test_task_result(self) -> None:
        result = TaskResult(
            task_id="abc",
            status="completed",
            output_data={"key": "value"},
            cost_usd=0.05,
        )
        assert result.status == "completed"
        assert result.cost_usd == 0.05
