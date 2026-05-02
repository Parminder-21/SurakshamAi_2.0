"""
Legitimate Pattern Whitelist
Identifies genuine bank/govt messages to reduce false positives.
"""
import re
from typing import Tuple

# ── Official Sender Patterns ──────────────────────────────────────────────────

OFFICIAL_SENDERS = [
    # Banks
    r"\bSBI\b", r"\bHDFC\b", r"\bICICI\b", r"\bAxis\b", r"\bKotak\b",
    r"\bPNB\b", r"\bBOB\b", r"\bCanara\b", r"\bUnion Bank\b",
    # Govt
    r"\bIRCTC\b", r"\bUIDAI\b", r"\bNPCI\b", r"\bGST\b", r"\bIncome Tax\b",
    # Telecom
    r"\bJio\b", r"\bAirtel\b", r"\bVodafone\b", r"\bBSNL\b",
    # Payments
    r"\bPaytm\b", r"\bPhonePe\b", r"\bGoogle Pay\b", r"\bBhim\b",
]

# ── Legitimate Transaction Patterns ──────────────────────────────────────────

LEGITIMATE_PATTERNS = [
    # Transaction confirmations with IDs
    r"\bTxn\s*(ID|No|Ref)[:\s]*[A-Z0-9]{6,}\b",
    r"\bTransaction\s*(ID|No)[:\s]*[A-Z0-9]{6,}\b",
    r"\bRef\s*(No|ID)[:\s]*[A-Z0-9]{6,}\b",
    r"\bPNR\s*[:\s]*\d{10}\b",
    r"\bOrder\s*(ID|No)[:\s]*[A-Z0-9\-]{6,}\b",

    # Debit/Credit confirmations (legitimate format)
    r"\bdebited\s+(?:Rs\.?|INR)\s*[\d,]+\b",
    r"\bcredited\s+(?:Rs\.?|INR)\s*[\d,]+\b",
    r"\bAvailable\s+[Bb]alance\b",
    r"\bA/c\s+[Xx*]+\d{4}\b",

    # Official contact numbers (toll-free)
    r"\b1800[-\s]?\d{2,3}[-\s]?\d{4}\b",
    r"\b1860[-\s]?\d{3}[-\s]?\d{4}\b",

    # Official websites
    r"\b(?:www\.)?(?:sbi|hdfc|icici|irctc|uidai|incometax|bescom|msedcl)\.(?:co\.in|gov\.in|org\.in|com)\b",

    # Date/time stamps (legitimate alerts have these)
    r"\b\d{2}[-/]\w{3}[-/]\d{4}\b",
    r"\b\d{2}[-/]\d{2}[-/]\d{4}\s+\d{2}:\d{2}\b",
]

# ── Scam Indicators (override whitelist if present) ───────────────────────────

SCAM_OVERRIDES = [
    r"http[s]?://(?!(?:www\.)?(?:sbi|hdfc|icici|irctc|uidai|incometax|bescom|msedcl|phonepe|paytm|googlepay)\.)",
    r"\bshare\s+(?:your\s+)?OTP\b",
    r"\benter\s+(?:your\s+)?(?:UPI\s+)?PIN\b",
    r"\bpay\s+(?:Rs\.?|INR)\s*[\d,]+\s+(?:to\s+)?(?:clear|avoid|prevent|stop)\b",
    r"\bregistration\s+fee\b",
    r"\bprocessing\s+fee\b",
    r"\bsecurity\s+deposit\b",
    r"\bclearance\s+fee\b",
]


def is_likely_legitimate(text: str) -> Tuple[bool, str]:
    """
    Returns (is_legitimate, reason).
    A message is likely legitimate if it has official patterns
    AND no scam override indicators.
    """
    text_lower = text.lower()

    # Check for scam overrides first
    for pattern in SCAM_OVERRIDES:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "scam_override"

    # Count legitimate signals
    legit_score = 0
    matched_patterns = []

    for pattern in LEGITIMATE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            legit_score += 1
            matched_patterns.append(pattern[:30])

    # Strong legitimate signal: transaction ID + balance = definitely legit
    has_txn_id = bool(re.search(r"\b(?:Txn|Transaction|Ref)\s*(?:ID|No)[:\s]*[A-Z0-9]{6,}\b", text, re.IGNORECASE))
    has_balance = bool(re.search(r"\bAvailable\s+[Bb]alance\b", text, re.IGNORECASE))
    has_official_url = bool(re.search(r"\b(?:sbi|hdfc|icici|irctc|uidai)\.(?:co\.in|gov\.in|com)\b", text, re.IGNORECASE))
    has_pnr = bool(re.search(r"\bPNR\s*[:\s]*\d{10}\b", text, re.IGNORECASE))
    has_tollfree = bool(re.search(r"\b1800[-\s]?\d{2,3}[-\s]?\d{4}\b", text))

    if has_txn_id or has_balance or has_official_url or has_pnr:
        return True, "official_transaction_pattern"

    if has_tollfree and legit_score >= 1:
        return True, "official_contact_with_legit_pattern"

    return False, "insufficient_legit_signals"
