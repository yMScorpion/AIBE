"use client";

import Link from "next/link";
import { useMemo } from "react";
import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { TIERS, ALL_AGENTS } from "@/lib/agents-data";
import { useWsStore } from "@/stores/ws-store";
import { useAgentStore } from "@/stores/agent-store";
import { useMeetingStore } from "@/stores/meeting-store";
import { 
  Activity, 
  Terminal, 
  Users, 
  Zap, 
  Cpu, 
  CheckCircle2, 
  Clock, 
  ShieldCheck, 
  Play, 
  TrendingUp,
  ArrowUpRight,
  BrainCircuit
} from "lucide-react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const performanceData = [
  { time: "00:00", tasks: 12, cost: 2.4 },
  { time: "04:00", tasks: 18, cost: 3.6 },
  { time: "08:00", tasks: 45, cost: 9.0 },
  { time: "12:00", tasks: 82, cost: 16.4 },
  { time: "16:00", tasks: 110, cost: 22.0 },
  { time: "20:00", tasks: 65, cost: 13.0 },
  { time: "24:00", tasks: 34, cost: 6.8 },
];

export default function Page() {
  const connected = useWsStore((s) => s.connected);
  const events = useWsStore((s) => s.events);
  const agents = useAgentStore((s) => s.agents);
  const spend = useAgentStore((s) => s.spendToday);
  const meetings = useMeetingStore((s) => s.meetings);
  const realtimeStatuses = useWsStore((s) => s.agentStatuses);
  
  const latestEvents = useMemo(() => events.slice(0, 5), [events]);
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
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Command Center"
        title="Autonomous Fleet Orchestration"
        subtitle="Real-time monitoring of all 40 autonomous AI agents. Track operational decisions, active workflows, system health, and economic metrics."
        cta={{ label: "Initialize Agency", href: "#" }}
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
      
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Overview</h2>
          <p className="text-sm text-muted-foreground mt-1">Key metrics for today's operations</p>
        </div>
        <button
          onClick={async () => {
            try {
              const res = await fetch("/api/system/start-agency", { method: "POST" });
              const data = await res.json();
              if (data.status === "error") {
                alert(data.message);
              } else {
                alert("Research team has started generating and debating business ideas!");
              }
            } catch (e) {
              console.error(e);
            }
          }}
          className="flex items-center gap-2 rounded-2xl bg-cyber-purple/20 px-6 py-3 text-sm font-semibold text-cyber-purple border border-cyber-purple/40 hover:bg-cyber-purple/30 transition-all shadow-[0_0_20px_rgba(124,58,237,0.15)]"
        >
          <Play size={16} className="fill-current" />
          Start Autonomous Debate
        </button>
      </div>

      <StatGrid
        stats={[
          { label: "Agents Online", value: `${activeAgents}`, trend: "24% up", trendUp: true, icon: <Terminal size={20} /> },
          { label: "Live Events", value: `${events.length}`, trend: "12% up", trendUp: true, icon: <Activity size={20} /> },
          { label: "Active Meetings", value: `${meetings.length}`, trend: "Stable", trendUp: true, icon: <Users size={20} /> },
          { label: "Spend Today", value: `$${spend.toFixed(2)}`, trend: "Within budget", trendUp: spend < 100, icon: <Zap size={20} /> },
        ]}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3 xl:grid-cols-12">
        {/* Main Chart Panel */}
        <Panel 
          title="Performance & Cost Analysis" 
          subtitle="Tasks completed vs API costs over 24h"
          className="xl:col-span-8"
          action={
            <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground bg-black/20 rounded-lg px-3 py-1.5 border border-white/5">
              <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-cyber-cyan"></span> Tasks</span>
              <span className="flex items-center gap-1.5 ml-2"><span className="h-2 w-2 rounded-full bg-cyber-purple"></span> Cost</span>
            </div>
          }
        >
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={performanceData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTasks" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorCost" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#7c3aed" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="tasks" stroke="#06b6d4" strokeWidth={3} fillOpacity={1} fill="url(#colorTasks)" />
                <Area type="monotone" dataKey="cost" stroke="#7c3aed" strokeWidth={3} fillOpacity={1} fill="url(#colorCost)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* System Health */}
        <Panel title="System Health" subtitle="Infrastructure status" className="xl:col-span-4">
          <div className="flex flex-col gap-5 mt-2">
            <div className="flex items-center justify-between p-4 rounded-2xl bg-black/20 border border-white/5">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                  <CheckCircle2 size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">API Gateway</p>
                  <p className="text-xs text-muted-foreground">99.99% Uptime</p>
                </div>
              </div>
              <span className="text-xs font-bold text-emerald-400">12ms</span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-2xl bg-black/20 border border-white/5">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyber-cyan/20 text-cyber-cyan">
                  <Cpu size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">LLM Router</p>
                  <p className="text-xs text-muted-foreground">OpenRouter Active</p>
                </div>
              </div>
              <span className="text-xs font-bold text-cyber-cyan">45ms</span>
            </div>

            <div className="flex items-center justify-between p-4 rounded-2xl bg-black/20 border border-white/5">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyber-purple/20 text-cyber-purple">
                  <ShieldCheck size={20} />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">Security Ops</p>
                  <p className="text-xs text-muted-foreground">Zero Incidents</p>
                </div>
              </div>
              <span className="text-xs font-bold text-cyber-purple">Safe</span>
            </div>
          </div>
        </Panel>

        {/* Agent Universe */}
        <Panel title="Agent Ecosystem" subtitle="Active swarms and their operational states" className="xl:col-span-8">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 mt-2">
            {TIERS.map((tier) => {
              const count = mappedAgents.filter((agent) => ALL_AGENTS.find((a) => a.id === agent.id)?.tier === tier.id).length;
              const total = tier.agents.length;
              const percentage = Math.round((count / (total || 1)) * 100);
              
              return (
                <Link key={tier.id} href={`/agents/${tier.agents[0]?.id || "oracle"}`} className="group relative overflow-hidden rounded-2xl border border-white/5 bg-black/20 p-5 transition-all hover:bg-white/5 hover:border-white/10">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full shadow-[0_0_10px_currentColor]" style={{ backgroundColor: tier.color, color: tier.color }}></div>
                      <p className="text-sm font-bold text-white">{tier.name}</p>
                    </div>
                    <ArrowUpRight size={16} className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex justify-between text-xs">
                      <span className="text-muted-foreground">Active Agents</span>
                      <span className="font-semibold text-white">{count} / {total}</span>
                    </div>
                    <div className="h-1.5 w-full rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full rounded-full transition-all duration-1000" style={{ width: `${percentage}%`, backgroundColor: tier.color }}></div>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </Panel>

        {/* Live Feed */}
        <Panel title="Event Stream" subtitle="Critical messages from the message bus" className="xl:col-span-4" action={<Link href="/events" className="text-xs font-medium text-cyber-cyan hover:underline">View All</Link>}>
          <div className="space-y-3 mt-2">
            {latestEvents.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 text-center">
                <Clock size={32} className="text-muted-foreground/30 mb-3" />
                <p className="text-sm text-muted-foreground">Waiting for bus events...</p>
              </div>
            ) : (
              latestEvents.map((event, index) => (
                <article key={`${event.timestamp}-${index}`} className="flex items-start gap-4 rounded-2xl border border-white/5 bg-black/20 p-4 transition-all hover:bg-white/5">
                  <div className="mt-1 flex h-2 w-2 shrink-0 rounded-full bg-cyber-purple shadow-[0_0_8px_rgba(124,58,237,0.8)]" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold text-white truncate capitalize">{event.event.replaceAll("_", " ")}</p>
                    <p className="mt-1 text-xs text-muted-foreground">{new Date(event.timestamp).toLocaleTimeString()}</p>
                  </div>
                </article>
              ))
            )}
          </div>
        </Panel>

        {/* Quick Actions */}
        <Panel title="Tactical Operations" subtitle="Quick access to priority flows" className="xl:col-span-12">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 mt-2">
            <Action href="/security" icon={<ShieldCheck />} title="Security Gate" description="Review open vulnerabilities." />
            <Action href="/finance" icon={<TrendingUp />} title="Cost Control" description="Adjust budget limits." />
            <Action href="/ml" icon={<BrainCircuit />} title="ML Pipeline" description="Monitor experiments." />
            <Action href="/office-3d" icon={<Users />} title="Virtual Office" description="Navigate 2D space." />
            <Action href="/settings" icon={<Terminal />} title="Routing Table" description="Edit LLM routing." />
          </div>
        </Panel>
      </div>
    </main>
  );
}

function Action({ href, title, description, icon }: { href: string; title: string; description: string; icon: React.ReactNode }) {
  return (
    <Link href={href} className="group flex flex-col justify-between rounded-2xl border border-white/5 bg-black/20 p-5 transition-all hover:border-cyber-cyan/30 hover:bg-cyber-cyan/5">
      <div className="mb-4 inline-flex h-10 w-10 items-center justify-center rounded-xl bg-white/5 text-muted-foreground transition-all group-hover:bg-cyber-cyan/20 group-hover:text-cyber-cyan">
        {icon}
      </div>
      <div>
        <p className="text-sm font-bold text-white group-hover:text-cyber-cyan transition-colors">{title}</p>
        <p className="mt-1 text-xs text-muted-foreground">{description}</p>
      </div>
    </Link>
  );
}

