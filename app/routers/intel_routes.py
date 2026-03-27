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
        # Auto-enrich the newly imported experience with LLM
        if exp_id:
            try:
                from intel.exp_extractor import enrich_pending_experiences
                enrich_pending_experiences(limit=1)
            except Exception:
                pass
        return {"saved": bool(exp_id), "id": exp_id, "company": body.company}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/enrich")
async def enrich_experiences(background_tasks: BackgroundTasks, limit: int = 30):
    """
    LLM-enrich pending experiences (those with no body_summary).
    Runs in background. Use after scraping to extract real questions from raw posts.
    """
    def _do():
        try:
            from intel.exp_extractor import enrich_pending_experiences
            enrich_pending_experiences(limit=limit)
        except Exception:
            pass
    background_tasks.add_task(_do)
    return {"ok": True, "message": f"Enriching up to {limit} experiences with LLM in background"}


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


# ─── JD Analysis Endpoints ────────────────────────────────────────────────────


class JDUploadRequest(BaseModel):
    """Upload and analyze a job description."""
    jd_text: str
    company: str
    role: str = "SDE"
    level: Optional[str] = None


@router.post("/jd/upload")
async def upload_jd(body: JDUploadRequest):
    """
    Upload a JD and extract skills.

    1. Calls Claude to extract skills from JD text
    2. Predicts likely interview questions
    3. Stores in database
    4. Returns extracted skills with importance scores

    Example:
        POST /api/intel/jd/upload
        {
          "jd_text": "We are looking for SDE-2...",
          "company": "Amazon",
          "role": "Backend SDE-2",
          "level": "senior"
        }
    """
    import uuid
    from intel.jd_analyzer import extract_skills_from_jd, predict_interview_questions, store_jd

    try:
        jd_id = f"{body.company.lower()}_{body.role.lower()}_{uuid.uuid4().hex[:8]}"

        # Extract skills
        skills_data = extract_skills_from_jd(
            body.jd_text, body.company, body.role
        )

        # Predict questions
        questions_data = predict_interview_questions(
            body.jd_text, body.company, skills_data.get("required_skills", [])
        )

        # Store in DB
        store_result = store_jd(
            jd_id=jd_id,
            company=body.company,
            role=body.role,
            level=body.level or "unknown",
            jd_text=body.jd_text,
            extracted_data=skills_data
        )

        if not store_result.get("success"):
            raise HTTPException(500, f"Failed to store JD: {store_result.get('error')}")

        return {
            "jd_id": jd_id,
            "company": body.company,
            "role": body.role,
            "extracted_skills": skills_data.get("required_skills", []),
            "preferred_skills": skills_data.get("preferred_skills", []),
            "key_technologies": skills_data.get("key_technologies", {}),
            "estimated_difficulty": skills_data.get("estimated_difficulty", "unknown"),
            "estimated_prep_hours": skills_data.get("estimated_prep_hours", 0),
            "predicted_questions": questions_data,
        }

    except Exception as e:
        raise HTTPException(500, f"Error analyzing JD: {str(e)}")


@router.get("/jd/{jd_id}")
async def get_jd_analysis(jd_id: str):
    """Get stored JD analysis by ID."""
    from intel.jd_analyzer import get_jd

    try:
        jd = get_jd(jd_id)
        if not jd:
            raise HTTPException(404, f"JD not found: {jd_id}")
        return jd
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/jd")
async def list_jds(company: Optional[str] = None, limit: int = Query(default=20, le=100)):
    """List all analyzed JDs, optionally filtered by company."""
    from intel.jd_analyzer import list_jds

    try:
        jds = list_jds(company=company, limit=limit)
        return {"jds": jds, "count": len(jds)}
    except Exception as e:
        raise HTTPException(500, str(e))
