"use client";
import { useState } from "react";
import Navbar from "@/components/Navbar";
import { reportScam } from "@/lib/api";
import { Send, CheckCircle, Loader2 } from "lucide-react";

const SCAM_TYPES = [
  "Fake KYC / Bank Verification",
  "UPI / Payment Scam",
  "Job Fraud",
  "Courier / Parcel Scam",
  "Lottery / Prize Scam",
  "Authority Impersonation",
  "Electricity / Utility Bill Scam",
  "OTP Theft",
  "Other",
];

export default function ReportPage() {
  const [content, setContent] = useState("");
  const [scamType, setScamType] = useState("");
  const [note, setNote] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!content.trim()) return;
    setLoading(true);
    setError("");

    try {
      await reportScam(content, scamType || undefined, note || undefined);
      setSuccess(true);
      setContent("");
      setScamType("");
      setNote("");
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Submission failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <main className="max-w-2xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-white mb-2">Report a Scam</h1>
        <p className="text-gray-400 mb-8">
          Help protect others by reporting scam messages or URLs you&apos;ve received.
          Your submission is anonymized and reviewed before being added to our database.
        </p>

        {success ? (
          <div className="card border-green-500/30 bg-green-500/5 text-center py-12">
            <CheckCircle className="text-green-400 mx-auto mb-3" size={40} />
            <h2 className="text-xl font-bold text-white mb-2">Thank you!</h2>
            <p className="text-gray-400 mb-6">
              Your report has been submitted. It will help protect others from this scam.
            </p>
            <button onClick={() => setSuccess(false)} className="btn-secondary">
              Report Another
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="card space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Scam Message or URL <span className="text-red-400">*</span>
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste the scam message or URL here..."
                rows={5}
                required
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none text-sm"
              />
              <p className="text-xs text-gray-500 mt-1">
                🔒 Phone numbers, PAN, and Aadhaar are automatically removed before storage.
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Scam Type (optional)
              </label>
              <select
                value={scamType}
                onChange={(e) => setScamType(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-gray-300 focus:outline-none focus:border-blue-500 text-sm"
              >
                <option value="">Select a type...</option>
                {SCAM_TYPES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Additional Notes (optional)
              </label>
              <textarea
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Any additional context about this scam..."
                rows={3}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:border-blue-500 resize-none text-sm"
              />
            </div>

            {error && (
              <p className="text-sm text-red-400">{error}</p>
            )}

            <button
              type="submit"
              disabled={loading || !content.trim()}
              className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
              {loading ? "Submitting..." : "Submit Report"}
            </button>
          </form>
        )}
      </main>
    </>
  );
}
