"""Intel endpoints — trending, experiences, company profiles, scraping."""
import sys
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Query
from typing import Optional

BASE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE))

router = APIRouter()


@router.get("/stats")
async def intel_stats():
    try:
        from intel.db import get_overall_stats
        return get_overall_stats() or {"total_experiences": 0, "companies": 0}
    except Exception as e:
        return {"error": str(e), "total_experiences": 0}


@router.get("/experiences")
async def get_experiences(
    company: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = Query(default=20, le=100),
):
    try:
        from intel.db import search_experiences
        results = search_experiences(company=company, role=role, limit=limit)
        # Scrub sensitive fields before returning
        clean = []
        for r in results:
            r.pop("body_raw", None)   # Don't expose full scraped text
            clean.append(r)
        return {"experiences": clean, "count": len(clean)}
    except Exception as e:
        return {"experiences": [], "error": str(e)}


@router.get("/trending")
async def get_trending(
    company: Optional[str] = None,
    days: int = Query(default=30, le=90),
):
    try:
        from intel.analyzer import get_trending_topics
        return get_trending_topics(company=company, days=days)
    except Exception as e:
        return {"error": str(e)}


@router.get("/resources")
async def get_resources(cat: Optional[str] = None):
    try:
        from intel.resources import get_resources
        return {"resources": get_resources(category=cat)}
    except Exception as e:
        return {"resources": [], "error": str(e)}


@router.get("/company/{company_name}")
async def company_profile(company_name: str):
    try:
        from intel.analyzer import get_company_summary
        return get_company_summary(company_name)
    except Exception as e:
        return {"error": str(e)}


def _run_scrape(source: Optional[str]):
    """Background job: run scraper."""
    try:
        from intel.scraper import run_scraper
        stats = run_scraper(source_name=source, verbose=False)
        return stats
    except Exception as e:
        return {"error": str(e)}


@router.post("/scrape")
async def trigger_scrape(background_tasks: BackgroundTasks, source: Optional[str] = None):
    """Trigger scraping in background — returns immediately."""
    background_tasks.add_task(_run_scrape, source)
    return {"ok": True, "message": f"Scraping {'all sources' if not source else source} in background"}
