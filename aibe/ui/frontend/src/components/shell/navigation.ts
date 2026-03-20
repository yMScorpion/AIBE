import {
  LayoutDashboard,
  Box,
  Users,
  Wrench,
  TrendingUp,
  Share2,
  ShieldAlert,
  Target,
  BrainCircuit,
  Dna,
  Landmark,
  Settings,
  Briefcase,
  Lightbulb
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface NavItem {
  href: string;
  label: string;
  shortLabel: string;
  icon: LucideIcon;
  badge?: string;
}

export const NAV_ITEMS: NavItem[] = [
  { href: "/", label: "Dashboard", shortLabel: "DB", icon: LayoutDashboard, badge: "Live" },
  { href: "/executive", label: "Executive", shortLabel: "EX", icon: Briefcase },
  { href: "/research", label: "Research", shortLabel: "RS", icon: Lightbulb },
  { href: "/office-3d", label: "Pixel Office", shortLabel: "2D", icon: Box, badge: "Live" },
  { href: "/meetings", label: "War Room", shortLabel: "WR", icon: Users },
  { href: "/product", label: "Builder View", shortLabel: "BV", icon: Wrench },
  { href: "/marketing", label: "Marketing", shortLabel: "MC", icon: TrendingUp },
  { href: "/social", label: "Social Studio", shortLabel: "SS", icon: Share2 },
  { href: "/security", label: "Security Ops", shortLabel: "SO", icon: ShieldAlert, badge: "Hot" },
  { href: "/sales", label: "Sales & CS", shortLabel: "SC", icon: Target },
  { href: "/ml", label: "AI/ML Lab", shortLabel: "ML", icon: BrainCircuit },
  { href: "/evolution", label: "Evolution Lab", shortLabel: "EL", icon: Dna },
  { href: "/finance", label: "Finance & Ops", shortLabel: "FO", icon: Landmark },
  { href: "/settings", label: "Settings", shortLabel: "ST", icon: Settings },
];
