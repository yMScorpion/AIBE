"""Tests for agent factory — catalog, creation, tier queries."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from aibe.agents.base.context import AgentContext
from aibe.agents.factory import (
    AGENT_CATALOG,
    create_agent,
    get_agent_names_by_tier,
    get_agent_tier,
    get_all_agent_ids,
)


def _mock_context(agent_id: str = "oracle") -> AgentContext:
    return AgentContext(
        bus=AsyncMock(),
        memory=AsyncMock(),
        router=MagicMock(),
        agent_id=agent_id,
        agent_name=agent_id.title(),
        tier=AGENT_CATALOG[agent_id][2],
        daily_budget_usd=5.0,
    )


class TestAgentCatalog:
    def test_has_41_agents(self) -> None:
        assert len(AGENT_CATALOG) == 41

    def test_all_tiers_represented(self) -> None:
        tiers = {t for _, _, t in AGENT_CATALOG.values()}
        assert tiers == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    def test_tier_0_has_oracle_and_minerva(self) -> None:
        tier_0 = get_agent_names_by_tier(0)
        assert "oracle" in tier_0
        assert "minerva" in tier_0

    def test_tier_5_has_procurator(self) -> None:
        tier_5 = get_agent_names_by_tier(5)
        assert "procurator" in tier_5
        assert "ledger" in tier_5
        assert "atlas" in tier_5

    def test_tier_6_is_evolution(self) -> None:
        tier_6 = get_agent_names_by_tier(6)
        assert "darwin" in tier_6
        assert "synth" in tier_6
        assert "automata" in tier_6

    def test_tier_7_is_ai_ml(self) -> None:
        tier_7 = get_agent_names_by_tier(7)
        assert "cipher" in tier_7
        assert "tensor" in tier_7
        assert "neural" in tier_7
        assert "optimus" in tier_7

    def test_tier_9_has_sales_agents(self) -> None:
        tier_9 = get_agent_names_by_tier(9)
        assert len(tier_9) == 5
        assert "mercury" in tier_9

    def test_get_all_ids(self) -> None:
        ids = get_all_agent_ids()
        assert len(ids) == 41
        assert "oracle" in ids
        assert "escalator" in ids
        assert "procurator" in ids

    def test_get_agent_tier(self) -> None:
        assert get_agent_tier("oracle") == 0
        assert get_agent_tier("forge") == 2
        assert get_agent_tier("sentinel") == 8
        assert get_agent_tier("darwin") == 6
        assert get_agent_tier("cipher") == 7


class TestAgentCreation:
    def test_create_oracle(self) -> None:
        ctx = _mock_context("oracle")
        agent = create_agent("oracle", ctx)
        assert agent.agent_id == "oracle"
        assert "CEO" in agent.get_system_prompt() or "Oracle" in agent.get_system_prompt()

    def test_create_sentinel(self) -> None:
        ctx = _mock_context("sentinel")
        agent = create_agent("sentinel", ctx)
        assert agent.agent_id == "sentinel"

    def test_create_procurator(self) -> None:
        ctx = _mock_context("procurator")
        agent = create_agent("procurator", ctx)
        assert agent.agent_id == "procurator"
        assert "Procurement" in agent.get_system_prompt() or "Procurator" in agent.get_system_prompt()

    def test_create_unknown_raises(self) -> None:
        ctx = _mock_context("oracle")
        with pytest.raises(ValueError, match="Unknown agent"):
            create_agent("nonexistent", ctx)

    def test_create_all_agents(self) -> None:
        """Verify every agent in the catalog can be instantiated."""
        for agent_id in AGENT_CATALOG:
            ctx = _mock_context(agent_id)
            ctx.agent_id = agent_id
            ctx.tier = AGENT_CATALOG[agent_id][2]
            agent = create_agent(agent_id, ctx)
            assert agent.agent_id == agent_id
            assert agent.get_system_prompt()  # Non-empty prompt