"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { TrendingUp, Users, Target, Activity, MessageSquare } from "lucide-react";
import { useState } from "react";

const campaignData = [
  { name: "Search Ads", spend: 4000, conversion: 2400 },
  { name: "Social Media", spend: 3000, conversion: 1398 },
  { name: "Email Marketing", spend: 2000, conversion: 9800 },
  { name: "Content SEO", spend: 2780, conversion: 3908 },
  { name: "Influencers", spend: 1890, conversion: 4800 },
];

const trafficData = [
  { day: "Mon", organic: 120, paid: 80 },
  { day: "Tue", organic: 135, paid: 90 },
  { day: "Wed", organic: 150, paid: 110 },
  { day: "Thu", organic: 180, paid: 130 },
  { day: "Fri", organic: 210, paid: 150 },
  { day: "Sat", organic: 190, paid: 140 },
  { day: "Sun", organic: 160, paid: 120 },
];

export default function MarketingPage() {
  const [kanban, setKanban] = useState([
    { id: 1, title: "Blog: Organic Traffic SEO", status: "To Do", assignee: "Marketing", type: "Blog" },
    { id: 2, title: "TikTok: Viral Challenge", status: "In Progress", assignee: "Social Team", type: "Video" },
    { id: 3, title: "Newsletter: Monthly Update", status: "Done", assignee: "Marketing", type: "Email" },
    { id: 4, title: "LinkedIn: Feature Launch", status: "In Progress", assignee: "Social Team", type: "Post" },
  ]);

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Marketing Command"
        title="Motor de crescimento com execução omnicanal orientada a ROI"
        subtitle="Campanhas, calendário editorial e SEO analytics com tomada de decisão instantânea."
      />
      <StatGrid
        stats={[
          { label: "Active Campaigns", value: "18", tone: "good", icon: <Activity size={20} /> },
          { label: "CTR Avg", value: "6.4%", tone: "good", icon: <Target size={20} /> },
          { label: "CAC Trend", value: "-9.1%", tone: "good", icon: <TrendingUp size={20} /> },
          { label: "Organic Lift", value: "+22%", tone: "default", icon: <Users size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Campaign Matrix" subtitle="Distribuição por canal, custo e performance">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={campaignData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="name" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="spend" name="Spend ($)" fill="#7c3aed" radius={[4, 4, 0, 0]} />
                <Bar dataKey="conversion" name="Conversions" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Traffic Evolution" subtitle="Crescimento de tráfego orgânico vs pago">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trafficData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorOrganic" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPaid" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="day" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="organic" name="Organic" stroke="#10b981" fillOpacity={1} fill="url(#colorOrganic)" />
                <Area type="monotone" dataKey="paid" name="Paid" stroke="#f59e0b" fillOpacity={1} fill="url(#colorPaid)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="SEO Dashboard" subtitle="Evolução de rankings, tráfego e intenção" className="xl:col-span-1">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">Keyword</th>
                  <th className="px-4 py-3 font-medium">Position</th>
                  <th className="px-4 py-3 font-medium">Vol</th>
                  <th className="px-4 py-3 font-medium">Trend</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { keyword: "ai agents orchestration", pos: 1, vol: "12.5K", intent: "Transactional", trend: "+2" },
                  { keyword: "autonomous team software", pos: 3, vol: "8.2K", intent: "Informational", trend: "+1" },
                  { keyword: "llm routing table", pos: 2, vol: "5.1K", intent: "Transactional", trend: "0" },
                  { keyword: "automated budget limits ai", pos: 5, vol: "3.4K", intent: "Commercial", trend: "+4" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.keyword}</td>
                    <td className="px-4 py-3 text-cyber-cyan">#{row.pos}</td>
                    <td className="px-4 py-3">{row.vol}</td>
                    <td className="px-4 py-3 text-emerald-400">{row.trend}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>

        <Panel title="Content Kanban (Marketing & Social)" subtitle="Sincronizado em tempo real com time de Social" className="xl:col-span-2">
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            {["To Do", "In Progress", "Done"].map(status => (
              <div key={status} className="rounded-xl border border-white/5 bg-black/20 p-4">
                <h3 className="text-sm font-semibold text-white/80 mb-3 flex items-center justify-between">
                  {status}
                  <span className="bg-white/10 text-white/60 text-xs px-2 py-0.5 rounded-full">
                    {kanban.filter(k => k.status === status).length}
                  </span>
                </h3>
                <div className="space-y-3">
                  {kanban.filter(k => k.status === status).map(item => (
                    <div key={item.id} className="rounded-lg border border-white/5 bg-white/5 p-3 hover:border-white/10 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <span className={`text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded ${item.assignee === 'Social Team' ? 'bg-cyber-purple/20 text-cyber-purple' : 'bg-emerald-500/20 text-emerald-400'}`}>
                          {item.assignee}
                        </span>
                        <span className="text-xs text-muted-foreground">{item.type}</span>
                      </div>
                      <p className="text-sm text-white font-medium">{item.title}</p>
                      <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
                        <span className="flex items-center gap-1"><MessageSquare size={12} /> Sync</span>
                        {status !== 'Done' && (
                          <button 
                            onClick={() => {
                              const nextStatus = status === 'To Do' ? 'In Progress' : 'Done';
                              setKanban(kanban.map(k => k.id === item.id ? { ...k, status: nextStatus } : k));
                            }}
                            className="hover:text-white transition-colors"
                          >
                            Move →
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>
    </main>
  );
}



