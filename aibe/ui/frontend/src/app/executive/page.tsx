"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { 
  TrendingUp, 
  Target, 
  AlertTriangle,
  DollarSign
} from "lucide-react";
import { Area, AreaChart, Bar, BarChart, Pie, PieChart, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, Line } from "recharts";

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

const COLORS = ['#7c3aed', '#06b6d4', '#10b981', '#f59e0b'];

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
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="month" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="actual" name="Actual Revenue" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorActual)" />
                <Line type="monotone" dataKey="projected" name="Projected" stroke="#52525b" strokeWidth={2} strokeDasharray="5 5" dot={false} />
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

        {/* OKR Progress */}
        <Panel title="Strategic OKRs Progress" subtitle="Quarterly Objectives and Key Results" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={okrData} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                <YAxis dataKey="name" type="category" stroke="#52525b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`${value}%`, 'Progress']}
                />
                <Bar dataKey="progress" fill="#7c3aed" radius={[0, 4, 4, 0]} barSize={24}>
                  {okrData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.progress > 80 ? '#10b981' : entry.progress > 50 ? '#f59e0b' : '#ef4444'} />
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
