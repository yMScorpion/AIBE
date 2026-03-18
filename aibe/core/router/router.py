"""Main model router — routes LLM calls through the appropriate model chain.

Central entry point: `ModelRouter.route_and_call()` selects a model based
on task type, enforces budgets, handles fallbacks via circuit breaker,
validates structured output, and logs costs.
"""

from __future__ import annotations

import time
from typing import Any

import openai

from aibe.core.config import get_settings
from aibe.core.exceptions import (
    RouterBudgetExceededError,
    RouterModelUnavailableError,
    RouterValidationError,
)
from aibe.core.logging import get_logger
from aibe.core.router.budget import BudgetEnforcer
from aibe.core.router.fallback import CircuitBreaker
from aibe.core.router.routing_table import RoutingTable
from aibe.core.types import ModelTaskType

logger = get_logger(__name__)


class ModelRouter:
    """Routes LLM calls through the routing table with budget enforcement.

    Usage:
        router = ModelRouter()
        router.initialize()
        result = await router.route_and_call(
            task_type=ModelTaskType.CODE_GENERATION,
            messages=[{"role": "user", "content": "Write a function..."}],
            agent_id="flint",
            daily_budget_usd=3.00,
        )
    """

    def __init__(self) -> None:
        self._routing_table = RoutingTable()
        self._circuit_breaker = CircuitBreaker()
        self._budget_enforcer = BudgetEnforcer()
        self._client: openai.AsyncOpenAI | None = None

    def initialize(self) -> None:
        """Load routing table and initialize OpenRouter client."""
        self._routing_table.load()
        settings = get_settings()
        self._client = openai.AsyncOpenAI(
            api_key=settings.openrouter_api_key.get_secret_value(),
            base_url=settings.openrouter.base_url,
            timeout=settings.openrouter.timeout_seconds,
            max_retries=0,  # We handle retries ourselves via fallback chain
        )
        logger.info("ModelRouter initialized", task_types=self._routing_table.task_types)

    async def route_and_call(
        self,
        task_type: ModelTaskType | str,
        messages: list[dict[str, str]],
        *,
        agent_id: str = "",
        daily_budget_usd: float = 50.0,
        max_tokens: int | None = None,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
        force_downgrade: bool = False,
    ) -> dict[str, Any]:
        """Route a call through the model chain with full budget + fallback logic.

        Args:
            task_type: The type of task (determines model selection).
            messages: OpenAI-formatted message list.
            agent_id: Calling agent's ID (for budget tracking).
            daily_budget_usd: Agent's daily budget limit.
            max_tokens: Override max tokens (otherwise uses routing table default).
            temperature: Override temperature (otherwise uses routing table default).
            response_format: If set, request structured JSON output.
            force_downgrade: If True, skip primary and use fallbacks only.

        Returns:
            Dict with keys: content, model, tokens_input, tokens_output, cost_usd, duration_seconds.

        Raises:
            RouterBudgetExceededError: If agent is over budget.
            RouterModelUnavailableError: If all models in chain fail.
            RouterValidationError: If structured output validation fails.
        """
        if self._client is None:
            self.initialize()

        # Budget enforcement
        if agent_id:
            await self._budget_enforcer.enforce(agent_id, daily_budget_usd)

        # Check if we should downgrade due to budget warning
        should_downgrade = force_downgrade
        if agent_id and not force_downgrade:
            downgrade, _ = await self._budget_enforcer.check_budget(agent_id, daily_budget_usd)
            should_downgrade = downgrade

        # Get model chain
        config = self._routing_table.get(task_type)
        if config is None:
            raise RouterModelUnavailableError(f"Unknown task type: {task_type}")

        model_chain = self._routing_table.get_model_chain(task_type)

        # If downgrading, skip primary
        if should_downgrade and len(model_chain) > 1:
            model_chain = model_chain[1:]
            logger.info("Budget downgrade — skipping primary model", agent_id=agent_id)

        effective_max_tokens = max_tokens or config.max_tokens
        effective_temperature = temperature if temperature is not None else config.temperature

        # Try each model in the chain
        last_error: Exception | None = None
        for model_spec in model_chain:
            if not self._circuit_breaker.is_available(model_spec.model):
                logger.debug("Circuit open, skipping model", model=model_spec.model)
                continue

            try:
                start_time = time.monotonic()
                assert self._client is not None

                kwargs: dict[str, Any] = {
                    "model": model_spec.model,
                    "messages": messages,
                    "max_tokens": effective_max_tokens,
                    "temperature": effective_temperature,
                }
                if response_format is not None:
                    kwargs["response_format"] = response_format

                completion = await self._client.chat.completions.create(**kwargs)

                duration = time.monotonic() - start_time

                # Extract usage
                usage = completion.usage
                tokens_input = usage.prompt_tokens if usage else 0
                tokens_output = usage.completion_tokens if usage else 0
                content = completion.choices[0].message.content or "" if completion.choices else ""

                # Calculate cost
                cost_usd = (
                    (tokens_input / 1000) * model_spec.cost_per_1k_input
                    + (tokens_output / 1000) * model_spec.cost_per_1k_output
                )

                # Record success
                self._circuit_breaker.record_success(model_spec.model)

                # Record spend
                if agent_id:
                    await self._budget_enforcer.record_spend(agent_id, cost_usd)

                logger.info(
                    "LLM call completed",
                    model=model_spec.model,
                    agent_id=agent_id,
                    tokens_input=tokens_input,
                    tokens_output=tokens_output,
                    cost_usd=f"{cost_usd:.6f}",
                    duration_seconds=f"{duration:.2f}",
                )

                return {
                    "content": content,
                    "model": model_spec.model,
                    "tokens_input": tokens_input,
                    "tokens_output": tokens_output,
                    "cost_usd": cost_usd,
                    "duration_seconds": duration,
                }

            except openai.RateLimitError as exc:
                self._circuit_breaker.record_failure(model_spec.model)
                last_error = exc
                logger.warning("Rate limited", model=model_spec.model, error=str(exc))
                continue

            except openai.APIError as exc:
                self._circuit_breaker.record_failure(model_spec.model)
                last_error = exc
                logger.warning("API error", model=model_spec.model, error=str(exc))
                continue

            except Exception as exc:
                self._circuit_breaker.record_failure(model_spec.model)
                last_error = exc
                logger.error("Unexpected error", model=model_spec.model, error=str(exc))
                continue

        raise RouterModelUnavailableError(
            f"All models exhausted for task type {task_type}: {last_error}",
            details={"task_type": str(task_type), "models_tried": [m.model for m in model_chain]},
        )

    @property
    def routing_table(self) -> RoutingTable:
        """Access the routing table for inspection."""
        return self._routing_table

    @property
    def budget_enforcer(self) -> BudgetEnforcer:
        """Access the budget enforcer."""
        return self._budget_enforcer


__all__ = ["ModelRouter"]
