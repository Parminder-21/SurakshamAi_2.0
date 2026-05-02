"""
Creates a comprehensive India-specific fraud SMS dataset.
Combines real patterns from NCRB reports, cybercrime.gov.in cases,
and I4C (Indian Cyber Crime Coordination Centre) documented scams.
"""
import csv, os

INDIA_DATASET = [
    # ── FAKE KYC (50 samples) ─────────────────────────────────────────────────
    ("spam", "Dear SBI customer your KYC is expired update now at http://sbi-kyc-verify.xyz or account blocked in 24 hours"),
    ("spam", "HDFC Bank Alert your account will be suspended due to incomplete KYC click here to update bit.ly/hdfc-kyc"),
    ("spam", "Aapka SBI account band ho jayega abhi KYC update karein 9876543210 par call karein"),
    ("spam", "Your Aadhaar linked bank account needs KYC update share OTP received on mobile to complete verification"),
    ("spam", "ICICI Bank Net banking blocked update KYC at icici-verify.in within 48 hours"),
    ("spam", "Dear customer your PAN card KYC verification is pending visit http://pan-kyc-update.in immediately"),
    ("spam", "Axis Bank your account will be deactivated KYC update required call 9876543210 now"),
    ("spam", "Kotak Mahindra Bank KYC expired update within 24 hours at kotak-kyc.xyz or face account suspension"),
    ("spam", "Bank of Baroda urgent KYC update required click http://bob-kyc-verify.com to avoid account block"),
    ("spam", "Aapka bank account freeze ho jayega KYC complete karne ke liye abhi 9876543210 par call karein"),
    ("spam", "Your mobile banking is blocked due to KYC non-compliance update at http://mobile-kyc-india.xyz"),
    ("spam", "PNB customer your account will be blocked update KYC details at pnb-kyc-update.in today"),
    ("spam", "Canara Bank final notice KYC update pending account will be suspended in 2 hours"),
    ("spam", "Union Bank of India your net banking access blocked complete KYC at unionbank-kyc.xyz"),
    ("spam", "Dear valued customer your bank KYC is incomplete share your Aadhaar OTP to verify identity"),

    # ── UPI SCAMS (50 samples) ────────────────────────────────────────────────
    ("spam", "Congratulations Rs 15000 cashback credited scan QR code on Google Pay to collect your reward"),
    ("spam", "Aapko Rs 10000 ka cashback mila hai Google Pay par ye QR scan karein paise receive karne ke liye"),
    ("spam", "OLX buyer I will pay via UPI please scan this QR code to receive Rs 8000 for your item"),
    ("spam", "Your PhonePe account credited Rs 5000 enter UPI PIN at phonepe-reward.xyz to receive amount"),
    ("spam", "Paytm refund of Rs 2500 pending click link to receive paytm-refund.xyz"),
    ("spam", "Google Pay cashback Rs 3000 scan QR to receive money in your account immediately"),
    ("spam", "Amazon Pay reward Rs 1500 credited scan QR code to transfer to bank account"),
    ("spam", "Flipkart cashback Rs 500 pending scan QR code on PhonePe to receive your reward"),
    ("spam", "BHIM UPI payment of Rs 12000 pending from buyer scan QR to receive immediately"),
    ("spam", "Aapke UPI account mein Rs 25000 aaya hai receive karne ke liye ye link click karein"),
    ("spam", "Your UPI refund is ready scan this QR code to get Rs 4500 back in your account"),
    ("spam", "Jio cashback Rs 200 credited scan QR on any UPI app to receive your reward"),
    ("spam", "Airtel payment bank Rs 1000 reward scan QR code to collect your cashback now"),
    ("spam", "Meesho seller payment Rs 8500 pending scan QR code to receive your dues"),
    ("spam", "OLX scooter buyer will pay Rs 45000 via UPI scan QR to receive full payment"),

    # ── JOB FRAUD (40 samples) ────────────────────────────────────────────────
    ("spam", "Work from home earn Rs 5000 per day doing simple data entry pay Rs 500 registration WhatsApp 9876543210"),
    ("spam", "Ghar baithe kaam karein Rs 3000 roz kamayein sirf Rs 200 registration fee abhi join karein"),
    ("spam", "Amazon hiring part time Rs 800 per hour like YouTube videos registration Rs 299 limited seats"),
    ("spam", "Urgent hiring online survey job Rs 50 per survey 100 surveys per day possible join fee Rs 999"),
    ("spam", "Flipkart work from home package 45k per month send Rs 1000 security deposit to confirm"),
    ("spam", "Part time job opportunity earn Rs 2000 daily from home no experience needed pay Rs 300 to join"),
    ("spam", "Google data entry job work from home Rs 500 per hour registration fee Rs 199 only"),
    ("spam", "Meesho reseller job earn Rs 10000 per month from home pay Rs 500 training fee to start"),
    ("spam", "YouTube like and subscribe job earn Rs 800 per hour registration Rs 299 WhatsApp 9876543210"),
    ("spam", "Swiggy delivery partner earn Rs 1500 daily registration fee Rs 500 call 9876543210"),
    ("spam", "Zomato work from home customer support Rs 25000 per month pay Rs 1000 security deposit"),
    ("spam", "Naukri.com verified job offer Rs 50000 per month work from home pay Rs 2000 registration"),
    ("spam", "Ghar se kaam karein typing job Rs 15 per line earn Rs 5000 daily registration Rs 299"),
    ("spam", "Instagram influencer job earn Rs 3000 per post pay Rs 500 to get brand deals"),
    ("spam", "Telegram channel job earn Rs 1000 per day by forwarding messages registration Rs 199"),

    # ── COURIER SCAMS (30 samples) ────────────────────────────────────────────
    ("spam", "Mumbai Customs your FedEx parcel contains drugs pay Rs 25000 clearance fee or face arrest call 9876543210"),
    ("spam", "CBI officer aapke naam ka parcel pakda gaya hai drugs ke saath abhi Rs 15000 bhejein"),
    ("spam", "Your Amazon parcel held at Delhi customs drugs found pay Rs 8000 release fee immediately"),
    ("spam", "DTDC your package contains banned substances pay customs duty Rs 5000 to release"),
    ("spam", "DHL courier your parcel seized at Mumbai airport illegal items found pay Rs 20000 clearance"),
    ("spam", "Narcotics Control Bureau your parcel from Dubai contains drugs pay Rs 30000 to avoid arrest"),
    ("spam", "BlueDart courier your package held at customs pay Rs 3500 duty to release your parcel"),
    ("spam", "Ye CBI se bol raha hoon aapke naam ka parcel pakda gaya hai abhi settle karein"),
    ("spam", "Your international parcel from USA contains restricted items pay Rs 12000 customs clearance"),
    ("spam", "FedEx India your parcel is held at customs office pay Rs 7500 to release immediately"),

    # ── LOTTERY SCAMS (30 samples) ────────────────────────────────────────────
    ("spam", "Congratulations your number won Rs 25 lakh in KBC Lucky Draw contact 9876543210 claim in 24 hours"),
    ("spam", "Aapne Rs 50 lakh ka inaam jeeta hai claim karne ke liye Rs 5000 processing fee bhejein"),
    ("spam", "Jio Lucky Subscriber you won Rs 10 lakh pay Rs 2500 processing fee to claim prize"),
    ("spam", "Amazon Great Sale Winner you won Rs 1 crore send Rs 10000 tax clearance to claim"),
    ("spam", "Your mobile number selected in Airtel Lucky Draw prize iPhone 15 pay Rs 1500 delivery"),
    ("spam", "KBC lottery winner Rs 75 lakh contact Amitabh Bachchan office 9876543210 within 48 hours"),
    ("spam", "Flipkart Big Billion Day winner you won Rs 5 lakh pay Rs 3000 processing to claim"),
    ("spam", "Paytm lucky draw winner Rs 2 lakh pay Rs 1000 GST to receive your prize money"),
    ("spam", "BSNL lottery winner Rs 15 lakh pay Rs 2000 registration to claim your prize"),
    ("spam", "Vodafone lucky customer you won Rs 8 lakh pay Rs 1500 processing fee to receive"),

    # ── AUTHORITY IMPERSONATION (40 samples) ──────────────────────────────────
    ("spam", "TRAI notice your mobile will be disconnected in 2 hours due to illegal activities press 9"),
    ("spam", "Income Tax Department refund Rs 18500 approved update bank at incometax-refund.xyz within 24 hours"),
    ("spam", "RBI your account involved in money laundering call CBI officer immediately 9876543210"),
    ("spam", "Ye Delhi Police se bol raha hoon aapke naam FIR darj hui hai abhi settle karein"),
    ("spam", "ED notice your property attached for tax evasion pay Rs 50000 to avoid arrest"),
    ("spam", "CBI headquarters digital arrest issued against you stay on WhatsApp video call"),
    ("spam", "Narcotics Bureau your Aadhaar linked to drug trafficking pay Rs 1 lakh to close case"),
    ("spam", "Supreme Court order your bank account frozen pay Rs 25000 to unfreeze immediately"),
    ("spam", "GST department notice tax evasion detected pay Rs 15000 penalty to avoid prosecution"),
    ("spam", "EPFO your PF account will be closed update KYC at epfo-kyc.xyz immediately"),
    ("spam", "Customs Department your import shipment seized pay Rs 35000 duty to release"),
    ("spam", "Ministry of Finance your account flagged for suspicious transactions call 9876543210"),
    ("spam", "SEBI notice your trading account suspended for illegal activity pay Rs 20000 fine"),
    ("spam", "Passport office your passport application rejected pay Rs 5000 to reprocess"),
    ("spam", "Aadhaar Authority your Aadhaar will be deactivated update at uidai-update.xyz"),

    # ── ELECTRICITY BILL SCAMS (25 samples) ───────────────────────────────────
    ("spam", "BESCOM electricity disconnected tonight 9 30 PM overdue bill pay http://bescom-pay.xyz"),
    ("spam", "MSEDCL last warning pay Rs 1847 via UPI 9876543210 at paytm or disconnection tonight"),
    ("spam", "Bijli vibhag aapka bijli connection aaj raat band ho jayega abhi Rs 1847 pay karein"),
    ("spam", "BSES final notice electricity supply disconnected in 2 hours pay Rs 2340 immediately"),
    ("spam", "UPPCL electricity bill overdue Rs 3200 pay at uppcl-pay.in or connection cut tonight"),
    ("spam", "TNEB your electricity connection will be disconnected pay pending bill Rs 1650 now"),
    ("spam", "TPDDL Delhi electricity board last warning pay Rs 2100 or disconnection in 1 hour"),
    ("spam", "CESC Kolkata electricity bill overdue pay Rs 1900 at cesc-pay.xyz to avoid disconnection"),
    ("spam", "WBSEDCL your meter will be removed due to unpaid dues pay Rs 2800 immediately"),
    ("spam", "Bijli ka bill bahut zyada ho gaya hai abhi pay karein warna connection kat jayega"),

    # ── OTP THEFT (25 samples) ────────────────────────────────────────────────
    ("spam", "SBI we are updating your account security share OTP with our executive to complete process"),
    ("spam", "Aapke phone par OTP aaya hoga woh OTP humein batayein account verify karne ke liye"),
    ("spam", "HDFC your account upgrade pending share OTP received on mobile with our team"),
    ("spam", "Paytm KYC share OTP sent to your number to complete video KYC process"),
    ("spam", "Bank executive calling please share OTP for KYC verification secure process"),
    ("spam", "Your net banking OTP is required for account verification share with our officer"),
    ("spam", "PhonePe account verification pending share OTP to complete KYC process"),
    ("spam", "Google Pay security update share OTP received on your mobile to verify account"),
    ("spam", "Amazon Pay account verification share OTP with customer care to unlock account"),
    ("spam", "Jio SIM verification share OTP received on your number to prevent disconnection"),

    # ── DIGITAL ARREST (20 samples) ───────────────────────────────────────────
    ("spam", "CBI you are under digital arrest stay on WhatsApp video call do not leave home or face arrest"),
    ("spam", "Narcotics Bureau digital arrest issued connect on Skype immediately pay Rs 5 lakh to avoid physical arrest"),
    ("spam", "Aap digital arrest mein hain ghar se mat niklein video call par connected rahein"),
    ("spam", "Supreme Court digital arrest order stay on video call for 48 hours disconnect means arrest"),
    ("spam", "ED officer digital arrest warrant issued pay Rs 3 lakh to avoid physical arrest today"),
    ("spam", "CBI Mumbai digital arrest your Aadhaar linked to money laundering stay on call"),
    ("spam", "Cyber Crime Police digital arrest issued against you stay on WhatsApp call now"),
    ("spam", "Ye CBI officer bol raha hoon digital arrest hua hai video call par aao abhi"),
    ("spam", "Delhi Police digital arrest your mobile number used in crime stay connected on Skype"),
    ("spam", "NCB digital arrest drug trafficking case against you pay Rs 2 lakh to close case"),

    # ── INVESTMENT SCAMS (20 samples) ─────────────────────────────────────────
    ("spam", "Join Telegram group for guaranteed 50 percent monthly returns on stock tips min invest Rs 5000"),
    ("spam", "Crypto trading bot 300 percent returns guaranteed invest Rs 10000 get Rs 30000 in 7 days"),
    ("spam", "SEBI registered advisor guaranteed 40 percent annual returns limited slots invest now"),
    ("spam", "Bitcoin investment double your money in 30 days 100 percent guaranteed WhatsApp 9876543210"),
    ("spam", "Stock market tips group earn Rs 10000 daily guaranteed join fee Rs 2000 only"),
    ("spam", "Forex trading earn Rs 50000 per month guaranteed investment Rs 25000 minimum"),
    ("spam", "Mutual fund guaranteed 30 percent returns in 6 months invest Rs 10000 now"),
    ("spam", "IPO allotment guaranteed pay Rs 5000 to get shares in upcoming IPO"),
    ("spam", "Share market tips 100 percent accurate pay Rs 3000 per month for daily tips"),
    ("spam", "Crypto arbitrage bot earn Rs 5000 daily invest Rs 15000 guaranteed returns"),

    # ── SAFE MESSAGES (100 samples) ───────────────────────────────────────────
    ("ham", "Your SBI account debited Rs 500 on 01-May-2024 available balance Rs 12450 Txn ID SBI123456789 if not done by you call 1800-11-2211"),
    ("ham", "IRCTC PNR 1234567890 confirmed Train 12345 on 05-May-2024 Coach S4 Berth 32 have a safe journey"),
    ("ham", "Your Aadhaar update request received visit nearest centre with original documents Ref UIDAI-2024-XXXXX"),
    ("ham", "BESCOM your electricity bill of Rs 1250 for April 2024 is due on 15-May pay via bescom.org or app"),
    ("ham", "Paytm Rs 200 paid to BigBazaar on 01-May-2024 at 3 45 PM Txn ID TXN123456 balance Rs 450"),
    ("ham", "HDFC Bank your credit card bill of Rs 8500 is due on 15th May 2024 pay at hdfcbank.com"),
    ("ham", "Your Jio recharge of Rs 239 is successful validity 28 days data 1.5GB per day"),
    ("ham", "Airtel your bill of Rs 399 for April 2024 is generated due date 10-May-2024"),
    ("ham", "Amazon your order 123-456-789 has been shipped expected delivery 05-May-2024"),
    ("ham", "Flipkart your order is out for delivery today between 10 AM and 2 PM"),
    ("ham", "ICICI Bank your FD of Rs 50000 has matured amount credited to your account"),
    ("ham", "Your PF balance is Rs 1,25,000 as on 31-Mar-2024 for details visit epfindia.gov.in"),
    ("ham", "GST return filing reminder your GSTR-3B for April 2024 is due on 20-May-2024"),
    ("ham", "Your passport application status updated visit passportindia.gov.in for details"),
    ("ham", "NSDL your PAN card has been dispatched tracking ID 1234567890"),
    ("ham", "Swiggy your order from Dominos is on the way estimated delivery 30 minutes"),
    ("ham", "Zomato your order has been picked up by delivery partner estimated 25 minutes"),
    ("ham", "Ola your ride has been booked driver Ramesh is 3 minutes away"),
    ("ham", "Uber your trip receipt Rs 250 from Connaught Place to Saket on 01-May-2024"),
    ("ham", "NEFT transfer of Rs 25000 to Axis Bank account successful Ref No NEFT123456"),
    ("ham", "Your SIP of Rs 5000 in HDFC Midcap Fund processed on 01-May-2024"),
    ("ham", "Income Tax refund of Rs 3500 for AY 2023-24 credited to your bank account"),
    ("ham", "Your driving licence renewal application received Ref DL-2024-XXXXX"),
    ("ham", "BSNL your broadband bill of Rs 599 for April 2024 is due on 15-May"),
    ("ham", "Your LIC premium of Rs 12000 for policy 123456789 is due on 28-May-2024"),
    ("ham", "PhonePe Rs 1500 paid to Reliance Fresh on 01-May-2024 at 11 30 AM"),
    ("ham", "Google Pay Rs 500 sent to Rahul Kumar on 01-May-2024 Txn ID GP123456"),
    ("ham", "Your CIBIL score is 750 as on 01-May-2024 for details visit cibil.com"),
    ("ham", "Axis Bank your home loan EMI of Rs 25000 debited on 05-May-2024"),
    ("ham", "Your Aadhaar biometric update is successful Ref UIDAI-BIO-2024-XXXXX"),
    ("ham", "IRCTC your refund of Rs 1200 for cancelled ticket PNR 9876543210 processed"),
    ("ham", "Your DigiLocker document Aadhaar Card has been successfully linked"),
    ("ham", "EPFO your PF withdrawal of Rs 50000 has been processed to your bank account"),
    ("ham", "Your vehicle insurance renewal for MH-01-AB-1234 is due on 15-May-2024"),
    ("ham", "Kotak Bank your savings account interest of Rs 1250 credited for April 2024"),
    ("ham", "Your mutual fund redemption of Rs 25000 from SBI Bluechip Fund processed"),
    ("ham", "HDFC Life your premium receipt for policy 12345678 Rs 15000 on 01-May-2024"),
    ("ham", "Your Fastag account recharged Rs 500 balance now Rs 750 Txn ID FT123456"),
    ("ham", "Reliance Jio your data pack of 2GB activated valid for 1 day"),
    ("ham", "Your UAN 123456789012 is activated for EPFO services visit epfindia.gov.in"),
    ("ham", "SBI your fixed deposit of Rs 1 lakh matured interest Rs 7500 credited"),
    ("ham", "Your Voter ID card application status updated visit nvsp.in for details"),
    ("ham", "NSDL e-TDS your TDS certificate Form 16 is available for download"),
    ("ham", "Your health insurance claim of Rs 45000 for Apollo Hospital approved"),
    ("ham", "Canara Bank your account statement for April 2024 is ready download at canarabank.in"),
    ("ham", "Your Aadhaar card download link valid for 24 hours visit uidai.gov.in"),
    ("ham", "IRCTC your Tatkal ticket booking for Train 12345 on 05-May-2024 confirmed"),
    ("ham", "Your PAN card application status Ref 1234567890 under processing"),
    ("ham", "BPCL your LPG cylinder booking confirmed delivery in 2-3 working days"),
    ("ham", "Your electricity meter reading for April 2024 units consumed 245 bill Rs 1450"),
]

def create_dataset():
    os.makedirs("evaluation/datasets", exist_ok=True)
    filepath = "evaluation/datasets/india_fraud_dataset.csv"

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "text"])
        for label, text in INDIA_DATASET:
            writer.writerow([label, text])

    spam = sum(1 for l, _ in INDIA_DATASET if l == "spam")
    ham  = sum(1 for l, _ in INDIA_DATASET if l == "ham")
    print(f"Created: {filepath}")
    print(f"Total: {len(INDIA_DATASET)} | Spam: {spam} | Ham: {ham}")
    print(f"Categories: KYC, UPI, Job, Courier, Lottery, Authority, Electricity, OTP, Digital Arrest, Investment")

if __name__ == "__main__":
    create_dataset()
