"""Career ladder, job trends, skill gap tracking endpoints."""
import sys, json
from pathlib import Path
from fastapi import APIRouter
from typing import Optional

BASE = Path(__file__).parent.parent.parent
sys.path.insert(0, str(BASE))

router = APIRouter()


@router.get("/career/ladder")
async def career_ladder():
    """SDE-2 → SDE-3 progression map based on industry data."""
    return {
        "transitions": [
            {
                "from": "SDE-2", "to": "SDE-3",
                "avg_months": 18, "key_signals": [
                    "Leads design of a component independently",
                    "Mentors 1-2 junior engineers",
                    "Drives cross-team technical decisions",
                    "Owns a service end-to-end in production",
                    "Designs for scale (10x growth)",
                ],
                "technical_bar": {
                    "dsa": "Hard LeetCode patterns, DP + Graphs fluently",
                    "system_design": "Deep dive 3 components, metrics-driven",
                    "lld": "Production-grade, testability, SOLID",
                    "behavioral": "Leadership stories, cross-team impact",
                },
            }
        ],
        "your_progress": {
            "current_level": "SDE-2",
            "target_level": "SDE-3",
            "phase": "Phase 1 — Foundation (Mar–Jun 2026)",
        }
    }


@router.get("/career/skill-map")
async def skill_map():
    """Skills Jayanti has vs what top companies want."""
    return {
        "strong": [
            {"skill": "Kafka + DLQ + exactly-once", "companies": ["Flipkart", "PhonePe", "Swiggy", "Amazon"]},
            {"skill": "Distributed caching (Redis, JBoss DataGrid)", "companies": ["All Tier-1"]},
            {"skill": "XA Transactions + Atomikos", "companies": ["Goldman Sachs", "Razorpay", "Juspay"]},
            {"skill": "Microservices at scale (14M users)", "companies": ["All Tier-1"]},
            {"skill": "Spring Boot + Hibernate", "companies": ["Adobe", "Infosys", "Oracle"]},
        ],
        "gaps": [
            {"skill": "Java DSA (Hard problems)", "urgency": "CRITICAL", "action": "150 Java LC problems — start today"},
            {"skill": "LLD (Parking Lot, Chess, etc.)", "urgency": "HIGH", "action": "5 LLD problems using Hello Interview"},
            {"skill": "Golang goroutines + channels", "urgency": "MEDIUM", "action": "2 hours/week brushup"},
            {"skill": "FAANG System Design framing", "urgency": "HIGH", "action": "Hello Interview Premium + Alex Xu Vol 2"},
        ],
    }


@router.get("/career/weekly-plan")
async def weekly_plan():
    """Current week's study plan based on 26-week programme."""
    from datetime import date
    prog_file = BASE / "logs" / "progress.json"
    try:
        progress = json.loads(prog_file.read_text())
    except Exception:
        progress = {}

    start = date(2026, 3, 19)
    today = date.today()
    week_num = min(26, max(1, ((today - start).days // 7) + 1))

    # Import week plan from prep.py WEEKS dict
    try:
        import importlib.util, sys as _sys
        spec = importlib.util.spec_from_file_location("prep", BASE / "prep.py")
        prep = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prep)
        week = prep.WEEKS.get(week_num, {})
        return {
            "week": week_num,
            "theme": week.get("theme", ""),
            "dsa_topic": week.get("dsa", ""),
            "difficulty": week.get("diff", ""),
            "lc_target": week.get("lc_target", 0),
            "lc_problems": week.get("lc_problems", []),
            "tasks": week.get("tasks", []),
            "questions": week.get("questions", []),
            "lc_done_this_week": len([
                x for x in progress.get("lc_done", [])
                if x.get("week") == week_num
            ]),
        }
    except Exception as e:
        return {"week": week_num, "error": str(e)}
