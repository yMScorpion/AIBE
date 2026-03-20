"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "@/components/shell/navigation";
import { ChevronLeft, ChevronRight, Hexagon } from "lucide-react";

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={`glass sticky top-4 flex h-[calc(100vh-32px)] flex-col rounded-3xl border border-white/10 transition-all duration-300 z-50 ${
        collapsed ? "w-[84px]" : "w-[260px]"
      }`}
    >
      <div className="flex items-center justify-between px-6 py-6 mt-2">
        <div className={`flex items-center gap-3 transition-opacity ${collapsed ? "opacity-0 hidden" : "opacity-100"}`}>
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br from-cyber-purple to-cyber-cyan text-white shadow-lg">
            <Hexagon size={18} className="fill-current" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">AIBE</span>
        </div>
        <button
          type="button"
          onClick={onToggle}
          className={`flex h-8 w-8 items-center justify-center rounded-full bg-white/5 text-muted-foreground transition-all hover:bg-white/10 hover:text-white ${
            collapsed ? "mx-auto" : ""
          }`}
          aria-label="Toggle Sidebar"
        >
          {collapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      <nav className="flex-1 space-y-2 overflow-y-auto px-4 py-4 scrollbar-hide">
        <div className={`mb-4 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground/60 ${collapsed ? "text-center" : ""}`}>
          {collapsed ? "•••" : "Menu"}
        </div>
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`group flex items-center gap-3 rounded-2xl px-3 py-3 transition-all duration-200 ${
                active
                  ? "bg-gradient-to-r from-cyber-purple/20 to-transparent text-white border border-cyber-purple/20 shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]"
                  : "text-muted-foreground hover:bg-white/5 hover:text-white"
              }`}
            >
              <span
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition-all duration-200 ${
                  active 
                    ? "bg-cyber-purple text-white shadow-[0_0_15px_rgba(124,58,237,0.4)]" 
                    : "bg-transparent group-hover:bg-white/5"
                }`}
              >
                <Icon size={20} strokeWidth={active ? 2.5 : 2} />
              </span>
              {!collapsed ? (
                <span className="flex min-w-0 flex-1 items-center justify-between gap-2">
                  <span className={`truncate font-medium ${active ? "text-white" : ""}`}>{item.label}</span>
                  {item.badge ? (
                    <span className="rounded-full bg-cyber-cyan/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-cyber-cyan border border-cyber-cyan/20">
                      {item.badge}
                    </span>
                  ) : null}
                </span>
              ) : null}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 mt-auto">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-white/5 to-white/0 border border-white/5 p-4 backdrop-blur-xl">
          <div className="absolute -right-4 -top-4 h-16 w-16 rounded-full bg-cyber-purple/20 blur-2xl" />
          <div className="absolute -bottom-4 -left-4 h-16 w-16 rounded-full bg-cyber-cyan/20 blur-2xl" />
          {!collapsed ? (
            <div className="relative z-10">
              <p className="text-xs font-semibold text-white">System Status</p>
              <div className="mt-2 flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
                </span>
                <span className="text-xs font-medium text-emerald-400">All Systems Operational</span>
              </div>
            </div>
          ) : (
            <div className="relative z-10 flex justify-center">
              <span className="relative flex h-3 w-3">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex h-3 w-3 rounded-full bg-emerald-500"></span>
              </span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
