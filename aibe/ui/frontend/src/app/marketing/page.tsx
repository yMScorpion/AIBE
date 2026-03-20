"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { useMockStream, fluctuateInt } from "@/lib/mock-stream";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, PieChart, Pie, Cell, ScatterChart, Scatter, ZAxis, ReferenceLine, LineChart, Line } from "recharts";
import { Target, TrendingUp, Activity, FileText, SplitSquareHorizontal, MessageSquare } from "lucide-react";
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

const funnelData = [
  { stage: "Impressions", count: 125000, fill: "hsl(var(--primary))" },
  { stage: "Clicks", count: 18400, fill: "hsl(var(--accent))" },
  { stage: "Leads", count: 3200, fill: "hsl(var(--chart-1))" },
  { stage: "Conversions", count: 840, fill: "hsl(var(--chart-2))" },
];

const roasData = [
  { platform: "Meta Ads", spend: 5000, return: 15000, z: 200, fill: "hsl(var(--primary))" },
  { platform: "Google Search", spend: 8000, return: 28000, z: 250, fill: "hsl(var(--destructive))" },
  { platform: "LinkedIn Ads", spend: 3000, return: 6000, z: 100, fill: "hsl(var(--chart-4))" },
  { platform: "TikTok Ads", spend: 2000, return: 8000, z: 150, fill: "hsl(var(--chart-3))" },
  { platform: "Twitter Ads", spend: 1500, return: 2000, z: 80, fill: "hsl(var(--chart-5))" },
];

const budgetData = [
  { name: "Google", value: 45 },
  { name: "Meta", value: 25 },
  { name: "LinkedIn", value: 15 },
  { name: "TikTok", value: 10 },
  { name: "Other", value: 5 },
];
const budgetCOLORS = ['hsl(var(--destructive))', 'hsl(var(--primary))', 'hsl(var(--chart-4))', 'hsl(var(--chart-3))', 'hsl(var(--muted-foreground))'];

const abTestData = [
  { variant: "A (Control)", conversions: 4.2, bounce: 45 },
  { variant: "B (AI Copy)", conversions: 6.8, bounce: 32 },
];

const cacData = [
  { month: 'Jan', cac: 125 },
  { month: 'Feb', cac: 118 },
  { month: 'Mar', cac: 105 },
  { month: 'Apr', cac: 98 },
  { month: 'May', cac: 92 },
  { month: 'Jun', cac: 85 },
];

const campaignTimeline = [
  { id: 1, name: "Summer Sale", start: 10, duration: 20, fill: "hsl(var(--primary))" },
  { id: 2, name: "B2B Outreach", start: 0, duration: 15, fill: "hsl(var(--chart-1))" },
  { id: 3, name: "Brand Awareness", start: 15, duration: 30, fill: "hsl(var(--chart-2))" },
  { id: 4, name: "Retargeting", start: 5, duration: 25, fill: "hsl(var(--chart-3))" },
];

export default function MarketingPage() {
  const dynamicFunnelData = useMockStream(funnelData, (data) => 
    data.map(d => ({ ...d, count: fluctuateInt(d.count, 0.03) }))
  , 3000);

  const dynamicRoasData = useMockStream(roasData, (data) => 
    data.map(d => ({ ...d, return: fluctuateInt(d.return, 0.05), spend: fluctuateInt(d.spend, 0.01) }))
  , 4000);

  const dynamicTrafficData = useMockStream(trafficData, (data) => 
    data.map(d => ({ ...d, organic: fluctuateInt(d.organic, 0.04), paid: fluctuateInt(d.paid, 0.06) }))
  , 2000);

  const dynamicCacData = useMockStream(cacData, (data) => 
    data.map(d => ({ ...d, cac: fluctuateInt(d.cac, 0.02) }))
  , 4000);

  const [kanban, setKanban] = useState([
    { id: 1, title: "Blog: Organic Traffic SEO", status: "To Do", assignee: "Marketing", type: "Blog" },
    { id: 2, title: "TikTok: Viral Challenge", status: "In Progress", assignee: "Social Team", type: "Video" },
    { id: 3, title: "Newsletter: Monthly Update", status: "Done", assignee: "Marketing", type: "Email" },
    { id: 4, title: "LinkedIn: Feature Launch", status: "In Progress", assignee: "Social Team", type: "Post" },
  ]);

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Tier 3 • Marketing Department"
        title="Growth & Acquisition"
        subtitle="Campaigns, editorial calendar, and SEO analytics managed by Helix, Quill, Lumen, Volt, and Prism."
      />
      <StatGrid
        stats={[
          { label: "Active Campaigns", value: "18", tone: "good", icon: <Activity size={20} /> },
          { label: "Copy Velocity", value: "12k words", trend: "per day", tone: "good", icon: <FileText size={20} /> },
          { label: "CAC Trend", value: "-9.1%", tone: "good", icon: <TrendingUp size={20} /> },
          { label: "Global SEO Score", value: "92/100", tone: "good", icon: <Target size={20} /> },
        ]}
      />
      
      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Conversion Funnel */}
        <Panel title="Prism Conversion Funnel" subtitle="Impressions to Conversions" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dynamicFunnelData} layout="vertical" margin={{ top: 10, right: 30, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="stage" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {dynamicFunnelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* ROAS Matrix */}
        <Panel title="Volt ROAS Matrix" subtitle="Ad Spend vs Return by Platform" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" dataKey="spend" name="Spend ($)" stroke="hsl(var(--muted-foreground))" fontSize={10} tickFormatter={(val) => `$${val/1000}k`} />
                <YAxis type="number" dataKey="return" name="Return ($)" stroke="hsl(var(--muted-foreground))" fontSize={10} tickFormatter={(val) => `$${val/1000}k`} />
                <ZAxis type="number" dataKey="z" range={[50, 400]} name="Volume" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any) => [value, name === 'z' ? 'Volume' : name]}
                />
                <ReferenceLine x={4000} stroke="hsl(var(--muted-foreground))" strokeOpacity={0.5} />
                <ReferenceLine y={10000} stroke="hsl(var(--muted-foreground))" strokeOpacity={0.5} />
                <Scatter name="Platforms" data={dynamicRoasData}>
                  {dynamicRoasData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* A/B Test Split View */}
        <Panel title="A/B Test Results" subtitle="Landing Page Conversion Optimization" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col justify-center gap-6">
            {abTestData.map((variant, i) => (
              <div key={i} className="flex flex-col gap-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-white font-medium">{variant.variant}</span>
                  <span className={i === 1 ? "text-emerald-400 font-bold" : "text-muted-foreground"}>{variant.conversions}% Conv.</span>
                </div>
                <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${i === 1 ? 'bg-emerald-500' : 'bg-52525b'}`}
                    style={{ width: `${variant.conversions * 10}%`, backgroundColor: i === 1 ? 'hsl(var(--chart-1))' : 'hsl(var(--muted-foreground))' }}
                  />
                </div>
                <p className="text-xs text-muted-foreground text-right">Bounce Rate: {variant.bounce}%</p>
              </div>
            ))}
            <div className="mt-4 p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-lg flex items-start gap-3">
              <SplitSquareHorizontal className="text-emerald-400 mt-0.5" size={16} />
              <p className="text-xs text-emerald-400/90 leading-relaxed">
                Variant B (AI Copy) shows a <strong className="text-emerald-400">61% relative increase</strong> in conversion rate. Deploy agent is preparing rollout.
              </p>
            </div>
          </div>
        </Panel>

        {/* Ad Budget Distribution */}
        <Panel title="Ad Budget Distribution" subtitle="Allocation by Platform" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={budgetData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {budgetData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={budgetCOLORS[index % budgetCOLORS.length]} />
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

        {/* Lumen Asset Engagement Heatmap */}
        <Panel title="Asset Engagement Heatmap" subtitle="CTR by Visual Style (Lumen)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col justify-center">
            <div className="grid grid-cols-4 gap-2">
              <div className="col-span-1"></div>
              {['Tech', 'Playful', 'Minimal'].map(d => <div key={d} className="text-center text-xs text-muted-foreground">{d}</div>)}
              
              {['Images', 'Videos', 'Carousels', 'Gifs'].map((format, i) => (
                <div key={format} className="contents">
                  <div className="text-xs text-muted-foreground flex items-center justify-end pr-2">{format}</div>
                  {Array.from({length: 3}).map((_, j) => {
                    const intensity = Math.random();
                    return (
                      <div 
                        key={`${i}-${j}`} 
                        className="h-10 rounded-md transition-all hover:scale-105 hover:ring-1 hover:ring-white/20 cursor-pointer"
                        style={{ backgroundColor: `rgba(16, 185, 129, ${intensity * 0.8 + 0.2})` }}
                        title={`${format} + ${['Tech', 'Playful', 'Minimal'][j]}: ${(intensity * 8 + 1).toFixed(1)}% CTR`}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
            <div className="mt-6 flex items-center justify-center gap-4 text-xs text-muted-foreground">
              <span>Low CTR</span>
              <div className="w-24 h-2 bg-gradient-to-r from-emerald-900 to-emerald-400 rounded-full"></div>
              <span>High CTR</span>
            </div>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Campaign Matrix" subtitle="Distribuição por canal, custo e performance">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={campaignData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="spend" name="Spend ($)" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                <Bar dataKey="conversion" name="Conversions" fill="hsl(var(--accent))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Traffic Evolution" subtitle="Crescimento de tráfego orgânico vs pago">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dynamicTrafficData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorOrganic" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPaid" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--chart-2))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--chart-2))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="organic" name="Organic" stroke="hsl(var(--chart-1))" fillOpacity={1} fill="url(#colorOrganic)" />
                <Area type="monotone" dataKey="paid" name="Paid" stroke="hsl(var(--chart-2))" fillOpacity={1} fill="url(#colorPaid)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        <Panel title="Content Kanban (Marketing & Social)" subtitle="Sincronizado em tempo real com time de Social" className="xl:col-span-12">
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
                        <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-1 rounded ${item.assignee === 'Social Team' ? 'bg-cyber-purple/20 text-cyber-purple' : 'bg-emerald-500/20 text-emerald-400'}`}>
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

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
        {/* CAC Trend */}
        <Panel title="CAC Trend" subtitle="Customer Acquisition Cost (Volt)">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dynamicCacData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `$${v}`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Line type="monotone" dataKey="cac" name="CAC ($)" stroke="hsl(var(--chart-1))" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Campaign Timeline (Gantt) */}
        <Panel title="Campaign Timeline" subtitle="Helix Orchestration">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={campaignTimeline} layout="vertical" margin={{ top: 10, right: 0, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="name" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Bar dataKey="start" stackId="a" fill="transparent" />
                <Bar dataKey="duration" stackId="a" radius={[0, 4, 4, 0]}>
                  {campaignTimeline.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>
    </main>
  );
}



