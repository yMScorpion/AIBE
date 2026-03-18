"""Meeting type definitions — schedule, participants, agenda templates."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class MeetingTemplate:
    """Configuration template for a meeting type."""

    meeting_type: str
    title_template: str
    required_participants: list[str] = field(default_factory=list)
    optional_participants: list[str] = field(default_factory=list)
    max_rounds: int = 3
    min_quorum: int = 2
    schedule_cron: str = ""  # Empty = on-demand
    agenda_items: list[str] = field(default_factory=list)
    description: str = ""


# ── Meeting templates from spec ───────────────────────────────

STRATEGY_SUMMIT = MeetingTemplate(
    meeting_type="strategy_summit",
    title_template="Strategy Summit — {topic}",
    required_participants=["oracle", "minerva", "forge", "helix", "ledger"],
    optional_participants=["sentinel", "darwin", "cipher"],
    max_rounds=4,
    min_quorum=4,
    schedule_cron="0 9 * * 1",  # Every Monday at 9am
    agenda_items=[
        "KPI review",
        "Strategic priorities update",
        "Resource allocation decisions",
        "Blocker resolution",
    ],
    description="Weekly executive alignment with C-suite agents.",
)

SPRINT_PLANNING = MeetingTemplate(
    meeting_type="sprint_planning",
    title_template="Sprint Planning — {sprint_name}",
    required_participants=["forge", "ember", "flint", "cinder", "patch"],
    optional_participants=["deploy", "auditor"],
    max_rounds=3,
    min_quorum=3,
    schedule_cron="0 10 * * 1",  # Every Monday at 10am
    agenda_items=[
        "Previous sprint outcomes",
        "Backlog review and prioritisation",
        "Task assignment and estimation",
        "Technical debt review",
    ],
    description="Engineering sprint planning session.",
)

SECURITY_REVIEW = MeetingTemplate(
    meeting_type="security_review",
    title_template="Security Review — {review_scope}",
    required_participants=["sentinel", "auditor", "vault_keeper"],
    optional_participants=["penetest", "incident_responder", "forge"],
    max_rounds=3,
    min_quorum=2,
    schedule_cron="0 14 * * 3",  # Every Wednesday at 2pm
    agenda_items=[
        "Open findings review",
        "Scan results discussion",
        "Remediation priorities",
        "Deployment gate status",
    ],
    description="Weekly security posture review.",
)

ML_ROADMAP = MeetingTemplate(
    meeting_type="ml_roadmap",
    title_template="ML Roadmap — {quarter}",
    required_participants=["cipher", "tensor", "neural"],
    optional_participants=["optimus", "automata", "darwin"],
    max_rounds=3,
    min_quorum=2,
    schedule_cron="0 11 1 * *",  # Monthly on 1st at 11am
    agenda_items=[
        "Active experiment updates",
        "New opportunity proposals",
        "Model performance review",
        "Infrastructure needs",
    ],
    description="Monthly ML/AI strategy alignment.",
)

SALES_PIPELINE_REVIEW = MeetingTemplate(
    meeting_type="sales_pipeline_review",
    title_template="Sales Pipeline Review — {period}",
    required_participants=["mercury", "closer", "orator"],
    optional_participants=["guardian", "escalator", "helix"],
    max_rounds=2,
    min_quorum=2,
    agenda_items=[
        "Pipeline metrics review",
        "Top deals update",
        "Conversion rate analysis",
        "Enablement needs",
    ],
    description="Sales team pipeline review (active only when sales tier enabled).",
)

INCIDENT_POSTMORTEM = MeetingTemplate(
    meeting_type="incident_postmortem",
    title_template="Incident Postmortem — {incident_id}",
    required_participants=["incident_responder", "sentinel"],
    optional_participants=["forge", "deploy", "auditor", "oracle"],
    max_rounds=3,
    min_quorum=2,
    agenda_items=[
        "Incident timeline",
        "Root cause analysis",
        "Response assessment",
        "Action items and prevention",
    ],
    description="Post-incident analysis meeting.",
)

EVOLUTION_REVIEW = MeetingTemplate(
    meeting_type="evolution_review",
    title_template="Evolution Review — Cycle {cycle_number}",
    required_participants=["darwin", "synth", "oracle"],
    optional_participants=["forge", "cipher", "sentinel"],
    max_rounds=3,
    min_quorum=2,
    schedule_cron="0 15 */2 * *",  # Every 2 days at 3pm
    agenda_items=[
        "Proposal review queue",
        "Shadow validation results",
        "Approved tool deployments",
        "System improvement metrics",
    ],
    description="Review evolution proposals and tool creation.",
)

STRATEGY_SUMMIT_EMERGENCY = MeetingTemplate(
    meeting_type="strategy_summit_emergency",
    title_template="EMERGENCY Summit — {trigger}",
    required_participants=["oracle", "minerva", "ledger"],
    optional_participants=["sentinel", "forge", "helix"],
    max_rounds=2,
    min_quorum=2,
    agenda_items=[
        "Situation assessment",
        "Immediate response plan",
        "Resource reallocation",
    ],
    description="Emergency strategy meeting triggered by critical events.",
)


ALL_MEETING_TEMPLATES = {
    t.meeting_type: t
    for t in [
        STRATEGY_SUMMIT,
        SPRINT_PLANNING,
        SECURITY_REVIEW,
        ML_ROADMAP,
        SALES_PIPELINE_REVIEW,
        INCIDENT_POSTMORTEM,
        EVOLUTION_REVIEW,
        STRATEGY_SUMMIT_EMERGENCY,
    ]
}


__all__ = [
    "ALL_MEETING_TEMPLATES",
    "EVOLUTION_REVIEW",
    "INCIDENT_POSTMORTEM",
    "ML_ROADMAP",
    "MeetingTemplate",
    "SALES_PIPELINE_REVIEW",
    "SECURITY_REVIEW",
    "SPRINT_PLANNING",
    "STRATEGY_SUMMIT",
    "STRATEGY_SUMMIT_EMERGENCY",
]
