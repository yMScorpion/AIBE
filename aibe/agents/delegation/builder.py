"""Task builder — fluent API for constructing validated task specs."""

from __future__ import annotations

from typing import Any, Optional

from aibe.agents.delegation.models import TaskSpec
from aibe.core.types import TaskPriority


class TaskBuilder:
    """Fluent builder for creating TaskSpec instances.

    Usage:
        task = (
            TaskBuilder("Research competitors")
            .from_agent("oracle")
            .to_agent("scout")
            .with_priority(TaskPriority.HIGH)
            .with_task_type("deep_research")
            .with_input({"industry": "fintech"})
            .with_success_criteria(["At least 5 competitors identified"])
            .with_deadline(30)
            .build()
        )
    """

    def __init__(self, title: str) -> None:
        self._title = title
        self._description = ""
        self._source_agent = ""
        self._target_agent = ""
        self._priority = 2
        self._task_type = "standard_reasoning"
        self._input_data: dict[str, Any] = {}
        self._success_criteria: list[str] = []
        self._deadline_minutes: Optional[int] = None
        self._escalation_path = ""
        self._max_retries = 1

    def described_as(self, description: str) -> TaskBuilder:
        """Add a description."""
        self._description = description
        return self

    def from_agent(self, agent_id: str) -> TaskBuilder:
        """Set the source (requesting) agent."""
        self._source_agent = agent_id
        return self

    def to_agent(self, agent_id: str) -> TaskBuilder:
        """Set the target (executing) agent."""
        self._target_agent = agent_id
        return self

    def with_priority(self, priority: TaskPriority | int) -> TaskBuilder:
        """Set task priority."""
        self._priority = priority.value if isinstance(priority, TaskPriority) else priority
        return self

    def with_task_type(self, task_type: str) -> TaskBuilder:
        """Set the model routing task type."""
        self._task_type = task_type
        return self

    def with_input(self, data: dict[str, Any]) -> TaskBuilder:
        """Set input data."""
        self._input_data = data
        return self

    def with_success_criteria(self, criteria: list[str]) -> TaskBuilder:
        """Define success criteria."""
        self._success_criteria = criteria
        return self

    def with_deadline(self, minutes: int) -> TaskBuilder:
        """Set a deadline in minutes."""
        self._deadline_minutes = minutes
        return self

    def with_escalation(self, escalation_agent: str) -> TaskBuilder:
        """Set the escalation path."""
        self._escalation_path = escalation_agent
        return self

    def with_retries(self, max_retries: int) -> TaskBuilder:
        """Set maximum retry attempts."""
        self._max_retries = max_retries
        return self

    def build(self) -> TaskSpec:
        """Build and validate the TaskSpec.

        Returns:
            Validated TaskSpec.

        Raises:
            ValueError: If required fields are missing.
        """
        if not self._title:
            raise ValueError("Task title is required")
        if not self._target_agent:
            raise ValueError("Target agent is required")

        return TaskSpec(
            title=self._title,
            description=self._description,
            source_agent=self._source_agent,
            target_agent=self._target_agent,
            priority=self._priority,
            task_type=self._task_type,
            input_data=self._input_data,
            success_criteria=self._success_criteria,
            deadline_minutes=self._deadline_minutes,
            escalation_path=self._escalation_path or self._source_agent,
            max_retries=self._max_retries,
        )


__all__ = ["TaskBuilder"]
