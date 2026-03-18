"""Agent context — dependency injection container for all agent deps."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aibe.agents.registry import AgentRegistry
    from aibe.core.browser.pool import BrowserPool
    from aibe.core.memory.client import OpenVikingClient
    from aibe.core.message_bus.client import NATSBus
    from aibe.core.router.router import ModelRouter
    from aibe.core.tools.registry import ToolRegistry
    from aibe.core.vm_manager.sandbox import SandboxManager


@dataclass
class AgentContext:
    """All dependencies an agent needs, injected at startup.

    Attributes:
        bus: NATS message bus client.
        memory: OpenViking memory client.
        router: LLM model router.
        agent_id: This agent's identifier.
        agent_name: Human-readable agent name.
        tier: Agent tier (0-9).
        daily_budget_usd: Daily LLM budget for this agent.
        browser_pool: Optional Lightpanda browser pool.
        vm_manager: Optional Docker sandbox manager.
        tool_registry: Optional tool registry for function calling.
        agent_registry: Optional registry for looking up other agents.
    """

    bus: NATSBus
    memory: OpenVikingClient
    router: ModelRouter
    agent_id: str
    agent_name: str
    tier: int
    daily_budget_usd: float = 5.0
    browser_pool: Optional[BrowserPool] = None
    vm_manager: Optional[SandboxManager] = None
    tool_registry: Optional[ToolRegistry] = None
    agent_registry: Optional[AgentRegistry] = None


async def create_agent_context(
    agent_id: str,
    agent_name: str,
    tier: int,
    daily_budget_usd: float = 5.0,
    bus: Optional["NATSBus"] = None,
    memory: Optional["OpenVikingClient"] = None,
    router: Optional["ModelRouter"] = None,
    browser_pool: Optional["BrowserPool"] = None,
    vm_manager: Optional["SandboxManager"] = None,
    tool_registry: Optional["ToolRegistry"] = None,
    agent_registry: Optional["AgentRegistry"] = None,
) -> AgentContext:
    """Factory for creating an AgentContext with shared infrastructure.

    If bus/memory/router are not provided, creates and connects new instances.

    Args:
        agent_id: Agent identifier.
        agent_name: Human-readable name.
        tier: Agent tier.
        daily_budget_usd: Daily LLM budget.
        bus: Optional pre-built NATS bus.
        memory: Optional pre-built memory client.
        router: Optional pre-built router.
        browser_pool: Optional pre-built browser pool.
        vm_manager: Optional pre-built VM sandbox manager.
        tool_registry: Optional pre-built tool registry.
        agent_registry: Optional pre-built agent registry.

    Returns:
        Fully initialized AgentContext.
    """
    from aibe.core.memory.client import OpenVikingClient
    from aibe.core.message_bus.client import NATSBus
    from aibe.core.router.router import ModelRouter

    if bus is None:
        bus = NATSBus()
        await bus.connect()
    if memory is None:
        memory = OpenVikingClient()
        await memory.connect()
    if router is None:
        router = ModelRouter()
        router.initialize()
    return AgentContext(
        bus=bus,
        memory=memory,
        router=router,
        agent_id=agent_id,
        agent_name=agent_name,
        tier=tier,
        daily_budget_usd=daily_budget_usd,
        browser_pool=browser_pool,
        vm_manager=vm_manager,
        tool_registry=tool_registry,
        agent_registry=agent_registry,
    )


__all__ = ["AgentContext", "create_agent_context"]