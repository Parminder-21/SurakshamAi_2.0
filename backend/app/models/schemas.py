from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    HIGH_RISK = "HIGH_RISK"


class ScamType(str, Enum):
    FAKE_KYC = "Fake KYC / Bank Verification"
    UPI_SCAM = "UPI / Payment Scam"
    JOB_FRAUD = "Job Fraud"
    COURIER_SCAM = "Courier / Parcel Scam"
    LOTTERY_SCAM = "Lottery / Prize Scam"
    AUTHORITY_IMPERSONATION = "Authority Impersonation"
    UTILITY_BILL_SCAM = "Electricity / Utility Bill Scam"
    OTP_THEFT = "OTP Theft"
    PHISHING_URL = "Phishing URL"
    UNKNOWN = "Unknown / General Scam"
    SAFE_MESSAGE = "Safe"


# ── Request Models ──────────────────────────────────────────────────────────

class AnalyzeMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000,
                         description="The SMS/chat/email message to analyze")
    language: str = Field(default="en", description="Preferred response language: en | hi")


class AnalyzeURLRequest(BaseModel):
    url: str = Field(..., description="The URL to check for phishing")
    context: Optional[str] = Field(None, description="Optional surrounding message context")


class AnalyzeCallRequest(BaseModel):
    summary: str = Field(..., min_length=1, max_length=3000,
                         description="Typed or transcribed call summary")
    language: str = Field(default="en")


class ReportScamRequest(BaseModel):
    content: str = Field(..., description="The scam message/URL being reported")
    scam_type: Optional[str] = None
    source: str = Field(default="app", description="app | website")
    reporter_note: Optional[str] = None


# ── Response Models ─────────────────────────────────────────────────────────

class RiskScoreBreakdown(BaseModel):
    urgency_score: int = Field(ge=0, le=25)
    authority_impersonation_score: int = Field(ge=0, le=25)
    payment_pressure_score: int = Field(ge=0, le=25)
    deception_fear_score: int = Field(ge=0, le=25)
    total: int = Field(ge=0, le=100)


class ExplainabilityDetail(BaseModel):
    evidence_chain: List[str]       # exact matched patterns with text
    keyword_verdict: str            # what keyword scorer said
    llm_verdict: str                # what LLM said
    verdicts_agree: bool            # do both models agree?
    authenticity_score: float       # 0.0 - 1.0
    authenticity_label: str         # VERIFIED / LIKELY / UNCERTAIN
    decision_summary: str           # plain English explanation
    triggered_rules: List[str]      # human-readable rules that fired


class AnalysisResult(BaseModel):
    risk_level: RiskLevel
    risk_score: int = Field(ge=0, le=100)
    score_breakdown: RiskScoreBreakdown
    scam_type: ScamType
    confidence: float = Field(ge=0.0, le=1.0)
    red_flags: List[str]
    why_risky: str
    what_not_to_do: List[str]
    what_to_do: List[str]
    scrubbed_text: str
    language: str = "en"
    explainability: Optional[ExplainabilityDetail] = None


class URLAnalysisResult(BaseModel):
    url: str
    is_safe: bool
    risk_level: RiskLevel
    risk_score: int
    threats: List[str]
    domain_age_days: Optional[int]
    is_brand_impersonation: bool
    impersonated_brand: Optional[str]
    safe_browsing_flagged: bool
    recommendation: str


class NewsFeedItem(BaseModel):
    id: str
    title: str
    slug: str
    summary: str
    scam_type: str
    severity: str
    report_count: int
    published_at: str
    tags: List[str]
    source_name: Optional[str] = None
    source_url: Optional[str] = None


class ReportScamResponse(BaseModel):
    success: bool
    report_id: str
    message: str
