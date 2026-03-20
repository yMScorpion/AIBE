import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function SocialPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Social Studio"
        title="Controle social-first com preview e inteligência de tendência"
        subtitle="Gestão integrada de posts, conversas e sinais culturais com visão de impacto em tempo real."
      />
      <StatGrid
        stats={[
          { label: "Posts Scheduled", value: "46" },
          { label: "Engagement Rate", value: "8.9%", tone: "good" },
          { label: "Trend Velocity", value: "High", tone: "warn" },
          { label: "Community SLA", value: "12m", tone: "good" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Panel title="Post Preview" subtitle="Pré-visualização cross-platform de conteúdo">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">3 criativos aguardando aprovação final com personalização por plataforma.</p>
        </Panel>
        <Panel title="Engagement Feed" subtitle="Fluxo vivo de menções e respostas">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Pico de menções em produto flagship com sentimento líquido positivo.</p>
        </Panel>
        <Panel title="Trend Radar" subtitle="Detecta movimentos emergentes de audiência">
          <p className="rounded-xl border border-white/5 bg-black/20 p-4 text-sm text-muted-foreground">Tema em ascensão: automação sustentável em SMB.</p>
        </Panel>
      </section>
    </main>
  );
}



