"""Progress data endpoints — reads/writes logs/progress.json"""
import json, time
from pathlib import Path
from datetime import date
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

def _progress():
    return _load(PROG_FILE, {})

def _save_progress(data):
    _save(PROG_FILE, data)


@router.get("/progress")
async def get_progress():
    p = _load(PROG_FILE, {})
    # Seed default username from config if not set (survives Railway deploys)
    if not p.get("lc_sync", {}).get("username"):
        try:
            from intel.config import PROFILE
            lc_user = PROFILE.get("lc_user", "")
            if lc_user:
                p.setdefault("lc_sync", {})["username"] = lc_user
                _save_progress(p)
        except Exception:
            pass
    return p

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
    try:
        from intel.analyzer import compute_gap_analysis, readiness_percentage
        progress = _load(PROG_FILE, {})
        gaps  = compute_gap_analysis(progress, level)
        score = readiness_percentage(progress, level)
        return {"gaps": gaps, "readiness": score, "level": level}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── Granular endpoints for the React UI ──────────────────────────────────────

@router.post("/progress/lc")
async def log_lc_problem(data: dict):
    """Log a single LeetCode problem without sending the entire progress blob."""
    p = _progress()
    lc_done = p.get("lc_done", [])
    entry = {"name": data.get("name", ""), "date": data.get("date", str(date.today()))}
    if data.get("pattern"): entry["pattern"] = data["pattern"]
    if data.get("time_mins"): entry["time_mins"] = data["time_mins"]
    if data.get("hard"): entry["hard"] = True
    lc_done.append(entry)
    p["lc_done"] = lc_done
    _save_progress(p)
    return {"ok": True, "total": len(lc_done)}


@router.post("/progress/lc/sync")
async def sync_leetcode():
    """Fetch latest LeetCode stats from the public GraphQL API."""
    import urllib.request
    p = _progress()
    username = p.get("lc_sync", {}).get("username", "")
    if not username:
        raise HTTPException(400, "Set lc_sync.username first via POST /api/progress/lc/username")

    payload = json.dumps({
        "query": """
        query getUserProfile($username: String!) {
          matchedUser(username: $username) {
            submitStatsGlobal {
              acSubmissionNum { difficulty count }
            }
            languageProblemCount { languageName problemsSolved }
            userCalendar { streak totalActiveDays }
          }
        }""",
        "variables": {"username": username},
    }).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode()
            if raw.strip().startswith("<"):
                raise HTTPException(502, "LeetCode returned HTML (possible rate-limit/block)")
            data = json.loads(raw)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(502, f"LeetCode API error: {e}")

    user = data.get("data", {}).get("matchedUser")
    if not user:
        raise HTTPException(404, f"LeetCode user '{username}' not found")

    stats = (user.get("submitStatsGlobal") or {}).get("acSubmissionNum") or []
    lang_stats = user.get("languageProblemCount") or []
    cal = user.get("userCalendar") or {}

    counts = {s["difficulty"]: s["count"] for s in stats if "difficulty" in s and "count" in s}
    lang_map = {l["languageName"]: l["problemsSolved"] for l in lang_stats if "languageName" in l}
    total = counts.get("All", 0)

    prev_total = p.get("lc_sync", {}).get("total", 0)
    p.setdefault("lc_sync", {}).update({
        "username": username,
        "total": total,
        "easy": counts.get("Easy", 0),
        "medium": counts.get("Medium", 0),
        "hard": counts.get("Hard", 0),
        "streak": cal.get("streak", 0),
        "total_active_days": cal.get("totalActiveDays", 0),
        "java_problems": lang_map.get("Java", 0),
        "cpp_problems": lang_map.get("C++", 0),
        "languages": lang_map,
        "last_sync": str(date.today()),
    })

    if total > prev_total:
        today = str(date.today())
        p.setdefault("daily_logs", {}).setdefault(today, []).append(
            f"[Sync] {total - prev_total} new LC problem(s) (total: {total})"
        )

    _save_progress(p)
    return {"ok": True, "lc_sync": p["lc_sync"]}


@router.post("/progress/lc/username")
async def set_lc_username(data: dict):
    """Set/update LeetCode username for sync."""
    username = data.get("username", "").strip()
    if not username:
        raise HTTPException(400, "username is required")
    p = _progress()
    p.setdefault("lc_sync", {})["username"] = username
    _save_progress(p)
    return {"ok": True, "username": username}

@router.post("/progress/apply")
async def log_application(data: dict):
    p = _progress()
    apps = p.get("applications", [])
    entry = {
        "id": int(time.time() * 1000), "company": data.get("company", ""),
        "role": data.get("role", ""), "link": data.get("link", ""),
        "stage": data.get("stage", "Applied"), "date": str(date.today()),
    }
    apps.append(entry)
    p["applications"] = apps
    _save_progress(p)
    return {"ok": True, "id": entry["id"]}

@router.patch("/progress/applications/{app_id}")
async def update_application(app_id: int, data: dict):
    p = _progress()
    apps = p.get("applications", [])
    for app in apps:
        if app.get("id") == app_id:
            app.update(data)
            break
    p["applications"] = apps
    _save_progress(p)
    return {"ok": True}

@router.post("/progress/bug")
async def log_bug(data: dict):
    p = _progress()
    bugs = p.get("bug_journal", [])
    entry = {
        "id": int(time.time() * 1000), "date": str(date.today()),
        "description": data.get("description", ""),
        "category": data.get("category", "other"),
        "context": data.get("context", ""),
    }
    bugs.append(entry)
    p["bug_journal"] = bugs
    _save_progress(p)
    return {"ok": True, "id": entry["id"]}

@router.post("/progress/retro")
async def log_retro(data: dict):
    p = _progress()
    retros = p.get("retros", [])
    entry = {"id": int(time.time() * 1000), "date": str(date.today()), **data}
    retros.append(entry)
    p["retros"] = retros
    _save_progress(p)
    return {"ok": True, "id": entry["id"]}

@router.post("/progress/failure")
async def log_failure(data: dict):
    p = _progress()
    failures = p.get("failures", [])
    entry = {"id": int(time.time() * 1000), "date": str(date.today()), **data}
    failures.append(entry)
    p["failures"] = failures
    _save_progress(p)
    return {"ok": True, "id": entry["id"]}

@router.post("/progress/sr/review")
async def sr_review(data: dict):
    """Record a spaced repetition review."""
    p = _progress()
    sr = p.get("spaced_repetition", [])
    item_id = data.get("id")
    confidence = data.get("confidence", 3)
    intervals = [0, 1, 3, 7, 14, 30]
    next_days = intervals[min(confidence, len(intervals) - 1)]
    from datetime import timedelta
    next_date = str(date.today() + timedelta(days=next_days))
    for item in sr:
        if item.get("id") == item_id:
            item["confidence"] = confidence
            item["reviews"] = item.get("reviews", 0) + 1
            item["next_review"] = next_date
            item["last_reviewed"] = str(date.today())
            break
    p["spaced_repetition"] = sr
    _save_progress(p)
    return {"ok": True, "next_review": next_date}

@router.post("/progress/sr/add")
async def sr_add(data: dict):
    """Add a new topic to spaced repetition."""
    p = _progress()
    sr = p.get("spaced_repetition", [])
    entry = {
        "id": int(time.time() * 1000), "topic": data.get("topic", ""),
        "category": data.get("category", "other"), "confidence": 0,
        "reviews": 0, "next_review": str(date.today()), "added": str(date.today()),
    }
    sr.append(entry)
    p["spaced_repetition"] = sr
    _save_progress(p)
    return {"ok": True, "id": entry["id"]}
