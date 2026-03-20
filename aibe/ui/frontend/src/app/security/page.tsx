"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { useMockStream, fluctuateInt } from "@/lib/mock-stream";
import { ResponsiveContainer, Tooltip, Cell, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, PieChart, Pie, Treemap, LineChart, Line, CartesianGrid, XAxis, YAxis, Legend } from "recharts";
import { ShieldAlert, Bug, Activity, ShieldCheck, Lock, Unlock } from "lucide-react";



const attackVectorData = [
  { subject: 'API Gateway', A: 120, fullMark: 150 },
  { subject: 'Auth', A: 98, fullMark: 150 },
  { subject: 'Database', A: 86, fullMark: 150 },
  { subject: 'Injection', A: 99, fullMark: 150 },
  { subject: 'Social Eng.', A: 85, fullMark: 150 },
  { subject: 'DDoS', A: 65, fullMark: 150 },
];

const falsePositiveData = [
  { name: 'True Positives', value: 85, fill: 'hsl(var(--destructive))' },
  { name: 'False Positives', value: 15, fill: 'hsl(var(--primary))' },
];

const playbookSteps = [
  { step: 1, name: "Detect", status: "completed", time: "10:02 AM" },
  { step: 2, name: "Contain", status: "current", time: "In Progress" },
  { step: 3, name: "Eradicate", status: "pending", time: "--" },
  { step: 4, name: "Recover", status: "pending", time: "--" },
  { step: 5, name: "Post-Mortem", status: "pending", time: "--" },
];

const treemapData = [
  {
    name: "Critical",
    children: [
      { name: "SQL Injection", size: 400 },
      { name: "RCE", size: 300 },
      { name: "Auth Bypass", size: 200 },
    ],
  },
  {
    name: "High",
    children: [
      { name: "XSS", size: 500 },
      { name: "CSRF", size: 300 },
    ],
  },
  {
    name: "Medium",
    children: [
      { name: "Information Disclosure", size: 200 },
      { name: "Misconfiguration", size: 100 },
    ],
  },
];

const mttdMttrData = [
  { day: "Mon", mttd: 15, mttr: 45 },
  { day: "Tue", mttd: 12, mttr: 40 },
  { day: "Wed", mttd: 18, mttr: 50 },
  { day: "Thu", mttd: 10, mttr: 35 },
  { day: "Fri", mttd: 8, mttr: 30 },
  { day: "Sat", mttd: 14, mttr: 42 },
  { day: "Sun", mttd: 11, mttr: 38 },
];

export default function SecurityPage() {
  const dynamicAttackVectorData = useMockStream(attackVectorData, (data) => 
    data.map(d => ({ ...d, A: fluctuateInt(d.A, 0.05) }))
  , 2000);

  const dynamicFalsePositiveData = useMockStream(falsePositiveData, (data) => {
    const total = 100;
    const falsePos = fluctuateInt(data[1].value, 0.1);
    const newFalse = Math.max(5, Math.min(30, falsePos));
    return [
      { ...data[0], value: total - newFalse },
      { ...data[1], value: newFalse }
    ];
  }, 5000);

  const dynamicMttdMttrData = useMockStream(mttdMttrData, (data) => 
    data.map(d => ({ ...d, mttd: fluctuateInt(d.mttd, 0.05), mttr: fluctuateInt(d.mttr, 0.05) }))
  , 3000);

  return (
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Tier 8 • Security Department"
        title="Postura defensiva contínua"
        subtitle="Superfície de vigilância, gestão de vulnerabilidades e resposta a incidentes pelo Sentinel e equipe."
      />
      <StatGrid
        stats={[
          { label: "Threat Level", value: "Elevated", tone: "warn", icon: <ShieldAlert size={20} /> },
          { label: "Open CVEs", value: "6", tone: "hot", icon: <Bug size={20} /> },
          { label: "MTTR", value: "23m", tone: "good", icon: <Activity size={20} /> },
          { label: "Policy Drift", value: "1.2%", tone: "default", icon: <ShieldCheck size={20} /> },
        ]}
      />
      
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6 mt-6">
        {/* Global Security Score (Gauge) */}
        <Panel title="Global Security Score" subtitle="Avaliação em tempo real (Sentinel)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col items-center justify-center">
            <div className="relative flex items-center justify-center">
              <svg className="w-56 h-28" viewBox="0 0 100 50">
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--border))" strokeWidth="10" strokeLinecap="round" />
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--chart-1))" strokeWidth="10" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="20" className="transition-all duration-1000" />
              </svg>
              <div className="absolute bottom-0 flex flex-col items-center">
                <span className="text-4xl font-bold text-white">84</span>
                <span className="text-xs text-emerald-400 uppercase tracking-wider font-semibold mt-1">Secure</span>
              </div>
            </div>
            <div className="mt-8 text-sm text-muted-foreground text-center px-4">
              O score atual indica uma postura de segurança robusta, com pequenos riscos identificados na camada de API.
            </div>
          </div>
        </Panel>

        {/* Attack Vector Radar */}
        <Panel title="Attack Vector Radar" subtitle="Simulações de quebra (Penetest)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={dynamicAttackVectorData}>
                <PolarGrid stroke="hsl(var(--border))" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Vectors" dataKey="A" stroke="hsl(var(--destructive))" fill="hsl(var(--destructive))" fillOpacity={0.3} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* False Positive Pie */}
        <Panel title="Alert Efficiency" subtitle="Taxa de falsos positivos (Monitoramento)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={dynamicFalsePositiveData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {dynamicFalsePositiveData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute flex flex-col items-center justify-center pointer-events-none">
              <span className="text-3xl font-bold text-white">{dynamicFalsePositiveData[1].value}%</span>
              <span className="text-[10px] text-muted-foreground uppercase tracking-widest mt-1">Noise</span>
            </div>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* Incident Playbook Tracker */}
        <Panel title="Incident Playbook Tracker" subtitle="Resposta ao vivo (IncidentResponder)" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4 flex flex-col justify-center px-8">
            <div className="relative">
              {/* Line connector */}
              <div className="absolute left-4 top-4 bottom-4 w-0.5 bg-white/10 z-0"></div>
              
              <div className="space-y-6 relative z-10">
                {playbookSteps.map((step, i) => (
                  <div key={i} className="flex items-start gap-4">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 shrink-0 ${
                      step.status === 'completed' ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400' :
                      step.status === 'current' ? 'bg-cyber-cyan/20 border-cyber-cyan text-cyber-cyan animate-pulse' :
                      'bg-black border-white/20 text-white/40'
                    }`}>
                      {step.status === 'completed' ? <ShieldCheck size={14} /> : <span className="text-xs font-bold">{step.step}</span>}
                    </div>
                    <div className="flex-1 pt-1.5">
                      <div className="flex justify-between items-center">
                        <span className={`font-medium ${step.status === 'pending' ? 'text-white/40' : 'text-white'}`}>
                          {step.name}
                        </span>
                        <span className="text-xs text-muted-foreground">{step.time}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Panel>

        {/* Security Gate Validations */}
        <Panel title="Deployment Gates" subtitle="Bloqueio/Liberação via Auditor" className="xl:col-span-6">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4 h-[300px] overflow-y-auto pr-2 scrollbar-hide">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80 sticky top-0">
                <tr>
                  <th className="px-4 py-3 font-medium">Service</th>
                  <th className="px-4 py-3 font-medium">Gate</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { service: "auth-gateway", gate: "SAST Scan", status: "Blocked" },
                  { service: "payment-processor", gate: "Dependency Check", status: "Passed" },
                  { service: "user-service", gate: "Secrets Audit", status: "Passed" },
                  { service: "ml-inference-node", gate: "Image Vulnerability", status: "Review" },
                  { service: "frontend-ui", gate: "SAST Scan", status: "Passed" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.service}</td>
                    <td className="px-4 py-3 flex items-center gap-2">
                      {row.status === 'Blocked' ? <Lock size={14} className="text-rose-400" /> : <Unlock size={14} className="text-emerald-400" />}
                      {row.gate}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                        row.status === 'Passed' ? 'bg-emerald-500/10 text-emerald-400' : 
                        row.status === 'Blocked' ? 'bg-rose-500/10 text-rose-400' : 
                        'bg-amber-500/10 text-amber-400'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* Heatmap de Vulnerabilidades (Treemap) */}
        <Panel title="Vulnerability Heatmap" subtitle="SAST results by Severity" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <Treemap
                data={treemapData}
                dataKey="size"
                aspectRatio={4 / 3}
                stroke="hsl(var(--border))"
                fill="hsl(var(--destructive))"
              >
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }} />
              </Treemap>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* MTTD / MTTR Trend */}
        <Panel title="Response Efficiency Trend" subtitle="MTTD vs MTTR" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dynamicMttdMttrData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="mttd" name="MTTD (mins)" stroke="hsl(var(--chart-2))" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="mttr" name="MTTR (mins)" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>

    </main>
  );
}



