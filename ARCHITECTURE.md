# PrepForge — Architecture Reference

Personal interview prep platform. Tracks DSA, mocks, behavioral, intel scraping, and AI coaching in one place. Built to be deployable to Railway via Docker with zero external database dependencies.

---

## 1. System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                 │
│                                                                     │
│  prep.py (CLI)          portal/index.html (Single-file Web UI)      │
│  100+ commands          Vanilla JS, no build step, served by API    │
│  aliases: prep plan,    Fetch → /api/* endpoints                    │
│  prep log, prep lc,     SSE stream for coach responses              │
│  prep jqa, prep mock    Static HTML/CSS/JS, no framework            │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ HTTP / local file read
┌───────────────────────────────▼─────────────────────────────────────┐
│                     app/ — FastAPI Server                           │
│                                                                     │
│  main.py                                                            │
│  ├─ RateLimitMiddleware (sliding window, in-memory, per-IP)         │
│  ├─ CORSMiddleware                                                  │
│  ├─ lifespan: init_db() + start_scheduler()                         │
│  └─ Router includes:                                                │
│      /api/           → progress.py    (progress.json CRUD)          │
│      /api/intel/     → intel_routes.py (experiences, trending)      │
│      /api/           → coach.py       (Claude streaming + RAG)      │
│      /api/           → career.py      (TC intel, company profiles)  │
│      /api/           → practice.py    (drill, mock, LLD, behavioral)│
│      /api/           → feedback.py    (activity log, AI plans)      │
│      GET /           → portal/index.html (raw HTML response)        │
│      GET /api/curriculum → merged HI + PP curriculum                │
│                                                                     │
│  scheduler.py (APScheduler, in-process)                             │
│  ├─ 06:00 IST daily   → job_scrape_all()                           │
│  ├─ every 4h          → job_sync_leetcode() (LeetCode GraphQL API)  │
│  ├─ 08:00 IST daily   → job_morning_brief() (ntfy.sh push)          │
│  └─ Sunday 08:00 IST  → job_weekly_trend_report()                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ Python imports (no HTTP between layers)
┌───────────────────────────────▼─────────────────────────────────────┐
│                     intel/ — Business Logic Layer                   │
│                                                                     │
│  db.py              SQLite schema + CRUD (WAL mode, foreign keys)   │
│  config.py          Paths, API keys from env, PROFILE dict,         │
│                     TARGET_COMPANIES, LEVEL_EXPECTATIONS            │
│  feedback_engine.py Activity logging + context builder + LLM plans  │
│  drill.py           211 DSA problems, NeetCode150 + extras,         │
│                     company tags, Java tips, daily selection logic   │
│  java_qa.py         123 P0 Java/Spring/Concurrency questions        │
│  mock_engine.py     Mock score tracking, readiness % per company    │
│  lld_engine.py      20 LLD problems, SOLID rubrics, AI evaluation   │
│  behavioral.py      14 Amazon LPs, gap detection, Bar Raiser probes │
│  analyzer.py        Trending topic analysis (Counter over DB rows)  │
│  brief.py           Morning brief generator + ntfy.sh HTTP push     │
│  scraper.py         Orchestrates all source scrapers                │
│  coach.py           (module-level Claude helpers, not the router)   │
│  pp_tracker.py      Programming Pathshala progress tracking         │
│  hello_interview.py Hello Interview course helpers                  │
│  resources.py       Resource catalog (GitHub repos, books, courses) │
│                                                                     │
│  sources/                                                           │
│  ├─ reddit.py           OAuth2 client_credentials scraper           │
│  ├─ leetcode_discuss.py GraphQL scraper (categoryTopicList query)    │
│  ├─ enginebogie.py      HTML scraper (enginebogie.com)              │
│  ├─ blind_helloiv.py    Blind + HelloInterview status tracker       │
│  └─ levelsfyi.py        Levels.fyi TC data scraper                  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ sqlite3 (stdlib)
┌───────────────────────────────▼─────────────────────────────────────┐
│                     PERSISTENCE LAYER                               │
│                                                                     │
│  data/interviews.db    SQLite (WAL mode)                            │
│  ├─ experiences        scraped interview posts                      │
│  ├─ experience_rounds  individual round details                     │
│  ├─ company_intel      aggregated company profiles                  │
│  ├─ trending_topics    rolling frequency counts                     │
│  ├─ jd_analyses        AI JD analysis results                       │
│  ├─ resource_log       study resources catalog                      │
│  ├─ drill_sessions     DSA drill history                            │
│  ├─ mock_sessions      mock round scores                            │
│  ├─ lld_sessions       LLD practice scores                          │
│  ├─ activity_log       all study activities (feedback engine)       │
│  └─ llm_plans          cached AI-generated daily/weekly plans       │
│                                                                     │
│  logs/progress.json    flat JSON state                              │
│  ├─ lc_sync            LeetCode stats (total, easy/med/hard,        │
│  │                     java_problems, cpp_problems, streak)         │
│  ├─ applications[]     job applications log                         │
│  ├─ offers[]           offers received                              │
│  ├─ daily_logs{}       date → string[] activity notes               │
│  └─ topics_done[]      curriculum topics completed                  │
│                                                                     │
│  data/hellointerviewcourse.json    5 HI courses, 218 lessons        │
│  data/programming_pathshala_courses.json   5 PP courses, 18 modules │
└─────────────────────────────────────────────────────────────────────┘

External APIs (outbound only):
  Anthropic API     → /v1/messages (planning: claude-haiku, coach: claude-sonnet)
  Reddit OAuth2     → /api/v1/access_token + /search.json
  LeetCode GraphQL  → /graphql (stats sync + discuss scraping)
  ntfy.sh           → HTTP POST (morning brief push notification)
```

---

## 2. Component Descriptions

### prep.py — CLI Tracker

Single-file Python script (~600 lines). No dependencies. Reads/writes `logs/progress.json` directly. All 26 weeks of DSA plan, task lists, and company interview formats are inlined as dicts.

Key commands: `plan` (today's schedule), `log` (record activity), `status` (dashboard), `lc <problem>` (mark LC done), `apply <company>` (log application), `offer <company>`, `jqa` (Java Q&A drill), `mock` (score tracking), `drill` (DSA drill), `sources` (scraper status), `ib` (InterviewBit tracker).

The CLI can also call local API endpoints if the server is running, but defaults to direct file I/O so it works offline.

### app/main.py — FastAPI Server

Entry point. Responsibilities:
- Registers all routers
- Applies `RateLimitMiddleware` globally
- On startup: calls `init_db()` and starts APScheduler
- Serves `portal/index.html` at `/` as a raw HTML string (no static files mount needed)
- Exposes `/api/curriculum` which merges Hello Interview + Programming Pathshala JSON at request time with week-mapping logic baked in

### app/scheduler.py — Background Jobs

Uses `APScheduler.BackgroundScheduler` (in-process, no Celery/Redis). Four jobs:
- Daily scrape (6 AM IST)
- LeetCode GraphQL stats sync (every 4h)
- Morning brief push to ntfy.sh (8 AM IST)
- Weekly trend report generation (Sunday 8 AM IST)

Degrades gracefully: if `apscheduler` is not installed, logs a warning and continues without background jobs.

### app/routers/coach.py — AI Coach

Two endpoints: `/api/coach` (blocking) and `/api/coach/stream` (SSE). Both use `urllib.request` directly — no Anthropic SDK, no extra dependency. The streaming endpoint reads the SSE response line-by-line and re-emits `data: {"text": "..."}` chunks.

RAG integration: before each call, `_get_rag_context()` queries `experiences` table filtered by company and injects the top 3 summaries into the system prompt.

Six context types with distinct system prompts: `jd`, `answer_eval`, `star`, `readiness`, `mock`, `general`. Two model tiers: `claude-haiku` for planning (fast, cheap), `claude-sonnet` for coaching (higher quality).

### app/routers/feedback.py — Activity Log + AI Plans

`POST /api/log` inserts into `activity_log`. `GET /api/plan/daily` returns the cached plan for today from `llm_plans` or generates a new one. `POST /api/plan/daily/refresh` forces regeneration. Same pattern for weekly. `BackgroundTasks` is imported but plans are generated synchronously on first request to avoid stale responses.

### intel/feedback_engine.py — Context Builder + LLM Planning

`_build_context()` assembles a markdown context string from:
1. `progress.json` (LC count, streak, applications)
2. `activity_log` (last 3 days for daily, 7 days for weekly)
3. `mock_sessions` (recent scores)
4. `trending_topics` (what companies asked recently)
5. `experiences` (recent target-company interview posts)
6. War plan week theme (hardcoded week→theme map)

This context is then sent to Claude with a structured prompt asking for a specific format (analysis + priority tasks + time blocks).

Plan caching: `llm_plans` table has `UNIQUE(date, period)`. First request generates and caches. Subsequent requests return cached version unless `force=True`. Cache key is today's ISO date for daily, Monday's date for weekly.

### intel/db.py — Database Layer

All SQL is raw SQLite via `sqlite3` stdlib. Every connection enables WAL mode (`PRAGMA journal_mode=WAL`) and foreign keys. `init_db()` uses `CREATE TABLE IF NOT EXISTS` — safe to call on every startup without migrations.

`INSERT OR IGNORE` on experiences (idempotent by `UNIQUE(source, source_id)`). `INSERT OR REPLACE` on `llm_plans`. `ON CONFLICT DO UPDATE` for `company_intel`.

### intel/drill.py — DSA Drill Engine

211 problems total: NeetCode 150 + additional company-tagged extras. Each problem is a tuple: `(lc_id, name, difficulty, pattern, [companies], java_tip)`.

Daily selection logic: picks 3 problems based on current week's topic (from 26-week plan), company filter if provided, and Java deficit (problems previously done in C++ are prioritized). `mark_drill_done()` inserts into `drill_sessions`.

### intel/sources/reddit.py — Reddit Scraper

Two-mode design: with `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` env vars, uses OAuth2 client credentials flow (`grant_type=client_credentials`). Without credentials, falls back to public `.json` endpoints (works locally, gets rate-limited/blocked on Railway).

Token caching: module-level `_oauth_token` + `_token_expiry`. Refreshes when within 60 seconds of expiry.

Scrapes 6 subreddits with keyword filters. Parses posts into the standard `experiences` schema and calls `insert_experience()` (idempotent).

### intel/sources/leetcode_discuss.py — GraphQL Scraper

Uses the `categoryTopicList` GraphQL query with `categories: ["interview-experience"]`. Extracts company name from post title/tags by matching against `KNOWN_COMPANIES` list. Normalizes into the `experiences` schema.

### intel/analyzer.py — Trend Analysis

Reads `experience_rounds` joined to `experiences` and uses `collections.Counter` to aggregate topic frequencies, round type distributions, and difficulty distributions. No ML — pure frequency counting over the last N days. Results feed into the LLM context for the feedback engine.

### portal/index.html — Web Portal

Single HTML file (~1500+ lines). Vanilla JS with `fetch()` calls to the API. No build step, no npm, no webpack. Served directly by FastAPI as an HTML string. Supports: dashboard, drill view, mock tracker, LLD practice, behavioral gaps, curriculum viewer, AI coach chat with streaming (reads SSE via `EventSource`).

---

## 3. Data Flow — User Action End to End

### Example: User logs a LeetCode solve from the portal

```
1. User fills form in portal/index.html
   → POST /api/log
   { activity_type: "lc", title: "Two Sum", duration_mins: 25,
     outcome: "solved", confidence: 4 }

2. RateLimitMiddleware (main.py:55)
   → checks _rate_store[ip], sliding window 120 req/60s
   → appends timestamp, allows through

3. feedback.router POST /api/log (feedback.py:39)
   → Pydantic validates LogRequest
   → calls intel.feedback_engine.log_activity()

4. feedback_engine.log_activity() (feedback_engine.py:70)
   → calls init_feedback_tables() (CREATE TABLE IF NOT EXISTS, idempotent)
   → sqlite3 INSERT INTO activity_log
   → returns new row id

5. Response: { "id": 42, "logged": True }

6. Next time user hits GET /api/plan/daily:
   → feedback_engine.generate_daily_plan()
   → checks llm_plans WHERE date=today AND period='daily'
   → if found and not force: returns cached {"plan": "...", "cached": True}
   → if not found:
       → _build_context("daily") pulls activity_log, progress.json,
         mock_sessions, trending_topics, experiences
       → _call_claude() → POST https://api.anthropic.com/v1/messages
         model: claude-haiku-4-5, max_tokens: 800
       → INSERT OR REPLACE INTO llm_plans
       → returns {"plan": "...", "cached": False}
```

### Example: Scheduled scrape (6 AM IST)

```
scheduler.py job_scrape_all()
  → intel/scraper.py run_scraper()
      → sources/reddit.py
          → _get_oauth_token() → POST reddit.com/api/v1/access_token
            (client_credentials grant, Base64 encoded credentials)
          → GET oauth.reddit.com/r/leetcode/search.json?q=...
          → parse posts → db.insert_experience()
               → INSERT OR IGNORE INTO experiences (source, source_id, ...)
                 UNIQUE(source, source_id) prevents duplicate inserts
      → sources/leetcode_discuss.py
          → POST leetcode.com/graphql (categoryTopicList query)
          → parse edges → db.insert_experience()
  → stats logged: N new experiences inserted
```

---

## 4. Database Schema

All tables in `data/interviews.db` (SQLite). WAL mode enabled on every connection.

```sql
-- Interview experience posts scraped from external sources
experiences (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    source        TEXT NOT NULL,        -- leetcode_discuss | reddit | blind | enginebogie
    source_id     TEXT,                 -- post ID from source (used for dedup)
    company       TEXT NOT NULL,
    role          TEXT DEFAULT 'SDE-2',
    date_posted   TEXT,                 -- ISO date from source
    date_scraped  TEXT NOT NULL,        -- when we stored it
    title         TEXT,
    body_raw      TEXT,                 -- original scraped text (not exposed via API)
    body_summary  TEXT,                 -- AI-generated summary (optional)
    overall_result TEXT,               -- offer | reject | ghosted | pending
    tc_offered    TEXT,
    prep_duration TEXT,
    resources_used TEXT,               -- JSON array
    tips          TEXT,
    url           TEXT,
    UNIQUE(source, source_id)          -- idempotent scraping
)

-- Individual rounds within an experience
experience_rounds (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    experience_id  INTEGER NOT NULL REFERENCES experiences(id),
    round_num      INTEGER,
    round_type     TEXT NOT NULL,      -- dsa | system_design | lld | behavioral | hr | machine_coding
    question       TEXT,
    difficulty     TEXT,               -- easy | medium | hard
    topics         TEXT,               -- JSON array: ["graphs", "dfs", "topological_sort"]
    key_insights   TEXT,
    outcome        TEXT,               -- pass | fail | unknown
    duration_mins  INTEGER
)

-- Aggregated company-level intelligence
company_intel (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company     TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    process     TEXT,                  -- JSON
    common_questions TEXT,            -- JSON array
    dsa_difficulty TEXT,
    sd_topics   TEXT,                 -- JSON array
    lld_topics  TEXT,                 -- JSON array
    behavioral_focus TEXT,
    tc_range    TEXT,
    tips        TEXT,                 -- JSON array
    success_patterns TEXT,            -- JSON array
    failure_patterns TEXT,            -- JSON array
    UNIQUE(company)
)

-- Trending topics (rolling frequency, refreshed weekly)
trending_topics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date_logged TEXT NOT NULL,
    company     TEXT,                  -- NULL = cross-company trend
    topic_type  TEXT NOT NULL,         -- dsa | sd | lld | behavioral
    topic       TEXT NOT NULL,
    frequency   INTEGER DEFAULT 1,
    examples    TEXT                   -- JSON array of question samples
)

-- AI JD analysis results
jd_analyses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date_done   TEXT NOT NULL,
    company     TEXT NOT NULL,
    role        TEXT NOT NULL,
    jd_text     TEXT,
    required_skills TEXT,             -- JSON
    gap_analysis TEXT,                -- JSON
    study_plan  TEXT,                 -- AI-generated markdown
    similar_experiences TEXT          -- JSON array of experience IDs
)

-- Study resource catalog
resource_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date_added  TEXT NOT NULL,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,         -- dsa | sd | lld | behavioral | java | full
    url         TEXT,
    source_type TEXT,                  -- book | course | github | youtube | blog | platform
    priority    TEXT DEFAULT 'P1',     -- P0 | P1 | P2
    notes       TEXT,
    completed   INTEGER DEFAULT 0,
    rating      INTEGER                -- 1-5
)

-- DSA drill session history
drill_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date_done    TEXT NOT NULL,
    problem_name TEXT NOT NULL,
    time_mins    INTEGER DEFAULT 0,
    struggled    INTEGER DEFAULT 0,    -- boolean 0/1
    language     TEXT DEFAULT 'java'
)

-- Mock round scores
mock_sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date_done       TEXT NOT NULL,
    company         TEXT NOT NULL,
    round_type      TEXT NOT NULL,     -- dsa | system_design | lld | behavioral
    score           REAL NOT NULL,     -- 1.0–5.0
    questions_json  TEXT,              -- JSON array
    time_mins       INTEGER DEFAULT 0,
    notes           TEXT,
    hire_verdict    TEXT               -- hire | no_hire
)

-- LLD practice scores
lld_sessions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    date_done    TEXT NOT NULL,
    problem_key  TEXT NOT NULL,        -- parking-lot | lru-cache | etc.
    score        INTEGER NOT NULL,     -- 1–5
    time_mins    INTEGER DEFAULT 0,
    notes        TEXT
)

-- Activity feed (all study activities)
activity_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    logged_at     TEXT DEFAULT (datetime('now')),
    date          TEXT NOT NULL,       -- YYYY-MM-DD
    activity_type TEXT NOT NULL,       -- lc | mock | curriculum | lld | jqa | system_design | behavioral | notes | drill
    title         TEXT,
    details       TEXT,                -- JSON blob
    duration_mins INTEGER DEFAULT 0,
    difficulty    TEXT,
    outcome       TEXT,                -- solved | struggled | failed | watched | practiced | skipped
    confidence    INTEGER DEFAULT 3,   -- 1–5
    notes         TEXT
)

-- Cached AI-generated plans
llm_plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT DEFAULT (datetime('now')),
    date            TEXT NOT NULL,     -- YYYY-MM-DD (today for daily, Monday for weekly)
    period          TEXT NOT NULL,     -- daily | weekly
    plan_text       TEXT,              -- markdown from Claude
    analysis_text   TEXT,
    context_summary TEXT,              -- first 500 chars of context sent to LLM (for debugging)
    UNIQUE(date, period)               -- one plan per day per period
)
```

Indexes: `idx_drill_date`, `idx_mock_company`, `idx_mock_date`, `idx_lld_date`, `idx_exp_company`, `idx_exp_date`, `idx_exp_source`, `idx_rounds_type`, `idx_rounds_topics`, `idx_trending_date`, `idx_trending_company`.

---

## 5. Key Design Decisions

### SQLite, not PostgreSQL

Single-user app. No concurrent writes from multiple processes. SQLite in WAL mode supports concurrent reads with one writer — sufficient here. The entire database ships in one file, can be volume-mounted in Docker, and backs up trivially (`cp interviews.db interviews.db.bak`). Zero ops overhead. On Railway, it's a mounted volume. Switching to Postgres would add a managed DB service, connection pooling, and migration tooling for no benefit at this scale.

### Single-file portal (no build step)

`portal/index.html` is ~1500 lines of vanilla HTML/CSS/JS. No React, no Vite, no `node_modules`. Reasons:
1. FastAPI serves it as a string — no static file server configuration needed
2. Deployable anywhere that runs Python
3. Changes are visible immediately without a build step
4. For a personal tool used by one person, React adds zero value

Tradeoff: no component reuse, no TypeScript type safety. Acceptable for this scope.

### No Anthropic SDK

Both `feedback_engine.py` and `coach.py` call the Anthropic API using `urllib.request` directly. This eliminates one dependency from `requirements.txt` and keeps the Docker image smaller. The API contract (`/v1/messages`, `anthropic-version` header, SSE format) is stable enough that the SDK would be overkill.

### In-process scheduler (APScheduler), not Celery

Celery requires a message broker (Redis/RabbitMQ) and a separate worker process. APScheduler runs in the same Python process as FastAPI. For a single-user prep tool with four scheduled jobs, this is the right tradeoff. If APScheduler is not installed, the app degrades gracefully — background jobs are skipped but the API works.

### Config via environment variables, not a config file

All secrets (`ANTHROPIC_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `PORTAL_SECRET`) are read from environment variables. `intel/config.py` uses `os.environ.get()` with empty-string defaults. Locally, a `.env` file works. On Railway, they're set in the variables panel. `config_local.py` is gitignored for local overrides.

### JSON for progress state, SQLite for intel

`logs/progress.json` holds the prep state (LC count, applications, offers, daily notes). It's modified by both `prep.py` (CLI) and the scheduler (LC sync job). Using a flat JSON file for this keeps `prep.py` dependency-free — it only uses stdlib. The intel data (experiences, trends, plans) goes into SQLite because it's relational, grows over time, and needs indexed queries.

### Two-tier LLM model strategy

- `claude-haiku` for daily/weekly planning (`feedback_engine.py`): fast, cheap, runs at scheduled times
- `claude-sonnet` for coaching, JD analysis, answer evaluation (`coach.py`): higher quality, user-initiated on-demand

Rate limiting on `/api/coach`: 30 req/min (stricter than the global 120 req/min) because it calls the expensive model.

---

## 6. System Design Patterns Implemented

### Rate Limiting — Sliding Window

`main.py:43` implements sliding window rate limiting in ~10 lines:
```python
hits = [h for h in hits if now - h < window]  # evict old timestamps
if len(hits) >= limit: return False
hits.append(now)
```
This is a sliding window log variant. Each request stores its timestamp; on the next request, expired timestamps are filtered out. Interviewer note: token bucket is more memory-efficient at high scale (store only count + refill rate), sliding window log is exact but stores all timestamps. This implementation is O(hits) per request — fine for single-user, would need Redis + sorted sets at multi-tenant scale.

### Background Task Queue — APScheduler + FastAPI BackgroundTasks

Two patterns coexist:
- APScheduler for time-based jobs (scraping, sync) — runs on a daemon thread
- FastAPI `BackgroundTasks` is imported in `feedback.py` for non-blocking operations (used for future plan pre-generation)

The scheduler uses `CronTrigger` with IST timezone. Job isolation: each job has its own try/except — one failing job does not kill the scheduler.

### LLM Integration — Context Building + Prompt Engineering + Caching

Three-layer pattern:
1. **Context assembly** (`_build_context()`): pulls structured data from multiple sources (JSON file, SQLite tables) and formats it as markdown. The context is the most important part — garbage in, garbage out.
2. **Prompt engineering**: fixed-format output requested from Claude (Analysis / Priority Tasks / Time Blocks / Watch For). This makes the response machine-parseable if needed.
3. **Response caching** (`llm_plans` table with `UNIQUE(date, period)`): `INSERT OR REPLACE` on force-refresh, `SELECT` check first on normal request. Cache key is date-based. Cost implication: without caching, every portal load would call the API. With caching, the API is called at most once per day per plan type.

### OAuth2 Client Credentials Flow (Reddit)

`sources/reddit.py` implements the full OAuth2 machine-to-machine flow:
1. Base64-encode `client_id:client_secret`
2. POST to `/api/v1/access_token` with `grant_type=client_credentials`
3. Extract `access_token` and `expires_in`
4. Cache token in module-level variable, refresh 60s before expiry
5. Use `Authorization: Bearer <token>` on all API calls

This is the standard OAuth2 flow for server-to-server integrations. Contrast with auth code flow (requires user redirect) or implicit flow (deprecated). The fallback to public endpoints covers the local development case where credentials aren't set.

### Event-Driven Scraping — Scheduler → Scraper → DB

```
CronTrigger(6:00 IST) → job_scrape_all() → run_scraper()
  → reddit.py: fetch posts → insert_experience() → DB
  → leetcode_discuss.py: GraphQL query → insert_experience() → DB
```
The scrapers are stateless functions. Idempotency is guaranteed by `UNIQUE(source, source_id)` + `INSERT OR IGNORE`. Re-running the same scrape multiple times produces the same DB state.

### Idempotent Writes — UNIQUE Constraints

Three patterns used:
- `INSERT OR IGNORE` on `experiences`: scraping the same Reddit post twice inserts once
- `INSERT OR REPLACE` on `llm_plans`: force-refresh replaces the existing plan for that date
- `ON CONFLICT(company) DO UPDATE` on `company_intel`: upsert pattern

These are SQLite's equivalent of Postgres `ON CONFLICT`. In distributed systems, idempotency prevents double-processing in message queues (exactly-once semantics).

### WAL Mode SQLite for Concurrent Reads

```python
conn.execute("PRAGMA journal_mode=WAL")
```
WAL (Write-Ahead Logging) allows readers to proceed while a writer is active. Without WAL, SQLite uses exclusive write locks that block all readers. With WAL, the scheduler's write job (LC sync, scraping) does not block the API's read queries. Relevant at interview: WAL trades slightly more disk I/O for better read concurrency. Not suitable if you need to run multiple writer processes — still single-writer.

### Separation of Concerns — CLI / API / DB Layers

```
prep.py       → reads/writes progress.json, calls graphql directly
               (no dependency on intel/ or app/)

app/routers/  → HTTP layer, Pydantic validation, rate limiting
               (imports intel/* but has no DB calls of its own)

intel/*.py    → business logic, DB access, external API calls
               (no HTTP server concerns)

intel/db.py   → all SQL, no business logic
```
`prep.py` works completely offline. The API layer has no SQL. The intel layer has no HTTP request handling. This separation means you can test `intel/` functions without spinning up a server, and you can swap the CLI for a different client without changing any business logic.

### RAG (Retrieval-Augmented Generation) for AI Coaching

`coach.py:_get_rag_context()` queries the `experiences` table filtered by company before every Claude call. The retrieved summaries are appended to the system prompt:
```
--- RELEVANT INTERVIEW EXPERIENCES FROM DB ---
[Razorpay SDE-2] "Offer after 4 rounds, heavy on system design..."
```
This grounds the AI coach's responses in real, recent interview data from the same target company. Classic RAG pattern: retrieve relevant documents → inject into prompt → generate.

### Single-File Frontend — No Build Step

The portal is served from FastAPI's `@app.get("/")` route reading `portal/index.html` as a string. This means:
- No `StaticFiles` mount required
- No CORS issue for the portal itself (same origin as the API)
- Streaming SSE for the coach works natively via `EventSource`

The SSE consumer in the portal reads `data: {"text": "..."}` chunks and appends them to the UI, creating the typing effect without any WebSocket setup.

---

## 7. What to Say About This Project in Interviews

### The core pitch (30 seconds)

"I built a personal interview prep platform called PrepForge — a FastAPI backend with a Python CLI and single-file web portal. It scrapes interview experiences from Reddit and LeetCode Discuss using OAuth2 and GraphQL, stores them in SQLite with idempotent writes, and uses Claude to generate adaptive daily prep plans based on my activity logs and trending topics at target companies. I also built a streaming AI coach endpoint with RAG — it retrieves relevant interview experiences from the DB before calling Claude, so responses are grounded in real recent data."

### Deep-dive angles (pick based on the round)

**System Design round:**
- "I implemented sliding window rate limiting as Starlette middleware — each request logs its timestamp, expired ones are evicted, enforces stricter limits on the expensive AI endpoint"
- "The scheduler runs in-process using APScheduler — no Redis, no Celery. For a single-user tool this is the right call, but I know the failure mode: if the server crashes, in-flight jobs are lost, and there's no job queue to replay from"
- "LLM plan caching uses a `UNIQUE(date, period)` constraint with `INSERT OR REPLACE` — so force-refresh replaces the cached plan atomically"

**Distributed Systems / Infra round:**
- "SQLite in WAL mode lets the scheduler's write jobs run concurrently with API read queries — WAL keeps a separate log file and merges at checkpoint, readers see a consistent snapshot"
- "Idempotent scraping: `UNIQUE(source, source_id)` + `INSERT OR IGNORE` means re-running the scraper on the same data produces identical DB state — same principle as idempotent Kafka consumers"
- "The Reddit scraper has two modes: OAuth2 client credentials for production (Railway blocks public endpoints), public JSON fallback for local dev"

**LLD / OOP round:**
- "The intel layer is organized as pure functions by domain — `drill.py`, `mock_engine.py`, `lld_engine.py` — each with a single responsibility. The router layer just delegates to them."
- "The LLM context builder uses the Builder pattern conceptually — assembles a structured context string from multiple data sources before calling the API"

**Behavioral round (Ownership, Invent and Simplify):**
- "I built this because existing prep trackers don't adapt — they don't know what I struggled with yesterday or what Razorpay has been asking this month. I integrated scraped data + personal logs + LLM to close that gap."
- "I chose SQLite over Postgres intentionally — eliminated a managed DB dependency, zero ops, backs up with a file copy. When scale doesn't demand Postgres, using it is over-engineering."
- "The platform runs on Railway for ~$5/month. I containerized it in a multi-layer Dockerfile with a non-root user (`useradd -m -u 1001 prepforge`). The volumes mount at `./data` and `./logs` so the DB persists across deploys."

### Connecting to GSTN experience

This project uses the same architectural patterns as GSTN at a smaller scale:
- Kafka consumer idempotency (GSTN) → scraper `INSERT OR IGNORE` idempotency
- Redis distributed cache with TTL (GSTN DistCacheUtil) → `llm_plans` table with date-keyed cache and force-refresh
- Strategy pattern for fee/workflow (GSTN Case engine) → `_build_system()` in coach.py selects prompt template by context_type
- XA transactions across shards (GSTN ledger) → SQLite WAL for concurrent access (same problem, different scale)
- Kafka DLQ for error isolation (GSTN) → APScheduler job isolation with per-job try/except

The honest framing: "GSTN taught me to design for correctness and fault isolation at scale. PrepForge let me apply the same principles in a system I designed end-to-end — which exposed the tradeoffs more clearly because I made every decision myself."
