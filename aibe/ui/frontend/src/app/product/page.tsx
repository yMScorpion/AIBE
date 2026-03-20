import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function ProductPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Builder View"
        title="Entrega contínua com visão integral do ciclo de engenharia"
        subtitle="Mapeamento do codebase, pipeline de deploy e rastreamento de bugs em uma única superfície."
      />
      <StatGrid
        stats={[
          { label: "PRs Open", value: "13" },
          { label: "Deploy Health", value: "99.4%", tone: "good" },
          { label: "Critical Bugs", value: "2", tone: "hot" },
          { label: "Lead Time", value: "4h 12m", tone: "good" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="Codebase Map" subtitle="Arquitetura de módulos, ownership e riscos">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Domínios core, integrações e hotspots de complexidade estão mapeados por criticidade.</p>
        </Panel>
        <Panel title="Deployment Pipeline" subtitle="Estado da esteira de build, testes e release">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Build green · QA validado · canary em 12% do tráfego.</p>
        </Panel>
        <Panel title="Bug Tracker" subtitle="Fila priorizada por impacto em negócio">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">2 críticos, 6 altos, 14 médios. SLA crítico: 2h.</p>
        </Panel>
      </section>
    </main>
  );
}



