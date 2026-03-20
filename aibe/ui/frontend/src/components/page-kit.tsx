import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function PageHero({
  eyebrow,
  title,
  subtitle,
  cta,
  onCtaClick,
}: {
  eyebrow: string;
  title: string;
  subtitle: string;
  cta?: { label: string; href: string };
  onCtaClick?: () => void;
}) {
  return (
    <section className="relative overflow-hidden mb-6 rounded-[32px] bg-gradient-to-br from-cyber-purple/20 via-black/40 to-black border border-white/10 p-8 md:p-12 shadow-2xl">
      <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-cyber-purple/30 blur-[80px]" />
      <div className="absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-cyber-cyan/20 blur-[80px]" />
      
      <div className="relative z-10 max-w-3xl">
        <div className="inline-flex items-center gap-2 rounded-full border border-cyber-cyan/30 bg-cyber-cyan/10 px-3 py-1 mb-4">
          <span className="flex h-2 w-2 rounded-full bg-cyber-cyan animate-pulse"></span>
          <p className="text-[11px] font-bold uppercase tracking-widest text-cyber-cyan">{eyebrow}</p>
        </div>
        
        <h1 className="text-4xl font-bold tracking-tight text-white md:text-5xl lg:text-6xl mb-4">
          {title}
        </h1>
        <p className="text-lg text-muted-foreground/90 mb-8 max-w-2xl leading-relaxed">
          {subtitle}
        </p>
        
        {cta ? (
          onCtaClick ? (
            <button
              onClick={onCtaClick}
              className="group inline-flex h-12 items-center justify-center gap-2 rounded-2xl bg-white px-8 text-sm font-semibold text-black transition-all hover:bg-white/90 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_40px_rgba(255,255,255,0.2)]"
            >
              {cta.label}
              <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
            </button>
          ) : (
            <Link
              href={cta.href}
              className="group inline-flex h-12 items-center justify-center gap-2 rounded-2xl bg-white px-8 text-sm font-semibold text-black transition-all hover:bg-white/90 hover:scale-[1.02] active:scale-[0.98] shadow-[0_0_40px_rgba(255,255,255,0.2)]"
            >
              {cta.label}
              <ArrowRight size={16} className="transition-transform group-hover:translate-x-1" />
            </Link>
          )
        ) : null}
      </div>
    </section>
  );
}

export function Panel({
  title,
  subtitle,
  children,
  className = "",
  action,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
  action?: React.ReactNode;
}) {
  return (
    <section className={`flex flex-col rounded-3xl border border-white/5 bg-card/50 backdrop-blur-xl p-6 shadow-sm transition-all hover:border-white/10 ${className}`}>
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-lg font-semibold text-white tracking-tight">{title}</h2>
          {subtitle ? <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p> : null}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div className="flex-1">{children}</div>
    </section>
  );
}

export function StatGrid({
  stats,
}: {
  stats: { label: string; value: string; trend?: string; trendUp?: boolean; icon?: React.ReactNode; tone?: "default" | "good" | "warn" | "hot" }[];
}) {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4 mb-6">
      {stats.map((stat) => (
        <article key={stat.label} className={`group relative overflow-hidden rounded-3xl border border-white/5 bg-card/40 p-6 transition-all hover:bg-card/60 hover:border-white/10 ${stat.tone === 'good' ? 'border-emerald-500/20' : stat.tone === 'warn' ? 'border-amber-500/20' : stat.tone === 'hot' ? 'border-rose-500/20' : ''}`}>
          <div className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-white/5 blur-2xl transition-all group-hover:bg-cyber-purple/10" />
          
          <div className="relative z-10 flex items-center justify-between mb-4">
            <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
            {stat.icon && <div className="text-muted-foreground/50">{stat.icon}</div>}
          </div>
          
          <div className="relative z-10 flex items-baseline gap-3">
            <p className="text-4xl font-bold tracking-tight text-white">{stat.value}</p>
            {stat.trend && (
              <span className={`text-xs font-semibold px-2 py-1 rounded-full ${stat.trendUp ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                {stat.trendUp ? '↑' : '↓'} {stat.trend}
              </span>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}
