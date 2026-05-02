"""
Privacy Scrubber Agent
Masks PII (phone numbers, PAN, Aadhaar, account IDs, UPI IDs)
using both Regex patterns AND spaCy NER for maximum coverage.
BEFORE any text is sent to an external LLM API.
"""
import re
from dataclasses import dataclass
from typing import Dict

# ── spaCy NER (lazy loaded) ───────────────────────────────────────────────────
_nlp = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
        except Exception:
            _nlp = False  # mark as unavailable
    return _nlp if _nlp else None


# ── Regex Patterns ───────────────────────────────────────────────────────────

PATTERNS: Dict[str, str] = {
    # Indian mobile numbers: +91-XXXXXXXXXX, 91XXXXXXXXXX, 0XXXXXXXXXX, XXXXXXXXXX
    "phone": r"(?:(?:\+|0{0,2})91[\s\-]?)?[6-9]\d{9}",

    # PAN card: ABCDE1234F
    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    # Aadhaar: 12-digit number (with or without spaces/dashes)
    "aadhaar": r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b",

    # Bank account numbers: 9–18 digits
    "bank_account": r"\b\d{9,18}\b",

    # IFSC code: ABCD0123456
    "ifsc": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",

    # UPI IDs: name@bank
    "upi": r"\b[\w.\-]+@[a-zA-Z]{3,}\b",

    # Email addresses
    "email": r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b",

    # CVV / OTP patterns (3-6 digit standalone numbers in sensitive context)
    "otp": r"\bOTP[\s:is]*\d{4,8}\b",
}

REPLACEMENT_LABELS = {
    "phone": "[PHONE]",
    "pan": "[PAN]",
    "aadhaar": "[AADHAAR]",
    "bank_account": "[ACCOUNT]",
    "ifsc": "[IFSC]",
    "upi": "[UPI_ID]",
    "email": "[EMAIL]",
    "otp": "[OTP]",
}


@dataclass
class ScrubResult:
    original_text: str
    scrubbed_text: str
    entities_found: Dict[str, int]  # entity_type -> count masked


def scrub(text: str) -> ScrubResult:
    """
    Scrub all PII from the input text using Regex + spaCy NER.
    Returns the scrubbed text and a summary of what was masked.
    """
    scrubbed = text
    entities_found: Dict[str, int] = {}

    # Step 1: Apply regex patterns (most specific first)
    order = ["otp", "email", "upi", "pan", "aadhaar", "ifsc", "phone", "bank_account"]
    for key in order:
        pattern = PATTERNS[key]
        label = REPLACEMENT_LABELS[key]
        matches = re.findall(pattern, scrubbed, flags=re.IGNORECASE)
        if matches:
            entities_found[key] = len(matches)
            scrubbed = re.sub(pattern, label, scrubbed, flags=re.IGNORECASE)

    # Step 2: spaCy NER — mask PERSON names and additional entities
    nlp = _get_nlp()
    if nlp:
        try:
            doc = nlp(scrubbed)
            # Mask in reverse order to preserve character positions
            replacements = []
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    replacements.append((ent.start_char, ent.end_char, "[PERSON]"))
                elif ent.label_ in ("GPE", "LOC") and len(ent.text) > 15:
                    # Only mask very specific location strings (not common city names)
                    replacements.append((ent.start_char, ent.end_char, "[LOCATION]"))

            # Apply replacements in reverse order
            for start, end, label in sorted(replacements, reverse=True):
                scrubbed = scrubbed[:start] + label + scrubbed[end:]
                key = label.strip("[]").lower()
                entities_found[key] = entities_found.get(key, 0) + 1
        except Exception:
            pass  # spaCy failure is non-fatal

    return ScrubResult(
        original_text=text,
        scrubbed_text=scrubbed,
        entities_found=entities_found,
    )


def scrub_text(text: str) -> str:
    """Convenience function — returns only the scrubbed string."""
    return scrub(text).scrubbed_text
