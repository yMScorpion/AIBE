import { create } from "zustand";
import { useWsStore } from "@/stores/ws-store";

export interface UiNotification {
  id: string;
  title: string;
  detail: string;
  timestamp: string;
  severity: "info" | "warning" | "critical";
  read: boolean;
}

interface NotificationState {
  notifications: UiNotification[];
  hydrateFromEvents: () => void;
  dismiss: (id: string) => void;
}

function normalizeSeverity(eventType: string): UiNotification["severity"] {
  if (eventType.includes("security") || eventType.includes("error")) return "critical";
  if (eventType.includes("budget") || eventType.includes("degraded")) return "warning";
  return "info";
}

export const useNotificationStore = create<NotificationState>((set) => ({
  notifications: [],
  hydrateFromEvents: () => {
    const events = useWsStore.getState().events.slice(0, 30);
    const notifications = events.map((event, index) => ({
      id: `${event.timestamp}-${index}`,
      title: event.event.replaceAll("_", " "),
      detail: JSON.stringify(event.data || {}),
      timestamp: event.timestamp,
      severity: normalizeSeverity(event.event),
      read: false,
    }));
    set({ notifications });
  },
  dismiss: (id) => set((state) => ({ notifications: state.notifications.filter((item) => item.id !== id) })),
}));
