"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, LineChart, Line, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { Users, MessageSquare, AlertTriangle, Eye, Flame } from "lucide-react";
import { useState } from "react";

const viralityData = [
  { time: "00:00", velocity: 12 },
  { time: "04:00", velocity: 15 },
  { time: "08:00", velocity: 45 },
  { time: "12:00", velocity: 120 },
  { time: "16:00", velocity: 180 },
  { time: "20:00", velocity: 95 },
  { time: "24:00", velocity: 40 },
];

const sentimentData = [
  { day: "Mon", positive: 65, neutral: 25, negative: 10 },
  { day: "Tue", positive: 70, neutral: 20, negative: 10 },
  { day: "Wed", positive: 60, neutral: 30, negative: 10 },
  { day: "Thu", positive: 80, neutral: 15, negative: 5 },
  { day: "Fri", positive: 85, neutral: 10, negative: 5 },
  { day: "Sat", positive: 90, neutral: 5, negative: 5 },
  { day: "Sun", positive: 88, neutral: 8, negative: 4 },
];

const platformRadarData = [
  { subject: 'Reddit', A: 120, fullMark: 150 },
  { subject: 'HackerNews', A: 98, fullMark: 150 },
  { subject: 'Twitter/X', A: 140, fullMark: 150 },
  { subject: 'LinkedIn', A: 85, fullMark: 150 },
  { subject: 'Instagram', A: 60, fullMark: 150 },
  { subject: 'TikTok', A: 110, fullMark: 150 },
];

const forumThreadsData = [
  { forum: "r/SaaS", threads: 12, replies: 145 },
  { forum: "r/Startups", threads: 8, replies: 89 },
  { forum: "HackerNews", threads: 3, replies: 210 },
  { forum: "IndieHackers", threads: 5, replies: 67 },
];

const topPosts = [
  { platform: "Twitter", content: "How we scaled our AI agents to 10k tasks/day 🧵...", engagement: "12.4k", score: 98 },
  { platform: "LinkedIn", content: "The future of autonomous enterprise operations is here.", engagement: "8.2k", score: 92 },
  { platform: "TikTok", content: "Day in the life of an AI Agent #tech", engagement: "45.1k", score: 88 },
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
        eyebrow="Tier 4 • Social Media Department"
        title="Community & Virality"
        subtitle="Brand presence, crisis management, and trend analysis by Nova, Spark, Bloom, Grove, and Echo."
      />
      <StatGrid
        stats={[
          { label: "Organic Reach", value: "2.4M", trend: "impressions", tone: "good", icon: <Eye size={20} /> },
          { label: "Trend Velocity", value: "High", tone: "warn", icon: <Flame size={20} /> },
          { label: "Crisis Escalation", value: "1.2%", tone: "good", icon: <AlertTriangle size={20} /> },
          { label: "Community SLA", value: "12m", tone: "good", icon: <MessageSquare size={20} /> },
        ]}
      />
      
      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Virality Monitor */}
        <Panel title="Echo Virality Monitor" subtitle="Momentum of current top trend (Engagements/hour)" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={viralityData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="time" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="velocity" name="Engagements/hr" stroke="#ec4899" strokeWidth={3} dot={{ fill: '#ec4899', strokeWidth: 2, r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Platform Engagement Radar */}
        <Panel title="Grove Platform Radar" subtitle="Where the community is most active" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="75%" data={platformRadarData}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Engagement Activity" dataKey="A" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.4} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Community Sentiment */}
        <Panel title="Bloom Community Sentiment" subtitle="Brand perception over time" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={sentimentData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorNeu" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#52525b" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#52525b" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="day" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="positive" name="Positive" stackId="1" stroke="#10b981" fillOpacity={1} fill="url(#colorPos)" />
                <Area type="monotone" dataKey="neutral" name="Neutral" stackId="1" stroke="#52525b" fillOpacity={1} fill="url(#colorNeu)" />
                <Area type="monotone" dataKey="negative" name="Negative" stackId="1" stroke="#ef4444" fillOpacity={1} fill="url(#colorNeg)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Mentions Queue */}
        <Panel title="Mentions & Crisis Queue" subtitle="Backlog awaiting Bloom's response" className="xl:col-span-6">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">User/Source</th>
                  <th className="px-4 py-3 font-medium">Sentiment</th>
                  <th className="px-4 py-3 font-medium">Priority</th>
                  <th className="px-4 py-3 font-medium">SLA</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { source: "@techreviewer (Twitter)", sentiment: "Negative", priority: "Critical", sla: "2m left" },
                  { source: "HackerNews Frontpage", sentiment: "Neutral", priority: "High", sla: "15m left" },
                  { source: "r/SaaS (Reddit)", sentiment: "Positive", priority: "Medium", sla: "1h left" },
                  { source: "LinkedIn Post Reply", sentiment: "Positive", priority: "Low", sla: "4h left" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.source}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                        row.sentiment === 'Negative' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                        row.sentiment === 'Positive' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                        'bg-white/5 text-muted-foreground border border-white/10'
                      }`}>
                        {row.sentiment}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`flex items-center gap-1.5 ${row.priority === 'Critical' ? 'text-rose-400' : row.priority === 'High' ? 'text-amber-400' : 'text-muted-foreground'}`}>
                        {row.priority}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs">{row.sla}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Forum Threads */}
        <Panel title="Forum Threads Activity" subtitle="Volume of initiated/maintained discussions" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={forumThreadsData} layout="vertical" margin={{ top: 10, right: 10, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="forum" type="category" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="threads" name="Active Threads" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                <Bar dataKey="replies" name="Replies Generated" fill="#0ea5e9" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Ideal Post Time Heatmap */}
        <Panel title="Ideal Post Time Predictor" subtitle="Echo's reach maximization matrix" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col justify-center">
            <div className="grid grid-cols-5 gap-1">
              <div className="col-span-1"></div>
              {['9AM', '12PM', '3PM', '6PM'].map(d => <div key={d} className="text-center text-[10px] text-muted-foreground">{d}</div>)}
              
              {['Mon', 'Wed', 'Fri', 'Sat'].map((day, i) => (
                <div key={day} className="contents">
                  <div className="text-[10px] text-muted-foreground flex items-center justify-end pr-2">{day}</div>
                  {Array.from({length: 4}).map((_, j) => {
                    const intensity = Math.random();
                    return (
                      <div 
                        key={`${i}-${j}`} 
                        className="h-10 rounded transition-all hover:scale-110 cursor-pointer border border-white/5"
                        style={{ backgroundColor: `rgba(236, 72, 153, ${intensity * 0.8 + 0.1})` }}
                        title={`${day} at ${['9AM', '12PM', '3PM', '6PM'][j]}: ${(intensity * 100).toFixed(0)}% reach potential`}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
            <div className="mt-6 flex items-center justify-center gap-4 text-xs text-muted-foreground">
              <span>Low</span>
              <div className="w-24 h-1.5 bg-gradient-to-r from-pink-950 to-pink-500 rounded-full"></div>
              <span>High</span>
            </div>
          </div>
        </Panel>

        {/* Top Posts Board */}
        <Panel title="Top Posts Board" subtitle="Most successful content of the week" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col gap-3 overflow-y-auto pr-2 scrollbar-hide">
            {topPosts.map((post, i) => (
              <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 transition-colors">
                <div className="flex justify-between items-center mb-2">
                  <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-md ${
                    post.platform === 'Twitter' ? 'bg-sky-500/20 text-sky-400' :
                    post.platform === 'LinkedIn' ? 'bg-blue-600/20 text-blue-400' :
                    'bg-pink-500/20 text-pink-400'
                  }`}>
                    {post.platform}
                  </span>
                  <div className="flex items-center gap-1 text-emerald-400 text-xs font-bold">
                    <Flame size={12} />
                    {post.score} Score
                  </div>
                </div>
                <p className="text-sm text-white/90 line-clamp-2 leading-relaxed">&quot;{post.content}&quot;</p>
                <div className="mt-3 flex items-center gap-4 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1.5"><Users size={14} /> {post.engagement}</span>
                  <span className="text-cyber-cyan cursor-pointer hover:underline">View Post ↗</span>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        <Panel title="Content Kanban (Marketing & Social)" subtitle="Sincronizado em tempo real com time de Marketing" className="xl:col-span-12">
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-6">
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
                    <div key={item.id} className="rounded-lg border border-white/5 bg-white/5 p-4 hover:border-white/10 transition-colors">
                      <div className="flex justify-between items-start mb-2">
                        <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded ${item.assignee === 'Marketing' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-cyber-purple/20 text-cyber-purple'}`}>
                          {item.assignee}
                        </span>
                        <span className="text-xs font-medium text-muted-foreground bg-white/5 px-2 py-1 rounded-md">{item.type}</span>
                      </div>
                      <p className="text-sm text-white font-medium mt-3 mb-4">{item.title}</p>
                      <div className="flex items-center justify-between text-xs text-muted-foreground pt-3 border-t border-white/5">
                        <span className="flex items-center gap-1.5"><MessageSquare size={14} /> Sync Active</span>
                        {status !== 'Done' && (
                          <button 
                            onClick={() => {
                              const nextStatus = status === 'To Do' ? 'In Progress' : 'Done';
                              setKanban(kanban.map(k => k.id === item.id ? { ...k, status: nextStatus } : k));
                            }}
                            className="hover:text-white transition-colors bg-white/5 px-3 py-1.5 rounded-md hover:bg-white/10"
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



