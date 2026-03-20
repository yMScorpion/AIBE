"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, LineChart, Line } from "recharts";
import { BrainCircuit, AlertCircle, Database, CheckCircle2 } from "lucide-react";

const performanceHistory = [
  { epoch: 10, accuracy: 0.75, loss: 0.45 },
  { epoch: 20, accuracy: 0.82, loss: 0.32 },
  { epoch: 30, accuracy: 0.88, loss: 0.25 },
  { epoch: 40, accuracy: 0.91, loss: 0.18 },
  { epoch: 50, accuracy: 0.94, loss: 0.12 },
];

const inferenceLatency = [
  { time: "10:00", latency: 45, p99: 85 },
  { time: "10:05", latency: 42, p99: 82 },
  { time: "10:10", latency: 55, p99: 110 },
  { time: "10:15", latency: 48, p99: 90 },
  { time: "10:20", latency: 46, p99: 88 },
  { time: "10:25", latency: 44, p99: 80 },
];

export default function MlPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="AI/ML Lab"
        title="Governança de modelos e experimentação com rastreabilidade"
        subtitle="Laboratório para registry, testes e observabilidade de pipelines de machine learning."
      />
      <StatGrid
        stats={[
          { label: "Models in Registry", value: "37", icon: <Database size={20} /> },
          { label: "Experiments Running", value: "9", tone: "good", icon: <BrainCircuit size={20} /> },
          { label: "Drift Alerts", value: "2", tone: "warn", icon: <AlertCircle size={20} /> },
          { label: "Pipeline Uptime", value: "99.1%", tone: "good", icon: <CheckCircle2 size={20} /> },
        ]}
      />
      <section className="mt-4 grid grid-cols-1 gap-6 xl:grid-cols-2">
        <Panel title="Model Training Performance" subtitle="Accuracy vs Loss over Epochs">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={performanceHistory} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="epoch" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="#10b981" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="#ef4444" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line yAxisId="left" type="monotone" dataKey="accuracy" name="Accuracy" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line yAxisId="right" type="monotone" dataKey="loss" name="Loss" stroke="#ef4444" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Inference Latency" subtitle="Avg vs P99 Latency (ms)">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={inferenceLatency} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorAvg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorP99" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="time" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="step" dataKey="p99" name="P99 Latency" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorP99)" />
                <Area type="step" dataKey="latency" name="Avg Latency" stroke="#06b6d4" fillOpacity={1} fill="url(#colorAvg)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Model Registry" subtitle="Catálogo versionado e status de deploy" className="xl:col-span-2">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80">
                <tr>
                  <th className="px-4 py-3 font-medium">Model Name</th>
                  <th className="px-4 py-3 font-medium">Version</th>
                  <th className="px-4 py-3 font-medium">F1 Score</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { name: "churn-predictor-xgb", ver: "v2.4.1", score: "0.89", status: "Production" },
                  { name: "intent-classifier-bert", ver: "v1.2.0", score: "0.92", status: "Production" },
                  { name: "lead-scorer-rf", ver: "v3.0.0-rc1", score: "0.85", status: "Staging" },
                  { name: "support-router-llm", ver: "v1.0.5", score: "0.78", status: "Archived" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.name}</td>
                    <td className="px-4 py-3 font-mono text-xs">{row.ver}</td>
                    <td className="px-4 py-3 text-cyber-cyan">{row.score}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        row.status === 'Production' ? 'bg-emerald-500/10 text-emerald-400' : 
                        row.status === 'Staging' ? 'bg-amber-500/10 text-amber-400' : 
                        'bg-white/10 text-white/60'
                      }`}>
                        {row.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <button className="text-cyber-cyan hover:underline text-xs">View Details</button>
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



