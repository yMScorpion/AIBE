"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { 
  TrendingUp, 
  Target, 
  AlertTriangle,
  DollarSign
} from "lucide-react";
import { Area, AreaChart, Bar, BarChart, Pie, PieChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, Line, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Scatter, ScatterChart, ZAxis, ReferenceLine } from "recharts";

const okrData = [
  { name: "Q1 Launch", progress: 85, target: 100 },
  { name: "ARR Growth", progress: 60, target: 100 },
  { name: "User Retention", progress: 92, target: 100 },
  { name: "Market Expansion", progress: 45, target: 100 },
];

const revenueData = [
  { month: "Jan", actual: 120, projected: 110 },
  { month: "Feb", actual: 135, projected: 125 },
  { month: "Mar", actual: 150, projected: 140 },
  { month: "Apr", actual: 180, projected: 160 },
  { month: "May", actual: 210, projected: 190 },
  { month: "Jun", actual: 250, projected: 220 },
];

const expenseAllocation = [
  { name: "R&D", value: 45 },
  { name: "Marketing", value: 25 },
  { name: "Operations", value: 20 },
  { name: "Sales", value: 10 },
];

const COLORS = ['hsl(var(--primary))', 'hsl(var(--accent))', 'hsl(var(--chart-1))', 'hsl(var(--chart-2))'];

const radarData = [
  { subject: 'Innovation', A: 120, B: 110, fullMark: 150 },
  { subject: 'Market Fit', A: 98, B: 130, fullMark: 150 },
  { subject: 'Efficiency', A: 86, B: 130, fullMark: 150 },
  { subject: 'Growth', A: 99, B: 100, fullMark: 150 },
  { subject: 'Stability', A: 85, B: 90, fullMark: 150 },
  { subject: 'Speed', A: 65, B: 85, fullMark: 150 },
];

const eisenhowerData = [
  { name: 'Core Rewrite', importance: 90, urgency: 85, z: 200, fill: 'hsl(var(--destructive))' }, // Do
  { name: 'New Feature X', importance: 80, urgency: 40, z: 200, fill: 'hsl(var(--primary))' }, // Schedule
  { name: 'Bug Fixes', importance: 30, urgency: 95, z: 200, fill: 'hsl(var(--chart-2))' }, // Delegate
  { name: 'UI Tweaks', importance: 20, urgency: 20, z: 200, fill: 'hsl(var(--chart-1))' }, // Eliminate
];

const funnelData = [
  { stage: 'Proposals', value: 120 },
  { stage: 'Reviewed', value: 80 },
  { stage: 'Approved', value: 30 },
  { stage: 'Execution', value: 10 },
];

export default function ExecutivePage() {
  return (
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Executive Department"
        title="Strategic Command"
        subtitle="High-level overview of company performance, strategic OKRs, and executive decision-making."
      />

      <StatGrid
        stats={[
          { label: "Total Revenue (YTD)", value: "$1.2M", trend: "18% vs last year", trendUp: true, icon: <DollarSign size={20} />, tone: "good" },
          { label: "Burn Rate", value: "$45k/mo", trend: "5% reduction", trendUp: false, icon: <TrendingUp size={20} />, tone: "good" },
          { label: "Active OKRs", value: "4", trend: "On track", trendUp: true, icon: <Target size={20} /> },
          { label: "Pending Approvals", value: "3", trend: "Requires attention", trendUp: false, icon: <AlertTriangle size={20} />, tone: "warn" },
        ]}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12">
        {/* Revenue vs Projection */}
        <Panel title="Revenue Performance" subtitle="Actual vs Projected Growth (in thousands)" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="actual" name="Actual Revenue" stroke="hsl(var(--chart-1))" strokeWidth={3} fillOpacity={1} fill="url(#colorActual)" />
                <Line type="monotone" dataKey="projected" name="Projected" stroke="hsl(var(--muted-foreground))" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Expense Allocation */}
        <Panel title="Expense Allocation" subtitle="Current budget distribution" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={expenseAllocation}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {expenseAllocation.map((entry, index) => (
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

        {/* Strategic Alignment Radar */}
        <Panel title="Strategic Alignment Radar" subtitle="Current focus vs Oracle's target" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="hsl(var(--border))" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Target (Oracle)" dataKey="A" stroke="hsl(var(--accent))" fill="hsl(var(--accent))" fillOpacity={0.3} />
                <Radar name="Actual (Minerva)" dataKey="B" stroke="hsl(var(--primary))" fill="hsl(var(--primary))" fillOpacity={0.3} />
                <Legend wrapperStyle={{ fontSize: '10px' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Eisenhower Matrix */}
        <Panel title="Eisenhower Matrix" subtitle="Automated task prioritization" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 relative">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" dataKey="urgency" name="Urgency" stroke="hsl(var(--muted-foreground))" fontSize={10} domain={[0, 100]} />
                <YAxis type="number" dataKey="importance" name="Importance" stroke="hsl(var(--muted-foreground))" fontSize={10} domain={[0, 100]} />
                <ZAxis type="number" dataKey="z" range={[100, 300]} name="Score" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any, props: any) => [props.payload.name, 'Task']}
                />
                <ReferenceLine x={50} stroke="hsl(var(--muted-foreground))" strokeOpacity={0.5} />
                <ReferenceLine y={50} stroke="hsl(var(--muted-foreground))" strokeOpacity={0.5} />
                <Scatter name="Tasks" data={eisenhowerData}>
                  {eisenhowerData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
            {/* Labels for quadrants */}
            <span className="absolute top-2 left-6 text-[10px] text-muted-foreground font-semibold">Important / Not Urgent</span>
            <span className="absolute top-2 right-6 text-[10px] text-muted-foreground font-semibold">Important / Urgent</span>
            <span className="absolute bottom-6 left-6 text-[10px] text-muted-foreground font-semibold">Not Imp / Not Urgent</span>
            <span className="absolute bottom-6 right-6 text-[10px] text-muted-foreground font-semibold">Not Imp / Urgent</span>
          </div>
        </Panel>

        {/* Idea Approval Funnel */}
        <Panel title="Idea Approval Funnel" subtitle="Research to Execution flow" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="stage" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Bar dataKey="value" fill="hsl(var(--accent))" radius={[0, 4, 4, 0]} barSize={30}>
                  {funnelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} fillOpacity={1 - index * 0.15} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* OKR Progress */}
        <Panel title="Strategic OKRs Progress" subtitle="Quarterly Objectives and Key Results" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={okrData} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                <YAxis dataKey="name" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`${value}%`, 'Progress']}
                />
                <Bar dataKey="progress" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} barSize={24}>
                  {okrData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.progress > 80 ? 'hsl(var(--chart-1))' : entry.progress > 50 ? 'hsl(var(--chart-2))' : 'hsl(var(--destructive))'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Recent Decisions */}
        <Panel title="Executive Decisions" subtitle="Recent strategic moves by Oracle & Minerva" className="xl:col-span-6">
          <div className="space-y-4 mt-4">
            {[
              { title: "Budget Reallocation: Q3 Marketing", agent: "Oracle", status: "Approved", time: "2 hours ago" },
              { title: "New Market Entry Strategy", agent: "Minerva", status: "In Review", time: "5 hours ago" },
              { title: "Hiring Freeze Exception: Engineering", agent: "Oracle", status: "Approved", time: "1 day ago" },
              { title: "Vendor Contract Renewal", agent: "Minerva", status: "Rejected", time: "2 days ago" }
            ].map((decision, i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-2xl bg-black/20 border border-white/5">
                <div>
                  <p className="text-sm font-semibold text-white">{decision.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">Proposed by <span className="text-cyber-cyan">{decision.agent}</span></p>
                </div>
                <div className="text-right">
                  <span className={`text-xs font-semibold px-2 py-1 rounded-full ${
                    decision.status === 'Approved' ? 'bg-emerald-500/10 text-emerald-400' :
                    decision.status === 'Rejected' ? 'bg-rose-500/10 text-rose-400' :
                    'bg-amber-500/10 text-amber-400'
                  }`}>
                    {decision.status}
                  </span>
                  <p className="text-[10px] text-muted-foreground mt-2">{decision.time}</p>
                </div>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </main>
  );
}
