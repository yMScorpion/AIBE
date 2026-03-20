"use client";

import { useMemo } from "react";
import { useWsStore } from "@/stores/ws-store";
import { useNotificationStore } from "../../stores/notification-store";

interface NotificationPanelProps {
  open: boolean;
  onClose: () => void;
}

export function NotificationPanel({ open, onClose }: NotificationPanelProps) {
  const wsEvents = useWsStore((s) => s.events);
  const notifications = useNotificationStore((s) => s.notifications);
  const dismiss = useNotificationStore((s) => s.dismiss);
  const hydrated = useMemo(() => {
    if (notifications.length > 0) {
      return notifications;
    }
    return wsEvents.slice(0, 20).map((event, index) => ({
      id: `${event.timestamp}-${index}`,
      title: event.event.replaceAll("_", " "),
      detail: JSON.stringify(event.data || {}),
      timestamp: event.timestamp,
      severity: "info" as const,
      read: false,
    }));
  }, [notifications, wsEvents]);

  return (
    <>
      {open ? <button type="button" className="fixed inset-0 z-30 bg-black/45" onClick={onClose} aria-label="Fechar notificações" /> : null}
      <aside
        className={`glass-heavy fixed right-0 top-0 z-40 h-screen w-full max-w-[420px] border-l border-border transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        aria-label="Painel de notificações"
      >
        <div className="flex items-center justify-between border-b border-border px-4 py-3">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-cyber-cyan">Notification Panel</p>
            <p className="text-lg font-semibold">Live Alerts & Events</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-lg border border-border bg-secondary px-2 py-1 text-sm hover:bg-accent">
            ✕
          </button>
        </div>
        <div className="h-[calc(100%-76px)] space-y-2 overflow-y-auto p-4">
          {hydrated.length === 0 ? <p className="rounded-xl bg-secondary p-3 text-sm text-muted-foreground">Nenhum alerta no momento.</p> : null}
          {hydrated.map((notification) => (
            <article key={notification.id} className="rounded-xl border border-border bg-secondary/80 p-3">
              <div className="mb-1 flex items-center justify-between gap-2">
                <p className="truncate text-sm font-semibold capitalize">{notification.title}</p>
                <button
                  type="button"
                  onClick={() => dismiss(notification.id)}
                  className="rounded border border-border px-1.5 py-0.5 text-[10px] uppercase tracking-wide text-muted-foreground hover:text-foreground"
                >
                  Dismiss
                </button>
              </div>
              <p className="line-clamp-3 text-xs text-muted-foreground">{notification.detail || "Evento recebido sem payload."}</p>
              <p className="mt-2 text-[11px] text-cyber-cyan">{new Date(notification.timestamp).toLocaleString()}</p>
            </article>
          ))}
        </div>
      </aside>
    </>
  );
}
