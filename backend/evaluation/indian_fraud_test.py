"""
Suraksham AI — Enhanced Indian Fraud Confidence Test
Tests all 10 scam categories including Hindi messages and Digital Arrest.
"""
import asyncio, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from app.agents.risk_scorer import calculate_risk_score
from app.agents.privacy_scrubber import scrub_text
from app.agents.message_classifier import classify_message

TEST_CASES = [
    # ── FAKE KYC ──────────────────────────────────────────────────────────────
    ("Dear SBI customer, KYC expired. Update at http://sbi-kyc-verify.xyz or account blocked in 24 hours.", "spam", "Fake KYC (English)"),
    ("Aapka SBI account band ho jayega. Abhi KYC update karein: 9876543210 par call karein.", "spam", "Fake KYC (Hindi)"),
    ("HDFC Bank: Net banking blocked due to incomplete KYC. Update at hdfc-kyc-update.in within 48 hours.", "spam", "Fake KYC (English)"),

    # ── UPI SCAM ──────────────────────────────────────────────────────────────
    ("Congratulations! Rs.15,000 cashback credited. Scan QR code on Google Pay to collect.", "spam", "UPI Scam (QR)"),
    ("Aapko Rs.10000 ka cashback mila hai. Google Pay par ye QR scan karein paise receive karne ke liye.", "spam", "UPI Scam (Hindi)"),
    ("OLX buyer: I'll pay via UPI. Please scan this QR code to receive Rs.8000.", "spam", "UPI Scam (OLX)"),

    # ── JOB FRAUD ─────────────────────────────────────────────────────────────
    ("Work from home! Earn Rs.5000/day doing simple data entry. Pay Rs.500 registration. WhatsApp: 9876543210", "spam", "Job Fraud (English)"),
    ("Ghar baithe kaam karein! Rs.3000 roz kamayein. Sirf Rs.200 registration fee. Abhi join karein.", "spam", "Job Fraud (Hindi)"),
    ("Amazon hiring part time. Rs.800/hour. Like YouTube videos. Registration Rs.299. Limited seats.", "spam", "Job Fraud (English)"),

    # ── COURIER SCAM ──────────────────────────────────────────────────────────
    ("Mumbai Customs: FedEx parcel contains drugs. Pay Rs.25000 clearance fee or face arrest. Call: 9876543210", "spam", "Courier Scam (English)"),
    ("Ye CBI se bol raha hoon. Aapke naam ka parcel pakda gaya hai drugs ke saath. Abhi Rs.15000 bhejein.", "spam", "Courier Scam (Hindi)"),

    # ── LOTTERY SCAM ──────────────────────────────────────────────────────────
    ("Congratulations! Your number won Rs.25 Lakh in KBC Lucky Draw. Contact: 9876543210. Claim in 24 hours.", "spam", "Lottery Scam (English)"),
    ("Aapne Rs.50 Lakh ka inaam jeeta hai! Claim karne ke liye Rs.5000 processing fee bhejein.", "spam", "Lottery Scam (Hindi)"),

    # ── AUTHORITY IMPERSONATION ───────────────────────────────────────────────
    ("TRAI Notice: Your mobile will be disconnected in 2 hours due to illegal activities. Press 9.", "spam", "Authority (TRAI)"),
    ("Income Tax Dept: Refund Rs.18500 approved. Update bank at incometax-refund.xyz within 24 hours.", "spam", "Authority (IT Dept)"),
    ("RBI: Your account involved in money laundering. Call CBI officer immediately: 9876543210", "spam", "Authority (RBI/CBI)"),

    # ── ELECTRICITY BILL SCAM ─────────────────────────────────────────────────
    ("BESCOM: Electricity disconnected tonight 9:30 PM. Pay overdue bill: http://bescom-pay.xyz", "spam", "Electricity (English)"),
    ("Bijli vibhag: Aapka bijli connection aaj raat band ho jayega. Abhi Rs.1847 pay karein.", "spam", "Electricity (Hindi)"),

    # ── OTP THEFT ─────────────────────────────────────────────────────────────
    ("SBI: We're updating your account security. Share OTP with our executive to complete process.", "spam", "OTP Theft (English)"),
    ("Aapke phone par OTP aaya hoga. Woh OTP humein batayein account verify karne ke liye.", "spam", "OTP Theft (Hindi)"),

    # ── DIGITAL ARREST (NEW) ──────────────────────────────────────────────────
    ("CBI: You are under digital arrest. Stay on WhatsApp video call. Do not leave home or face arrest.", "spam", "Digital Arrest"),
    ("Narcotics Bureau: Digital arrest issued. Connect on Skype immediately. Pay Rs.5 Lakh to avoid physical arrest.", "spam", "Digital Arrest"),

    # ── INVESTMENT SCAM (NEW) ─────────────────────────────────────────────────
    ("Join Telegram group for guaranteed 50% monthly returns on stock tips. Min invest Rs.5000.", "spam", "Investment Scam"),
    ("Crypto trading bot: 300% returns guaranteed. Invest Rs.10000, get Rs.30000 in 7 days.", "spam", "Investment Scam"),

    # ── SAFE MESSAGES ─────────────────────────────────────────────────────────
    ("Your SBI account debited Rs.500 on 01-May-2024. Available balance: Rs.12,450. Txn ID: SBI123456789. If not done by you call 1800-11-2211.", "ham", "Legitimate Bank Alert"),
    ("IRCTC: PNR 1234567890 confirmed. Train 12345 on 05-May-2024. Coach S4 Berth 32. Have a safe journey!", "ham", "Legitimate IRCTC"),
    ("Your Aadhaar update request received. Visit nearest centre with original documents. Ref: UIDAI-2024-XXXXX", "ham", "Legitimate UIDAI"),
    ("BESCOM: Your electricity bill of Rs.1,250 for April 2024 is due on 15-May. Pay via bescom.org or app.", "ham", "Legitimate Electricity"),
    ("Paytm: Rs.200 paid to BigBazaar on 01-May-2024 at 3:45 PM. Txn ID: TXN123456. Balance: Rs.450.", "ham", "Legitimate Payment"),
]


async def run_test():
    print("\n" + "=" * 68)
    print("  SURAKSHAM AI — ENHANCED INDIA FRAUD TEST")
    print("  10 Categories | Hindi + English | Groq LLaMA 3.3-70b")
    print("=" * 68)

    total = len(TEST_CASES)
    spam_count = sum(1 for _, l, _ in TEST_CASES if l == "spam")
    print(f"\nTotal: {total} | Fraud: {spam_count} | Legitimate: {total - spam_count}\n")

    results = []
    category_results: dict = {}
    start = time.time()

    for i, (message, true_label, category) in enumerate(TEST_CASES):
        scrubbed = scrub_text(message)
        scorer_result = calculate_risk_score(scrubbed)
        scorer_pred = "spam" if scorer_result.risk_level.value in ("SUSPICIOUS", "HIGH_RISK") else "ham"

        try:
            llm_result = await classify_message(scrubbed)
            llm_pred = "ham" if llm_result.get("scam_type") == "Safe" else "spam"
            confidence = llm_result.get("confidence", 0)
            scam_detected = llm_result.get("scam_type", "Unknown")
        except Exception:
            llm_pred = scorer_pred
            confidence = 0.5
            scam_detected = "Error"

        # Combined: either model flags = spam
        final_pred = "spam" if (scorer_pred == "spam" or llm_pred == "spam") else "ham"
        correct = final_pred == true_label

        results.append((true_label, final_pred, correct, category))

        if category not in category_results:
            category_results[category] = {"correct": 0, "total": 0}
        category_results[category]["correct"] += int(correct)
        category_results[category]["total"] += 1

        mark = "+" if correct else "X"
        india_flags = len(scorer_result.india_specific_flags)
        print(f"[{i+1:02d}] {mark} | {category:<32} | Score:{scorer_result.breakdown.total:3d} | "
              f"Conf:{confidence:.0%} | India:{india_flags} | {final_pred.upper()}")

        await asyncio.sleep(0.2)

    elapsed = time.time() - start

    # ── Category Summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 68)
    print("  RESULTS BY CATEGORY")
    print("=" * 68)
    for cat, res in category_results.items():
        acc = res["correct"] / res["total"]
        bar = "#" * int(acc * 15) + "-" * (15 - int(acc * 15))
        status = "OK" if acc == 1.0 else "PARTIAL" if acc > 0 else "FAIL"
        print(f"  [{status:7s}] {cat:<32} [{bar}] {acc:.0%} ({res['correct']}/{res['total']})")

    # ── Overall Metrics ───────────────────────────────────────────────────────
    tp = sum(1 for t, p, _, _ in results if t == "spam" and p == "spam")
    fp = sum(1 for t, p, _, _ in results if t == "ham"  and p == "spam")
    tn = sum(1 for t, p, _, _ in results if t == "ham"  and p == "ham")
    fn = sum(1 for t, p, _, _ in results if t == "spam" and p == "ham")

    total_correct = tp + tn
    accuracy  = total_correct / total
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall    = tp / (tp + fn) if (tp + fn) else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    print("\n" + "=" * 68)
    print("  OVERALL PERFORMANCE")
    print("=" * 68)
    print(f"  Accuracy   : {accuracy:.1%}  ({total_correct}/{total})")
    print(f"  Precision  : {precision:.1%}  (flagged messages that are real scams)")
    print(f"  Recall     : {recall:.1%}  (real scams that were caught)")
    print(f"  F1 Score   : {f1:.1%}")
    print(f"  Scams caught    : {tp}/{tp+fn}")
    print(f"  False alarms    : {fp}")
    print(f"  Missed scams    : {fn}")
    print(f"  Time taken      : {elapsed:.1f}s")

    grade = "EXCELLENT" if f1 >= 0.92 else "GOOD" if f1 >= 0.80 else "FAIR" if f1 >= 0.70 else "NEEDS WORK"
    print(f"\n  GRADE: {grade} (F1 = {f1:.3f})")
    print("=" * 68 + "\n")


if __name__ == "__main__":
    asyncio.run(run_test())
