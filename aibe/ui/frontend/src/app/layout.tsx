import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";
import { Toaster } from "sonner";

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
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrains.variable} font-sans`}>
        <Providers>
          {/* Ambient background */}
          <div className="fixed inset-0 -z-10">
            <div className="absolute inset-0 bg-[#06060a]" />
            <div className="absolute inset-0 bg-cyber-mesh bg-mesh opacity-30" />
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-gradient-radial from-cyber-purple/[0.07] via-transparent to-transparent" />
            <div className="absolute bottom-0 right-0 w-[600px] h-[400px] bg-gradient-radial from-cyber-cyan/[0.04] via-transparent to-transparent" />
          </div>
          {children}
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
        </Providers>
      </body>
    </html>
  );
}