# aibe/agents/base/agent.py
"""Base agent class with autonomous loop support."""

from __future__ import annotations

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class BaseAgent(ABC):
    """Abstract base for all AIBE agents."""

    agent_id: str = "base"
    name: str = "Base Agent"
    tier: int = -1
    escalation_target: str | None = None
    daily_budget_usd: float = 1.0

    def __init__(self, context: Any = None) -> None:
        self._context = context
        self._logger = logging.getLogger(f"aibe.agent.{self.agent_id}")
        self._running = False
        self._start_time: float | None = None
        self._tasks_completed: int = 0
        self._error_count: int = 0
        self._autonomous_tasks: list[asyncio.Task] = []
        self._status = "initializing"
        self._handlers: dict[str, Callable] = {}

    # --- Properties ----------------------------------------------------------

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    # --- Abstract methods ----------------------------------------------------

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the agent's system prompt."""
        ...

    # --- Lifecycle -----------------------------------------------------------

    async def start(self) -> None:
        """Start the agent: subscribe to bus, launch autonomous loops."""
        self._running = True
        self._start_time = time.time()
        self._status = "ready"
        self._logger.info("Agent %s starting", self.agent_id)

        # Subscribe handlers to bus
        bus = self._get_bus()
        if bus is not None:
            for subject, handler in self._handlers.items():
                try:
                    await bus.subscribe(subject, handler)
                except Exception:
                    self._logger.warning("Could not subscribe to %s", subject)

        # Launch autonomous loops
        for coro_fn, interval in self.autonomous_loops():
            task = asyncio.create_task(self._loop_wrapper(coro_fn, interval))
            self._autonomous_tasks.append(task)

        self._status = "running" if self._autonomous_tasks else "ready"
        self._logger.info("Agent %s started (%d loops)", self.agent_id, len(self._autonomous_tasks))

    async def stop(self) -> None:
        """Stop the agent and cancel all autonomous loops."""
        self._running = False
        self._status = "stopped"
        for task in self._autonomous_tasks:
            if not task.done():
                task.cancel()
        if self._autonomous_tasks:
            await asyncio.gather(*self._autonomous_tasks, return_exceptions=True)
        self._autonomous_tasks.clear()
        self._logger.info("Agent %s stopped", self.agent_id)

    # --- Autonomous loops ----------------------------------------------------

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        """Override to define (coroutine_fn, interval_seconds) pairs.
        Default: no autonomous loops.
        """
        return []

    async def _loop_wrapper(self, coro_fn: Callable, interval: float) -> None:
        """Run a coroutine on a fixed interval with error recovery."""
        await asyncio.sleep(1)  # Initial delay
        while self._running:
            try:
                await coro_fn()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                self._error_count += 1
                self._logger.error(
                    "Autonomous loop %s failed: %s",
                    coro_fn.__name__,
                    str(exc),
                )
            await asyncio.sleep(interval)

    # --- Core capabilities ---------------------------------------------------

    async def think(self, prompt: str, **kwargs) -> str:
        """Call the LLM through the model router."""
        router = self._get_router()
        if router is None:
            self._logger.warning("No router available — returning empty response")
            return ""
        try:
            from aibe.core.exceptions import BudgetExceededError

            try:
                result = await router.route_and_call(
                    agent_id=self.agent_id,
                    system_prompt=self.get_system_prompt(),
                    user_prompt=prompt,
                    **kwargs,
                )
                return result
            except BudgetExceededError:
                await self.escalate("Daily budget exceeded", severity="high")
                raise
        except ImportError:
            return ""

    async def escalate(self, message: str, severity: str = "medium") -> None:
        """Escalate an issue to the escalation target."""
        self._logger.warning(
            "ESCALATION [%s] from %s: %s",
            severity,
            self.agent_id,
            message,
        )
        bus = self._get_bus()
        if bus and self.escalation_target:
            try:
                await bus.publish(
                    f"tasks.escalation.{self.escalation_target}",
                    {
                        "source": self.agent_id,
                        "message": message,
                        "severity": severity,
                    },
                )
            except Exception:
                pass

    async def on_task_receive(self, data: dict) -> dict:
        """Handle an incoming task. Override for custom logic."""
        self._logger.info("Received task: %s", data.get("title", "untitled"))
        prompt = f"Task: {data.get('title', '')}\nDescription: {data.get('description', '')}"
        result = await self.think(prompt)
        self._tasks_completed += 1
        return {"status": "completed", "output": result}

    # --- Memory access -------------------------------------------------------

    async def memory_store(self, namespace: str, key: str, value: Any) -> None:
        memory = self._get_memory()
        if memory:
            try:
                await memory.store(namespace, key, value)
            except Exception:
                self._logger.debug("Memory store failed")

    async def memory_recall(self, namespace: str, key: str) -> Any:
        memory = self._get_memory()
        if memory:
            try:
                return await memory.recall(namespace, key)
            except Exception:
                return None
        return None

    # --- Internal helpers ----------------------------------------------------

    def _get_bus(self):
        if self._context and hasattr(self._context, "bus"):
            return self._context.bus
        return None

    def _get_router(self):
        if self._context and hasattr(self._context, "router"):
            return self._context.router
        return None

    def _get_memory(self):
        if self._context and hasattr(self._context, "memory"):
            return self._context.memory
        return None

    def register_handler(self, subject: str, handler: Callable) -> None:
        """Register a message bus handler."""
        self._handlers[subject] = handler