import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function SalesPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Sales & CS"
        title="Execução comercial com retenção ativa e visibilidade total"
        subtitle="Pipeline, conversas e escalations em um cockpit único para receita previsível."
      />
      <StatGrid
        stats={[
          { label: "Pipeline Value", value: "$1.8M", tone: "good" },
          { label: "Win Rate", value: "39%" },
          { label: "Escalations", value: "5", tone: "warn" },
          { label: "NPS Pulse", value: "74", tone: "good" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="PipelineKanban.tsx" subtitle="Negócios por etapa e probabilidade de fechamento">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Maior concentração em proposal e legal review.</p>
        </Panel>
        <Panel title="LiveConversations.tsx" subtitle="Interações comerciais em andamento">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">12 conversas ativas com score de intenção acima de 0.8.</p>
        </Panel>
        <Panel title="EscalationQueue.tsx" subtitle="Fila de casos sensíveis de clientes">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Prioridade máxima para contas enterprise em risco.</p>
        </Panel>
      </section>
    </main>
  );
}



