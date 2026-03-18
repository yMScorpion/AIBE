"""Built-in tools available to all agents.

These are registered automatically during system startup.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from aibe.core.tools.registry import BaseTool, ToolDefinition, ToolParameter


class WebSearchTool(BaseTool):
    """Search the web via Exa/SerpApi/Jina."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="web_search",
            description="Search the web for current information on a topic.",
            parameters=[
                ToolParameter(name="query", type="string", description="Search query"),
                ToolParameter(name="max_results", type="integer", description="Max results", required=False, default=10),
            ],
            category="research",
            risk_level=1,
        )

    async def execute(self, **kwargs: Any) -> Any:
        # Placeholder — will be connected to Exa/SerpApi in Phase 3
        query = kwargs.get("query", "")
        return {"query": query, "results": [], "source": "web_search", "note": "Not yet connected"}


class WebScrapeTool(BaseTool):
    """Scrape a webpage for content extraction."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="web_scrape",
            description="Scrape and extract content from a specific URL.",
            parameters=[
                ToolParameter(name="url", type="string", description="URL to scrape"),
                ToolParameter(name="selector", type="string", description="CSS selector", required=False, default="body"),
            ],
            category="research",
            risk_level=2,
        )

    async def execute(self, **kwargs: Any) -> Any:
        url = kwargs.get("url", "")
        return {"url": url, "content": "", "note": "Requires Lightpanda connection"}


class SendEmailTool(BaseTool):
    """Send an email via Resend API."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="send_email",
            description="Send an email to a recipient via Resend.",
            parameters=[
                ToolParameter(name="to", type="string", description="Recipient email"),
                ToolParameter(name="subject", type="string", description="Email subject"),
                ToolParameter(name="body", type="string", description="Email body (HTML supported)"),
            ],
            category="communication",
            requires_approval=True,
            risk_level=5,
        )

    async def execute(self, **kwargs: Any) -> Any:
        return {"status": "pending_approval", "note": "Requires human approval and Resend API key"}


class RunCodeTool(BaseTool):
    """Execute code in a sandboxed Docker container."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="run_code",
            description="Execute code safely in an isolated sandbox container.",
            parameters=[
                ToolParameter(name="code", type="string", description="Code to execute"),
                ToolParameter(name="language", type="string", description="Language: python, node, shell", required=False, default="python"),
            ],
            category="development",
            requires_approval=True,
            risk_level=7,
        )

    async def execute(self, **kwargs: Any) -> Any:
        return {"status": "pending", "note": "Requires Docker sandbox manager"}


class GetCurrentTimeTool(BaseTool):
    """Get the current UTC timestamp."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_current_time",
            description="Get the current UTC date and time.",
            parameters=[],
            category="utility",
            risk_level=1,
        )

    async def execute(self, **kwargs: Any) -> Any:
        now = datetime.now(tz=timezone.utc)
        return {
            "utc_timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"),
        }


class MemorySearchTool(BaseTool):
    """Semantic search across agent memory namespaces."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="memory_search",
            description="Search agent memory for relevant past information.",
            parameters=[
                ToolParameter(name="query", type="string", description="Search query"),
                ToolParameter(name="namespace", type="string", description="Memory namespace to search"),
                ToolParameter(name="limit", type="integer", description="Max results", required=False, default=10),
            ],
            category="memory",
            risk_level=1,
        )

    async def execute(self, **kwargs: Any) -> Any:
        return {"results": [], "note": "Requires OpenViking connection"}


class CalculateTool(BaseTool):
    """Perform mathematical calculations safely."""

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="calculate",
            description="Evaluate mathematical expressions safely.",
            parameters=[
                ToolParameter(name="expression", type="string", description="Math expression (e.g. '(100 * 0.15) + 50')"),
            ],
            category="utility",
            risk_level=1,
        )

    async def execute(self, **kwargs: Any) -> Any:
        expression = kwargs.get("expression", "")
        try:
            # Safe eval with restricted builtins
            allowed = {"__builtins__": {"abs": abs, "round": round, "min": min, "max": max, "sum": sum}}
            result = eval(expression, allowed)  # noqa: S307
            return {"expression": expression, "result": result}
        except Exception as exc:
            return {"expression": expression, "error": str(exc)}


# ── All built-in tools ────────────────────────────────────────

BUILTIN_TOOLS = [
    WebSearchTool(),
    WebScrapeTool(),
    SendEmailTool(),
    RunCodeTool(),
    GetCurrentTimeTool(),
    MemorySearchTool(),
    CalculateTool(),
]


def register_builtins(registry: Any) -> None:
    """Register all built-in tools with a ToolRegistry.

    Args:
        registry: ToolRegistry instance.
    """
    for tool in BUILTIN_TOOLS:
        registry.register(tool)


__all__ = [
    "BUILTIN_TOOLS",
    "CalculateTool",
    "GetCurrentTimeTool",
    "MemorySearchTool",
    "RunCodeTool",
    "SendEmailTool",
    "WebScrapeTool",
    "WebSearchTool",
    "register_builtins",
]
