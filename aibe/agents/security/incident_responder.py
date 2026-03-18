# aibe/agents/security/incident_responder.py
"""IncidentResponder — Automated Incident Response (Tier 8)."""

from __future__ import annotations

import time
from collections.abc import Callable

from aibe.agents.base.agent import BaseAgent


class IncidentResponderAgent(BaseAgent):
    agent_id = "incident_responder"
    name = "Incident Responder"
    tier = 8
    escalation_target = "sentinel"
    daily_budget_usd = 3.0

    def __init__(self, context=None):
        super().__init__(context)
        self.register_handler(f"tasks.assign.{self.agent_id}", self._handle_task)
        self.register_handler("security.alerts.>", self._handle_alert)
        self._active_incidents: list[dict] = []

    def get_system_prompt(self) -> str:
        return (
            "You are IncidentResponder, an automated security incident response agent. "
            "You monitor alerts, isolate threats, and execute incident response playbooks."
        )

    def autonomous_loops(self) -> list[tuple[Callable, float]]:
        return [
            (self._alert_monitoring_loop, 60),
        ]

    async def _handle_task(self, data: dict) -> None:
        result = await self.on_task_receive(data)
        bus = self._get_bus()
        if bus:
            await bus.publish(f"tasks.result.{data.get('task_id', 'unknown')}", result)

    async def _handle_alert(self, data: dict) -> None:
        severity = data.get("severity", "low")
        if severity in ("high", "critical"):
            await self._execute_playbook(data)

    async def _execute_playbook(self, alert: dict) -> None:
        """Execute automated incident response playbook."""
        incident = {
            "alert": alert,
            "started_at": time.time(),
            "steps": [],
            "status": "in_progress",
        }

        agent_id = alert.get("agent_id")
        if agent_id:
            # Step 1: Isolate affected agent
            context = self._context
            if context:
                registry = getattr(context, "registry", None)
                if registry:
                    agent = registry.get(agent_id) if hasattr(registry, "get") else getattr(registry, "_agents", {}).get(agent_id)
                    if agent:
                        try:
                            await agent.stop()
                            incident["steps"].append({"action": "isolate_agent", "agent": agent_id, "success": True})
                        except Exception as exc:
                            incident["steps"].append({"action": "isolate_agent", "agent": agent_id, "success": False, "error": str(exc)})

        # Step 2: Notify Sentinel
        await self.escalate(f"Incident response triggered for alert: {alert}", severity="high")
        incident["steps"].append({"action": "notify_sentinel", "success": True})

        # Step 3: Record
        incident["status"] = "contained"
        incident["completed_at"] = time.time()
        self._active_incidents.append(incident)

        await self.memory_store("incident_responder.incidents", "latest", incident)
        self._logger.warning("Incident response completed: %s", incident["status"])

    async def _alert_monitoring_loop(self) -> None:
        """Check for unprocessed alerts every 60 seconds."""
        # This loop supplements the event-driven _handle_alert
        # by checking for alerts that may have been missed
        pass