"""
PrepForge FastAPI Server
Replaces portal/server.py with production-grade API.

Run locally:    uvicorn app.main:app --reload --port 5555
Run production: uvicorn app.main:app --host 0.0.0.0 --port $PORT
"""

import os, json, sys, time
from pathlib import Path
from datetime import date, datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE        = Path(__file__).parent.parent
PORTAL_DIR  = BASE / "portal"
PROG_FILE   = BASE / "logs" / "progress.json"
PORTAL_DATA = BASE / "data" / "portal_data.json"

# Ensure directories
(BASE / "logs").mkdir(exist_ok=True)
(BASE / "data").mkdir(exist_ok=True)

sys.path.insert(0, str(BASE))

# ─── Config ───────────────────────────────────────────────────────────────────
ANTHROPIC_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
PORTAL_SECRET   = os.environ.get("PORTAL_SECRET", "")   # Optional: lock portal with a key
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5555,http://localhost:3000").split(",")
ENV             = os.environ.get("ENV", "development")


# ─── Rate Limiting (simple in-memory) ─────────────────────────────────────────
_rate_store: dict = {}

def check_rate_limit(ip: str, limit: int = 20, window: int = 60) -> bool:
    now = time.time()
    key = f"{ip}"
    hits = _rate_store.get(key, [])
    hits = [h for h in hits if now - h < window]
    if len(hits) >= limit:
        return False
    hits.append(now)
    _rate_store[key] = hits
    return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        # Stricter limits on AI endpoints (personal use — 30/min for coach, 120/min for others)
        limit = 30 if "/api/coach" in path else 120
        if not check_rate_limit(ip, limit=limit, window=60):
            return JSONResponse({"error": "Rate limit exceeded. Please wait."}, status_code=429)
        return await call_next(request)


# ─── Startup/Shutdown ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init intel DB
    try:
        from intel.db import init_db
        init_db()
        print("  ✅ Intel DB initialized")
    except Exception as e:
        print(f"  ⚠️  Intel DB: {e}")

    # Start background scheduler
    try:
        from app.scheduler import start_scheduler
        start_scheduler()
        print("  ✅ Background scheduler started")
    except Exception as e:
        print(f"  ⚠️  Scheduler: {e}")

    yield

    # Shutdown
    try:
        from app.scheduler import stop_scheduler
        stop_scheduler()
    except Exception:
        pass


# ─── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="PrepForge Intelligence Engine",
    description="Personal interview prep + career intelligence platform",
    version="2.0.0",
    docs_url="/docs" if ENV == "development" else None,  # Hide docs in prod
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.add_middleware(RateLimitMiddleware)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, default=str, ensure_ascii=False), encoding="utf-8")

def scrub_pii(data: dict) -> dict:
    """Remove fields that could leak PII before sending to AI."""
    scrubbed = dict(data)
    for key in ["email", "phone", "address", "linkedin", "github_token"]:
        scrubbed.pop(key, None)
    return scrubbed


# ─── Include Routers ──────────────────────────────────────────────────────────
from app.routers import progress, intel_routes, coach, career, practice

app.include_router(progress.router, prefix="/api")
app.include_router(intel_routes.router, prefix="/api/intel")
app.include_router(coach.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(practice.router, prefix="/api")


# ─── Portal Static Files ──────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_portal():
    index = PORTAL_DIR / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>PrepForge Portal — index.html not found in portal/</h1>", status_code=404)

@app.get("/health")
async def health():
    return {"status": "ok", "time": str(datetime.now()), "env": ENV}


@app.get("/api/hi-curriculum")
async def hi_curriculum():
    """Legacy endpoint — kept for backwards compat. Use /api/curriculum instead."""
    for candidate in [
        BASE / "data" / "hellointerviewcourse.json",
        BASE / "data" / "programming_pathshala_courses.json",
    ]:
        if candidate.exists():
            return load_json(candidate, {})
    return {"error": "No course JSON found."}


@app.get("/api/curriculum")
async def master_curriculum():
    """Merged master curriculum: Hello Interview + Programming Pathshala.

    Returns a normalized list of items:
      {id, category, source, week_start, week_end, module, section, title, url, item_type, duration}
    """
    items = []

    # ── Hello Interview ───────────────────────────────────────────────────────
    HI_BASE_URL = "https://www.hellointerview.com"
    HI_WEEK_MAP = {
        "system-design|In a Hurry":                    (1,  2),
        "system-design|Core Concepts":                 (9,  12),
        "system-design|Patterns":                      (12, 14),
        "system-design|Key Technologies (Deep Dives)": (13, 16),
        "system-design|Advanced Topics":               (16, 17),
        "system-design|Question Breakdowns":           (14, 26),
        "ml-system-design|In a Hurry":                 (16, 17),
        "ml-system-design|Core Concepts":              (17, 18),
        "ml-system-design|Question Breakdowns":        (18, 20),
        "low-level-design|In a Hurry":                 (4,  5),
        "low-level-design|Concurrency":                (5,  6),
        "low-level-design|Problem Breakdowns":         (10, 13),
        "dsa|Two Pointers":                            (1,  1),
        "dsa|Sliding Window":                          (1,  2),
        "dsa|Intervals":                               (2,  2),
        "dsa|Stack":                                   (2,  3),
        "dsa|Linked List":                             (3,  3),
        "dsa|Binary Search":                           (3,  4),
        "dsa|Heap":                                    (4,  5),
        "dsa|Depth-First Search (DFS)":                (5,  6),
        "dsa|Breadth-First Search (BFS)":              (6,  7),
        "dsa|Backtracking":                            (7,  8),
        "dsa|Graphs":                                  (8,  9),
        "dsa|Dynamic Programming":                     (9,  11),
        "dsa|Greedy Algorithms":                       (11, 11),
        "dsa|Trie":                                    (11, 12),
        "dsa|Prefix Sum":                              (12, 12),
        "dsa|Matrices":                                (12, 12),
        "behavioral|Course":                           (1,  5),
        "behavioral|Story Builder":                    (4,  26),
    }
    HI_CAT_MAP = {
        "system-design": "system-design",
        "ml-system-design": "ml-system-design",
        "low-level-design": "lld",
        "dsa": "dsa",
        "behavioral": "behavioral",
    }
    hi_file = BASE / "data" / "hellointerviewcourse.json"
    if hi_file.exists():
        hi_data = load_json(hi_file, {})
        for course in hi_data.get("courses", []):
            cid = course["id"]
            category = HI_CAT_MAP.get(cid, cid)
            for section in course.get("sections", []):
                sec_name = section["section"]
                key = f"{cid}|{sec_name}"
                ws, we = HI_WEEK_MAP.get(key, (13, 20))
                lessons = section.get("lessons", [])
                n = len(lessons)
                for i, lesson in enumerate(lessons):
                    week = ws + round(i * (we - ws) / max(n - 1, 1)) if n > 1 else ws
                    url = lesson.get("url", "")
                    items.append({
                        "id":        f"hi_{cid}_{lesson.get('url','').replace('/','_')}",
                        "category":  category,
                        "source":    "hi",
                        "source_label": "Hello Interview",
                        "week_start": week,
                        "week_end":  week,
                        "module":    course["title"],
                        "section":   sec_name,
                        "title":     lesson["title"],
                        "url":       HI_BASE_URL + url if url else HI_BASE_URL,
                        "item_type": lesson.get("type", "problem" if section.get("type") == "problem_breakdowns" else "lesson"),
                        "difficulty": lesson.get("difficulty", ""),
                        "duration":  "",
                    })

    # ── Programming Pathshala ─────────────────────────────────────────────────
    PP_BASE_URL = "https://app.programmingpathshala.com"
    PP_WEEK_MAP = {
        # (course_name, module_number): (week_start, week_end, category)
        ("DSA", 3):  (1,  3,  "dsa"),
        ("DSA", 4):  (3,  5,  "dsa"),
        ("DSA", 5):  (5,  7,  "dsa"),
        ("DSA", 6):  (8,  11, "dsa"),
        ("LLD & Concurrency", 7):  (4,  5,  "lld"),
        ("LLD & Concurrency", 8):  (14, 16, "lld"),
        ("System Design", 9):      (9,  12, "system-design"),
        ("System Design", 10):     (12, 14, "system-design"),
        ("Java Springboot", 11):   (6,  8,  "java"),
    }
    pp_file = BASE / "data" / "programming_pathshala_courses.json"
    if pp_file.exists():
        pp_data = load_json(pp_file, {})
        for course in pp_data.get("courses", []):
            cname = course["course_name"]
            for module in course.get("modules", []):
                mnum = module["module_number"]
                key = (cname, mnum)
                if key not in PP_WEEK_MAP:
                    continue  # skip non-interview-relevant modules (Full Stack, etc.)
                ws, we, category = PP_WEEK_MAP[key]
                for topic in module.get("topics", []):
                    topic_id = topic.get("topic_id", "")
                    # Map topic to a PP URL (best-effort — platform requires auth)
                    topic_url = f"{PP_BASE_URL}/learn/renaissance/topics/{topic_id}" if topic_id else PP_BASE_URL
                    items.append({
                        "id":        f"pp_{topic_id}",
                        "category":  category,
                        "source":    "pp",
                        "source_label": "Programming Pathshala",
                        "week_start": ws,
                        "week_end":  we,
                        "module":    f"Module {mnum}: {module['module_name']}",
                        "section":   module["module_name"],
                        "title":     topic["topic_name"],
                        "url":       topic_url,
                        "item_type": "lesson",
                        "difficulty": "",
                        "duration":  topic.get("estimated_duration", ""),
                    })

    items.sort(key=lambda x: (x["week_start"], x["source"], x["category"]))
    return {"items": items, "total": len(items)}
