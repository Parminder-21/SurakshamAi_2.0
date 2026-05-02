"""
Risk Scoring Engine — India-Specific Enhanced
Calculates a 0-100 risk score across 4 dimensions + India-specific boosters:
  - Urgency language          (0-25)
  - Authority impersonation   (0-25)
  - Payment pressure          (0-25)
  - Deception / fear tactics  (0-25)
  + India-specific boosters   (up to +40 per pattern, capped at 100)
"""
import re
from dataclasses import dataclass, field
from typing import List, Tuple

from app.models.schemas import RiskLevel, RiskScoreBreakdown
from app.agents.india_scam_patterns import (
    HINDI_URGENCY, HINDI_AUTHORITY, INDIA_BANKS,
    INDIA_PAYMENT_APPS, INDIA_GOVT_IMPERSONATION,
    INDIA_SCAM_PHRASES, HIGH_RISK_BOOSTERS,
)


# ── Base Keyword Banks (English) ──────────────────────────────────────────────

URGENCY_KEYWORDS = [
    r"\burgent\b", r"\bimmediately\b", r"\bturant\b", r"\babhi\b",
    r"\blast chance\b", r"\bexpires? (today|now|in \d+ hours?)\b",
    r"\bwithin \d+ (hours?|minutes?|days?)\b", r"\bdeadline\b",
    r"\bact now\b", r"\bdo not delay\b", r"\bfinal (notice|warning|reminder)\b",
    r"\baccount (will be|is being) (blocked|suspended|deactivated)\b",
    r"\bservice (will be|is being) disconnected\b",
    r"\bband ho jayega\b", r"\bblock ho jayega\b",
    r"\baaj hi\b", r"\btatkal\b", r"\bjaldi\b",
]

AUTHORITY_KEYWORDS = [
    r"\bRBI\b", r"\bSEBI\b", r"\bIRDA\b", r"\bIncome Tax\b", r"\bIT Department\b",
    r"\bCBI\b", r"\bCID\b", r"\bpolice\b", r"\bED\b", r"\bNarcotics\b", r"\bNCB\b",
    r"\bTRAI\b", r"\bDOT\b", r"\bgovernment\b", r"\bsarkari\b",
    r"\bSBI\b", r"\bHDFC\b", r"\bICICI\b", r"\bAxis Bank\b",
    r"\bAmazon\b", r"\bFlipkart\b",
    r"\bPM (Modi|Office)\b", r"\bPrime Minister\b",
    r"\bverified (agent|officer|executive)\b",
    r"\bofficial (notice|communication|message)\b",
    r"\bEnforcement Directorate\b", r"\bCustoms Department\b",
    r"\bSupreme Court\b", r"\bHigh Court\b",
]

PAYMENT_KEYWORDS = [
    r"\bpay\b", r"\bpayment\b", r"\btransfer\b",
    r"\bsend (money|cash|amount|rs\.?|₹)\b",
    r"\bUPI\b", r"\bGoogle Pay\b", r"\bPhonePe\b", r"\bPaytm\b",
    r"\bBHIM\b", r"\bNEFT\b", r"\bIMPS\b", r"\bRTGS\b",
    r"\brefund\b", r"\bcashback\b", r"\bprize money\b",
    r"\bclick (the |this )?link (to |and )?pay\b",
    r"\bwallet\b", r"\brecharge\b", r"\bfee\b", r"\bcharge\b",
    r"\bRs\.?\s*\d+\b", r"\b₹\s*\d+\b",
    r"\bregistration (fee|charge)\b", r"\bprocessing (fee|charge)\b",
    r"\bclearance (fee|charge)\b", r"\bsecurity deposit\b",
]

DECEPTION_KEYWORDS = [
    r"\bwon\b", r"\bwinner\b", r"\bcongratulations\b", r"\bcongrats\b",
    r"\bselected\b", r"\bchosen\b", r"\blucky\b",
    r"\bfree\b", r"\bno cost\b", r"\bzero cost\b",
    r"\bKYC\b",
    r"\bverify (your )?(account|identity|KYC|Aadhaar|PAN)\b",
    r"\bOTP\b", r"\bshare (the |your )?OTP\b",
    r"\bdo not (tell|share|disclose)\b",
    r"\bjob offer\b", r"\bwork from home\b", r"\bpart.?time\b",
    r"\bearning\b", r"\bincome\b", r"\bper day\b",
    r"\bparcel (held|blocked|seized)\b", r"\bcustoms\b",
    r"\belectricity (bill|connection) (cut|disconnected|blocked)\b",
    r"\bprize\b", r"\bclaim\b", r"\blottery\b",
    r"\bblocked\b", r"\bsuspended\b", r"\bdeactivated\b",
    r"\bdigital arrest\b", r"\bguaranteed (returns|profit|income)\b",
    r"\bdouble (your )?money\b", r"\bFIR\b", r"\barrest warrant\b",
    r"\binaam\b", r"\bjeeta\b", r"\bKBC\b",
    r"\bghare baithe\b", r"\bghar se kaam\b",
]


def _count_matches(text: str, patterns: List[str]) -> int:
    count = 0
    for p in patterns:
        try:
            if re.search(p, text, re.IGNORECASE):
                count += 1
        except re.error:
            pass
    return count


def _score_dimension(matches: int, max_matches: int, max_score: int = 25) -> int:
    if matches == 0:
        return 0
    ratio = min(matches / max_matches, 1.0)
    return round(ratio * max_score)


def _apply_india_boosters(text: str) -> Tuple[int, List[str]]:
    """Apply India-specific high-risk pattern boosters."""
    boost = 0
    triggered = []
    for pattern, weight, label in HIGH_RISK_BOOSTERS:
        try:
            if re.search(pattern, text, re.IGNORECASE):
                boost += weight
                triggered.append(label)
        except re.error:
            pass
    return min(boost, 50), triggered  # cap booster at 50


def _check_india_scam_phrases(text: str) -> int:
    """Check India-specific scam phrases — returns hit count."""
    hits = 0
    for pattern in INDIA_SCAM_PHRASES:
        try:
            if re.search(pattern, text, re.IGNORECASE):
                hits += 1
        except re.error:
            pass
    return hits


@dataclass
class ScoringResult:
    breakdown: RiskScoreBreakdown
    risk_level: RiskLevel
    red_flags: List[str]
    india_specific_flags: List[str] = field(default_factory=list)


def calculate_risk_score(text: str) -> ScoringResult:
    # Step 1: Check legitimate patterns — reduces false positives
    from app.agents.legitimate_patterns import is_likely_legitimate
    is_legit, _ = is_likely_legitimate(text)

    # Step 2: Base dimension scoring
    urgency_hits    = _count_matches(text, URGENCY_KEYWORDS)
    authority_hits  = _count_matches(text, AUTHORITY_KEYWORDS)
    payment_hits    = _count_matches(text, PAYMENT_KEYWORDS)
    deception_hits  = _count_matches(text, DECEPTION_KEYWORDS)

    # Step 3: India-specific phrase hits (adds to deception)
    india_hits = _check_india_scam_phrases(text)
    deception_hits += min(india_hits, 3)  # add up to 3 extra hits

    urgency_score   = _score_dimension(urgency_hits,   max_matches=3)
    authority_score = _score_dimension(authority_hits, max_matches=2)
    payment_score   = _score_dimension(payment_hits,   max_matches=3)
    deception_score = _score_dimension(deception_hits, max_matches=4)

    base_total = urgency_score + authority_score + payment_score + deception_score

    # Step 4: India-specific boosters (high-confidence patterns)
    boost, india_flags = _apply_india_boosters(text)

    total = min(base_total + boost, 100)

    # Step 5: Apply legitimacy discount
    if is_legit:
        discount = min(total, 30)
        total = max(0, total - discount)
        urgency_score   = max(0, urgency_score   - 8)
        authority_score = max(0, authority_score - 8)
        payment_score   = max(0, payment_score   - 8)
        deception_score = max(0, deception_score - 6)

    breakdown = RiskScoreBreakdown(
        urgency_score=min(urgency_score, 25),
        authority_impersonation_score=min(authority_score, 25),
        payment_pressure_score=min(payment_score, 25),
        deception_fear_score=min(deception_score, 25),
        total=total,
    )

    if total <= 20:
        risk_level = RiskLevel.SAFE
    elif total <= 60:
        risk_level = RiskLevel.SUSPICIOUS
    else:
        risk_level = RiskLevel.HIGH_RISK

    # Build red flags
    red_flags: List[str] = []
    if urgency_score > 10:
        red_flags.append("Urgency / time-pressure language detected")
    if authority_score > 10:
        red_flags.append("Impersonation of authority / trusted brand")
    if payment_score > 10:
        red_flags.append("Payment or money transfer pressure")
    if deception_score > 10:
        red_flags.append("Deceptive tactics (fake prize, KYC, OTP request)")
    if india_hits > 0:
        red_flags.append(f"India-specific scam pattern detected ({india_hits} signals)")

    return ScoringResult(
        breakdown=breakdown,
        risk_level=risk_level,
        red_flags=red_flags,
        india_specific_flags=india_flags,
    )
