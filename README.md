# 🛡️ Suraksham AI 2.0

> India's AI Shield Against Digital Fraud — Microsoft Agentic AI Hackathon

Suraksham AI is a privacy-first, India-focused fraud detection ecosystem that detects suspicious messages, phishing URLs, and scam calls in real time using a multi-agent AI pipeline powered by Groq LLaMA 3.3-70b.

## 📊 Performance

| Metric | Score |
|--------|-------|
| F1 Score | **97.6%** on Indian fraud dataset |
| Recall Rate | **100%** — no scam missed |
| Response Time | **< 2s** powered by Groq |
| Scam Types | **14** India-specific categories |

## 🏗️ Project Structure

```
suraksham-ai/
├── backend/          # FastAPI + multi-agent backend (Groq LLaMA 3.3-70b)
├── website/          # Next.js 14 cyber awareness portal
├── android/          # Kotlin + Jetpack Compose mobile app
└── docker-compose.yml
```

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Fill in your API keys
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

### Website
```bash
cd website
npm install
cp .env.local.example .env.local
npm run dev
```

### Android
Open `android/` in Android Studio and run on emulator or device.

### Docker (Full Stack)
```bash
docker-compose up --build
```

## 🧠 Architecture

```
Input (SMS / URL / Call)
  → Privacy Scrubber        — masks PAN, Aadhaar, phone, UPI IDs
  → Decision Router         — routes to message / url / call agent
  → [Message Classifier | URL Agent | Call Agent]
  → Risk Scorer             — 4-dimension scoring + India-specific boosters
  → Explainability Engine   — evidence chain, verdict agreement
  → Response
```

### Agent Pipeline

| Agent | Role |
|-------|------|
| Privacy Scrubber | Masks all PII before any external API call |
| Message Classifier | Groq LLaMA 3.3-70b classifies scam type + guidance |
| URL Agent | 789k phishing pattern engine + Google Safe Browsing + WHOIS |
| Call Agent | Same pipeline as message classifier, tuned for call summaries |
| Risk Scorer | 4-dimension keyword scoring + India-specific boosters |
| Explainability | Evidence chain, authenticity score, dual-verdict agreement |

## 🎯 Scam Categories Detected

| # | Category |
|---|----------|
| 1 | Fake KYC / Bank Verification |
| 2 | UPI / Payment Scams |
| 3 | Job Fraud |
| 4 | Courier / Parcel Scams |
| 5 | Lottery / Prize Scams |
| 6 | Authority Impersonation (CBI, ED, Police, TRAI) |
| 7 | Electricity / Utility Bill Scams |
| 8 | OTP Theft |
| 9 | Digital Arrest Scam |
| 10 | Investment / Stock Market Scam |
| 11 | Aadhaar / PAN Scam |
| 12 | Ransomware / Malware |
| 13 | Social Media Scam |
| 14 | Romance / Sextortion Scam |

## 🔒 Privacy First

All messages are scrubbed of PAN, Aadhaar, phone numbers, UPI IDs, and bank account numbers **before** any LLM or external API call. Original messages are never stored.

## 📊 Risk Scoring

| Score | Status | Meaning |
|-------|--------|---------|
| 0–20 | 🟢 Safe | No significant threat indicators |
| 21–60 | 🟡 Suspicious | Some risk signals detected |
| 61–100 | 🔴 High Risk | Multiple strong fraud indicators |

### Scoring Dimensions (0–25 each)
- **Urgency** — time pressure, account blocking threats
- **Authority Impersonation** — fake RBI, CBI, SBI, TRAI, etc.
- **Payment Pressure** — UPI, NEFT, transfer requests
- **Deception / Fear** — fake prizes, KYC, OTP requests, digital arrest

India-specific pattern boosters add up to +50 on top of the base score.

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze/message` | Analyze SMS / chat / email |
| POST | `/analyze/url` | Check URL for phishing |
| POST | `/analyze/call` | Analyze call summary |
| GET | `/news-feed/` | Live cyber fraud news feed |
| GET | `/news-feed/stats` | News feed statistics |
| POST | `/news-feed/refresh` | Force news cache refresh |
| POST | `/report-scam/` | Submit community scam report |
| GET | `/health` | Service health check |
| GET | `/docs` | Interactive API docs (Swagger) |

## 📰 Cyber News Feed

Live news scraped from 8 RSS sources with 30-minute cache:
- Economic Times, India Today, The Hindu, Hindustan Times
- NDTV, Times of India, Mint, News18

Falls back to 12 curated India-specific scam alerts covering all major categories. Supports filtering by severity (`HIGH` / `MEDIUM`) and scam type.

## 🔗 URL Analysis

The URL agent combines three detection layers:
1. **Phishing pattern engine** — trained on 789,054 real phishing URLs ([mitchellkrogza/Phishing.Database](https://github.com/mitchellkrogza/Phishing.Database))
2. **Google Safe Browsing API** — real-time threat lookup
3. **WHOIS domain age** — flags newly registered domains (< 90 days)
4. **Brand impersonation detection** — India + global brands

## 📱 Android App

Built with Kotlin + Jetpack Compose. Screens:

| Screen | Description |
|--------|-------------|
| Home | Dashboard with quick actions |
| Scan | Manual message / URL / call analysis |
| Shield | Permission management for background scanning |
| History | Past scan results |
| News | Live cyber fraud news feed |
| Report | Community scam reporting |

Background features:
- **SMS Receiver** — auto-scans incoming SMS
- **Call Receiver** — monitors incoming calls
- **Boot Receiver** — restarts scanner service on device reboot
- **Scanner Service** — foreground service for continuous protection

## 📦 Tech Stack

| Layer | Tech |
|-------|------|
| Mobile | Kotlin + Jetpack Compose + Retrofit |
| Backend | FastAPI + Python 3.11 |
| LLM | Groq LLaMA 3.3-70b (default) · OpenAI · Azure · Gemini |
| NLP | spaCy + Regex pattern engine |
| URL Analysis | 789k phishing patterns + Google Safe Browsing + WHOIS |
| Website | Next.js 14 + Tailwind CSS |
| Database | Firebase / Supabase (optional) |
| Containerization | Docker + Docker Compose |
| Hosting | Render (backend) · Vercel (website) |

## ⚙️ Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

```env
# Primary LLM (Groq is default and fastest)
GROQ_API_KEY=your_groq_api_key

# Optional LLM providers
OPENAI_API_KEY=
GOOGLE_API_KEY=

# LLM selection: groq | openai | azure | gemini
LLM_PROVIDER=groq
LLM_MODEL=llama-3.3-70b-versatile

# URL analysis
GOOGLE_SAFE_BROWSING_API_KEY=your_key

# Optional storage
SUPABASE_URL=
SUPABASE_KEY=
```

## 🆘 Emergency Resources

- **Cyber Crime Helpline**: [1930](tel:1930)
- **Report Online**: [cybercrime.gov.in](https://cybercrime.gov.in)
- **CERT-In Advisories**: [cert-in.org.in](https://cert-in.org.in)
