"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, PieChart, Pie, Cell, LineChart, Line } from "recharts";
import { GitPullRequest, Activity, Bug, Clock, Server, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";

const burndownData = [
  { day: "Day 1", ideal: 100, actual: 100 },
  { day: "Day 2", ideal: 90, actual: 95 },
  { day: "Day 3", ideal: 80, actual: 85 },
  { day: "Day 4", ideal: 70, actual: 60 },
  { day: "Day 5", ideal: 60, actual: 55 },
  { day: "Day 6", ideal: 50, actual: 50 },
  { day: "Day 7", ideal: 40, actual: 35 },
  { day: "Day 8", ideal: 30, actual: 25 },
  { day: "Day 9", ideal: 20, actual: 20 },
  { day: "Day 10", ideal: 10, actual: 5 },
  { day: "Day 11", ideal: 0, actual: 0 },
];

const prSuccessData = [
  { name: "Approved", value: 85 },
  { name: "Changes Requested", value: 10 },
  { name: "Rejected", value: 5 },
];

const prCOLORS = ['hsl(var(--chart-1))', 'hsl(var(--chart-2))', 'hsl(var(--destructive))'];

const latencyData = [
  { time: "10:00", p95: 120, p99: 250 },
  { time: "10:05", p95: 125, p99: 260 },
  { time: "10:10", p95: 115, p99: 240 },
  { time: "10:15", p95: 140, p99: 310 },
  { time: "10:20", p95: 130, p99: 280 },
  { time: "10:25", p95: 120, p99: 245 },
];

const velocityData = [
  { sprint: "Sprint 42", prs: 35, deploys: 12, bugs: 8 },
  { sprint: "Sprint 43", prs: 42, deploys: 15, bugs: 6 },
  { sprint: "Sprint 44", prs: 38, deploys: 14, bugs: 10 },
  { sprint: "Sprint 45", prs: 55, deploys: 20, bugs: 5 },
  { sprint: "Sprint 46", prs: 48, deploys: 18, bugs: 4 },
];

const codebaseData = [
  { module: "Core API", complexity: 85, coverage: 92 },
  { module: "Auth Service", complexity: 40, coverage: 98 },
  { module: "UI Frontend", complexity: 65, coverage: 75 },
  { module: "ML Inference", complexity: 90, coverage: 60 },
  { module: "Payment", complexity: 55, coverage: 95 },
];

export default function ProductPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Tier 2 • Product Department"
        title="Engineering & Infrastructure"
        subtitle="Continuous delivery, code quality, and infrastructure managed by Forge, Ember, and Cinder."
      />
      <StatGrid
        stats={[
          { label: "PRs Open", value: "13", tone: "default", icon: <GitPullRequest size={20} /> },
          { label: "Deploy Health", value: "99.4%", tone: "good", icon: <Activity size={20} /> },
          { label: "Critical Bugs", value: "2", tone: "hot", icon: <Bug size={20} /> },
          { label: "Lead Time", value: "4h 12m", tone: "good", icon: <Clock size={20} /> },
        ]}
      />
      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Sprint Burndown */}
        <Panel title="Sprint Burndown" subtitle="Progress of technical tasks vs estimated time" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={burndownData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--accent))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--accent))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="actual" name="Actual Tasks" stroke="hsl(var(--accent))" strokeWidth={2} fillOpacity={1} fill="url(#colorActual)" />
                <Line type="monotone" dataKey="ideal" name="Ideal Burndown" stroke="hsl(var(--muted-foreground))" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* PR Success Rate */}
        <Panel title="Forge PR Review Rate" subtitle="Code approved vs rejected" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={prSuccessData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {prSuccessData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={prCOLORS[index % prCOLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`${value}%`, 'Share']}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* CI/CD Pipeline Steppers */}
        <Panel title="CI/CD Pipeline" subtitle="Deploy Agent stages in real-time" className="xl:col-span-6">
          <div className="h-[200px] w-full mt-4 flex items-center justify-between px-4">
            {[
              { step: "Build", status: "success", icon: <Server size={24} /> },
              { step: "Test", status: "success", icon: <CheckCircle2 size={24} /> },
              { step: "Canary", status: "active", icon: <RefreshCw size={24} className="animate-spin" /> },
              { step: "Production", status: "pending", icon: <AlertCircle size={24} /> },
            ].map((stage, i, arr) => (
              <div key={i} className="flex items-center flex-1 last:flex-none">
                <div className="flex flex-col items-center gap-3">
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center border-2 ${
                    stage.status === 'success' ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400' :
                    stage.status === 'active' ? 'bg-cyber-cyan/10 border-cyber-cyan text-cyber-cyan shadow-[0_0_15px_rgba(6,182,212,0.5)]' :
                    'bg-white/5 border-white/10 text-muted-foreground'
                  }`}>
                    {stage.icon}
                  </div>
                  <span className={`text-sm font-medium ${stage.status === 'active' ? 'text-white' : 'text-muted-foreground'}`}>{stage.step}</span>
                </div>
                {i < arr.length - 1 && (
                  <div className="flex-1 h-1 mx-4 rounded-full overflow-hidden bg-white/5">
                    <div className={`h-full ${stage.status === 'success' ? 'bg-emerald-500' : stage.status === 'active' ? 'bg-cyber-cyan w-1/2 animate-pulse' : 'bg-transparent'}`}></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Panel>

        {/* API Latency */}
        <Panel title="API Latency Monitor" subtitle="Flint generated endpoints health" className="xl:col-span-6">
          <div className="h-[200px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={latencyData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="time" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="p95" name="p95 (ms)" stroke="hsl(var(--chart-1))" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="p99" name="p99 (ms)" stroke="hsl(var(--destructive))" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Engineering Velocity" subtitle="PRs, Deploys e Bugs por Sprint">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={velocityData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPrs" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="sprint" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="prs" name="PRs Merged" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorPrs)" />
                <Area type="monotone" dataKey="deploys" name="Deploys" stroke="hsl(var(--chart-1))" fillOpacity={0} />
                <Area type="monotone" dataKey="bugs" name="Bugs Found" stroke="hsl(var(--destructive))" fillOpacity={0} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Codebase Health" subtitle="Complexidade ciclomática vs Cobertura de Testes">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={codebaseData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="module" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="coverage" name="Test Coverage (%)" fill="hsl(var(--chart-1))" radius={[4, 4, 0, 0]} />
                <Bar dataKey="complexity" name="Complexity Score" fill="hsl(var(--chart-2))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Active Deployments" subtitle="Status do pipeline e ambientes" className="xl:col-span-2">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">Service</th>
                  <th className="px-4 py-3 font-medium">Environment</th>
                  <th className="px-4 py-3 font-medium">Version</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { service: "frontend-ui", env: "Production", version: "v2.4.1", status: "Healthy", time: "10m ago" },
                  { service: "auth-gateway", env: "Staging", version: "v2.5.0-rc1", status: "Deploying", time: "2m ago" },
                  { service: "ml-router", env: "Production", version: "v1.9.2", status: "Degraded", time: "1h ago" },
                  { service: "payment-api", env: "Production", version: "v3.0.0", status: "Healthy", time: "5h ago" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.service}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 rounded-full text-xs bg-white/10 text-white/80">{row.env}</span>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs">{row.version}</td>
                    <td className="px-4 py-3">
                      <span className={`flex items-center gap-1.5 ${row.status === 'Healthy' ? 'text-emerald-400' : row.status === 'Deploying' ? 'text-cyber-cyan' : 'text-amber-400'}`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${row.status === 'Healthy' ? 'bg-emerald-400' : row.status === 'Deploying' ? 'bg-cyber-cyan animate-pulse' : 'bg-amber-400'}`}></span>
                        {row.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">{row.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      </section>
    </main>
  );
}



