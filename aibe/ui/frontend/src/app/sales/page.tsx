"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, PieChart, Pie, Cell } from "recharts";
import { DollarSign, CheckCircle2, AlertTriangle, Activity } from "lucide-react";

const pipelineData = [
  { stage: "Lead", value: 1200000 },
  { stage: "Meeting", value: 850000 },
  { stage: "Proposal", value: 500000 },
  { stage: "Negotiation", value: 300000 },
  { stage: "Closed Won", value: 180000 },
];

const revenueTrend = [
  { month: "Jan", actual: 120, target: 150 },
  { month: "Feb", actual: 140, target: 160 },
  { month: "Mar", actual: 165, target: 170 },
  { month: "Apr", actual: 190, target: 180 },
  { month: "May", actual: 210, target: 190 },
  { month: "Jun", actual: 250, target: 200 },
];

const winLossData = [
  { name: "Won", value: 65 },
  { name: "Lost (Price)", value: 15 },
  { name: "Lost (Competitor)", value: 10 },
  { name: "Lost (Timing)", value: 10 },
];
const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function SalesPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Sales & CS"
        title="Execução comercial com retenção ativa e visibilidade total"
        subtitle="Pipeline, conversas e escalations em um cockpit único para receita previsível."
      />
      <StatGrid
        stats={[
          { label: "Pipeline Value", value: "$1.8M", tone: "good", icon: <DollarSign size={20} /> },
          { label: "Win Rate", value: "39%", icon: <CheckCircle2 size={20} /> },
          { label: "Escalations", value: "5", tone: "warn", icon: <AlertTriangle size={20} /> },
          { label: "NPS Pulse", value: "74", tone: "good", icon: <Activity size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Pipeline Funnel" subtitle="Negócios por etapa (USD)">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineData} layout="vertical" margin={{ top: 10, right: 30, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `$${v/1000}k`} />
                <YAxis dataKey="stage" type="category" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} width={80} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`$${(value/1000).toFixed(0)}k`, 'Value']}
                />
                <Bar dataKey="value" name="Pipeline Value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={32} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Revenue Trend" subtitle="Actual vs Target (in thousands)">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueTrend} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="month" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="actual" name="Actual Revenue" stroke="#10b981" fillOpacity={1} fill="url(#colorActual)" />
                <Area type="monotone" dataKey="target" name="Target" stroke="#a1a1aa" strokeDasharray="5 5" fill="none" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Win/Loss Analysis" subtitle="Distribuição de motivos de perda">
          <div className="h-[250px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={winLossData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {winLossData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`${value}%`, 'Share']}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Escalation Queue" subtitle="Fila de casos sensíveis de clientes">
          <div className="space-y-3 mt-4">
            {[
              { client: "Acme Corp", issue: "Contract Renewal Delay", status: "Critical", agent: "Negotiator-1" },
              { client: "Globex", issue: "Technical Integration", status: "High", agent: "Tech-Support-2" },
              { client: "Initech", issue: "Feature Request Blocked", status: "Medium", agent: "CS-Lead" },
            ].map((escalation, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl border border-white/5 bg-black/20">
                <div>
                  <p className="text-sm font-medium text-white">{escalation.client}</p>
                  <p className="text-xs text-muted-foreground">{escalation.issue}</p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${escalation.status === 'Critical' ? 'bg-rose-500/10 text-rose-400' : escalation.status === 'High' ? 'bg-amber-500/10 text-amber-400' : 'bg-blue-500/10 text-blue-400'}`}>
                    {escalation.status}
                  </span>
                  <p className="text-[10px] text-muted-foreground mt-1">{escalation.agent}</p>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>
    </main>
  );
}



