"""Tests for tool registry and built-in tools."""

from __future__ import annotations

import pytest

from aibe.core.tools.registry import BaseTool, ToolDefinition, ToolParameter, ToolRegistry
from aibe.core.tools.builtins.tools import (
    BUILTIN_TOOLS,
    CalculateTool,
    GetCurrentTimeTool,
    register_builtins,
)


class TestToolDefinition:
    def test_basic_definition(self) -> None:
        defn = ToolDefinition(
            name="test_tool",
            description="A test tool",
            parameters=[
                ToolParameter(name="query", type="string"),
            ],
        )
        assert defn.name == "test_tool"
        assert len(defn.parameters) == 1
        assert not defn.requires_approval


class TestToolRegistry:
    def test_register_and_get(self) -> None:
        registry = ToolRegistry()
        tool = GetCurrentTimeTool()
        registry.register(tool)
        assert registry.get("get_current_time") is tool
        assert registry.count == 1

    def test_unregister(self) -> None:
        registry = ToolRegistry()
        tool = GetCurrentTimeTool()
        registry.register(tool)
        registry.unregister("get_current_time")
        assert registry.get("get_current_time") is None
        assert registry.count == 0

    def test_list_definitions(self) -> None:
        registry = ToolRegistry()
        register_builtins(registry)
        definitions = registry.list_definitions()
        assert len(definitions) == len(BUILTIN_TOOLS)
        names = [d.name for d in definitions]
        assert "web_search" in names
        assert "calculate" in names

    def test_get_by_category(self) -> None:
        registry = ToolRegistry()
        register_builtins(registry)
        research_tools = registry.get_by_category("research")
        assert len(research_tools) >= 2  # web_search, web_scrape

    @pytest.mark.asyncio
    async def test_execute(self) -> None:
        registry = ToolRegistry()
        registry.register(GetCurrentTimeTool())
        result = await registry.execute("get_current_time")
        assert "utc_timestamp" in result
        assert "date" in result

    @pytest.mark.asyncio
    async def test_execute_nonexistent_raises(self) -> None:
        registry = ToolRegistry()
        with pytest.raises(ValueError, match="not found"):
            await registry.execute("nonexistent")


class TestBuiltinTools:
    def test_builtin_count(self) -> None:
        assert len(BUILTIN_TOOLS) == 7

    @pytest.mark.asyncio
    async def test_get_current_time(self) -> None:
        tool = GetCurrentTimeTool()
        result = await tool.execute()
        assert "utc_timestamp" in result
        assert "day_of_week" in result

    @pytest.mark.asyncio
    async def test_calculate(self) -> None:
        tool = CalculateTool()
        result = await tool.execute(expression="(100 * 0.15) + 50")
        assert result["result"] == 65.0

    @pytest.mark.asyncio
    async def test_calculate_error(self) -> None:
        tool = CalculateTool()
        result = await tool.execute(expression="invalid_expr")
        assert "error" in result

    def test_all_tools_have_definitions(self) -> None:
        for tool in BUILTIN_TOOLS:
            defn = tool.definition()
            assert defn.name
            assert defn.description
            assert defn.category

    def test_high_risk_tools_require_approval(self) -> None:
        for tool in BUILTIN_TOOLS:
            defn = tool.definition()
            if defn.risk_level >= 5:
                assert defn.requires_approval, f"{defn.name} is high-risk but doesn't require approval"
