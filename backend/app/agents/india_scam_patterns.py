"""
India-Specific Scam Pattern Database
Expanded training data covering regional variations, Hindi messages,
and India-specific fraud tactics.
"""

# ── EXPANDED KEYWORD BANKS ────────────────────────────────────────────────────

# Hindi/Hinglish urgency words
HINDI_URGENCY = [
    r"\bturant\b", r"\babhi\b", r"\bfauran\b", r"\bjaldi\b",
    r"\btatkal\b", r"\bfori\b", r"\bder mat karo\b",
    r"\bkal tak\b", r"\baaj hi\b", r"\bsirf aaj\b",
    r"\bakhiri mauka\b", r"\bakhri chance\b",
    r"\bband ho jayega\b", r"\bblock ho jayega\b",
    r"\bband kar diya jayega\b",
]

# Hindi authority impersonation
HINDI_AUTHORITY = [
    r"\bsarkari\b", r"\bsarkar\b", r"\bpolice\b",
    r"\bdaroga\b", r"\bthana\b", r"\bCBI officer\b",
    r"\bIT vibhag\b", r"\bkaryalay\b",
    r"\bpradhan mantri\b", r"\bmukhyamantri\b",
    r"\bnayab tehsildar\b", r"\btehsildar\b",
    r"\bpatwari\b", r"\bsarpanch\b",
]

# India-specific bank names
INDIA_BANKS = [
    r"\bSBI\b", r"\bState Bank\b",
    r"\bHDFC\b", r"\bICICI\b", r"\bAxis\b",
    r"\bKotak\b", r"\bPNB\b", r"\bPunjab National\b",
    r"\bBank of Baroda\b", r"\bBOB\b",
    r"\bCanara\b", r"\bUnion Bank\b",
    r"\bIDBI\b", r"\bYes Bank\b",
    r"\bIndusInd\b", r"\bFederal Bank\b",
    r"\bBandhan\b", r"\bRBL\b",
    r"\bPost Office\b", r"\bIndia Post\b",
    r"\bPayments Bank\b",
]

# India-specific UPI/payment apps
INDIA_PAYMENT_APPS = [
    r"\bGoogle Pay\b", r"\bGPay\b",
    r"\bPhonePe\b", r"\bPhone Pe\b",
    r"\bPaytm\b", r"\bBHIM\b",
    r"\bAmazon Pay\b", r"\bMobikwik\b",
    r"\bFreecharge\b", r"\bAirtel Money\b",
    r"\bJio Money\b", r"\bWhatsApp Pay\b",
    r"\bCred\b", r"\bSlice\b",
]

# India-specific govt bodies used in scams
INDIA_GOVT_IMPERSONATION = [
    r"\bTRAI\b", r"\bDOT\b", r"\bBSNL\b",
    r"\bRBI\b", r"\bSEBI\b", r"\bIRDA\b",
    r"\bNarcotics\b", r"\bNCB\b",
    r"\bED\b", r"\bEnforcement Directorate\b",
    r"\bIncome Tax\b", r"\bIT Department\b",
    r"\bGST\b", r"\bCustoms\b",
    r"\bCentral Bank\b", r"\bFinance Ministry\b",
    r"\bUIDAI\b", r"\bAadhaar Authority\b",
    r"\bEPFO\b", r"\bPF Office\b",
    r"\bESIC\b", r"\bLabour Department\b",
    r"\bMCA\b", r"\bROC\b",
    r"\bNHAI\b", r"\bFASTag\b",
]

# India-specific scam phrases
INDIA_SCAM_PHRASES = [
    # KYC scams
    r"\bKYC (update|verify|pending|expired|incomplete|required)\b",
    r"\bKYC (nahi|nahin) (kiya|hua)\b",
    r"\bKYC (karo|karein|kijiye)\b",
    r"\baccount (freeze|block|suspend) (ho|kar) (jayega|diya)\b",

    # UPI scams
    r"\bUPI (pin|PIN) (share|batao|dalo|enter)\b",
    r"\bQR (code|scan) (karo|karein|scan)\b",
    r"\bpaise (receive|prapt) (karne|karo) (ke liye|hetu)\b",
    r"\brefund (lene|pane) ke liye\b",
    r"\bcashback (lene|pane) ke liye\b",

    # Job fraud
    r"\bghare baithe (kaam|job|paisa)\b",
    r"\bghar se kaam\b",
    r"\bpart time (kaam|job|income)\b",
    r"\bregistration (fee|charge|amount) (do|bhejo|pay)\b",
    r"\btraining (fee|charge) (do|bhejo)\b",

    # Lottery/prize
    r"\bInaam (jeeta|mila|milega)\b",
    r"\blucky (draw|winner|number)\b",
    r"\bKBC (winner|jeeta|lucky)\b",
    r"\bcrore (jeeta|mila|milega)\b",
    r"\blakh (jeeta|mila|milega)\b",

    # Courier scams
    r"\bparcel (rok|roka|pakda|seized|hold)\b",
    r"\bcustoms (duty|fee|charge) (do|bharo|pay)\b",
    r"\bDHL|FedEx|BlueDart|DTDC\b",
    r"\bpackage (mein|me) (drugs|illegal|banned)\b",

    # Electricity scams
    r"\bbijli (kat|kategi|band) (jayegi|hogi)\b",
    r"\blight (kat|kategi|band) (jayegi|hogi)\b",
    r"\belectricity (bill|connection) (pending|due|overdue)\b",
    r"\bMESCOM|BESCOM|MSEDCL|BSES|TPDDL|UPPCL|TNEB\b",

    # OTP theft
    r"\bOTP (share|batao|do|bhejo|bolo)\b",
    r"\bone time password (share|batao|do)\b",
    r"\bverification (code|number) (share|batao|do)\b",
    r"\bOTP (kisi ko|kisi bhi) (mat|nahi) (batao|dena)\b",  # legitimate warning pattern

    # Digital arrest (new scam)
    r"\bdigital arrest\b",
    r"\bvideo call (par|pe) (rehna|raho|baithe)\b",
    r"\bskype (par|pe) (aao|aana|connect)\b",
    r"\bwhatsapp video (call|pe) (aao|raho)\b",
    r"\bghar (mat|nahi) (jao|jaana|niklo)\b",
]

# ── EXPANDED SCAM TAXONOMY ────────────────────────────────────────────────────

INDIA_SCAM_TAXONOMY = {
    "Fake KYC / Bank Verification": {
        "description": "Fraudsters impersonate banks asking to update KYC",
        "keywords": [
            "KYC update", "KYC expired", "KYC pending", "account blocked",
            "account suspended", "verify account", "bank verification",
            "link Aadhaar", "update PAN", "net banking blocked",
        ],
        "sample_messages": [
            "Dear SBI customer, your KYC is expired. Update now at http://sbi-kyc.xyz or account will be blocked in 24 hours.",
            "HDFC Bank: Your account will be suspended due to incomplete KYC. Click here to update: bit.ly/hdfc-kyc",
            "Aapka SBI account band ho jayega. Abhi KYC update karein: 9876543210 par call karein.",
            "Your Aadhaar-linked bank account needs KYC update. Share OTP received on your mobile.",
            "ICICI Bank Alert: Net banking access blocked. Update KYC at icici-verify.in within 48 hours.",
        ],
        "red_flags": [
            "Unofficial URL", "Urgency language", "OTP request",
            "Asks to call unknown number", "Threatens account block",
        ],
    },

    "UPI / Payment Scam": {
        "description": "Scammers trick victims into sending money via UPI",
        "keywords": [
            "UPI", "Google Pay", "PhonePe", "Paytm", "QR code",
            "scan to receive", "refund", "cashback", "payment link",
        ],
        "sample_messages": [
            "Congratulations! Rs.15000 cashback credited. Scan QR code on Google Pay to collect.",
            "OLX buyer: I'll pay via UPI. Please scan this QR code to receive Rs.8000.",
            "Your PhonePe account credited Rs.5000. Enter UPI PIN at phonepe-reward.xyz to receive.",
            "Paytm: Refund of Rs.2500 pending. Click link to receive: paytm-refund.xyz",
            "Aapko Rs.10000 ka cashback mila hai. Google Pay par ye QR scan karein.",
        ],
        "red_flags": [
            "QR code to receive money (you never need PIN to receive)",
            "Unofficial payment links", "Too-good-to-be-true cashback",
        ],
    },

    "Job Fraud": {
        "description": "Fake job offers requiring registration fees",
        "keywords": [
            "work from home", "part time", "earn per day",
            "registration fee", "training fee", "data entry",
            "simple tasks", "no experience", "immediate joining",
        ],
        "sample_messages": [
            "Work from home! Earn Rs.5000/day doing simple data entry. Pay Rs.500 registration. WhatsApp: 9876543210",
            "Amazon hiring! Part time job Rs.800/hour. Like YouTube videos. Registration Rs.299.",
            "Ghar baithe kaam karein! Rs.3000 roz kamayein. Sirf Rs.200 registration fee.",
            "Urgent hiring: Online survey job. Rs.50 per survey. 100 surveys/day possible. Join fee Rs.999.",
            "Flipkart work from home. Package 45k/month. Send Rs.1000 security deposit to confirm.",
        ],
        "red_flags": [
            "Registration/training fee required", "Unrealistic earnings",
            "WhatsApp-only contact", "No company verification possible",
        ],
    },

    "Courier / Parcel Scam": {
        "description": "Fake customs/CBI calls about illegal parcels",
        "keywords": [
            "parcel", "courier", "customs", "FedEx", "DHL",
            "illegal items", "drugs", "CBI", "arrest", "clearance fee",
        ],
        "sample_messages": [
            "Mumbai Customs: Your FedEx parcel contains drugs. Pay Rs.25000 clearance or face arrest. Call: 9876543210",
            "CBI officer: Aadhaar-linked parcel seized with illegal items. Pay Rs.15000 to close case.",
            "Your Amazon parcel held at Delhi customs. Drugs found. Pay Rs.8000 release fee immediately.",
            "Ye CBI se bol raha hoon. Aapke naam ka parcel pakda gaya hai. Abhi call karein.",
            "DTDC: Your package contains banned substances. Pay customs duty Rs.5000 to release.",
        ],
        "red_flags": [
            "Threatens arrest", "Demands immediate payment",
            "Real agencies never call for money", "Digital arrest threat",
        ],
    },

    "Lottery / Prize Scam": {
        "description": "Fake lottery wins requiring processing fees",
        "keywords": [
            "won", "winner", "lottery", "prize", "KBC",
            "lucky draw", "congratulations", "claim", "processing fee",
        ],
        "sample_messages": [
            "Congratulations! Your number won Rs.25 Lakh in KBC Lucky Draw. Contact: 9876543210. Claim in 24 hours.",
            "Jio Lucky Subscriber: You won Rs.10 Lakh. Pay Rs.2500 processing fee to claim.",
            "Aapne Rs.50 Lakh ka inaam jeeta hai! Claim karne ke liye Rs.5000 processing fee bhejein.",
            "Your mobile number selected in Airtel Lucky Draw. Prize: iPhone 15. Pay Rs.1500 delivery.",
            "Amazon Great Sale Winner: You won Rs.1 Crore. Send Rs.10000 tax clearance to claim.",
        ],
        "red_flags": [
            "You cannot win lottery you didn't enter",
            "Processing/delivery fee for prize",
            "Urgency to claim", "Unverifiable organization",
        ],
    },

    "Authority Impersonation": {
        "description": "Scammers pose as TRAI, CBI, IT Dept, Police",
        "keywords": [
            "TRAI", "CBI", "Income Tax", "police", "RBI",
            "government notice", "legal action", "FIR", "arrest warrant",
        ],
        "sample_messages": [
            "TRAI Notice: Your mobile will be disconnected in 2 hours due to illegal activities. Press 9.",
            "Income Tax Dept: Refund Rs.18500 approved. Update bank at incometax-refund.xyz",
            "RBI: Your account involved in money laundering. Call CBI officer: 9876543210",
            "Ye Delhi Police se bol raha hoon. Aapke naam FIR darj hui hai. Abhi settle karein.",
            "ED Notice: Your property attached for tax evasion. Pay Rs.50000 to avoid arrest.",
        ],
        "red_flags": [
            "Government never calls for money",
            "Threatens arrest/FIR", "Asks for immediate payment",
            "Digital arrest via video call",
        ],
    },

    "Electricity / Utility Bill Scam": {
        "description": "Fake disconnection threats from electricity boards",
        "keywords": [
            "electricity", "bijli", "BESCOM", "MSEDCL", "BSES",
            "disconnection", "overdue", "last warning", "tonight",
        ],
        "sample_messages": [
            "BESCOM: Electricity disconnected tonight 9:30 PM. Overdue bill. Pay: http://bescom-pay.xyz",
            "MSEDCL Alert: Last warning. Pay Rs.1847 via UPI: 9876543210@paytm or disconnection.",
            "Bijli vibhag: Aapka bijli connection aaj raat band ho jayega. Abhi pay karein.",
            "BSES: Your electricity meter will be removed due to unpaid dues. Pay Rs.2340 immediately.",
            "UPPCL: Final notice. Electricity supply disconnected in 2 hours. Pay at uppcl-pay.in",
        ],
        "red_flags": [
            "Unofficial payment URL", "Urgency (tonight/2 hours)",
            "UPI to unknown number", "No official account number",
        ],
    },

    "OTP Theft": {
        "description": "Scammers trick victims into sharing OTPs",
        "keywords": [
            "OTP", "one time password", "verification code",
            "share OTP", "tell OTP", "bank executive",
        ],
        "sample_messages": [
            "SBI: We're updating security. Share OTP with our executive to complete process.",
            "Bank executive calling: Please share OTP for KYC verification. Secure process.",
            "Aapke phone par OTP aaya hoga. Woh OTP humein batayein account verify karne ke liye.",
            "HDFC: Your account upgrade pending. Share OTP received on mobile with our team.",
            "Paytm KYC: Share OTP sent to your number to complete video KYC process.",
        ],
        "red_flags": [
            "Banks NEVER ask for OTP",
            "OTP is personal — never share",
            "Legitimate KYC never needs OTP sharing",
        ],
    },

    "Digital Arrest Scam": {
        "description": "New scam: victims kept on video call under fake 'digital arrest'",
        "keywords": [
            "digital arrest", "video call", "Skype", "WhatsApp call",
            "don't leave home", "stay connected", "CBI headquarters",
        ],
        "sample_messages": [
            "CBI: You are under digital arrest. Stay on WhatsApp video call. Do not leave home.",
            "Narcotics Bureau: Digital arrest issued. Connect on Skype: cbi.officer@skype immediately.",
            "Aap digital arrest mein hain. Ghar se mat niklein. Video call par connected rahein.",
            "Supreme Court order: You must remain on video call for 48 hours. Disconnect = arrest.",
            "ED officer: Digital arrest warrant issued. Pay Rs.5 Lakh to avoid physical arrest.",
        ],
        "red_flags": [
            "No such thing as 'digital arrest' in Indian law",
            "Real agencies never conduct video call arrests",
            "Designed to isolate and extort victim",
        ],
    },

    "Investment / Trading Scam": {
        "description": "Fake investment schemes promising high returns",
        "keywords": [
            "investment", "trading", "stock market", "crypto",
            "guaranteed returns", "double money", "profit",
        ],
        "sample_messages": [
            "Join our Telegram group for guaranteed 50% monthly returns on stock tips. Min invest Rs.5000.",
            "Crypto trading bot: 300% returns guaranteed. Invest Rs.10000, get Rs.30000 in 7 days.",
            "SEBI registered advisor: Guaranteed 40% annual returns. Limited slots. Invest now.",
            "Hamara trading group mein join karein. Roz Rs.2000-5000 kamayein. Sirf Rs.1000 fee.",
            "Bitcoin investment: Double your money in 30 days. 100% guaranteed. WhatsApp: 9876543210",
        ],
        "red_flags": [
            "Guaranteed returns (no investment is guaranteed)",
            "Telegram-only groups", "Pressure to invest quickly",
            "Unregistered with SEBI",
        ],
    },
}

# ── WHITELIST PATTERNS (Legitimate Indian Messages) ───────────────────────────

INDIA_LEGITIMATE_PATTERNS = {
    "Bank Transaction Alerts": [
        r"\bdebited\s+(?:Rs\.?|INR)\s*[\d,]+.*?(?:Txn|Ref|UPI)\s*(?:ID|No|Ref)[:\s]*[A-Z0-9]{6,}",
        r"\bcredited\s+(?:Rs\.?|INR)\s*[\d,]+.*?(?:Txn|Ref)\s*(?:ID|No)[:\s]*[A-Z0-9]{6,}",
        r"\bAvail(?:able)?\s+[Bb]al(?:ance)?\s*(?:Rs\.?|INR|:)\s*[\d,]+",
        r"\bA/c\s+[Xx*]+\d{4}\b",
        r"\bIMPS|NEFT|RTGS\b.*\bRef\s*No[:\s]*[A-Z0-9]{6,}",
    ],
    "IRCTC Tickets": [
        r"\bPNR\s*[:\s]*\d{10}\b",
        r"\bTrain\s*(?:No\.?|Number)?\s*\d{5}\b",
        r"\bCoach\s*[A-Z]\d+\b",
        r"\bBerth\s*(?:No\.?)?\s*\d+\b",
        r"\birctc\.co\.in\b",
    ],
    "Official Govt Messages": [
        r"\buidai\.gov\.in\b",
        r"\bincometax(?:india)?\.gov\.in\b",
        r"\bgstn\.org\.in\b",
        r"\bepfindia\.gov\.in\b",
        r"\bRef(?:erence)?\s*(?:No\.?|ID)[:\s]*[A-Z0-9\-]{8,}",
    ],
    "Telecom OTP (Legitimate)": [
        r"\b(?:OTP|One.?Time.?Password)\s*(?:for|to)\s*(?:login|verify|register|activate)\b",
        r"\bDo\s+NOT\s+share\s+(?:this\s+)?OTP\b",
        r"\bValid\s+for\s+\d+\s+(?:minutes?|mins?)\b",
    ],
    "Delivery Updates": [
        r"\bOut\s+for\s+delivery\b",
        r"\bDelivered\s+(?:successfully|to)\b",
        r"\bTracking\s*(?:ID|No\.?)[:\s]*[A-Z0-9]{8,}",
        r"\bExpected\s+delivery\s*:\s*\d{2}[-/]\w{3}[-/]\d{4}\b",
    ],
}

# ── RISK WEIGHT ADJUSTMENTS ───────────────────────────────────────────────────

# These patterns increase risk score significantly
HIGH_RISK_BOOSTERS = [
    (r"\bdigital arrest\b", 40, "Digital arrest scam"),
    # Courier/Parcel scam Hindi patterns
    (r"\bparcel\b.{0,50}\b(?:pakda|roka|seized|drugs|illegal|banned)\b", 40, "Parcel scam threat"),
    (r"\b(?:drugs|illegal|banned|narcotics)\b.{0,50}\bparcel\b", 40, "Parcel drugs threat"),
    (r"\bcustoms\b.{0,50}\b(?:duty|fee|charge|bharo|pay|bhejein)\b", 35, "Customs fee demand"),
    (r"\b(?:FedEx|DHL|BlueDart|DTDC|Delhivery)\b.{0,80}\b(?:seized|held|drugs|illegal|pakda)\b", 35, "Courier scam"),
    (r"\bparcel\b.{0,50}\b(?:arrest|giraftari|pakad|gaya|roka)\b", 35, "Parcel arrest threat"),
    (r"\b(?:customs|CBI|narcotics)\b.{0,80}\b(?:parcel|package|courier)\b", 35, "Authority parcel scam"),
    (r"\bpakda\s+gaya\b", 30, "Hindi seized/caught language"),
    (r"\b(?:arrest|giraftari)\b.{0,50}\b(?:hoga|ho\s+jayega|karenge|kar\s+denge)\b", 35, "Arrest threat Hindi"),
    (r"\bshare\s+(?:your\s+)?OTP\b", 35, "OTP sharing request"),
    (r"\bregistration\s+fee\b", 30, "Registration fee demand"),
    (r"\bclearance\s+fee\b", 35, "Clearance fee demand"),
    (r"\bprocessing\s+fee\b", 30, "Processing fee demand"),
    (r"\bsecurity\s+deposit\b", 30, "Security deposit demand"),
    (r"http[s]?://(?!(?:www\.)?(?:sbi|hdfc|icici|irctc|uidai|incometax|bescom|msedcl|phonepe|paytm|googlepay|amazon|flipkart)\.(?:co\.in|gov\.in|com|org\.in|net\.in))", 25, "Unofficial URL"),
    (r"\benter\s+(?:your\s+)?(?:UPI\s+)?PIN\b", 35, "UPI PIN entry request"),
    (r"\bscan\s+(?:this\s+)?QR\s+(?:code\s+)?to\s+receive\b", 30, "Fake QR receive scam"),
    (r"\bvideo\s+call\s+(?:par|pe|on)\s+(?:rehna|raho|stay)\b", 40, "Digital arrest video call"),
    (r"\bguaranteed\s+(?:\d+%|returns|profit|income)\b", 25, "Guaranteed returns claim"),
    (r"\bdouble\s+(?:your\s+)?money\b", 30, "Double money scam"),
    (r"\bCBI\s+(?:officer|headquarters|notice)\b", 25, "CBI impersonation"),
    (r"\bnarcotics\b", 30, "Narcotics threat"),
    (r"\bFIR\s+(?:darj|register|file)\b", 25, "FIR threat"),
    (r"\barrest\s+(?:warrant|hoga|kar|karenge)\b", 30, "Arrest threat"),
    # Universal spam patterns (UK/International)
    (r"\b150p(?:pm|/msg)?\b", 20, "UK premium rate SMS"),
    (r"\bringtone\b.*\bfree\b", 20, "Free ringtone scam"),
    (r"\bfree\s+entry\b.*\bcomp\b", 25, "Competition entry scam"),
    (r"\bwkly\s+comp\b", 25, "Weekly competition scam"),
    (r"\bunredeemed\s+(?:points|bonus)\b", 25, "Unredeemed points scam"),
    (r"\bbonus\s+caller\s+prize\b", 30, "Bonus caller prize scam"),
    (r"\bprivate.*account\s+statement\b", 25, "Fake account statement"),
    (r"\bsim\s+points\b", 20, "SIM points scam"),
    (r"\b(?:prize|award|reward)\b.*\bguaranteed\b", 25, "Guaranteed prize claim"),
    (r"\bguaranteed\b.*\b(?:prize|award|reward|cash)\b", 25, "Guaranteed prize claim"),
    (r"\bclaim\b.*\b(?:prize|award|reward)\b.*\bcall\b", 25, "Claim prize by calling"),
    (r"\bmobile.*upgrade.*free\b", 20, "Free mobile upgrade scam"),
    (r"\bfree.*mobile.*upgrade\b", 20, "Free mobile upgrade scam"),
    (r"\bsubscription\b.*\bcharged\b", 20, "Subscription charge scam"),
]
