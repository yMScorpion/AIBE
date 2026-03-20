const API_ORIGIN = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "";

export class ApiError extends Error {
  constructor(
    public status: number,
    public statusText: string,
    public body: unknown,
  ) {
    super(`${status} ${statusText}`);
    this.name = "ApiError";
  }
}

async function fetcher<T>(path: string, init?: RequestInit): Promise<T> {
  const url = API_ORIGIN ? `${API_ORIGIN}${path}` : path;
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    let body: unknown;
    try {
      body = await res.json();
    } catch {
      body = null;
    }
    throw new ApiError(res.status, res.statusText, body);
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

export const api = {
  agents: {
    list: (params?: { tier?: number; status?: string }) => {
      const q = new URLSearchParams();
      if (params?.tier != null) q.set("tier", String(params.tier));
      if (params?.status) q.set("status", params.status);
      return fetcher<AgentListResponse>(`/api/agents?${q}`);
    },
    get: (id: string) => fetcher<AgentDetailResponse>(`/api/agents/${id}`),
    restart: (id: string) => fetcher<{ restarted: boolean }>(`/api/agents/${id}/restart`, { method: "POST" }),
  },
  tasks: {
    list: (params?: { agent_id?: string; status?: string }) => {
      const q = new URLSearchParams();
      if (params?.agent_id) q.set("agent_id", params.agent_id);
      if (params?.status) q.set("status", params.status);
      return fetcher<TaskListResponse>(`/api/tasks?${q}`);
    },
    submit: (body: TaskSubmit) => fetcher<{ task_id: string; status: string }>("/api/tasks", { method: "POST", body: JSON.stringify(body) }),
    get: (id: string) => fetcher<TaskResponse>(`/api/tasks/${id}`),
  },
  meetings: {
    list: () => fetcher<MeetingListResponse>("/api/meetings"),
    create: (body: MeetingCreate) => fetcher<{ meeting_id: string }>("/api/meetings", { method: "POST", body: JSON.stringify(body) }),
    get: (id: string) => fetcher<MeetingResponse>(`/api/meetings/${id}`),
  },
  costs: {
    summary: () => fetcher<CostSummaryResponse>("/api/costs/summary"),
    history: (days?: number) => fetcher<CostHistoryResponse>(`/api/costs/history?days=${days || 7}`),
    agent: (id: string) => fetcher<AgentCostDetailResponse>(`/api/costs/agent/${id}`),
  },
  system: {
    status: () => fetcher<SystemStatusResponse>("/api/system/status"),
    boot: (body?: { tiers?: number[]; exclude_agents?: string[] }) =>
      fetcher("/api/system/boot", { method: "POST", body: JSON.stringify(body || {}) }),
    shutdown: () => fetcher("/api/system/shutdown", { method: "POST" }),
    health: () => fetcher<{ status: string; version: string }>("/api/health"),
  },
};

// Types
export interface AgentResponse {
  agent_id: string;
  agent_name: string;
  tier: number;
  status: string;
  uptime_seconds: number;
  tasks_completed: number;
  error_count: number;
}
export interface AgentDetailResponse extends AgentResponse {
  escalation_target: string | null;
  daily_budget_usd: number;
}
export interface AgentListResponse { agents: AgentResponse[]; total: number }
export interface TaskSubmit { target_agent: string; title: string; description?: string; priority?: number }
export interface TaskResponse { task_id: string; source: string; target: string; title: string; description: string; priority: number; status: string; created_at: string; completed_at: string | null; output_data: Record<string, unknown> | null; error_message: string | null }
export interface TaskListResponse { tasks: TaskResponse[]; total: number }
export interface MeetingCreate { topic: string; participants: string[]; max_rounds?: number; meeting_type?: string }
export interface MeetingResponse { meeting_id: string; topic: string; participants: string[]; meeting_type: string; status: string; rounds_completed: number; transcript: Record<string, unknown>[]; result: Record<string, unknown> | null; created_at: string; completed_at: string | null }
export interface MeetingListResponse { meetings: MeetingResponse[]; total: number }
export interface CostSummaryResponse { total_spent_usd: number; total_budget_usd: number; period: string; by_agent: { agent_id: string; spent_usd: number; budget_usd: number; utilization_pct: number }[]; by_tier: { tier: number; tier_name: string; spent_usd: number; agent_count: number }[] }
export interface CostHistoryResponse { days: number; history: { date: string; spent_usd: number }[] }
export interface AgentCostDetailResponse { agent_id: string; total_spent_usd: number; budget_usd: number; by_model: { model: string; calls: number; tokens_in: number; tokens_out: number; cost_usd: number }[] }
export interface SystemStatusResponse { running: boolean; mode: string; total_agents: number; active_agents: number; agents_by_status: Record<string, number>; uptime_seconds: number; boot_time: string | null }
