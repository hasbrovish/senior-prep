"""
Feedback loop routes — activity logging + LLM adaptive planning.

Endpoints:
  POST /api/log               — log an activity
  GET  /api/log/recent        — last N days of logs
  GET  /api/log/today         — today's summary
  GET  /api/plan/daily        — today's AI plan (cached)
  POST /api/plan/daily/refresh — force-regenerate daily plan
  GET  /api/plan/weekly       — this week's AI plan (cached)
  POST /api/plan/weekly/refresh — force-regenerate weekly plan
  GET  /api/plan/stats        — progress analysis for dashboard
"""

import sys
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

BASE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE))

router = APIRouter()


class LogRequest(BaseModel):
    activity_type: str      # lc, mock, curriculum, lld, jqa, drill, system_design, behavioral, notes
    title: str
    duration_mins: Optional[int] = 0
    difficulty: Optional[str] = ""
    outcome: Optional[str] = ""      # solved, struggled, failed, watched, practiced
    confidence: Optional[int] = 3    # 1-5
    notes: Optional[str] = ""
    details: Optional[dict] = None
    date: Optional[str] = None       # defaults to today


@router.post("/log")
async def log_activity(body: LogRequest):
    """Log a study activity."""
    try:
        from intel.feedback_engine import log_activity
        entry_id = log_activity(
            activity_type=body.activity_type,
            title=body.title,
            duration_mins=body.duration_mins or 0,
            difficulty=body.difficulty or "",
            outcome=body.outcome or "",
            confidence=body.confidence or 3,
            notes=body.notes or "",
            details=body.details,
            log_date=body.date,
        )
        return {"id": entry_id, "logged": True}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/log/recent")
async def get_recent_logs(days: int = 7):
    """Get activity logs from the last N days."""
    try:
        from intel.feedback_engine import get_recent_logs
        logs = get_recent_logs(days=min(days, 30))
        return {"logs": logs, "count": len(logs)}
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/log/today")
async def get_today_summary():
    """Get today's activity summary."""
    try:
        from intel.feedback_engine import get_daily_summary
        return get_daily_summary()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/plan/daily")
async def get_daily_plan(refresh: bool = False):
    """Get today's AI-generated adaptive plan. Cached — regenerates once per day."""
    try:
        from intel.feedback_engine import generate_daily_plan
        return generate_daily_plan(force=refresh)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/plan/daily/refresh")
async def refresh_daily_plan(background_tasks: BackgroundTasks):
    """Force-regenerate today's daily plan in the background."""
    def _regen():
        try:
            from intel.feedback_engine import generate_daily_plan
            generate_daily_plan(force=True)
        except Exception:
            pass
    background_tasks.add_task(_regen)
    return {"ok": True, "message": "Regenerating daily plan in background — reload in 15s"}


@router.get("/plan/weekly")
async def get_weekly_plan(refresh: bool = False):
    """Get this week's AI-generated plan. Cached — regenerates once per week."""
    try:
        from intel.feedback_engine import generate_weekly_plan
        return generate_weekly_plan(force=refresh)
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/plan/weekly/refresh")
async def refresh_weekly_plan(background_tasks: BackgroundTasks):
    """Force-regenerate this week's plan in the background."""
    def _regen():
        try:
            from intel.feedback_engine import generate_weekly_plan
            generate_weekly_plan(force=True)
        except Exception:
            pass
    background_tasks.add_task(_regen)
    return {"ok": True, "message": "Regenerating weekly plan in background — reload in 20s"}


@router.get("/plan/stats")
async def get_plan_stats():
    """Progress analysis: velocity, weak areas, confidence trend."""
    try:
        from intel.feedback_engine import get_progress_analysis
        return get_progress_analysis()
    except Exception as e:
        raise HTTPException(500, str(e))
