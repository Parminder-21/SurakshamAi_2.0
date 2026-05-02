import Navbar from "@/components/Navbar";
import { Shield, AlertTriangle, Phone, CreditCard, Briefcase, Package, Trophy, Zap, Key } from "lucide-react";

const SCAM_GUIDE = [
  {
    icon: CreditCard,
    type: "Fake KYC / Bank Verification",
    color: "text-blue-400",
    how: "Fraudsters send messages claiming your bank account will be blocked unless you update KYC via a link.",
    signs: ["Urgent language about account suspension", "Link to unofficial website", "Asks for Aadhaar/PAN/OTP"],
    doNot: ["Click the link", "Share OTP or card details", "Call back on the number given"],
    doThis: ["Log in to your bank's official app", "Call the official bank helpline", "Report to cybercrime.gov.in"],
  },
  {
    icon: Zap,
    type: "UPI / Payment Scam",
    color: "text-yellow-400",
    how: "Scammers send UPI payment requests disguised as 'receive money' or share QR codes that debit your account.",
    signs: ["QR code to 'receive' money", "UPI link from unknown sender", "Urgency to complete payment"],
    doNot: ["Scan QR codes from strangers", "Enter UPI PIN to receive money", "Click payment links in messages"],
    doThis: ["Remember: you never need PIN to receive money", "Verify sender identity before any transaction", "Use only official payment apps"],
  },
  {
    icon: Briefcase,
    type: "Job Fraud",
    color: "text-green-400",
    how: "Fake job offers on Telegram/WhatsApp promising high pay for simple tasks, then asking for registration fees.",
    signs: ["Unsolicited job offer", "Too-good-to-be-true salary", "Registration or training fee required"],
    doNot: ["Pay any registration fee", "Share bank details for 'salary setup'", "Download unknown apps"],
    doThis: ["Verify company on official website", "Never pay to get a job", "Report on cybercrime.gov.in"],
  },
  {
    icon: Package,
    type: "Courier / Parcel Scam",
    color: "text-orange-400",
    how: "Callers claim your parcel contains illegal items and threaten arrest unless you pay a 'clearance fee'.",
    signs: ["Call from 'CBI/Customs/Police'", "Threat of arrest", "Demand for immediate payment"],
    doNot: ["Pay any 'clearance fee'", "Share personal details over phone", "Stay on a 'digital arrest' call"],
    doThis: ["Hang up immediately", "Real agencies never call for money", "Report to 1930 or cybercrime.gov.in"],
  },
  {
    icon: Trophy,
    type: "Lottery / Prize Scam",
    color: "text-purple-400",
    how: "Messages claiming you've won a lottery or prize, asking for processing fees or personal details to claim it.",
    signs: ["Unexpected prize notification", "Processing fee to claim prize", "Urgency to respond"],
    doNot: ["Pay any processing fee", "Share bank details", "Believe unsolicited prize claims"],
    doThis: ["Ignore and delete the message", "You cannot win a lottery you didn't enter", "Report the number"],
  },
  {
    icon: Key,
    type: "OTP Theft",
    color: "text-red-400",
    how: "Fraudsters call posing as bank/telecom staff and trick you into sharing OTPs to 'verify your account'.",
    signs: ["Request to share OTP over phone", "Claim that OTP is needed for verification", "Urgency to share immediately"],
    doNot: ["Share OTP with anyone, ever", "Read OTP aloud on a call", "Enter OTP on unknown websites"],
    doThis: ["Banks never ask for OTP", "Hang up and call your bank directly", "Change passwords immediately if shared"],
  },
];

export default function KnowledgeBasePage() {
  return (
    <>
      <Navbar />
      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="mb-10">
          <h1 className="text-3xl font-bold text-white mb-2">Scam Knowledge Base</h1>
          <p className="text-gray-400">
            Understand how each scam works and how to protect yourself.
          </p>
        </div>

        <div className="space-y-6">
          {SCAM_GUIDE.map((scam) => (
            <div key={scam.type} className="card">
              <div className="flex items-center gap-3 mb-4">
                <scam.icon className={scam.color} size={24} />
                <h2 className="text-lg font-bold text-white">{scam.type}</h2>
              </div>

              <p className="text-sm text-gray-400 mb-5">{scam.how}</p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <h3 className="text-xs font-semibold text-yellow-400 uppercase tracking-wide mb-2">
                    Warning Signs
                  </h3>
                  <ul className="space-y-1">
                    {scam.signs.map((s) => (
                      <li key={s} className="text-xs text-gray-400 flex items-start gap-1.5">
                        <AlertTriangle size={11} className="mt-0.5 shrink-0 text-yellow-400" />
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">
                    Do NOT
                  </h3>
                  <ul className="space-y-1">
                    {scam.doNot.map((s) => (
                      <li key={s} className="text-xs text-gray-400 flex items-start gap-1.5">
                        <span className="text-red-400 shrink-0">✗</span>
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="text-xs font-semibold text-green-400 uppercase tracking-wide mb-2">
                    What to Do
                  </h3>
                  <ul className="space-y-1">
                    {scam.doThis.map((s) => (
                      <li key={s} className="text-xs text-gray-400 flex items-start gap-1.5">
                        <span className="text-green-400 shrink-0">✓</span>
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </>
  );
}
