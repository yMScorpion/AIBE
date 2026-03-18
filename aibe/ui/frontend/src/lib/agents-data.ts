export interface TierDef {
  id: number;
  name: string;
  color: string;
  agents: { id: string; name: string; role: string }[];
}

export const TIERS: TierDef[] = [
  { id: 0, name: "Executive", color: "#7c3aed", agents: [
    { id: "oracle", name: "Oracle", role: "CEO · Strategic Director" },
    { id: "minerva", name: "Minerva", role: "Chief Strategist · OKRs" },
  ]},
  { id: 1, name: "Research", color: "#3b82f6", agents: [
    { id: "scout", name: "Scout", role: "Market Intelligence" },
    { id: "vega", name: "Vega", role: "Strategic Analyst" },
    { id: "pulse", name: "Pulse", role: "Real-Time Data" },
  ]},
  { id: 2, name: "Product", color: "#06b6d4", agents: [
    { id: "forge", name: "Forge", role: "Tech Lead" },
    { id: "ember", name: "Ember", role: "Frontend Engineer" },
    { id: "flint", name: "Flint", role: "Backend Engineer" },
    { id: "cinder", name: "Cinder", role: "DevOps" },
    { id: "patch", name: "Patch", role: "Bug Fix Specialist" },
    { id: "deploy", name: "Deploy", role: "Release Manager" },
  ]},
  { id: 3, name: "Marketing", color: "#10b981", agents: [
    { id: "helix", name: "Helix", role: "CMO" },
    { id: "quill", name: "Quill", role: "Content Writer" },
    { id: "lumen", name: "Lumen", role: "Visual Creator" },
    { id: "volt", name: "Volt", role: "Paid Ads" },
    { id: "prism", name: "Prism", role: "Analytics" },
  ]},
  { id: 4, name: "Social", color: "#f59e0b", agents: [
    { id: "nova", name: "Nova", role: "Social Director" },
    { id: "spark", name: "Spark", role: "Publishing" },
    { id: "bloom", name: "Bloom", role: "Community" },
    { id: "grove", name: "Grove", role: "Forums" },
    { id: "echo", name: "Echo", role: "Trends" },
  ]},
  { id: 5, name: "Finance", color: "#8b5cf6", agents: [
    { id: "ledger", name: "Ledger", role: "CFO" },
    { id: "atlas", name: "Atlas", role: "Compliance" },
    { id: "procurator", name: "Procurator", role: "Procurement" },
  ]},
  { id: 6, name: "Evolution", color: "#14b8a6", agents: [
    { id: "darwin", name: "Darwin", role: "Self-Improvement" },
    { id: "synth", name: "Synth", role: "Tool Builder" },
    { id: "automata", name: "Automata", role: "Workflow" },
  ]},
  { id: 7, name: "AI / ML", color: "#ec4899", agents: [
    { id: "cipher", name: "Cipher", role: "ML Strategy" },
    { id: "tensor", name: "Tensor", role: "Data Engineer" },
    { id: "neural", name: "Neural", role: "Model Trainer" },
    { id: "optimus", name: "Optimus", role: "MLOps" },
  ]},
  { id: 8, name: "Security", color: "#ef4444", agents: [
    { id: "sentinel", name: "Sentinel", role: "CISO" },
    { id: "auditor", name: "Auditor", role: "Scanner" },
    { id: "vault_keeper", name: "VaultKeeper", role: "Secrets" },
    { id: "penetest", name: "Penetest", role: "Pen Tester" },
    { id: "incident_responder", name: "IncidentResponder", role: "Incidents" },
  ]},
  { id: 9, name: "Sales", color: "#f97316", agents: [
    { id: "mercury", name: "Mercury", role: "Sales Director" },
    { id: "closer", name: "Closer", role: "Deal Closer" },
    { id: "orator", name: "Orator", role: "Demos" },
    { id: "guardian", name: "Guardian", role: "Customer Success" },
    { id: "escalator", name: "Escalator", role: "Upsell" },
  ]},
];

export const ALL_AGENTS = TIERS.flatMap((t) => t.agents.map((a) => ({ ...a, tier: t.id, tierName: t.name, tierColor: t.color })));
export const TIER_COLORS: Record<number, string> = Object.fromEntries(TIERS.map((t) => [t.id, t.color]));