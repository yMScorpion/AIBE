import Link from "next/link";

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
    <section className="glass-heavy mb-5 rounded-3xl border border-border/70 p-6 md:p-8">
      <p className="text-xs uppercase tracking-[0.24em] text-cyber-cyan">{eyebrow}</p>
      <h1 className="mt-2 text-2xl font-semibold leading-tight md:text-4xl">{title}</h1>
      <p className="mt-3 max-w-3xl text-sm text-muted-foreground md:text-base">{subtitle}</p>
      {cta ? (
        onCtaClick ? (
          <button
            onClick={onCtaClick}
            className="mt-5 inline-flex items-center rounded-xl border border-cyber-purple/40 bg-cyber-purple/20 px-4 py-2 text-sm font-medium text-white hover:bg-cyber-purple/30"
          >
            {cta.label}
          </button>
        ) : (
          <Link
            href={cta.href}
            className="mt-5 inline-flex items-center rounded-xl border border-cyber-purple/40 bg-cyber-purple/20 px-4 py-2 text-sm font-medium text-white hover:bg-cyber-purple/30"
          >
            {cta.label}
          </Link>
        )
      ) : null}
    </section>
  );
}

export function Panel({
  title,
  subtitle,
  children,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-border/80 bg-card/80 p-4 md:p-5">
      <h2 className="text-sm font-semibold md:text-base">{title}</h2>
      {subtitle ? <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p> : null}
      <div className="mt-4">{children}</div>
    </section>
  );
}

export function StatGrid({
  stats,
}: {
  stats: { label: string; value: string; tone?: "default" | "good" | "warn" | "hot" }[];
}) {
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => (
        <article key={stat.label} className={`rounded-2xl border p-4 ${toneClass(stat.tone)}`}>
          <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">{stat.label}</p>
          <p className="mt-2 text-2xl font-semibold">{stat.value}</p>
        </article>
      ))}
    </div>
  );
}

function toneClass(tone: "default" | "good" | "warn" | "hot" = "default") {
  if (tone === "good") return "border-emerald-500/25 bg-emerald-500/10";
  if (tone === "warn") return "border-amber-500/30 bg-amber-500/10";
  if (tone === "hot") return "border-rose-500/30 bg-rose-500/10";
  return "border-border/80 bg-card/80";
}
