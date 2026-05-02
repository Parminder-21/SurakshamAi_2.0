"""
Suraksham AI — Model Evaluation Script
=========================================
Tests our fraud detection model against a real dataset.

Usage:
    python evaluation/evaluate.py --file evaluation/datasets/spam.csv
    python evaluation/evaluate.py --file evaluation/datasets/fraud_sms.csv --limit 100

Supported CSV formats:
    - columns: text, label         (label: spam/ham or 1/0)
    - columns: message, category
    - columns: sms, type
    - columns: Message, Class
"""

import asyncio
import argparse
import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from app.agents.risk_scorer import calculate_risk_score
from app.agents.privacy_scrubber import scrub_text
from app.agents.message_classifier import classify_message


# ── Dataset Loader ────────────────────────────────────────────────────────────

def detect_columns(headers: list) -> tuple:
    """Auto-detect text and label columns from CSV headers."""
    headers_lower = [h.lower().strip() for h in headers]

    text_candidates  = ["text", "message", "sms", "msg", "content", "body"]
    label_candidates = ["label", "category", "type", "class", "spam", "target"]

    text_col = label_col = None
    for c in text_candidates:
        if c in headers_lower:
            text_col = headers[headers_lower.index(c)]
            break

    for c in label_candidates:
        if c in headers_lower:
            label_col = headers[headers_lower.index(c)]
            break

    return text_col, label_col


def normalize_label(label: str) -> str:
    """Normalize various label formats to 'spam' or 'ham'."""
    label = str(label).lower().strip()
    if label in ["spam", "1", "fraud", "scam", "phishing", "yes", "true"]:
        return "spam"
    return "ham"


def load_dataset(filepath: str, limit: int = None) -> list:
    """Load CSV dataset and return list of (text, true_label) tuples."""
    rows = []
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        text_col, label_col = detect_columns(list(headers))

        if not text_col or not label_col:
            print(f"ERROR: Could not detect columns. Found: {headers}")
            print("Expected columns like: text/message/sms AND label/category/type")
            sys.exit(1)

        print(f"Detected columns — Text: '{text_col}' | Label: '{label_col}'")

        for row in reader:
            text  = row.get(text_col, "").strip()
            label = normalize_label(row.get(label_col, "ham"))
            if text:
                rows.append((text, label))
            if limit and len(rows) >= limit:
                break

    return rows


# ── Prediction ────────────────────────────────────────────────────────────────

def predict_with_scorer(text: str) -> str:
    """Fast keyword-based prediction (no API call)."""
    scrubbed = scrub_text(text)
    result   = calculate_risk_score(scrubbed)
    return "spam" if result.risk_level.value in ("SUSPICIOUS", "HIGH_RISK") else "ham"


async def predict_with_llm(text: str) -> str:
    """LLM-based prediction via Groq (slower but more accurate)."""
    scrubbed = scrub_text(text)
    result   = await classify_message(scrubbed)
    scam_type = result.get("scam_type", "Safe")
    return "ham" if scam_type == "Safe" else "spam"


# ── Metrics ───────────────────────────────────────────────────────────────────

def compute_metrics(results: list) -> dict:
    """Compute accuracy, precision, recall, F1."""
    tp = fp = tn = fn = 0
    for true, pred in results:
        if true == "spam" and pred == "spam": tp += 1
        elif true == "ham"  and pred == "spam": fp += 1
        elif true == "ham"  and pred == "ham":  tn += 1
        elif true == "spam" and pred == "ham":  fn += 1

    total    = tp + fp + tn + fn
    accuracy = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall    = tp / (tp + fn) if (tp + fn) else 0
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) else 0)

    return {
        "total": total, "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "accuracy": accuracy, "precision": precision,
        "recall": recall, "f1": f1,
    }


def print_report(metrics: dict, mode: str, elapsed: float):
    print("\n" + "=" * 55)
    print(f"  SURAKSHAM AI — EVALUATION REPORT ({mode.upper()})")
    print("=" * 55)
    print(f"  Total samples   : {metrics['total']}")
    print(f"  True Positives  : {metrics['tp']}  (spam correctly caught)")
    print(f"  False Positives : {metrics['fp']}  (ham wrongly flagged)")
    print(f"  True Negatives  : {metrics['tn']}  (ham correctly passed)")
    print(f"  False Negatives : {metrics['fn']}  (spam missed)")
    print("-" * 55)
    print(f"  Accuracy        : {metrics['accuracy']:.1%}")
    print(f"  Precision       : {metrics['precision']:.1%}")
    print(f"  Recall          : {metrics['recall']:.1%}")
    print(f"  F1 Score        : {metrics['f1']:.1%}")
    print(f"  Time taken      : {elapsed:.1f}s")
    print("=" * 55)

    # Grade
    f1 = metrics["f1"]
    if f1 >= 0.90:
        grade = "EXCELLENT"
    elif f1 >= 0.80:
        grade = "GOOD"
    elif f1 >= 0.70:
        grade = "FAIR"
    else:
        grade = "NEEDS IMPROVEMENT"
    print(f"  Grade           : {grade} (F1={f1:.2f})")
    print("=" * 55 + "\n")


# ── Main ──────────────────────────────────────────────────────────────────────

async def run_evaluation(filepath: str, limit: int, use_llm: bool):
    print(f"\nLoading dataset: {filepath}")
    rows = load_dataset(filepath, limit)
    print(f"Loaded {len(rows)} samples")

    spam_count = sum(1 for _, l in rows if l == "spam")
    ham_count  = len(rows) - spam_count
    print(f"Distribution — Spam: {spam_count} | Ham: {ham_count}")

    results = []
    start   = time.time()
    mode    = "LLM (Groq)" if use_llm else "Keyword Scorer"

    print(f"\nRunning predictions using: {mode}")
    print("Progress: ", end="", flush=True)

    for i, (text, true_label) in enumerate(rows):
        if use_llm:
            pred = await predict_with_llm(text)
            await asyncio.sleep(0.1)  # Respect rate limits
        else:
            pred = predict_with_scorer(text)

        results.append((true_label, pred))

        if (i + 1) % 10 == 0:
            print(f"{i+1}", end=" ", flush=True)

    elapsed = time.time() - start
    print("\n")

    metrics = compute_metrics(results)
    print_report(metrics, mode, elapsed)

    # Save results to CSV
    out_path = Path(filepath).parent / f"results_{Path(filepath).stem}.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "true_label", "predicted", "correct"])
        for (text, true), (_, pred) in zip(rows, results):
            writer.writerow([text[:80], true, pred, true == pred])
    print(f"Detailed results saved to: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Suraksham AI on a dataset")
    parser.add_argument("--file",  required=True, help="Path to CSV dataset file")
    parser.add_argument("--limit", type=int, default=200, help="Max samples to test (default: 200)")
    parser.add_argument("--llm",   action="store_true", help="Use LLM (Groq) instead of keyword scorer")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"ERROR: File not found: {args.file}")
        print(f"Place your dataset in: backend/evaluation/datasets/")
        sys.exit(1)

    asyncio.run(run_evaluation(args.file, args.limit, args.llm))
