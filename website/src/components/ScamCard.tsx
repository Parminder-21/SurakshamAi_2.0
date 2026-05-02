import { Users, Clock, ExternalLink, Shield } from "lucide-react";
import type { NewsFeedItem } from "@/lib/api";

const SEVERITY_CONFIG = {
  HIGH:   { badge: "text-red-400 bg-red-400/10 border-red-400/20",       dot: "bg-red-400",    label: "HIGH RISK",  bar: "bg-red-500" },
  MEDIUM: { badge: "text-amber-400 bg-amber-400/10 border-amber-400/20", dot: "bg-amber-400",  label: "MEDIUM",     bar: "bg-amber-500" },
  LOW:    { badge: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20", dot: "bg-emerald-400", label: "LOW", bar: "bg-emerald-500" },
};

// Scam type → emoji mapping
const SCAM_EMOJI: Record<string, string> = {
  "UPI / Payment Scam":           "💸",
  "Fake KYC / Bank Verification": "🏦",
  "Job Fraud":                    "💼",
  "Courier / Parcel Scam":        "📦",
  "Lottery / Prize Scam":         "🎰",
  "Digital Arrest Scam":          "⚖️",
  "Investment Scam":              "📈",
  "OTP Theft":                    "🔑",
  "Phishing URL":                 "🔗",
  "Electricity / Utility Scam":   "⚡",
  "Aadhaar / PAN Scam":           "🪪",
  "Ransomware / Malware":         "🦠",
  "Social Media Scam":            "📱",
  "Romance / Sextortion Scam":    "💔",
  "Banking Alert":                "🏛️",
  "Government Alert":             "🏛️",
  "Cyber Advisory":               "🛡️",
  "News Report":                  "📰",
};

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const days = Math.floor(diff / 86400000);
  const hours = Math.floor(diff / 3600000);
  const mins = Math.floor(diff / 60000);
  if (days > 30) return new Date(dateStr).toLocaleDateString("en-IN", { day: "numeric", month: "short" });
  if (days > 0) return `${days}d ago`;
  if (hours > 0) return `${hours}h ago`;
  if (mins > 0) return `${mins}m ago`;
  return "Just now";
}

export default function ScamCard({ item }: { item: NewsFeedItem }) {
  const cfg = SEVERITY_CONFIG[item.severity as keyof typeof SEVERITY_CONFIG] || SEVERITY_CONFIG.MEDIUM;
  const emoji = SCAM_EMOJI[item.scam_type] || "⚠️";

  return (
    <div className="card hover:border-slate-600 transition-all duration-200 hover:translate-y-[-2px] group flex flex-col">
      {/* Top row — severity + time */}
      <div className="flex items-center justify-between mb-3">
        <span className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${cfg.badge}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot} animate-pulse`} />
          {cfg.label}
        </span>
        <div className="flex items-center gap-1 text-xs text-slate-600">
          <Clock size={10} />
          {timeAgo(item.published_at)}
        </div>
      </div>

      {/* Scam type pill */}
      <div className="flex items-center gap-1.5 mb-2">
        <span className="text-base">{emoji}</span>
        <span className="text-xs text-slate-500 font-medium">{item.scam_type}</span>
      </div>

      {/* Title */}
      <h3 className="font-semibold text-white mb-2 leading-snug group-hover:text-blue-400 transition-colors line-clamp-2 text-[15px]">
        {item.title}
      </h3>

      {/* Summary — full, not truncated */}
      <p className="text-sm text-slate-400 mb-4 leading-relaxed flex-1">
        {item.summary}
      </p>

      {/* Tags */}
      {item.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {item.tags.slice(0, 4).map(tag => (
            <span key={tag} className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded-md border border-white/5">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-white/5">
        <div className="flex items-center gap-1.5 text-xs text-slate-500">
          <Users size={11} />
          <span className="font-medium text-slate-400">{item.report_count.toLocaleString()}</span>
          <span>reports</span>
        </div>
        <div className="flex items-center gap-2">
          {item.source_name && (
            <span className="text-xs text-slate-600 bg-slate-800/50 px-2 py-0.5 rounded border border-white/5">
              {item.source_name}
            </span>
          )}
          {item.source_url && (
            <a
              href={item.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-slate-600 hover:text-blue-400 transition-colors"
              title="View source"
            >
              <ExternalLink size={12} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
