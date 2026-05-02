"""
Explainability Engine
Provides evidence-based reasoning for every fraud detection decision.
Makes the model's decisions transparent and trustworthy.
"""
import re
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from app.models.schemas import RiskLevel


@dataclass
class Evidence:
    category: str          # e.g. "Urgency Language"
    matched_text: str      # exact text that triggered
    pattern_name: str      # human-readable pattern name
    weight: int            # contribution to score (0-25)


@dataclass
class ExplainabilityReport:
    evidence_chain: List[Evidence]
    keyword_verdict: str        # SAFE / SUSPICIOUS / HIGH_RISK
    llm_verdict: str            # SAFE / SUSPICIOUS / HIGH_RISK
    verdicts_agree: bool
    authenticity_score: float   # 0.0 - 1.0
    authenticity_label: str     # VERIFIED / LIKELY / UNCERTAIN
    decision_summary: str       # plain English explanation
    triggered_rules: List[str]  # human-readable rules that fired


# ── Evidence Extraction ───────────────────────────────────────────────────────

EVIDENCE_PATTERNS = {
    "Urgency Language": [
        (r"\burgent\b", "Word 'urgent' detected"),
        (r"\bimmediately\b", "Word 'immediately' detected"),
        (r"\bwithin \d+ (hours?|minutes?)\b", "Time pressure phrase"),
        (r"\baccount (will be|is being) (blocked|suspended)\b", "Account block threat"),
        (r"\bfinal (notice|warning)\b", "Final warning language"),
        (r"\bdo not delay\b", "Delay warning"),
        (r"\blast chance\b", "Last chance pressure"),
        (r"\bservice (will be|is being) disconnected\b", "Service disconnection threat"),
    ],
    "Authority Impersonation": [
        (r"\bRBI\b", "Claims to be RBI"),
        (r"\bCBI\b", "Claims to be CBI"),
        (r"\bTRAI\b", "Claims to be TRAI"),
        (r"\bIncome Tax\b", "Claims to be Income Tax Dept"),
        (r"\bpolice\b", "Mentions police"),
        (r"\bgovernment\b", "Claims government authority"),
        (r"\bverified (agent|officer|executive)\b", "Claims verified official"),
        (r"\bSBI\b", "Mentions SBI (possible impersonation)"),
        (r"\bHDFC\b", "Mentions HDFC (possible impersonation)"),
    ],
    "Payment Pressure": [
        (r"\bpay\b", "Payment demand"),
        (r"\bUPI\b", "UPI payment mentioned"),
        (r"\bGoogle Pay\b", "Google Pay mentioned"),
        (r"\bPhonePe\b", "PhonePe mentioned"),
        (r"\bregistration fee\b", "Registration fee demand"),
        (r"\bprocessing fee\b", "Processing fee demand"),
        (r"\bclearance fee\b", "Clearance fee demand"),
        (r"\bsecurity deposit\b", "Security deposit demand"),
        (r"\bRs\.?\s*\d+\b", "Specific amount mentioned"),
        (r"\bscan (this |the )?QR\b", "QR code scan request"),
    ],
    "Deception Tactics": [
        (r"\bOTP\b", "OTP mentioned"),
        (r"\bshare (the |your )?OTP\b", "Asks to share OTP"),
        (r"\bKYC\b", "KYC update request"),
        (r"\bwon\b|\bwinner\b", "Prize/lottery claim"),
        (r"\bcongratulations\b", "Fake congratulations"),
        (r"\bwork from home\b", "Work from home offer"),
        (r"\bper day\b", "Daily earning promise"),
        (r"\bparcel (held|blocked|seized)\b", "Parcel seizure claim"),
        (r"\bcustoms\b", "Customs claim"),
        (r"\blottery\b|\bprize\b", "Lottery/prize claim"),
        (r"\bblocked\b|\bsuspended\b", "Account blocked threat"),
    ],
    "Suspicious URLs": [
        (r"http[s]?://(?!(?:www\.)?(?:sbi|hdfc|icici|irctc|uidai|incometax|bescom|phonepe|paytm)\.(?:co\.in|gov\.in|com|org\.in))",
         "Unofficial/suspicious URL detected"),
        (r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "Raw IP address in URL"),
        (r"bit\.ly|tinyurl|t\.co", "URL shortener used"),
        (r"\.xyz|\.tk|\.ml|\.ga\b", "Suspicious domain extension"),
    ],
}


def extract_evidence(text: str) -> List[Evidence]:
    """Extract all matching evidence from text with exact matched strings."""
    evidence_list = []

    for category, patterns in EVIDENCE_PATTERNS.items():
        for pattern, description in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Get the actual matched text
                match_obj = re.search(pattern, text, re.IGNORECASE)
                matched_text = match_obj.group(0) if match_obj else str(matches[0])
                evidence_list.append(Evidence(
                    category=category,
                    matched_text=f'"{matched_text}"',
                    pattern_name=description,
                    weight=5,
                ))

    return evidence_list


def build_decision_summary(
    evidence: List[Evidence],
    risk_level: RiskLevel,
    scam_type: str,
    verdicts_agree: bool,
) -> str:
    """Build a plain-English explanation of the decision."""
    if risk_level == RiskLevel.SAFE:
        return (
            "This message appears to be legitimate. "
            "No significant fraud indicators were detected. "
            "It matches patterns of genuine bank/service notifications."
        )

    categories = list({e.category for e in evidence})
    evidence_count = len(evidence)

    if not categories:
        return "This message contains general patterns associated with fraud."

    cat_str = ", ".join(categories[:3])
    agree_str = "Both keyword analysis and AI agree" if verdicts_agree else "AI analysis indicates"

    return (
        f"{agree_str} this is likely a '{scam_type}'. "
        f"Found {evidence_count} suspicious indicator(s) across: {cat_str}. "
        f"Key signals: {', '.join(e.pattern_name for e in evidence[:3])}."
    )


def compute_authenticity(
    keyword_verdict: str,
    llm_verdict: str,
    evidence_count: int,
    confidence: float,
) -> Tuple[float, str]:
    """
    Compute authenticity score — how trustworthy is this prediction?

    High authenticity = keyword scorer AND LLM agree + strong evidence
    """
    score = 0.0

    # Both models agree = +0.4
    kw_spam = keyword_verdict in ("SUSPICIOUS", "HIGH_RISK")
    llm_spam = llm_verdict in ("SUSPICIOUS", "HIGH_RISK")

    if kw_spam == llm_spam:
        score += 0.40
    else:
        score += 0.10  # Disagreement reduces trust

    # LLM confidence contribution = up to +0.35
    score += confidence * 0.35

    # Evidence count contribution = up to +0.25
    evidence_contribution = min(evidence_count / 8, 1.0) * 0.25
    score += evidence_contribution

    score = min(score, 1.0)

    if score >= 0.80:
        label = "VERIFIED"
    elif score >= 0.60:
        label = "LIKELY"
    else:
        label = "UNCERTAIN"

    return round(score, 2), label


def generate_report(
    text: str,
    keyword_risk_level: RiskLevel,
    llm_scam_type: str,
    llm_confidence: float,
) -> ExplainabilityReport:
    """Generate full explainability report for a prediction."""

    evidence = extract_evidence(text)

    # Determine verdicts
    keyword_verdict = keyword_risk_level.value
    llm_is_scam = llm_scam_type not in ("Safe", "Safe Message")
    llm_verdict = "HIGH_RISK" if llm_is_scam else "SAFE"
    verdicts_agree = (keyword_verdict in ("SUSPICIOUS", "HIGH_RISK")) == llm_is_scam

    # Authenticity
    auth_score, auth_label = compute_authenticity(
        keyword_verdict, llm_verdict, len(evidence), llm_confidence
    )

    # Decision summary
    final_risk = keyword_risk_level if not llm_is_scam else (
        RiskLevel.HIGH_RISK if keyword_risk_level == RiskLevel.HIGH_RISK
        else RiskLevel.SUSPICIOUS
    )
    summary = build_decision_summary(evidence, final_risk, llm_scam_type, verdicts_agree)

    # Triggered rules
    triggered_rules = [f"{e.category}: {e.pattern_name} — {e.matched_text}"
                       for e in evidence[:6]]

    return ExplainabilityReport(
        evidence_chain=evidence,
        keyword_verdict=keyword_verdict,
        llm_verdict=llm_verdict,
        verdicts_agree=verdicts_agree,
        authenticity_score=auth_score,
        authenticity_label=auth_label,
        decision_summary=summary,
        triggered_rules=triggered_rules,
    )
