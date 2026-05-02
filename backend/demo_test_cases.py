"""
Suraksham AI — Demo Test Cases
Run: python demo_test_cases.py
Tests the 5 key scam scenarios for the hackathon demo.
"""
import asyncio
from app.orchestration.workflow import run_workflow


DEMO_CASES = [
    {
        "name": "🔴 UPI Scam",
        "input": (
            "URGENT: Your SBI account will be blocked in 24 hours! "
            "Update KYC immediately at http://sbi-kyc-update.xyz "
            "Pay Rs. 1 via UPI to verify. Share OTP: 9876543210"
        ),
        "type": "message",
    },
    {
        "name": "🔴 Fake Job Fraud",
        "input": (
            "Congratulations! You have been selected for a work-from-home job. "
            "Earn Rs. 5000 per day. Pay Rs. 500 registration fee to start. "
            "Contact HR at hr@jobs-india-fake.com"
        ),
        "type": "message",
    },
    {
        "name": "🔴 Courier Scam (CBI Impersonation)",
        "input": (
            "This is CBI officer Sharma. Your parcel from FedEx contains illegal items. "
            "You will be arrested unless you pay Rs. 25,000 clearance fee immediately. "
            "Call back on 9876543210 within 2 hours."
        ),
        "type": "call",
    },
    {
        "name": "🟡 Suspicious Lottery",
        "input": (
            "You have won Rs. 10 Lakh in the KBC lottery! "
            "To claim your prize, contact us with your bank details."
        ),
        "type": "message",
    },
    {
        "name": "🟢 Safe Message",
        "input": (
            "Your electricity bill of Rs. 1,250 is due on 15th June 2024. "
            "Pay via the official BESCOM app or website bescom.org"
        ),
        "type": "message",
    },
]


async def run_demo():
    print("\n" + "=" * 60)
    print("  🛡️  SURAKSHAM AI — DEMO TEST CASES")
    print("=" * 60)

    for case in DEMO_CASES:
        print(f"\n{case['name']}")
        print("-" * 40)
        print(f"Input: {case['input'][:80]}...")

        state = await run_workflow(
            raw_input=case["input"],
            input_type=case["type"],
        )

        print(f"Risk Level : {state.get('risk_level', 'N/A')}")
        print(f"Risk Score : {state.get('risk_score', 0)}/100")
        print(f"Scam Type  : {state.get('scam_type', 'N/A')}")
        print(f"Confidence : {state.get('confidence', 0):.0%}")
        if state.get("red_flags"):
            print(f"Red Flags  : {', '.join(state['red_flags'])}")
        print(f"Scrubbed   : {state.get('scrubbed_text', '')[:60]}...")

    print("\n" + "=" * 60)
    print("  Demo complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_demo())
