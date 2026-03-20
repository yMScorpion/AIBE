import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function MlPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="AI/ML Lab"
        title="Governança de modelos e experimentação com rastreabilidade"
        subtitle="Laboratório para registry, testes e observabilidade de pipelines de machine learning."
      />
      <StatGrid
        stats={[
          { label: "Models in Registry", value: "37" },
          { label: "Experiments Running", value: "9", tone: "good" },
          { label: "Drift Alerts", value: "2", tone: "warn" },
          { label: "Pipeline Uptime", value: "99.1%", tone: "good" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="ModelRegistry.tsx" subtitle="Catálogo versionado e aprovado por política">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">4 modelos candidatos prontos para promoção.</p>
        </Panel>
        <Panel title="ExperimentTracker.tsx" subtitle="Comparativo de métricas e hipóteses">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Melhor experimento superou baseline em +4.3% F1.</p>
        </Panel>
        <Panel title="PipelineHealth.tsx" subtitle="Saúde de jobs de treino e serving">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Sem backlog crítico nos workers de inferência.</p>
        </Panel>
      </section>
    </main>
  );
}
