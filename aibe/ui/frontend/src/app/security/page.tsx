"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { ResponsiveContainer, Tooltip, Cell, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, PieChart, Pie } from "recharts";
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
  { name: 'True Positives', value: 85, fill: '#ef4444' },
  { name: 'False Positives', value: 15, fill: '#3b82f6' },
];

const playbookSteps = [
  { step: 1, name: "Detect", status: "completed", time: "10:02 AM" },
  { step: 2, name: "Contain", status: "current", time: "In Progress" },
  { step: 3, name: "Eradicate", status: "pending", time: "--" },
  { step: 4, name: "Recover", status: "pending", time: "--" },
  { step: 5, name: "Post-Mortem", status: "pending", time: "--" },
];

export default function SecurityPage() {
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
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#27272a" strokeWidth="10" strokeLinecap="round" />
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#10b981" strokeWidth="10" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="20" className="transition-all duration-1000" />
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
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={attackVectorData}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Vectors" dataKey="A" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
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
                  data={falsePositiveData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {falsePositiveData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute flex flex-col items-center justify-center pointer-events-none">
              <span className="text-3xl font-bold text-white">15%</span>
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

    </main>
  );
}



