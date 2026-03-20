"use client";

import { useEffect } from "react";
import { ThemeProvider } from "next-themes";
import { useWsStore } from "@/stores/ws-store";

export function Providers({ children }: { children: React.ReactNode }) {
  const connect = useWsStore((s) => s.connect);
  const disconnect = useWsStore((s) => s.disconnect);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
      {children}
    </ThemeProvider>
  );
}
