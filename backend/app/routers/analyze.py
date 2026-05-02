"""
/analyze endpoints — core fraud detection API
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AnalyzeMessageRequest, AnalyzeURLRequest, AnalyzeCallRequest,
    AnalysisResult, URLAnalysisResult, RiskScoreBreakdown, RiskLevel, ScamType,
)
from app.orchestration.workflow import run_workflow
from app.agents.url_agent import analyze_url

router = APIRouter(prefix="/analyze", tags=["Analysis"])


def _state_to_result(state: dict, language: str) -> AnalysisResult:
    """Convert workflow state to AnalysisResult response model."""
    if state.get("status") == "error":
        raise HTTPException(status_code=500, detail=state.get("error", "Analysis failed"))

    breakdown = RiskScoreBreakdown(
        urgency_score=state.get("urgency_score", 0),
        authority_impersonation_score=state.get("authority_score", 0),
        payment_pressure_score=state.get("payment_score", 0),
        deception_fear_score=state.get("deception_score", 0),
        total=state.get("risk_score", 0),
    )

    scam_type_str = state.get("scam_type", "Unknown / General Scam")
    try:
        scam_type = ScamType(scam_type_str)
    except ValueError:
        scam_type = ScamType.UNKNOWN

    # Build explainability detail
    from app.models.schemas import ExplainabilityDetail
    explain_obj = state.get("explainability")
    explainability = None
    if explain_obj:
        explainability = ExplainabilityDetail(
            evidence_chain=[
                f"{e.category}: {e.pattern_name} — {e.matched_text}"
                for e in explain_obj.evidence_chain[:8]
            ],
            keyword_verdict=explain_obj.keyword_verdict,
            llm_verdict=explain_obj.llm_verdict,
            verdicts_agree=explain_obj.verdicts_agree,
            authenticity_score=explain_obj.authenticity_score,
            authenticity_label=explain_obj.authenticity_label,
            decision_summary=explain_obj.decision_summary,
            triggered_rules=explain_obj.triggered_rules,
        )

    return AnalysisResult(
        risk_level=RiskLevel(state.get("risk_level", "SAFE")),
        risk_score=state.get("risk_score", 0),
        score_breakdown=breakdown,
        scam_type=scam_type,
        confidence=state.get("confidence", 0.5),
        red_flags=state.get("red_flags", []),
        why_risky=state.get("why_risky", ""),
        what_not_to_do=state.get("what_not_to_do", []),
        what_to_do=state.get("what_to_do", []),
        scrubbed_text=state.get("scrubbed_text", ""),
        language=language,
        explainability=explainability,
    )


@router.post("/message", response_model=AnalysisResult, summary="Analyze a suspicious message")
async def analyze_message(request: AnalyzeMessageRequest):
    """
    Analyze an SMS, chat message, or email for fraud indicators.
    PII is scrubbed before any LLM call.
    """
    state = await run_workflow(
        raw_input=request.message,
        input_type="message",
        language=request.language,
    )
    return _state_to_result(state, request.language)


@router.post("/url", response_model=URLAnalysisResult, summary="Check a URL for phishing")
async def check_url(request: AnalyzeURLRequest):
    """
    Check a URL against Google Safe Browsing, WHOIS, and brand impersonation patterns.
    """
    result = await analyze_url(request.url)
    return result


@router.post("/call", response_model=AnalysisResult, summary="Analyze a call summary")
async def analyze_call(request: AnalyzeCallRequest):
    """
    Analyze a typed or transcribed call summary for scam indicators.
    """
    state = await run_workflow(
        raw_input=request.summary,
        input_type="call",
        language=request.language,
    )
    return _state_to_result(state, request.language)
