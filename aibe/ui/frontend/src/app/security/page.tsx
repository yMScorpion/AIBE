import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function SecurityPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Security Ops"
        title="Postura defensiva contínua para ambiente multiagente"
        subtitle="Superfície de vigilância para ameaças, vulnerabilidades e governança de risco operacional."
      />
      <StatGrid
        stats={[
          { label: "Threat Level", value: "Elevated", tone: "warn" },
          { label: "Open CVEs", value: "6", tone: "hot" },
          { label: "MTTR", value: "23m", tone: "good" },
          { label: "Policy Drift", value: "1.2%", tone: "default" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="SecurityGate.tsx" subtitle="Validação de políticas antes de ações críticas">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Bloqueio ativo para deploy sem assinatura de segurança.</p>
        </Panel>
        <Panel title="VulnerabilityBoard.tsx" subtitle="Kanban de remediação com priorização por risco">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Colunas: Triage, In Progress, Validation, Closed.</p>
        </Panel>
        <Panel title="ThreatFeed.tsx" subtitle="Inteligência de ameaças e anomalias de runtime">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Indicador recente: tentativas de brute force mitigadas no edge.</p>
        </Panel>
      </section>
    </main>
  );
}



