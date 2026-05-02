"""
/report-scam endpoint — community scam reporting
Scrubs PII before storing, feeds into training pipeline.
"""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models.schemas import ReportScamRequest, ReportScamResponse
from app.agents.privacy_scrubber import scrub_text

router = APIRouter(prefix="/report-scam", tags=["Community Reporting"])

# In production, store in Firebase/Supabase
_report_store: list = []


@router.post("/", response_model=ReportScamResponse, summary="Report a scam message or URL")
async def report_scam(request: ReportScamRequest):
    """
    Submit a scam message or URL for community review.
    PII is automatically scrubbed before storage.
    """
    scrubbed_content = scrub_text(request.content)

    report = {
        "id": str(uuid.uuid4()),
        "content": scrubbed_content,
        "scam_type": request.scam_type,
        "source": request.source,
        "reporter_note": request.reporter_note,
        "status": "pending_review",
        "submitted_at": datetime.utcnow().isoformat(),
    }

    _report_store.append(report)

    return ReportScamResponse(
        success=True,
        report_id=report["id"],
        message="Thank you! Your report has been submitted for review. It will help protect others.",
    )


@router.get("/count", summary="Get total report count")
async def get_report_count():
    return {"total_reports": len(_report_store)}
