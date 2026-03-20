import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function EvolutionPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Evolution Lab"
        title="Ciclo contínuo de autoaperfeiçoamento e seleção de estratégias"
        subtitle="Ambiente para propostas evolutivas, catálogo de ferramentas e análise Darwin de adaptação."
      />
      <StatGrid
        stats={[
          { label: "Proposals", value: "24" },
          { label: "Accepted", value: "11", tone: "good" },
          { label: "Regression Risk", value: "Low", tone: "good" },
          { label: "Tool Candidates", value: "7" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="Proposals Timeline" subtitle="Linha temporal de mudanças propostas">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Roadmap de otimizações alinhado com metas trimestrais.</p>
        </Panel>
        <Panel title="Tool Registry" subtitle="Inventário de capacidades disponíveis e em teste">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Novas ferramentas focadas em automação de diagnóstico.</p>
        </Panel>
        <Panel title="Darwin Analysis" subtitle="Seleção de estratégias por fitness operacional">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Estratégia vencedora reduz custo computacional em 14%.</p>
        </Panel>
      </section>
    </main>
  );
}



