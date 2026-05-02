"""
LangGraph-style Workflow Orchestrator
Defines the agent graph: nodes + conditional edges + execution order.

Flow:
  START
    → privacy_scrubber
    → decision_router (message | url | call)
    → [message_classifier | url_agent | call_agent]
    → risk_scorer
    → guidance_agent
    → END
"""
import re
from typing import Literal

from app.orchestration.state import SurakshaState
from app.agents import privacy_scrubber, risk_scorer, message_classifier, url_agent


# ── Node Functions ───────────────────────────────────────────────────────────

async def node_privacy_scrubber(state: SurakshaState) -> SurakshaState:
    """Mask all PII before any external API call."""
    result = privacy_scrubber.scrub(state["raw_input"])
    return {
        **state,
        "scrubbed_text": result.scrubbed_text,
        "entities_masked": result.entities_found,
    }


def node_decision_router(state: SurakshaState) -> Literal["message", "url", "call"]:
    """Route to the appropriate agent based on input type."""
    input_type = state.get("input_type", "message")
    if input_type == "url":
        return "url"
    elif input_type == "call":
        return "call"
    return "message"


async def node_message_classifier(state: SurakshaState) -> SurakshaState:
    """Classify the message type and generate guidance."""
    result = await message_classifier.classify_message(
        state["scrubbed_text"],
        language=state.get("language", "en"),
    )
    return {
        **state,
        "scam_type": result["scam_type"],
        "confidence": result["confidence"],
        "why_risky": result["why_risky"],
        "what_not_to_do": result["what_not_to_do"],
        "what_to_do": result["what_to_do"],
    }


async def node_url_agent(state: SurakshaState) -> SurakshaState:
    """Analyze a URL for phishing indicators."""
    url = state["raw_input"].strip()
    result = await url_agent.analyze_url(url)
    return {
        **state,
        "url_result": result,
        "scam_type": "Phishing URL" if not result.is_safe else "Safe",
        "confidence": 0.9,
        "why_risky": result.recommendation,
        "what_not_to_do": ["Do not open this link", "Do not enter any credentials"],
        "what_to_do": ["Verify the official website directly", "Report to cybercrime.gov.in"],
    }


async def node_call_agent(state: SurakshaState) -> SurakshaState:
    """Analyze a call summary (same pipeline as message)."""
    result = await message_classifier.classify_message(
        state["scrubbed_text"],
        language=state.get("language", "en"),
    )
    return {
        **state,
        "scam_type": result["scam_type"],
        "confidence": result["confidence"],
        "why_risky": result["why_risky"],
        "what_not_to_do": result["what_not_to_do"],
        "what_to_do": result["what_to_do"],
    }


def node_risk_scorer(state: SurakshaState) -> SurakshaState:
    """Calculate the 0-100 risk score and generate explainability report."""
    text = state.get("scrubbed_text", state.get("raw_input", ""))
    result = risk_scorer.calculate_risk_score(text)

    # If URL agent already set a high risk, blend scores
    url_result = state.get("url_result")
    if url_result:
        url_score = url_result.risk_score
        blended = max(result.breakdown.total, url_score)
        result.breakdown.total = blended
        if blended > 70:
            result.risk_level = risk_scorer.RiskLevel.HIGH_RISK
        elif blended > 30:
            result.risk_level = risk_scorer.RiskLevel.SUSPICIOUS

    # Generate explainability report
    from app.agents.explainability import generate_report
    explain = generate_report(
        text=text,
        keyword_risk_level=result.risk_level,
        llm_scam_type=state.get("scam_type", "Unknown / General Scam"),
        llm_confidence=state.get("confidence", 0.5),
    )

    return {
        **state,
        "risk_score": result.breakdown.total,
        "urgency_score": result.breakdown.urgency_score,
        "authority_score": result.breakdown.authority_impersonation_score,
        "payment_score": result.breakdown.payment_pressure_score,
        "deception_score": result.breakdown.deception_fear_score,
        "risk_level": result.risk_level.value,
        "red_flags": result.red_flags,
        "explainability": explain,
        "status": "completed",
    }


# ── Graph Execution ──────────────────────────────────────────────────────────

async def run_workflow(
    raw_input: str,
    input_type: str = "message",
    language: str = "en",
) -> SurakshaState:
    """
    Execute the full Suraksham AI workflow.
    Returns the final state with all analysis results.
    """
    state: SurakshaState = {
        "raw_input": raw_input,
        "input_type": input_type,
        "language": language,
        "status": "running",
    }

    try:
        # Step 1: Privacy scrubber (always first)
        state = await node_privacy_scrubber(state)

        # Step 2: Route to appropriate agent
        route = node_decision_router(state)
        if route == "url":
            state = await node_url_agent(state)
        elif route == "call":
            state = await node_call_agent(state)
        else:
            state = await node_message_classifier(state)

        # Step 3: Risk scoring
        state = node_risk_scorer(state)

    except Exception as e:
        state["status"] = "error"
        state["error"] = str(e)

    return state
