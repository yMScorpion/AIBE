"use client";

import Link from "next/link";
import { useMemo } from "react";
import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { TIERS, ALL_AGENTS } from "@/lib/agents-data";
import { useWsStore } from "@/stores/ws-store";
import { useAgentStore } from "@/stores/agent-store";
import { useMeetingStore } from "@/stores/meeting-store";

export default function Page() {
  const connected = useWsStore((s) => s.connected);
  const events = useWsStore((s) => s.events);
  const agents = useAgentStore((s) => s.agents);
  const spend = useAgentStore((s) => s.spendToday);
  const meetings = useMeetingStore((s) => s.meetings);
  const realtimeStatuses = useWsStore((s) => s.agentStatuses);
  const latestEvents = useMemo(() => events.slice(0, 8), [events]);
  const mappedAgents = useMemo(
    () =>
      (agents.length > 0 ? agents.map((agent) => ({ id: agent.agent_id, name: agent.agent_name, status: realtimeStatuses[agent.agent_id] || agent.status })) : ALL_AGENTS.map((agent) => ({ id: agent.id, name: agent.name, status: realtimeStatuses[agent.id] || "initializing" }))),
    [agents, realtimeStatuses],
  );
  const activeAgents = useMemo(
    () => mappedAgents.filter((agent) => agent.status === "running" || agent.status === "ready").length,
    [mappedAgents],
  );

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Command Center"
        title="Orquestração visual da frota autônoma em tempo real"
        subtitle="Visual premium para monitorar operações, decisões e custos de todos os agentes com clareza executiva."
        cta={{ label: "Boot Agency", href: "#" }}
        onCtaClick={async () => {
          try {
            await fetch("/api/system/boot", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({}),
            });
            alert("Agency Initialization Started!");
          } catch (e) {
            console.error(e);
            alert("Failed to boot agency.");
          }
        }}
      />
      
      <div className="mb-6 flex gap-4">
        <button
          onClick={async () => {
            try {
              const res = await fetch("/api/system/start-agency", {
                method: "POST",
              });
              const data = await res.json();
              if (data.status === "error") {
                alert(data.message);
              } else {
                alert("Research team has started generating and debating business ideas!");
              }
            } catch (e) {
              console.error(e);
              alert("Failed to start research.");
            }
          }}
          className="rounded-xl bg-cyber-cyan/20 px-6 py-3 text-sm font-semibold text-cyber-cyan border border-cyber-cyan/40 hover:bg-cyber-cyan/30 transition-all shadow-[0_0_15px_rgba(6,182,212,0.15)]"
        >
          Iniciar Pesquisa & Debate Autônomo (Start Agency)
        </button>
      </div>

      <StatGrid
        stats={[
          { label: "Agents Online", value: `${activeAgents}`, tone: connected ? "good" : "warn" },
          { label: "Live Feed Events", value: `${events.length}`, tone: "default" },
          { label: "Meetings", value: `${meetings.length}`, tone: "default" },
          { label: "Spend Today", value: `$${spend.toFixed(2)}`, tone: spend > 100 ? "warn" : "default" },
        ]}
      />

      <section className="mt-4 grid grid-cols-1 gap-4 2xl:grid-cols-[1.45fr_1fr_1fr]">
        <Panel title="AgentUniverse.tsx" subtitle="Visão macro por tier e estado operacional">
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
            {TIERS.map((tier) => {
              const count = mappedAgents.filter((agent) => ALL_AGENTS.find((a) => a.id === agent.id)?.tier === tier.id).length;
              return (
                <Link key={tier.id} href={`/agents/${tier.agents[0]?.id || "oracle"}`} className="rounded-xl border border-border/70 bg-secondary/60 p-3 hover:border-cyber-purple/40 hover:bg-accent/70">
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-semibold" style={{ color: tier.color }}>
                      Tier {tier.id} · {tier.name}
                    </p>
                    <span className="rounded-md border border-border px-2 py-0.5 text-xs">{count}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">Clique para navegar para agentes da trilha.</p>
                </Link>
              );
            })}
          </div>
        </Panel>

        <Panel title="LiveFeed.tsx" subtitle="Fluxo de eventos críticos do ecossistema">
          <div className="space-y-2">
            {latestEvents.length === 0 ? (
              <p className="rounded-xl bg-secondary p-3 text-sm text-muted-foreground">Aguardando eventos do barramento.</p>
            ) : (
              latestEvents.map((event, index) => (
                <article key={`${event.timestamp}-${index}`} className="rounded-xl border border-border/70 bg-secondary/50 p-3">
                  <p className="text-sm font-semibold capitalize">{event.event.replaceAll("_", " ")}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{new Date(event.timestamp).toLocaleString()}</p>
                </article>
              ))
            )}
          </div>
        </Panel>

        <Panel title="QuickActions.tsx" subtitle="Atalhos táticos para fluxos prioritários">
          <div className="grid grid-cols-1 gap-2">
            <Action href="/security" title="Security Gate" description="Revisar incidentes e vulnerabilidades em aberto." />
            <Action href="/finance" title="Cost Control" description="Ajustar orçamento e política de contenção." />
            <Action href="/ml" title="Pipeline Health" description="Monitorar experimentos e registries de modelos." />
            <Action href="/office-3d" title="Virtual Office 3D" description="Navegar o escritório espacial com todos os agentes." />
            <Action href="/settings" title="Routing Table" description="Editar roteamento e toggles globais." />
          </div>
        </Panel>
      </section>
    </main>
  );
}

function Action({ href, title, description }: { href: string; title: string; description: string }) {
  return (
    <Link href={href} className="rounded-xl border border-border bg-secondary/70 p-3 transition hover:border-cyber-cyan/40 hover:bg-accent">
      <p className="text-sm font-semibold">{title}</p>
      <p className="mt-1 text-xs text-muted-foreground">{description}</p>
    </Link>
  );
}
