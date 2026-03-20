import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function MarketingPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Marketing Command"
        title="Motor de crescimento com execução omnicanal orientada a ROI"
        subtitle="Campanhas, calendário editorial e SEO analytics com tomada de decisão instantânea."
      />
      <StatGrid
        stats={[
          { label: "Active Campaigns", value: "18", tone: "good" },
          { label: "CTR Avg", value: "6.4%", tone: "good" },
          { label: "CAC Trend", value: "-9.1%", tone: "good" },
          { label: "Organic Lift", value: "+22%", tone: "default" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="Campaign Matrix" subtitle="Distribuição por canal, custo e performance">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Search, social e lifecycle sincronizados com alocação dinâmica de verba.</p>
        </Panel>
        <Panel title="Content Calendar" subtitle="Planejamento de narrativas e lançamentos">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">5 janelas de lançamento esta semana com assets em revisão final.</p>
        </Panel>
        <Panel title="SEO Dashboard" subtitle="Evolução de rankings, tráfego e intenção">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">42 keywords em top 3 e crescimento consistente em cluster estratégico.</p>
        </Panel>
      </section>
    </main>
  );
}



