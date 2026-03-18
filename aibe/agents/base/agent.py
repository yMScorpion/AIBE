"""Base agent abstract class — the foundation all 35 agents inherit from.

Provides the full lifecycle: start, stop, task loop, LLM calls,
memory I/O, browser access, VM execution, task delegation, and
escalation.
"""

from __future__ import annotations

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Optional
from uuid import uuid4

from aibe.agents.base.context import AgentContext
from aibe.agents.base.lifecycle import LifecycleManager
from aibe.core.logging import bind_context, get_logger
from aibe.core.memory.namespaces import agent_namespace
from aibe.core.message_bus.models import (
    AgentStatusChangedMessage,
    EscalationMessage,
    HeartbeatMessage,
    TaskAssignMessage,
    TaskResultMessage,
)
from aibe.core.message_bus.streams import SUBJECT_HEARTBEAT, SUBJECT_TASK_ASSIGN
from aibe.core.types import AgentStatus, ModelTaskType, HEARTBEAT_INTERVAL_SECONDS

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Abstract base class for all AIBE agents.

    Subclasses MUST implement:
        - get_system_prompt() → str
        - on_task_receive(task: TaskAssignMessage) → dict[str, Any]

    Subclasses MAY override:
        - autonomous_loops() → list of async coroutines to run
    """

    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self._lifecycle = LifecycleManager(ctx.agent_id)
        self._logger = get_logger(ctx.agent_id, agent_id=ctx.agent_id, tier=ctx.tier)
        self._start_time = 0.0
        self._tasks_completed = 0
        self._error_count = 0
        self._heartbeat_task: Optional[asyncio.Task[None]] = None
        self._task_loop_task: Optional[asyncio.Task[None]] = None
        self._running = False

    # ── Properties ────────────────────────────────────────────

    @property
    def agent_id(self) -> str:
        return self.ctx.agent_id

    @property
    def agent_name(self) -> str:
        return self.ctx.agent_name

    @property
    def status(self) -> AgentStatus:
        return self._lifecycle.status

    @property
    def uptime_seconds(self) -> float:
        if self._start_time == 0.0:
            return 0.0
        return time.monotonic() - self._start_time

    # ── Abstract methods (subclasses MUST implement) ──────────

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent's LLM calls."""
        ...

    @abstractmethod
    async def on_task_receive(self, task: TaskAssignMessage) -> dict[str, Any]:
        """Handle an incoming task assignment.

        Args:
            task: The task to execute.

        Returns:
            Output data dict to include in TaskResultMessage.
        """
        ...

    # ── Lifecycle ─────────────────────────────────────────────

    async def start(self) -> None:
        """Start the agent: transition to READY, begin heartbeat and task loop."""
        self._lifecycle.transition(AgentStatus.READY, reason="Agent starting")
        self._start_time = time.monotonic()
        self._running = True

        bind_context(agent_id=self.agent_id)

        # Subscribe to task assignments
        subject = SUBJECT_TASK_ASSIGN.format(agent_id=self.agent_id)
        await self.ctx.bus.subscribe(
            subject,
            self._on_raw_task_message,
            durable=f"agent-{self.agent_id}",
        )

        # Start heartbeat
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        self._logger.info("Agent started", agent_name=self.agent_name)

    async def stop(self) -> None:
        """Stop the agent gracefully."""
        self._running = False

        if self._heartbeat_task is not None:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

        if self._task_loop_task is not None:
            self._task_loop_task.cancel()
            self._task_loop_task = None

        self._lifecycle.transition(AgentStatus.STOPPED, reason="Agent stopping")
        self._logger.info("Agent stopped")

    # ── Core capabilities ─────────────────────────────────────

    async def think(
        self,
        prompt: str,
        *,
        task_type: Optional[ModelTaskType] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Make an LLM call via the model router.

        Args:
            prompt: The user/task prompt.
            task_type: Override task type for routing.
            temperature: Override temperature.
            max_tokens: Override max tokens.

        Returns:
            The LLM response content.
        """
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": prompt},
        ]

        result = await self.ctx.router.route_and_call(
            task_type=task_type or ModelTaskType.STANDARD_REASONING,
            messages=messages,
            agent_id=self.agent_id,
            daily_budget_usd=self.ctx.daily_budget_usd,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return str(result["content"])

    async def remember(
        self,
        key: str,
        value: dict[str, Any],
        *,
        namespace_suffix: str = "episodic",
    ) -> None:
        """Store a memory in OpenViking.

        Args:
            key: Memory key.
            value: Data to store.
            namespace_suffix: Namespace suffix (default: 'episodic').
        """
        ns = agent_namespace(self.agent_id, namespace_suffix)
        await self.ctx.memory.store(ns, key, value, agent_id=self.agent_id)

    async def recall(
        self,
        key: str,
        *,
        namespace_suffix: str = "episodic",
    ) -> Optional[dict[str, Any]]:
        """Recall a memory from OpenViking.

        Args:
            key: Memory key.
            namespace_suffix: Namespace suffix.

        Returns:
            Stored value or None.
        """
        ns = agent_namespace(self.agent_id, namespace_suffix)
        return await self.ctx.memory.recall(ns, key)

    async def assign_task(
        self,
        target_agent: str,
        title: str,
        description: str = "",
        *,
        priority: int = 2,
        task_type: str = "standard_reasoning",
    ) -> str:
        """Assign a task to another agent via the message bus.

        Args:
            target_agent: Target agent ID.
            title: Task title.
            description: Task description.
            priority: Task priority (0=critical, 3=low).
            task_type: Model routing hint.

        Returns:
            The generated task ID.
        """
        task_id = str(uuid4())
        message = TaskAssignMessage(
            task_id=task_id,
            source_agent=self.agent_id,
            target_agent=target_agent,
            title=title,
            description=description,
            priority=priority,
            task_type=task_type,
            escalation_path=self.agent_id,
        )

        subject = SUBJECT_TASK_ASSIGN.format(agent_id=target_agent)
        await self.ctx.bus.publish(subject, message)

        self._logger.info(
            "Task assigned",
            task_id=task_id,
            target_agent=target_agent,
            title=title,
        )
        return task_id

    async def escalate(
        self,
        reason: str,
        severity: str = "medium",
        context: Optional[dict[str, Any]] = None,
    ) -> None:
        """Escalate an issue to a higher-tier agent.

        Args:
            reason: Why the escalation is needed.
            severity: Severity level.
            context: Additional context data.
        """
        message = EscalationMessage(
            source_agent=self.agent_id,
            target_agent="oracle",  # Default escalation target
            severity=severity,
            reason=reason,
            context=context or {},
        )

        await self.ctx.bus.publish("tasks.escalation.oracle", message)
        self._logger.warning("Escalation sent", reason=reason, severity=severity)

    # ── Internal loops ────────────────────────────────────────

    async def _heartbeat_loop(self) -> None:
        """Periodically publish heartbeat messages."""
        while self._running:
            try:
                heartbeat = HeartbeatMessage(
                    source_agent=self.agent_id,
                    agent_status=self.status.value,
                    uptime_seconds=self.uptime_seconds,
                    tasks_completed=self._tasks_completed,
                    error_count=self._error_count,
                )
                subject = SUBJECT_HEARTBEAT.format(agent_id=self.agent_id)
                await self.ctx.bus.publish(subject, heartbeat)
            except Exception as exc:
                self._logger.error("Heartbeat failed", error=str(exc))

            await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)

    async def _on_raw_task_message(self, msg: Any) -> None:
        """Handle raw NATS task message — deserialize and dispatch."""
        try:
            task = TaskAssignMessage.model_validate_json(msg.data)
            self._lifecycle.transition(AgentStatus.RUNNING, reason=f"Task: {task.title}")

            output_data = await self.on_task_receive(task)

            # Publish result
            result = TaskResultMessage(
                source_agent=self.agent_id,
                target_agent=task.source_agent,
                task_id=task.task_id,
                status="completed",
                output_data=output_data,
            )
            await self.ctx.bus.publish(
                f"tasks.result.{task.source_agent}",
                result,
            )

            self._tasks_completed += 1
            self._lifecycle.transition(AgentStatus.READY, reason="Task completed")

        except Exception as exc:
            self._error_count += 1
            self._logger.error("Task execution failed", error=str(exc))

            if self._lifecycle.can_transition(AgentStatus.ERROR):
                self._lifecycle.transition(AgentStatus.ERROR, reason=str(exc))

            # Try to recover
            if self._lifecycle.can_transition(AgentStatus.READY):
                self._lifecycle.transition(AgentStatus.READY, reason="Error recovery")

        finally:
            # Acknowledge the message
            try:
                await msg.ack()
            except Exception:
                pass


__all__ = ["BaseAgent"]
