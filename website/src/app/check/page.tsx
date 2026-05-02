"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import RiskBadge from "@/components/RiskBadge";
import { analyzeMessage, analyzeURL, type AnalysisResult } from "@/lib/api";
import {
  Shield, AlertTriangle, CheckCircle, XCircle,
  Loader2, Link2, MessageSquare, Phone,
  Lock, ChevronDown, ChevronUp, Fingerprint
} from "lucide-react";

type Tab = "message" | "url" | "call";

const SAMPLE_MESSAGES = [
  { label: "Fake KYC", text: "URGENT: Your SBI account will be blocked! Update KYC at http://sbi-kyc-update.xyz and pay Rs.1 via UPI. Share OTP to verify." },
  { label: "Job Fraud", text: "Work from home job! Earn Rs.5000/day doing simple tasks. Pay Rs.500 registration fee to start. WhatsApp: 9876543210" },
  { label: "Lottery Scam", text: "Congratulations! Your number won Rs.25 Lakh in KBC Lucky Draw. Contact Mr. Amitabh office: 9876543210. Claim within 24 hours." },
];

export default function CheckPage() {
  const [tab, setTab] = useState<Tab>("message");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [urlResult, setUrlResult] = useState<any>(null);
  const [error, setError] = useState("");
  const [showEvidence, setShowEvidence] = useState(false);

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    setUrlResult(null);
    setShowEvidence(false);
    try {
      if (tab === "url") {
        setUrlResult(await analyzeURL(input));
      } else {
        setResult(await analyzeMessage(input, tab === "call" ? "en" : "en"));
      }
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Analysis failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const riskBg: Record<string, string> = {
    SAFE:       "border-emerald-500/30 bg-emerald-500/5",
    SUSPICIOUS: "border-amber-500/30 bg-amber-500/5",
    HIGH_RISK:  "border-red-500/30 bg-red-500/5",
  };

  const riskGlow: Record<string, string> = {
    SAFE: "glow-green", SUSPICIOUS: "", HIGH_RISK: "glow-red",
  };

  const authColor: Record<string, string> = {
    VERIFIED: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
    LIKELY:   "text-blue-400 bg-blue-400/10 border-blue-400/20",
    UNCERTAIN:"text-amber-400 bg-amber-400/10 border-amber-400/20",
  };

  return (
    <>
      <Navbar />
      <main className="max-w-3xl mx-auto px-4 py-12">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Fraud Detector</h1>
          <p className="text-slate-400">
            Paste any suspicious message, URL, or call summary for instant AI analysis.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-5 p-1 bg-slate-900 rounded-xl border border-white/5">
          {([
            { id: "message", label: "SMS / Chat", icon: MessageSquare },
            { id: "url",     label: "URL / Link",  icon: Link2 },
            { id: "call",    label: "Call Summary", icon: Phone },
          ] as { id: Tab; label: string; icon: any }[]).map((t) => (
            <button
              key={t.id}
              onClick={() => { setTab(t.id); setInput(""); setResult(null); setUrlResult(null); setError(""); }}
              className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-medium transition-all ${
                tab === t.id
                  ? "bg-blue-600 text-white shadow-lg"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <t.icon size={14} />
              {t.label}
            </button>
          ))}
        </div>

        {/* Sample messages */}
        {tab === "message" && (
          <div className="flex flex-wrap gap-2 mb-4">
            <span className="text-xs text-slate-500 self-center">Try sample:</span>
            {SAMPLE_MESSAGES.map((s) => (
              <button
                key={s.label}
                onClick={() => setInput(s.text)}
                className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-white/5 transition-colors"
              >
                {s.label}
              </button>
            ))}
          </div>
        )}

        {/* Input area */}
        <div className="card mb-5">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.ctrlKey && e.key === "Enter") handleAnalyze(); }}
            placeholder={
              tab === "message" ? "Paste suspicious SMS, WhatsApp message, or email here..." :
              tab === "url"     ? "Paste suspicious URL (e.g. https://sbi-kyc-update.xyz)..." :
                                  "Describe the suspicious call in detail..."
            }
            rows={tab === "url" ? 3 : 6}
            className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none text-sm leading-relaxed"
          />
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center gap-1.5 text-xs text-slate-500">
              <Lock size={11} />
              PAN, Aadhaar, phone masked before analysis
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-600 hidden sm:block">Ctrl+Enter</span>
              <button
                onClick={handleAnalyze}
                disabled={loading || !input.trim()}
                className="btn-primary text-sm py-2.5 px-5"
              >
                {loading
                  ? <><Loader2 size={14} className="animate-spin" /> Analyzing...</>
                  : <><Shield size={14} /> Analyze</>
                }
              </button>
            </div>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="card border-red-500/30 bg-red-500/5 text-red-400 text-sm mb-5 flex items-center gap-2">
            <AlertTriangle size={14} className="shrink-0" />
            {error}
          </div>
        )}

        {/* ── Message / Call Result ─────────────────────────────────────── */}
        {result && (
          <div className={`card border ${riskBg[result.risk_level]} ${riskGlow[result.risk_level]} mb-5`}>

            {/* Top row */}
            <div className="flex items-start justify-between gap-3 mb-5">
              <div>
                <RiskBadge level={result.risk_level} score={result.risk_score} size="lg" />
                <p className="text-xs text-slate-500 mt-1.5">{result.scam_type}</p>
              </div>
              {result.explainability && (
                <span className={`text-xs font-semibold px-2.5 py-1 rounded-full border ${authColor[result.explainability.authenticity_label] || authColor.UNCERTAIN}`}>
                  <Fingerprint size={10} className="inline mr-1" />
                  {result.explainability.authenticity_label} · {Math.round((result.explainability.authenticity_score || 0) * 100)}%
                </span>
              )}
            </div>

            {/* Score bars */}
            <div className="grid grid-cols-2 gap-2.5 mb-5">
              {[
                { label: "Urgency",          val: result.score_breakdown.urgency_score },
                { label: "Authority",        val: result.score_breakdown.authority_impersonation_score },
                { label: "Payment Pressure", val: result.score_breakdown.payment_pressure_score },
                { label: "Deception",        val: result.score_breakdown.deception_fear_score },
              ].map((s) => (
                <div key={s.label} className="bg-slate-900 rounded-xl p-3 border border-white/5">
                  <div className="flex justify-between text-xs mb-1.5">
                    <span className="text-slate-400">{s.label}</span>
                    <span className="text-white font-semibold">{s.val}/25</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-700 ${
                        s.val >= 20 ? "bg-red-500" : s.val >= 12 ? "bg-amber-500" : "bg-blue-500"
                      }`}
                      style={{ width: `${(s.val / 25) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>

            {/* AI Summary */}
            {result.explainability?.decision_summary && (
              <div className="bg-slate-900/60 rounded-xl p-4 mb-4 border border-white/5">
                <p className="text-sm text-slate-300 leading-relaxed">
                  {result.explainability.decision_summary}
                </p>
                {result.explainability.verdicts_agree && (
                  <div className="flex items-center gap-1.5 mt-2 text-xs text-emerald-400">
                    <CheckCircle size={11} />
                    Keyword scorer and AI both agree on this verdict
                  </div>
                )}
              </div>
            )}

            {/* Why risky */}
            {result.why_risky && (
              <div className="mb-4">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Why it&apos;s risky</h3>
                <p className="text-sm text-slate-300 leading-relaxed">{result.why_risky}</p>
              </div>
            )}

            {/* Red flags */}
            {result.red_flags.length > 0 && (
              <div className="mb-4">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Red Flags</h3>
                <div className="space-y-1.5">
                  {result.red_flags.map((f) => (
                    <div key={f} className="flex items-center gap-2 text-sm text-red-400">
                      <AlertTriangle size={12} className="shrink-0" />
                      {f}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div className="bg-red-500/5 border border-red-500/15 rounded-xl p-4">
                <h3 className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">Do NOT</h3>
                <div className="space-y-2">
                  {result.what_not_to_do.map((a) => (
                    <div key={a} className="flex items-start gap-2 text-sm text-slate-400">
                      <XCircle size={13} className="shrink-0 mt-0.5 text-red-500" />
                      {a}
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-emerald-500/5 border border-emerald-500/15 rounded-xl p-4">
                <h3 className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3">What to Do</h3>
                <div className="space-y-2">
                  {result.what_to_do.map((a) => (
                    <div key={a} className="flex items-start gap-2 text-sm text-slate-400">
                      <CheckCircle size={13} className="shrink-0 mt-0.5 text-emerald-500" />
                      {a}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Evidence chain (collapsible) */}
            {result.explainability?.triggered_rules && result.explainability.triggered_rules.length > 0 && (
              <div>
                <button
                  onClick={() => setShowEvidence(!showEvidence)}
                  className="flex items-center gap-2 text-xs text-slate-500 hover:text-slate-300 transition-colors w-full"
                >
                  {showEvidence ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
                  {showEvidence ? "Hide" : "Show"} evidence chain ({result.explainability.triggered_rules.length} signals)
                </button>
                {showEvidence && (
                  <div className="mt-3 space-y-1.5">
                    {result.explainability.triggered_rules.map((r, i) => (
                      <div key={i} className="text-xs text-slate-500 bg-slate-900 rounded-lg px-3 py-2 border border-white/5 font-mono">
                        {r}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* ── URL Result ────────────────────────────────────────────────── */}
        {urlResult && (
          <div className={`card border ${riskBg[urlResult.risk_level] || riskBg.SUSPICIOUS} mb-5`}>
            <div className="flex items-center justify-between mb-4">
              <RiskBadge level={urlResult.risk_level} score={urlResult.risk_score} size="lg" />
              {urlResult.is_brand_impersonation && (
                <span className="text-xs text-red-400 bg-red-400/10 border border-red-400/20 px-2.5 py-1 rounded-full">
                  Impersonates {urlResult.impersonated_brand}
                </span>
              )}
            </div>
            <p className="text-sm text-slate-300 mb-4 leading-relaxed">{urlResult.recommendation}</p>
            {urlResult.threats?.length > 0 && (
              <div className="space-y-2">
                <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Threats Detected</h3>
                {urlResult.threats.map((t: string) => (
                  <div key={t} className="flex items-center gap-2 text-sm text-red-400">
                    <AlertTriangle size={12} className="shrink-0" />
                    {t}
                  </div>
                ))}
              </div>
            )}
            {urlResult.domain_age_days != null && (
              <p className="text-xs text-slate-600 mt-3">Domain age: {urlResult.domain_age_days} days</p>
            )}
          </div>
        )}

      </main>
    </>
  );
}
