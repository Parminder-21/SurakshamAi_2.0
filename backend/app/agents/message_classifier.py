"""
Message Classifier Agent
Uses LLM to classify the scam type and generate guidance.
Falls back to keyword-based classification if LLM is unavailable.
"""
import json
import re
from typing import Optional

from app.models.schemas import ScamType
from app.utils.llm_client import get_llm_response


CLASSIFICATION_PROMPT = """You are a cybersecurity expert specializing in Indian fraud detection.
You understand Indian scams including UPI fraud, fake KYC, digital arrest, courier scams, and Hindi/Hinglish messages.

Analyze the following message (PII already scrubbed) and respond with JSON only.

Message:
\"\"\"
{message}
\"\"\"

INDIA-SPECIFIC RULES:
1. Legitimate bank alerts with Txn ID + balance = "Safe"
2. IRCTC PNR confirmations = "Safe"
3. UIDAI/Aadhaar official updates = "Safe"
4. OTP received for YOUR OWN action = "Safe" | Asked to SHARE OTP = SCAM
5. "Digital arrest" on video call = SCAM (no such law exists in India)
6. Any "clearance fee / processing fee / registration fee" = SCAM
7. "Scan QR to RECEIVE money" = SCAM (you never need to scan to receive)
8. TRAI/CBI/ED/Narcotics calling for money = SCAM
9. "Guaranteed returns / double money" = Investment SCAM
10. Unofficial URLs (not .gov.in, .co.in of known brands) = SCAM
11. Hindi/Hinglish scam phrases like "band ho jayega", "digital arrest", "inaam jeeta" = SCAM

Respond ONLY with valid JSON:
{{
  "scam_type": "<one of: Fake KYC / Bank Verification | UPI / Payment Scam | Job Fraud | Courier / Parcel Scam | Lottery / Prize Scam | Authority Impersonation | Electricity / Utility Bill Scam | OTP Theft | Digital Arrest Scam | Investment / Trading Scam | Phishing URL | Unknown / General Scam | Safe>",
  "confidence": <float 0.0-1.0>,
  "why_risky": "<1-2 sentences in simple English explaining the danger>",
  "what_not_to_do": ["<action 1>", "<action 2>", "<action 3>"],
  "what_to_do": ["<action 1>", "<action 2>", "<action 3>"]
}}
"""

HINDI_GUIDANCE_PROMPT = """
Translate the following JSON guidance fields to Hindi. Keep JSON structure intact.
Only translate: why_risky, what_not_to_do items, what_to_do items.

{json_data}

Respond with valid JSON only.
"""

# Keyword fallback map
KEYWORD_SCAM_MAP = {
    ScamType.FAKE_KYC:    [r"\bKYC\b", r"\bverify (your )?account\b", r"\bbank (account )?verification\b"],
    ScamType.UPI_SCAM:    [r"\bUPI\b", r"\bGoogle Pay\b", r"\bPhonePe\b", r"\bPaytm\b", r"\bpayment link\b", r"\bQR (code|scan)\b"],
    ScamType.JOB_FRAUD:   [r"\bjob offer\b", r"\bwork from home\b", r"\bpart.?time\b", r"\bearning\b", r"\bper day\b", r"\bregistration fee\b", r"\bghare baithe\b"],
    ScamType.COURIER_SCAM:[r"\bparcel\b", r"\bcourier\b", r"\bcustoms\b", r"\bpackage (held|blocked)\b", r"\bFedEx\b", r"\bDHL\b"],
    ScamType.LOTTERY_SCAM:[r"\bwon\b", r"\bwinner\b", r"\blottery\b", r"\bprize\b", r"\bcongratulations\b", r"\bKBC\b", r"\binaam\b"],
    ScamType.AUTHORITY_IMPERSONATION: [r"\bCBI\b", r"\bpolice\b", r"\bIT Department\b", r"\bIncome Tax\b", r"\bTRAI\b", r"\bNarcotics\b", r"\bED\b", r"\bdigital arrest\b"],
    ScamType.UTILITY_BILL_SCAM: [r"\belectricity\b", r"\bpower (cut|bill)\b", r"\bMESCOM\b", r"\bBESCOM\b", r"\bMSEDCL\b", r"\bbijli\b"],
    ScamType.OTP_THEFT:   [r"\bOTP\b", r"\bshare (the )?OTP\b", r"\bone.?time password\b"],
}


def classify_by_keywords(text: str) -> ScamType:
    for scam_type, patterns in KEYWORD_SCAM_MAP.items():
        for p in patterns:
            if re.search(p, text, re.IGNORECASE):
                return scam_type
    return ScamType.UNKNOWN


async def classify_message(scrubbed_text: str, language: str = "en") -> dict:
    """
    Classify a scrubbed message using LLM.
    Returns dict with scam_type, confidence, why_risky, what_not_to_do, what_to_do.
    """
    prompt = CLASSIFICATION_PROMPT.format(message=scrubbed_text)

    try:
        raw = await get_llm_response(prompt)
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            # Validate scam_type
            valid_types = [e.value for e in ScamType]
            if result.get("scam_type") not in valid_types:
                result["scam_type"] = ScamType.UNKNOWN.value
            return result
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"LLM call failed: {e}")

    # Fallback to keyword classification
    scam_type = classify_by_keywords(scrubbed_text)
    return {
        "scam_type": scam_type.value,
        "confidence": 0.6,
        "why_risky": "This message contains patterns commonly associated with fraud.",
        "what_not_to_do": [
            "Do not share any personal information",
            "Do not click any links",
            "Do not make any payments",
        ],
        "what_to_do": [
            "Verify through official channels only",
            "Report to cybercrime.gov.in",
            "Block the sender",
        ],
    }
