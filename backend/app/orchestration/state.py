"""
Shared State — the Risk Registry that flows through all agents.
LangGraph-style TypedDict state object.
"""
from typing import TypedDict, List, Optional, Any


class SurakshaState(TypedDict, total=False):
    # Input
    raw_input: str
    input_type: str          # "message" | "url" | "call"
    language: str            # "en" | "hi"

    # After Privacy Scrubber
    scrubbed_text: str
    entities_masked: dict

    # After Message Classifier
    scam_type: str
    confidence: float
    why_risky: str
    what_not_to_do: List[str]
    what_to_do: List[str]

    # After Risk Scorer
    risk_score: int
    urgency_score: int
    authority_score: int
    payment_score: int
    deception_score: int
    risk_level: str          # "SAFE" | "SUSPICIOUS" | "HIGH_RISK"
    red_flags: List[str]

    # After URL Agent (if URL present)
    url_result: Optional[Any]

    # Explainability
    explainability: Optional[Any]

    # Final output
    status: str
    error: Optional[str]
