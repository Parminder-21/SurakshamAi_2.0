import Link from "next/link";
import { Shield, Zap, Eye, Globe, MessageSquare, Phone, ArrowRight, TrendingUp, Users, CheckCircle, Lock, AlertTriangle } from "lucide-react";
import Navbar from "@/components/Navbar";
import ScamCard from "@/components/ScamCard";
import { getNewsFeed, type NewsFeedItem } from "@/lib/api";

const STATS = [
  { value: "97.6%", label: "F1 Score", sub: "on Indian fraud dataset" },
  { value: "100%", label: "Recall Rate", sub: "no scam missed" },
  { value: "8", label: "Scam Types", sub: "India-specific" },
  { value: "< 2s", label: "Response Time", sub: "powered by Groq" },
];

const FEATURES = [
  {
    icon: MessageSquare,
    title: "Message Scanner",
    desc: "Paste any SMS, WhatsApp, or email. Get instant risk score with evidence.",
    href: "/check",
    color: "from-blue-500/20 to-blue-600/5",
    iconColor: "text-blue-400",
    border: "border-blue-500/20",
  },
  {
    icon: Globe,
    title: "URL Checker",
    desc: "Detect phishing links, brand impersonation, and malicious domains.",
    href: "/check",
    color: "from-violet-500/20 to-violet-600/5",
    iconColor: "text-violet-400",
    border: "border-violet-500/20",
  },
  {
    icon: Phone,
    title: "Call Analyzer",
    desc: "Describe a suspicious call. AI identifies scam patterns instantly.",
    href: "/check",
    color: "from-emerald-500/20 to-emerald-600/5",
    iconColor: "text-emerald-400",
    border: "border-emerald-500/20",
  },
  {
    icon: Eye,
    title: "Cyber News",
    desc: "Live feed of trending scams targeting Indians. Stay one step ahead.",
    href: "/scams",
    color: "from-amber-500/20 to-amber-600/5",
    iconColor: "text-amber-400",
    border: "border-amber-500/20",
  },
];

const SCAM_TYPES = [
  { label: "Fake KYC", color: "text-blue-400 bg-blue-400/10 border-blue-400/20" },
  { label: "UPI Scams", color: "text-yellow-400 bg-yellow-400/10 border-yellow-400/20" },
  { label: "Job Fraud", color: "text-green-400 bg-green-400/10 border-green-400/20" },
  { label: "Courier Scams", color: "text-orange-400 bg-orange-400/10 border-orange-400/20" },
  { label: "Lottery Scams", color: "text-purple-400 bg-purple-400/10 border-purple-400/20" },
  { label: "Authority Impersonation", color: "text-red-400 bg-red-400/10 border-red-400/20" },
  { label: "Electricity Bill Scams", color: "text-cyan-400 bg-cyan-400/10 border-cyan-400/20" },
  { label: "OTP Theft", color: "text-pink-400 bg-pink-400/10 border-pink-400/20" },
];

export default async function HomePage() {
  let newsItems: NewsFeedItem[] = [];
  try { newsItems = await getNewsFeed(3); } catch { /* backend may not be running */ }

  return (
    <>
      <Navbar />
      <main className="overflow-hidden">

        {/* ── Hero ─────────────────────────────────────────────────────────── */}
        <section className="relative max-w-7xl mx-auto px-4 pt-20 pb-24 text-center">
          {/* Background glow */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />

          <div className="relative">
            <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium px-4 py-2 rounded-full mb-8">
              <div className="pulse-dot" />
              Live Threat Detection · Powered by Groq LLaMA 3.3-70b
            </div>

            <h1 className="text-5xl md:text-7xl font-black text-white mb-6 leading-[1.05] tracking-tight">
              India&apos;s AI Shield
              <br />
              Against <span className="gradient-text-danger">Digital Fraud</span>
            </h1>

            <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
              Suraksham AI detects UPI scams, fake KYC, phishing URLs, and courier fraud
              in real-time — with explainable AI and 97.6% accuracy.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Link href="/check" className="btn-primary text-base py-3.5 px-8">
                <Shield size={18} />
                Check a Message Free
              </Link>
              <Link href="/scams" className="btn-secondary text-base py-3.5 px-8">
                <TrendingUp size={18} />
                View Cyber News
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
              {STATS.map((s) => (
                <div key={s.label} className="card-sm text-center">
                  <div className="text-2xl font-black gradient-text mb-1">{s.value}</div>
                  <div className="text-sm font-semibold text-white">{s.label}</div>
                  <div className="text-xs text-slate-500 mt-0.5">{s.sub}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Features ─────────────────────────────────────────────────────── */}
        <section className="max-w-7xl mx-auto px-4 py-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Complete Cyber Safety Suite
            </h2>
            <p className="text-slate-400 max-w-xl mx-auto">
              Every tool you need to stay safe from India&apos;s most common digital frauds
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {FEATURES.map((f) => (
              <Link
                key={f.title}
                href={f.href}
                className={`card border ${f.border} bg-gradient-to-b ${f.color} hover:scale-[1.02] transition-all duration-200 group`}
              >
                <div className={`w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center mb-4 ${f.iconColor}`}>
                  <f.icon size={20} />
                </div>
                <h3 className="font-semibold text-white mb-2 group-hover:text-blue-400 transition-colors">
                  {f.title}
                </h3>
                <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
                <div className="flex items-center gap-1 mt-4 text-xs text-slate-500 group-hover:text-blue-400 transition-colors">
                  Try now <ArrowRight size={12} />
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* ── Live Cyber News ───────────────────────────────────────────────── */}
        {newsItems.length > 0 && (
          <section className="max-w-7xl mx-auto px-4 py-20">
            <div className="flex items-center justify-between mb-8">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <div className="pulse-dot" />
                  <span className="text-xs text-red-400 font-semibold uppercase tracking-wider">Live Threats</span>
                </div>
                <h2 className="text-3xl font-bold text-white">Latest Cyber Threats</h2>
              </div>
              <Link href="/scams" className="btn-secondary text-sm py-2 px-4">
                View All <ArrowRight size={14} />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {newsItems.map((item) => (
                <ScamCard key={item.id} item={item} />
              ))}
            </div>
          </section>
        )}

        {/* ── Scam Types ────────────────────────────────────────────────────── */}
        <section className="max-w-7xl mx-auto px-4 py-20">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-white mb-3">8 Scam Types Detected</h2>
            <p className="text-slate-400">Trained specifically on Indian fraud patterns</p>
          </div>
          <div className="flex flex-wrap justify-center gap-3">
            {SCAM_TYPES.map((s) => (
              <span key={s.label} className={`border px-4 py-2 rounded-full text-sm font-medium ${s.color}`}>
                {s.label}
              </span>
            ))}
          </div>
        </section>

        {/* ── How it works ─────────────────────────────────────────────────── */}
        <section className="max-w-7xl mx-auto px-4 py-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-3">How It Works</h2>
            <p className="text-slate-400">Multi-agent AI pipeline for maximum accuracy</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { step: "01", title: "Privacy Scrub", desc: "PAN, Aadhaar, phone numbers masked before any API call", icon: Lock },
              { step: "02", title: "Risk Scoring", desc: "4-dimension keyword analysis: urgency, authority, payment, deception", icon: AlertTriangle },
              { step: "03", title: "AI Classification", desc: "Groq LLaMA 3.3-70b classifies scam type with 95%+ confidence", icon: Zap },
              { step: "04", title: "Explainability", desc: "Evidence chain shows exactly which patterns triggered the alert", icon: CheckCircle },
            ].map((item) => (
              <div key={item.step} className="card relative overflow-hidden">
                <div className="absolute top-4 right-4 text-4xl font-black text-white/5">{item.step}</div>
                <item.icon size={20} className="text-blue-400 mb-3" />
                <h3 className="font-semibold text-white mb-2">{item.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── Privacy Banner ────────────────────────────────────────────────── */}
        <section className="max-w-7xl mx-auto px-4 py-10 pb-20">
          <div className="card border-blue-500/20 bg-gradient-to-r from-blue-500/5 to-violet-500/5">
            <div className="flex flex-col md:flex-row items-center gap-6 text-center md:text-left">
              <div className="w-14 h-14 rounded-2xl bg-blue-500/10 flex items-center justify-center shrink-0">
                <Lock size={24} className="text-blue-400" />
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-white mb-1">Privacy First, Always</h3>
                <p className="text-slate-400 text-sm leading-relaxed">
                  Your phone numbers, PAN card, Aadhaar, UPI IDs, and bank account numbers are
                  automatically masked <strong className="text-white">before</strong> any message
                  reaches our AI. We never store your original messages.
                </p>
              </div>
              <Link href="/check" className="btn-primary shrink-0">
                Try It Free
              </Link>
            </div>
          </div>
        </section>

        {/* ── Footer ───────────────────────────────────────────────────────── */}
        <footer className="border-t border-white/5 py-10">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
                  <Shield size={14} className="text-white" />
                </div>
                <span className="font-bold text-white">Suraksham AI</span>
                <span className="text-slate-600">·</span>
                <span className="text-slate-500 text-sm">Microsoft Agentic AI Hackathon</span>
              </div>
              <div className="flex items-center gap-6 text-sm text-slate-500">
                <Link href="/scams" className="hover:text-white transition-colors">Cyber News</Link>
                <Link href="/knowledge-base" className="hover:text-white transition-colors">Learn</Link>
                <Link href="/report" className="hover:text-white transition-colors">Report Scam</Link>
                <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  cybercrime.gov.in
                </a>
                <span className="text-red-400 font-semibold">Helpline: 1930</span>
              </div>
            </div>
          </div>
        </footer>

      </main>
    </>
  );
}
