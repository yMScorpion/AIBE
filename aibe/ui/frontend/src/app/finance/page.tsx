import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function FinancePage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Finance & Ops"
        title="Controle financeiro em tempo real com foco em margem e eficiência"
        subtitle="Visão consolidada de P&L, limites de custos e gestão de parceiros operacionais."
      />
      <StatGrid
        stats={[
          { label: "MRR", value: "$480k", tone: "good" },
          { label: "Gross Margin", value: "71%", tone: "good" },
          { label: "Runway", value: "22 months" },
          { label: "Budget Variance", value: "+2.4%", tone: "warn" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="PLDashboard.tsx" subtitle="Resultado operacional consolidado e previsões">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Receita cresce acima da projeção em três unidades de negócio.</p>
        </Panel>
        <Panel title="CostControl.tsx" subtitle="Políticas de teto, alertas e mitigação de gastos">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Alertas ativos para custo de inferência em horários de pico.</p>
        </Panel>
        <Panel title="ContractorTracker.tsx" subtitle="Governança de terceiros e compromissos financeiros">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Renovação de contratos estratégicos em janela de 15 dias.</p>
        </Panel>
      </section>
    </main>
  );
}



