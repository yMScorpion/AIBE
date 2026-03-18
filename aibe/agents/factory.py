"""Agent factory — instantiates all 35 agents with their configs.

Maps agent IDs to their implementation classes and creates
fully configured agent instances from agents.yaml config.
"""

from __future__ import annotations

from typing import Any, Optional, Type

from aibe.agents.base.agent import BaseAgent
from aibe.agents.base.context import AgentContext
from aibe.core.logging import get_logger

logger = get_logger(__name__)

# ── Agent class registry ──────────────────────────────────────
# Maps agent_id to (module_path, class_name, tier)

AGENT_CATALOG: dict[str, tuple[str, str, int]] = {
    # Tier 0 — Executive
    "oracle": ("aibe.agents.executive.oracle", "Oracle", 0),
    "minerva": ("aibe.agents.executive.minerva", "Minerva", 0),
    # Tier 1 — Research
    "scout": ("aibe.agents.research.scout", "Scout", 1),
    "vega": ("aibe.agents.research.vega", "Vega", 1),
    "pulse": ("aibe.agents.research.pulse", "Pulse", 1),
    # Tier 2 — Product Development
    "forge": ("aibe.agents.product.forge", "Forge", 2),
    "ember": ("aibe.agents.product.ember", "Ember", 2),
    "flint": ("aibe.agents.product.flint", "Flint", 2),
    "cinder": ("aibe.agents.product.cinder", "Cinder", 2),
    "patch": ("aibe.agents.product.patch", "Patch", 2),
    "deploy": ("aibe.agents.product.deploy", "Deploy", 2),
    # Tier 3 — Marketing
    "helix": ("aibe.agents.marketing.helix", "Helix", 3),
    "quill": ("aibe.agents.marketing.quill", "Quill", 3),
    "lumen": ("aibe.agents.marketing.lumen", "Lumen", 3),
    "volt": ("aibe.agents.marketing.volt", "Volt", 3),
    "prism": ("aibe.agents.marketing.prism", "Prism", 3),
    # Tier 4 — Social Media
    "nova": ("aibe.agents.social.nova", "Nova", 4),
    "spark": ("aibe.agents.social.spark", "Spark", 4),
    "bloom": ("aibe.agents.social.bloom", "Bloom", 4),
    "grove": ("aibe.agents.social.grove", "Grove", 4),
    "echo": ("aibe.agents.social.echo", "Echo", 4),
    # Tier 5 — Finance
    "ledger": ("aibe.agents.finance.ledger", "Ledger", 5),
    "atlas": ("aibe.agents.finance.atlas", "Atlas", 5),
    # Tier 6 — AI/ML
    "cipher": ("aibe.agents.ai_ml.cipher", "Cipher", 6),
    "tensor": ("aibe.agents.ai_ml.tensor", "Tensor", 6),
    "neural": ("aibe.agents.ai_ml.neural", "Neural", 6),
    "optimus": ("aibe.agents.ai_ml.optimus", "Optimus", 6),
    # Tier 7 — Evolution
    "darwin": ("aibe.agents.evolution.darwin", "Darwin", 7),
    "synth": ("aibe.agents.evolution.synth", "Synth", 7),
    "automata": ("aibe.agents.evolution.automata", "Automata", 7),
    # Tier 8 — Security
    "sentinel": ("aibe.agents.security.sentinel", "Sentinel", 8),
    "auditor": ("aibe.agents.security.auditor", "Auditor", 8),
    "vault_keeper": ("aibe.agents.security.vault_keeper", "VaultKeeper", 8),
    "penetest": ("aibe.agents.security.penetest", "Penetest", 8),
    "incident_responder": ("aibe.agents.security.incident_responder", "IncidentResponder", 8),
    # Tier 9 — Sales (conditional)
    "mercury": ("aibe.agents.sales.mercury", "Mercury", 9),
    "closer": ("aibe.agents.sales.closer", "Closer", 9),
    "orator": ("aibe.agents.sales.orator", "Orator", 9),
    "guardian": ("aibe.agents.sales.guardian", "Guardian", 9),
    "escalator": ("aibe.agents.sales.escalator", "Escalator", 9),
}


def _import_agent_class(module_path: str, class_name: str) -> Type[BaseAgent]:
    """Dynamically import an agent class."""
    import importlib
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def create_agent(
    agent_id: str,
    ctx: AgentContext,
) -> BaseAgent:
    """Create a single agent by ID with the given context.

    Args:
        agent_id: Agent identifier (must be in AGENT_CATALOG).
        ctx: Pre-configured AgentContext.

    Returns:
        Instantiated agent.

    Raises:
        ValueError: If agent_id is not in the catalog.
    """
    if agent_id not in AGENT_CATALOG:
        raise ValueError(f"Unknown agent: {agent_id}. Available: {list(AGENT_CATALOG.keys())}")

    module_path, class_name, _ = AGENT_CATALOG[agent_id]
    agent_cls = _import_agent_class(module_path, class_name)
    agent = agent_cls(ctx)

    logger.info("Agent created", agent_id=agent_id, class_name=class_name)
    return agent


def get_agent_names_by_tier(tier: int) -> list[str]:
    """Get all agent IDs for a specific tier."""
    return [aid for aid, (_, _, t) in AGENT_CATALOG.items() if t == tier]


def get_all_agent_ids() -> list[str]:
    """Get all registered agent IDs."""
    return list(AGENT_CATALOG.keys())


def get_agent_tier(agent_id: str) -> int:
    """Get the tier of an agent."""
    if agent_id not in AGENT_CATALOG:
        raise ValueError(f"Unknown agent: {agent_id}")
    return AGENT_CATALOG[agent_id][2]


__all__ = [
    "AGENT_CATALOG",
    "create_agent",
    "get_agent_names_by_tier",
    "get_agent_tier",
    "get_all_agent_ids",
]
