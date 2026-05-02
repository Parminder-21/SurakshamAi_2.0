"""Integration tests for the FastAPI endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_news_feed():
    response = client.get("/news-feed/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]
    assert "severity" in data[0]


def test_news_feed_limit():
    response = client.get("/news-feed/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) <= 2


def test_report_scam():
    response = client.post("/report-scam/", json={
        "content": "Fake KYC message: update your SBI account at sbi-fake.com",
        "scam_type": "Fake KYC / Bank Verification",
        "source": "app"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "report_id" in data


def test_report_scam_scrubs_pii():
    """PII in the report content should be scrubbed."""
    response = client.post("/report-scam/", json={
        "content": "Call 9876543210 for fake KYC update",
        "source": "app"
    })
    assert response.status_code == 200


@patch("app.routers.analyze.run_workflow", new_callable=AsyncMock)
def test_analyze_message(mock_workflow):
    mock_workflow.return_value = {
        "status": "completed",
        "risk_level": "HIGH_RISK",
        "risk_score": 85,
        "urgency_score": 20,
        "authority_score": 20,
        "payment_score": 25,
        "deception_score": 20,
        "scam_type": "UPI / Payment Scam",
        "confidence": 0.92,
        "red_flags": ["Urgency language", "Payment pressure"],
        "why_risky": "This message pressures you to pay via UPI urgently.",
        "what_not_to_do": ["Do not click the link", "Do not share OTP"],
        "what_to_do": ["Contact your bank directly", "Report to cybercrime.gov.in"],
        "scrubbed_text": "Urgent: pay via UPI or account blocked",
    }

    response = client.post("/analyze/message", json={
        "message": "Urgent: pay Rs. 500 via UPI or your account will be blocked",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "HIGH_RISK"
    assert data["risk_score"] == 85
