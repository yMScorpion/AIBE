"use client";

import { useEffect } from "react";
import { useWsStore } from "@/stores/ws-store";

export function Providers({ children }: { children: React.ReactNode }) {
  const connect = useWsStore((s) => s.connect);

  useEffect(() => {
    connect();
  }, [connect]);

  return <>{children}</>;
}