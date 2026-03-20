import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "../globals.css";
import { Providers } from "@/components/providers";
import { ErrorBoundary } from "@/components/error-boundary";
import { AppShell } from "@/components/shell/app-shell";
import { AppToaster } from "@/components/app-toaster";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
});

export const metadata: Metadata = {
  title: "AIBE — AI Business Engine",
  description: "Real-time dashboard for 40 autonomous AI agents",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${jetbrains.variable} font-sans`}>
        <Providers>
          <div className="fixed inset-0 -z-10">
            <div className="absolute inset-0 bg-[#06060a]" />
            <div className="absolute inset-0 bg-cyber-mesh bg-mesh opacity-30" />
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-gradient-radial from-cyber-purple/[0.07] via-transparent to-transparent" />
            <div className="absolute bottom-0 right-0 w-[600px] h-[400px] bg-gradient-radial from-cyber-cyan/[0.04] via-transparent to-transparent" />
          </div>
          <ErrorBoundary>
            <AppShell>{children}</AppShell>
          </ErrorBoundary>
          <AppToaster />
        </Providers>
      </body>
    </html>
  );
}
