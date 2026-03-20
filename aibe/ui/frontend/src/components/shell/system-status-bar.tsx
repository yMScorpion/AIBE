"use client";

import { useMemo } from "react";
import { useWsStore } from "@/stores/ws-store";
import { useAgentStore } from "../../stores/agent-store";
import { Bell, Search, Terminal } from "lucide-react";

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
    <header className="sticky top-4 z-20 mb-6 flex items-center justify-between gap-4 rounded-3xl bg-card/40 backdrop-blur-md border border-white/5 px-6 py-4 shadow-sm">
      <div className="flex flex-1 items-center gap-6">
        <div className="relative w-full max-w-md hidden md:block">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" size={18} />
          <input 
            type="text" 
            placeholder="Search agents, tasks, or metrics..." 
            className="w-full rounded-2xl bg-black/20 border border-white/10 py-2 pl-10 pr-12 text-sm text-white placeholder-muted-foreground outline-none transition-all focus:border-cyber-purple/50 focus:bg-black/40 focus:ring-1 focus:ring-cyber-purple/50"
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 rounded bg-white/10 px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">
            ⌘K
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 mr-4">
          <StatusChip icon={<Terminal size={14}/>} value={`${runningCount}/${agents.length || 40} Agents`} tone="info" />
          <StatusChip value={`$${spend.toFixed(2)} Cost`} tone={spend > 100 ? "warn" : "neutral"} />
          <div className="h-6 w-[1px] bg-white/10 mx-2"></div>
        </div>

        <button
          type="button"
          onClick={onOpenNotifications}
          className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-muted-foreground transition-all hover:bg-white/10 hover:text-white"
          aria-label="Abrir painel de notificações"
        >
          <Bell size={18} />
          {events.length > 0 && (
            <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-cyber-purple text-[9px] font-bold text-white shadow-sm ring-2 ring-background">
              {events.length > 99 ? "99+" : events.length}
            </span>
          )}
        </button>

        <div className="flex items-center gap-3 pl-2">
          <div className="flex flex-col items-end">
            <span className="text-sm font-semibold text-white">Adriano Admin</span>
            <span className="text-xs text-muted-foreground">CEO Assistant</span>
          </div>
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyber-cyan to-cyber-purple p-[2px] shadow-sm">
            <div className="h-full w-full rounded-[10px] bg-card overflow-hidden">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Adriano" alt="Profile" className="h-full w-full object-cover" />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function StatusChip({
  icon,
  value,
  tone,
}: {
  icon?: React.ReactNode;
  value: string;
  tone: "good" | "warn" | "info" | "neutral";
}) {
  const toneClass =
    tone === "good"
      ? "text-emerald-400"
      : tone === "warn"
        ? "text-amber-400"
        : tone === "info"
          ? "text-cyber-cyan"
          : "text-muted-foreground";

  return (
    <div className="flex items-center gap-1.5 rounded-full border border-white/5 bg-black/20 px-3 py-1 text-sm font-medium">
      {icon && <span className={toneClass}>{icon}</span>}
      <span className={toneClass}>{value}</span>
    </div>
  );
}
