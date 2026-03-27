# PrepForge — Technical Design Document

**System:** Personal Interview Preparation Intelligence Platform  
**Stack:** Python 3.11 (FastAPI) + React 19 (Vite) + SQLite + Claude API  
**Author:** Jayanti Vishnoi  
**Last Updated:** March 2026

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Data Layer — SQLite with WAL](#3-data-layer--sqlite-with-wal)
4. [RAG Pipeline — Keyword-Based Retrieval](#4-rag-pipeline--keyword-based-retrieval)
5. [LLM Integration — Claude API](#5-llm-integration--claude-api)
6. [Streaming SSE — Server to Browser](#6-streaming-sse--server-to-browser)
7. [Web Scraping Pipeline](#7-web-scraping-pipeline)
8. [Background Scheduling](#8-background-scheduling)
9. [Rate Limiting — Sliding Window](#9-rate-limiting--sliding-window)
10. [Adaptive Planning Engine](#10-adaptive-planning-engine)
11. [Drill Selection Algorithm](#11-drill-selection-algorithm)
12. [Mock Score Trending](#12-mock-score-trending)
13. [React Frontend Architecture](#13-react-frontend-architecture)
14. [Multi-Stage Docker Build](#14-multi-stage-docker-build)
15. [Trade-Offs and Design Decisions](#15-trade-offs-and-design-decisions)
16. [Interview Talking Points](#16-interview-talking-points)

---

## 1. System Overview

PrepForge is a **single-user, full-stack application** that combines data scraping, LLM-powered coaching, progress tracking, and practice tools into one system. It serves three interfaces:

```
                    ┌──────────────┐
                    │   Browser    │
                    │  React SPA   │
                    └──────┬───────┘
                           │ fetch /api/*
                           ▼
┌──────────┐      ┌────────────────┐       ┌─────────────┐
│  CLI     │─────▶│   FastAPI      │──────▶│  Claude API  │
│ prep.py  │      │   (uvicorn)    │       │  (Anthropic) │
└──────────┘      │                │       └─────────────┘
                  │  APScheduler   │
                  │  (cron jobs)   │       ┌─────────────┐
                  │                │──────▶│  Reddit API  │
                  └───────┬────────┘       │  LeetCode GQL│
                          │                └─────────────┘
                  ┌───────┴────────┐
                  │    SQLite      │
                  │  (WAL mode)    │
                  │  interviews.db │
                  └────────────────┘
```

**Key constraint:** Single-user, single-process. This simplifies many decisions (no Redis, no Postgres, no Celery, no auth) while keeping the system production-deployable on a $5/month Railway instance.

---

## 2. Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────┐
│  Presentation Layer                              │
│  ├── ui/ (React 19 + Vite)                      │
│  │   ├── Pages (16 routes via React Router)     │
│  │   ├── Components (charts, timers, cards)     │
│  │   └── Hooks (TanStack Query, timer)          │
│  └── prep.py (CLI, 55+ commands)                │
├─────────────────────────────────────────────────┤
│  Transport Layer                                 │
│  └── app/ (FastAPI)                              │
│      ├── main.py (middleware, lifespan, SPA)    │
│      ├── routers/ (60+ endpoints, 6 modules)   │
│      └── scheduler.py (APScheduler, 4 jobs)     │
├─────────────────────────────────────────────────┤
│  Domain Layer                                    │
│  └── intel/ (business logic)                     │
│      ├── knowledge_base.py (chunking + keyword RAG) │
│      ├── coach.py (Claude prompt engineering)   │
│      ├── analyzer.py (gap analysis, readiness)  │
│      ├── drill.py (problem selection algorithm) │
│      ├── mock_engine.py (score trending)        │
│      ├── feedback_engine.py (adaptive planning) │
│      ├── scraper.py (source orchestration)      │
│      └── sources/ (Reddit, LeetCode, HN)        │
├─────────────────────────────────────────────────┤
│  Persistence Layer                               │
│  ├── data/interviews.db (SQLite, WAL, 9 tables) │
│  ├── logs/progress.json (flat-file state)       │
│  └── data/portal_data.json (UI state)           │
└─────────────────────────────────────────────────┘
```

### Request Flow (AI Coach example)

```
Browser POST /api/coach/stream
  │
  ├── RateLimitMiddleware: sliding window check (30 req/min for coach)
  │
  ├── coach.py router:
  │     ├── Extract last user message as RAG query
  │     │
  │     ├── _get_rag_context(query, company):
  │     │     ├── knowledge_base.get_coach_context()
  │     │     │     ├── search_kb(): keyword scoring across kb_chunks
  │     │     │     └── Returns top-K chunks as formatted text
  │     │     ├── db.search_experiences(): recent interview posts
  │     │     └── exp_extractor.get_enriched_questions()
  │     │
  │     ├── _build_system(rag_ctx): inject PROFILE + RAG into system prompt
  │     │
  │     └── _call_claude_stream():
  │           ├── POST to api.anthropic.com with stream=True
  │           ├── Read line-by-line, yield SSE data frames
  │           └── StreamingResponse(generator, media_type="text/event-stream")
  │
  └── Browser: ReadableStream.getReader() → parse SSE → update React state
```

---

## 3. Data Layer — SQLite with WAL

### Why SQLite

- **Zero configuration:** Ships with Python, no database server to manage
- **WAL mode:** Allows concurrent reads during writes (critical for scraper + API serving simultaneously)
- **Single-file:** Easy backup, volume mount in Docker, Railway persistent disk

### Schema (9 core tables)

```sql
-- Scraped interview experiences
experiences (
    id INTEGER PRIMARY KEY,
    source TEXT,              -- 'reddit', 'leetcode_discuss', 'enginebogie'
    source_id TEXT,           -- Original post ID for dedup
    company TEXT,
    role TEXT,
    date_posted TEXT,
    date_scraped TEXT,
    title TEXT,
    body_raw TEXT,            -- Full post (up to 5000 chars)
    body_summary TEXT,        -- AI or heuristic summary
    result TEXT,              -- 'offer', 'reject', 'pending'
    ...
    UNIQUE(source, source_id) -- Dedup constraint
);

-- Individual interview rounds per experience
experience_rounds (
    id INTEGER PRIMARY KEY,
    experience_id INTEGER REFERENCES experiences(id),
    round_type TEXT,          -- 'dsa', 'system_design', 'lld', 'behavioral'
    question TEXT,
    difficulty TEXT,
    topics TEXT,              -- JSON array of topic tags
    ...
);

-- Knowledge base chunks (keyword RAG)
kb_chunks (
    id INTEGER PRIMARY KEY,
    source_key TEXT,           -- File path identifier
    category TEXT,             -- 'system_design', 'java', 'behavioral', etc.
    chunk_idx INTEGER,
    heading TEXT,              -- Nearest markdown heading
    content TEXT,              -- Chunk text (~1200 chars)
    keywords TEXT,             -- Extracted unigrams + bigrams
    chunk_hash TEXT            -- SHA-1 of source file (for change detection)
);
```

### Pragmas

```python
conn.execute("PRAGMA journal_mode=WAL")     # concurrent reads during writes
conn.execute("PRAGMA foreign_keys=ON")      # referential integrity
```

### Indexing Strategy

Indexes target the most common query patterns (company lookups, date-range scans, round type filters):

```sql
CREATE INDEX idx_exp_company ON experiences(company);
CREATE INDEX idx_exp_date ON experiences(date_scraped);
CREATE INDEX idx_rounds_type ON experience_rounds(round_type);
CREATE INDEX idx_mock_company ON mock_sessions(company);
CREATE INDEX idx_trending_date ON trending_topics(date_logged);
```

### Deduplication

The `UNIQUE(source, source_id)` constraint on `experiences` combined with `INSERT OR IGNORE` means the scraper is **idempotent** — re-running it never creates duplicate rows. The scraper counts "new inserts" by checking if `lastrowid` is truthy after the ignore.

### JSON File Persistence

`progress.json` stores mutable user state (LeetCode done list, applications, spaced repetition, bug journal, retros, failures). This is a deliberate trade-off:
- **Pro:** Human-readable, easy backup, no schema migration
- **Con:** No concurrent write safety (acceptable for single-user)
- **Structure:** Flat object with arrays per feature (`lc_done`, `applications`, `spaced_repetition`, etc.)

---

## 4. RAG Pipeline — Keyword-Based Retrieval

### Why Not Vector Embeddings

For a corpus of ~2,000 chunks, keyword-based retrieval with domain-aware scoring is:
- **Faster to deploy:** No embedding API costs, no Qdrant/Pinecone dependency
- **Explainable:** You can see exactly why a chunk was retrieved (keyword match scores)
- **Good enough:** Domain-specific bigram boosting handles the "vocabulary problem" that embeddings solve more generally

### Chunking Algorithm

```
Input: Markdown/PDF/DOCX file → plain text
Parameters: CHUNK_SIZE=1200 chars (~300 tokens), CHUNK_OVERLAP=150

Algorithm:
  pos = 0
  while pos < len(text):
    chunk = text[pos : pos + CHUNK_SIZE]
    heading = last markdown heading (# / ## / ###) found before pos
    if len(chunk.strip()) >= 50:
      store (chunk_idx, heading, chunk)
    pos += CHUNK_SIZE - CHUNK_OVERLAP
```

The **150-character overlap** ensures that concepts spanning chunk boundaries appear in at least one chunk completely. The heading attachment gives each chunk context about which section it belongs to.

### Keyword Extraction (Index Time)

```
1. Tokenize: extract words matching [a-zA-Z][a-zA-Z0-9]{2,}
2. Remove stopwords (English + code noise: 'public', 'void', 'return')
3. Score unigrams:
   - Domain-boosted words (e.g. 'kafka', 'redis', 'concurrency'): +5 per occurrence
   - Regular words: +1 per occurrence
   - Keep top 35 by score
4. Extract bigrams:
   - Only if at least one word is in the domain boost set
   - Format: "word1_word2"
   - Keep top 20 unique bigrams
5. Store as space-separated string in 'keywords' column
```

### Retrieval Scoring (Query Time)

```
For each chunk in kb_chunks (filtered by optional category/source):

  score = 0
  for each query_word:
    if query_word in chunk.heading:   score += 10  (heading match is strongest)
    if query_word in chunk.keywords:  score += 3   (indexed keyword match)
    if query_word in chunk.content:   score += 1   (full-text fallback)

  for each query_bigram (consecutive query words):
    if bigram in chunk.keywords:      score += 6   (phrase match bonus)

  Sort by score DESC
  Deduplicate by (source_key, heading)
  Return top K results
```

### Three-Tier Scoring Rationale

| Tier | Signal | Points | Why |
|------|--------|--------|-----|
| Heading match | `heading` field | +10 | Heading = topic; strongest relevance signal |
| Keyword match | `keywords` field | +3 | Pre-extracted, domain-boosted terms |
| Content match | `content` field | +1 | Full-text substring; noisy but catches edge cases |
| Bigram bonus | `keywords` field | +6 | Phrase matching ("rate_limiter") beats single words |

### Change Detection

Each file is hashed (SHA-1, truncated to 12 hex chars). On reindex, if the hash matches existing chunks, the file is skipped. If changed, all existing chunks for that `source_key` are deleted and re-indexed.

---

## 5. LLM Integration — Claude API

### Raw HTTP (No SDK)

PrepForge uses `urllib.request` to call the Anthropic Messages API directly:

```python
payload = {
    "model": "claude-sonnet-4-5",       # from config
    "max_tokens": 4096,
    "system": system_prompt,
    "messages": [{"role": "user", "content": user_message}]
}

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps(payload).encode(),
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
)
```

**Why no SDK:** Zero external dependency for the AI layer. The `anthropic` Python package adds ~50MB of transitive deps. For a personal tool on Railway, raw HTTP keeps the Docker image small and the behavior transparent.

### Prompt Engineering Patterns

1. **Role assignment:** "You are an expert SDE-2/SDE-3 interview coach specializing in the Indian tech market"
2. **Structured output:** Prompts specify numbered sections (e.g., "1. REQUIRED SKILLS, 2. GAP ANALYSIS, 3. STUDY PLAN")
3. **Profile grounding:** The candidate's full profile (YOE, projects, strengths, weak areas, achievements) is injected into every system prompt
4. **RAG context injection:** Retrieved chunks and interview experiences are appended to the system prompt as "RELEVANT CONTEXT"
5. **Company-specific conditioning:** When a company is specified, `TARGET_COMPANIES[company]` data (level, rounds, focus areas) is added
6. **Rubric injection:** Answer evaluation includes per-round-type criteria (DSA focuses on complexity + edge cases, SD on scalability + trade-offs)

### Model Selection Strategy

| Use Case | Model | Max Tokens | Rationale |
|----------|-------|-----------|-----------|
| Coach chat, JD analysis, answer eval | claude-sonnet-4-5 | 4096 | Quality matters for coaching |
| Daily/weekly adaptive plans | claude-haiku-4-5 | 800-1200 | Cost/latency; plans are shorter |
| Streaming chat | claude-sonnet-4-5 | 2048 | Balanced quality + responsiveness |

---

## 6. Streaming SSE — Server to Browser

### Server Side (FastAPI Generator)

```python
def _call_claude_stream(system_prompt, messages):
    """Generator that yields SSE-formatted data frames."""
    payload = {
        "model": CLAUDE_MODEL,
        "stream": True,        # Enable streaming
        "system": system_prompt,
        "messages": messages,
    }

    resp = urllib.request.urlopen(req)

    for line in resp:
        line = line.decode("utf-8").strip()
        if line.startswith("data:"):
            data = json.loads(line[5:])
            if data["type"] == "content_block_delta":
                text = data["delta"]["text"]
                yield f"data: {json.dumps({'text': text})}\n\n"

    yield "data: [DONE]\n\n"
```

The router wraps this in a `StreamingResponse`:

```python
return StreamingResponse(
    generator,
    media_type="text/event-stream",
    headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"      # Prevents nginx/proxy buffering
    }
)
```

### Client Side (React fetch + ReadableStream)

```javascript
const response = await fetch('/api/coach/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history: messages.slice(-10) }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
        if (line.startsWith('data: ')) {
            const chunk = line.slice(6);
            if (chunk === '[DONE]') return;
            onChunk(chunk);  // Updates React state
        }
    }
}
```

**Why not `EventSource`?** The browser's `EventSource` API only supports GET requests. LLM chat requires POST with a JSON body, so we use `fetch` with manual SSE line parsing.

### React State Update Pattern

```javascript
const assistantMsg = { role: 'assistant', content: '' };

// Mutable buffer pattern: mutate the object, spread for React
onChunk = (chunk) => {
    assistantMsg.content += chunk;
    setMessages([...history, { ...assistantMsg }]);  // New reference triggers re-render
};
```

This is a deliberate trade-off: mutating `assistantMsg.content` avoids creating a new string for every chunk (cheaper for long responses), while spreading into `setMessages` ensures React sees a new reference.

---

## 7. Web Scraping Pipeline

### Source Orchestration

```python
SCRAPERS = {
    "leetcode_discuss": {"fn": leetcode_scrape, "label": "LeetCode Discuss"},
    "reddit":           {"fn": reddit_scrape,   "label": "Reddit"},
    "enginebogie":      {"fn": ebogie_scrape,   "label": "EngineBogie/HN"},
}

def run_scraper(source_name=None):
    for name, config in SCRAPERS.items():
        if source_name and name != source_name:
            continue
        try:
            experiences = config["fn"]()
            for exp in experiences:
                try:
                    db.insert_experience(exp)  # INSERT OR IGNORE (dedup)
                except:
                    pass  # Skip malformed rows, don't fail batch
        except:
            pass  # Skip failed sources, don't fail whole run
```

**Pattern:** Registry/strategy — each source is a callable returning a normalized list. Double try/except provides **per-source and per-row resilience**.

### Reddit OAuth2 Flow

```
1. POST https://www.reddit.com/api/v1/access_token
   - HTTP Basic Auth: client_id:client_secret
   - Body: grant_type=client_credentials

2. Cache token in module-level globals (_oauth_token, _token_expiry)
   - Reuse if now < expiry - 60s (safety margin)

3. Replace host: www.reddit.com → oauth.reddit.com
   - Add Authorization: Bearer <token>

4. Rate limit handling:
   - Read X-Ratelimit-Remaining from response headers
   - If remaining < 5: sleep(min(reset + 1, 30))
   - On 429: sleep(reset + 1, default 60)
   - On 403 with token: clear token, force re-auth

5. Retry: up to 3 attempts with 2^attempt second backoff
```

### LeetCode GraphQL

```graphql
query categoryTopicList($skip: Int, $first: Int) {
  categoryTopicList(
    orderBy: "newest_to_oldest"
    skip: $skip
    first: $first
    categories: ["interview-experience"]
  ) {
    edges {
      node {
        id, title,
        post { content, creationDate, voteCount }
        tags { name, slug }
      }
    }
  }
}
```

**Pagination:** `skip` increments by 20 (page size); stops when response is empty or `max_posts` reached.

### Experience Normalization

All scrapers output the same shape:

```python
{
    "source": "reddit",
    "source_id": "abc123",          # For UNIQUE constraint dedup
    "company": "Google",            # Extracted from title/body
    "role": "SDE-2",                # Heuristic extraction
    "title": "Google L4 Interview Experience",
    "body_raw": "...",              # Truncated to 5000 chars
    "result": "offer",              # Keyword-based classification
    "rounds": [                     # Parsed from body structure
        {"round_type": "dsa", "question": "...", "difficulty": "hard"}
    ]
}
```

---

## 8. Background Scheduling

### APScheduler Integration

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

scheduler.add_job(job_scrape_all,       CronTrigger(hour=6, minute=0))     # 6 AM daily
scheduler.add_job(job_sync_leetcode,    CronTrigger(hour="*/4", minute=30)) # Every 4h
scheduler.add_job(job_morning_brief,    CronTrigger(hour=8, minute=0))     # 8 AM daily
scheduler.add_job(job_weekly_trends,    CronTrigger(day_of_week="sun", hour=8))  # Sunday
```

**Why APScheduler over Celery/Redis?**
- Single process — no broker dependency
- Cron expressions built-in
- `BackgroundScheduler` runs in a daemon thread alongside uvicorn
- Sufficient for 4 lightweight jobs on a $5/month instance

### LeetCode Sync Job

```python
def job_sync_leetcode():
    progress = load_json("logs/progress.json")
    username = progress.get("lc_sync", {}).get("username")
    if not username:
        return

    # GraphQL query to LeetCode
    data = graphql_query("""
        query { matchedUser(username: $username) {
            submitStats { acSubmissionNum { difficulty count } }
            userCalendar(year: $year) { streak totalActiveDays }
            languageProblemCount { languageName problemsSolved }
        }}
    """)

    # Update progress atomically
    prev_total = progress["lc_sync"].get("total", 0)
    new_total = sum(d["count"] for d in data["acSubmissionNum"])

    progress["lc_sync"].update({
        "total": new_total, "easy": ..., "medium": ..., "hard": ...,
        "java_problems": ..., "streak": ..., "last_sync": now()
    })

    if new_total > prev_total:
        progress["daily_logs"][today].append(f"Auto-sync: +{new_total - prev_total}")

    save_json("logs/progress.json", progress)
```

---

## 9. Rate Limiting — Sliding Window

### Algorithm

```
Data structure: Dict[IP, List[float]]  (in-memory, per-process)

check_rate_limit(ip, limit=20, window=60):
    now = time.time()
    hits = store.get(ip, [])

    # Evict expired timestamps (sliding window)
    hits = [h for h in hits if now - h < window]

    if len(hits) >= limit:
        return False  # Rate limited

    hits.append(now)
    store[ip] = hits
    return True
```

### Path-Based Limits

```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ip = request.client.host
        limit = 30 if "/api/coach" in request.url.path else 120
        if not check_rate_limit(ip, limit=limit, window=60):
            return JSONResponse({"error": "Rate limit exceeded"}, 429)
        return await call_next(request)
```

**Trade-offs:**
- **Pro:** No Redis dependency, zero config
- **Con:** Not shared across workers (acceptable: single-process deployment)
- **Con:** No cleanup — old IPs accumulate (acceptable: single-user, low traffic)
- **Upgrade path:** Redis `ZRANGEBYSCORE` for multi-process setups

---

## 10. Adaptive Planning Engine

### How It Works

```
1. Collect context:
   ├── progress.json (LC stats, streak, week number)
   ├── activity_log table (last 3-7 days)
   ├── Weak areas (outcomes = 'struggled' or 'failed')
   ├── Mock scores (recent trend)
   ├── Trending topics (from scraper data)
   ├── Recent experiences (target companies)
   └── War plan week theme

2. Build prompt:
   "You are PrepForge, an adaptive interview coach.
    Here is the candidate's current state: [context]
    Generate a [daily/weekly] plan with:
    - Analysis of current trajectory
    - Prioritized task list
    - Time blocks
    - Risk warnings"

3. Call Claude Haiku (cheap + fast):
   - max_tokens: 800 (daily) / 1200 (weekly)
   - Single user message (no system/user split)

4. Cache in SQLite:
   llm_plans (date, period, plan_text)
   UNIQUE(date, period) — one plan per day/week
   INSERT OR REPLACE — regenerate overwrites cache
```

### Cache Strategy

- **Daily plan:** Cached by today's date. Hitting `GET /api/plan/daily` returns cached if exists, generates if not.
- **Weekly plan:** Cached by Monday's ISO date. One plan per calendar week.
- **Force refresh:** `POST /api/plan/daily/refresh` bypasses cache.

---

## 11. Drill Selection Algorithm

### Problem Pool

211 problems from NeetCode 150 + company-specific extras, each with:

```python
(lc_id, name, difficulty, pattern, companies, java_tip)
# (1, "Two Sum", "Easy", "Arrays", ["google", "amazon"], "Use HashMap")
```

### Selection Logic

```
Input: week_number, company (optional), java_count, limit=3

Path A — Warplan alignment (preferred):
  If WEEK_PROBLEMS[week_num] exists:
    Return those exact problems in order (curated by hand)

Path B — Scoring fallback:
  For each problem in deduplicated pool:
    score = 0
    if pattern matches this week's focus:     score += 3
    if pattern is trending in interview DB:   score += 2
    if tagged with requested company:         score += 2
    if java_count < 30 and easy:              score += 2  (Java ramp-up bias)
    if java_count < 30 and medium:            score += 1
    if week >= 15 and hard:                   score += 1  (Phase 2 hard bias)

  Sort by score DESC, difficulty ASC
  Return top K
```

### Trending Pattern Detection

```python
def _get_trending_patterns(company=None):
    # Query recent experience_rounds from DB
    # Parse 'topics' JSON column
    # Match against canonical pattern names via keyword map
    # Return top 3 patterns by frequency
```

This creates a **feedback loop:** real interview questions from scraping influence which drill problems are recommended.

---

## 12. Mock Score Trending

### Score Persistence

```python
save_mock_score(company, round_type, score, questions, time_mins, notes):
    hire_verdict = "hire" if score >= 3.5 else "no_hire"
    INSERT INTO mock_sessions (date_done, company, round_type, score, ...)
```

### Trend Calculation

```
1. Query mock_sessions WHERE date_done >= (today - 8 weeks)
2. Bucket by ISO week (Monday):
   week_key = date - timedelta(days=date.weekday())  # Previous Monday
3. Average scores per week bucket
4. Classify trend:
   improvement = last_week_avg - first_week_avg
   if improvement > 0.3:  "improving"
   if improvement < -0.3: "declining"
   else:                   "stable"
5. Return {weeks: {date: avg}, trend, improvement, latest_avg, first_avg}
```

### Company Readiness

```
For each round_type in COMPANY_ROUND_MAP[company]:
    trend = get_score_trend(company, round_type, weeks=4)
    readiness_pct = min(latest_avg / 5 * 100, 100)

Overall = average of non-zero round percentages
```

---

## 13. React Frontend Architecture

### Component Hierarchy

```
App (sidebar nav + Routes)
├── Dashboard
│   ├── ReadinessGauge (RadialBarChart)
│   ├── LCProgressChart (PieChart)
│   ├── GapRadar (RadarChart)
│   ├── StreakHeatmap (custom SVG)
│   ├── MockTrendChart (LineChart)
│   ├── WeeklyComparison (BarChart)
│   ├── TodayPlan
│   ├── QuickActions
│   ├── ActivityFeed
│   └── DrillStatsCard
├── Today (session launcher + PomodoroTimer)
├── Drills (drill cards + company bank)
├── MockInterview (round selector + timer + scoring)
├── LLDPractice (problem browser + AI evaluation)
├── Behavioral (LP gaps + STAR builder)
├── JavaQA (topic list + questions)
├── LeetCode (logger + heatmap + pattern chart)
├── Applications (kanban board)
├── SpacedRepetition (review queue)
├── Curriculum (progress charts + item checklist)
├── Coach (streaming chat)
├── Intelligence (stats + trending + experiences + company intel)
├── BugJournal (categorized mistake log)
├── Retros (weekly retro + failure log)
└── Settings (system status + KB + data management)
```

### State Management Pattern

```
TanStack Query (server state)
├── useProgress()     → GET /api/progress      (stale: 30s)
├── useGaps()         → GET /api/gaps           (stale: 60s)
├── useDailyPlan()    → GET /api/plan/daily     (stale: 120s)
├── useTodayLog()     → GET /api/log/today      (stale: 15s)
├── useDrillStats()   → GET /api/drill/stats    (stale: 60s)
├── useMockTrend()    → GET /api/mock/trend     (stale: 60s)
└── useCurriculum()   → GET /api/curriculum     (stale: 300s)

Mutations → invalidate related queries:
├── useSaveProgress() → invalidates ['progress']
└── useLogActivity()  → invalidates ['todayLog', 'planStats']
```

**No global client state library** (no Redux, Zustand, Context). Each page manages its own local state with `useState`. Server state is the single source of truth.

### Custom SVG Heatmap

The streak heatmap renders 120 days as a grid of `<rect>` elements:

```jsx
// 7 rows (days of week) × N columns (weeks)
cells.map((cell, i) => {
    const col = Math.floor(i / 7);
    const row = i % 7;
    return (
        <rect
            x={col * 14 + 2}  y={row * 14 + 2}
            width={11}         height={11}
            rx={2}
            fill={getColor(cell.intensity)}  // 0-5 → opacity ramp
        />
    );
});
```

### Pomodoro Timer (useRef Pattern)

```javascript
const intervalRef = useRef(null);

const start = useCallback(() => {
    if (intervalRef.current) return;   // Guard against double-start
    setRunning(true);
    intervalRef.current = setInterval(() => {
        setRemaining(r => {
            if (r <= 1) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
                return 0;
            }
            return r - 1;
        });
    }, 1000);
}, []);
```

**Why `useRef` for the interval?** `useRef` persists across renders without causing re-renders. Storing the interval ID in state would create a render loop; storing it in a closure variable would lose it on re-render.

---

## 14. Multi-Stage Docker Build

```dockerfile
# Stage 1: Build React UI (Node 22)
FROM node:22-slim AS ui-build
WORKDIR /workspace
COPY ui/ ./ui/
RUN cd ui && npm ci && npm run build
# Output: /workspace/portal/ (index.html + assets/)

# Stage 2: Python application
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ intel/ prep.py data/*.json docs/ Interview_Answers/ ./
COPY --from=ui-build /workspace/portal/ ./portal/
RUN useradd -m -u 1001 prepforge && chown -R prepforge:prepforge /app
USER prepforge
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Why multi-stage?**
- Final image has **no Node.js** — just Python + built static assets
- `node_modules` (200MB+) never enters the production image
- Docker layer caching: `npm ci` layer is cached until `package.json` changes

### SPA Serving

FastAPI serves the built React app with a **catch-all route**:

```python
# Serve Vite build assets
if (PORTAL_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory="portal/assets"))

# SPA catch-all: serve index.html for all non-API routes
@app.get("/{path:path}")
async def serve_portal(path: str = ""):
    if path.startswith("api/"):
        raise HTTPException(404)      # Let API 404s pass through
    return HTMLResponse(PORTAL_DIR / "index.html")
```

This enables React Router's client-side routing: `/drills`, `/coach`, etc. all serve the same `index.html`, and React Router handles the path.

---

## 15. Trade-Offs and Design Decisions

| Decision | Chosen | Alternative | Rationale |
|----------|--------|-------------|-----------|
| Database | SQLite (WAL) | PostgreSQL | Zero config, ships with Python, single-user |
| RAG | Keyword scoring | Vector embeddings (Qdrant) | No embedding API cost, explainable, sufficient for ~2K chunks |
| LLM client | Raw `urllib` | `anthropic` SDK | Fewer deps, smaller Docker image, transparent behavior |
| Task queue | APScheduler (in-process) | Celery + Redis | No broker needed for 4 cron jobs |
| Rate limiting | In-memory sliding window | Redis sorted sets | Single process, no external dependency |
| Frontend | React 19 + Vite | Vanilla JS (original) | 16 pages with charts, streaming, timers outgrew single file |
| State mgmt | TanStack Query only | Redux / Zustand | Server state is source of truth; no complex client state |
| Auth | None | JWT / sessions | Single-user personal tool |
| Config | JSON file + env vars | Database config table | Simple, human-readable, git-trackable |
| Notifications | ntfy.sh HTTP POST | APNs / FCM | Free, no app registration, works on any device |

---

## 16. Interview Talking Points

These are real system design concepts demonstrated in PrepForge that you can reference in interviews:

### 1. "Tell me about a system you designed with multiple data sources"
- **PrepForge scraping pipeline:** Three sources (Reddit OAuth2, LeetCode GraphQL, HN Algolia), each with different auth patterns, rate limits, and data shapes. Unified into a common `experience` schema with `INSERT OR IGNORE` dedup.

### 2. "How would you implement RAG?"
- **Keyword-based RAG with three-tier scoring:** Chunking with overlap, domain-aware keyword extraction (bigram + boost), heading/keyword/content scoring hierarchy. Trade-off vs. vector embeddings explained.

### 3. "How do you handle concurrent reads and writes?"
- **SQLite WAL mode:** Write-ahead logging allows readers to see a consistent snapshot while a writer modifies the database. Used for scraper writes concurrent with API reads.

### 4. "Design a rate limiter"
- **Sliding window algorithm:** Per-IP timestamp list, evict expired entries on each check. Path-based limits (stricter for AI endpoints). Trade-off: in-memory (no Redis) is fine for single-process.

### 5. "How do you handle streaming responses?"
- **SSE over POST:** Claude API streams `content_block_delta` events; FastAPI generator yields SSE frames; browser uses `ReadableStream` with manual line parsing (can't use `EventSource` for POST).

### 6. "Tell me about caching strategies"
- **LLM plan caching:** `UNIQUE(date, period)` in SQLite; daily/weekly plans cached until manually refreshed. TanStack Query on frontend with per-endpoint `staleTime` tuning.

### 7. "How would you build an adaptive recommendation engine?"
- **Drill selection algorithm:** Multi-signal scoring (warplan alignment + trending patterns from real interviews + company tags + difficulty bias based on current progress). Creates a feedback loop between scraped data and recommendations.

### 8. "Explain your Docker deployment strategy"
- **Multi-stage build:** Node stage builds React assets; Python stage runs the server. Final image has no Node.js. Layer caching optimizes rebuild times.

### 9. "How do you handle background jobs?"
- **APScheduler with BackgroundScheduler:** In-process daemon thread, cron triggers with timezone. Four jobs: scrape, LC sync, morning brief, weekly trends. Trade-off vs. Celery: no broker for 4 jobs.

### 10. "What patterns do you use for API design?"
- **Layered architecture:** Routers (transport) → Intel modules (domain) → DB/JSON (persistence). Strategy pattern for scrapers. Repository pattern for data access. SPA catch-all for client-side routing.
