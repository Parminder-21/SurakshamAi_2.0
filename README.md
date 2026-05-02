# 🛡️ Suraksham AI

> AI-powered Cyber Safety & Fraud Detection — Microsoft Agentic AI Hackathon

Suraksham AI is a privacy-first, India-focused fraud detection ecosystem that helps users identify suspicious messages, phishing URLs, and scam calls in real time.

## 🏗️ Project Structure

```
suraksham-ai/
├── backend/          # FastAPI + LangGraph multi-agent backend
├── website/          # Next.js 14 cyber awareness portal
└── android/          # Kotlin + Jetpack Compose mobile app
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

### Website
```bash
cd website
npm install
cp .env.local.example .env.local
npm run dev
```

### Android
Open `android/` in Android Studio and run on emulator or device.

## 🧠 Architecture

- **Input Layer** — Android app, manual paste, URL input, call summary
- **Orchestration Layer** — LangGraph-style stateful multi-agent workflow
- **Intelligence Layer** — Privacy Scrubber, Message Classifier, URL Research, Call Context, Guidance, Risk Scoring agents
- **Risk Registry** — Shared state with score, flags, recommendations
- **Presentation Layer** — Risk status, score, explanation, action steps

## 🎯 Scam Categories Detected

1. Fake KYC / Bank Verification
2. UPI / Payment Scams
3. Job Fraud
4. Courier / Parcel Scams
5. Lottery / Prize Scams
6. Authority Impersonation (Police, IT Dept)
7. Electricity / Utility Bill Scams
8. OTP Theft

## 🔒 Privacy First

All messages are scrubbed of PAN, Aadhaar, phone numbers, and account IDs **before** any API call.

## 📊 Risk Scoring

| Score | Status | Color |
|-------|--------|-------|
| 0–30 | Safe | 🟢 Green |
| 31–70 | Suspicious | 🟡 Yellow |
| 71–100 | High Risk | 🔴 Red |

## 🌐 Website Features

- Trending scam news feed
- Searchable scam knowledge base
- Community scam reporting
- Admin dashboard + model retraining trigger
- Connected to mobile app via shared API

## 📱 Tech Stack

| Layer | Tech |
|-------|------|
| Mobile | Kotlin + Jetpack Compose |
| Backend | FastAPI + LangGraph/LangChain |
| LLM | OpenAI GPT-4 / Azure / Gemini |
| NLP | spaCy + Regex |
| Website | Next.js 14 + Tailwind CSS |
| Database | Firebase / Supabase |
| Hosting | Render / Vercel |
