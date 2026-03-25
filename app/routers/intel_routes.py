"""Intel endpoints — trending, experiences, company profiles, scraping, manual import."""
import sys
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List

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


# ─── Manual Import (Blind / enginebogie paste) ───────────────────────────────

class ManualImportRequest(BaseModel):
    source: str          # "blind", "enginebogie", "linkedin", "other"
    company: str
    role: str = "SDE-2"
    title: str
    body: str            # paste the full post text
    result: str = "unknown"  # "offer", "reject", "unknown"
    url: str = ""


@router.post("/import")
async def manual_import(body: ManualImportRequest):
    """
    Manually import a Blind/enginebogie/LinkedIn interview experience.
    Use this when you read a useful post and want to save it to the intel DB.

    Example: copy a Blind post about Razorpay interview → paste here → saved to DB
    and will appear in /api/intel/experiences?company=razorpay
    """
    try:
        from intel.db import insert_experience
        exp = {
            "source":         body.source,
            "source_id":      f"manual_{body.source}_{hash(body.title) % 100000}",
            "company":        body.company,
            "role":           body.role,
            "title":          body.title,
            "body_raw":       body.body[:8000],
            "overall_result": body.result,
            "url":            body.url,
            "rounds":         [],
            "date_posted":    None,
        }
        exp_id = insert_experience(exp)
        return {"saved": bool(exp_id), "id": exp_id, "company": body.company}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/import/guide")
async def import_guide():
    """How to manually import from Blind, enginebogie, etc."""
    return {
        "blind": {
            "status": "Manual only (login-required JS SPA, cannot auto-scrape)",
            "steps": [
                "1. Go to teamblind.com → search your target company",
                "2. Read interview experience posts",
                "3. Copy the post title + body text",
                "4. POST to /api/intel/import with source='blind'",
                "Or use CLI: prep scraper --add  (prompts for fields)",
            ],
            "best_searches": [
                "Razorpay interview experience",
                "PhonePe SDE-2 interview",
                "Flipkart machine coding round",
                "Swiggy system design interview",
            ]
        },
        "enginebogie": {
            "status": "Manual only (React SPA with login)",
            "steps": [
                "1. Go to enginebogie.com/interview/experiences",
                "2. Filter by company + SDE-2 level",
                "3. Copy post text → POST to /api/intel/import with source='enginebogie'",
            ]
        },
        "reddit": {
            "status": "Automated (with OAuth keys) or fallback public API",
            "setup": [
                "1. Go to reddit.com/prefs/apps → create 'script' app",
                "2. Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to Railway env vars",
                "3. Trigger: POST /api/intel/scrape?source=reddit",
            ]
        },
        "leetcode_discuss": {
            "status": "Automated (no keys needed — GraphQL public API)",
            "trigger": "POST /api/intel/scrape?source=leetcode_discuss",
        }
    }
