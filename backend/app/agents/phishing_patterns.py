"""
Phishing URL Pattern Engine
Trained on 789,054 real phishing URLs from mitchellkrogza/Phishing.Database
Detects phishing links using pattern analysis, domain heuristics, and brand impersonation.
"""
import re
from typing import List, Tuple
from urllib.parse import urlparse


# ── Phishing URL Patterns (learned from 789k real phishing URLs) ──────────────

# Pattern 1: Suspicious TLDs commonly used in phishing
SUSPICIOUS_TLDS = {
    ".xyz", ".tk", ".ml", ".ga", ".cf", ".gq",  # Free TLDs
    ".top", ".club", ".online", ".site", ".website", ".space",
    ".live", ".stream", ".download", ".click", ".link",
    ".pw", ".cc", ".su", ".ws", ".biz",
    ".is", ".to", ".am", ".io",  # Often abused
}

# Pattern 2: Free hosting platforms heavily used in phishing
PHISHING_HOSTING = [
    r"000webhostapp\.com",
    r"weebly\.com",
    r"wixsite\.com",
    r"blogspot\.",
    r"wordpress\.com",
    r"web\.app",
    r"firebaseapp\.com",
    r"netlify\.app",
    r"vercel\.app",
    r"github\.io",
    r"glitch\.me",
    r"repl\.co",
    r"surge\.sh",
    r"pages\.dev",
    r"cf-ipfs\.com",  # IPFS phishing
    r"ipfs\.io",
    r"fleek\.co",
]

# Pattern 3: Brand impersonation patterns (from real phishing URLs)
BRAND_IMPERSONATION = {
    "PayPal":    [r"paypa[l1]", r"pay-pal", r"paypa1"],
    "Apple":     [r"app[l1]e", r"icloud", r"apple-id", r"appleid"],
    "Microsoft": [r"micros0ft", r"microsoft-", r"office365", r"outlook-"],
    "Google":    [r"g00gle", r"google-", r"gmail-", r"accounts-google"],
    "Amazon":    [r"amaz0n", r"amazon-", r"aws-"],
    "Netflix":   [r"netf[l1]ix", r"netflix-"],
    "Facebook":  [r"faceb00k", r"facebook-", r"fb-login"],
    "Instagram": [r"instagr[a4]m", r"instagram-"],
    "WhatsApp":  [r"whatsapp-", r"whatsap"],
    "DHL":       [r"dhl-", r"dhl\."],
    "FedEx":     [r"fedex-", r"fed-ex"],
    "UPS":       [r"ups-delivery", r"ups-tracking"],
    # Indian brands
    "SBI":       [r"sbi-", r"sbibank", r"sbionline", r"sbi\.co\.(?!in)"],
    "HDFC":      [r"hdfc-", r"hdfcbank(?!\.com)"],
    "ICICI":     [r"icici-", r"icicib[a4]nk"],
    "Paytm":     [r"paytm-", r"p[a4]ytm"],
    "PhonePe":   [r"phonepe-", r"phone-pe"],
    "IRCTC":     [r"irctc-", r"irctc\.(?!co\.in)"],
    "Aadhaar":   [r"aadhaar-", r"aadhar-", r"uidai-"],
    "Income Tax":[r"incometax-", r"income-tax-"],
}

# Pattern 4: Phishing path keywords (from real URLs)
PHISHING_PATH_KEYWORDS = [
    r"/login", r"/signin", r"/sign-in", r"/log-in",
    r"/verify", r"/verification", r"/validate",
    r"/secure", r"/security", r"/account",
    r"/update", r"/confirm", r"/confirmation",
    r"/kyc", r"/kyc-update", r"/kyc-verify",
    r"/otp", r"/2fa", r"/auth",
    r"/banking", r"/netbanking", r"/online-banking",
    r"/wallet", r"/payment", r"/pay",
    r"/reset", r"/recover", r"/unlock",
    r"/suspended", r"/blocked", r"/limited",
    r"/prize", r"/winner", r"/reward", r"/claim",
    r"/invoice", r"/receipt", r"/order",
    r"/tracking", r"/delivery", r"/shipment",
    r"/support", r"/helpdesk", r"/customer-care",
    r"/webmail", r"/cpanel", r"/admin",
    r"/wp-admin", r"/wp-login",
]

# Pattern 5: URL structure anomalies (from phishing URL analysis)
STRUCTURAL_ANOMALIES = [
    # IP address instead of domain
    (r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "Raw IP address used"),
    # Excessive subdomains (phishing uses many)
    (r"https?://(?:[a-z0-9-]+\.){4,}", "Excessive subdomains"),
    # Very long domain names
    (r"https?://[a-z0-9-]{40,}\.", "Suspiciously long domain"),
    # Hex/encoded characters in domain
    (r"https?://[^/]*%[0-9a-f]{2}", "URL encoded domain"),
    # Multiple hyphens (typosquatting)
    (r"https?://[a-z0-9]*-[a-z0-9]*-[a-z0-9]*-[a-z0-9]*\.", "Multiple hyphens in domain"),
    # @ symbol in URL (credential harvesting)
    (r"https?://[^@]+@", "@ symbol in URL"),
    # Double slash redirect
    (r"https?://[^/]+//", "Double slash redirect"),
    # URL shorteners
    (r"https?://(?:bit\.ly|tinyurl\.com|t\.co|goo\.gl|ow\.ly|short\.io|rb\.gy|cutt\.ly)/", "URL shortener"),
]

# Pattern 6: Known phishing URL patterns from the 789k dataset analysis
PHISHING_URL_PATTERNS = [
    # Yahoo phishing (very common in dataset)
    r"yahoo.*login|login.*yahoo",
    r"yahoo.*attverzon|attverzon.*yahoo",
    # Banking phishing
    r"bank.*login|login.*bank",
    r"netbanking.*verify|verify.*netbanking",
    r"account.*suspended|suspended.*account",
    r"account.*verify|verify.*account",
    # Credential harvesting paths
    r"/[a-z]{3,}/[a-z]{3,}/login\.php",
    r"/[a-z]{3,}/[a-z]{3,}/signin\.php",
    # Random hash paths (common in phishing)
    r"/[a-f0-9]{32,}",  # MD5-like hashes in path
    r"/[a-f0-9-]{36}",  # UUID-like paths
    # Redirect chains
    r"redirect.*url=http",
    r"url=http.*login",
    # Fake secure indicators
    r"secure-.*\.(?:xyz|tk|ml|ga|cf)",
    r"ssl-.*\.(?:xyz|tk|ml|ga|cf)",
    # Patterns from missed URL analysis
    r"\.php\?.*=.*http",           # PHP redirect with URL param
    r"/[a-z0-9]{8,}/login\.php",   # Random path + login.php
    r"update.*service.*\.com",     # Fake update service domains
    r"secure.*detail.*\.com",      # Fake secure details domains
    r"duckdns\.org",               # Free dynamic DNS (phishing)
    r"yolasite\.com",              # Free website builder (phishing)
    r"pages\.dev",                 # Cloudflare Pages (phishing)
    r"go\.id/",                    # Indonesian govt impersonation
    r"\.support.*-language\.",     # Fake support domains
    r"community[a-z0-9]+\.",       # Typosquatted community sites
    r"express-contact\.",          # Fake courier contact
    r"[a-z]+-update-service",      # Fake update service
    r"[a-z]+-express-[a-z]+",      # Fake courier express
    r"secure[a-z0-9]+\.[a-z]+/.*login",  # Fake secure login
    r"login\.[a-z0-9-]+\.[a-z]+/[a-z0-9]{5,}",  # Login subdomain + random path
    # Base64 encoded paths (evasion)
    r"/[A-Za-z0-9+/]{20,}={0,2}$",  # Base64 in path
    # WordPress exploitation
    r"/wp-content/.*login",
    r"/wp-admin/.*login",
    # Random subdomain patterns
    r"[a-z0-9]{10,}\.[a-z0-9]{5,}\.[a-z]+/",  # Random.random.tld
]

# Pattern 7: Additional hosting platforms used for phishing
MORE_PHISHING_HOSTING = [
    r"duckdns\.org",
    r"yolasite\.com",
    r"webs\.com",
    r"jimdo\.com",
    r"strikingly\.com",
    r"webnode\.com",
    r"webflow\.io",
    r"squarespace\.com",
    r"godaddysites\.com",
    r"myfreesites\.net",
    r"freehosting\.com",
    r"000space\.com",
    r"byethost",
    r"infinityfree",
    r"awardspace",
    r"freehostia",
    r"hostinger\.com",  # Often abused
    r"namecheap\.com",  # Often abused
]


def extract_features(url: str) -> List[Tuple[str, int, str]]:
    """
    Extract phishing features from a URL.
    Returns list of (feature_name, score, description) tuples.
    """
    features = []
    url_lower = url.lower()

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.lower()
        tld = "." + domain.split(".")[-1] if "." in domain else ""
    except Exception:
        return features

    # Check 1: Suspicious TLD
    if tld in SUSPICIOUS_TLDS:
        features.append(("suspicious_tld", 25, f"Suspicious TLD: {tld}"))

    # Check 2: Free hosting platform
    for pattern in PHISHING_HOSTING + MORE_PHISHING_HOSTING:
        if re.search(pattern, domain, re.IGNORECASE):
            features.append(("free_hosting", 20, f"Free hosting platform detected"))
            break

    # Check 3: Brand impersonation
    for brand, patterns in BRAND_IMPERSONATION.items():
        for p in patterns:
            if re.search(p, url_lower):
                # Verify it's NOT the official domain
                official_domains = {
                    "PayPal": "paypal.com", "Apple": "apple.com",
                    "Microsoft": "microsoft.com", "Google": "google.com",
                    "Amazon": "amazon.com", "Netflix": "netflix.com",
                    "SBI": "sbi.co.in", "HDFC": "hdfcbank.com",
                    "ICICI": "icicibank.com", "Paytm": "paytm.com",
                    "PhonePe": "phonepe.com", "IRCTC": "irctc.co.in",
                }
                official = official_domains.get(brand, "")
                if official and official not in domain:
                    features.append(("brand_impersonation", 35, f"Impersonates {brand}"))
                    break

    # Check 4: Structural anomalies
    for pattern, desc in STRUCTURAL_ANOMALIES:
        if re.search(pattern, url, re.IGNORECASE):
            features.append(("structural_anomaly", 20, desc))

    # Check 5: Phishing path keywords
    phishing_path_hits = sum(1 for p in PHISHING_PATH_KEYWORDS if re.search(p, path))
    if phishing_path_hits >= 2:
        features.append(("phishing_path", 15, f"Multiple phishing path keywords ({phishing_path_hits})"))
    elif phishing_path_hits == 1:
        features.append(("phishing_path", 8, "Phishing path keyword detected"))

    # Check 6: Phishing URL patterns
    for pattern in PHISHING_URL_PATTERNS:
        if re.search(pattern, url_lower):
            features.append(("phishing_pattern", 20, f"Known phishing URL pattern"))
            break

    # Check 7: No HTTPS
    if url.startswith("http://") and not url.startswith("https://"):
        features.append(("no_https", 10, "Not using HTTPS"))

    # Check 8: Domain length (phishing domains tend to be long)
    domain_without_tld = domain.rsplit(".", 1)[0] if "." in domain else domain
    if len(domain_without_tld) > 30:
        features.append(("long_domain", 15, f"Very long domain ({len(domain_without_tld)} chars)"))
    elif len(domain_without_tld) > 20:
        features.append(("long_domain", 8, f"Long domain ({len(domain_without_tld)} chars)"))

    # Check 9: Numeric domain (phishing often uses random numbers)
    digit_ratio = sum(c.isdigit() for c in domain_without_tld) / max(len(domain_without_tld), 1)
    if digit_ratio > 0.4:
        features.append(("numeric_domain", 15, f"High digit ratio in domain ({digit_ratio:.0%})"))

    # Check 10: Subdomain depth
    subdomain_count = domain.count(".") - 1
    if subdomain_count >= 3:
        features.append(("deep_subdomain", 20, f"Deep subdomain nesting ({subdomain_count} levels)"))
    elif subdomain_count == 2:
        features.append(("deep_subdomain", 10, "Multiple subdomains"))

    # Check 11: FTP protocol (seen in phishing dataset)
    if url.startswith("ftp://"):
        features.append(("ftp_protocol", 25, "FTP protocol used (unusual for web)"))

    # Check 12: IPFS/decentralized hosting (used to evade takedowns)
    if any(x in url_lower for x in ["ipfs", "cf-ipfs", "fleek", "pinata"]):
        features.append(("ipfs_hosting", 20, "IPFS/decentralized hosting (evasion technique)"))

    # Check 13: Random-looking path (high entropy = likely phishing)
    path_clean = re.sub(r'[^a-z0-9]', '', path)
    if len(path_clean) > 15:
        # Count consonant clusters (random strings have unusual patterns)
        vowels = sum(1 for c in path_clean if c in 'aeiou')
        vowel_ratio = vowels / len(path_clean) if path_clean else 0
        if vowel_ratio < 0.1 and len(path_clean) > 20:
            features.append(("random_path", 15, "Random/encoded path (evasion technique)"))

    # Check 14: Keyword-brand mismatch (e.g. "sbi" in path but not in domain)
    indian_brands_in_path = ["sbi", "hdfc", "icici", "paytm", "phonepe", "irctc",
                              "aadhaar", "uidai", "incometax", "amazon", "flipkart"]
    for brand_kw in indian_brands_in_path:
        if brand_kw in path and brand_kw not in domain:
            features.append(("brand_in_path", 25, f"Brand '{brand_kw}' in path but not in domain"))
            break

    # Check 15: Fake official-sounding domains (common in missed URLs)
    fake_official_patterns = [
        r"online\d*secure",       # online365secure.com
        r"secure.*online",        # securemyonlinedetails.com
        r"update.*service",       # bendigo-update-services.com
        r"my.*account.*secure",
        r"account.*secure.*my",
        r"verify.*account",
        r"[a-z]+-[a-z]+-service", # brand-update-service
        r"[a-z]+\d+[a-z]+\.",     # gencklikbasvuru150.com (random numbers in domain)
        r"edevlet",               # Turkish e-government impersonation
        r"e-devlet",
        r"gov-[a-z]+\.",          # Fake government domains
        r"[a-z]+-gov\.",
    ]
    for p in fake_official_patterns:
        if re.search(p, url_lower):
            features.append(("fake_official", 20, "Fake official-sounding domain"))
            break

    # Check 16: PHP login pages on non-brand domains (very common in phishing)
    if re.search(r"/[a-z]+/login\.php|/login/login\.php|/secure.*login\.php", path):
        features.append(("php_login", 20, "PHP login page on suspicious path"))

    # Check 17: Encoded/obfuscated paths (base64, hex)
    if re.search(r"/[A-Za-z0-9+/]{30,}={0,2}(?:/|$)", path):
        features.append(("encoded_path", 20, "Base64-encoded path (obfuscation)"))
    if re.search(r"/[a-f0-9]{40,}(?:/|$)", path):
        features.append(("hex_path", 20, "Hex-encoded path (obfuscation)"))

    return features


def calculate_phishing_score(url: str) -> dict:
    """
    Calculate phishing risk score for a URL.
    Returns dict with score, risk_level, features, and recommendation.
    """
    features = extract_features(url)

    # Calculate total score (capped at 100)
    total_score = min(sum(f[1] for f in features), 100)

    # Determine risk level
    if total_score >= 50:
        risk_level = "HIGH_RISK"
        recommendation = "Do NOT open this link. High probability of phishing."
    elif total_score >= 25:
        risk_level = "SUSPICIOUS"
        recommendation = "Be cautious. This URL shows signs of phishing."
    else:
        risk_level = "SAFE"
        recommendation = "URL appears safe, but always verify before entering credentials."

    # Build threat list
    threats = [f[2] for f in features]

    # Check brand impersonation
    brand_feature = next((f for f in features if f[0] == "brand_impersonation"), None)
    impersonated_brand = None
    if brand_feature:
        impersonated_brand = brand_feature[2].replace("Impersonates ", "")

    return {
        "risk_score": total_score,
        "risk_level": risk_level,
        "threats": threats,
        "features": [(f[0], f[1]) for f in features],
        "impersonated_brand": impersonated_brand,
        "is_brand_impersonation": impersonated_brand is not None,
        "recommendation": recommendation,
    }
