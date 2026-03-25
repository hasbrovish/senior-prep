"""
Practice routes — Drill, Mock Tracker, LLD, Behavioral, TC Intelligence.

Endpoints:
  GET  /api/drill/today         — today's Java DSA drill problems
  POST /api/drill/done          — mark drill problem done
  GET  /api/drill/stats         — drill streak and history

  GET  /api/mock/trend          — score trend over time
  POST /api/mock/score          — save a mock session score
  GET  /api/mock/readiness/{company} — readiness % per round type

  GET  /api/lld/problems        — list LLD problems
  GET  /api/lld/problem/{key}   — get problem details
  POST /api/lld/score           — save an LLD session score
  GET  /api/lld/scores          — recent LLD history

  GET  /api/behavioral/check    — LP gap analysis
  GET  /api/behavioral/probes/{lp}  — probing questions for an LP

  GET  /api/tc/{company}        — TC intelligence
  GET  /api/brief               — generate morning brief
"""

import os, sys, json
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

BASE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE))

router = APIRouter()


# ─── Drill ────────────────────────────────────────────────────────────────────

@router.get("/drill/today")
async def get_drill_today(company: Optional[str] = None, week: Optional[int] = None):
    try:
        from intel.drill import get_drill
        prog_path = BASE / "logs" / "progress.json"
        java_count = 0
        try:
            p = json.loads(prog_path.read_text())
            java_count = p.get("lc_sync", {}).get("java_problems", 0)
        except Exception:
            pass
        problems = get_drill(week_num=week, company=company, java_count=java_count)
        return {"problems": problems, "java_count": java_count}
    except Exception as e:
        raise HTTPException(500, str(e))


class DrillDoneRequest(BaseModel):
    problem_name: str
    time_mins: Optional[int] = 0
    struggled: Optional[bool] = False
    language: Optional[str] = "java"


@router.post("/drill/done")
async def mark_drill_done(body: DrillDoneRequest):
    try:
        from intel.drill import mark_drill_done
        success = mark_drill_done(
            body.problem_name, body.time_mins, body.struggled, body.language
        )
        return {"success": success}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/drill/stats")
async def get_drill_stats():
    try:
        from intel.drill import get_drill_stats, get_drill_history
        return {
            "stats": get_drill_stats(),
            "history": get_drill_history(limit=7),
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Mock Score Tracker ───────────────────────────────────────────────────────

@router.get("/mock/trend")
async def get_mock_trend(company: Optional[str] = None, round_type: Optional[str] = None,
                          weeks: Optional[int] = 8):
    try:
        from intel.mock_engine import get_score_trend
        return get_score_trend(company=company, round_type=round_type, weeks=weeks)
    except Exception as e:
        raise HTTPException(500, str(e))


class MockScoreRequest(BaseModel):
    company: str
    round_type: str
    score: float
    questions: Optional[list] = None
    time_mins: Optional[int] = 0
    notes: Optional[str] = ""


@router.post("/mock/score")
async def save_mock_score(body: MockScoreRequest):
    try:
        from intel.mock_engine import save_mock_score
        session_id = save_mock_score(
            body.company, body.round_type, body.score,
            body.questions, body.time_mins, body.notes
        )
        return {"session_id": session_id, "saved": session_id > 0}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/mock/readiness/{company}")
async def get_mock_readiness(company: str):
    try:
        from intel.mock_engine import get_readiness_by_company, COMPANY_ROUND_MAP
        readiness = get_readiness_by_company(company)
        rounds = COMPANY_ROUND_MAP.get(company.lower(), [])
        return {"company": company, "rounds": rounds, "readiness": readiness}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── LLD Practice ─────────────────────────────────────────────────────────────

@router.get("/lld/problems")
async def list_lld_problems(company: Optional[str] = None, difficulty: Optional[str] = None):
    try:
        from intel.lld_engine import list_lld_problems
        problems = list_lld_problems(company=company, difficulty=difficulty)
        return {"problems": problems, "count": len(problems)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/lld/problem/{key}")
async def get_lld_problem(key: str):
    try:
        from intel.lld_engine import get_lld_problem
        problem = get_lld_problem(key)
        if not problem:
            raise HTTPException(404, f"LLD problem '{key}' not found")
        return problem
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


class LLDScoreRequest(BaseModel):
    problem_key: str
    score: int
    time_mins: Optional[int] = 0
    notes: Optional[str] = ""


@router.post("/lld/score")
async def save_lld_score(body: LLDScoreRequest):
    try:
        from intel.lld_engine import save_lld_score
        save_lld_score(body.problem_key, body.score, body.time_mins, body.notes)
        return {"saved": True}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/lld/scores")
async def get_lld_scores(limit: int = 20):
    try:
        from intel.lld_engine import get_lld_scores
        return {"scores": get_lld_scores(limit=limit)}
    except Exception as e:
        raise HTTPException(500, str(e))


class LLDEvalRequest(BaseModel):
    problem_key: str
    design_description: str


@router.post("/lld/evaluate")
async def evaluate_lld(body: LLDEvalRequest):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(400, "ANTHROPIC_API_KEY not set")
    try:
        from intel.lld_engine import evaluate_lld_with_ai
        result = evaluate_lld_with_ai(body.problem_key, body.design_description)
        return {"evaluation": result}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Behavioral ───────────────────────────────────────────────────────────────

@router.get("/behavioral/check")
async def behavioral_check():
    try:
        from intel.behavioral import run_lp_check
        return run_lp_check()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/behavioral/probes/{lp_key}")
async def get_probes(lp_key: str):
    try:
        from intel.behavioral import get_probing_questions
        questions = get_probing_questions(lp_key, count=5)
        return {"lp_key": lp_key, "questions": questions}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── TC Intelligence ──────────────────────────────────────────────────────────

@router.get("/tc/{company}")
async def get_tc(company: str):
    try:
        from intel.sources.levelsfyi import get_tc_data
        return get_tc_data(company)
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Morning Brief ────────────────────────────────────────────────────────────

@router.get("/brief")
async def get_brief(send: bool = False):
    try:
        from intel.brief import generate_brief_text, send_morning_brief
        brief = generate_brief_text()
        sent = False
        if send:
            sent = send_morning_brief()
        return {"brief": brief, "sent": sent}
    except Exception as e:
        raise HTTPException(500, str(e))
