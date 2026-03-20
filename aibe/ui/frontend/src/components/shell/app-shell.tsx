"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "@/components/shell/sidebar";
import { SystemStatusBar } from "@/components/shell/system-status-bar";
import { NotificationPanel } from "@/components/shell/notification-panel";
import { useAgentStore } from "../../stores/agent-store";
import { useMeetingStore } from "../../stores/meeting-store";
import { useNotificationStore } from "../../stores/notification-store";

export function AppShell({ children }: { children: React.ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [notificationOpen, setNotificationOpen] = useState(false);
  const refreshAgents = useAgentStore((s) => s.refreshAgents);
  const refreshCosts = useAgentStore((s) => s.refreshCosts);
  const refreshMeetings = useMeetingStore((s) => s.refreshMeetings);
  const hydrateFromEvents = useNotificationStore((s) => s.hydrateFromEvents);

  useEffect(() => {
    void refreshAgents();
    void refreshCosts();
    void refreshMeetings();
    const timer = setInterval(() => {
      void refreshAgents();
      void refreshCosts();
    }, 30_000);
    return () => clearInterval(timer);
  }, [refreshAgents, refreshCosts, refreshMeetings]);

  useEffect(() => hydrateFromEvents(), [hydrateFromEvents]);

  return (
    <div className="relative flex min-h-screen">
      <div className="pl-4 pt-4 pb-4">
        <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed((v) => !v)} />
      </div>
      <div className="min-w-0 flex-1 px-4 pb-6 pt-4 md:px-6">
        <SystemStatusBar onOpenNotifications={() => setNotificationOpen(true)} />
        {children}
      </div>
      <NotificationPanel open={notificationOpen} onClose={() => setNotificationOpen(false)} />
    </div>
  );
}
