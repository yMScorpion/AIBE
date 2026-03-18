# aibe/core/exceptions.py
"""Custom exceptions for AIBE system."""

from __future__ import annotations


class AIBEError(Exception):
    """Base exception for all AIBE errors."""

    pass


class BudgetExceededError(AIBEError):
    """Raised when an agent exceeds its daily budget."""

    def __init__(self, agent_id: str, budget: float, spent: float, requested: float) -> None:
        self.agent_id = agent_id
        self.budget = budget
        self.spent = spent
        self.requested = requested
        super().__init__(
            f"Agent '{agent_id}' budget exceeded: "
            f"${spent:.4f} spent + ${requested:.4f} requested > ${budget:.4f} budget"
        )


class AgentNotFoundError(AIBEError):
    """Raised when an agent is not found in the registry."""

    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        super().__init__(f"Agent not found: {agent_id}")


class AgentStartError(AIBEError):
    """Raised when an agent fails to start."""

    def __init__(self, agent_id: str, reason: str) -> None:
        self.agent_id = agent_id
        self.reason = reason
        super().__init__(f"Agent '{agent_id}' failed to start: {reason}")


class TaskExecutionError(AIBEError):
    """Raised when a task execution fails."""

    def __init__(self, task_id: str, agent_id: str, reason: str) -> None:
        self.task_id = task_id
        self.agent_id = agent_id
        self.reason = reason
        super().__init__(f"Task '{task_id}' failed on agent '{agent_id}': {reason}")


class EscalationError(AIBEError):
    """Raised when an escalation cannot be processed."""

    def __init__(self, source: str, target: str, reason: str) -> None:
        self.source = source
        self.target = target
        self.reason = reason
        super().__init__(f"Escalation from '{source}' to '{target}' failed: {reason}")


class ConfigurationError(AIBEError):
    """Raised when configuration is invalid."""

    def __init__(self, key: str, reason: str) -> None:
        self.key = key
        self.reason = reason
        super().__init__(f"Configuration error for '{key}': {reason}")


class InfrastructureError(AIBEError):
    """Raised when infrastructure components fail."""

    def __init__(self, component: str, reason: str) -> None:
        self.component = component
        self.reason = reason
        super().__init__(f"Infrastructure '{component}' error: {reason}")


class ToolExecutionError(AIBEError):
    """Raised when a tool execution fails."""

    def __init__(self, tool_name: str, reason: str) -> None:
        self.tool_name = tool_name
        self.reason = reason
        super().__init__(f"Tool '{tool_name}' execution failed: {reason}")


class WorkflowError(AIBEError):
    """Raised when a workflow execution fails."""

    def __init__(self, workflow_id: str, step_id: str, reason: str) -> None:
        self.workflow_id = workflow_id
        self.step_id = step_id
        self.reason = reason
        super().__init__(f"Workflow '{workflow_id}' failed at step '{step_id}': {reason}")