"""Progress data endpoints — reads/writes logs/progress.json"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

BASE       = Path(__file__).parent.parent.parent
PROG_FILE  = BASE / "logs" / "progress.json"
PORTAL_DATA = BASE / "data" / "portal_data.json"

router = APIRouter()

def _load(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default or {}

def _save(path, data):
    path.write_text(json.dumps(data, indent=2, default=str, ensure_ascii=False), encoding="utf-8")


@router.get("/progress")
async def get_progress():
    return _load(PROG_FILE, {})

@router.post("/progress")
async def save_progress(request_data: dict):
    _save(PROG_FILE, request_data)
    return {"ok": True}

@router.get("/portal-data")
async def get_portal_data():
    return _load(PORTAL_DATA, {
        "resources": [], "notes": [], "goals": [], "career": {},
        "coach_history": [], "sessions": [],
    })

@router.post("/portal-data")
async def save_portal_data(request_data: dict):
    _save(PORTAL_DATA, request_data)
    return {"ok": True}

@router.get("/gaps")
async def get_gaps(level: str = "sde2"):
    import sys
    sys.path.insert(0, str(BASE))
    try:
        from intel.analyzer import compute_gap_analysis, readiness_percentage
        progress = _load(PROG_FILE, {})
        gaps  = compute_gap_analysis(progress, level)
        score = readiness_percentage(progress, level)
        return {"gaps": gaps, "readiness": score, "level": level}
    except Exception as e:
        raise HTTPException(500, str(e))
