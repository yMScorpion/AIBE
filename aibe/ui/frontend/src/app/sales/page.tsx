"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, Cell, ScatterChart, Scatter, ZAxis, Line, ComposedChart } from "recharts";
import { DollarSign, CheckCircle2, Activity, Zap } from "lucide-react";

const pipelineData = [
  { stage: "Lead", value: 1200000, count: 120 },
  { stage: "Meeting", value: 850000, count: 85 },
  { stage: "Proposal", value: 500000, count: 40 },
  { stage: "Negotiation", value: 300000, count: 15 },
  { stage: "Closed Won", value: 180000, count: 8 },
];

const customerHealthData = [
  { name: "Acme Corp", engagement: 90, risk: 10, mrr: 15000, fill: "hsl(var(--chart-1))" },
  { name: "Globex", engagement: 40, risk: 60, mrr: 8000, fill: "hsl(var(--chart-2))" },
  { name: "Initech", engagement: 20, risk: 85, mrr: 12000, fill: "hsl(var(--destructive))" },
  { name: "Soylent", engagement: 80, risk: 15, mrr: 5000, fill: "hsl(var(--chart-1))" },
  { name: "Massive Dynamic", engagement: 65, risk: 35, mrr: 25000, fill: "hsl(var(--primary))" },
  { name: "Umbrella", engagement: 30, risk: 75, mrr: 18000, fill: "hsl(var(--destructive))" },
];

const waterfallData = [
  { name: "Starting MRR", uv: 150, pv: 0, fill: "hsl(var(--primary))" },
  { name: "New Biz", uv: 25, pv: 150, fill: "hsl(var(--chart-1))" },
  { name: "Expansion", uv: 15, pv: 175, fill: "hsl(var(--chart-1))" },
  { name: "Contraction", uv: -5, pv: 190, fill: "hsl(var(--chart-2))" },
  { name: "Churn", uv: -10, pv: 185, fill: "hsl(var(--destructive))" },
  { name: "Ending MRR", uv: 175, pv: 0, fill: "hsl(var(--primary))" },
];

const demoPerformanceData = [
  { week: "W1", engagement: 65, conversions: 12 },
  { week: "W2", engagement: 72, conversions: 15 },
  { week: "W3", engagement: 68, conversions: 14 },
  { week: "W4", engagement: 85, conversions: 22 },
  { week: "W5", engagement: 82, conversions: 20 },
  { week: "W6", engagement: 90, conversions: 28 },
];



export default function SalesPage() {
  return (
    <main className="mx-auto max-w-[1600px] pb-12">
      <PageHero
        eyebrow="Tier 9 • Sales & CS Department"
        title="Predictable Revenue Engine"
        subtitle="Pipeline velocity, customer health, and expansion tracking by Mercury, Closer, and Guardian."
      />
      <StatGrid
        stats={[
          { label: "Pipeline Value", value: "$1.8M", tone: "good", icon: <DollarSign size={20} /> },
          { label: "Win Rate", value: "39%", icon: <CheckCircle2 size={20} /> },
          { label: "Sales Velocity", value: "24d", trend: "-2d", trendUp: true, tone: "good", icon: <Zap size={20} /> },
          { label: "NRR Pulse", value: "112%", tone: "good", icon: <Activity size={20} /> },
        ]}
      />
      
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mt-6 mb-6">
        {/* 3D Funnel (Simulated with BarChart) */}
        <Panel title="Sales Pipeline Funnel" subtitle="Prospects to Closed Won" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineData} layout="vertical" margin={{ top: 10, right: 30, left: 40, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `$${v/1000}k`} />
                <YAxis dataKey="stage" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} width={80} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any, props: any) => [`$${(value/1000).toFixed(0)}k (${props.payload.count} deals)`, 'Pipeline']}
                />
                <Bar dataKey="value" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]}>
                  {pipelineData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={`rgba(59, 130, 246, ${1 - index * 0.15})`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Customer Health Scatter */}
        <Panel title="Customer Health Matrix" subtitle="Engagement vs Churn Risk (Guardian)" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" dataKey="engagement" name="Engagement" stroke="hsl(var(--muted-foreground))" fontSize={10} domain={[0, 100]} />
                <YAxis type="number" dataKey="risk" name="Churn Risk" stroke="hsl(var(--muted-foreground))" fontSize={10} domain={[0, 100]} />
                <ZAxis type="number" dataKey="mrr" range={[50, 400]} name="MRR" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any) => [name === 'mrr' ? `$${value}` : `${value}%`, name]}
                />
                <Scatter name="Customers" data={customerHealthData}>
                  {customerHealthData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* Revenue Forecast Waterfall (Simulated via BarChart) */}
        <Panel title="Revenue Forecast Waterfall" subtitle="MRR Bridges (Mercury)" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={waterfallData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(v) => `$${v}k`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`$${value}k`, 'Value']}
                />
                <Bar dataKey="pv" stackId="a" fill="transparent" />
                <Bar dataKey="uv" stackId="a">
                  {waterfallData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Demo Performance Line Chart */}
        <Panel title="Demo Performance" subtitle="Engagement vs Conversion (Orator)" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={demoPerformanceData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="week" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar yAxisId="right" dataKey="conversions" name="Conversions" fill="hsl(var(--primary))" barSize={20} radius={[4, 4, 0, 0]} />
                <Line yAxisId="left" type="monotone" dataKey="engagement" name="Engagement Score" stroke="hsl(var(--chart-1))" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-12 mb-6">
        {/* VIP Negotiations Table */}
        <Panel title="VIP Negotiations" subtitle="High-ticket deals in progress (Closer)" className="xl:col-span-8">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4 h-[300px] overflow-y-auto pr-2 scrollbar-hide">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80 sticky top-0">
                <tr>
                  <th className="px-4 py-3 font-medium">Prospect</th>
                  <th className="px-4 py-3 font-medium">Value</th>
                  <th className="px-4 py-3 font-medium">Probability</th>
                  <th className="px-4 py-3 font-medium">Next Action</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { prospect: "Wayne Enterprises", value: "$250,000", prob: "85%", action: "Send final contract", status: "Hot" },
                  { prospect: "Stark Industries", value: "$400,000", prob: "60%", action: "Security review", status: "Warm" },
                  { prospect: "Cyberdyne Systems", value: "$120,000", prob: "90%", action: "Awaiting signature", status: "Hot" },
                  { prospect: "Tyrell Corp", value: "$850,000", prob: "30%", action: "Technical deep dive", status: "Cold" },
                  { prospect: "Oscorp", value: "$180,000", prob: "75%", action: "Pricing negotiation", status: "Warm" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.prospect}</td>
                    <td className="px-4 py-3 font-medium text-emerald-400">{row.value}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-16 bg-white/10 rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-500 rounded-full" style={{ width: row.prob }}></div>
                        </div>
                        <span className="text-xs">{row.prob}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-xs">{row.action}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                        row.status === 'Hot' ? 'bg-rose-500/10 text-rose-400' : 
                        row.status === 'Warm' ? 'bg-amber-500/10 text-amber-400' : 
                        'bg-blue-500/10 text-blue-400'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>

        {/* NRR Gauge */}
        <Panel title="Net Retention Rate" subtitle="Health of customer base" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col items-center justify-center">
            <div className="relative flex items-center justify-center">
              <svg className="w-56 h-28" viewBox="0 0 100 50">
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--border))" strokeWidth="10" strokeLinecap="round" />
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--primary))" strokeWidth="10" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="15" className="transition-all duration-1000" />
              </svg>
              <div className="absolute bottom-0 flex flex-col items-center">
                <span className="text-4xl font-bold text-white">112%</span>
                <span className="text-xs text-blue-400 uppercase tracking-wider font-semibold mt-1">Excellent</span>
              </div>
            </div>
            <div className="mt-8 text-sm text-muted-foreground text-center px-4">
              NRR is above the 100% threshold, indicating that expansion revenue outpaces churn.
            </div>
          </div>
        </Panel>
      </div>

    </main>
  );
}



