# Jayanti Vishnoi — SDE-2/SDE-3 Interview Prep
### 6-Month Programme · March → September 2026 · 5.5 YOE at GSTN

---

```
PHASE 1 (Mar–Jun 2026)  →  First offer at Razorpay / CRED / Juspay / Meesho
PHASE 2 (Jun–Sep 2026)  →  Dream offer at Amazon / Flipkart / Goldman / Swiggy / Stripe
```

---

## Daily Commands

```bash
# Setup once
echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc && source ~/.zshrc

prep              # today's plan
prep check        # health check + coach advice
prep sync         # sync LeetCode stats (hasbrovish95)
prep log          # log what you did today
prep status       # full progress dashboard
prep lc "Two Sum" # mark a LeetCode problem done (Java only!)
prep apply "Razorpay"  # log a job application
prep mock sd      # system design mock (45 min)
prep mock java    # Java internals mock (45 min)
prep mock lld     # LLD mock (45 min)
prep review       # weekly feedback
```

---

## The Interview Rounds & Your Files

Every SDE-2/SDE-3 interview has these 5 rounds. Here's exactly what to open for each.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ROUND 1 · DSA / Problem Solving (45-60 min)                               │
│  Bar: LeetCode Medium (Phase 1) → Medium-Hard (Phase 2)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  OPEN: Interview_Answers/Section_DSA_Java_Patterns.md                      │
│    Section 1 → C++ to Java translation (read first week)                   │
│    Section 2 → 12 pattern templates (Sliding Window, BFS, DP, etc.)        │
│    Section 3 → Full DP guide (10 core problems with Java code)             │
│    Section 4 → Graph algorithms in Java                                    │
│    Section 6 → Top 30 must-do problems (includes P0 from real interviews)  │
│                                                                             │
│  P0 PROBLEMS (appeared in Apple/Oracle/Amazon/DoorDash real rounds):       │
│    LRU Cache #146 · Trapping Rain Water #42 · Task Scheduler #621          │
│    First Missing Positive #41 · Evaluate RPN #150 · Container Water #11    │
│                                                                             │
│  RULE: Every problem in Java. No exceptions.                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ROUND 2 · Low-Level Design / LLD (45-60 min)                              │
│  Bar: OOP, SOLID, Design Patterns, class hierarchy, concurrency            │
├─────────────────────────────────────────────────────────────────────────────┤
│  OPEN: Interview_Answers/Section_LLD_Complete.md                           │
│    Section 1 → 45-min LLD interview framework (minute-by-minute)           │
│    Section 2 → SOLID principles with Java before/after code                │
│    Section 3 → 5 full problems with COMPLETE Java code:                    │
│                  Problem 1: Parking Lot (Strategy + Singleton)             │
│                  Problem 2: Vending Machine (State pattern)                │
│                  Problem 3: Elevator System (LOOK algo, threading)         │
│                  Problem 4: BookMyShow (concurrency, seat locking)         │
│                  Problem 5: LRU Cache (LinkedHashMap + DLL + HashMap)      │
│    Section 4 → 10 design patterns quick reference with trigger phrases     │
│    Section 5 → SDE-3 bar: what extra is expected                           │
│                                                                             │
│  START: Week 3. Phase 1 companies ask LLD in Round 1 or 2.                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ROUND 3 · High-Level Design / System Design (45-60 min)                   │
│  Bar: Clean thinking + trade-offs (Phase 1) → FAANG scale (Phase 2)       │
├─────────────────────────────────────────────────────────────────────────────┤
│  YOUR STRONGEST WEAPON: GSTN designs (use "I've built this")               │
│                                                                             │
│  GSTN-based designs (Phase 1):                                             │
│    Interview_Answers/Section_21_SystemDesign_DeepDive_With_Answers.md     │
│      → GST Return Filing System (14M users, 500M filings/yr)              │
│      → Case Management Workflow Engine                                     │
│      → Distributed Tax Ledger (MySQL + HBase dual-storage)                │
│      → Distributed Cache Layer (70+ regions, 2-tier)                      │
│      → Async Event Pipeline (Kafka + DLQ + retry)                         │
│      → Notification System · E-Invoice · Auth System                      │
│                                                                             │
│  Consumer product designs (Phase 2):                                       │
│    Interview_Answers/Section_SD_Consumer_Products.md                       │
│      → Twitter/Instagram Feed (fan-out hybrid, celebrity problem)          │
│      → Google Drive (chunking, deduplication, sync)                       │
│      → WhatsApp (WebSocket, delivery receipts, group messaging)            │
│      → Uber/Ola (Geohash, driver matching, surge pricing)                 │
│      → BONUS: Decision trees (which DB / queue / cache to pick)           │
│                                                                             │
│  Framework cheatsheet:                                                     │
│    Interview_Answers/SystemDesign_Interview_Cheatsheet.md                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ROUND 4 · Java/Spring Deep Dive + Past Work (45-60 min)                   │
│  Bar: Internals, GSTN war stories, concurrency, distributed systems        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Core Java/Spring (foundation):                                            │
│    Interview_Answers/Section_01_Java_Core.md         → JVM, GC, threading │
│    Interview_Answers/Section_02_Spring_Boot.md       → Auto-config, @Tx   │
│    Interview_Answers/Section_03_Hibernate_JPA.md     → N+1, caching, lazy │
│    Interview_Answers/Section_04_05_06_...Kafka_Redis.md → Your strongest  │
│    Interview_Answers/Section_07_08_Database...md     → DB + distributed   │
│                                                                             │
│  FAANG-level depth (Phase 2):                                              │
│    Interview_Answers/Section_20_FAANG_SDE2_SDE3_Advanced.md               │
│      → JVM lock internals (biased/thin/fat lock)                          │
│      → Java Memory Model, happens-before, volatile                        │
│      → ConcurrentHashMap CAS, ReentrantLock vs synchronized               │
│                                                                             │
│  Modern Java + 2025-2026 trends (new — critical):                         │
│    Interview_Answers/Section_Modern_Java_Observability_CQRS.md            │
│      → Java 17-21: Records, Sealed Classes, Virtual Threads (Loom)        │
│      → Spring Boot 3.x: Micrometer, Observability, Security 6             │
│      → Observability: SLOs, RED method, OpenTelemetry, distributed tracing│
│      → CQRS + Event Sourcing (Apple asked this directly)                  │
│      → DDD: Bounded Context, Aggregates, Value Objects                    │
│                                                                             │
│  Your GSTN codebase as answers:                                            │
│    Interview_Answers/GSTN_Architecture_Reference.md                        │
│    Interview_Answers/GSTN_Complete_SDE2_SDE3_InterviewPrep.md             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ROUND 5 · Behavioral / Hiring Manager (30-45 min)                         │
│  Bar: STAR stories, "why this company", SDE-3 leadership signals          │
├─────────────────────────────────────────────────────────────────────────────┤
│  For Amazon (LP format):                                                   │
│    Interview_Answers/Amazon_LP_STAR_Bank.md                                │
│      → 22 GSTN STAR stories covering all 14 Amazon LPs                    │
│      → Every round has 2 LP questions — prepare as warmup, not afterthought│
│                                                                             │
│  For all other companies (non-Amazon format):                              │
│    Interview_Answers/Section_Behavioral_DB_Golang.md  → Part 1            │
│      → STARL framework (better than plain STAR)                           │
│      → 8 SDE-3-specific questions with GSTN-based answers                 │
│      → Company-specific behavioral angles (Razorpay, Swiggy, Goldman...)  │
│      → "Why this company?" templates for 6 companies                      │
│      → Negotiation playbook (offer anatomy, scripts, what to negotiate)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Complete File Map

### Master Plan & Tracker

| File | What it is |
|---|---|
| `MASTER_6MONTH_PROGRAMME.md` | **The single source of truth.** 26-week plan, weekly goals, study material map, milestones. Open this every Sunday. |
| `prep.py` | Python CLI tracker. Run `prep` daily. Tracks LeetCode, applications, daily logs, offers. |
| `logs/progress.json` | Auto-persisted data. Don't edit manually. |
| `GSTN_Interview_QuestionBank_296Q.md` | 296 Q&A bank. Mapped to weekly sections (Q1-25 = Java Core, etc.). |

---

### Interview_Answers/ — Your Study Library

#### NEW FILES (built this session — biggest gaps closed)

| File | Lines | Round | When |
|---|---|---|---|
| `Section_LLD_Complete.md` | 1,192 | Round 2 | **Start Week 3** |
| `Section_DSA_Java_Patterns.md` | 920 | Round 1 | **Start Week 1** |
| `Section_SD_Consumer_Products.md` | 724 | Round 3 | Week 7 + Phase 2 |
| `Section_Modern_Java_Observability_CQRS.md` | 860 | Round 4 | Week 8 onwards |
| `Section_Behavioral_DB_Golang.md` | 731 | Round 4+5 | Week 8 onwards |
| `Section_API_Design_SQL_Practice.md` | 2,435 | Round 4 | Week 8 onwards |
| `Company_Questions_Phase1.md` | 799 | All rounds | **Before each Phase 1 application** |
| `Company_Questions_Phase2.md` | 1,082 | All rounds | Before each Phase 2 application |

#### ORIGINAL FILES

| File | Lines | Round | When |
|---|---|---|---|
| `Section_21_SystemDesign_DeepDive_With_Answers.md` | 2,275 | Round 3 | Week 7 |
| `Section_20_FAANG_SDE2_SDE3_Advanced.md` | 2,320 | Round 4 | Phase 2 |
| `GSTN_Complete_SDE2_SDE3_InterviewPrep.md` | 1,817 | All rounds | Always |
| `GSTN_Architecture_Reference.md` | 1,345 | Round 3+4 | Always |
| `Section_02_Spring_Boot.md` | 2,019 | Round 4 | Week 3 |
| `Section_01_Java_Core.md` | 1,017 | Round 4 | Week 2 |
| `Section_04_05_06_Microservices_Kafka_Redis.md` | 894 | Round 4 | Week 4 |
| `Section_09_10_11_Patterns_Docker_CICD.md` | 725 | Round 4 | Week 9 |
| `Section_16_17_18_19_Testing_Behavioral_Scenarios.md` | 552 | Round 5 | Week 10 |
| `Section_07_08_Database_DistributedSystems.md` | 573 | Round 4 | Week 8 |
| `Section_12_13_14_15_Cloud_Network_Design_Go.md` | 445 | Round 4 | Week 9 |
| `Section_03_Hibernate_JPA.md` | 656 | Round 4 | Week 3 |
| `Amazon_LP_STAR_Bank.md` | 237 | Round 5 | Week 10 |
| `SystemDesign_Interview_Cheatsheet.md` | 430 | Round 3 | Always |

---

### Research & Company Intel

| File | What it is |
|---|---|
| `DEEP_RESEARCH_INTERVIEW_PATTERNS_2025_2026.md` | 54-company research: interview formats, salary, DSA/SD bar, Java depth |
| `COMPANY_ANALYSIS.md` | Tiered company list with salary, stack, pass rate |
| `Interview_exp.txt` | Real interview experiences: Apple, Oracle, Amazon, DoorDash — exact questions asked |

---

### Resume & LinkedIn

| File | What it is |
|---|---|
| `RESUME_VARIANTS.md` | **3 resume variants**: Fintech / Consumer Product / Finance — swap top 6 bullets per company type |
| `LINKEDIN_RESUME_GUIDE.md` | ATS resume template + LinkedIn optimization guide |
| `LinkedIn_Profile_Complete_Update.md` | Ready-to-copy LinkedIn sections |
| `LinkedIn Saved Posts - Part 1/2/3.md` | 447 posts analyzed for prep insights |

---

### Mock Interviews & GitHub Project

| File/Dir | What it is |
|---|---|
| `MOCK_INTERVIEW_GUIDE.md` | Full mock interview structure — scoring rubrics, problem banks, self-assessment checklists |
| `projects/kafka-pipeline/` | **Working Spring Boot project**: idempotent Kafka producer + consumer (DLQ + Redis dedup + Micrometer) — show interviewers real code |

---

## Week-by-Week: What to Open

```
WEEK 1  (Mar 19) → MASTER_6MONTH_PROGRAMME + Section_DSA_Java_Patterns (S1, S2)
WEEK 2  (Mar 26) → Section_01_Java_Core + Section_DSA_Java_Patterns (S2 Two Pointer/Sliding)
WEEK 3  (Apr 2)  → Section_02_Spring_Boot + Section_03_Hibernate + Section_LLD_Complete (S1, S2, P1)
WEEK 4  (Apr 9)  → Section_04_05_06_Microservices_Kafka_Redis + Section_LLD_Complete (P2, P3) + DSA Patterns (S3 DP)
WEEK 5  (Apr 16) → Review week + Mock interview
WEEK 6  (Apr 19) → Section_LLD_Complete (P4, P5, S4, S5) — LLD fluency
WEEK 7  (Apr 26) → Section_21_SystemDesign + Section_SD_Consumer_Products (Twitter design)
WEEK 8  (May 3)  → Section_07_08_Database + Section_Behavioral_DB_Golang (Part 2) + Section_Modern_Java (Parts 1-4)
WEEK 9  (May 10) → Section_09_10_11 + Section_12_13_14_15 + Section_Modern_Java (Part 3 Observability)
WEEK 10 (May 17) → Amazon_LP_STAR_Bank + Section_Behavioral_DB_Golang (Part 1) + Applications push
WEEK 11 (May 19) → Full mock interview week (all 5 rounds)
WEEK 12-13       → Active interviews. Log every question with prep interview-log
WEEK 14          → Close first offer
─────────────── PHASE 2 ───────────────────────────────────────────────────
WEEK 15-16       → DSA hard mode: 2 hrs/day. NeetCode Blind 75.
WEEK 17-18       → Section_SD_Consumer_Products (Drive, WhatsApp, Uber) + Section_Behavioral_DB_Golang (Part 3 Go)
WEEK 19-20       → DSA: Graphs, DP hard, Heap hard
WEEK 21-22       → Company-specific: Amazon LPs, Goldman Java, PhonePe/Razorpay fintech
WEEK 23-24       → Final polish + dream company applications
WEEK 25-26       → Close dream offer + negotiate
```

---

## Your Competitive Advantages (Use These Every Round)

```
GSTN scale:   14M taxpayers · 3B invoices/year · 500 filings/sec peak
Caching:      JBoss DataGrid + EhCache · 70+ regions · 40% DB load reduction
Kafka:        Consumer framework with DLQ · exactly-once semantics · 2M+ events/day
Transactions: XA distributed transactions (Atomikos) · cross-service ledger consistency
Patterns:     Strategy (CaseCustomizerFactory) · Template Method (Consumer.java) · Factory
Scale:        Survived multiple filing season peaks · zero data loss in 18 months
```

---

## Content Score vs Interview Bar

| Round | Phase 1 Score | Phase 2 Score | Status |
|---|---|---|---|
| DSA (Java) | 7/10 | 5/10 | Switch to Java NOW. DP + Graphs started. |
| LLD | 8/10 | 7/10 | 5 problems with full code. Need 5 more in Phase 2. |
| System Design | 8/10 | 7/10 | GSTN designs strong. Consumer products now written. |
| Java/Spring Internals | 9/10 | 8/10 | Java 17-21 + Observability + CQRS added. |
| Behavioral | 8/10 | 7/10 | Amazon LP + SDE-3 behavioral + company-specific added. |
| **Overall** | **8/10** | **7/10** | Up from 5.5/10 before this session. |

---

## Quick Reference Cheatsheets

```bash
# Before a DSA round:
open Interview_Answers/Section_DSA_Java_Patterns.md
# → Read Section 2 for the pattern you'll likely see

# Before an LLD round:
open Interview_Answers/Section_LLD_Complete.md
# → Read Section 1 (framework) + the problem type

# Before a System Design round:
open Interview_Answers/SystemDesign_Interview_Cheatsheet.md
# → 45-min framework + estimation formulas

# Before behavioral:
open Interview_Answers/Amazon_LP_STAR_Bank.md          # Amazon
open Interview_Answers/Section_Behavioral_DB_Golang.md # Others

# Before Java round:
open Interview_Answers/Section_20_FAANG_SDE2_SDE3_Advanced.md
open Interview_Answers/Section_Modern_Java_Observability_CQRS.md
```

---

---

## Before Each Application — Company Cheat Sheet

```bash
# Phase 1 companies (Razorpay, CRED, Juspay, Meesho, Paytm, MMT, Atlassian, Groww, WGT, Slice)
open Interview_Answers/Company_Questions_Phase1.md
# → Find company section → check DSA table, SD question, Java deep-dive, your GSTN angle

# Phase 2 companies (Flipkart, Amazon, Goldman, PhonePe, Swiggy, Stripe, Uber, etc.)
open Interview_Answers/Company_Questions_Phase2.md

# Resume variant — pick one per application
open RESUME_VARIANTS.md
# → Fintech companies → Variant A bullets
# → Consumer product → Variant B bullets
# → Banking/Finance  → Variant C bullets

# Run a mock before applying:
prep mock sd      # 45-min system design
prep mock java    # 45-min Java depth
prep mock lld     # 45-min LLD
```

---

*Last updated: March 2026 | Programme Day 2 of 184*
*Stack: Java · Spring Boot · Kafka · Redis · MySQL · MongoDB · Golang · Docker · K8s · AWS*
