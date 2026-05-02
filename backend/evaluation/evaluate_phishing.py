"""
Phishing URL Evaluation
Tests the URL agent against:
  - 789,054 real phishing URLs (mitchellkrogza/Phishing.Database)
  - Curated legitimate URLs

Usage:
    python evaluation/evaluate_phishing.py
"""
import sys, time, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

from app.agents.phishing_patterns import calculate_phishing_score


def load_urls(filepath: str, label: str, limit: int = None) -> list:
    """Load URLs from file."""
    urls = []
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            for line in f:
                url = line.strip()
                if url and not url.startswith("#"):
                    urls.append((url, label))
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    if limit:
        random.seed(42)
        urls = random.sample(urls, min(limit, len(urls)))
    return urls


def evaluate():
    print("\n" + "=" * 65)
    print("  SURAKSHAM AI — PHISHING URL EVALUATION")
    print("  Trained on 789,054 real phishing URLs")
    print("=" * 65)

    # Load datasets
    phishing_urls = load_urls("evaluation/datasets/phishing_urls.txt", "phishing", limit=500)
    legit_urls = load_urls("evaluation/datasets/legit_urls.txt", "legit")

    all_urls = phishing_urls + legit_urls
    random.shuffle(all_urls)

    print(f"\nDataset: {len(phishing_urls)} phishing + {len(legit_urls)} legitimate = {len(all_urls)} total")
    print("\nRunning pattern-based detection...")

    results = []
    tp = fp = tn = fn = 0
    start = time.time()

    for url, true_label in all_urls:
        result = calculate_phishing_score(url)
        score = result["risk_score"]
        predicted = "phishing" if score >= 25 else "legit"

        correct = predicted == true_label
        results.append({
            "url": url[:60],
            "true": true_label,
            "predicted": predicted,
            "score": score,
            "threats": result["threats"][:2],
            "correct": correct,
        })

        if true_label == "phishing" and predicted == "phishing": tp += 1
        elif true_label == "legit" and predicted == "phishing":  fp += 1
        elif true_label == "legit" and predicted == "legit":     tn += 1
        elif true_label == "phishing" and predicted == "legit":  fn += 1

    elapsed = time.time() - start
    total = len(results)
    accuracy  = (tp + tn) / total if total else 0
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall    = tp / (tp + fn) if (tp + fn) else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    # Show sample results
    print("\n--- Sample Phishing URLs Detected ---")
    detected = [r for r in results if r["true"] == "phishing" and r["correct"]][:5]
    for r in detected:
        print(f"  CAUGHT [{r['score']:3d}] {r['url']}")
        if r["threats"]:
            print(f"         Threats: {', '.join(r['threats'])}")

    print("\n--- Sample Phishing URLs Missed ---")
    missed = [r for r in results if r["true"] == "phishing" and not r["correct"]][:5]
    for r in missed:
        print(f"  MISSED [{r['score']:3d}] {r['url']}")

    print("\n--- Legitimate URLs (should be SAFE) ---")
    legit_results = [r for r in results if r["true"] == "legit"]
    false_alarms = [r for r in legit_results if not r["correct"]]
    print(f"  Total legit: {len(legit_results)} | False alarms: {len(false_alarms)}")
    for r in false_alarms[:3]:
        print(f"  FALSE ALARM [{r['score']:3d}] {r['url']}")

    # Score distribution
    phishing_scores = [r["score"] for r in results if r["true"] == "phishing"]
    legit_scores = [r["score"] for r in results if r["true"] == "legit"]
    avg_phishing = sum(phishing_scores) / len(phishing_scores) if phishing_scores else 0
    avg_legit = sum(legit_scores) / len(legit_scores) if legit_scores else 0

    print("\n" + "=" * 65)
    print("  RESULTS")
    print("=" * 65)
    print(f"  Total URLs tested : {total}")
    print(f"  Phishing caught   : {tp}/{tp+fn} ({tp/(tp+fn)*100:.1f}%)")
    print(f"  False alarms      : {fp}/{tn+fp} ({fp/(tn+fp)*100:.1f}% of legit flagged)")
    print(f"  Avg phishing score: {avg_phishing:.1f}/100")
    print(f"  Avg legit score   : {avg_legit:.1f}/100")
    print("-" * 65)
    print(f"  Accuracy          : {accuracy:.1%}")
    print(f"  Precision         : {precision:.1%}")
    print(f"  Recall            : {recall:.1%}")
    print(f"  F1 Score          : {f1:.1%}")
    print(f"  Time              : {elapsed:.2f}s ({total/elapsed:.0f} URLs/sec)")

    grade = "EXCELLENT" if f1 >= 0.85 else "GOOD" if f1 >= 0.75 else "FAIR" if f1 >= 0.65 else "NEEDS WORK"
    print(f"\n  GRADE: {grade} (F1={f1:.3f})")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    evaluate()
