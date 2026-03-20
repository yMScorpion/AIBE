import { create } from "zustand";
import { api, type AgentResponse } from "@/lib/api";

interface AgentState {
  agents: AgentResponse[];
  spendToday: number;
  pendingTasks: number;
  loading: boolean;
  refreshAgents: () => Promise<void>;
  refreshCosts: () => Promise<void>;
}

export const useAgentStore = create<AgentState>((set) => ({
  agents: [],
  spendToday: 0,
  pendingTasks: 0,
  loading: false,
  refreshAgents: async () => {
    set({ loading: true });
    try {
      const data = await api.agents.list();
      const pendingTasks = data.agents.reduce((acc, agent) => acc + Math.max(agent.tasks_completed - agent.error_count, 0), 0);
      set({ agents: data.agents, pendingTasks });
    } catch {
      set({ agents: [] });
    } finally {
      set({ loading: false });
    }
  },
  refreshCosts: async () => {
    try {
      const summary = await api.costs.summary();
      set({ spendToday: summary.total_spent_usd || 0 });
    } catch {
      set({ spendToday: 0 });
    }
  },
}));
