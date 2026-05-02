"""
URL Research Agent — Enhanced with Phishing Pattern Training
Trained on 789,054 real phishing URLs from mitchellkrogza/Phishing.Database

Checks URLs using:
  1. Phishing pattern engine (789k URL training)
  2. Google Safe Browsing API
  3. Domain age via WHOIS
  4. Brand impersonation detection (India + Global)
  5. Structural anomaly detection
  6. Free hosting / suspicious TLD detection
"""
import re
import httpx
from datetime import datetime, timezone
from typing import Optional, Tuple
from urllib.parse import urlparse

from app.config import settings
from app.models.schemas import RiskLevel, URLAnalysisResult
from app.agents.phishing_patterns import calculate_phishing_score


async def check_google_safe_browsing(url: str) -> bool:
    """Returns True if URL is flagged by Google Safe Browsing."""
    api_key = settings.google_safe_browsing_api_key
    if not api_key:
        return False
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "suraksha-agent", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(endpoint, json=payload)
            return bool(resp.json().get("matches"))
    except Exception:
        return False


async def get_domain_age_days(domain: str) -> Optional[int]:
    """Returns domain age in days via WHOIS."""
    try:
        import whois
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            now = datetime.now(timezone.utc)
            if creation_date.tzinfo is None:
                creation_date = creation_date.replace(tzinfo=timezone.utc)
            return (now - creation_date).days
    except Exception:
        pass
    return None


async def analyze_url(url: str) -> URLAnalysisResult:
    """
    Full URL phishing analysis pipeline.
    Combines pattern-based detection (trained on 789k URLs) + WHOIS + Google Safe Browsing.
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")

    # ── Step 1: Pattern-based phishing detection (789k training) ─────────────
    phishing_result = calculate_phishing_score(url)
    risk_score = phishing_result["risk_score"]
    threats = list(phishing_result["threats"])
    is_impersonation = phishing_result["is_brand_impersonation"]
    impersonated_brand = phishing_result["impersonated_brand"]

    # ── Step 2: Google Safe Browsing ──────────────────────────────────────────
    gsb_flagged = await check_google_safe_browsing(url)
    if gsb_flagged:
        threats.insert(0, "Flagged by Google Safe Browsing")
        risk_score = min(risk_score + 50, 100)

    # ── Step 3: Domain age via WHOIS ──────────────────────────────────────────
    domain_age = await get_domain_age_days(domain)
    if domain_age is not None:
        if domain_age < 7:
            threats.append(f"Brand new domain (only {domain_age} days old)")
            risk_score = min(risk_score + 30, 100)
        elif domain_age < 30:
            threats.append(f"Very new domain ({domain_age} days old)")
            risk_score = min(risk_score + 20, 100)
        elif domain_age < 90:
            threats.append(f"Relatively new domain ({domain_age} days old)")
            risk_score = min(risk_score + 10, 100)

    # ── Step 4: Determine final risk level ────────────────────────────────────
    if risk_score >= 50:
        risk_level = RiskLevel.HIGH_RISK
    elif risk_score >= 25:
        risk_level = RiskLevel.SUSPICIOUS
    else:
        risk_level = RiskLevel.SAFE

    is_safe = risk_level == RiskLevel.SAFE

    # ── Step 5: Build recommendation ─────────────────────────────────────────
    if gsb_flagged:
        recommendation = "DANGER: This URL is confirmed malicious by Google Safe Browsing. Do NOT open."
    elif is_impersonation:
        recommendation = f"WARNING: This URL impersonates {impersonated_brand}. Visit the official website directly."
    elif risk_level == RiskLevel.HIGH_RISK:
        recommendation = "Do NOT open this link. Multiple phishing indicators detected."
    elif risk_level == RiskLevel.SUSPICIOUS:
        recommendation = "Be cautious. Do not enter personal information or credentials on this site."
    else:
        recommendation = "URL appears safe. Always verify before entering credentials."

    return URLAnalysisResult(
        url=url,
        is_safe=is_safe,
        risk_level=risk_level,
        risk_score=risk_score,
        threats=threats,
        domain_age_days=domain_age,
        is_brand_impersonation=is_impersonation,
        impersonated_brand=impersonated_brand,
        safe_browsing_flagged=gsb_flagged,
        recommendation=recommendation,
    )
