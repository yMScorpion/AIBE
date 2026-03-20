"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { 
  Lightbulb, 
  CheckCircle, 
  AlertTriangle,
  Globe
} from "lucide-react";
import { 
  Area, AreaChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ScatterChart, Scatter, ZAxis, ReferenceLine,
  LineChart, Line
} from "recharts";

const throughputData = [
  { day: "Mon", ideas: 12, debates: 8, approved: 2 },
  { day: "Tue", ideas: 15, debates: 10, approved: 3 },
  { day: "Wed", ideas: 22, debates: 18, approved: 5 },
  { day: "Thu", ideas: 18, debates: 14, approved: 4 },
  { day: "Fri", ideas: 25, debates: 20, approved: 7 },
  { day: "Sat", ideas: 10, debates: 5, approved: 1 },
  { day: "Sun", ideas: 8, debates: 4, approved: 1 },
];



const sentimentData = [
  { subject: 'Innovation', A: 120, B: 110, fullMark: 150 },
  { subject: 'Feasibility', A: 98, B: 130, fullMark: 150 },
  { subject: 'Market Size', A: 86, B: 130, fullMark: 150 },
  { subject: 'Cost', A: 99, B: 100, fullMark: 150 },
  { subject: 'Risk', A: 85, B: 90, fullMark: 150 },
  { subject: 'Impact', A: 65, B: 85, fullMark: 150 },
];

const scatterIdeasData = [
  { name: "AI CRM", feasibility: 80, sentiment: 90, z: 200, fill: "#10b981" },
  { name: "Web3 Identity", feasibility: 40, sentiment: 60, z: 150, fill: "#f59e0b" },
  { name: "DevOps Tool", feasibility: 90, sentiment: 75, z: 250, fill: "#06b6d4" },
  { name: "VR Meeting", feasibility: 30, sentiment: 40, z: 100, fill: "#ef4444" },
  { name: "NoCode App", feasibility: 70, sentiment: 85, z: 180, fill: "#7c3aed" },
];

const scrapingVolumeData = [
  { hour: "00:00", volume: 1200 },
  { hour: "04:00", volume: 800 },
  { hour: "08:00", volume: 3500 },
  { hour: "12:00", volume: 5000 },
  { hour: "16:00", volume: 4800 },
  { hour: "20:00", volume: 2200 },
];



const wordCloudTags = [
  { text: "AI Agents", size: "text-2xl", color: "text-cyber-cyan", weight: "font-bold" },
  { text: "Serverless", size: "text-lg", color: "text-white/80", weight: "font-medium" },
  { text: "RAG", size: "text-xl", color: "text-cyber-purple", weight: "font-semibold" },
  { text: "Micro-SaaS", size: "text-sm", color: "text-white/60", weight: "font-normal" },
  { text: "Automation", size: "text-3xl", color: "text-emerald-400", weight: "font-black" },
  { text: "Fintech", size: "text-base", color: "text-rose-400", weight: "font-medium" },
  { text: "Observability", size: "text-xl", color: "text-white/90", weight: "font-bold" },
  { text: "LLMOps", size: "text-lg", color: "text-amber-400", weight: "font-semibold" },
  { text: "B2B", size: "text-sm", color: "text-white/50", weight: "font-normal" },
];

export default function ResearchPage() {
  return (
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Tier 1 • Research Department"
        title="Innovation & Intelligence"
        subtitle="Market analysis, idea generation, and validation by Scout, Vega, and Pulse."
      />

      <StatGrid
        stats={[
          { label: "Total Ideas Generated", value: "342", trend: "12% up", trendUp: true, icon: <Lightbulb size={20} /> },
          { label: "Idea Survival Rate", value: "18.5%", trend: "Vega approved", trendUp: true, icon: <CheckCircle size={20} />, tone: "good" },
          { label: "Market Saturation", value: "High", trend: "Pulse Alert", trendUp: false, icon: <AlertTriangle size={20} />, tone: "hot" },
          { label: "Scraping Volume", value: "45.2k", trend: "Sources/day", trendUp: true, icon: <Globe size={20} /> },
        ]}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* Research Throughput */}
        <Panel title="Research Throughput" subtitle="Ideas generated vs Debates vs Approvals" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={throughputData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorIdeas" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#7c3aed" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#7c3aed" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorDebates" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="day" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="ideas" name="Ideas" stroke="#7c3aed" strokeWidth={2} fillOpacity={1} fill="url(#colorIdeas)" />
                <Area type="monotone" dataKey="debates" name="Debates" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#colorDebates)" />
                <Area type="monotone" dataKey="approved" name="Approved" stroke="#10b981" strokeWidth={2} fillOpacity={0.1} fill="#10b981" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Idea Feasibility vs Sentiment (Scatter) */}
        <Panel title="Idea Scatter Plot" subtitle="Feasibility (Vega) vs Sentiment (Pulse)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                <XAxis type="number" dataKey="feasibility" name="Feasibility" stroke="#52525b" fontSize={10} domain={[0, 100]} />
                <YAxis type="number" dataKey="sentiment" name="Sentiment" stroke="#52525b" fontSize={10} domain={[0, 100]} />
                <ZAxis type="number" dataKey="z" range={[50, 400]} name="Score" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any) => [value, name === 'z' ? 'Score' : name]}
                />
                <ReferenceLine x={50} stroke="#52525b" strokeOpacity={0.5} />
                <ReferenceLine y={50} stroke="#52525b" strokeOpacity={0.5} />
                <Scatter name="Ideas" data={scatterIdeasData}>
                  {scatterIdeasData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* Trend Radar */}
        <Panel title="Market Trend Radar" subtitle="Emerging topics by momentum" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={sentimentData}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Current Trends" dataKey="A" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                <Radar name="Past Trends" dataKey="B" stroke="#52525b" fill="#52525b" fillOpacity={0.3} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Scraping Volume */}
        <Panel title="Scout Scraping Volume" subtitle="Headlines & sources consumed per hour" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={scrapingVolumeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="hour" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Line type="monotone" dataKey="volume" stroke="#06b6d4" strokeWidth={3} dot={{ fill: '#06b6d4', strokeWidth: 2, r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Sentiment Gauge & Word Cloud */}
        <Panel title="Market Pulse" subtitle="Real-time sentiment & keyword analysis" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col items-center justify-between">
            {/* Gauge */}
            <div className="flex flex-col items-center justify-center flex-1 w-full">
              <div className="relative flex items-center justify-center">
                <svg className="w-40 h-20" viewBox="0 0 100 50">
                  <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#27272a" strokeWidth="12" strokeLinecap="round" />
                  <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#10b981" strokeWidth="12" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="40" className="transition-all duration-1000" />
                </svg>
                <div className="absolute bottom-0 flex flex-col items-center">
                  <span className="text-2xl font-bold text-white">78</span>
                  <span className="text-[10px] text-emerald-400 uppercase tracking-wider">Positive</span>
                </div>
              </div>
            </div>
            
            {/* Word Cloud (Simulated) */}
            <div className="flex-1 w-full flex flex-wrap items-center justify-center gap-x-4 gap-y-2 p-4 bg-black/20 rounded-xl border border-white/5">
              {wordCloudTags.map((tag, i) => (
                <span key={i} className={`${tag.size} ${tag.color} ${tag.weight} transition-all hover:scale-110 cursor-default`}>
                  {tag.text}
                </span>
              ))}
            </div>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12">
        {/* Business Hypotheses Table */}
        <Panel title="Business Hypotheses" subtitle="Detailed breakdown of current ideas" className="xl:col-span-8">
          <div className="mt-4 overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-white/5 border-b border-white/10 text-muted-foreground">
                <tr>
                  <th className="p-3 font-medium rounded-tl-lg">Idea</th>
                  <th className="p-3 font-medium">Revenue Model</th>
                  <th className="p-3 font-medium">Target Audience</th>
                  <th className="p-3 font-medium">Status</th>
                  <th className="p-3 font-medium rounded-tr-lg">Avg Refinement Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { idea: "AI-Powered CRM", model: "SaaS / B2B", audience: "Mid-market Sales", status: "Approved", time: "2.4h" },
                  { idea: "DevOps Bot", model: "Usage-based", audience: "SRE Teams", status: "Debating", time: "1.2h" },
                  { idea: "Web3 Identity", model: "Transaction Fee", audience: "Crypto Exchanges", status: "Rejected", time: "4.5h" },
                  { idea: "NoCode App Builder", model: "Tiered Sub", audience: "Founders", status: "Debating", time: "3.1h" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/[0.02] transition-colors">
                    <td className="p-3 font-medium text-white">{row.idea}</td>
                    <td className="p-3 text-muted-foreground">{row.model}</td>
                    <td className="p-3 text-muted-foreground">{row.audience}</td>
                    <td className="p-3">
                      <span className={`px-2 py-1 rounded-full text-[10px] uppercase tracking-wider font-semibold ${
                        row.status === 'Approved' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                        row.status === 'Rejected' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                        'bg-cyber-cyan/10 text-cyber-cyan border border-cyber-cyan/20'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="p-3 text-muted-foreground">{row.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>

        {/* Live Source Heatmap */}
        <Panel title="Source Quality Heatmap" subtitle="Profitability vs Source (Reddit, HN, etc)" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col justify-center">
            <div className="grid grid-cols-5 gap-2">
              <div className="col-span-1"></div>
              {['Mon', 'Tue', 'Wed', 'Thu'].map(d => <div key={d} className="text-center text-xs text-muted-foreground">{d}</div>)}
              
              {['HackerNews', 'Reddit', 'ProductHunt', 'Twitter'].map((source, i) => (
                <div key={source} className="contents">
                  <div className="text-xs text-muted-foreground flex items-center justify-end pr-2">{source}</div>
                  {Array.from({length: 4}).map((_, j) => {
                    const intensity = Math.random();
                    return (
                      <div 
                        key={`${i}-${j}`} 
                        className="h-12 rounded-md transition-all hover:scale-105 hover:ring-1 hover:ring-white/20 cursor-pointer"
                        style={{ backgroundColor: `rgba(16, 185, 129, ${intensity * 0.9 + 0.1})` }}
                        title={`${source}: ${(intensity * 100).toFixed(0)}% quality score`}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </Panel>
      </div>
    </main>
  );
}
