"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { Share2, Users, MessageSquare, TrendingUp } from "lucide-react";
import { useState } from "react";

const engagementData = [
  { day: "Mon", likes: 4000, shares: 2400, comments: 2400 },
  { day: "Tue", likes: 3000, shares: 1398, comments: 2210 },
  { day: "Wed", likes: 2000, shares: 9800, comments: 2290 },
  { day: "Thu", likes: 2780, shares: 3908, comments: 2000 },
  { day: "Fri", likes: 1890, shares: 4800, comments: 2181 },
  { day: "Sat", likes: 2390, shares: 3800, comments: 2500 },
  { day: "Sun", likes: 3490, shares: 4300, comments: 2100 },
];

export default function SocialPage() {
  const [kanban, setKanban] = useState([
    { id: 1, title: "Blog: Organic Traffic SEO", status: "To Do", assignee: "Marketing", type: "Blog" },
    { id: 2, title: "TikTok: Viral Challenge", status: "In Progress", assignee: "Social Team", type: "Video" },
    { id: 3, title: "Newsletter: Monthly Update", status: "Done", assignee: "Marketing", type: "Email" },
    { id: 4, title: "LinkedIn: Feature Launch", status: "In Progress", assignee: "Social Team", type: "Post" },
  ]);

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Social Studio & Marketing Ally"
        title="Controle social-first com preview e inteligência de tendência"
        subtitle="Gestão integrada de posts, conversas e sinais culturais com visão de impacto em tempo real."
      />
      <StatGrid
        stats={[
          { label: "Posts Scheduled", value: "46", tone: "default", icon: <Share2 size={20} /> },
          { label: "Engagement Rate", value: "8.9%", tone: "good", icon: <TrendingUp size={20} /> },
          { label: "Trend Velocity", value: "High", tone: "warn", icon: <Users size={20} /> },
          { label: "Community SLA", value: "12m", tone: "good", icon: <MessageSquare size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Engagement Evolution" subtitle="Likes, Shares e Comments por dia">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={engagementData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorLikes" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ec4899" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ec4899" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorShares" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
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
                <Area type="monotone" dataKey="likes" stroke="#ec4899" fillOpacity={1} fill="url(#colorLikes)" />
                <Area type="monotone" dataKey="shares" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorShares)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Audience Demographics" subtitle="Distribuição por plataforma e faixa etária">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={engagementData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="day" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="likes" name="Instagram" stackId="a" fill="#ec4899" radius={[0, 0, 4, 4]} />
                <Bar dataKey="shares" name="TikTok" stackId="a" fill="#8b5cf6" />
                <Bar dataKey="comments" name="LinkedIn" stackId="a" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Content Kanban (Marketing & Social)" subtitle="Sincronizado em tempo real com time de Marketing" className="xl:col-span-2">
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
                        <span className={`text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded ${item.assignee === 'Marketing' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-cyber-purple/20 text-cyber-purple'}`}>
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



