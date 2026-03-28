"""Intel endpoints — trending, experiences, company profiles, scraping, manual import."""
import re
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


@router.get("/experiences/{exp_id}/rounds")
async def get_experience_rounds(exp_id: int):
    try:
        from intel.db import get_rounds_for_experience
        rounds = get_rounds_for_experience(exp_id)
        return {"rounds": rounds, "count": len(rounds)}
    except Exception as e:
        return {"rounds": [], "error": str(e)}


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


_scrape_status = {"running": False, "last_run": None, "last_result": None}


def _run_scrape(source: Optional[str]):
    """Background job: run scraper, then auto-extract questions from new posts."""
    global _scrape_status
    _scrape_status["running"] = True
    try:
        from intel.scraper import run_scraper
        stats = run_scraper(source_name=source, verbose=False)
    except Exception as e:
        _scrape_status["running"] = False
        _scrape_status["last_result"] = {"error": str(e)}
        return

    try:
        from intel.question_extractor import bulk_extract_from_db
        extract_stats = bulk_extract_from_db(limit=500)
        if isinstance(stats, dict):
            stats["question_extraction"] = extract_stats
    except Exception as e:
        if isinstance(stats, dict):
            stats["question_extraction_error"] = str(e)

    from datetime import datetime
    _scrape_status["running"] = False
    _scrape_status["last_run"] = datetime.now().isoformat()
    _scrape_status["last_result"] = stats


@router.post("/scrape")
async def trigger_scrape(background_tasks: BackgroundTasks, source: Optional[str] = None):
    """Trigger scraping in background — returns immediately."""
    background_tasks.add_task(_run_scrape, source)
    return {"ok": True, "message": f"Scraping {'all sources' if not source else source} in background"}


@router.get("/scrape/status")
async def scrape_status():
    """Check if scraping is running and when it last completed."""
    try:
        from intel.db import get_overall_stats
        db_stats = get_overall_stats()
        return {
            **_scrape_status,
            "total_experiences": db_stats.get("total_experiences", 0),
            "total_companies": db_stats.get("companies", 0),
        }
    except Exception as e:
        return {**_scrape_status, "error": str(e)}


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
            extracted_data=skills_data,
            predicted_questions=questions_data,
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


# ─── Phase 2: Skill Gap Analysis ──────────────────────────────────────────────


class GapAnalysisRequest(BaseModel):
    """User's self-assessed skill levels (1-10 scale)."""
    user_skills: dict  # {"Kafka": 7, "Java": 8, "System Design": 5}


@router.post("/jd/{jd_id}/gap-analysis")
async def gap_analysis(jd_id: str, body: GapAnalysisRequest):
    """
    Compare user skill levels vs JD requirements.

    Input: {"user_skills": {"Kafka": 7, "Java": 8, "System Design": 5}}

    Returns:
    - overall_readiness (0-100%)
    - per-skill gap breakdown
    - priority skills to focus on
    - estimated total prep hours
    - company-specific behavioral guide
    """
    from intel.jd_analyzer import analyze_skill_gap

    try:
        result = analyze_skill_gap(jd_id, body.user_skills)
        if "error" in result:
            raise HTTPException(404, result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Phase 3: Roadmap Generation ──────────────────────────────────────────────


class RoadmapRequest(BaseModel):
    """Request for a personalized prep roadmap."""
    user_skills: dict  # {"Kafka": 7, "Java": 8}
    weeks: int = 4     # weeks available (2-8)


@router.post("/jd/{jd_id}/roadmap")
async def generate_roadmap(jd_id: str, body: RoadmapRequest):
    """
    Generate a week-by-week personalized prep roadmap.

    Input: {"user_skills": {"Kafka": 7, "Java": 8}, "weeks": 4}

    Returns weekly plans with:
    - Theme and focus skill
    - Daily targets and resources
    - LeetCode problem targets
    - Behavioral prep schedule
    """
    from intel.jd_analyzer import generate_prep_roadmap

    weeks = max(2, min(8, body.weeks))
    try:
        result = generate_prep_roadmap(jd_id, body.user_skills, weeks)
        if "error" in result:
            raise HTTPException(404, result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Behavioral Guide ─────────────────────────────────────────────────────────


@router.get("/jd/behavioral/{company}")
async def behavioral_guide(company: str):
    """
    Get company-specific behavioral interview framework.

    Returns: framework name, key principles, top questions, tips, TC range.

    Supports: Amazon, Google, Stripe, Flipkart, Razorpay, PhonePe, Swiggy,
              CRED, DoorDash, Microsoft, Bloomberg
    """
    from intel.jd_analyzer import get_behavioral_guide

    try:
        return get_behavioral_guide(company)
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Extracted Questions Endpoint ─────────────────────────────────────────────

QUESTION_WORDS = re.compile(
    r'\b(design|implement|find|solve|what|how|why|when|describe|explain|'
    r'tell|given|write|build|create|calculate|determine|check|validate|'
    r'optimis|optimize|debug|fix|improve|compare|difference|approach)\b',
    re.IGNORECASE,
)


# ─── Experiences Portal Endpoints ────────────────────────────────────────────

class TipRequest(BaseModel):
    company: str = ""
    round_type: str = ""
    tip: str
    author: str = "me"


@router.get("/portal/stats")
async def portal_stats():
    """Master stats for the Experiences Portal dashboard."""
    try:
        from intel.db import get_portal_stats
        return get_portal_stats()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/portal/questions")
async def portal_questions(
    round_type: Optional[str] = None,
    company: Optional[str] = None,
    limit: int = Query(default=100, le=200),
):
    """Aggregated questions bank from all experience_rounds, with frequency."""
    try:
        from intel.db import get_questions_bank
        questions = get_questions_bank(
            round_type=round_type, company=company, limit=limit
        )
        return {"questions": questions, "count": len(questions)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/portal/company/{name}")
async def portal_company_profile(name: str):
    """Full company profile: experiences, round breakdown, top questions, tips."""
    try:
        from intel.db import get_company_profile
        return get_company_profile(name)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/portal/tips")
async def portal_save_tip(body: TipRequest):
    """Save a user-submitted tip."""
    if not body.tip.strip():
        raise HTTPException(400, "tip text is required")
    try:
        from intel.db import save_user_tip
        tip_id = save_user_tip(
            company=body.company or None,
            round_type=body.round_type or None,
            tip_text=body.tip.strip(),
            author=body.author or "me",
        )
        return {"saved": True, "id": tip_id}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/portal/tips")
async def portal_get_tips(
    company: Optional[str] = None,
    round_type: Optional[str] = None,
):
    """Get user tips, optionally filtered by company / round_type."""
    try:
        from intel.db import get_user_tips
        tips = get_user_tips(company=company, round_type=round_type)
        return {"tips": tips, "count": len(tips)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.delete("/portal/tips/{tip_id}")
async def portal_delete_tip(tip_id: int):
    """Delete a user tip by ID."""
    try:
        from intel.db import delete_user_tip
        delete_user_tip(tip_id)
        return {"deleted": True, "id": tip_id}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/portal/questions/{round_id}/practice")
async def portal_add_to_practice(round_id: int):
    """Queue a round question into the appropriate practice session table."""
    try:
        import sqlite3 as _sqlite3
        from intel.config import DB_PATH
        from datetime import date as _date

        conn = _sqlite3.connect(str(DB_PATH))
        conn.row_factory = _sqlite3.Row
        row = conn.execute(
            "SELECT er.*, e.company FROM experience_rounds er JOIN experiences e ON er.experience_id = e.id WHERE er.id = ?",
            (round_id,)
        ).fetchone()
        if not row:
            conn.close()
            raise HTTPException(404, f"Round {round_id} not found")

        rt = row["round_type"] or "dsa"
        question = row["question"] or f"Round {round_id} question"
        company = row["company"] or "Unknown"
        today = str(_date.today())

        if rt == "dsa":
            conn.execute(
                "INSERT INTO drill_sessions (date_done, problem_name, time_mins, struggled, language) VALUES (?,?,0,0,'java')",
                (today, question[:200])
            )
        elif rt == "lld":
            conn.execute(
                "INSERT INTO lld_sessions (date_done, problem_key, score, time_mins, notes) VALUES (?,?,0,0,?)",
                (today, f"portal_{round_id}", f"queued: {question[:200]}")
            )
        else:
            # system_design, behavioral, hr, machine_coding → mock_sessions
            conn.execute(
                "INSERT INTO mock_sessions (date_done, company, round_type, score, questions_json, time_mins, notes, hire_verdict) VALUES (?,?,?,0,?,0,'queued','pending')",
                (today, company, rt, json.dumps([question[:200]]))
            )
        conn.commit()
        conn.close()
        return {"queued": True, "round_id": round_id, "round_type": rt}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/questions")
async def get_extracted_questions(
    company: Optional[str] = None,
    round_type: Optional[str] = None,
    limit: int = Query(default=20, le=100),
):
    """
    GET /api/intel/questions?company=amazon&round_type=system_design&limit=20

    Returns extracted interview questions from experience_rounds, joined with
    experiences for company/role/url/date context.

    Filters:
    - company:    partial match on company name (case-insensitive)
    - round_type: dsa | system_design | lld | behavioral | hr | machine_coding
    - limit:      max rows (default 20, max 100)

    Only returns rows where the question field looks like a real question
    (length > 30 and contains at least one recognised question-type word).
    """
    try:
        import sqlite3 as _sqlite3
        from intel.config import DB_PATH
        from pathlib import Path as _Path

        if not _Path(str(DB_PATH)).exists():
            return {"questions": [], "count": 0, "error": "database not initialised yet"}

        conn = _sqlite3.connect(str(DB_PATH))
        conn.row_factory = _sqlite3.Row

        sql = """
            SELECT
                e.company,
                e.role,
                er.round_type,
                er.question,
                er.difficulty,
                e.url,
                e.date_posted   AS date,
                e.overall_result
            FROM experience_rounds er
            JOIN experiences e ON er.experience_id = e.id
            WHERE
                LENGTH(er.question) > 30
        """
        params: list = []

        if company:
            sql += " AND LOWER(e.company) LIKE ?"
            params.append(f"%{company.lower()}%")

        if round_type:
            sql += " AND er.round_type = ?"
            params.append(round_type)

        sql += " ORDER BY e.date_scraped DESC LIMIT ?"
        params.append(limit * 5)   # over-fetch to allow post-filter

        rows = conn.execute(sql, params).fetchall()
        conn.close()

        # Post-filter: question must contain at least one question-type word
        results = []
        for row in rows:
            q = row["question"] or ""
            if QUESTION_WORDS.search(q):
                results.append({
                    "company":    row["company"],
                    "role":       row["role"],
                    "round_type": row["round_type"],
                    "question":   q,
                    "difficulty": row["difficulty"],
                    "url":        row["url"],
                    "date":       row["date"],
                    "result":     row["overall_result"],
                })
            if len(results) >= limit:
                break

        return {"questions": results, "count": len(results)}

    except Exception as e:
        raise HTTPException(500, str(e))


