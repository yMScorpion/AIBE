import { PageHero, Panel, StatGrid } from "@/components/page-kit";

export default function SettingsPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Settings"
        title="Governança global de políticas, orçamento e roteamento"
        subtitle="Painel de configuração central para limites, toggles e trilhas de auditoria."
      />
      <StatGrid
        stats={[
          { label: "Routing Rules", value: "42" },
          { label: "Budget Caps", value: "12" },
          { label: "Agent Toggles", value: "40" },
          { label: "Log Retention", value: "180d" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-2">
        <Panel title="Routing Table Editor" subtitle="Regras de roteamento por contexto e prioridade">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Edição segura com validação e simulação antes de publicar.</p>
        </Panel>
        <Panel title="Budget Limits" subtitle="Limites por domínio, agente e tipo de operação">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Thresholds automáticos com fallback para modo econômico.</p>
        </Panel>
        <Panel title="Agent Toggles" subtitle="Habilitação granular de capacidades e permissões">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Controle fino de tools, web access e autonomia operacional.</p>
        </Panel>
        <Panel title="Audit Logs" subtitle="Trilhas de eventos administrativos e compliance">
          <p className="rounded-lg border border-border bg-secondary/60 p-3 text-sm">Assinatura criptográfica e retenção orientada a política.</p>
        </Panel>
      </section>
    </main>
  );
}
