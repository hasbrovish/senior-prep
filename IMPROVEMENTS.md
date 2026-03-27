# PrepForge — Improvements & Recent Enhancements

**Last Updated:** Mar 27, 2026 · Session: KB Automation Engine + Portal Foundation

---

## 🚀 Major Improvements This Session

### 1. **Knowledge Base (KB) Automation Engine**
**Status:** ✅ Deployed to Railway

Self-enriching interview prep knowledge base powered by Claude LLM. System ingests your activity, weak areas, job descriptions, and trending topics → generates targeted interview Q&A automatically.

#### Components:
- **2,061 KB chunks** indexed from 76 sources across 6 categories:
  - System Design (405 chunks)
  - General (384 chunks)
  - Java/Spring/Concurrency (512 chunks)
  - LLD (223 chunks)
  - DSA (389 chunks)
  - Behavioral (148 chunks)

- **7 LLM-powered Automation Flows:**
  1. `kb_enrich_from_logs()` - Analyzes activity logs → generates Q&A for weak areas
  2. `kb_generate_from_jd()` - Predicts interview questions from job descriptions
  3. `kb_learn_from_mock()` - Improves answers based on mock round performance
  4. `kb_fill_gaps()` - Identifies coverage gaps → generates missing content
  5. `kb_refresh_trending()` - Generates Q&A from trending interview topics
  6. `kb_digest_notes()` - Converts raw study notes to structured Q&A
  7. `kb_generate_topic()` - On-demand Q&A generation for specific topics

#### Usage:
```bash
# CLI (prep.py)
prep kb status                    # View KB health, file counts, recommendations
prep kb enrich                    # Generate Q&A from last 24h activity logs
prep kb jd "job description.txt"  # Predict interview questions from JD
prep kb fill                      # Auto-fill gaps in coverage
prep kb trending                  # Generate trending topic Q&A
prep kb digest "my notes.md"      # Convert notes to interview format

# API (FastAPI)
POST /api/coach/kb/enrich         # Background enrichment
POST /api/coach/kb/generate       # Generate Q&A for specific topic
POST /api/coach/kb/jd             # JD-targeted generation
POST /api/coach/kb/fill           # Gap-filling (background task)
POST /api/coach/kb/trending       # Trending topics (background)
POST /api/coach/kb/digest         # Note digestion (background)
POST /api/coach/kb/reindex        # Force KB re-index (background)
```

#### 3-Tier Search Scoring:
- Heading match: +10 points
- Keyword match (domain-boosted): +3 points
- Content match: +1 point
- Bigram bonus: +6 points

**Example:** Query "kafka dlq" → scores 21 on exact match vs 24 on content match = improved relevance

#### Files Generated:
- `intel/knowledge_base.py` (648 lines) - KB indexing, search, dynamic discovery
- `intel/kb_automation.py` (638 lines) - 7 automation flows + status checker
- API endpoints in `app/routers/coach.py` - 6 new KB endpoints

---

### 2. **Interview_Answers Directory Added to Git**
**Status:** ✅ Committed & Deployed

35 markdown + HTML files (2MB total) now tracked in git:
- Amazon_LP_STAR_Bank.md (22 GSTN STAR stories)
- SystemDesign_Interview_Cheatsheet.md (45-min interview map)
- GSTN_Complete_SDE2_SDE3_InterviewPrep.md (full system design)
- 20 sections covering Java, Spring, Kafka, Redis, System Design, LLD, etc.

**Why:** Ensures KB content is available on Railway portal deployment. Previously local-only, inaccessible to deployed container.

---

### 3. **Dockerfile Optimization**
**Status:** ✅ Working

**Fixes applied:**
- Removed hardcoded missing file copies (01_Career_Interview_Prep)
- Added selective COPY for Interview_Answers (*.md + *.html)
- Proper .dockerignore configuration (binary files excluded)
- Non-root user (prepforge, UID 1001) for security
- Python 3.11-slim base (450MB image)

**Build process:**
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ intel/ portal/ prep.py .
COPY data/*.json ./data/
COPY docs/ ./docs/
COPY Interview_Answers/*.{md,html} ./Interview_Answers/
```

---

## 🏗️ System Architecture

### Full Stack Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  prep.py (CLI)                  portal/index.html               │
│  100+ commands                  Single-file web UI              │
│  Local execution                Browser (Railway URL)           │
└───────────────┬─────────────────────────────────────┬───────────┘
                │ HTTP / local file                   │
                │                                     │
┌───────────────▼──────────────────────────────────────▼───────────┐
│                     FastAPI Server (app/)                         │
├─────────────────────────────────────────────────────────────────┤
│ main.py                                                          │
│  ├─ RateLimitMiddleware (20/min on /coach, 120/min others)       │
│  ├─ CORS (http://localhost:*, Railway URL)                       │
│  ├─ Background Scheduler (APScheduler)                           │
│  └─ 36 REST Endpoints:                                           │
│      /api/progress      → progress.json CRUD                    │
│      /api/intel/*       → company intel, trending, search       │
│      /api/coach/*       → Claude streaming + KB RAG + 7 flows   │
│      /api/practice/*    → drill, mock, LLD, behavioral, TC      │
│      /api/feedback/*    → activity log, daily/weekly plans      │
│      /api/career/*      → skill ladder, company analysis        │
└───────────────┬──────────────────────────────────────┬───────────┘
                │ Python imports (no HTTP)             │
                │                                     │
┌───────────────▼──────────────────────────────────────▼───────────┐
│                  Business Logic (intel/)                          │
├─────────────────────────────────────────────────────────────────┤
│ Knowledge Base System (NEW)                                      │
│  ├─ knowledge_base.py    Search (3-tier scoring)                │
│  ├─ kb_automation.py     7 LLM automation flows                 │
│  └─ 2,061 chunks indexed from 76 sources                        │
│                                                                 │
│ Other Modules                                                    │
│  ├─ db.py               SQLite schema (9 tables)                │
│  ├─ feedback_engine.py  Activity log → AI plans                 │
│  ├─ drill.py            211 DSA problems per-week               │
│  ├─ java_qa.py          123 P0 Java/Spring questions           │
│  ├─ mock_engine.py      Mock scoring + readiness %              │
│  ├─ lld_engine.py       20 LLD problems + SOLID rubrics         │
│  ├─ behavioral.py       14 Amazon LPs + gap detection           │
│  ├─ scraper.py          Reddit, LeetCode, levels.fyi            │
│  └─ coach.py            Claude API wrapper                      │
└───────────────┬──────────────────────────────────────┬───────────┘
                │ sqlite3 (WAL mode)                   │
                │                                     │
┌───────────────▼──────────────────────────────────────▼───────────┐
│                  Persistence Layer                               │
├─────────────────────────────────────────────────────────────────┤
│ data/interviews.db     9 SQLite tables                           │
│  ├─ experiences        Raw interview posts                      │
│  ├─ activity_log       Study activities (feedback engine)       │
│  ├─ llm_plans          Cached AI-generated plans                │
│  ├─ mock_sessions      Mock scores + trends                     │
│  ├─ jd_analyses        Job description analyses                 │
│  └─ (+ 4 more tables)                                            │
│                                                                 │
│ logs/progress.json     User progress state                       │
│  ├─ lc_sync            LeetCode stats (total, by lang)          │
│  ├─ daily_logs         Date → activity list                     │
│  ├─ topics_done        Completed curriculum topics              │
│  └─ (+ applications, offers, etc.)                              │
│                                                                 │
│ Interview_Answers/     35 knowledge files (2MB)                 │
│ docs/MASTER_16H_WARPLAN.md   26-week schedule                   │
└─────────────────────────────────────────────────────────────────┘

External Services (Optional)
  ├─ Claude API (coaching, KB automation)
  ├─ LeetCode GraphQL (DSA sync)
  ├─ Reddit OAuth2 (interview scraping)
  └─ Railway (production deployment)
```

---

## 📊 Logging System Analysis

### Current State
✅ **Logging backend exists:**
- `POST /api/log` - Record activity (type, title, outcome, confidence)
- `GET /api/log/recent` - Retrieve last N days of logs
- `GET /api/log/today` - Today's summary
- `activity_log` SQLite table - All activities persisted
- `feedback_engine.py` - Context builder for AI plans based on logs

### Portal Visibility Gap ⚠️
❌ **Missing:** Dashboard to *view* historical logs in web portal

**What's missing:**
1. **Activity History Tab** - Show logs by date, type, confidence
2. **Logging Stats** - Weekly summary (% DSA, % Theory, % Behavioral)
3. **Weakness Heatmap** - Visual: which areas need more work
4. **KB Enrichment Status** - Show which topics were auto-generated
5. **Plan Execution Tracker** - Check warplan adherence

### Recommended Additions

#### A. Activity History Dashboard
```javascript
// portal/index.html → new tab "Activity Log"
GET /api/log/recent?days=7
Response: {
  logs: [
    { date: "2026-03-27", type: "dsa", title: "LC #1 Two Sum",
      outcome: "solved", confidence: 4, duration: 25 },
    { date: "2026-03-27", type: "java", title: "OOP concepts",
      outcome: "reviewed", confidence: 3, duration: 30 },
    ...
  ],
  weekly_summary: {
    dsa: 240,        // minutes
    java: 90,
    behavioral: 30,
    hld: 120,
    lld: 45
  }
}
```

#### B. Logging Endpoint Enhancement (backend)
```python
# Add to feedback.py router
@router.get("/log/stats")
async def get_log_statistics(period: str = "week"):
    """Return activity stats for pie chart, heatmap"""
    # percent time by category
    # confidence distribution
    # trends (avg confidence over time)
    # kb enrichment triggers

@router.get("/log/heatmap")
async def get_activity_heatmap():
    """7x24 grid: hour-of-day × topic areas"""
    # Shows when user studies what
    # Identifies gaps
```

#### C. UI Improvements for portal/index.html
- **"Activity Log" Tab:** Date filter, type filter, confidence color-coding
- **"Insights" Tab:** Weekly breakdown, trending weak areas, enrichment status
- **"KB Status" Tab:** Show kb_status() output (2,061 chunks, file list, recommendations)
- **Logging Sidebar:** Quick log (already exists) + recent 5 logs preview

---

## 🔧 Improvements Still Needed

### Priority 1 (This Week)
| Item | Impact | Work |
|------|--------|------|
| **Activity Log UI Tab** | High | Show /api/log/recent data in portal |
| **KB Status Dashboard** | High | Display kb_status() in portal "KB" tab |
| **Warplan Progress Tracker** | High | Visual: Week #, day checklist, completion % |
| **Test KB Automation** | High | Run `prep kb enrich`, `prep kb jd` with real data |

### Priority 2 (Before Week 2)
| Item | Impact | Work |
|------|--------|------|
| **DSA Sync Integration** | Medium | Auto-pull solved problems from LeetCode |
| **Weekly Recap** | Medium | Sunday email: progress, trending weak areas |
| **Mock Session Replay** | Medium | Store + replay Q&A from mocks |
| **Behavioral Gap Heatmap** | Medium | Visual: which LPs weak, which strong |

### Priority 3 (Nice-to-Have)
| Item | Impact | Work |
|------|--------|------|
| **Mobile responsive portal** | Low | Optimize for phone |
| **Dark mode toggle** | Low | CSS theme switch |
| **Export to PDF** | Low | Progress report PDF generator |
| **Offline mode** | Low | Service worker caching |

---

## 📈 Performance & Deployment

### Railway Deployment Status
- ✅ Docker image: 450MB (python:3.11-slim)
- ✅ Build time: ~90s
- ✅ Startup time: ~5s (init_db + KB index)
- ✅ KB indexing: 2,061 chunks in <3s
- ✅ Rate limiting: 20 req/min on /coach, 120/min others
- ✅ Zero external DB (SQLite WAL)

### Local Development
```bash
# Start server with debug logs
python3 -m uvicorn app.main:app --reload --port 5555

# Test KB functions
python3 -c "from intel.kb_automation import kb_status; print(kb_status())"

# Run CLI with KB commands
prep kb status
prep kb enrich
```

---

## ✅ Git Commit History (This Session)

| Commit | Description |
|--------|-------------|
| 9758223 | Fix Dockerfile: remove COPY for untracked directories |
| 324f959 | Add Interview_Answers to git for portal deployment; restore Dockerfile COPY |
| (earlier) | Add KB automation engine: prep kb commands + API endpoints |

---

## 📝 Next Steps for User

1. **This Week (Mar 27–30):** Execute Week 1 warplan (DSA, Java theory, behavioral)
2. **Next Session:** Add Activity Log UI tab to portal (simple HTML + fetch)
3. **Week 2:** Test KB automation with real mock + JD data
4. **Week 3:** Add weekly recap email + progress dashboard

---

**Questions?** Check:
- KB automation details: `intel/kb_automation.py` docstrings
- Architecture deep-dive: `ARCHITECTURE.md`
- Warplan details: `docs/MASTER_16H_WARPLAN.md`
- Logging API: `app/routers/feedback.py` + `intel/feedback_engine.py`
