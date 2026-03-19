# SDE-2/SDE-3 Interview Prep System
### Jayanti Vishnoi — 6-Month Programme (Mar–Sep 2026)

A complete, self-contained interview preparation system built around a Python CLI tracker,
26-week structured plan, 296-question bank, spaced repetition, and daily automation.

---

## Quick Start

```bash
# One-time setup
echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
source ~/.zshrc

# Every day
prep             # today's plan
prep check       # health check + coach advice
prep sync        # sync LeetCode stats
```

---

## What's In This Repo

```
senior-prep/
├── prep.py                          ← Main CLI tracker (run this daily)
├── MASTER_6MONTH_PROGRAMME.md       ← The plan — 26 weeks, Phase 1 + Phase 2
├── GUIDE.md                         ← How everything works (read first)
│
├── Interview_Answers/               ← Study material (21 sections, ~1000 questions)
│   ├── Section_01_Java_Core.md          Q1–Q25   Java internals, GC, concurrency
│   ├── Section_02_Spring_Boot.md        Q26–Q60  Spring, @Transactional, Security
│   ├── Section_03_Hibernate_JPA.md      Q61–Q90  ORM, N+1, caching
│   ├── Section_04_05_06_...Kafka_Redis  Q91–Q135 Microservices, Kafka, Redis
│   ├── Section_07_08_...DistSystems     Q136–Q165 DB, SQL, distributed systems
│   ├── Section_09_10_11_...Docker_CICD  Q166–Q210 Patterns, Docker, CI/CD
│   ├── Section_12_13_14_15_...Go        Q211–Q250 Cloud, AWS, networking, Golang
│   ├── Section_16_17_18_19_...Behavioral Q251–Q296 Testing, behavioral, STAR
│   ├── Section_20_FAANG_SDE2_SDE3       Advanced FAANG-level questions
│   ├── Section_21_SystemDesign_DeepDive System design with full answers
│   ├── GSTN_Architecture_Reference.md   Full GSTN system design (your strongest asset)
│   └── GSTN_Complete_SDE2_SDE3_...md    Mock rounds, code walkthroughs, company prep
│
├── GSTN_Interview_QuestionBank_296Q.md  ← All 296 questions in one file
├── COMPANY_ANALYSIS.md                  ← 30+ companies: format, salary, DSA level
├── LINKEDIN_RESUME_GUIDE.md             ← LinkedIn + ATS resume template
│
├── trackers-docs/                   ← Excel trackers
│   ├── SDE2_Master_Tracker_Jayanti.xlsx     Main progress tracker
│   ├── Java_SpringBoot_Master_Interview_Sheet.xlsx
│   ├── System_Design_Master_Interview_Sheet.xlsx
│   ├── LLD_Master_Interview_Sheet_v2.xlsx
│   ├── DB_OS_CN_Master_Interview_Sheet_v2.xlsx
│   ├── Project_Experience_Master_Checklist.xlsx
│   └── Tech_Stack_Skills_Evaluation_Matrix.xlsx
│
├── generate_calendar.py             ← Generates ICS calendar (404 events)
├── SDE_Prep_Calendar.ics            ← Pre-generated calendar (import to Google/Notion)
├── setup_reminders.sh               ← macOS reminders setup (6AM, 8PM, Sunday 7PM)
└── logs/progress.json               ← Auto-persisted progress data
```

---

## The Programme

**Phase 1 (Weeks 1–13, Mar–Jun 2026):** First offer at a mid-tier product company
- Targets: Razorpay, Juspay, CRED, MakeMyTrip, Meesho, Paytm
- DSA: Easy → Medium, 7 problems/week
- Topics: Java Core → Spring → Kafka → System Design → LLD → Mock Interviews

**Phase 2 (Weeks 14–26, Jun–Sep 2026):** Dream offer at a top-tier company
- Targets: Amazon, Flipkart, Goldman Sachs, PhonePe, Swiggy, Google
- DSA: Hard problems, 10 problems/week, mock contests
- Topics: FAANG-level SD, advanced LLD, leadership principles, negotiation

---

## CLI Commands

### Daily
```
prep                           → today's plan (default)
prep log                       → log what you did today
prep check                     → health check + personalised coach advice
prep sync                      → sync LeetCode stats from hasbrovish95
```

### DSA & LeetCode
```
prep lc "Two Sum"              → mark a LeetCode problem done
prep java                      → Java language gap tracker (you have 154 total, 3 in Java!)
prep quiz <topic>              → active recall quiz question
prep focus [mins]              → Pomodoro timer (default 25 min)
```

### Spaced Repetition
```
prep sr                        → show review queue (due today + upcoming 7 days)
prep study <topic> <1-5>       → log topic studied, schedule next review
prep teach <topic>             → Feynman teach-it protocol with guiding prompts
```

### Bug Journal
```
prep bug "what I got wrong"    → log a stumbling block / failure pattern
prep bugs                      → view journal + weak area frequency chart
```

### Interviews
```
prep interview-log "Company"   → log an interview (questions, outcome, action items)
prep interviews                → interview history + recurring struggle analysis
```

### Applications
```
prep apply "Razorpay"          → log a job application
prep offer "Razorpay" 25LPA    → log an offer received
```

### Progress & Review
```
prep status                    → full dashboard (LeetCode, apps, offers, timeline)
prep review                    → weekly feedback + next actions
prep retro                     → structured weekly retrospective
```

### Topics (for study / quiz / teach / sr)
```
java-core    spring-boot    hibernate    microservices    kafka
redis        database       distributed  patterns         cloud
golang       testing        system-design    lld    behavioral
```

---

## Study Protocols Built In

| Protocol | Command | What it does |
|---|---|---|
| **Spaced Repetition** | `prep sr` / `prep study` | SM-2 algorithm — shows topics due for review, schedules based on confidence (1–5) |
| **Active Recall** | `prep quiz <topic>` | Random question from built-in bank, hint on Enter, auto-logs confidence |
| **Feynman Technique** | `prep teach <topic>` | Guided prompts to explain a topic out loud — gaps reveal exactly what interviewers find |
| **Bug Journal** | `prep bug` / `prep bugs` | Personal failure-pattern tracker with frequency analysis |
| **Pomodoro** | `prep focus [mins]` | Focus timer with live progress bar + macOS notification |
| **Interview Log** | `prep interview-log` | Structured post-interview capture: questions, struggle areas, action items |
| **Weekly Retro** | `prep retro` | Numbers + 5 reflection prompts + next-week preview |
| **Health Coach** | `prep check` | 9-signal analysis: streak, DSA pace, Java gap, hard ratio, apps, consistency |

---

## Reminders Setup (one time)

```bash
bash setup_reminders.sh
```

Sets up:
- 6:00 AM daily — LeetCode reminder + streak alert
- 8:00 PM daily — Evening study + log reminder
- Sunday 7:00 PM — Weekly review reminder
- Every terminal open — 1-line daily briefing

To remove: `bash setup_reminders.sh --remove`

---

## Calendar Import

```bash
python3 generate_calendar.py          # generates SDE_Prep_Calendar.ics
python3 generate_calendar.py --lite   # weekly + milestones only
```

Import `SDE_Prep_Calendar.ics` into Google Calendar or Notion Calendar.
Contains 404 events: 10 milestones + 26 weekly overviews + 184 morning DSA + 184 evening study blocks.

---

## Your Strongest Assets (from GSTN)

Turn these into stories for every interview:

| What you built | Why it matters | Translates to |
|---|---|---|
| JBoss DataGrid + EhCache across 45+ microservices | ~40% DB load reduction | Caching, distributed systems, performance |
| Kafka consumer with DLQ + exactly-once | 10+ async pipelines in production | Event-driven systems, reliability |
| XA transactions (Atomikos JTA) | ACID across Appeal + Ledger + Notification | Distributed transactions, data consistency |
| Strategy + Factory case workflow engine | 10+ litigation case types | LLD, design patterns, extensibility |
| HBase + MySQL ledger (300Cr+ invoices) | < 2s SLA at 14M user scale | Database design, large-scale systems |

---

## Current Gaps to Close

1. **Java DSA** — 154 problems solved, only 3 in Java. Run `prep java` for action plan.
2. **Hard problems** — Start adding 1 Hard per week from Week 10 onward.
3. **LLD practice** — Parking lot, chess, elevator. Use `trackers-docs/LLD_Master_Interview_Sheet_v2.xlsx`.
4. **FAANG system design framing** — Translate government-scale to product-scale language.
5. **Golang** — Brush up goroutines, channels, context. Use `Section_12_13_14_15`.

---

## Progress is Persisted

`logs/progress.json` stores everything:
- LeetCode problems done (with names + dates)
- Job applications + companies
- Daily logs
- Offers received
- LeetCode sync data (from API)
- Spaced repetition schedule
- Bug journal
- Interview logs
- Weekly retrospectives

---

*Started: March 19, 2026 — Phase 1 deadline: June 19, 2026 — Phase 2 deadline: September 19, 2026*
