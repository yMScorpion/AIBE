import { create } from "zustand";

export interface WsEvent {
  event: string;
  timestamp: string;
  data: Record<string, unknown>;
}

function resolveWebSocketUrl(): string {
  if (typeof window === "undefined") {
    return "ws://localhost:8000/ws";
  }

  const explicitWsUrl = process.env.NEXT_PUBLIC_WS_URL?.trim();
  if (explicitWsUrl) {
    return explicitWsUrl;
  }

  const apiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (apiUrl && apiUrl.startsWith("http")) {
    const origin = apiUrl.replace(/\/$/, "");
    const wsOrigin = origin.startsWith("https://") ? origin.replace("https://", "wss://") : origin.replace("http://", "ws://");
    return `${wsOrigin}/ws`;
  }

  if (window.location.hostname === "localhost") {
    return "ws://localhost:8000/ws";
  }

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}/ws`;
}

interface WsState {
  connected: boolean;
  events: WsEvent[];
  agentStatuses: Record<string, string>;
  connect: () => void;
  disconnect: () => void;
}

export const useWsStore = create<WsState>((set) => {
  let ws: WebSocket | null = null;
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  let reconnectAttempt = 0;
  let manuallyDisconnected = false;
  const MAX_RECONNECT_DELAY = 30_000;

  function scheduleReconnect() {
    if (manuallyDisconnected) return;
    if (reconnectTimer) clearTimeout(reconnectTimer);
    const delay = Math.min(1_000 * 2 ** reconnectAttempt, MAX_RECONNECT_DELAY);
    reconnectAttempt += 1;
    reconnectTimer = setTimeout(doConnect, delay);
  }

  function doConnect() {
    manuallyDisconnected = false;
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    const url = resolveWebSocketUrl();

    try {
      ws = new WebSocket(url);

      ws.onopen = () => {
        reconnectAttempt = 0;
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
              const incoming = evt.data.statuses as Record<string, string>;
              let hasChanges = false;
              const nextStatuses: Record<string, string> = {};
              for (const [id, status] of Object.entries(incoming)) {
                nextStatuses[id] = status;
                if (s.agentStatuses[id] !== status) {
                  hasChanges = true;
                }
              }
              if (Object.keys(s.agentStatuses).length !== Object.keys(nextStatuses).length) {
                hasChanges = true;
              }
              if (!hasChanges) {
                return { events };
              }
              return { events, agentStatuses: nextStatuses };
            }
            return { events, agentStatuses };
          });
        } catch {}
      };

      ws.onclose = () => {
        set({ connected: false });
        ws = null;
        scheduleReconnect();
      };

      ws.onerror = () => {
        set({ connected: false });
        ws?.close();
      };
    } catch {
      set({ connected: false });
      scheduleReconnect();
    }
  }

  return {
    connected: false,
    events: [],
    agentStatuses: {},
    connect: () => doConnect(),
    disconnect: () => {
      manuallyDisconnected = true;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      reconnectTimer = null;
      ws?.close();
      ws = null;
      reconnectAttempt = 0;
      set({ connected: false });
    },
  };
});
