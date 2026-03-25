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
    """Serve course curriculum JSON for portal Courses tab.
    Priority: hellointerviewcourse.json → programming_pathshala_courses.json → error.
    """
    for candidate in [
        BASE / "data" / "hellointerviewcourse.json",
        BASE / "data" / "programming_pathshala_courses.json",
    ]:
        if candidate.exists():
            return load_json(candidate, {})
    return {"error": "No course JSON found. Expected hellointerviewcourse.json or programming_pathshala_courses.json at project root."}
