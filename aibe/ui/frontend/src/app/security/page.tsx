"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, Cell } from "recharts";
import { ShieldAlert, Bug, Activity, ShieldCheck } from "lucide-react";

const threatData = [
  { time: "00:00", threats: 12, blocked: 12 },
  { time: "04:00", threats: 19, blocked: 18 },
  { time: "08:00", threats: 45, blocked: 42 },
  { time: "12:00", threats: 82, blocked: 80 },
  { time: "16:00", threats: 60, blocked: 58 },
  { time: "20:00", threats: 35, blocked: 35 },
  { time: "24:00", threats: 20, blocked: 20 },
];

const vulnData = [
  { severity: "Critical", count: 2 },
  { severity: "High", count: 8 },
  { severity: "Medium", count: 15 },
  { severity: "Low", count: 34 },
];

export default function SecurityPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Security Ops"
        title="Postura defensiva contínua para ambiente multiagente"
        subtitle="Superfície de vigilância para ameaças, vulnerabilidades e governança de risco operacional."
      />
      <StatGrid
        stats={[
          { label: "Threat Level", value: "Elevated", tone: "warn", icon: <ShieldAlert size={20} /> },
          { label: "Open CVEs", value: "6", tone: "hot", icon: <Bug size={20} /> },
          { label: "MTTR", value: "23m", tone: "good", icon: <Activity size={20} /> },
          { label: "Policy Drift", value: "1.2%", tone: "default", icon: <ShieldCheck size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Threat Feed Evolution" subtitle="Ameaças detectadas vs bloqueadas nas últimas 24h">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={threatData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorThreats" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorBlocked" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="time" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="threats" name="Threats" stroke="#ef4444" fillOpacity={1} fill="url(#colorThreats)" />
                <Area type="monotone" dataKey="blocked" name="Blocked" stroke="#10b981" fillOpacity={1} fill="url(#colorBlocked)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Vulnerability Distribution" subtitle="CVEs abertas por severidade">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={vulnData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="severity" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Bar dataKey="count" name="Count">
                  {vulnData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.severity === 'Critical' ? '#ef4444' : entry.severity === 'High' ? '#f97316' : entry.severity === 'Medium' ? '#eab308' : '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Security Gate Validations" subtitle="Status das validações de CI/CD e Deploy" className="xl:col-span-2">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">Service</th>
                  <th className="px-4 py-3 font-medium">Action</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { service: "auth-gateway", action: "Deploy to Prod", status: "Blocked", time: "10m ago" },
                  { service: "payment-processor", action: "Config Update", status: "Passed", time: "1h ago" },
                  { service: "user-service", action: "Deploy to Staging", status: "Passed", time: "2h ago" },
                  { service: "ml-inference-node", action: "Scale Up", status: "Review", time: "3h ago" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.service}</td>
                    <td className="px-4 py-3">{row.action}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs ${row.status === 'Passed' ? 'bg-emerald-500/10 text-emerald-400' : row.status === 'Blocked' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'}`}>
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



