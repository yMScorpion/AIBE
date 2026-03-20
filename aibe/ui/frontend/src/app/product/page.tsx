"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { GitPullRequest, Activity, Bug, Clock } from "lucide-react";

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
        eyebrow="Builder View"
        title="Entrega contínua com visão integral do ciclo de engenharia"
        subtitle="Mapeamento do codebase, pipeline de deploy e rastreamento de bugs em uma única superfície."
      />
      <StatGrid
        stats={[
          { label: "PRs Open", value: "13", tone: "default", icon: <GitPullRequest size={20} /> },
          { label: "Deploy Health", value: "99.4%", tone: "good", icon: <Activity size={20} /> },
          { label: "Critical Bugs", value: "2", tone: "hot", icon: <Bug size={20} /> },
          { label: "Lead Time", value: "4h 12m", tone: "good", icon: <Clock size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Engineering Velocity" subtitle="PRs, Deploys e Bugs por Sprint">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={velocityData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPrs" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="sprint" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="prs" name="PRs Merged" stroke="#3b82f6" fillOpacity={1} fill="url(#colorPrs)" />
                <Area type="monotone" dataKey="deploys" name="Deploys" stroke="#10b981" fillOpacity={0} />
                <Area type="monotone" dataKey="bugs" name="Bugs Found" stroke="#ef4444" fillOpacity={0} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Codebase Health" subtitle="Complexidade ciclomática vs Cobertura de Testes">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={codebaseData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="module" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="coverage" name="Test Coverage (%)" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="complexity" name="Complexity Score" fill="#f59e0b" radius={[4, 4, 0, 0]} />
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



