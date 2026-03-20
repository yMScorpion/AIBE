"use client";

import { useMemo } from "react";
import { useWsStore } from "@/stores/ws-store";
import { useAgentStore } from "../../stores/agent-store";

interface SystemStatusBarProps {
  onOpenNotifications: () => void;
}

export function SystemStatusBar({ onOpenNotifications }: SystemStatusBarProps) {
  const connected = useWsStore((s) => s.connected);
  const events = useWsStore((s) => s.events);
  const agents = useAgentStore((s) => s.agents);
  const runningCount = useMemo(
    () => agents.filter((agent) => agent.status === "running" || agent.status === "ready").length,
    [agents],
  );
  const spend = useAgentStore((s) => s.spendToday);
  const pendingTasks = useAgentStore((s) => s.pendingTasks);

  return (
    <header className="glass sticky top-3 z-20 mb-4 rounded-2xl border border-border/70 px-4 py-3">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <StatusChip label="System Health" value={connected ? "Online" : "Offline"} tone={connected ? "good" : "warn"} />
          <StatusChip label="Agents" value={`${runningCount}/${agents.length || 40}`} tone="info" />
          <StatusChip label="Active Tasks" value={String(pendingTasks)} tone="neutral" />
          <StatusChip label="Cost Today" value={`$${spend.toFixed(2)}`} tone="info" />
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={onOpenNotifications}
            className="rounded-lg border border-border bg-secondary px-3 py-1.5 text-sm hover:bg-accent"
            aria-label="Abrir painel de notificações"
          >
            Alerts
          </button>
          <span className="rounded-lg border border-border bg-secondary px-2.5 py-1 text-xs text-muted-foreground">
            {events.length} eventos
          </span>
        </div>
      </div>
    </header>
  );
}

function StatusChip({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "good" | "warn" | "info" | "neutral";
}) {
  const toneClass =
    tone === "good"
      ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
      : tone === "warn"
        ? "border-amber-500/30 bg-amber-500/10 text-amber-200"
        : tone === "info"
          ? "border-cyber-cyan/30 bg-cyber-cyan/10 text-cyber-cyan"
          : "border-border bg-secondary text-muted-foreground";

  return (
    <div className={`rounded-xl border px-3 py-1.5 ${toneClass}`}>
      <p className="text-[10px] uppercase tracking-[0.2em]">{label}</p>
      <p className="font-mono text-sm font-semibold">{value}</p>
    </div>
  );
}
