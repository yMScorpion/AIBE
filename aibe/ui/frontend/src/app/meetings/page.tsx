"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Users, Activity, CheckCircle2, MessageSquare } from "lucide-react";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, PieChart, Pie, Cell } from "recharts";

const meetingActivityData = [
  { time: "08:00", participants: 4, messages: 120 },
  { time: "09:00", participants: 6, messages: 250 },
  { time: "10:00", participants: 8, messages: 410 },
  { time: "11:00", participants: 12, messages: 550 },
  { time: "12:00", participants: 5, messages: 180 },
  { time: "13:00", participants: 7, messages: 320 },
  { time: "14:00", participants: 10, messages: 480 },
];

const consensusData = [
  { name: "Strong Agreement", value: 65 },
  { name: "Conditional", value: 25 },
  { name: "Disagreement", value: 10 },
];
const COLORS = ['hsl(var(--chart-1))', 'hsl(var(--chart-2))', 'hsl(var(--destructive))'];

export default function MeetingsPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="War Room"
        title="Coordenação de debates e decisões de alto impacto"
        subtitle="Sala de comando com visão ao vivo de reuniões críticas, divergências e deliberações finais."
      />
      <StatGrid
        stats={[
          { label: "Live Meetings", value: "4", tone: "good", icon: <Users size={20} /> },
          { label: "Debates", value: "11", tone: "hot", icon: <Activity size={20} /> },
          { label: "Decisions Today", value: "27", icon: <CheckCircle2 size={20} /> },
          { label: "Consensus Score", value: "91%", tone: "good", icon: <MessageSquare size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Meeting Activity" subtitle="Volume de mensagens vs Participantes">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={meetingActivityData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorMessages" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="time" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="hsl(var(--accent))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area yAxisId="left" type="monotone" dataKey="messages" name="Messages" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorMessages)" />
                <Area yAxisId="right" type="step" dataKey="participants" name="Participants" stroke="hsl(var(--accent))" fill="none" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Consensus Breakdown" subtitle="Qualidade do alinhamento entre agentes">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={consensusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {consensusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
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

        <Panel title="Live Debate Board" subtitle="Transmissão estruturada das sessões em andamento" className="xl:col-span-2">
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-xl border border-white/5 bg-black/20 p-5">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="text-sm font-semibold text-white">Growth Budget Rebalance</h4>
                  <p className="text-xs text-muted-foreground mt-1">Status: Votação Ativa</p>
                </div>
                <span className="px-2 py-1 rounded bg-amber-500/20 text-amber-400 text-[10px] font-bold tracking-wider uppercase">Hot Debate</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold">+</div>
                  <p className="text-sm text-white/90 leading-snug">Aumentar investimento em aquisição acelera pipeline de vendas B2B no curto prazo. <span className="text-xs text-muted-foreground block mt-1">— Marketing-Lead</span></p>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center text-xs font-bold">−</div>
                  <p className="text-sm text-white/90 leading-snug">Risco de saturação e aumento do CAC além da margem aceitável. <span className="text-xs text-muted-foreground block mt-1">— Finance-Oracle</span></p>
                </li>
              </ul>
            </div>

            <div className="rounded-xl border border-white/5 bg-black/20 p-5">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="text-sm font-semibold text-white">Feature Rollout Q3</h4>
                  <p className="text-xs text-muted-foreground mt-1">Status: Consenso Atingido</p>
                </div>
                <span className="px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-bold tracking-wider uppercase">Approved</span>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold">+</div>
                  <p className="text-sm text-white/90 leading-snug">Priorizar integrações de terceiros desbloqueia clientes enterprise. <span className="text-xs text-muted-foreground block mt-1">— Product-Lead</span></p>
                </li>
                <li className="flex items-start gap-3">
                  <div className="h-6 w-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold">+</div>
                  <p className="text-sm text-white/90 leading-snug">Engenharia confirma viabilidade técnica com recursos atuais. <span className="text-xs text-muted-foreground block mt-1">— Tech-Lead</span></p>
                </li>
              </ul>
            </div>
          </div>
        </Panel>
      </section>
    </main>
  );
}



