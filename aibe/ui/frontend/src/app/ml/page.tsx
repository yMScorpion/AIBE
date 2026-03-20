"use client";

import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, Legend, LineChart, Line, BarChart, Bar, PieChart, Pie, Cell } from "recharts";
import { BrainCircuit, AlertCircle, Database, CheckCircle2, Activity, ArrowRight } from "lucide-react";

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

const gpuUsageData = [
  { time: "00:00", memory: 45, compute: 60 },
  { time: "04:00", memory: 55, compute: 75 },
  { time: "08:00", memory: 85, compute: 95 },
  { time: "12:00", memory: 90, compute: 98 },
  { time: "16:00", memory: 70, compute: 85 },
  { time: "20:00", memory: 50, compute: 65 },
];

const canaryData = [
  { name: "V1 (Stable)", value: 85 },
  { name: "V2 (Canary)", value: 15 },
];
const canaryCOLORS = ['#3b82f6', '#10b981'];

const modelImpactData = [
  { model: "Churn Pred", value: 125000, cost: 15000 },
  { model: "Lead Scorer", value: 85000, cost: 8000 },
  { model: "Support Bot", value: 45000, cost: 12000 },
  { model: "Rec Engine", value: 210000, cost: 35000 },
];

export default function MlPage() {
  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <PageHero
        eyebrow="Tier 7 • AI / ML Department"
        title="Model Intelligence & MLOps"
        subtitle="Data pipelines, model training, and production inference managed by Cipher, Tensor, Neural, and Optimus."
      />
      <StatGrid
        stats={[
          { label: "Models in Prod", value: "14", icon: <Database size={20} /> },
          { label: "Active Training", value: "3", tone: "good", icon: <BrainCircuit size={20} /> },
          { label: "Data Drift Alerts", value: "1", tone: "warn", icon: <AlertCircle size={20} /> },
          { label: "Feature Store Quality", value: "99.8%", tone: "good", icon: <CheckCircle2 size={20} /> },
        ]}
      />

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* Loss/Accuracy Live Chart */}
        <Panel title="Neural Training Curves" subtitle="Real-time fine-tuning status (Loss vs Accuracy)" className="xl:col-span-8">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={performanceHistory} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="epoch" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="#10b981" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="#ef4444" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Line yAxisId="left" type="monotone" dataKey="accuracy" name="Accuracy" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line yAxisId="right" type="monotone" dataKey="loss" name="Loss" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Data Drift Gauge */}
        <Panel title="Tensor Data Drift Alert" subtitle="Input distribution shift detection" className="xl:col-span-4">
          <div className="h-[300px] w-full mt-4 flex flex-col items-center justify-center">
            <div className="relative flex items-center justify-center">
              <svg className="w-48 h-24" viewBox="0 0 100 50">
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#27272a" strokeWidth="12" strokeLinecap="round" />
                <path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="#f59e0b" strokeWidth="12" strokeLinecap="round" strokeDasharray="125" strokeDashoffset="80" className="transition-all duration-1000" />
              </svg>
              <div className="absolute bottom-0 flex flex-col items-center">
                <span className="text-3xl font-bold text-white">0.14</span>
                <span className="text-xs text-amber-400 uppercase tracking-wider mt-1">Warning</span>
              </div>
            </div>
            <div className="mt-8 text-center text-xs text-muted-foreground max-w-[220px]">
              Drift detected in feature <span className="text-white">user_engagement_score</span>. Retraining pipeline scheduled.
            </div>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* GPU Usage */}
        <Panel title="GPU Cluster Utilization" subtitle="Compute and Memory allocation" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={gpuUsageData} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorComp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorMem" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="time" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Area type="monotone" dataKey="compute" name="Compute %" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorComp)" />
                <Area type="monotone" dataKey="memory" name="Memory %" stroke="#0ea5e9" fillOpacity={1} fill="url(#colorMem)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        {/* Model Impact */}
        <Panel title="Model Business Impact" subtitle="Value generated vs Inference/Training cost" className="xl:col-span-6">
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={modelImpactData} layout="vertical" margin={{ top: 10, right: 20, left: 30, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" horizontal={false} />
                <XAxis type="number" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(v) => `$${v/1000}k`} />
                <YAxis dataKey="model" type="category" stroke="#a1a1aa" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  cursor={{ fill: '#27272a', opacity: 0.4 }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(val: any, name: any) => [`$${val.toLocaleString()}`, name]}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="value" name="Value Added ($)" fill="#10b981" radius={[0, 4, 4, 0]} />
                <Bar dataKey="cost" name="Cost ($)" fill="#ef4444" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-12">
        {/* DAG Data Pipeline */}
        <Panel title="Tensor Data Pipeline DAG" subtitle="ETL execution status" className="xl:col-span-8">
          <div className="h-[250px] w-full mt-4 flex items-center justify-center p-6 bg-black/20 rounded-xl border border-white/5 overflow-x-auto">
            <div className="flex items-center gap-4 min-w-max">
              <div className="flex flex-col gap-4">
                <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-sm font-medium flex items-center gap-2"><CheckCircle2 size={16} /> Extract DB</div>
                <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg text-sm font-medium flex items-center gap-2"><CheckCircle2 size={16} /> API Ingest</div>
              </div>
              <ArrowRight className="text-muted-foreground" />
              <div className="px-6 py-4 bg-cyber-cyan/10 border border-cyber-cyan/30 text-cyber-cyan rounded-lg text-sm font-bold flex items-center gap-2 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                <Activity size={18} className="animate-pulse" /> Transform & Clean
              </div>
              <ArrowRight className="text-muted-foreground" />
              <div className="flex flex-col gap-4">
                <div className="px-4 py-2 bg-white/5 border border-white/10 text-muted-foreground rounded-lg text-sm font-medium flex items-center gap-2">Feature Eng</div>
                <div className="px-4 py-2 bg-white/5 border border-white/10 text-muted-foreground rounded-lg text-sm font-medium flex items-center gap-2">Vector Embeddings</div>
              </div>
              <ArrowRight className="text-muted-foreground" />
              <div className="px-4 py-2 bg-white/5 border border-white/10 text-muted-foreground rounded-lg text-sm font-medium flex items-center gap-2"><Database size={16} /> Feature Store</div>
            </div>
          </div>
        </Panel>

        {/* Canary Release */}
        <Panel title="Optimus Canary Traffic" subtitle="Inference routing distribution" className="xl:col-span-4">
          <div className="h-[250px] w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={canaryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {canaryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={canaryCOLORS[index % canaryCOLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [`${value}%`, 'Traffic']}
                />
                <Legend iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </section>

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
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

        <Panel title="Cipher Experiment Leaderboard" subtitle="A/B Test metrics ranking">
          <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden mt-4 h-[300px] overflow-y-auto pr-2 scrollbar-hide">
            <table className="w-full text-left text-sm text-muted-foreground">
              <thead className="bg-white/5 text-white/80 sticky top-0">
                <tr>
                  <th className="px-4 py-3 font-medium">Experiment ID</th>
                  <th className="px-4 py-3 font-medium">Model</th>
                  <th className="px-4 py-3 font-medium">Lift (%)</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {[
                  { id: "EXP-842", model: "XGBoost v3", lift: "+12.4%", status: "Winner" },
                  { id: "EXP-841", model: "RandomForest v2", lift: "+5.1%", status: "Completed" },
                  { id: "EXP-845", model: "NeuralNet L4", lift: "+2.8%", status: "Running" },
                  { id: "EXP-840", model: "LogisticReg", lift: "-1.2%", status: "Discarded" },
                  { id: "EXP-839", model: "BERT-Tiny", lift: "-4.5%", status: "Discarded" },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3 font-medium text-white">{row.id}</td>
                    <td className="px-4 py-3">{row.model}</td>
                    <td className={`px-4 py-3 font-bold ${row.lift.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}`}>{row.lift}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded-full text-[10px] uppercase font-bold tracking-wider ${
                        row.status === 'Winner' ? 'bg-amber-500/20 text-amber-400' : 
                        row.status === 'Running' ? 'bg-cyber-cyan/20 text-cyber-cyan' : 
                        row.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-400' :
                        'bg-white/5 text-muted-foreground'
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
      </section>
    </main>
  );
}



