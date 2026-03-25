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


# ─── Drill Company Bank ──────────────────────────────────────────────────────

@router.get("/drill/companies")
async def list_drill_companies():
    try:
        from intel.drill import get_all_companies
        return {"companies": get_all_companies()}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/drill/company/{company}")
async def get_drill_by_company(company: str):
    try:
        from intel.drill import get_company_problems
        problems = get_company_problems(company)
        return {"company": company, "problems": problems, "count": len(problems)}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Java QA (Theory) ────────────────────────────────────────────────────────

@router.get("/jqa")
async def get_jqa_today(week: Optional[int] = None):
    """Get today's Java theory topic based on current week."""
    try:
        from intel.java_qa import get_today_topic, get_progress, JAVA_QA
        prog_path = BASE / "logs" / "progress.json"
        current_week = week or 1
        try:
            p = json.loads(prog_path.read_text())
            current_week = week or p.get("current_week", 1)
        except Exception:
            pass
        today = get_today_topic(current_week)
        progress = get_progress()
        return {
            "today": today,
            "progress": progress,
            "total_topics": len(JAVA_QA),
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/jqa/topic/{topic_id}")
async def get_jqa_topic(topic_id: str, hints: bool = False):
    """Get questions for a specific Java theory topic."""
    try:
        from intel.java_qa import JAVA_QA, get_questions
        if topic_id not in JAVA_QA:
            raise HTTPException(404, f"Topic '{topic_id}' not found. Available: {list(JAVA_QA.keys())}")
        topic = JAVA_QA[topic_id]
        # get_questions returns list of dicts with id, q, priority, company, hint, studied
        questions = get_questions(topic_id, priority=None)  # all priorities
        return {
            "topic_id": topic_id,
            "label": topic["label"],
            "questions": questions,
            "count": len(questions),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/jqa/list")
async def list_jqa_topics():
    """List all Java theory topics with study status."""
    try:
        from intel.java_qa import JAVA_QA, get_topics
        topics_data = get_topics()  # returns list of dicts with id, label, p0_total, p0_done, pct, week
        topics = []
        for t in topics_data:
            topics.append({
                "id": t["id"],
                "label": t["label"],
                "total_questions": len(JAVA_QA.get(t["id"], {}).get("questions", [])),
                "p0_count": t["p0_total"],
                "p0_done": t["p0_done"],
                "pct": t["pct"],
                "studied": t["pct"] > 0,
            })
        studied_count = sum(1 for t in topics if t["studied"])
        return {"topics": topics, "studied_count": studied_count, "total": len(topics)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/jqa/done/{topic_id}")
async def mark_jqa_done(topic_id: str):
    """Mark a Java theory topic as studied."""
    try:
        from intel.java_qa import mark_topic_studied
        count = mark_topic_studied(topic_id)
        return {"topic_id": topic_id, "questions_logged": count, "success": True}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── War Plan ────────────────────────────────────────────────────────────────

@router.get("/warplan")
async def get_warplan(week: Optional[int] = None):
    """Get the war plan content, optionally filtered to a specific week."""
    plan_candidates = [
        BASE / "ULTIMATE_INTERVIEW_ASSAULT.md",
        BASE / "MASTER_16H_WARPLAN.md",
    ]
    plan_file = None
    for pf in plan_candidates:
        if pf.exists():
            plan_file = pf
            break
    if not plan_file:
        raise HTTPException(404, "No war plan file found")

    content = plan_file.read_text(encoding="utf-8")
    if week:
        lines = content.split("\n")
        block = []
        in_block = False
        for line in lines:
            if f"WEEK {week}" in line and (line.startswith("##") or line.startswith("###")):
                in_block = True
            if in_block:
                block.append(line)
                if len(block) > 1 and (line.startswith("## WEEK") or line.startswith("### WEEK")) and f"WEEK {week}" not in line:
                    break
        return {"week": week, "content": "\n".join(block), "source": plan_file.name}

    return {"content": content, "source": plan_file.name}


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
