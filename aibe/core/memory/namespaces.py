"""OpenViking memory namespace definitions.

Maps the full namespace tree from the spec. Every memory
read/write targets a specific namespace path.
"""

from __future__ import annotations

# ═══════════════════════════════════════════════════════════════
# BUSINESS STATE
# ═══════════════════════════════════════════════════════════════
NS_BUSINESS_DECISIONS = "/business/decisions"
NS_BUSINESS_STRATEGY = "/business/strategy"
NS_BUSINESS_KPIS = "/business/kpis"
NS_BUSINESS_MODEL = "/business/model"
NS_BUSINESS_OKRS = "/business/okrs"

# ═══════════════════════════════════════════════════════════════
# AGENT STATE
# ═══════════════════════════════════════════════════════════════
NS_AGENT_EPISODIC = "/agents/{agent_id}/episodic"
NS_AGENT_CONTEXT = "/agents/{agent_id}/context"
NS_AGENT_TASKS = "/agents/{agent_id}/tasks"

# ═══════════════════════════════════════════════════════════════
# MEETINGS
# ═══════════════════════════════════════════════════════════════
NS_MEETINGS_TRANSCRIPTS = "/meetings/transcripts"
NS_MEETINGS_DECISIONS = "/meetings/decisions"
NS_MEETINGS_ACTION_ITEMS = "/meetings/action_items"

# ═══════════════════════════════════════════════════════════════
# RESEARCH
# ═══════════════════════════════════════════════════════════════
NS_RESEARCH_MARKET = "/research/market"
NS_RESEARCH_COMPETITORS = "/research/competitors"
NS_RESEARCH_HYPOTHESES = "/research/hypotheses"
NS_RESEARCH_TRENDS = "/research/trends"

# ═══════════════════════════════════════════════════════════════
# CODEBASE
# ═══════════════════════════════════════════════════════════════
NS_CODEBASE_ARCHITECTURE = "/codebase/architecture"
NS_CODEBASE_SPRINTS = "/codebase/sprints"
NS_CODEBASE_TECH_DEBT = "/codebase/tech_debt"

# ═══════════════════════════════════════════════════════════════
# SECURITY
# ═══════════════════════════════════════════════════════════════
NS_SECURITY_SCANS = "/security/scans"
NS_SECURITY_FINDINGS = "/security/findings"
NS_SECURITY_INCIDENTS = "/security/incidents"
NS_SECURITY_POSTURE = "/security/posture"

# ═══════════════════════════════════════════════════════════════
# ML
# ═══════════════════════════════════════════════════════════════
NS_ML_EXPERIMENTS = "/ml/experiments"
NS_ML_MODELS = "/ml/models"
NS_ML_OPPORTUNITIES = "/ml/opportunities"
NS_ML_PIPELINES = "/ml/pipelines"

# ═══════════════════════════════════════════════════════════════
# SALES
# ═══════════════════════════════════════════════════════════════
NS_SALES_PIPELINE = "/sales/pipeline"
NS_SALES_LEADS = "/sales/leads"
NS_SALES_CONVERSATIONS = "/sales/conversations"

# ═══════════════════════════════════════════════════════════════
# CONTRACTOR
# ═══════════════════════════════════════════════════════════════
NS_CONTRACTOR_ENGAGEMENTS = "/contractor/engagements"
NS_CONTRACTOR_VENDORS = "/contractor/vendors"

# ═══════════════════════════════════════════════════════════════
# MARKETING
# ═══════════════════════════════════════════════════════════════
NS_MARKETING_CAMPAIGNS = "/marketing/campaigns"
NS_MARKETING_CONTENT = "/marketing/content"
NS_MARKETING_SEO = "/marketing/seo"

# ═══════════════════════════════════════════════════════════════
# SOCIAL
# ═══════════════════════════════════════════════════════════════
NS_SOCIAL_POSTS = "/social/posts"
NS_SOCIAL_ENGAGEMENT = "/social/engagement"
NS_SOCIAL_BRAND_VOICE = "/social/brand_voice"

# ═══════════════════════════════════════════════════════════════
# ERRORS & SYSTEM
# ═══════════════════════════════════════════════════════════════
NS_ERRORS_LOG = "/errors/log"
NS_ERRORS_PATTERNS = "/errors/patterns"

# ═══════════════════════════════════════════════════════════════
# EVOLUTION
# ═══════════════════════════════════════════════════════════════
NS_EVOLUTION_PROPOSALS = "/evolution/proposals"
NS_EVOLUTION_TOOLS = "/evolution/tools"
NS_EVOLUTION_ANALYSIS = "/evolution/analysis"

# ═══════════════════════════════════════════════════════════════
# TOOLS
# ═══════════════════════════════════════════════════════════════
NS_TOOLS_REGISTRY = "/tools/registry"
NS_TOOLS_USAGE = "/tools/usage"

# ═══════════════════════════════════════════════════════════════
# PROCUREMENT
# ═══════════════════════════════════════════════════════════════
NS_PROCUREMENT_REQUESTS = "/procurement/requests"
NS_PROCUREMENT_APPROVALS = "/procurement/approvals"

# ═══════════════════════════════════════════════════════════════
# AUDIT
# ═══════════════════════════════════════════════════════════════
NS_AUDIT_COST_LOG = "/audit/cost_log"
NS_AUDIT_ACCESS_LOG = "/audit/access_log"
NS_AUDIT_SYSTEM_LOG = "/audit/system_log"


def agent_namespace(agent_id: str, suffix: str) -> str:
    """Build an agent-specific namespace path.

    Args:
        agent_id: Agent identifier.
        suffix: Namespace suffix (e.g. 'episodic', 'context', 'tasks').

    Returns:
        Full namespace path like '/agents/oracle/episodic'.
    """
    return f"/agents/{agent_id}/{suffix}"


__all__ = [
    "NS_AUDIT_ACCESS_LOG",
    "NS_AUDIT_COST_LOG",
    "NS_AUDIT_SYSTEM_LOG",
    "NS_BUSINESS_DECISIONS",
    "NS_BUSINESS_KPIS",
    "NS_BUSINESS_MODEL",
    "NS_BUSINESS_OKRS",
    "NS_BUSINESS_STRATEGY",
    "NS_CODEBASE_ARCHITECTURE",
    "NS_CODEBASE_SPRINTS",
    "NS_CODEBASE_TECH_DEBT",
    "NS_CONTRACTOR_ENGAGEMENTS",
    "NS_CONTRACTOR_VENDORS",
    "NS_ERRORS_LOG",
    "NS_ERRORS_PATTERNS",
    "NS_EVOLUTION_ANALYSIS",
    "NS_EVOLUTION_PROPOSALS",
    "NS_EVOLUTION_TOOLS",
    "NS_MARKETING_CAMPAIGNS",
    "NS_MARKETING_CONTENT",
    "NS_MARKETING_SEO",
    "NS_MEETINGS_ACTION_ITEMS",
    "NS_MEETINGS_DECISIONS",
    "NS_MEETINGS_TRANSCRIPTS",
    "NS_ML_EXPERIMENTS",
    "NS_ML_MODELS",
    "NS_ML_OPPORTUNITIES",
    "NS_ML_PIPELINES",
    "NS_PROCUREMENT_APPROVALS",
    "NS_PROCUREMENT_REQUESTS",
    "NS_RESEARCH_COMPETITORS",
    "NS_RESEARCH_HYPOTHESES",
    "NS_RESEARCH_MARKET",
    "NS_RESEARCH_TRENDS",
    "NS_SALES_CONVERSATIONS",
    "NS_SALES_LEADS",
    "NS_SALES_PIPELINE",
    "NS_SECURITY_FINDINGS",
    "NS_SECURITY_INCIDENTS",
    "NS_SECURITY_POSTURE",
    "NS_SECURITY_SCANS",
    "NS_SOCIAL_BRAND_VOICE",
    "NS_SOCIAL_ENGAGEMENT",
    "NS_SOCIAL_POSTS",
    "NS_TOOLS_REGISTRY",
    "NS_TOOLS_USAGE",
    "agent_namespace",
]
