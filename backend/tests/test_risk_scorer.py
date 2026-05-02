"""Tests for the Risk Scoring Engine."""
import pytest
from app.agents.risk_scorer import calculate_risk_score
from app.models.schemas import RiskLevel


def test_safe_message():
    result = calculate_risk_score("Your electricity bill of Rs. 450 is due on 15th June.")
    assert result.risk_level == RiskLevel.SAFE
    assert result.breakdown.total <= 20


def test_high_risk_upi_scam():
    msg = (
        "URGENT: Your SBI account will be blocked immediately! "
        "Update KYC now by clicking this link and paying Rs. 1 via UPI. "
        "Share OTP to verify. Do not delay!"
    )
    result = calculate_risk_score(msg)
    assert result.risk_level == RiskLevel.HIGH_RISK
    assert result.breakdown.total > 70


def test_suspicious_message():
    msg = "Congratulations! You have won a prize. Click the link to claim."
    result = calculate_risk_score(msg)
    assert result.risk_level in (RiskLevel.SUSPICIOUS, RiskLevel.HIGH_RISK)
    assert result.breakdown.total > 0


def test_score_breakdown_sums_correctly():
    msg = "Urgent: Pay Rs. 500 via UPI to avoid account suspension. RBI notice."
    result = calculate_risk_score(msg)
    breakdown = result.breakdown
    calculated_total = (
        breakdown.urgency_score
        + breakdown.authority_impersonation_score
        + breakdown.payment_pressure_score
        + breakdown.deception_fear_score
    )
    assert breakdown.total == calculated_total


def test_red_flags_populated_for_high_risk():
    msg = "URGENT: RBI notice — pay Rs. 5000 via UPI or account blocked. Share OTP now!"
    result = calculate_risk_score(msg)
    assert len(result.red_flags) > 0
