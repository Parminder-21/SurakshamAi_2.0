"""
/news-feed endpoints
Real cyber fraud news scraped from:
  - CERT-In, PIB, RBI, TRAI (official sources)
  - Times of India, NDTV, India Today, Economic Times, The Hindu (RSS)
  - Curated fallback data for all 12 India scam categories

Cache: 30-minute TTL, auto-refreshes in background.
"""
import asyncio
import logging
from datetime import datetime
from fastapi import APIRouter, Query, BackgroundTasks, HTTPException
from typing import List, Optional

from app.models.schemas import NewsFeedItem
from app.agents.news_scraper import get_news_cached, force_refresh

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news-feed", tags=["News Feed"])


def _to_schema(item: dict) -> NewsFeedItem:
    return NewsFeedItem(
        id=item["id"],
        title=item["title"],
        slug=item["slug"],
        summary=item["summary"],
        scam_type=item["scam_type"],
        severity=item["severity"],
        report_count=item["report_count"],
        published_at=item["published_at"],
        tags=item.get("tags", []),
        source_name=item.get("source_name"),
        source_url=item.get("source_url"),
    )


@router.get(
    "/",
    response_model=List[NewsFeedItem],
    summary="Get live cyber fraud news feed",
    description="""
Returns real-time cyber fraud news scraped from:
- **Official**: CERT-In, PIB, RBI, TRAI
- **News**: Times of India, NDTV, India Today, Economic Times, The Hindu
- **Fallback**: 12 curated India-specific scam alerts

Cache TTL: 30 minutes. Use `?refresh=true` to force refresh.
    """,
)
async def get_news_feed(
    background_tasks: BackgroundTasks,
    limit: int = Query(default=20, ge=1, le=100, description="Number of items to return"),
    severity: Optional[str] = Query(default=None, description="Filter: HIGH | MEDIUM | LOW"),
    scam_type: Optional[str] = Query(default=None, description="Filter by scam type keyword"),
    refresh: bool = Query(default=False, description="Force cache refresh"),
):
    """Fetch live cyber fraud news from scraped + curated sources."""
    if refresh:
        items = await force_refresh()
    else:
        items = await get_news_cached()

    # Filter by severity
    if severity:
        items = [i for i in items if i.get("severity", "").upper() == severity.upper()]

    # Filter by scam type keyword
    if scam_type:
        kw = scam_type.lower()
        items = [
            i for i in items
            if kw in i.get("scam_type", "").lower()
            or kw in i.get("title", "").lower()
            or any(kw in t.lower() for t in i.get("tags", []))
        ]

    return [_to_schema(i) for i in items[:limit]]


@router.get(
    "/stats",
    summary="Get news feed statistics",
)
async def get_news_stats():
    """Return stats about the current news feed."""
    items = await get_news_cached()
    scam_types = {}
    for item in items:
        st = item.get("scam_type", "Unknown")
        scam_types[st] = scam_types.get(st, 0) + 1

    return {
        "total_items": len(items),
        "high_risk": sum(1 for i in items if i.get("severity") == "HIGH"),
        "medium_risk": sum(1 for i in items if i.get("severity") == "MEDIUM"),
        "total_reports": sum(i.get("report_count", 0) for i in items),
        "scam_type_breakdown": scam_types,
        "sources": list({i.get("source_name", "Unknown") for i in items}),
        "last_updated": datetime.now().isoformat(),
    }


@router.post(
    "/refresh",
    summary="Force refresh news cache",
)
async def refresh_news():
    """Manually trigger a news cache refresh from all sources."""
    items = await force_refresh()
    return {
        "success": True,
        "items_fetched": len(items),
        "message": f"Refreshed {len(items)} news items from all sources",
        "timestamp": datetime.now().isoformat(),
    }


@router.get(
    "/{item_id}",
    response_model=NewsFeedItem,
    summary="Get a single news item by ID or slug",
)
async def get_news_item(item_id: str):
    """Fetch a single news item by its ID or slug."""
    items = await get_news_cached()
    for item in items:
        if item["id"] == item_id or item["slug"] == item_id:
            return _to_schema(item)
    raise HTTPException(status_code=404, detail=f"News item '{item_id}' not found")
