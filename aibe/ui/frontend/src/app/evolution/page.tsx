"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { Lightbulb, Settings, GitPullRequest, ShieldCheck } from "lucide-react";

const proposalsData = [
  { sprint: "Sprint 1", proposals: 12, accepted: 4, rejected: 8 },
  { sprint: "Sprint 2", proposals: 18, accepted: 6, rejected: 12 },
  { sprint: "Sprint 3", proposals: 15, accepted: 7, rejected: 8 },
  { sprint: "Sprint 4", proposals: 22, accepted: 10, rejected: 12 },
  { sprint: "Sprint 5", proposals: 24, accepted: 11, rejected: 13 },
];

const fitnessScores = [
  { subject: "Efficiency", score: 85, fullMark: 100 },
  { subject: "Cost", score: 92, fullMark: 100 },
  { subject: "Reliability", score: 78, fullMark: 100 },
  { subject: "Speed", score: 88, fullMark: 100 },
  { subject: "Security", score: 95, fullMark: 100 },
];

export default function EvolutionPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Evolution Lab"
        title="Ciclo contínuo de autoaperfeiçoamento e seleção de estratégias"
        subtitle="Ambiente para propostas evolutivas, catálogo de ferramentas e análise Darwin de adaptação."
      />
      <StatGrid
        stats={[
          { label: "Proposals", value: "24", icon: <Lightbulb size={20} /> },
          { label: "Accepted", value: "11", tone: "good", icon: <GitPullRequest size={20} /> },
          { label: "Regression Risk", value: "Low", tone: "good", icon: <ShieldCheck size={20} /> },
          { label: "Tool Candidates", value: "7", icon: <Settings size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Proposals Timeline" subtitle="Aceitação de propostas por Sprint">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={proposalsData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="sprint" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="accepted" name="Accepted" fill="#10b981" radius={[0, 0, 4, 4]} stackId="a" />
                <Bar dataKey="rejected" name="Rejected" fill="#ef4444" radius={[4, 4, 0, 0]} stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Darwin Analysis" subtitle="Fitness score da estratégia atual">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={fitnessScores}>
                <PolarGrid stroke="#27272a" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#a1a1aa', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Current Strategy" dataKey="score" stroke="#7c3aed" fill="#7c3aed" fillOpacity={0.4} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Tool Registry" subtitle="Inventário de capacidades disponíveis e em teste" className="xl:col-span-2">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">Tool Name</th>
                  <th className="px-4 py-3 font-medium">Category</th>
                  <th className="px-4 py-3 font-medium">Success Rate</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { name: "CodeRefactorBot", cat: "Engineering", rate: "94%", status: "Active" },
                  { name: "MarketAnalyzer", cat: "Research", rate: "88%", status: "Active" },
                  { name: "SentimentScraper", cat: "Marketing", rate: "76%", status: "Testing" },
                  { name: "BudgetOptimizer", cat: "Finance", rate: "—", status: "Proposed" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.name}</td>
                    <td className="px-4 py-3">{row.cat}</td>
                    <td className="px-4 py-3 text-cyber-cyan">{row.rate}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        row.status === 'Active' ? 'bg-emerald-500/10 text-emerald-400' : 
                        row.status === 'Testing' ? 'bg-amber-500/10 text-amber-400' : 
                        'bg-white/10 text-white/60'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <button className="text-cyber-cyan hover:underline text-xs">Review</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      </section>
    </main>
  );
}



