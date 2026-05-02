"use client";

import { useState, useEffect, useMemo } from "react";
import Navbar from "@/components/Navbar";
import ScamCard from "@/components/ScamCard";
import { getNewsFeed, type NewsFeedItem } from "@/lib/api";
import {
  TrendingUp, AlertTriangle, Shield, RefreshCw,
  Search, Filter, Newspaper, Wifi, WifiOff,
  ChevronDown, ChevronUp, BarChart2
} from "lucide-react";

// All scam categories for filter
const SCAM_CATEGORIES = [
  "All Types",
  "Digital Arrest Scam",
  "UPI / Payment Scam",
  "Fake KYC / Bank Verification",
  "Investment Scam",
  "Job Fraud",
  "Courier / Parcel Scam",
  "Phishing URL",
  "OTP Theft",
  "Electricity / Utility Scam",
  "Aadhaar / PAN Scam",
  "Ransomware / Malware",
  "Social Media Scam",
  "Romance / Sextortion Scam",
  "Lottery / Prize Scam",
];

const SCAM_EMOJI: Record<string, string> = {
  "Digital Arrest Scam":          "⚖️",
  "UPI / Payment Scam":           "💸",
  "Fake KYC / Bank Verification": "🏦",
  "Investment Scam":              "📈",
  "Job Fraud":                    "💼",
  "Courier / Parcel Scam":        "📦",
  "Phishing URL":                 "🔗",
  "OTP Theft":                    "🔑",
  "Electricity / Utility Scam":   "⚡",
  "Aadhaar / PAN Scam":           "🪪",
  "Ransomware / Malware":         "🦠",
  "Social Media Scam":            "📱",
  "Romance / Sextortion Scam":    "💔",
  "Lottery / Prize Scam":         "🎰",
};

export default function ScamsPage() {
  const [items, setItems] = useState<NewsFeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState<"ALL" | "HIGH" | "MEDIUM">("ALL");
  const [categoryFilter, setCategoryFilter] = useState("All Types");
  const [showStats, setShowStats] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchNews = async (forceRefresh = false) => {
    try {
      setError(false);
      const url = forceRefresh
        ? `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/news-feed/?limit=50&refresh=true`
        : `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/news-feed/?limit=50`;
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error("Failed");
      const data = await res.json();
      setItems(data);
      setLastUpdated(new Date());
    } catch {
      setError(true);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => { fetchNews(); }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchNews(true);
  };

  // Filtered + searched items
  const filteredItems = useMemo(() => {
    let result = items;

    if (severityFilter !== "ALL") {
      result = result.filter(i => i.severity === severityFilter);
    }

    if (categoryFilter !== "All Types") {
      result = result.filter(i =>
        i.scam_type.toLowerCase().includes(categoryFilter.toLowerCase()) ||
        i.tags.some(t => t.toLowerCase().includes(categoryFilter.toLowerCase()))
      );
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(i =>
        i.title.toLowerCase().includes(q) ||
        i.summary.toLowerCase().includes(q) ||
        i.scam_type.toLowerCase().includes(q) ||
        i.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    return result;
  }, [items, severityFilter, categoryFilter, searchQuery]);

  const highRisk = filteredItems.filter(i => i.severity === "HIGH");
  const medRisk = filteredItems.filter(i => i.severity !== "HIGH");
  const totalReports = items.reduce((sum, i) => sum + i.report_count, 0);

  // Stats breakdown
  const scamTypeBreakdown = useMemo(() => {
    const map: Record<string, number> = {};
    items.forEach(i => {
      map[i.scam_type] = (map[i.scam_type] || 0) + 1;
    });
    return Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 8);
  }, [items]);

  const sources = useMemo(() => {
    return [...new Set(items.map(i => (i as any).source_name).filter(Boolean))];
  }, [items]);

  return (
    <>
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-10">

        {/* ── Header ─────────────────────────────────────────────────────── */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <div className="pulse-dot" />
            <span className="text-xs text-red-400 font-semibold uppercase tracking-wider">
              Live Threat Intelligence
            </span>
            {!loading && !error && (
              <span className="flex items-center gap-1 text-xs text-emerald-400 ml-2">
                <Wifi size={10} />
                {sources.length} sources active
              </span>
            )}
          </div>
          <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">Cyber Fraud News</h1>
              <p className="text-slate-400 max-w-2xl text-sm">
                Real-time intelligence scraped from CERT-In, RBI, Times of India, NDTV, India Today,
                Economic Times, The Hindu + curated India-specific scam alerts. Updated every 30 minutes.
              </p>
            </div>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-2 text-sm text-slate-400 hover:text-white border border-white/10 hover:border-white/20 px-4 py-2 rounded-lg transition-all shrink-0"
            >
              <RefreshCw size={14} className={refreshing ? "animate-spin" : ""} />
              {refreshing ? "Refreshing..." : "Refresh"}
            </button>
          </div>
          {lastUpdated && (
            <p className="text-xs text-slate-600 mt-2">
              Last updated: {lastUpdated.toLocaleTimeString("en-IN")}
            </p>
          )}
        </div>

        {/* ── Stats Bar ──────────────────────────────────────────────────── */}
        {!loading && items.length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <div className="card-sm text-center">
              <div className="text-2xl font-bold text-red-400">{items.filter(i => i.severity === "HIGH").length}</div>
              <div className="text-xs text-slate-500 mt-1">High Risk Alerts</div>
            </div>
            <div className="card-sm text-center">
              <div className="text-2xl font-bold text-white">{items.length}</div>
              <div className="text-xs text-slate-500 mt-1">Active Threats</div>
            </div>
            <div className="card-sm text-center">
              <div className="text-2xl font-bold text-amber-400">{totalReports.toLocaleString()}</div>
              <div className="text-xs text-slate-500 mt-1">Total Reports</div>
            </div>
            <div className="card-sm text-center">
              <div className="text-2xl font-bold text-blue-400">{sources.length || "8"}</div>
              <div className="text-xs text-slate-500 mt-1">News Sources</div>
            </div>
          </div>
        )}

        {/* ── Scam Type Breakdown (collapsible) ──────────────────────────── */}
        {!loading && items.length > 0 && (
          <div className="card mb-6">
            <button
              onClick={() => setShowStats(!showStats)}
              className="flex items-center justify-between w-full"
            >
              <div className="flex items-center gap-2">
                <BarChart2 size={16} className="text-blue-400" />
                <span className="font-semibold text-white text-sm">Scam Type Breakdown</span>
                <span className="text-xs text-slate-500">({scamTypeBreakdown.length} categories)</span>
              </div>
              {showStats ? <ChevronUp size={16} className="text-slate-500" /> : <ChevronDown size={16} className="text-slate-500" />}
            </button>

            {showStats && (
              <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2">
                {scamTypeBreakdown.map(([type, count]) => {
                  const pct = Math.round((count / items.length) * 100);
                  const emoji = SCAM_EMOJI[type] || "⚠️";
                  return (
                    <div key={type} className="flex items-center gap-3">
                      <span className="text-sm w-5">{emoji}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-slate-300 truncate">{type}</span>
                          <span className="text-slate-500 ml-2 shrink-0">{count} alerts</span>
                        </div>
                        <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-500 rounded-full transition-all"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* ── Filters ────────────────────────────────────────────────────── */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          {/* Search */}
          <div className="relative flex-1">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Search scams, keywords, tags..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="w-full bg-slate-900 border border-white/10 rounded-lg pl-9 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50"
            />
          </div>

          {/* Severity filter */}
          <div className="flex gap-2">
            {(["ALL", "HIGH", "MEDIUM"] as const).map(s => (
              <button
                key={s}
                onClick={() => setSeverityFilter(s)}
                className={`px-3 py-2 rounded-lg text-xs font-semibold border transition-all ${
                  severityFilter === s
                    ? s === "HIGH"
                      ? "bg-red-500/20 text-red-400 border-red-500/30"
                      : s === "MEDIUM"
                      ? "bg-amber-500/20 text-amber-400 border-amber-500/30"
                      : "bg-blue-500/20 text-blue-400 border-blue-500/30"
                    : "bg-transparent text-slate-500 border-white/10 hover:border-white/20"
                }`}
              >
                {s === "ALL" ? "All" : s === "HIGH" ? "🔴 High" : "🟡 Medium"}
              </button>
            ))}
          </div>
        </div>

        {/* Category filter pills */}
        <div className="flex flex-wrap gap-2 mb-8">
          {SCAM_CATEGORIES.map(cat => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                categoryFilter === cat
                  ? "bg-blue-500/20 text-blue-400 border-blue-500/30"
                  : "bg-transparent text-slate-500 border-white/10 hover:border-white/20 hover:text-slate-300"
              }`}
            >
              {SCAM_EMOJI[cat] || ""} {cat}
            </button>
          ))}
        </div>

        {/* ── Loading ─────────────────────────────────────────────────────── */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 bg-slate-800 rounded w-24 mb-3" />
                <div className="h-5 bg-slate-800 rounded w-full mb-2" />
                <div className="h-5 bg-slate-800 rounded w-3/4 mb-4" />
                <div className="h-16 bg-slate-800 rounded mb-4" />
                <div className="h-3 bg-slate-800 rounded w-1/2" />
              </div>
            ))}
          </div>
        )}

        {/* ── Error ───────────────────────────────────────────────────────── */}
        {!loading && error && (
          <div className="card border-red-500/20 bg-red-500/5 text-center py-12">
            <WifiOff size={32} className="text-red-400 mx-auto mb-3" />
            <p className="text-white font-semibold mb-1">Could not connect to backend</p>
            <p className="text-slate-400 text-sm mb-4">Make sure the backend is running at localhost:8000</p>
            <button onClick={() => fetchNews()} className="btn-primary text-sm py-2 px-4">
              Try Again
            </button>
          </div>
        )}

        {/* ── Results ─────────────────────────────────────────────────────── */}
        {!loading && !error && (
          <>
            {/* Result count */}
            {(searchQuery || severityFilter !== "ALL" || categoryFilter !== "All Types") && (
              <p className="text-sm text-slate-500 mb-4">
                Showing <span className="text-white font-medium">{filteredItems.length}</span> of {items.length} alerts
                {searchQuery && <> matching "<span className="text-blue-400">{searchQuery}</span>"</>}
              </p>
            )}

            {/* High risk section */}
            {highRisk.length > 0 && (
              <div className="mb-10">
                <div className="flex items-center gap-2 mb-4">
                  <AlertTriangle size={16} className="text-red-400" />
                  <h2 className="text-lg font-semibold text-white">High Risk Alerts</h2>
                  <span className="text-xs bg-red-500/10 text-red-400 border border-red-500/20 px-2 py-0.5 rounded-full">
                    {highRisk.length} active
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {highRisk.map(item => <ScamCard key={item.id} item={item} />)}
                </div>
              </div>
            )}

            {/* Medium/trending section */}
            {medRisk.length > 0 && (
              <div className="mb-10">
                <div className="flex items-center gap-2 mb-4">
                  <TrendingUp size={16} className="text-amber-400" />
                  <h2 className="text-lg font-semibold text-white">Trending Threats</h2>
                  <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded-full">
                    {medRisk.length} alerts
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {medRisk.map(item => <ScamCard key={item.id} item={item} />)}
                </div>
              </div>
            )}

            {/* No results */}
            {filteredItems.length === 0 && (
              <div className="card text-center py-16">
                <Shield size={40} className="text-slate-600 mx-auto mb-4" />
                <p className="text-slate-400 mb-2 font-medium">No alerts match your filters</p>
                <button
                  onClick={() => { setSearchQuery(""); setSeverityFilter("ALL"); setCategoryFilter("All Types"); }}
                  className="text-sm text-blue-400 hover:underline"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </>
        )}

        {/* ── Sources Info ─────────────────────────────────────────────────── */}
        {!loading && sources.length > 0 && (
          <div className="card border-slate-700/50 mb-6">
            <div className="flex items-center gap-2 mb-3">
              <Newspaper size={14} className="text-slate-400" />
              <span className="text-sm font-semibold text-slate-300">Active News Sources</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {sources.map(src => (
                <span key={src} className="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded-md border border-white/5">
                  {src}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ── Report CTA ───────────────────────────────────────────────────── */}
        <div className="card border-blue-500/20 bg-blue-500/5">
          <div className="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
            <AlertTriangle size={24} className="text-blue-400 shrink-0" />
            <div className="flex-1">
              <h3 className="font-semibold text-white mb-1">Received a scam message?</h3>
              <p className="text-sm text-slate-400">
                Report it to help protect others. Your submission is anonymized and helps train our AI model.
              </p>
            </div>
            <a href="/report" className="btn-primary text-sm py-2.5 px-5 shrink-0">
              Report Scam →
            </a>
          </div>
        </div>

      </main>
    </>
  );
}
