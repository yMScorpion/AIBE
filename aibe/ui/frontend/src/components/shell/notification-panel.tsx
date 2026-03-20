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
        className={`glass-heavy fixed right-0 top-0 z-40 h-screen w-full max-w-[420px] border-l border-white/10 transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        aria-label="Painel de notificações"
      >
        <div className="flex items-center justify-between border-b border-white/5 px-6 py-5 bg-black/40">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-widest text-cyber-cyan mb-1">Notification Panel</p>
            <p className="text-xl font-bold tracking-tight text-white">Live Alerts</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-full flex h-8 w-8 items-center justify-center border border-white/10 bg-white/5 text-muted-foreground transition-all hover:bg-white/10 hover:text-white">
            ✕
          </button>
        </div>
        <div className="h-[calc(100%-88px)] space-y-3 overflow-y-auto p-6 scrollbar-hide">
          {hydrated.length === 0 ? <p className="rounded-xl bg-black/20 border border-white/5 p-4 text-sm text-muted-foreground text-center">Nenhum alerta no momento.</p> : null}
          {hydrated.map((notification) => (
            <article key={notification.id} className="relative overflow-hidden rounded-2xl border border-white/5 bg-black/40 p-4 transition-all hover:border-white/10 hover:bg-black/60">
              <div className="absolute left-0 top-0 h-full w-1 bg-cyber-purple/50"></div>
              <div className="mb-2 flex items-center justify-between gap-2">
                <p className="truncate text-sm font-bold capitalize text-white">{notification.title}</p>
                <button
                  type="button"
                  onClick={() => dismiss(notification.id)}
                  className="rounded-md border border-white/10 bg-white/5 px-2 py-1 text-[10px] font-medium uppercase tracking-wide text-muted-foreground transition-all hover:bg-white/10 hover:text-white"
                >
                  Dismiss
                </button>
              </div>
              <p className="line-clamp-3 text-xs leading-relaxed text-muted-foreground">{notification.detail || "Evento recebido sem payload."}</p>
              <div className="mt-3 flex items-center gap-2">
                <span className="flex h-1.5 w-1.5 rounded-full bg-cyber-cyan"></span>
                <p className="text-[11px] font-medium text-cyber-cyan/80">{new Date(notification.timestamp).toLocaleString()}</p>
              </div>
            </article>
          ))}
        </div>
      </aside>
    </>
  );
}
