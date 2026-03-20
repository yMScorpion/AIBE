"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend } from "recharts";
import { DollarSign, TrendingUp, AlertTriangle, Briefcase, RefreshCw } from "lucide-react";
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
        eyebrow="Finance & Ops"
        title="Controle financeiro em tempo real com foco em margem e eficiência"
        subtitle="Visão consolidada de P&L, limites de custos e gestão de parceiros operacionais."
      />
      <StatGrid
        stats={[
          { label: "MRR", value: "$65k", tone: "good", icon: <DollarSign size={20} /> },
          { label: "Gross Margin", value: "71%", tone: "good", icon: <TrendingUp size={20} /> },
          { label: "Runway", value: "22 months", tone: "default", icon: <Briefcase size={20} /> },
          { label: "Budget Variance", value: "+2.4%", tone: "warn", icon: <AlertTriangle size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Revenue vs Expenses" subtitle="Evolução de P&L nos últimos 6 meses">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={revenueData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorExp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="month" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="revenue" name="Revenue ($)" stroke="#10b981" fillOpacity={1} fill="url(#colorRev)" />
                <Area type="monotone" dataKey="expenses" name="Expenses ($)" stroke="#ef4444" fillOpacity={1} fill="url(#colorExp)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Cost Distribution" subtitle="Distribuição de custos operacionais por categoria">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={costDistribution} layout="vertical" margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis dataKey="category" type="category" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
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



