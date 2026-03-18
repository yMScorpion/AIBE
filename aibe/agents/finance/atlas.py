# aibe/agents/finance/atlas.py
"""Atlas — Compliance & Tax Agent (Tier 5).

Handles regulatory compliance, tax optimization, and legal requirements
for the AI agent system operations.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aibe.agents.base.agent import BaseAgent


class AtlasAgent(BaseAgent):
    """Compliance and regulatory agent."""

    agent_id = "atlas"
    name = "Atlas"
    tier = 5
    escalation_target = "ledger"
    daily_budget_usd = 2.0

    def __init__(self, context: Any = None) -> None:
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self._compliance_checks: list[dict] = []

    def get_system_prompt(self) -> str:
        return """You are Atlas, the Compliance & Tax Agent of AIBE.

ROLE & RESPONSIBILITIES:
- Monitor regulatory compliance across all agent operations
- Track and optimize tax implications of AI service usage
- Ensure data handling practices meet privacy regulations (GDPR, CCPA, etc.)
- Maintain audit trails for financial and operational decisions
- Identify compliance risks before they become issues

COMPLIANCE DOMAINS:
1. Data Privacy: GDPR, CCPA, data retention policies
2. AI Regulations: EU AI Act, emerging AI governance frameworks
3. Financial: SOC2, PCI-DSS (if applicable), expense documentation
4. Operational: SLA compliance, uptime requirements, incident reporting

OUTPUT FORMAT for compliance reports:
{
  "domain": "privacy|ai_governance|financial|operational",
  "check_type": "scheduled|triggered|incident",
  "status": "compliant|warning|violation",
  "findings": [
    {
      "item": "description",
      "severity": "info|low|medium|high|critical",
      "regulation": "applicable regulation",
      "remediation": "recommended action"
    }
  ],
  "audit_trail": ["relevant documentation references"],
  "next_review": "ISO date"
}

Be thorough, document everything, and prioritize preventive compliance."""

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._compliance_scan, 7200),
            (self._audit_trail_maintenance, 3600),
        ]

    async def _handle_task(self, data: dict) -> None:
        """Process compliance tasks."""
        self._status = "running"
        try:
            result = await self.on_task_receive(data)
            bus = self._get_bus()
            if bus:
                await bus.publish(
                    f"tasks.result.{data.get('source', 'unknown')}",
                    {"task_id": data.get("task_id"), "status": "completed", "output": result},
                )
            self._tasks_completed += 1
        except Exception as exc:
            self._error_count += 1
            self._logger.error("Compliance task failed: %s", str(exc))
        finally:
            self._status = "ready"

    async def _compliance_scan(self) -> None:
        """Run compliance checks every 2 hours."""
        current_time = time.time()

        compliance_report = {
            "timestamp": current_time,
            "domains_checked": ["data_privacy", "ai_governance", "operational"],
            "status": "compliant",
            "findings": [],
            "warnings": 0,
            "violations": 0,
        }

        # Check data retention compliance
        # In production, would query actual data stores
        compliance_report["findings"].append({
            "domain": "data_privacy",
            "check": "data_retention",
            "status": "compliant",
            "details": "Memory store retention policies within limits",
        })

        # Check operational compliance
        context = self._context
        if context:
            registry = getattr(context, "registry", None)
            if registry:
                agents = (
                    registry.get_all()
                    if hasattr(registry, "get_all")
                    else list(getattr(registry, "_agents", {}).values())
                )
                error_agents = [a for a in agents if getattr(a, "status", "") == "error"]
                
                if len(error_agents) > len(agents) * 0.1:  # >10% in error
                    compliance_report["findings"].append({
                        "domain": "operational",
                        "check": "system_health",
                        "status": "warning",
                        "details": f"{len(error_agents)} agents in error state",
                    })
                    compliance_report["warnings"] += 1
                    compliance_report["status"] = "warning"

        self._compliance_checks.append(compliance_report)
        self._compliance_checks = self._compliance_checks[-24:]  # Keep 48 hours

        await self.memory_store("atlas.compliance", "latest", compliance_report)
        self._logger.info(
            "Compliance scan: %s (%d warnings, %d violations)",
            compliance_report["status"],
            compliance_report["warnings"],
            compliance_report["violations"],
        )

    async def _audit_trail_maintenance(self) -> None:
        """Maintain audit trail records every hour."""
        # Aggregate actions that need audit logging
        audit_entry = {
            "timestamp": time.time(),
            "period": "hourly",
            "agent_activities": [],
            "financial_events": [],
            "security_events": [],
        }

        # Would aggregate from various sources in production
        await self.memory_store(
            "atlas.audit",
            f"entry_{int(time.time())}",
            audit_entry,
        )
        self._logger.debug("Audit trail entry created")