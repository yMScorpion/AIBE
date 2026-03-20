"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { 
  Lightbulb, 
  MessageSquareText, 
  CheckCircle, 
  FlaskConical,
  Activity
} from "lucide-react";
import { Area, AreaChart, Pie, PieChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from "recharts";

const throughputData = [
  { day: "Mon", ideas: 12, debates: 8, approved: 2 },
  { day: "Tue", ideas: 15, debates: 10, approved: 3 },
  { day: "Wed", ideas: 22, debates: 18, approved: 5 },
  { day: "Thu", ideas: 18, debates: 14, approved: 4 },
  { day: "Fri", ideas: 25, debates: 20, approved: 7 },
  { day: "Sat", ideas: 10, debates: 5, approved: 1 },
  { day: "Sun", ideas: 8, debates: 4, approved: 1 },
];

const categoryData = [
  { name: "SaaS Products", value: 35 },
  { name: "E-commerce", value: 25 },
  { name: "Developer Tools", value: 20 },
  { name: "AI Services", value: 15 },
  { name: "Hardware", value: 5 },
];

const sentimentData = [
  { subject: 'Innovation', A: 120, B: 110, fullMark: 150 },
  { subject: 'Feasibility', A: 98, B: 130, fullMark: 150 },
  { subject: 'Market Size', A: 86, B: 130, fullMark: 150 },
  { subject: 'Cost', A: 99, B: 100, fullMark: 150 },
  { subject: 'Risk', A: 85, B: 90, fullMark: 150 },
  { subject: 'Impact', A: 65, B: 85, fullMark: 150 },
];

const COLORS = ['#7c3aed', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'];

export default function ResearchPage() {
  return (
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Research Department"
        title="Innovation Engine"
        subtitle="Tracking idea generation, market analysis, and autonomous debate outcomes by the Research Swarm."
      />

      <StatGrid
        stats={[
          { label: "Total Ideas Generated", value: "342", trend: "12% up", trendUp: true, icon: <Lightbulb size={20} /> },
          { label: "Active Debates", value: "18", trend: "High activity", trendUp: true, icon: <MessageSquareText size={20} />, tone: "hot" },
          { label: "Proposals Approved", value: "45", trend: "Steady", trendUp: true, icon: <CheckCircle size={20} />, tone: "good" },
          { label: "Research Cost", value: "$1.2k", trend: "Within limits", trendUp: false, icon: <FlaskConical size={20} /> },
        ]}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12">
        {/* Research Throughput */}
        <Panel title="Research Throughput" subtitle="Ideas generated vs Debates vs Approvals (7 Days)" className="xl:col-span-8">
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

        {/* Idea Categories */}
        <Panel title="Idea Categories" subtitle="Distribution of generated concepts" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {categoryData.map((entry, index) => (
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

        {/* Debate Analysis */}
        <Panel title="Debate Sentiment Analysis" subtitle="Evaluation metrics for current top proposals" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={sentimentData}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Project Alpha" dataKey="A" stroke="#7c3aed" fill="#7c3aed" fillOpacity={0.3} />
                <Radar name="Project Beta" dataKey="B" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Live Debates Feed */}
        <Panel title="Live Debates" subtitle="Ongoing discussions between Scout, Vega, and Pulse" className="xl:col-span-6">
          <div className="space-y-4 mt-4 h-[300px] overflow-y-auto pr-2 scrollbar-hide">
            {[
              { topic: "AI-Powered CRM Integration", agents: "Scout vs Pulse", status: "Hot", time: "Just now" },
              { topic: "Serverless Edge Functions Tooling", agents: "Vega vs Scout", status: "Concluding", time: "10 mins ago" },
              { topic: "Web3 Identity Verification", agents: "Pulse vs Vega", status: "Stalled", time: "1 hour ago" },
              { topic: "Automated QA Platform", agents: "Scout vs Vega", status: "Hot", time: "2 hours ago" },
              { topic: "B2B Marketplace Protocol", agents: "All", status: "Review", time: "3 hours ago" }
            ].map((debate, i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-2xl bg-black/20 border border-white/5">
                <div>
                  <div className="flex items-center gap-2">
                    <Activity size={14} className={debate.status === 'Hot' ? 'text-rose-500' : 'text-cyber-cyan'} />
                    <p className="text-sm font-semibold text-white">{debate.topic}</p>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Debaters: <span className="text-cyber-cyan">{debate.agents}</span></p>
                </div>
                <div className="text-right">
                  <span className={`text-[10px] font-semibold px-2 py-1 rounded-full uppercase tracking-wider ${
                    debate.status === 'Hot' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                    debate.status === 'Concluding' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                    debate.status === 'Review' ? 'bg-cyber-purple/10 text-cyber-purple border border-cyber-purple/20' :
                    'bg-white/5 text-muted-foreground border border-white/10'
                  }`}>
                    {debate.status}
                  </span>
                  <p className="text-[10px] text-muted-foreground mt-2">{debate.time}</p>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </main>
  );
}
