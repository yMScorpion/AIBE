"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_ITEMS } from "@/components/shell/navigation";

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={`glass-heavy sticky top-0 flex h-screen flex-col border-r border-border/80 transition-all duration-300 ${
        collapsed ? "w-[84px]" : "w-[270px]"
      }`}
    >
      <div className="flex items-center justify-between border-b border-border/70 px-4 py-4">
        <div className={`transition-opacity ${collapsed ? "opacity-0" : "opacity-100"}`}>
          <p className="text-xs uppercase tracking-[0.22em] text-cyber-cyan">AIBE v2.0</p>
          <p className="text-lg font-semibold">Operations Grid</p>
        </div>
        <button
          type="button"
          onClick={onToggle}
          className="rounded-lg border border-border bg-secondary px-2 py-1 text-xs font-medium hover:bg-accent"
          aria-label="Alternar navegação"
        >
          {collapsed ? "›" : "‹"}
        </button>
      </div>

      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`group flex items-center gap-3 rounded-xl border px-3 py-2.5 transition ${
                active
                  ? "border-cyber-purple/50 bg-cyber-purple/10 text-white"
                  : "border-transparent bg-transparent text-muted-foreground hover:border-border hover:bg-secondary hover:text-foreground"
              }`}
            >
              <span
                className={`flex h-8 w-8 items-center justify-center rounded-md text-xs font-semibold ${
                  active ? "bg-cyber-purple/25 text-cyber-cyan" : "bg-secondary"
                }`}
              >
                {item.shortLabel}
              </span>
              {!collapsed ? (
                <span className="flex min-w-0 flex-1 items-center justify-between gap-2">
                  <span className="truncate text-sm font-medium">{item.label}</span>
                  {item.badge ? (
                    <span className="rounded-full border border-cyber-cyan/30 bg-cyber-cyan/10 px-2 py-0.5 text-[10px] uppercase tracking-wide text-cyber-cyan">
                      {item.badge}
                    </span>
                  ) : null}
                </span>
              ) : null}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border/70 p-3">
        <div className="rounded-xl border border-border/70 bg-secondary/50 p-3">
          {!collapsed ? (
            <>
              <p className="text-xs uppercase tracking-wide text-muted-foreground">Fleet Runtime</p>
              <p className="mt-1 text-sm font-medium text-cyber-green">Stable · Synced</p>
            </>
          ) : (
            <div className="mx-auto h-2 w-2 rounded-full bg-cyber-green" aria-hidden="true" />
          )}
        </div>
      </div>
    </aside>
  );
}
