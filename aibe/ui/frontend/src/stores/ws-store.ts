import { create } from "zustand";

export interface WsEvent {
  event: string;
  timestamp: string;
  data: Record<string, unknown>;
}

interface WsState {
  connected: boolean;
  events: WsEvent[];
  agentStatuses: Record<string, string>;
  connect: () => void;
  disconnect: () => void;
}

export const useWsStore = create<WsState>((set, get) => {
  let ws: WebSocket | null = null;
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

  function doConnect() {
    const url =
      typeof window !== "undefined" && window.location.hostname === "localhost"
        ? "ws://localhost:8000/ws"
        : `ws://${typeof window !== "undefined" ? window.location.host : ""}/ws`;

    try {
      ws = new WebSocket(url);

      ws.onopen = () => {
        set({ connected: true });
        ws?.send(JSON.stringify({ type: "subscribe", topics: ["*"] }));
      };

      ws.onmessage = (e) => {
        try {
          const evt: WsEvent = JSON.parse(e.data);
          if (evt.event === "pong") return;

          set((s) => {
            const events = [evt, ...s.events].slice(0, 200);
            const agentStatuses = { ...s.agentStatuses };
            if (evt.event === "agent_status_changed" && evt.data.agent_id) {
              agentStatuses[evt.data.agent_id as string] = evt.data.new_status as string;
            }
            if (evt.event === "system_heartbeat" && evt.data.statuses) {
              Object.assign(agentStatuses, evt.data.statuses);
            }
            return { events, agentStatuses };
          });
        } catch {}
      };

      ws.onclose = () => {
        set({ connected: false });
        reconnectTimer = setTimeout(doConnect, 3000);
      };

      ws.onerror = () => {
        set({ connected: false });
      };
    } catch {
      set({ connected: false });
      reconnectTimer = setTimeout(doConnect, 5000);
    }
  }

  return {
    connected: false,
    events: [],
    agentStatuses: {},
    connect: () => doConnect(),
    disconnect: () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      ws?.close();
      set({ connected: false });
    },
  };
});