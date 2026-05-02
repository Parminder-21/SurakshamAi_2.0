"""Tests for the Privacy Scrubber Agent."""
import pytest
from app.agents.privacy_scrubber import scrub, scrub_text


def test_phone_number_masked():
    result = scrub("Call me at 9876543210 for details")
    assert "9876543210" not in result.scrubbed_text
    assert "[PHONE]" in result.scrubbed_text
    assert result.entities_found.get("phone", 0) == 1


def test_pan_masked():
    result = scrub("My PAN is ABCDE1234F please verify")
    assert "ABCDE1234F" not in result.scrubbed_text
    assert "[PAN]" in result.scrubbed_text


def test_aadhaar_masked():
    result = scrub("Aadhaar number: 1234 5678 9012")
    assert "1234 5678 9012" not in result.scrubbed_text
    assert "[AADHAAR]" in result.scrubbed_text


def test_upi_masked():
    result = scrub("Send money to user@paytm immediately")
    assert "user@paytm" not in result.scrubbed_text
    assert "[UPI_ID]" in result.scrubbed_text


def test_email_masked():
    result = scrub("Contact us at support@sbi-fake.com")
    assert "support@sbi-fake.com" not in result.scrubbed_text
    assert "[EMAIL]" in result.scrubbed_text


def test_clean_text_unchanged():
    clean = "Your electricity bill is due next week."
    result = scrub(clean)
    assert result.scrubbed_text == clean
    assert result.entities_found == {}


def test_multiple_pii_types():
    text = "Call 9876543210 or email me@bank.com, PAN: ABCDE1234F"
    result = scrub(text)
    assert "9876543210" not in result.scrubbed_text
    assert "me@bank.com" not in result.scrubbed_text
    assert "ABCDE1234F" not in result.scrubbed_text


def test_scrub_text_convenience():
    result = scrub_text("My number is 9876543210")
    assert "[PHONE]" in result
    assert "9876543210" not in result
