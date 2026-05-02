import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";

type RiskLevel = "SAFE" | "SUSPICIOUS" | "HIGH_RISK";

const CONFIG = {
  SAFE:       { label: "Safe",      icon: ShieldCheck, cls: "text-emerald-400 bg-emerald-400/10 border-emerald-400/25" },
  SUSPICIOUS: { label: "Suspicious",icon: ShieldAlert, cls: "text-amber-400 bg-amber-400/10 border-amber-400/25" },
  HIGH_RISK:  { label: "High Risk", icon: ShieldX,     cls: "text-red-400 bg-red-400/10 border-red-400/25" },
};

const SIZES = {
  sm: "text-xs px-2.5 py-1 gap-1",
  md: "text-sm px-3 py-1.5 gap-1.5",
  lg: "text-base px-4 py-2 gap-2",
};

const ICON_SIZES = { sm: 12, md: 14, lg: 18 };

export default function RiskBadge({
  level, score, size = "md",
}: {
  level: RiskLevel; score?: number; size?: "sm" | "md" | "lg";
}) {
  const { label, icon: Icon, cls } = CONFIG[level] || CONFIG.SUSPICIOUS;
  return (
    <span className={`inline-flex items-center font-semibold border rounded-full ${cls} ${SIZES[size]}`}>
      <Icon size={ICON_SIZES[size]} />
      {label}
      {score !== undefined && (
        <span className="opacity-60 font-normal">· {score}/100</span>
      )}
    </span>
  );
}
