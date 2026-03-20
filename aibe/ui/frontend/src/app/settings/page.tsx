"use client";

import { useState } from "react";
import { PageHero, Panel, StatGrid } from "@/components/page-kit";
import { Save, RefreshCw, Server, Shield, DollarSign, Cpu } from "lucide-react";

export default function SettingsPage() {
  const [isSaving, setIsSaving] = useState(false);
  const [budgetLimits, setBudgetLimits] = useState({
    dailyLlmUsd: 50.00,
    dailyAdsCapUsd: 0.00, // Initial budget 0 for organic traffic
    monthlyContractorUsd: 500.00,
  });

  const [toggles, setToggles] = useState({
    humanReviewMode: false,
    securityBlockOnHigh: true,
    autoScaling: true,
  });

  const [routingRules] = useState([
    { id: 1, context: "Research", priority: "High", llm: "openrouter/free" },
    { id: 2, context: "Executive", priority: "Critical", llm: "claude-3-opus" },
    { id: 3, context: "Marketing", priority: "Medium", llm: "gpt-4-turbo" },
  ]);

  const handleSave = () => {
    setIsSaving(true);
    setTimeout(() => {
      setIsSaving(false);
      alert("Configurações salvas com sucesso!");
    }, 800);
  };

  return (
    <main className="mx-auto max-w-[1680px] pb-8">
      <div className="flex items-start justify-between mb-2">
        <PageHero
          eyebrow="Settings"
          title="Governança global de políticas, orçamento e roteamento"
          subtitle="Painel de configuração central para limites, toggles e trilhas de auditoria."
        />
        <div className="pt-4 pr-4">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="flex items-center gap-2 rounded-xl bg-cyber-purple/20 px-6 py-3 text-sm font-semibold text-cyber-purple border border-cyber-purple/40 hover:bg-cyber-purple/30 transition-all"
          >
            {isSaving ? <RefreshCw size={18} className="animate-spin" /> : <Save size={18} />}
            {isSaving ? "Salvando..." : "Salvar Alterações"}
          </button>
        </div>
      </div>

      <StatGrid
        stats={[
          { label: "Routing Rules", value: String(routingRules.length) },
          { label: "Budget Caps", value: "3 Active" },
          { label: "Agent Toggles", value: "3 Active" },
          { label: "System Status", value: "Optimal", tone: "good" },
        ]}
      />

      <section className="mt-6 grid grid-cols-1 gap-6 xl:grid-cols-2">
        {/* Routing Table Editor */}
        <Panel title="Routing Table Editor" subtitle="Regras de roteamento por contexto e prioridade">
          <div className="space-y-4">
            <div className="rounded-xl border border-white/5 bg-black/20 overflow-hidden">
              <table className="w-full text-left text-sm text-muted-foreground">
                <thead className="bg-white/5 text-white/80">
                  <tr>
                    <th className="px-4 py-3 font-medium">Context</th>
                    <th className="px-4 py-3 font-medium">Priority</th>
                    <th className="px-4 py-3 font-medium">LLM Provider</th>
                    <th className="px-4 py-3 font-medium">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {routingRules.map((rule) => (
                    <tr key={rule.id} className="hover:bg-white/5 transition-colors">
                      <td className="px-4 py-3 font-medium text-white">{rule.context}</td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-1 rounded-full text-xs ${rule.priority === 'Critical' ? 'bg-rose-500/10 text-rose-400' : rule.priority === 'High' ? 'bg-amber-500/10 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'}`}>
                          {rule.priority}
                        </span>
                      </td>
                      <td className="px-4 py-3">{rule.llm}</td>
                      <td className="px-4 py-3">
                        <button className="text-cyber-cyan hover:underline text-xs">Edit</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <button className="w-full rounded-xl border border-dashed border-white/20 py-3 text-sm text-muted-foreground hover:bg-white/5 hover:text-white transition-colors">
              + Adicionar Nova Regra
            </button>
          </div>
        </Panel>

        {/* Budget Limits */}
        <Panel title="Budget Limits" subtitle="Limites diários e mensais por categoria">
          <div className="space-y-5 rounded-xl border border-white/5 bg-black/20 p-5">
            <div className="space-y-2">
              <label className="flex items-center justify-between text-sm font-medium text-white">
                <span className="flex items-center gap-2"><Cpu size={16} className="text-cyber-cyan"/> Daily LLM Budget (USD)</span>
                <span className="text-cyber-cyan font-mono">${budgetLimits.dailyLlmUsd.toFixed(2)}</span>
              </label>
              <input 
                type="range" 
                min="10" max="500" step="10" 
                value={budgetLimits.dailyLlmUsd}
                onChange={(e) => setBudgetLimits({...budgetLimits, dailyLlmUsd: Number(e.target.value)})}
                className="w-full accent-cyber-cyan"
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center justify-between text-sm font-medium text-white">
                <span className="flex items-center gap-2"><DollarSign size={16} className="text-emerald-400"/> Daily Ads Cap (USD)</span>
                <span className="text-emerald-400 font-mono">${budgetLimits.dailyAdsCapUsd.toFixed(2)}</span>
              </label>
              <input 
                type="range" 
                min="0" max="1000" step="50" 
                value={budgetLimits.dailyAdsCapUsd}
                onChange={(e) => setBudgetLimits({...budgetLimits, dailyAdsCapUsd: Number(e.target.value)})}
                className="w-full accent-emerald-400"
              />
            </div>

            <div className="space-y-2">
              <label className="flex items-center justify-between text-sm font-medium text-white">
                <span className="flex items-center gap-2"><Server size={16} className="text-cyber-purple"/> Monthly Contractor (USD)</span>
                <span className="text-cyber-purple font-mono">${budgetLimits.monthlyContractorUsd.toFixed(2)}</span>
              </label>
              <input 
                type="range" 
                min="100" max="5000" step="100" 
                value={budgetLimits.monthlyContractorUsd}
                onChange={(e) => setBudgetLimits({...budgetLimits, monthlyContractorUsd: Number(e.target.value)})}
                className="w-full accent-cyber-purple"
              />
            </div>
          </div>
        </Panel>

        {/* Agent Toggles */}
        <Panel title="System & Agent Toggles" subtitle="Habilitação granular de capacidades operacionais">
          <div className="space-y-3">
            {Object.entries(toggles).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between rounded-xl border border-white/5 bg-black/20 p-4 transition-colors hover:bg-white/5">
                <div>
                  <p className="text-sm font-medium text-white capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    {key === 'humanReviewMode' ? 'Exige aprovação humana para decisões críticas.' : 
                     key === 'securityBlockOnHigh' ? 'Bloqueia operações se risco de segurança for alto.' : 
                     'Aumenta instâncias de agentes sob alta demanda.'}
                  </p>
                </div>
                <button 
                  onClick={() => setToggles({...toggles, [key]: !value})}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${value ? 'bg-cyber-cyan' : 'bg-white/20'}`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${value ? 'translate-x-6' : 'translate-x-1'}`} />
                </button>
              </div>
            ))}
          </div>
        </Panel>

        {/* Audit Logs */}
        <Panel title="Security & Compliance" subtitle="Trilhas de auditoria e retenção">
          <div className="space-y-4 rounded-xl border border-white/5 bg-black/20 p-5">
            <div className="flex items-start gap-4">
              <div className="rounded-full bg-rose-500/20 p-3 text-rose-400">
                <Shield size={24} />
              </div>
              <div>
                <h4 className="text-sm font-medium text-white">Cryptographic Signature</h4>
                <p className="text-xs text-muted-foreground mt-1 mb-3">Todas as decisões executivas são assinadas e armazenadas de forma imutável.</p>
                <div className="flex gap-2">
                  <button className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs font-medium text-white hover:bg-white/10 transition-colors">
                    Export Logs
                  </button>
                  <button className="rounded-lg border border-rose-500/20 bg-rose-500/10 px-3 py-1.5 text-xs font-medium text-rose-400 hover:bg-rose-500/20 transition-colors">
                    Clear Cache
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Panel>
      </section>
    </main>
  );
}



