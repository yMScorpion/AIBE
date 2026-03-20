"use client";

import { Toaster } from "sonner";

export function AppToaster() {
  return (
    <Toaster
      theme="dark"
      position="bottom-right"
      toastOptions={{
        style: {
          background: "rgba(12,12,18,0.9)",
          border: "1px solid hsl(240 5% 12%)",
          backdropFilter: "blur(20px)",
        },
      }}
    />
  );
}
