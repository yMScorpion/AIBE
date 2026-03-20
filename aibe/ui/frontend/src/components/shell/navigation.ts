export interface NavItem {
  href: string;
  label: string;
  shortLabel: string;
  badge?: string;
}

export const NAV_ITEMS: NavItem[] = [
  { href: "/", label: "Command Center", shortLabel: "CC", badge: "Live" },
  { href: "/office-3d", label: "Pixel Office 2D", shortLabel: "2D", badge: "Live" },
  { href: "/meetings", label: "War Room", shortLabel: "WR" },
  { href: "/product", label: "Builder View", shortLabel: "BV" },
  { href: "/marketing", label: "Marketing Command", shortLabel: "MC" },
  { href: "/social", label: "Social Studio", shortLabel: "SS" },
  { href: "/security", label: "Security Ops", shortLabel: "SO", badge: "Hot" },
  { href: "/sales", label: "Sales & CS", shortLabel: "SC" },
  { href: "/ml", label: "AI/ML Lab", shortLabel: "ML" },
  { href: "/evolution", label: "Evolution Lab", shortLabel: "EL" },
  { href: "/finance", label: "Finance & Ops", shortLabel: "FO" },
  { href: "/settings", label: "Settings", shortLabel: "ST" },
];
