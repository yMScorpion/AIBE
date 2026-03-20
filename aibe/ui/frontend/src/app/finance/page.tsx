"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, ScatterChart, Scatter, ZAxis, ReferenceLine, LineChart, Line, Cell } from "recharts";
import { DollarSign, TrendingUp, Briefcase, RefreshCw, ShieldCheck, CheckCircle2, AlertCircle } from "lucide-react";
import { useState } from "react";

const revenueData = [
  { month: "Jan", revenue: 10000, expenses: 5000, profit: 5000 },
  { month: "Feb", revenue: 15000, expenses: 7000, profit: 8000 },
  { month: "Mar", revenue: 22000, expenses: 9000, profit: 13000 },
  { month: "Apr", revenue: 35000, expenses: 12000, profit: 23000 },
  { month: "May", revenue: 48000, expenses: 15000, profit: 33000 },
  { month: "Jun", revenue: 65000, expenses: 19000, profit: 46000 },
];

const costDistribution = [
  { category: "Infrastructure", cost: 12000 },
  { category: "LLM API", cost: 8000 },
  { category: "Marketing", cost: 0 },
  { category: "Contractors", cost: 5000 },
  { category: "Software", cost: 2000 },
];

const tokenUsageData = [
  { day: "Mon", input: 1200000, output: 400000 },
  { day: "Tue", input: 1500000, output: 500000 },
  { day: "Wed", input: 1800000, output: 600000 },
  { day: "Thu", input: 1400000, output: 450000 },
  { day: "Fri", input: 2200000, output: 800000 },
  { day: "Sat", input: 900000, output: 300000 },
  { day: "Sun", input: 800000, output: 250000 },
];

const efficiencyData = [
  { model: "GPT-4", complexity: 90, cost: 0.03, z: 200, fill: "hsl(var(--primary))" },
  { model: "Claude 3.5", complexity: 85, cost: 0.015, z: 150, fill: "hsl(var(--chart-5))" },
  { model: "Llama 3", complexity: 75, cost: 0.005, z: 300, fill: "hsl(var(--chart-1))" },
  { model: "Mixtral 8x22B", complexity: 60, cost: 0.002, z: 400, fill: "hsl(var(--chart-2))" },
];

const burnForecastData = [
  { date: "1st", actual: 100, forecast: 100 },
  { date: "5th", actual: 500, forecast: 500 },
  { date: "10th", actual: 1200, forecast: 1000 },
  { date: "15th", actual: 1800, forecast: 1500 },
  { date: "20th", actual: null, forecast: 2000 },
  { date: "25th", actual: null, forecast: 2500 },
  { date: "30th", actual: null, forecast: 3000 },
];

export default function FinancePage() {
  const currentRevenue = 65000;
  const [marketingBudget, setMarketingBudget] = useState(0);

  const handleAutoAdjust = () => {
    // Simulated auto-adjustment based on revenue
    let newBudget = 0;
    if (currentRevenue > 50000) newBudget = 5000;
    else if (currentRevenue > 20000) newBudget = 2000;
    else if (currentRevenue > 10000) newBudget = 500;

    setMarketingBudget(newBudget);
  };

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Tier 5 • Finance & Ops"
        title="Financial Command Center"
        subtitle="Compliance, audit, and strict cost tracking managed by Ledger, Atlas, and Procurator."
      />
      <StatGrid
        stats={[
          { label: "MRR", value: "$65k", tone: "good", icon: <DollarSign size={20} /> },
          { label: "Operational ROI", value: "3.4x", tone: "good", icon: <TrendingUp size={20} /> },
          { label: "Runway", value: "22 months", tone: "default", icon: <Briefcase size={20} /> },
          { label: "Compliance Score", value: "98%", tone: "good", icon: <ShieldCheck size={20} /> },
        ]}
      />
      
      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Token Usage Stack */}
        <Panel title="Ledger Token Usage" subtitle="Daily Input vs Output tokens (Millions)" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={tokenUsageData} margin={{ top: 10, right: 0, left: 10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorInput" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorOutput" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--chart-5))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--chart-5))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="day" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `${v/1000000}M`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(val: any, name: any) => [(val/1000000).toFixed(1) + 'M', name]}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="input" name="Input Tokens" stackId="1" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorInput)" />
                <Area type="monotone" dataKey="output" name="Output Tokens" stackId="1" stroke="hsl(var(--chart-5))" fillOpacity={1} fill="url(#colorOutput)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Compliance Gauge */}
        <Panel title="Atlas Compliance Score" subtitle="LGPD, SOC2 & Security Adherence" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col items-center justify-center">
            <div className="relative flex items-center justify-center">
              <svg className="w-48 h-24" viewBox="0 0 100 50">
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--border))" strokeWidth="12" strokeLinecap="round" />
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="hsl(var(--chart-1))" strokeWidth="12" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="5" className="transition-all duration-1000" />
              </svg>
              <div className="absolute bottom-0 flex flex-col items-center">
                <span className="text-3xl font-bold text-white">98%</span>
                <span className="text-xs text-emerald-400 uppercase tracking-wider mt-1">Compliant</span>
              </div>
            </div>
            <div className="mt-8 flex flex-col gap-2 w-full max-w-[200px]">
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">SOC2 Type II</span>
                <span className="text-emerald-400">Pass</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">LGPD / GDPR</span>
                <span className="text-emerald-400">Pass</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted-foreground">Access Audit</span>
                <span className="text-emerald-400">Pass</span>
              </div>
            </div>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Cost Efficiency Scatter */}
        <Panel title="Cost Efficiency Matrix" subtitle="Task Complexity vs LLM Cost (USD)" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" dataKey="complexity" name="Complexity" stroke="hsl(var(--muted-foreground))" fontSize={10} domain={[0, 100]} />
                <YAxis type="number" dataKey="cost" name="Cost (USD/1k)" stroke="hsl(var(--muted-foreground))" fontSize={10} />
                <ZAxis type="number" dataKey="z" range={[50, 400]} name="Usage" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any, name: any) => [name === 'z' ? `Count: ${value}` : `$${value}`, name === 'z' ? 'Volume' : name]}
                />
                <ReferenceLine y={0.01} stroke="hsl(var(--destructive))" strokeOpacity={0.5} strokeDasharray="3 3" label={{ value: 'Cost Limit', fill: 'hsl(var(--destructive))', fontSize: 10 }} />
                <Scatter name="Models" data={efficiencyData}>
                  {efficiencyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Burn Rate Forecast */}
        <Panel title="Burn Rate Forecast" subtitle="Actual spend vs projected limit" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={burnForecastData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line type="monotone" dataKey="actual" name="Actual Spend" stroke="hsl(var(--destructive))" strokeWidth={3} dot={{ fill: 'hsl(var(--destructive))', strokeWidth: 2, r: 4 }} />
                <Line type="monotone" dataKey="forecast" name="Forecast" stroke="hsl(var(--muted-foreground))" strokeWidth={2} strokeDasharray="5 5" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Procurator Pipeline */}
        <Panel title="Procurator Hiring Pipeline" subtitle="Freelancer sourcing flow" className="xl:col-span-8">
          <div className="h-[200px] w-full mt-4 flex items-center justify-between px-4">
            {[
              { step: "Justification", status: "success", icon: <CheckCircle2 size={24} />, desc: "LLM failed 3x" },
              { step: "Sourcing", status: "success", icon: <RefreshCw size={24} />, desc: "Upwork API" },
              { step: "Negotiation", status: "active", icon: <DollarSign size={24} />, desc: "Awaiting quote" },
              { step: "Approved", status: "pending", icon: <Briefcase size={24} />, desc: "Not started" },
            ].map((stage, i, arr) => (
              <div key={i} className="flex items-center flex-1 last:flex-none">
                <div className="flex flex-col items-center gap-3">
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center border-2 ${
                    stage.status === 'success' ? 'bg-emerald-500/10 border-emerald-500 text-emerald-400' :
                    stage.status === 'active' ? 'bg-cyber-purple/10 border-cyber-purple text-cyber-purple shadow-[0_0_15px_rgba(168,85,247,0.5)]' :
                    'bg-white/5 border-white/10 text-muted-foreground'
                  }`}>
                    {stage.icon}
                  </div>
                  <div className="text-center">
                    <span className={`block text-sm font-medium ${stage.status === 'active' ? 'text-white' : 'text-muted-foreground'}`}>{stage.step}</span>
                    <span className="text-[10px] text-muted-foreground">{stage.desc}</span>
                  </div>
                </div>
                {i < arr.length - 1 && (
                  <div className="flex-1 h-1 mx-4 rounded-full overflow-hidden bg-white/5">
                    <div className={`h-full ${stage.status === 'success' ? 'bg-emerald-500' : stage.status === 'active' ? 'bg-cyber-purple w-1/2 animate-pulse' : 'bg-transparent'}`}></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Panel>

        {/* Financial Anomalies */}
        <Panel title="Financial Anomalies" subtitle="Unusual API requests detected" className="xl:col-span-4">
          <div className="space-y-3 mt-4 h-[200px] overflow-y-auto pr-2 scrollbar-hide">
            {[
              { agent: "Forge", issue: "Spike in GPT-4 calls", amount: "+$45.20", time: "10m ago" },
              { agent: "Scout", issue: "High bandwidth scraping", amount: "+$12.50", time: "1h ago" },
            ].map((alert, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
                <div className="flex items-start gap-3">
                  <AlertCircle size={16} className="text-rose-400 mt-0.5" />
                  <div>
                    <p className="text-sm font-semibold text-rose-100">{alert.agent}</p>
                    <p className="text-xs text-rose-400/80">{alert.issue}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-sm font-bold text-rose-400">{alert.amount}</span>
                  <p className="text-[10px] text-rose-400/60">{alert.time}</p>
                </div>
              </div>
            ))}
            <div className="flex items-center justify-center p-4 border border-dashed border-white/10 rounded-xl">
              <span className="text-xs text-muted-foreground">All other systems nominal</span>
            </div>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Revenue vs Expenses" subtitle="Evolução de P&L nos últimos 6 meses">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorExp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--destructive))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--destructive))" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis dataKey="month" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="revenue" name="Revenue ($)" stroke="hsl(var(--chart-1))" fillOpacity={1} fill="url(#colorRev)" />
                <Area type="monotone" dataKey="expenses" name="Expenses ($)" stroke="hsl(var(--destructive))" fillOpacity={1} fill="url(#colorExp)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Cost Distribution" subtitle="Distribuição de custos operacionais por categoria">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={costDistribution} layout="vertical" margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" horizontal={false} />
                <XAxis type="number" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="category" type="category" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--card))', borderColor: 'hsl(var(--border))', borderRadius: '12px', color: 'hsl(var(--foreground))' }}
                  itemStyle={{ color: 'hsl(var(--foreground))' }}
                  cursor={{ fill: 'hsl(var(--border))', opacity: 0.4 }}
                />
                <Bar dataKey="cost" name="Cost ($)" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Marketing Budget Auto-Adjustment" subtitle="Ajuste automático baseado em faturamento (Organic First)" className="xl:col-span-2">
          <div className="rounded-xl border border-white/5 bg-black/20 p-6 mt-4 flex flex-col md:flex-row items-center gap-8 justify-between">
            <div className="flex-1 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Current MRR:</span>
                <span className="text-xl font-bold text-emerald-400">${currentRevenue.toLocaleString()}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Marketing Budget:</span>
                <span className="text-xl font-bold text-cyber-cyan">${marketingBudget.toLocaleString()}</span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Estratégia inicial focada em tráfego orgânico (Budget $0). O sistema ajustará automaticamente os limites na página de configurações assim que os marcos de faturamento forem atingidos.
              </p>
            </div>
            <div className="w-[1px] h-24 bg-white/10 hidden md:block"></div>
            <div className="flex-1 flex flex-col items-center justify-center gap-4">
              <button 
                onClick={handleAutoAdjust}
                className="flex items-center gap-2 rounded-xl bg-cyber-purple/20 px-6 py-3 text-sm font-semibold text-cyber-purple border border-cyber-purple/40 hover:bg-cyber-purple/30 transition-all"
              >
                <RefreshCw size={18} />
                Run Auto-Adjust Sync
              </button>
              {marketingBudget > 0 && (
                <span className="text-xs text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                  Budget liberado baseado no MRR atual!
                </span>
              )}
            </div>
          </div>
        </Panel>
      </section>
    </main>
  );
}



