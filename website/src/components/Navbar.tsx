"use client";
import Link from "next/link";
import { Shield, Menu, X, AlertTriangle } from "lucide-react";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/check", label: "Check Now" },
  { href: "/scams", label: "Cyber News" },
  { href: "/knowledge-base", label: "Learn" },
  { href: "/report", label: "Report" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Alert ticker */}
      <div className="bg-red-950/60 border-b border-red-900/40 py-1.5 overflow-hidden">
        <div className="flex whitespace-nowrap ticker-inner">
          {[...Array(2)].map((_, i) => (
            <span key={i} className="flex items-center gap-6 px-4 text-xs text-red-300">
              <span className="flex items-center gap-1.5"><AlertTriangle size={10} className="text-red-400" /> NEW: FedEx Parcel Scam targeting Indians — Do NOT pay any clearance fee</span>
              <span className="text-red-600">•</span>
              <span className="flex items-center gap-1.5"><AlertTriangle size={10} className="text-red-400" /> ALERT: Fake SBI KYC messages circulating on WhatsApp</span>
              <span className="text-red-600">•</span>
              <span className="flex items-center gap-1.5"><AlertTriangle size={10} className="text-red-400" /> WARNING: UPI QR code refund scam — scanning QR sends money, not receives</span>
              <span className="text-red-600">•</span>
              <span className="flex items-center gap-1.5"><AlertTriangle size={10} className="text-red-400" /> TRAI impersonation calls on the rise — hang up immediately</span>
              <span className="text-red-600">•</span>
            </span>
          ))}
        </div>
      </div>

      {/* Main nav */}
      <nav className="sticky top-0 z-50 bg-[#020817]/95 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
              <Shield size={16} className="text-white" />
            </div>
            <div className="flex items-baseline gap-1">
              <span className="font-bold text-white text-lg">Suraksham</span>
              <span className="font-bold gradient-text text-lg">AI</span>
            </div>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className="px-4 py-2 text-sm text-slate-400 hover:text-white hover:bg-white/5 rounded-lg transition-all"
              >
                {l.label}
              </Link>
            ))}
          </div>

          {/* CTA */}
          <div className="hidden md:flex items-center gap-3">
            <Link href="/check" className="btn-primary text-sm py-2 px-4">
              <Shield size={14} />
              Check Message
            </Link>
          </div>

          {/* Mobile toggle */}
          <button
            className="md:hidden text-slate-400 hover:text-white p-2"
            onClick={() => setOpen(!open)}
            aria-label="Toggle menu"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        {/* Mobile menu */}
        {open && (
          <div className="md:hidden border-t border-white/5 bg-[#020817] px-4 py-3 flex flex-col gap-1">
            {NAV_LINKS.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className="px-4 py-3 text-sm text-slate-300 hover:text-white hover:bg-white/5 rounded-lg transition-all"
              >
                {l.label}
              </Link>
            ))}
            <Link href="/check" onClick={() => setOpen(false)} className="btn-primary mt-2 justify-center text-sm">
              Check Message Now
            </Link>
          </div>
        )}
      </nav>
    </>
  );
}
