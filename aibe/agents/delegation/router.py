"""Task router — matches tasks to the best available agent."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from aibe.agents.delegation.models import DelegationRule, TaskSpec
from aibe.core.exceptions import TaskRoutingError
from aibe.core.logging import get_logger

if TYPE_CHECKING:
    from aibe.agents.registry import AgentRegistry

logger = get_logger(__name__)

# ── Default delegation rules ─────────────────────────────────

DEFAULT_RULES: list[DelegationRule] = [
    DelegationRule(
        task_type="deep_research",
        preferred_agents=["scout", "vega", "pulse"],
        fallback_agents=["lumen"],
    ),
    DelegationRule(
        task_type="code_generation",
        preferred_agents=["flint", "ember", "cinder"],
        fallback_agents=["forge", "synth"],
    ),
    DelegationRule(
        task_type="standard_generation",
        preferred_agents=["quill", "spark", "bloom", "grove"],
        fallback_agents=["prism"],
    ),
    DelegationRule(
        task_type="complex_reasoning",
        preferred_agents=["oracle", "minerva", "forge", "darwin"],
        fallback_agents=["cipher"],
    ),
    DelegationRule(
        task_type="security_analysis",
        preferred_agents=["auditor", "penetest", "sentinel"],
        fallback_agents=["vault_keeper", "incident_responder"],
    ),
    DelegationRule(
        task_type="ml_design",
        preferred_agents=["cipher", "neural", "tensor"],
        fallback_agents=["optimus"],
    ),
    DelegationRule(
        task_type="simple_classification",
        preferred_agents=["echo", "pulse"],
        fallback_agents=["mercury"],
    ),
    DelegationRule(
        task_type="simple_extraction",
        preferred_agents=["scout", "tensor"],
        fallback_agents=["pulse"],
    ),
    DelegationRule(
        task_type="standard_reasoning",
        preferred_agents=["helix", "nova", "ledger", "atlas"],
        fallback_agents=["oracle"],
    ),
]


class TaskRouter:
    """Routes tasks to the best available agent based on delegation rules.

    Uses a priority-based matching algorithm:
    1. If task.target_agent is set → use it directly
    2. Else find the rule for task.task_type
    3. Try preferred agents in order (only active ones)
    4. Try fallback agents
    5. Raise TaskRoutingError if nobody available
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        rules: Optional[list[DelegationRule]] = None,
    ) -> None:
        self._registry = registry
        self._rules = {r.task_type: r for r in (rules or DEFAULT_RULES)}

    def set_registry(self, registry: AgentRegistry) -> None:
        """Set the agent registry (may be set after init)."""
        self._registry = registry

    def route(self, task: TaskSpec) -> str:
        """Find the best agent for a task.

        Args:
            task: Task specification.

        Returns:
            Agent ID to assign the task to.

        Raises:
            TaskRoutingError: If no suitable agent found.
        """
        # Direct assignment
        if task.target_agent:
            return task.target_agent

        # Rule-based routing
        rule = self._rules.get(task.task_type)
        if rule is None:
            raise TaskRoutingError(
                f"No delegation rule for task type: {task.task_type}",
                details={"task_type": task.task_type, "available_types": list(self._rules.keys())},
            )

        # Try preferred agents
        for agent_id in rule.preferred_agents:
            if self._is_available(agent_id):
                logger.debug("Routed to preferred agent", agent_id=agent_id, task_type=task.task_type)
                return agent_id

        # Try fallback agents
        for agent_id in rule.fallback_agents:
            if self._is_available(agent_id):
                logger.info("Routed to fallback agent", agent_id=agent_id, task_type=task.task_type)
                return agent_id

        raise TaskRoutingError(
            f"No available agent for task type: {task.task_type}",
            details={
                "task_type": task.task_type,
                "preferred": rule.preferred_agents,
                "fallback": rule.fallback_agents,
            },
        )

    def _is_available(self, agent_id: str) -> bool:
        """Check if an agent is registered and in an active state."""
        if self._registry is None:
            return True  # No registry = accept all (testing mode)

        agent = self._registry.get(agent_id)
        if agent is None:
            return False
        return agent.status.value in {"ready", "running"}

    def add_rule(self, rule: DelegationRule) -> None:
        """Add or update a delegation rule."""
        self._rules[rule.task_type] = rule

    def get_rule(self, task_type: str) -> Optional[DelegationRule]:
        """Get the delegation rule for a task type."""
        return self._rules.get(task_type)


__all__ = ["DEFAULT_RULES", "TaskRouter"]
