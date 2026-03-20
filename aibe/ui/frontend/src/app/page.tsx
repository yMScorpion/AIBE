"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
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
import { Area, AreaChart, Bar, BarChart, Pie, PieChart, Line, LineChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";

const performanceDataAll = {
  "24h": [
    { time: "00:00", tasks: 12, cost: 2.4, debates: 2, ideas: 1 },
    { time: "04:00", tasks: 18, cost: 3.6, debates: 4, ideas: 3 },
    { time: "08:00", tasks: 45, cost: 9.0, debates: 12, ideas: 8 },
    { time: "12:00", tasks: 82, cost: 16.4, debates: 24, ideas: 15 },
    { time: "16:00", tasks: 110, cost: 22.0, debates: 30, ideas: 22 },
    { time: "20:00", tasks: 65, cost: 13.0, debates: 18, ideas: 12 },
    { time: "24:00", tasks: 34, cost: 6.8, debates: 5, ideas: 4 },
  ],
  "7d": [
    { time: "Mon", tasks: 210, cost: 42.0, debates: 45, ideas: 28 },
    { time: "Tue", tasks: 280, cost: 56.0, debates: 60, ideas: 35 },
    { time: "Wed", tasks: 320, cost: 64.0, debates: 72, ideas: 40 },
    { time: "Thu", tasks: 290, cost: 58.0, debates: 65, ideas: 38 },
    { time: "Fri", tasks: 350, cost: 70.0, debates: 80, ideas: 45 },
    { time: "Sat", tasks: 150, cost: 30.0, debates: 30, ideas: 15 },
    { time: "Sun", tasks: 120, cost: 24.0, debates: 20, ideas: 10 },
  ],
  "30d": [
    { time: "Week 1", tasks: 1800, cost: 360.0, debates: 400, ideas: 220 },
    { time: "Week 2", tasks: 2100, cost: 420.0, debates: 450, ideas: 260 },
    { time: "Week 3", tasks: 2500, cost: 500.0, debates: 550, ideas: 310 },
    { time: "Week 4", tasks: 2300, cost: 460.0, debates: 500, ideas: 290 },
  ]
};

const departmentData = [
  { name: "Executive", value: 12 },
  { name: "Research", value: 25 },
  { name: "Product", value: 30 },
  { name: "Marketing", value: 18 },
  { name: "Sales", value: 15 },
  { name: "Engineering", value: 22 },
  { name: "Support", value: 10 },
];
const COLORS = ['#7c3aed', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#3b82f6', '#ef4444'];

const conversionData = [
  { name: 'Mon', views: 4000, clicks: 2400, sales: 1400, conversion: 35 },
  { name: 'Tue', views: 3000, clicks: 1398, sales: 1210, conversion: 40 },
  { name: 'Wed', views: 2000, clicks: 9800, sales: 2290, conversion: 23 },
  { name: 'Thu', views: 2780, clicks: 3908, sales: 2000, conversion: 71 },
  { name: 'Fri', views: 1890, clicks: 4800, sales: 2181, conversion: 45 },
  { name: 'Sat', views: 2390, clicks: 3800, sales: 2500, conversion: 65 },
  { name: 'Sun', views: 3490, clicks: 4300, sales: 2100, conversion: 60 },
];

const profitData = [
  { month: 'Jan', revenue: 40000, expenses: 24000, profit: 16000 },
  { month: 'Feb', revenue: 45000, expenses: 28000, profit: 17000 },
  { month: 'Mar', revenue: 55000, expenses: 30000, profit: 25000 },
  { month: 'Apr', revenue: 60000, expenses: 32000, profit: 28000 },
  { month: 'May', revenue: 75000, expenses: 35000, profit: 40000 },
  { month: 'Jun', revenue: 85000, expenses: 38000, profit: 47000 },
];

const interactionData = [
  { source: "Oracle", target: "Scout", messages: 120 },
  { source: "Scout", target: "Pulse", messages: 85 },
  { source: "Minerva", target: "Darwin", messages: 64 },
  { source: "Darwin", target: "Synth", messages: 150 },
  { source: "Synth", target: "Oracle", messages: 45 },
];

type TimeRange = "24h" | "7d" | "30d";

export default function Page() {
  const [timeRange, setTimeRange] = useState<TimeRange>("7d");
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

  const performanceData = performanceDataAll[timeRange];

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
      
      <div className="mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Overview</h2>
          <p className="text-sm text-muted-foreground mt-1">Key metrics for today&apos;s operations</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center rounded-lg bg-black/40 border border-white/10 p-1">
            <button 
              onClick={() => setTimeRange("24h")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${timeRange === "24h" ? "bg-white/10 text-white" : "text-muted-foreground hover:text-white"}`}
            >
              24h
            </button>
            <button 
              onClick={() => setTimeRange("7d")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${timeRange === "7d" ? "bg-white/10 text-white" : "text-muted-foreground hover:text-white"}`}
            >
              7d
            </button>
            <button 
              onClick={() => setTimeRange("30d")}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${timeRange === "30d" ? "bg-white/10 text-white" : "text-muted-foreground hover:text-white"}`}
            >
              30d
            </button>
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
            className="flex items-center gap-2 rounded-xl bg-cyber-purple/20 px-5 py-2.5 text-sm font-semibold text-cyber-purple border border-cyber-purple/40 hover:bg-cyber-purple/30 transition-all shadow-[0_0_20px_rgba(124,58,237,0.15)]"
          >
            <Play size={16} className="fill-current" />
            Start Autonomous Debate
          </button>
        </div>
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
          <div className="space-y-3 mt-2 h-[300px] overflow-y-auto pr-2 scrollbar-hide">
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

        {/* Profit Trend */}
        <Panel title="Revenue & Profit" subtitle="Financial tracking across all operations" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={profitData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="month" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value/1000}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`$${value.toLocaleString()}`, undefined]}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="revenue" name="Revenue" stroke="#10b981" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="expenses" name="Expenses" stroke="#ef4444" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="profit" name="Net Profit" stroke="#06b6d4" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Department Allocation */}
        <Panel title="Resource Allocation" subtitle="Agent distribution by department" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={departmentData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {departmentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Conversion Funnel */}
        <Panel title="Conversion Metrics" subtitle="Weekly sales pipeline performance" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={conversionData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="name" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="views" name="Views" fill="#7c3aed" radius={[4, 4, 0, 0]} maxBarSize={40} />
                <Bar dataKey="clicks" name="Clicks" fill="#06b6d4" radius={[4, 4, 0, 0]} maxBarSize={40} />
                <Bar dataKey="sales" name="Sales" fill="#10b981" radius={[4, 4, 0, 0]} maxBarSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Agent Interactions */}
        <Panel title="Agent Interactions" subtitle="Cross-department communication volume" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={interactionData} layout="vertical" margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="source" type="category" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} width={80} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any, props: any) => [`${value} messages to ${props.payload.target}`, 'Volume']}
                />
                <Bar dataKey="messages" fill="#f59e0b" radius={[0, 4, 4, 0]} barSize={24}>
                  {interactionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[(index + 3) % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
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

