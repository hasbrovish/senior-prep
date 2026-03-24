# PrepForge — SDE-2/SDE-3 Interview Prep System
### Jayanti Vishnoi · 5.5 YOE at GSTN · March → September 2026

```
PHASE 1  Mar–Jun 2026  →  First offer: Razorpay / CRED / Juspay / Flipkart
PHASE 2  Jun–Sep 2026  →  Dream offer: Amazon / Google / Goldman / Swiggy
```

---

## Project Overview

This is a **personal, full-stack interview preparation system** — not just notes. It combines:

- **CLI tracker** (`prep`) — daily planner, LeetCode tracker, mock runner, progress dashboards
- **Intelligence Engine** (`intel/`) — scrapes real interview experiences from LeetCode, Reddit, HackerNews; feeds them into an RAG-based AI coach
- **FastAPI server** (`app/`) — REST API + web portal with background jobs
- **Practice Engines** — Java DSA drill, LLD practice (20 problems), mock round score tracker, behavioral gap detector, TC intelligence

---

## Quick Start

```bash
# 1. Setup alias (one time)
echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
source ~/.zshrc

# 2. Start your day
prep               # today's plan + current block
prep drill         # today's 3 Java DSA problems
prep brief         # morning brief (streak, intel, plan)

# 3. Study
prep mock-round google dsa      # mock round (saves score to DB)
prep lld parking-lot            # LLD practice session
prep lp-check                   # behavioral gap analysis
prep tc amazon                  # TC ranges + negotiation tips

# 4. Track
prep lc "Two Sum"               # mark LeetCode problem done
prep log                        # log today's work
prep check                      # health check + coach advice

# 5. Web portal
prep portal                     # starts FastAPI at http://localhost:5555
```

---

## Project Structure

```
senior-prep/
│
├── prep.py                     ← Main CLI (55+ commands, 3500+ lines)
├── requirements.txt            ← Python dependencies
├── Dockerfile                  ← Production container
├── docker-compose.yml          ← Local containerized run
├── .env.example                ← Required env vars template
│
├── app/                        ← FastAPI server
│   ├── main.py                 ← App factory, CORS, rate limiting, startup
│   ├── scheduler.py            ← Background jobs (scrape 6AM, LC sync, brief 8AM)
│   └── routers/
│       ├── coach.py            ← AI coaching endpoints (stream + non-stream)
│       ├── practice.py         ← Drill, Mock, LLD, Behavioral, TC, Brief
│       ├── intel_routes.py     ← Intel search, trending, company profiles
│       ├── progress.py         ← Progress read/write, portal data, gap analysis
│       └── career.py           ← Ladder, skill map, weekly plan
│
├── intel/                      ← Intelligence Engine
│   ├── config.py               ← Models, API keys, profile data, targets
│   ├── db.py                   ← SQLite schema + CRUD (9 tables)
│   ├── scraper.py              ← Orchestrates all sources
│   ├── coach.py                ← Claude API calls (JD analyze, evaluate, STAR, mock)
│   ├── analyzer.py             ← Trend analysis, gap analysis, readiness scoring
│   ├── resources.py            ← Curated resource index
│   ├── drill.py                ← Java DSA drill engine (104 NeetCode problems)
│   ├── mock_engine.py          ← Mock score tracking + trend charts
│   ├── lld_engine.py           ← 20 LLD problems with SOLID rubrics
│   ├── behavioral.py           ← Amazon LP gap detector + Bar Raiser probes
│   ├── brief.py                ← Morning brief generator + ntfy.sh push
│   └── sources/
│       ├── reddit.py           ← Reddit r/leetcode, r/cscareerquestions, r/ExperiencedDevs
│       ├── leetcode_discuss.py ← LeetCode Discuss GraphQL (fixed for 2025 API)
│       ├── enginebogie.py      ← Reddit r/IndiaTechies + HackerNews Algolia
│       └── levelsfyi.py        ← TC intelligence (levels.fyi + static data)
│
├── portal/
│   └── index.html              ← Web dashboard frontend
│
├── data/                       ← Runtime data (git-ignored)
│   └── interviews.db           ← SQLite: 9 tables, all scraped + practice data
│
├── logs/                       ← Runtime logs (git-ignored)
│   └── progress.json           ← All CLI tracker state
│
├── Interview_Answers/          ← Study library (git-ignored, personal)
│   ├── Amazon_LP_STAR_Bank.md  ← 22 GSTN STAR stories × 14 Amazon LPs
│   ├── SystemDesign_Interview_Cheatsheet.md
│   ├── GSTN_Architecture_Reference.md
│   ├── Section_01_Java_Core.md ... Section_21_SystemDesign.md
│   └── Company_Questions_Phase1/2.md
│
└── projects/
    └── kafka-pipeline/         ← GitHub portfolio project (Spring Boot + Kafka + Redis)
```

---

## All Commands

### Daily Workflow
```bash
prep                            # today's plan (time-aware: shows current block)
prep plan                       # same as above
prep full                       # all blocks expanded
prep log                        # log what you did today
prep check                      # health check + AI coach note
prep sync                       # sync LeetCode stats (hasbrovish95)
prep score                      # one-line scoreboard
prep brief                      # today's morning brief
prep brief --send               # send to phone (requires NTFY_TOPIC env var)
```

### Java DSA Drill Engine ✅ NEW
```bash
prep drill                      # today's 3 Java problems (company-tagged, pattern-aligned)
prep drill google               # tuned for Google's trending patterns
prep drill done "Two Sum"       # mark done
prep drill done "Two Sum" --time 28 --struggled   # with flags
prep drill stats                # drill streak + history
```

### Mock Round Simulator (tracks scores over time) ✅ NEW
```bash
prep mock-round google dsa      # AI mock DSA round, saves score to DB
prep mock-round amazon behavioral
prep mock-round flipkart system_design
prep mock-trend                 # score trend chart — all companies
prep mock-trend google          # Google-specific trend
prep mock-trend amazon dsa      # filter by company + round type
```

### LLD Practice Engine (20 problems) ✅ NEW
```bash
prep lld                        # list all 20 LLD problems
prep lld list google            # filter by company
prep lld parking-lot            # 45-min timed session with SOLID scoring
prep lld lru-cache              # practice LRU Cache (must-do)
prep lld notification-system    # Notification System (your GSTN advantage)
prep lld elevator               # Elevator System
prep lld chess                  # Chess Game
prep lld bookmyshow             # Movie Booking
prep lld splitwise              # Expense Sharing
prep lld scores                 # view your LLD history + scores
```

### Behavioral Gap Detector ✅ NEW
```bash
prep lp-check                   # Amazon LP gap analysis (reads STAR bank file)
                                # Shows: coverage %, thin LPs, missing quantified results
                                # Bar Raiser probing questions for weakest LPs
```

### TC Intelligence ✅ NEW
```bash
prep tc                         # TC overview for all 11 target companies
prep tc google                  # Google TC (L4/L5) + negotiation playbook
prep tc amazon                  # Amazon TC structure (RSU cliff, signing bonus)
prep tc flipkart                # Flipkart ESOP + base breakdown
prep tc goldman                 # Goldman deferred comp structure
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
prep scrape                     # scrape all sources (LeetCode, Reddit, HackerNews)
prep scrape reddit              # scrape specific source
prep trending                   # what's being asked across all companies
prep trending google            # Google-specific last 30 days
prep experiences                # browse all scraped interview experiences
prep experiences amazon sde2    # filter by company + role
prep company google             # full company intelligence profile
prep add-experience             # manually add an experience
prep intel-status               # DB dashboard (total experiences, sources)
prep resources                  # curated resource index
prep resources dsa              # DSA resources only
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
prep week-summary               # export week snapshot
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
prep apply "Razorpay"           # log job application
prep offer "Razorpay" 32LPA     # log offer received
```

### Timers & Focus
```bash
prep focus 45                   # Pomodoro timer (45 min)
prep focus                      # default 25 min
```

### Web Portal
```bash
prep portal                     # start FastAPI at http://localhost:5555
prep portal 8080                # custom port
# API docs:  http://localhost:5555/docs
```

---

## Environment Setup

```bash
# Copy and fill in your keys
cp .env.example .env

# Minimum required
export ANTHROPIC_API_KEY=sk-ant-...        # for AI features
export NTFY_TOPIC=prepforge-yourname       # for phone push notifications

# Optional — improves Reddit scraping (2x rate limit)
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
```

### ntfy.sh Setup (Free Phone Notifications)
```bash
# 1. Install ntfy app on phone (Android/iOS)
# 2. Subscribe to a topic of your choice: prepforge-jayanti
# 3. Set env var:
export NTFY_TOPIC=prepforge-jayanti
# 4. Test:
prep brief --send
```

### Reddit API Setup (Optional, Free)
```bash
# 1. Go to reddit.com/prefs/apps
# 2. Create app → script type → name: PrepForge
# 3. Copy client ID and secret:
export REDDIT_CLIENT_ID=your_client_id
export REDDIT_CLIENT_SECRET=your_client_secret
```

---

## API Reference

When running `prep portal`, all features are available via REST:

| Endpoint | Method | Description |
|---|---|---|
| `/api/drill/today` | GET | Today's Java DSA drill |
| `/api/drill/done` | POST | Mark drill problem done |
| `/api/mock/trend` | GET | Score trend over time |
| `/api/mock/score` | POST | Save mock session score |
| `/api/mock/readiness/{company}` | GET | Readiness % per round |
| `/api/lld/problems` | GET | List 20 LLD problems |
| `/api/lld/problem/{key}` | GET | Problem details |
| `/api/lld/evaluate` | POST | AI-evaluate your design |
| `/api/behavioral/check` | GET | Amazon LP gap analysis |
| `/api/behavioral/probes/{lp}` | GET | Probing questions |
| `/api/tc/{company}` | GET | TC intelligence |
| `/api/brief` | GET | Morning brief (add `?send=true`) |
| `/api/coach` | POST | AI coaching (non-stream) |
| `/api/coach/stream` | POST | AI coaching (SSE stream) |
| `/api/intel/stats` | GET | DB dashboard |
| `/api/intel/experiences` | GET | Search experiences |
| `/api/intel/trending` | GET | Trending topics |
| `/api/intel/company/{name}` | GET | Company profile |
| `/api/intel/scrape` | POST | Trigger scrape |
| `/api/progress` | GET/POST | Progress data |
| `/api/gaps` | GET | Gap analysis |
| `/api/career/ladder` | GET | SDE-2→SDE-3 map |
| `/health` | GET | Health check |

---

## Deployment

See [DEPLOY.md](DEPLOY.md) for full deployment guide.

**Option A — Local:**
```bash
pip install -r requirements.txt
prep portal
```

**Option B — Docker:**
```bash
docker-compose up
```

**Option C — Railway.app (free, recommended for personal use):**
```bash
# Push to GitHub → connect Railway → set env vars → auto-deploys
# Free tier: 500 MB RAM, always-on, custom .railway.app domain
```

---

## What's Done ✅

| Feature | Status | Command |
|---|---|---|
| 26-week daily prep plan | ✅ Done | `prep` |
| LeetCode sync (auto + manual) | ✅ Done | `prep sync`, `prep lc` |
| Pattern heatmap | ✅ Done | `prep heatmap` |
| Java language tracker | ✅ Done | `prep java` |
| Spaced repetition (15 topics) | ✅ Done | `prep sr` |
| Bug journal + failure analysis | ✅ Done | `prep bug`, `prep recover` |
| Application + offer tracking | ✅ Done | `prep apply`, `prep offer` |
| Interview round logging | ✅ Done | `prep interview-log` |
| 296-question verbal practice bank | ✅ Done | `prep question` |
| Built-in mock interviews (6 types) | ✅ Done | `prep mock` |
| Health check + coach notes | ✅ Done | `prep check` |
| Weekly retro + summary export | ✅ Done | `prep retro` |
| FastAPI web server | ✅ Done | `prep portal` |
| Intel scraping (Reddit, LC, HN) | ✅ Done | `prep scrape` |
| RAG-based AI coach | ✅ Done | `prep ask` |
| JD gap analysis | ✅ Done | `prep jd-analyze` |
| Answer evaluation (hire rubric) | ✅ Done | `prep evaluate` |
| STAR story generator | ✅ Done | `prep story` |
| Company intelligence profiles | ✅ Done | `prep company` |
| Readiness assessment | ✅ Done | `prep readiness` |
| Background scheduler (APScheduler) | ✅ Done | auto runs with portal |
| Docker + docker-compose | ✅ Done | `docker-compose up` |
| Java DSA Drill Engine (104 problems) | ✅ Done | `prep drill` |
| Mock score tracker (trend charts) | ✅ Done | `prep mock-round` |
| LLD Practice Engine (20 problems) | ✅ Done | `prep lld` |
| Behavioral gap detector (Amazon LPs) | ✅ Done | `prep lp-check` |
| TC intelligence (11 companies) | ✅ Done | `prep tc` |
| Morning brief + ntfy.sh push | ✅ Done | `prep brief` |
| DB schema (9 tables, WAL mode) | ✅ Done | auto on startup |

---

## What's Pending 🔲

### P0 — Do this week
| Task | Why | How |
|---|---|---|
| Set `ANTHROPIC_API_KEY` | Unlocks all AI features | `export ANTHROPIC_API_KEY=sk-ant-...` |
| Switch LeetCode to Java | Critical gap: 4/155 in Java | LeetCode → Code → change language |
| Run `prep drill` daily | Fixes Java gap in 6 weeks | 30 min morning block |
| Complete missing LP stories | 4 critical LPs have 0 stories | `prep lp-check` → write stories |

### P1 — This month
| Task | Why | How |
|---|---|---|
| Set up ntfy.sh phone push | Automatic daily brief on phone | `export NTFY_TOPIC=prepforge-yourname` |
| Set up Reddit PRAW API | 2x more experiences scraped | reddit.com/prefs/apps → 2 min |
| Deploy to Railway.app | Access from anywhere | See DEPLOY.md → Option C |
| Add LP stories for 4 critical gaps | Amazon LP every single round | Dive Deep, Bias for Action, Earn Trust, Have Backbone |
| Run `prep lld parking-lot` weekly | LLD is asked at Adobe, Flipkart | Every Saturday |

### P2 — Phase 2 (after first offer)
| Feature | Status | Effort |
|---|---|---|
| Vector search (Qdrant semantic RAG) | Not started | 1 day — replaces keyword search |
| Blind/TeamBlind scraper | Not started | 2h — needs your session cookie |
| Portal UI for new practice features | Partial — needs new routes wired | 1 day |
| Live TC scraper (levels.fyi) | Static data only (live fallback exists) | Working, may hit rate limits |
| Test suite | Not started | Not critical for personal tool |
| PRAW enhanced scraping | Config exists, needs credentials | 2 min setup |

---

## Database Schema

```
interviews.db (SQLite, WAL mode)
│
├── experiences         ← scraped interview posts (source, company, role, outcome)
├── experience_rounds   ← individual rounds per experience (questions, topics, difficulty)
├── company_intel       ← aggregated company profiles (process, SD topics, TC)
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
LeetCode:  155 solved  (Easy: ~50, Medium: ~90, Hard: ~15)
Java:      4 problems  ← CRITICAL: must reach 30 by Week 6
Streak:    2 days
Week:      1/26  (Phase 1)
Day:       6/184

Amazon LP coverage:   57%  (4 critical LPs with 0 stories)
Critical missing LPs: Dive Deep, Bias for Action, Earn Trust, Have Backbone

Interview experiences in DB: run 'prep intel-status' to see current count
```

---

## Your Competitive Advantages

Use these in every round — they are real, verifiable, production-scale:

```
Scale:        14M taxpayers  ·  3B invoices/year  ·  500 GST filings/sec peak
Caching:      JBoss DataGrid + EhCache  ·  70+ regions  ·  40% DB load reduction
Kafka:        Consumer framework with DLQ  ·  exactly-once semantics  ·  2M+ events/day
Transactions: XA distributed (Atomikos)  ·  cross-service ledger consistency
Patterns:     Strategy (CaseCustomizerFactory)  ·  Template Method (Consumer)  ·  Factory
LLD example:  Notification System (CommunicationService)  ←  strongest LLD answer
SD example:   GST Return Filing System  ←  can speak to every design decision
```

---

## Study Library (Interview_Answers/)

| File | Round | Phase |
|---|---|---|
| `Section_DSA_Java_Patterns.md` | DSA | 1 |
| `Section_LLD_Complete.md` | LLD | 1 |
| `Section_21_SystemDesign_DeepDive_With_Answers.md` | SD | 1 |
| `Section_01_Java_Core.md` | Java | 1 |
| `Section_02_Spring_Boot.md` | Java | 1 |
| `Section_03_Hibernate_JPA.md` | Java | 1 |
| `Section_04_05_06_Microservices_Kafka_Redis.md` | Java | 1 |
| `Section_07_08_Database_DistributedSystems.md` | Java | 1 |
| `Section_Modern_Java_Observability_CQRS.md` | Java | 2 |
| `Section_20_FAANG_SDE2_SDE3_Advanced.md` | Java | 2 |
| `Section_SD_Consumer_Products.md` | SD | 2 |
| `Amazon_LP_STAR_Bank.md` | Behavioral | 1+2 |
| `GSTN_Architecture_Reference.md` | SD + Java | Always |
| `GSTN_Complete_SDE2_SDE3_InterviewPrep.md` | All | Always |
| `SystemDesign_Interview_Cheatsheet.md` | SD | Always |
| `Company_Questions_Phase1.md` | All | Phase 1 |
| `Company_Questions_Phase2.md` | All | Phase 2 |

---

## Week-by-Week Plan

```
WEEK 1  (Mar 19)  Resume + Profile Setup       DSA: Arrays, Strings
WEEK 2  (Mar 26)  Java Core Internals           DSA: Two Pointers, Sliding Window
WEEK 3  (Apr 2)   Spring Boot + Hibernate       DSA: HashMap, Linked Lists
WEEK 4  (Apr 9)   Microservices + Kafka + Redis DSA: Stack, Queue, Binary Search
WEEK 5  (Apr 16)  Review + First Mock           DSA: Review backlog
WEEK 6  (Apr 23)  Low-Level Design Focus        DSA: Trees BFS/DFS
WEEK 7  (Apr 30)  System Design Mid-Tier        DSA: Dynamic Programming Easy
WEEK 8  (May 7)   Databases + Distributed       DSA: Graphs BFS/DFS
WEEK 9  (May 14)  Cloud + Docker + K8s          DSA: Heap / Priority Queue
WEEK 10 (May 21)  Behavioral + Acceleration     DSA: Mixed Medium
WEEK 11 (May 28)  Full Mock Interview Week      DSA: Backtracking, Recursion
WEEK 12 (Jun 4)   Interview Blitz               DSA: Binary Search Medium
WEEK 13 (Jun 11)  Interview Blitz Refine        DSA: Medium/Hard
WEEK 14 (Jun 18)  Close First Offer             DSA: Greedy, Intervals
─── PHASE 2 ────────────────────────────────────────────────────────────────────
WEEK 15-16        DSA Hard Mode + FAANG SD      2 hrs DSA daily
WEEK 17-18        Graphs + Golang brush-up      Advanced patterns
WEEK 19-20        Consumer products SD          Twitter, Google Drive, Uber
WEEK 21-22        Company-specific prep         Amazon LPs, Goldman depth
WEEK 23-24        Final polish                  Dream company applications
WEEK 25-26        Close dream offer             Negotiate
```

---

*Last updated: March 2026 · Day 6/184 · Week 1/26 · Phase 1*
*Stack: Java · Spring Boot · Kafka · Redis · MySQL · MongoDB · Golang · Docker · K8s · AWS*
