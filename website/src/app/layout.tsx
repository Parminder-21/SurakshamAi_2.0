import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Suraksham AI — Cyber Safety for India",
  description:
    "Detect scams, phishing URLs, and fraud patterns. Stay safe from UPI scams, fake KYC, job fraud, and more.",
  keywords: ["cyber safety", "scam detector", "fraud detection", "India", "UPI scam", "phishing"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-gray-100 min-h-screen font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
