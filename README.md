# PrepForge — SDE-2/SDE-3 Interview Prep System
### Jayanti Vishnoi · 5.5 YOE at GSTN · March → September 2026

```
PHASE 1  Mar–Jun 2026  →  First offer: Razorpay / CRED / PhonePe / Juspay  (30–40 LPA)
PHASE 2  Jun–Sep 2026  →  Dream offer: Amazon / Google / Goldman / Swiggy   (45–75 LPA)
```

> **Today:** Day 6/184 · Week 1/26 · Phase 1 · Start date: Mar 24, 2026

---

## Project Overview

A **personal, full-stack interview preparation system** — not just notes. Built for one purpose: getting from GSTN → FAANG/Tier-1 India in 26 weeks. Deployed on Railway, accessible from anywhere.

| Layer | What it does |
|-------|-------------|
| **CLI** (`prep`) | Daily planner, drill engine, mock runner, AI coach, 100+ commands |
| **Intelligence Engine** (`intel/`) | Reddit OAuth2 scraper, LeetCode Discuss GraphQL, trending topic analysis, LLM feedback loop |
| **FastAPI Server** (`app/`) | REST API (36 endpoints) + web portal + background scheduler |
| **Practice Engines** | DSA drill (211 problems, 16 companies), LLD (20 problems), mock score tracker, behavioral gap detector, TC intel |
| **Master Curriculum** | Hello Interview (218 lessons) + PP (9 modules) merged into unified 26-week tracker |
| **LLM Adaptive Planning** | Daily/weekly AI plans from Claude Haiku — adapts based on logs, mock scores, intel trends |
| **War Plan** (`docs/MASTER_16H_WARPLAN.md`) | 26-week 16h/day schedule, weekly LC targets, company strategies |
| **React Dashboard** (`ui/`) | Full React 19 + Vite SPA: Dashboard visualizations, AI Coach (streaming), Drills, Mock Simulator, LLD, Behavioral, LeetCode Tracker, Applications Kanban, Spaced Repetition, Curriculum, Intelligence, Settings (16 pages) |

See [ARCHITECTURE.md](ARCHITECTURE.md) for system design deep-dive, data flow, DB schema, and interview talking points.

**Recent improvements:** [IMPROVEMENTS.md](IMPROVEMENTS.md) — KB automation engine (2,061 chunks, 7 LLM flows), Interview_Answers now in git, logging system analysis & UI roadmap.

---

## Quick Start

```bash
# 1. Setup alias (one time)
echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
source ~/.zshrc

# 2. Start your day
prep status        # full dashboard: streak, LC count, apps, week
prep brief         # morning brief (streak, intel, plan)
prep drill         # today's Java DSA problems (warplan-aligned)
prep jqa           # today's Java theory topic + P0 questions

# 3. Study
prep warplan       # open 26-week war plan
prep warplan 4     # jump to Week 4 details
prep assault       # alias for warplan
prep drill company amazon   # Amazon-specific problem bank (160 problems)
prep drill bank             # list all companies + problem counts
prep java          # today's recommended Java theory topic
prep java list     # all 16 topics + readiness %
prep lld parking-lot  # LLD practice session
prep lp-check      # behavioral gap analysis

# 4. Track
prep lc "Two Sum"            # mark LeetCode problem done (in Java!)
prep jqa done oop            # mark Java OOP topic as studied
prep log "worked on trees"   # log today's activity
prep check                   # health check + coach advice

# 5. Web portal
prep portal        # starts FastAPI at http://localhost:5555
# Or open your Railway deployment URL in any browser
```

---

## Project Structure

```
senior-prep/
│
├── prep.py                      ← Main CLI (55+ commands)
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
│
├── app/                         ← FastAPI server
│   ├── main.py                  ← App factory, CORS, rate limiting, startup
│   ├── scheduler.py             ← Background jobs (scrape, LC sync, brief)
│   └── routers/
│       ├── coach.py             ← AI coaching (stream + non-stream)
│       ├── practice.py          ← Drill, Mock, LLD, Behavioral, TC, Brief
│       ├── intel_routes.py      ← Intel search, trending, company profiles
│       ├── progress.py          ← Progress read/write, gap analysis
│       ├── career.py            ← Skill ladder, weekly plan
│       └── feedback.py          ← Activity log, adaptive daily/weekly plan
│
├── intel/                       ← Intelligence Engine
│   ├── config.py                ← Models (claude-sonnet-4-5), profile, 14 companies
│   ├── db.py                    ← SQLite schema + CRUD (9 tables)
│   ├── knowledge_base.py        ← KB indexing + search (2,061 chunks, 3-tier scoring)
│   ├── kb_automation.py         ← 7 LLM automation flows (enrich, fill, generate, etc)
│   ├── feedback_engine.py       ← Activity log → adaptive plans
│   ├── scraper.py               ← Orchestrates all sources
│   ├── coach.py                 ← Claude API (JD analyze, evaluate, STAR, mock, KB)
│   ├── analyzer.py              ← Trend analysis, gap analysis, readiness score
│   ├── drill.py                 ← Java DSA drill (warplan-aligned per-week lists)
│   ├── java_qa.py               ← 160 P0 Java/Spring/Concurrency Q&A
│   ├── pp_tracker.py            ← Programming Pathshala course tracker
│   ├── mock_engine.py           ← Mock score tracking + trend charts
│   ├── lld_engine.py            ← 20 LLD problems with SOLID rubrics
│   ├── behavioral.py            ← Amazon LP gap detector + Bar Raiser probes
│   ├── brief.py                 ← Morning brief generator + ntfy.sh push
│   ├── hello_interview.py       ← Hello Interview course lesson tracker
│   ├── resources.py             ← Curated resource index
│   └── sources/
│       ├── reddit.py            ← Reddit (r/leetcode, r/cscareerquestions)
│       ├── leetcode_discuss.py  ← LeetCode Discuss GraphQL
│       ├── enginebogie.py       ← r/IndiaTechies + HackerNews Algolia
│       ├── levelsfyi.py         ← TC intelligence (levels.fyi)
│       └── blind_helloiv.py     ← Source status + InterviewBit fetcher
│
├── ui/                          ← React 19 + Vite dashboard (source)
│   ├── src/pages/               ← 16 page components
│   ├── src/components/          ← Reusable chart/widget components
│   ├── src/hooks/               ← TanStack Query hooks, timer
│   └── vite.config.js           ← Builds to portal/ for production
│
├── portal/                      ← Built React app (served by FastAPI)
│   ├── index.html               ← Vite build output
│   └── assets/                  ← JS + CSS bundles
│
├── data/                        ← Runtime + course data (git-ignored)
│   ├── interviews.db            ← SQLite: 9 tables (WAL mode)
│   ├── portal_data.json         ← Portal state
│   ├── programming_pathshala_courses.json  ← PP catalog (138 topics)
│   └── hellointerviewcourse.json           ← Hello Interview curriculum
│
├── logs/                        ← Runtime logs (git-ignored)
│   └── progress.json            ← All tracker state (LC, SR, failures, offers)
│
├── Interview_Answers/           ← Knowledge base content (35 files, 2MB)
│   ├── Amazon_LP_STAR_Bank.md   ← 22 GSTN STAR stories (all 14 LPs)
│   ├── SystemDesign_Interview_Cheatsheet.md ← 45-min interview map
│   ├── GSTN_Complete_SDE2_SDE3_InterviewPrep.md
│   ├── Section_*.md/.html       ← 20 sections (Java, Spring, Kafka, System Design, LLD, etc)
│   └── (+ other content files)
│
├── docs/                        ← All documentation (git-tracked)
│   ├── MASTER_16H_WARPLAN.md    ← 26-week war plan (read by prep.py)
│   ├── GSTN_Interview_QuestionBank_296Q.md  ← 296-question bank (read by prep.py)
│   ├── DEPLOY.md                ← Deployment guide
│   ├── IMPROVEMENTS.md          ← Recent enhancements & architecture
│   ├── COMPANY_ANALYSIS.md
│   ├── CPP_to_Java_DSA_CheatSheet.md
│   ├── DEEP_RESEARCH_INTERVIEW_PATTERNS_2025_2026.md
│   ├── INTELLIGENCE_GUIDE.md
│   ├── MOCK_INTERVIEW_GUIDE.md
│   ├── RESOURCES.md
│   ├── RESUME_VARIANTS.md
│   ├── MASTER_6MONTH_PROGRAMME.md
│   ├── LINKEDIN_RESUME_GUIDE.md
│   ├── LinkedIn_Profile_Complete_Update.md
│   ├── LinkedIn_Saved_Posts_Part1/2/3.md
│   ├── Interview_exp.txt
│   ├── books/                   ← Reference books (git-ignored, local only)
│   │   ├── Alex_Xu_SystemDesign_Vol1.pdf
│   │   ├── Alex_Xu_SystemDesign_Vol2.pdf
│   │   └── Java_SpringBoot_Microservices_Interview_Guide.docx
│   └── library/                 ← Study library (git-ignored, personal)
│       ├── 01_Career_Interview_Prep/
│       ├── 02_Resumes/
│       └── trackers-docs/
│
└── projects/
    └── kafka-pipeline/          ← Portfolio: Spring Boot + Kafka + Redis + DLQ
```

---

## All Commands

### Daily Workflow
```bash
prep                            # today's plan (time-aware, shows current block)
prep plan                       # same as above
prep full                       # all blocks expanded
prep log                        # log what you did today
prep check                      # health check + AI coach note
prep sync                       # sync LeetCode stats (hasbrovish95)
prep score                      # one-line scoreboard
prep brief                      # today's morning brief
prep brief --send               # send to phone (requires NTFY_TOPIC env var)
```

### AI Adaptive Planning
```bash
prep aiplan                     # today's AI plan (Claude Haiku, cached)
prep weekplan                   # this week's adaptive plan
prep logx lc "Two Sum"          # log a structured activity
prep logx mock "Razorpay SD" --outcome struggled --conf 2
```

### Java DSA Drill Engine
```bash
prep drill                      # this week's exact LC problems (from warplan)
prep drill week 3               # week 3 problems
prep drill company amazon       # Amazon problem bank (160 problems)
prep drill company google       # Google bank (133 problems)
prep drill company stripe       # Stripe bank (9 problems)
prep drill bank                 # list all 16 companies + problem counts
prep drill done "Two Sum"       # mark done
prep drill done "Two Sum" --time 28 --struggled
prep drill stats                # drill streak + history
```

### Java Theory — `prep java` / `prep jqa`
```bash
prep jqa                        # today's Java topic + P0 questions
prep jqa list                   # all 16 topics with study %
prep jqa done threads           # mark topic as studied
prep java                       # today's recommended Java topic + weak areas
prep java list                  # all 16 topics with P0 question count + readiness %
prep java oop                   # show all OOP P0 questions
prep java concurrency           # critical: Java concurrency (Goldman, PhonePe, Adobe)
prep java kafka                 # Kafka internals + patterns
prep java done oop              # mark OOP as studied today
prep java reset oop             # reset (re-study next week)
prep java oop --hints           # show 1-line answer hints
```

### War Plan
```bash
prep warplan                    # open MASTER_16H_WARPLAN.md (26-week summary)
prep warplan 1                  # jump to Week 1 detail
prep warplan 19                 # Amazon full-prep week detail
prep assault                    # alias for warplan
```

### Programming Pathshala Tracker
```bash
prep pp                         # today's PP module (warplan-aligned, e.g. DSA Module 3)
prep pp list                    # full optimised watch order (all 26 weeks)
prep pp progress                # completion % with progress bar
prep pp week 6                  # Week 6: Graphs (DSA Module 5) — shows topics from JSON
prep pp done "DSA Module 3"     # mark module phase as watched
```

### Mock Round Simulator
```bash
prep mock-round google dsa      # AI mock DSA round, saves score to DB
prep mock-round amazon behavioral
prep mock-round flipkart system_design
prep mock-trend                 # score trend chart — all companies
prep mock-trend google          # Google-specific trend
prep mock-trend amazon dsa      # filter by company + round type
```

### LLD Practice Engine (20 problems)
```bash
prep lld                        # list all 20 LLD problems
prep lld list google            # filter by company
prep lld parking-lot            # 45-min timed session with SOLID scoring
prep lld lru-cache              # LRU Cache (must-do)
prep lld notification-system    # Notification System (your GSTN advantage)
prep lld elevator               # Elevator System
prep lld chess                  # Chess Game
prep lld splitwise              # Expense Sharing (Phase 2)
prep lld scores                 # LLD history + scores
```

### Behavioral Gap Detector
```bash
prep lp-check                   # Amazon LP gap analysis
                                # Shows: coverage %, thin LPs, Bar Raiser probing questions
```

### TC Intelligence
```bash
prep tc                         # TC overview for all 11 target companies
prep tc google                  # Google TC (L4/L5) + negotiation playbook
prep tc amazon                  # Amazon TC structure (RSU cliff, signing bonus)
prep tc goldman                 # Goldman deferred comp structure
```

### Knowledge Base Automation (requires ANTHROPIC_API_KEY)
```bash
prep kb status                  # View KB health (2,061 chunks, 6 categories, file list)
prep kb enrich                  # Analyze last 24h activity → generate Q&A for weak areas
prep kb jd <jd.txt>            # Predict interview questions from job description
prep kb fill                    # Identify coverage gaps → auto-generate missing content
prep kb generate <topic>        # On-demand Q&A generation for specific topic
prep kb digest <notes.md>       # Convert raw notes to interview Q&A format
prep kb trending                # Generate Q&A for trending interview topics
prep kb reindex                 # Force re-index all KB files (2,061 chunks)
```

### AI Coaching (requires ANTHROPIC_API_KEY)
```bash
prep ask "question"             # ask Claude anything (reads your actual data)
prep ai-review                  # intelligent weekly review with real numbers
prep ai-check                   # smart daily health check
prep jd-analyze                 # paste a JD → gap analysis + study plan
prep evaluate                   # paste your answer → hire/no-hire rubric
prep story                      # generate STAR story from raw experience
prep readiness                  # multi-dimensional readiness score
prep readiness sde3             # SDE-3 bar assessment
prep ai-mock sd                 # AI system design question
prep ai-mock dsa google hard    # Google-style hard DSA question
```

### Intelligence Engine
```bash
prep scrape                     # scrape all sources (Reddit OAuth2, LeetCode Discuss)
prep scrape reddit              # scrape specific source
prep scrape lc                  # just LeetCode Discuss
prep trending                   # what's being asked across all companies
prep trending google 30         # Google-specific last 30 days
prep experiences                # browse scraped interview experiences
prep experiences amazon sde2    # filter by company + role
prep company google             # full company intelligence profile
prep add-experience             # manually add an experience (Blind/enginebogie paste)
prep intel-status               # DB dashboard (total experiences, sources)
prep resources                  # curated resource index
prep resources dsa              # DSA resources only
prep sources                    # external source status (Blind, HI, IB, levels.fyi)
prep ib                         # InterviewBit problem list for target topics
```

### Built-in Mock Interviews (no API key needed)
```bash
prep mock java                  # Java deep dive (45 min)
prep mock dsa                   # DSA / problem solving (45 min)
prep mock sd                    # System Design (45 min)
prep mock lld                   # Low-Level Design (45 min)
prep mock behavioral            # Behavioral / STAR (30 min)
prep mock full                  # Full loop (90 min)
```

### LeetCode & DSA
```bash
prep lc "Two Sum"               # mark done (prompts: time, pattern, struggled)
prep lc "Two Sum" --time 28 --pattern two-pointers
prep heatmap                    # colored pattern strength heatmap
prep java                       # Java language gap tracker (4/30 critical!)
```

### Spaced Repetition
```bash
prep sr                         # review queue (due today + upcoming)
prep sr-init                    # seed queue with confidence ratings
prep study kafka 4              # mark topic studied (1–5 confidence)
prep teach system-design        # Feynman protocol
prep quiz java-core             # random quiz question
```

### Progress & Reviews
```bash
prep status                     # full progress dashboard
prep review                     # weekly feedback + next steps
prep retro                      # weekly retrospective
prep week-summary               # export week snapshot to logs/week_N.txt
```

### Interview Tracking
```bash
prep interview-log "Amazon"     # structured post-round logging
prep interviews                 # history + pattern analysis
prep bug "blanked on DP"        # log a stumbling block
prep bugs                       # weak area analysis
prep recover                    # failed round recovery protocol
prep failures                   # failure pattern analysis
```

### Applications
```bash
prep apply "Razorpay"           # log job application (opens Week 4)
prep offer "Razorpay" 32LPA     # log offer received
```

### Timers & Focus
```bash
prep focus 45                   # Pomodoro timer (45 min)
prep focus                      # default 25 min
```

### Web Portal
```bash
# Option 1: Production build (one command)
prep portal                     # starts FastAPI at http://localhost:5555 (serves built React app)
prep portal 8080                # custom port

# Option 2: Development (hot reload)
uvicorn app.main:app --reload --port 5555   # Terminal 1: API server
cd ui && npm run dev                         # Terminal 2: Vite dev server at :5173

# Build React UI for production
cd ui && npm run build                       # outputs to portal/

# API docs:  http://localhost:5555/docs  (dev mode only)
```

---

## Environment Setup

```bash
cp .env.example .env

# Required for AI features
export ANTHROPIC_API_KEY=sk-ant-...

# Optional — phone push notifications
export NTFY_TOPIC=prep

# Optional — 2x Reddit scraping rate
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...

# Override AI models (defaults already set)
# export CLAUDE_MODEL=claude-sonnet-4-5
# export CLAUDE_MODEL_FAST=claude-haiku-4-5
```

### ntfy.sh Setup (Free Phone Notifications)
```bash
# 1. Install ntfy app on phone
# 2. Subscribe to your topic
export NTFY_TOPIC=prep
prep brief --send
```

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/drill/today` | GET | Today's Java DSA drill (warplan-aligned) |
| `/api/drill/done` | POST | Mark drill problem done |
| `/api/drill/stats` | GET | Drill streak + history |
| `/api/drill/companies` | GET | All companies + problem counts |
| `/api/drill/company/{company}` | GET | Problems for a specific company |
| `/api/jqa` | GET | Today's Java theory topic + P0 questions |
| `/api/jqa/list` | GET | All 16 topics with study % |
| `/api/jqa/topic/{id}` | GET | Questions for a specific topic |
| `/api/jqa/done/{id}` | POST | Mark topic as studied |
| `/api/warplan` | GET | War plan content (`?week=N` for a specific week) |
| `/api/mock/trend` | GET | Score trend over time |
| `/api/mock/score` | POST | Save mock session score |
| `/api/mock/readiness/{company}` | GET | Readiness % per round type |
| `/api/lld/problems` | GET | List LLD problems |
| `/api/lld/problem/{key}` | GET | Problem details |
| `/api/lld/score` | POST | Save LLD session score |
| `/api/lld/evaluate` | POST | AI-evaluate your design |
| `/api/behavioral/check` | GET | Amazon LP gap analysis |
| `/api/behavioral/probes/{lp}` | GET | Probing questions for an LP |
| `/api/tc/{company}` | GET | TC intelligence |
| `/api/brief` | GET | Morning brief (`?send=true` for push) |
| `/api/coach` | POST | AI coaching (non-stream, 30 req/min) |
| `/api/coach/stream` | POST | AI coaching (SSE stream) |
| `/api/intel/stats` | GET | DB dashboard |
| `/api/intel/experiences` | GET | Search experiences (`?company=&role=`) |
| `/api/intel/trending` | GET | Trending topics (`?company=&days=30`) |
| `/api/intel/company/{name}` | GET | Company intelligence profile |
| `/api/intel/scrape` | POST | Trigger scrape in background |
| `/api/intel/import` | POST | Manual import (Blind/enginebogie paste) |
| `/api/intel/import/guide` | GET | Setup guide for each source |
| `/api/intel/resources` | GET | Curated resources (`?cat=dsa`) |
| `/api/curriculum` | GET | Merged master curriculum (HI + PP, ~317 items) |
| `/api/log` | POST | Log an activity (feeds LLM planner) |
| `/api/log/recent` | GET | Last N days of logs (`?days=7`) |
| `/api/log/today` | GET | Today's activity summary |
| `/api/plan/daily` | GET | Today's AI adaptive plan (cached) |
| `/api/plan/daily/refresh` | POST | Force-regenerate daily plan |
| `/api/plan/weekly` | GET | This week's AI plan (cached) |
| `/api/plan/weekly/refresh` | POST | Force-regenerate weekly plan |
| `/api/plan/stats` | GET | Progress analytics (velocity, weak areas) |
| `/api/progress` | GET/POST | Progress data |
| `/api/gaps` | GET | Gap analysis |
| `/api/career/ladder` | GET | SDE-2→SDE-3 skill map |
| `/api/log` | POST | Log a study activity |
| `/api/log/recent` | GET | Last N days of logs |
| `/api/log/today` | GET | Today's activity summary |
| `/api/plan/daily` | GET | Today's adaptive plan (cached) |
| `/api/plan/weekly` | GET | This week's adaptive plan |
| `/api/plan/stats` | GET | Velocity + weak areas analysis |
| `/api/curriculum` | GET | Merged HI + PP curriculum by week |
| `/health` | GET | Health check |

---

## What's Done ✅

| Feature | Status | Command / Where |
|---|---|---|
| 26-week daily prep plan | ✅ | `prep` / `prep plan` |
| 26-week war plan (16h/day) | ✅ | `prep warplan` / `prep assault` |
| LeetCode sync (auto + manual) | ✅ | `prep sync`, `prep lc` |
| Pattern heatmap | ✅ | `prep heatmap` |
| Java language tracker | ✅ | `prep java` |
| Java Q&A bank (123 P0 questions, 16 topics) | ✅ | `prep jqa` / portal War Plan |
| Programming Pathshala tracker | ✅ | `prep pp` |
| Spaced repetition (15 topics) | ✅ | `prep sr` |
| Bug journal + failure analysis | ✅ | `prep bug`, `prep recover` |
| Application + offer tracking | ✅ | `prep apply`, `prep offer` |
| Interview round logging | ✅ | `prep interview-log` |
| 296-question verbal practice bank | ✅ | `prep question` |
| Built-in mock interviews (6 types) | ✅ | `prep mock` |
| Health check + coach notes | ✅ | `prep check` |
| Weekly retro + summary export | ✅ | `prep retro` |
| FastAPI web server | ✅ | `prep portal` |
| **Deployed on Railway** | ✅ | push to main → auto-deploy |
| **Master Curriculum (HI + PP merged)** | ✅ | portal Courses tab — 317 items, category/source/week filters |
| **LLM Adaptive Planning** | ✅ | `prep aiplan` / portal Dashboard — daily+weekly, Claude Haiku |
| **Structured Activity Logging** | ✅ | `prep logx` / portal Dashboard log row |
| Intel scraping (Reddit OAuth2, LC Discuss) | ✅ | `prep scrape` / portal Intel |
| **Manual import (Blind/enginebogie paste)** | ✅ | portal Intel → form / `POST /api/intel/import` |
| **Trending topics (7/14/30/90d, by company)** | ✅ | portal Intel → Trends |
| **Hot Questions panel (30 real questions)** | ✅ | portal Intel tab |
| RAG-based AI coach | ✅ | `prep ask` / portal AI Coach |
| JD gap analysis | ✅ | `prep jd-analyze` |
| Answer evaluation (hire rubric) | ✅ | `prep evaluate` |
| STAR story generator | ✅ | `prep story` |
| Company intelligence profiles | ✅ | `prep company` |
| Readiness assessment | ✅ | `prep readiness` |
| Background scheduler | ✅ | auto with portal |
| Docker + docker-compose | ✅ | `docker-compose up` |
| **Java DSA Drill Bank (211 problems, 16 companies)** | ✅ | `prep drill company amazon` |
| Mock score tracker (trend charts) | ✅ | `prep mock-round` |
| LLD Practice Engine (20 problems) | ✅ | `prep lld` |
| Behavioral gap detector (Amazon LPs) | ✅ | `prep lp-check` |
| TC intelligence (11 companies) | ✅ | `prep tc` |
| Morning brief + push notifications | ✅ | `prep brief` |
| Source status dashboard | ✅ | `prep sources` |
| InterviewBit fetcher | ✅ | `prep ib` |
| **War Plan portal tab** | ✅ | portal → War Plan (W1–W26 selector) |
| DB schema (SQLite, WAL mode) | ✅ | auto on startup |

---

## What's Pending 🔲

### P0 — Do this week (Week 1)
| Task | Why | How |
|---|---|---|
| Switch LeetCode to Java | Critical gap: only 4/155 in Java | LeetCode → Code → change language |
| `prep drill` every morning | Fixes Java gap in 6 weeks | 30 min morning block — 12 problems target |
| `prep jqa done oop` after studying | Tracks Java theory progress | `prep jqa list` to see all 16 topics |
| Complete missing LP stories | 4 critical LPs have 0 stories | `prep lp-check` → write stories |
| Add Reddit API keys to Railway | Enables auto-scraping on cloud | reddit.com/prefs/apps → Railway env vars |

### P1 — This month
| Task | Why | How |
|---|---|---|
| Set up ntfy.sh phone push | Automatic daily brief on phone | `export NTFY_TOPIC=prep` |
| Import Blind posts manually | High-quality India-specific intel | Portal Intel tab → Manual Import form |
| Add LP stories for 4 critical gaps | Amazon LP asked every round | Dive Deep, Bias for Action, Earn Trust, Have Backbone |
| `prep lld parking-lot` weekly | LLD at Adobe, Flipkart, CRED | Every Saturday |

### P2 — Phase 2 (after first offer)
| Feature | Effort |
|---|---|
| Vector search (Qdrant semantic RAG) | 1 day |
| Live TC scraper (levels.fyi) | Working, may hit rate limits |
| Test suite | Not critical for personal tool |

---

## Database Schema

```
interviews.db (SQLite, WAL mode)
│
├── experiences         ← scraped interview posts (source, company, role, outcome)
├── experience_rounds   ← individual rounds per experience
├── company_intel       ← aggregated company profiles
├── trending_topics     ← trending DSA/SD/LLD topics by company + date
├── jd_analyses         ← saved JD gap analyses
├── resource_log        ← curated learning resources
├── drill_sessions      ← Java DSA drill completions (streak tracking)
├── mock_sessions       ← mock round scores over time (trend charts)
└── lld_sessions        ← LLD practice scores per problem
```

---

## Your Data — Current State

```
LeetCode:  155 solved  (Easy: 62, Medium: 77, Hard: 16)
Java:      4 problems  ← CRITICAL: must reach 30 by Week 6 end
Week 1 target: 12 Java problems by Mar 30 (run: prep drill daily)

PP Course: 0/13 phases watched  (run: prep pp list)
Java Q&A:  0/15 topics studied  (run: prep java list)

Streak:    2 days
Week:      1/26  (Phase 1)
Day:       6/184

Amazon LP coverage:   57%  (4 critical LPs with 0 stories)
Missing:   Dive Deep, Bias for Action, Earn Trust, Have Backbone

Interview experiences in DB: run 'prep intel-status'
Applications:  0 (opens Week 4 — Apr 14)
```

---

## Your Competitive Advantages

Use these in every round — real, verifiable, production-scale:

```
Scale:        14M taxpayers  ·  3B invoices/year  ·  500 GST filings/sec peak
Caching:      JBoss DataGrid + EhCache  ·  70+ regions  ·  40% DB load reduction
Kafka:        Consumer framework with DLQ  ·  exactly-once semantics  ·  2M+ events/day
Transactions: XA distributed (Atomikos)  ·  cross-service ledger consistency
Patterns:     Strategy (CaseCustomizerFactory)  ·  Template Method (Consumer)  ·  Factory
LLD example:  Notification System (CommunicationService)  ←  strongest LLD answer
SD example:   GST Return Filing System  ←  can speak to every design decision
Java wins:    60% order processing ↓ (45m→18m)  ·  99.9% ledger accuracy  ·  0 misappropriations
```

---

## Week-by-Week Plan (MASTER_16H_WARPLAN.md)

```
WEEK 1  (Mar 24)  Arrays, Two Pointers, Sliding Window  |  PP: DSA Module 3
WEEK 2  (Mar 31)  Linked Lists, Recursion               |  PP: DSA Module 3
WEEK 3  (Apr 7)   Stacks, Queues                        |  PP: DSA Module 4
WEEK 4  (Apr 14)  Binary Trees                          |  PP: DSA Module 4  ← Apply opens
WEEK 5  (Apr 21)  BST, Heap — Machine Coding starts     |  PP: DSA Module 5
WEEK 6  (Apr 28)  Graphs, Kafka                         |  PP: DSA Module 5
WEEK 7  (May 5)   Backtracking, Concurrency basics      |  PP: DSA Module 6
WEEK 8  (May 12)  Dynamic Programming Part 1            |  PP: DSA Module 6
WEEK 9  (May 19)  Dynamic Programming Part 2            |  PP: DSA Module 6
WEEK 10 (May 26)  Tries, Advanced Trees                 |  PP: DSA Module 6
WEEK 11 (Jun 2)   Greedy, Bit Manipulation              |  PP: LLD Module 7
WEEK 12 (Jun 9)   MOCK WEEK — Phase 1 Simulation        |  PP: LLD Module 7
WEEK 13 (Jun 16)  Polish Week — fix weak areas          |  PP: LLD Module 8
──── PHASE 2 ─────────────────────────────────────────────────────────────────────
WEEK 14-16        Hard DSA + Goldman Concurrency         |  PP: LLD Module 8 Concurrency
WEEK 17-18        String Algorithms + Swiggy             |  PP: Java Springboot Module 11
WEEK 19           Amazon Full Prep Week                  |  PP: System Design Module 9
WEEK 20           Google Full Prep Week                  |  PP: System Design Module 9
WEEK 21-22        MOCK WEEK 2 + Goldman Finance          |  PP: Java Springboot Module 11
WEEK 23-24        Hard Problem Mastery + HLD Patterns    |  PP: LLD Module 8 Case Studies
WEEK 25           Final Polish                           |  PP: Review
WEEK 26           EXECUTION WEEK — Trust your prep       |  PP: Review
```

For full weekly details: `prep warplan` or `prep warplan <week_number>`

---

## Deployment

**Option A — Local Development (recommended for day-to-day use):**
```bash
# 1. Install Python deps
pip install -r requirements.txt

# 2. Install UI deps + build
cd ui && npm install && npm run build && cd ..

# 3. Start server (serves built React app at /)
prep portal
# Open http://localhost:5555

# For hot-reload UI development (two terminals):
uvicorn app.main:app --reload --port 5555    # Terminal 1
cd ui && npm run dev                          # Terminal 2 → http://localhost:5173
```

**Option B — Docker (multi-stage build, includes UI):**
```bash
docker-compose up
# Builds React UI in Node stage, then Python app → http://localhost:5555
```

**Option C — Railway.app (deployed, recommended for cloud):**
```bash
# Push to main → auto-redeploys in ~3 min (multi-stage Dockerfile builds UI automatically)
git push origin main

# Required Railway env vars:
# ANTHROPIC_API_KEY    — AI Coach (required)
# REDDIT_CLIENT_ID     — Reddit OAuth2 scraping (optional)
# REDDIT_CLIENT_SECRET — Reddit OAuth2 scraping (optional)
# NTFY_TOPIC           — phone push notifications via ntfy.sh (optional, e.g. prep)
# NTFY_TOKEN           — only needed for private ntfy.sh topics (optional)
```

### Reddit Setup (for cloud scraping)
1. Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps) — **check the reCAPTCHA box**
2. Create "script" app → copy Client ID + Secret
3. Add to Railway Variables → auto-redeploys
4. Portal Intel → "Scrape Sources" now fetches from 6 subreddits via OAuth2

Without keys, public `.json` API is used (works locally, blocked on cloud IPs).

---


*Stack: Java · Spring Boot · Kafka · Redis · MySQL · MongoDB · Golang · Docker · K8s · AWS*

---

## Architecture Deep Dive

> Read this to understand how the system works and learn from the design decisions.

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PREPFORGE SYSTEM                                   │
│                                                                             │
│  YOU (CLI)                  SERVER                      EXTERNAL            │
│  ──────────                 ──────────                  ────────            │
│                                                                             │
│  prep.py ──────────────▶  FastAPI (port 5555)           Anthropic API      │
│  (4000+ lines)             ├── app/main.py               (Claude Sonnet)   │
│   ├── 55+ commands         ├── app/scheduler.py  ──▶    Reddit API         │
│   ├── WEEKS dict           └── app/routers/             LeetCode GraphQL   │
│   └── dispatch fn              ├── practice.py          ntfy.sh (push)     │
│                                ├── coach.py    ──────▶  Anthropic API      │
│  Browser (React 19)            ├── intel_routes.py                         │
│  ──────────                    ├── progress.py                             │
│  ui/ → portal/index.html ──▶   ├── career.py                               │
│  (Vite + React SPA)           └── feedback.py                             │
│   ├── 16 pages, 13 components                                              │
│   ├── TanStack Query + Router  intel/ (Engine)                              │
│   ├── Recharts visualizations  ├── config.py   ← profile, models, 14 companies │
│                            ├── db.py       ← SQLite (9 tables, WAL)         │
│  Railway.app               ├── scraper.py  ← orchestrates all sources      │
│  ──────────                ├── analyzer.py ← trends, gap analysis          │
│  git push → deploy         ├── coach.py    ← Claude calls (RAG-enhanced)   │
│  Docker container          ├── drill.py    ← 211 LC problems, week mapping │
│  Persistent volume         ├── java_qa.py  ← 160 P0 Q&A, 16 topics        │
│                            ├── mock_engine.py ← scores, trend charts       │
│                            ├── lld_engine.py ← 20 problems, SOLID rubric   │
│                            ├── behavioral.py ← Amazon LP gap detector      │
│                            ├── brief.py    ← ntfy.sh push notifications    │
│                            ├── pp_tracker.py ← PP course watch order       │
│                            ├── hello_interview.py ← HI lesson tracker      │
│                            ├── resources.py ← curated resource index       │
│                            └── sources/    ← 5 scrapers                    │
│                                                                             │
│  DATA STORES                                                                │
│  ───────────                                                                │
│  data/interviews.db     ← SQLite (scraped intel, drill, mock, LLD scores)  │
│  logs/progress.json     ← all personal tracker state (LC, SR, offers...)   │
│  data/portal_data.json  ← portal state (resources, notes, settings)        │
│  data/hellointerviewcourse.json  ← HI curriculum (committed to git)        │
│  data/programming_pathshala_courses.json ← PP catalog (committed to git)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### How Data Flows — End to End

#### 1. Morning Brief (ntfy.sh)
```
app/scheduler.py (8 AM IST cron)
  └─▶ intel/brief.py::send_morning_brief()
        ├─ reads logs/progress.json  → streak, LC count, Java count
        ├─ reads prep.py::WEEKS      → today's theme, DSA topic
        ├─ intel/drill.py::get_drill → top 3 Java problems for today
        ├─ intel/db.py               → trending company from yesterday
        ├─ intel/behavioral.py       → weakest LP story reminder
        └─▶ POST https://ntfy.sh/prep
              Title: "PrepForge Brief - Wed D7/184 W1/26"  (ASCII header)
              Body:  streak + drill problems + intel + behavioral
```

#### 2. CLI drill command (`prep drill`)
```
prep.py::cmd_drill()
  └─▶ intel/drill.py::print_drill(week_num, java_count)
        ├─ Calculates current week from start date (Mar 19, 2026)
        ├─ Looks up WEEK_PROBLEMS[week_num] → explicit LC problem IDs
        ├─ Fetches problem details from NEETCODE_150 list
        ├─ _enrich_companies() → adds trending company problems from DB
        └─ Prints colour-coded table with Java tips + LeetCode URLs
```

#### 3. AI Coach request (portal or CLI)
```
Browser::fetch POST /api/coach
  └─▶ app/routers/coach.py::coach_chat()
        ├─ _get_rag_context(query, company)
        │    └─ intel/db.py::search_experiences() → recent interview posts
        ├─ _build_system(context_type, company, rag_ctx)
        │    └─ Returns Claude system prompt with:
        │         - Your full PROFILE from config.py (GSTN wins, stack, gaps)
        │         - RAG context (real interview experiences from DB)
        │         - Prompt template for context_type (jd/eval/star/mock...)
        └─▶ POST https://api.anthropic.com/v1/messages
              model: claude-sonnet-4-5
              stream: false (or true for /api/coach/stream SSE)
```

#### 4. Intel scraping pipeline
```
app/scheduler.py (6 AM IST cron) OR prep scrape
  └─▶ intel/scraper.py::run_scraper()
        ├─ sources/leetcode_discuss.py → GraphQL query, no key needed
        ├─ sources/reddit.py → Reddit OAuth2 (REDDIT_CLIENT_ID env var)
        │    └─ r/leetcode, r/cscareerquestions, r/leetcodedesi, r/IndiaTechies
        └─ sources/enginebogie.py → HackerNews Algolia API
             │
             ▼  (for each scraped post)
        intel/db.py::insert_experience()
             └─ UNIQUE(source, source_id) → safe to re-run, no duplicates
                 SQLite WAL mode → concurrent reads during writes
```

#### 5. Gap Analysis
```
Browser::GET /api/gaps OR prep check
  └─▶ app/routers/progress.py::get_gaps()
        └─▶ intel/analyzer.py::compute_gap_analysis(progress_data)
              ├─ Reads LEVEL_EXPECTATIONS from config.py (SDE-2 / SDE-3 bar)
              ├─ java_lc < 100 → CRITICAL severity gap
              ├─ hard < 30    → HIGH severity gap
              ├─ sd_studied < 15 → HIGH severity gap
              └─ Returns sorted list of gaps with action items
        └─▶ intel/analyzer.py::readiness_percentage()
              └─ 100 - sum(severity_weights) → score
                 CRITICAL=-25, HIGH=-15, MEDIUM=-8
```

---

### Key Design Decisions (Learn From These)

#### 1. React 19 + Vite dashboard (multi-stage Docker build)
**Why:** 16 pages with visualizations, streaming chat, timers, and interactive practice sessions outgrew a single HTML file.
**How:** React 19, Vite 6, TanStack Query for caching, Recharts for charts, Lucide for icons. Vite proxies to FastAPI in dev, builds to `portal/` for production.
```bash
# Development: hot-reload on both frontend and backend
uvicorn app.main:app --reload --port 5555   # API
cd ui && npm run dev                         # UI at :5173 (proxied to :5555)

# Production: multi-stage Dockerfile builds UI in Node, serves from FastAPI
docker-compose up                            # builds automatically
```

#### 2. SQLite over PostgreSQL
**Why:** Zero config, ships with Python, WAL mode handles concurrent reads.
**When to use Postgres instead:** multiple servers writing, >10GB data, complex JOINs at scale.
```python
conn.execute("PRAGMA journal_mode=WAL")   # allows reads during writes
conn.execute("PRAGMA foreign_keys=ON")    # data integrity
```

#### 3. No SDK — raw urllib for Claude API
**Why:** Avoids the `anthropic` package dependency, works on Python 3.9+, shows you exactly what's happening.
**Trade-off:** More boilerplate. Worth it for a personal tool on Railway.
```python
req = urllib.request.Request("https://api.anthropic.com/v1/messages",
    data=json.dumps(payload).encode(), headers={...})
```

#### 4. APScheduler inside FastAPI (no Celery/Redis)
**Why:** Single-process, no broker needed. Works on Railway's $5/month plan.
**When you'd need Celery:** multiple workers, job retries, job queues, distributed tasks.
```python
_scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
_scheduler.add_job(job_scrape_all, CronTrigger(hour=6, minute=0))
```

#### 5. RAG pattern without a vector DB
**Why:** SQLite full-text search is fast enough for <10K documents.
**How:** `search_experiences(company=company, limit=5)` → recent posts → injected into system prompt.
**When to upgrade:** >50K documents → use Qdrant/Pinecone with embeddings.

#### 6. In-memory rate limiting
**Why:** No Redis dependency for a personal tool.
**How:** Dict of `{ip: [timestamps]}` — sliding window, cleaned on every request.
**Limit:** 120 req/min general, 30 req/min for AI endpoints.

#### 7. prep.py dispatch pattern
All 55+ CLI commands follow the same pattern — single `if/elif` chain:
```python
cmd = args[0].lower()
if cmd in ("plan", "today"):
    cmd_plan(args[1:])
elif cmd in ("drill",):
    cmd_drill(args[1:])
elif cmd in ("pp",):
    cmd_pp(args[1:])   # thin wrapper → intel/pp_tracker.py
```
**Lesson:** Keep the CLI file as a router only. All logic lives in `intel/`.

#### 8. ntfy.sh push notifications
**Lesson learned in this project:** HTTP headers must be ASCII strings.
Passing `bytes` as a header value to `urllib.request` silently corrupts it.
The notification rang but had no content until this was fixed.
```python
# WRONG: brief["title"].encode() → bytes → urllib sends as b'...' literally
# RIGHT:
safe_title = brief["title"].replace("—", "-").encode("ascii", errors="ignore").decode()
headers = {"Title": safe_title, "Content-Type": "text/plain; charset=utf-8"}
```

---

### Dependency Map

```
prep.py
  → intel/drill.py         → intel/db.py
  → intel/pp_tracker.py    → data/programming_pathshala_courses.json
  → intel/java_qa.py       → logs/progress.json
  → intel/mock_engine.py   → intel/db.py
  → intel/lld_engine.py    → intel/db.py
  → intel/behavioral.py    → docs/GSTN_Interview_QuestionBank_296Q.md (for qbank)
  → intel/brief.py         → intel/drill.py, intel/behavioral.py, intel/db.py
  → intel/coach.py         → intel/config.py (ANTHROPIC_API_KEY, CLAUDE_MODEL)

app/main.py
  → app/routers/*          → intel/* (lazy imports inside handlers)
  → app/scheduler.py       → intel/scraper.py, intel/brief.py

intel/config.py            → PROFILE, TARGET_COMPANIES, LEVEL_EXPECTATIONS
                             (single source of truth for all AI prompts)
```

---

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for full system design documentation including:
- Component overview + ASCII system diagram
- SQLite schema (11 tables) and data flow
- LLM integration patterns (caching, context assembly, adaptive planning)
- Rate limiting, OAuth2, WAL mode, idempotent writes
- **Interview talking points** derived from building PrepForge

---

*Last updated: Mar 25, 2026 · Day 7/184 · Week 1/26 · Phase 1 · ntfy topic: senior_prep/sde2*
