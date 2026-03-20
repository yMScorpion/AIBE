import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function MeetingsPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="War Room"
        title="Coordenação de debates e decisões de alto impacto"
        subtitle="Sala de comando com visão ao vivo de reuniões críticas, divergências e deliberações finais."
      />
      <StatGrid
        stats={[
          { label: "Live Meetings", value: "4", tone: "good" },
          { label: "Debates", value: "11", tone: "hot" },
          { label: "Decisions Today", value: "27" },
          { label: "Consensus Score", value: "91%" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="LiveMeetingView.tsx" subtitle="Transmissão estruturada das sessões em andamento">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Sessão: Growth Budget Rebalance · 8 participantes · fase de votação.</p>
        </Panel>
        <Panel title="DebatePanel.tsx" subtitle="Argumentos pró e contra com peso estratégico">
          <ul className="space-y-2 text-sm">
            <li className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">+ Aumentar investimento em aquisição acelera pipeline.</li>
            <li className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">− Risco de saturação se CAC ultrapassar meta.</li>
          </ul>
        </Panel>
        <Panel title="DecisionLedger.tsx" subtitle="Registro oficial de decisões e responsáveis">
          <ul className="space-y-2 text-sm">
            <li className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Aprovado: corte de 7% em canais com ROAS baixo.</li>
            <li className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Delegado: revisão de pricing até 18:00 UTC.</li>
          </ul>
        </Panel>
      </section>
    </main>
  );
}



