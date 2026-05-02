import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

export interface ExplainabilityDetail {
  evidence_chain: string[];
  keyword_verdict: string;
  llm_verdict: string;
  verdicts_agree: boolean;
  authenticity_score: number;
  authenticity_label: string;
  decision_summary: string;
  triggered_rules: string[];
}

export interface AnalysisResult {
  risk_level: "SAFE" | "SUSPICIOUS" | "HIGH_RISK";
  risk_score: number;
  score_breakdown: {
    urgency_score: number;
    authority_impersonation_score: number;
    payment_pressure_score: number;
    deception_fear_score: number;
    total: number;
  };
  scam_type: string;
  confidence: number;
  red_flags: string[];
  why_risky: string;
  what_not_to_do: string[];
  what_to_do: string[];
  scrubbed_text: string;
  explainability?: ExplainabilityDetail;
}

export interface NewsFeedItem {
  id: string;
  title: string;
  slug: string;
  summary: string;
  scam_type: string;
  severity: string;
  report_count: number;
  published_at: string;
  tags: string[];
  source_name?: string;
  source_url?: string;
}

export interface NewsStats {
  total_items: number;
  high_risk: number;
  medium_risk: number;
  total_reports: number;
  scam_type_breakdown: Record<string, number>;
  sources: string[];
  last_updated: string;
}

export async function analyzeMessage(message: string, language = "en"): Promise<AnalysisResult> {
  const { data } = await api.post("/analyze/message", { message, language });
  return data;
}

export async function analyzeURL(url: string): Promise<any> {
  const { data } = await api.post("/analyze/url", { url });
  return data;
}

export async function getNewsFeed(
  limit = 20,
  severity?: string,
  scam_type?: string
): Promise<NewsFeedItem[]> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (severity) params.set("severity", severity);
  if (scam_type) params.set("scam_type", scam_type);
  const { data } = await api.get(`/news-feed/?${params}`);
  return data;
}

export async function getNewsStats(): Promise<NewsStats> {
  const { data } = await api.get("/news-feed/stats");
  return data;
}

export async function reportScam(content: string, scam_type?: string, reporter_note?: string) {
  const { data } = await api.post("/report-scam/", {
    content,
    scam_type,
    reporter_note,
    source: "website",
  });
  return data;
}
