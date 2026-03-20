"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ALL_AGENTS } from "@/lib/agents-data";
import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { api, type AgentCostDetailResponse, type AgentDetailResponse, type TaskResponse } from "@/lib/api";
import { useWsStore } from "@/stores/ws-store";

export default function AgentDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const liveStatus = useWsStore((s) => s.agentStatuses[id]);
  const [agentDetail, setAgentDetail] = useState<AgentDetailResponse | null>(null);
  const [costDetail, setCostDetail] = useState<AgentCostDetailResponse | null>(null);
  const [tasks, setTasks] = useState<TaskResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);
  const catalogAgent = useMemo(() => ALL_AGENTS.find((item) => item.id === id) || null, [id]);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setApiError(null);

    Promise.all([
      api.agents.get(id),
      api.costs.agent(id).catch(() => null),
      api.tasks.list({ agent_id: id }).catch(() => ({ tasks: [], total: 0 })),
    ])
      .then(([detail, cost, taskList]) => {
        if (!active) {
          return;
        }
        setAgentDetail(detail);
        setCostDetail(cost);
        setTasks(taskList.tasks);
      })
      .catch(() => {
        if (!active) {
          return;
        }
        setApiError("Não foi possível carregar os dados reais deste agente.");
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [id]);

  if (!catalogAgent && !agentDetail && !loading) {
    return (
      <main className="mx-auto max-w-[1680px] pb-8">
        <PageHero
          eyebrow="Agent Detail"
          title="Agente não encontrado"
          subtitle="Este identificador não existe no catálogo nem no backend."
          cta={{ label: "Voltar ao Command Center", href: "/" }}
        />
      </main>
    );
  }

  const displayName = agentDetail?.agent_name || catalogAgent?.name || id;
  const displayRole = catalogAgent?.role || "Agente operacional";
  const displayTier = catalogAgent?.tierName || `Tier ${agentDetail?.tier ?? "-"}`;
  const status = liveStatus || agentDetail?.status || "unknown";
  const dailyBudget = agentDetail?.daily_budget_usd ?? costDetail?.budget_usd ?? 0;
  const spent = costDetail?.total_spent_usd ?? 0;
  const utilization = dailyBudget > 0 ? (spent / dailyBudget) * 100 : 0;

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Agent Detail"
        title={`${displayName} · ${displayRole}`}
        subtitle="Dados operacionais carregados do backend com atualização em tempo real."
        cta={{ label: "Voltar ao Command Center", href: "/" }}
      />
      <StatGrid
        stats={[
          { label: "Tier", value: displayTier },
          { label: "Agent ID", value: id },
          { label: "Status", value: status, tone: status === "running" || status === "ready" ? "good" : "warn" },
          { label: "Tasks", value: String(agentDetail?.tasks_completed ?? tasks.length), tone: "default" },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-2">
        <Panel title="Operational Snapshot" subtitle="Estado e orçamento obtidos pela API">
          <div className="space-y-2 text-sm text-muted-foreground">
            {apiError ? <p className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-3 text-amber-200">{apiError}</p> : null}
            <p>Status atual: {status}</p>
            <p>Uptime: {agentDetail?.uptime_seconds ?? 0}s</p>
            <p>Erros: {agentDetail?.error_count ?? 0}</p>
            <p>Orçamento diário: ${dailyBudget.toFixed(2)}</p>
            <p>Gasto do dia: ${spent.toFixed(2)} ({utilization.toFixed(1)}%)</p>
          </div>
        </Panel>
        <Panel title="Task Stream" subtitle="Últimas tarefas registradas para este agente">
          <ul className="space-y-2 text-sm">
            {loading ? (
              <li className="rounded-lg border border-border bg-secondary/60 p-3">Carregando tarefas...</li>
            ) : tasks.length === 0 ? (
              <li className="rounded-lg border border-border bg-secondary/60 p-3">Nenhuma tarefa encontrada para este agente.</li>
            ) : (
              tasks.slice(0, 6).map((task) => (
                <li key={task.task_id} className="rounded-lg border border-border bg-secondary/60 p-3">
                  <p className="font-medium">{task.title}</p>
                  <p className="mt-1 text-xs text-muted-foreground">Status: {task.status} · Prioridade: {task.priority}</p>
                </li>
              ))
            )}
          </ul>
        </Panel>
        <Panel title="Cost by Model" subtitle="Consumo real por modelo de inferência">
          <ul className="space-y-2 text-sm">
            {costDetail?.by_model?.length ? (
              costDetail.by_model.slice(0, 6).map((entry) => (
                <li key={entry.model} className="rounded-lg border border-border bg-secondary/60 p-3">
                  <p className="font-medium">{entry.model}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    Calls: {entry.calls} · Tokens: {entry.tokens_in + entry.tokens_out} · Custo: ${entry.cost_usd.toFixed(4)}
                  </p>
                </li>
              ))
            ) : (
              <li className="rounded-lg border border-border bg-secondary/60 p-3">Sem breakdown de custo disponível.</li>
            )}
          </ul>
        </Panel>
        <Panel title="Quick Actions" subtitle="Atalhos operacionais para análise e controle">
          <div className="rounded-lg border border-border bg-black/70 p-3 font-mono text-xs text-cyber-green">
            <p>$ aibe agent inspect --id {id}</p>
            <p className="mt-1">$ aibe task list --agent {id}</p>
            <p className="mt-1">$ aibe budget show --agent {id}</p>
            <div className="mt-3 border-t border-border pt-3 text-xs">
              <Link href="/office-3d" className="text-cyber-cyan hover:underline">
                Abrir Escritório 3D
              </Link>
            </div>
          </div>
        </Panel>
      </section>
    </main>
  );
}
