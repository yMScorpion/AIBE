"""Base tool class and tool registry for AIBE agents.

Tools extend agent capabilities by providing structured,
validated functions they can invoke.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, Field

from aibe.core.logging import get_logger

logger = get_logger(__name__)


# ═══════════════════════════════════════════════════════════════
# BASE TOOL
# ═══════════════════════════════════════════════════════════════


class ToolParameter(BaseModel):
    """A single tool parameter definition."""

    name: str
    type: str = "string"
    description: str = ""
    required: bool = True
    default: Optional[Any] = None


class ToolDefinition(BaseModel):
    """Tool metadata returned to LLMs for function calling."""

    name: str
    description: str
    parameters: list[ToolParameter] = Field(default_factory=list)
    category: str = "general"
    requires_approval: bool = False
    risk_level: int = 1  # 1-10


class BaseTool(ABC):
    """Abstract base class for all tools.

    Subclasses must implement:
        - definition() → ToolDefinition
        - execute(**kwargs) → Any
    """

    @abstractmethod
    def definition(self) -> ToolDefinition:
        """Return the tool metadata for LLM function calling."""
        ...

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with given parameters.

        Args:
            **kwargs: Tool parameters as keyword arguments.

        Returns:
            Tool execution result.
        """
        ...

    @property
    def name(self) -> str:
        """Tool name from its definition."""
        return self.definition().name

    @property
    def requires_approval(self) -> bool:
        """Whether tool execution requires human or higher-tier approval."""
        return self.definition().requires_approval


# ═══════════════════════════════════════════════════════════════
# TOOL REGISTRY
# ═══════════════════════════════════════════════════════════════


class ToolRegistry:
    """Central registry for all available tools.

    Tools can be built-in or dynamically registered by agents
    (e.g. Synth creating new tools).
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register.
        """
        self._tools[tool.name] = tool
        logger.info(
            "Tool registered",
            tool_name=tool.name,
            category=tool.definition().category,
        )

    def unregister(self, name: str) -> None:
        """Remove a tool.

        Args:
            name: Tool name to remove.
        """
        self._tools.pop(name, None)
        logger.info("Tool unregistered", tool_name=name)

    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name.

        Args:
            name: Tool name.

        Returns:
            The tool instance or None.
        """
        return self._tools.get(name)

    def get_by_category(self, category: str) -> list[BaseTool]:
        """Get all tools in a category.

        Args:
            category: Category name.

        Returns:
            List of matching tools.
        """
        return [
            t for t in self._tools.values()
            if t.definition().category == category
        ]

    def list_definitions(self) -> list[ToolDefinition]:
        """Get definitions of all registered tools (for LLM function calling).

        Returns:
            List of ToolDefinition objects.
        """
        return [t.definition() for t in self._tools.values()]

    def list_names(self) -> list[str]:
        """List all registered tool names."""
        return list(self._tools.keys())

    @property
    def count(self) -> int:
        """Number of registered tools."""
        return len(self._tools)

    async def execute(self, name: str, **kwargs: Any) -> Any:
        """Execute a tool by name.

        Args:
            name: Tool name.
            **kwargs: Tool parameters.

        Returns:
            Tool result.

        Raises:
            ValueError: If tool not found.
        """
        tool = self.get(name)
        if tool is None:
            raise ValueError(f"Tool not found: {name}")

        logger.info("Executing tool", tool_name=name)
        result = await tool.execute(**kwargs)
        logger.info("Tool executed", tool_name=name)
        return result


__all__ = [
    "BaseTool",
    "ToolDefinition",
    "ToolParameter",
    "ToolRegistry",
]
