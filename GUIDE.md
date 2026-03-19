# COMPLETE GUIDE — Jayanti's SDE-2/SDE-3 Prep System
# Start here. Everything you need is in this repo.
# Last updated: March 19, 2026

---

## QUICK START — First 10 Minutes

```bash
# Step 1: Set up the one-command shortcut (do this once)
echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
source ~/.zshrc

# Step 2: See today's plan
prep

# Step 3: Mark your first LeetCode problem done
prep lc "Two Sum"

# Step 4: Log what you did today (do this every evening)
prep log

# That's it. Repeat daily for 184 days.
```

---

## WHAT'S IN THIS REPO — File by File

```
senior-prep/
│
├── GUIDE.md                              ← YOU ARE HERE — master reference
│
├── prep.py                               ← Daily command-line tracker (run this every day)
│
├── MASTER_6MONTH_PROGRAMME.md            ← Full 26-week plan + NeetCode tracker + company list
│
├── COMPANY_ANALYSIS.md                   ← 30+ companies: tiers, salary, interview format, questions
│
├── LINKEDIN_RESUME_GUIDE.md              ← LinkedIn optimization + ATS resume template
│
├── GSTN_Interview_QuestionBank_296Q.md   ← 296 interview questions, all topics, all mapped to GSTN
│
├── logs/
│   └── progress.json                     ← Auto-saved: LeetCode done, applications, daily logs, offers
│
├── Interview_Answers/                    ← Deep-dive answer docs (study from these)
│   ├── Section_01_Java_Core.md           ← Q1–Q25: HashMap, Threads, JVM, Java 8+
│   ├── Section_02_Spring_Boot.md         ← Q26–Q60: Auto-config, @Transactional, Beans
│   ├── Section_03_Hibernate_JPA.md       ← Q61–Q90: N+1, Caching, Dirty checking
│   ├── Section_04_05_06_Microservices_Kafka_Redis.md  ← Q91–Q135: Kafka, Redis, Circuit breaker
│   ├── Section_07_08_Database_DistributedSystems.md   ← Q136–Q165: DB, CAP, HBase, SQL
│   ├── Section_09_10_11_Patterns_Docker_CICD.md       ← Q166–Q210: Design patterns, Docker, CI/CD
│   ├── Section_12_13_14_15_Cloud_Network_Design_Go.md ← Q211–Q250: AWS, Golang, Networking
│   ├── Section_16_17_18_19_Testing_Behavioral_Scenarios.md ← Q251–Q296: Testing, Behavioral
│   ├── Section_20_FAANG_SDE2_SDE3_Advanced.md         ← FAANG-level Java + system concepts
│   ├── Section_21_SystemDesign_DeepDive_With_Answers.md ← Full system design walkthroughs
│   ├── GSTN_Architecture_Reference.md    ← Complete GSTN system architecture for interviews
│   └── GSTN_Complete_SDE2_SDE3_InterviewPrep.md  ← Code walkthroughs, mock rounds, company prep
│
└── trackers-docs/                        ← Excel trackers + programme documents
    ├── SDE2_Master_Tracker_Jayanti.xlsx
    ├── LLD_Master_Interview_Sheet_v2.xlsx
    ├── System_Design_Master_Interview_Sheet.xlsx
    ├── Java_SpringBoot_Master_Interview_Sheet.xlsx
    ├── DB_OS_CN_Master_Interview_Sheet_v2.xlsx
    ├── Tech_Stack_Skills_Evaluation_Matrix.xlsx
    ├── Project_Experience_Master_Checklist.xlsx
    ├── The_Badass_Senior_Developer_Programme.docx
    └── The_Comeback_Protocol_6Month_Roadmap.docx
```

---

## THE DAILY SYSTEM — How to Use prep.py

### Every Morning (6:00–7:00 AM)

```bash
prep                    # shows today's plan, DSA list, progress bars
```

Pick 1–2 problems from the DSA list shown. Solve on LeetCode. Then:

```bash
prep lc "Problem Name"  # marks it done, updates progress bar
```

### Every Evening (8:00–9:00 PM)

Study the evening topic shown in the plan. Then before bed:

```bash
prep log                # you'll be prompted to type what you did, line by line
                        # blank line to finish. Takes 2 minutes.
```

### Every Sunday Evening

```bash
prep review             # shows your week's performance + specific feedback
prep status             # full dashboard — all 26 weeks, every LeetCode, all applications
```

### When you apply to a company

```bash
prep apply "Razorpay"
```

### When you receive an offer

```bash
prep offer "Razorpay" 32LPA
```

---

## ALL COMMANDS — Reference Card

| Command | What it does |
|---|---|
| `prep` | Today's plan (DSA list, study tasks, progress) |
| `prep plan` | Same as above |
| `prep log` | Log what you did today (interactive, 2 min) |
| `prep status` | Full progress dashboard — all weeks, all stats |
| `prep review` | Weekly feedback with specific improvement actions |
| `prep lc "Name"` | Mark a LeetCode problem as done |
| `prep apply "Co"` | Log a job application |
| `prep offer "Co" CTC` | Log an offer received |
| `prep help` | Show all commands |

---

## THE 6-MONTH PLAN — Big Picture

```
PHASE 1 (Weeks 1–14 | Mar 19 – Jun 19, 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal:   First job offer in hand
Target: Razorpay, Juspay, CRED, MakeMyTrip, Meesho, Paytm,
        Walmart Global Tech, ThoughtWorks, MakeMyTrip
Why:    Removes financial pressure. Gives real interview experience.
        Makes Phase 2 negotiation from strength, not desperation.

Week 1  Resume + LinkedIn + GitHub setup
Week 2  Java Core internals
Week 3  Spring Boot + Hibernate
Week 4  Microservices + Kafka + Redis → FIRST APPLICATIONS
Week 5  Review + Mock Interview 1
Week 6  Low-Level Design (LLD)
Week 7  System Design — mid-tier level
Week 8  Databases + Distributed Systems
Week 9  Cloud + Docker + K8s + Testing
Week 10 Behavioral + Interview Acceleration
Week 11 Full Mock Interview Week
Week 12 Interview Blitz (active interviews)
Week 13 Interview Blitz (refine from feedback)
Week 14 CLOSE FIRST OFFER + negotiate

PHASE 2 (Weeks 15–26 | Jun 19 – Sep 19, 2026)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goal:   Dream offer — top product company
Target: Amazon, Flipkart, Goldman Sachs, PhonePe, Swiggy,
        Google, Microsoft, Uber India, Stripe India
Why:    Armed with Phase 1 offer, you negotiate without desperation.

Week 15–16  DSA serious mode (2 hrs/day) + FAANG system design
Week 17–18  Graphs mastery + Golang + LLD hard mode
Week 19–20  Hard problems mode + Amazon prep
Week 21–22  Goldman + Fintech + Google + Swiggy prep
Week 23–24  Dream applications push + final polish
Week 25–26  CLOSE DREAM OFFER + negotiate
```

Full week-by-week detail: → `MASTER_6MONTH_PROGRAMME.md`

---

## DAILY SCHEDULE

```
Weekdays (2.5 hours minimum)
──────────────────────────────
6:00–7:00 AM    DSA — LeetCode (non-negotiable daily habit)
7:00–7:30 AM    Flashcards — Java/Spring/concept review
8:00–9:00 PM    Evening topic — study from Interview_Answers/ sections

Weekends (5–6 hours)
──────────────────────────────
Morning 3 hrs   System Design practice OR full mock interview round
Afternoon 2 hrs Topic completion + make notes
Evening 1 hr    Run: prep review → plan next week
```

---

## WHAT TO STUDY WHEN — Study Material Map

| Topic | File to read | Questions |
|---|---|---|
| Java Core | `Interview_Answers/Section_01_Java_Core.md` | Q1–Q25 |
| Spring Boot | `Interview_Answers/Section_02_Spring_Boot.md` | Q26–Q60 |
| Hibernate/JPA | `Interview_Answers/Section_03_Hibernate_JPA.md` | Q61–Q90 |
| Microservices + Kafka + Redis | `Interview_Answers/Section_04_05_06_Microservices_Kafka_Redis.md` | Q91–Q135 |
| Database + Distributed Systems | `Interview_Answers/Section_07_08_Database_DistributedSystems.md` | Q136–Q165 |
| Design Patterns + Docker + CI/CD | `Interview_Answers/Section_09_10_11_Patterns_Docker_CICD.md` | Q166–Q210 |
| Cloud + Network + Golang | `Interview_Answers/Section_12_13_14_15_Cloud_Network_Design_Go.md` | Q211–Q250 |
| Testing + Behavioral | `Interview_Answers/Section_16_17_18_19_Testing_Behavioral_Scenarios.md` | Q251–Q296 |
| FAANG Advanced Java | `Interview_Answers/Section_20_FAANG_SDE2_SDE3_Advanced.md` | Extra |
| System Design Deep Dives | `Interview_Answers/Section_21_SystemDesign_DeepDive_With_Answers.md` | Extra |
| GSTN Architecture (your past work) | `Interview_Answers/GSTN_Architecture_Reference.md` | — |
| Code Walkthroughs + Mock Rounds | `Interview_Answers/GSTN_Complete_SDE2_SDE3_InterviewPrep.md` | — |
| All 296 Questions (practice list) | `GSTN_Interview_QuestionBank_296Q.md` | Q1–Q296 |

---

## DSA STRATEGY — How to Build the Habit

### The Rule
```
1 problem per day minimum — no matter what.
Even 1 Easy at 10pm beats 0.
Missing 1 day is allowed. Missing 2 in a row is a pattern. Fix it.
```

### Platform
Use NeetCode.io — follow their roadmap order. It groups problems by pattern.
LeetCode for actual solving (free tier is sufficient).

### How to do a problem right
```
1. Read problem — understand input/output. 5 min.
2. Think out loud before typing. Write edge cases on paper.
3. Attempt solution — set a 35-min timer.
4. If stuck at 20 min: look at the CATEGORY hint (e.g., "sliding window"), not the solution.
5. If stuck at 35 min: read the approach, NOT the code. Then implement yourself.
6. After solving: read the optimal solution. Understand WHY it's better.
7. Mark done: prep lc "Problem Name"
```

### Weekly LeetCode targets
```
Phase 1 (Weeks 1–14):   7 problems/week = 98 total
Phase 2 (Weeks 15–26):  10–14 problems/week = 130+ more

Total target by end: 150+ (quality > quantity)
```

### NeetCode Blind 75 — work through in this order
Full tracker in `MASTER_6MONTH_PROGRAMME.md` → DSA Progress Tracker section.

---

## SYSTEM DESIGN STRATEGY

### The 5-Step Framework (use in EVERY design round)
```
Step 1 (5 min)  — Clarify requirements
                  "Is this for 1M users or 100M users?"
                  "Do we need real-time or eventual consistency?"
                  "Read-heavy or write-heavy?"

Step 2 (3 min)  — Estimate scale
                  "10M users × 10 req/day = 100M req/day = ~1200 RPS"
                  "Each request = 1KB → 100GB/day storage"

Step 3 (5 min)  — High-level components
                  Draw: Client → API Gateway → Services → DB/Cache
                  Name each component. Don't go deep yet.

Step 4 (20 min) — Deep dive on 2-3 critical components
                  Interviewer will pick. You should also propose: "Let me go
                  deep on the Kafka consumer layer — that's the trickiest part."

Step 5 (5 min)  — Failure + monitoring
                  "What happens if the DB goes down?" → Replica failover
                  "How do you know if Kafka is lagging?" → Consumer lag metrics
```

### Must-know designs (practice these end-to-end, on paper, timed)
```
Phase 1 targets:
  1. Rate Limiter (token bucket vs sliding window)
  2. Notification System ← your GSTN CommunicationService
  3. URL Shortener
  4. Job Queue with retry + DLQ ← your Kafka consumer framework

Phase 2 targets:
  5. Twitter/Instagram Feed (fan-out on write vs read)
  6. Google Drive / Dropbox (chunked upload, sync, conflict resolution)
  7. Uber / Swiggy (geospatial, matching, surge)
  8. WhatsApp (WebSocket, ordering, multi-device)
  9. Distributed Rate Limiter (Goldman Sachs favourite)
  10. GST Filing System ← your strongest, most personalized design
```

Full walkthroughs: → `Interview_Answers/Section_21_SystemDesign_DeepDive_With_Answers.md`

---

## LLD STRATEGY

### What LLD rounds test
- Can you model a real-world problem as classes?
- Do you apply SOLID principles naturally?
- Do you know design patterns and use them where appropriate?

### Patterns you must know cold
```
Strategy     → your CaseCustomizerFactory at GSTN (best real example)
Factory      → CaseCustomizerFactory
Observer     → Kafka producers/consumers
Builder      → Building complex request/response objects
Template Method → your Consumer.java base class (abstract + concrete)
Singleton    → Spring beans
Decorator    → Adding logging/metrics to existing classes
```

### LLD problems to practice (in order)
```
Phase 1 (weeks 6–10):
  1. Parking Lot
  2. Vending Machine
  3. Library Management System

Phase 2 (weeks 17–18):
  4. Elevator System
  5. Chess Game
  6. Hotel Booking (Booking.com style)
  7. Food Delivery App (Swiggy LLD)
  8. LRU Cache (implement in code — MUST MEMORIZE)
  9. Pub-Sub System ← map to your Kafka framework
```

Practice resource: → `trackers-docs/LLD_Master_Interview_Sheet_v2.xlsx`

---

## BEHAVIORAL STRATEGY

### Your 6 Must-Have STAR Stories

Prepare all of these fully written out. 2 minutes each. Specific. Numbers.

```
1. Most complex technical problem
   → XA transaction consistency across Appeal + Ledger + Notification at GSTN
   → "3 services, 1 distributed transaction, Atomikos JTA, ACID compliance at scale"

2. Worked under extreme pressure / deadline
   → GST peak filing deadline (July 31 every year, 14M filers, system at 10x load)
   → "We had 6 hours to fix X before the filing window opened"

3. Disagreed with team or manager
   → A technical decision you pushed back on and why
   → What happened, what you learned

4. Led without formal authority
   → Drove adoption of a pattern/framework across teams
   → "I proposed the DLQ retry pattern — other teams adopted it"

5. Production incident you caused (or were part of)
   → Specific: what broke, what you did, what you fixed, what you changed after
   → Showing ownership and learning > showing perfection

6. Mentored or helped someone grow
   → Even informal: "I reviewed PRs for junior developers, ran knowledge sessions"
```

For Amazon: map these to Leadership Principles.
Full mapping: → `Interview_Answers/GSTN_Complete_SDE2_SDE3_InterviewPrep.md` Part 5.1

---

## COMPANY TARGETING — Who to Apply and When

### Phase 1 (apply starting Week 4)
See full list: → `COMPANY_ANALYSIS.md` → Tier 3 section

Quick list:
```
Razorpay, Juspay, CRED, MakeMyTrip, Meesho, Paytm, Slice,
Walmart Global Tech, ThoughtWorks, Publicis Sapient, Nagarro,
Atlassian, Freshworks, Browserstack, Persistent Systems
```

### Phase 2 (apply starting Week 23)
```
Amazon, Flipkart, Goldman Sachs, Morgan Stanley,
PhonePe, Swiggy, Zomato, Uber India, Google, Microsoft,
Zerodha, Stripe India
```

Full analysis of each: → `COMPANY_ANALYSIS.md`

---

## RESUME + LINKEDIN — Quick Reference

Full guide: → `LINKEDIN_RESUME_GUIDE.md`

### LinkedIn headline (copy this)
```
Backend Engineer | Java · Spring Boot · Kafka · Redis · Microservices | 5.5 YOE | Open to SDE-2/SDE-3
```

### Resume bullet formula
```
[Action verb] [what you built] [technology] → [metric impact]

Example:
"Designed JBoss DataGrid + EhCache layer across 45+ microservices,
 reducing DB load ~40% during peak filing season (14M taxpayers)"
```

### Referral message template (gets 3–4x callback rate)
```
Hi [Name],
I'm Jayanti Vishnoi, a backend engineer with 5.5 YOE in Java/Kafka
distributed systems at GSTN. I'm exploring SDE-2/SDE-3 backend roles and
[Company] is my top choice. Would you be open to referring me?
Happy to share my resume. No pressure at all.
— Jayanti
```

---

## WHAT GETS PEOPLE REJECTED — The Honest List

```
DSA round:      Cannot code BFS/DFS from scratch. Brute force only.
                Cannot explain time/space complexity. Off-by-one errors.
→ Fix: 1 problem daily. Pattern recognition > memorisation.

System Design: Jumps to solution without clarifying requirements.
               Describes components but cannot explain WHY.
               Cannot do back-of-envelope estimation.
→ Fix: 5-step framework every single time. Practice on paper.

Java round:    Cannot explain their OWN code when probed.
               Knows @Transactional works, cannot explain JVM proxy mechanism.
               Good theory but cannot write working Kafka consumer from memory.
→ Fix: Explain every concept as if teaching a junior. Write code, don't just read.

Behavioral:    Vague stories ("we built a system"). No numbers.
               Everything went smoothly — no challenge (unbelievable).
               No "I" statements — only "we".
→ Fix: Every story: Situation → YOUR specific action → Measurable result.
```

---

## WEEKLY RHYTHM — What to Do Each Day of the Week

```
Monday      Morning DSA (new problem) + Evening: new week's topic, first 30 min
Tuesday     Morning DSA + Evening: deep dive on same topic (code examples)
Wednesday   Morning DSA + Evening: practice questions Q&A from question bank
Thursday    Morning DSA + Evening: system design or LLD practice
Friday      Morning DSA + Evening: weak area review (what you couldn't answer Tue/Wed)
Saturday    3-hr block: full system design OR mock interview round (recorded)
Sunday      2-hr block: 2 DSA problems + prep review → plan next week
```

---

## MENTAL PROTOCOLS — How People Actually Crack These Interviews

### The discipline loop
```
1. Show up daily (DSA). Not 90%, not when motivated — daily.
2. Log it (prep log). Makes it real. Makes skipping uncomfortable.
3. Apply early. Real interviews > mock interviews. Apply from Week 4.
4. Iterate from feedback. After each interview, log all questions. Fix gaps.
5. Don't change strategy mid-course. Trust the plan.
```

### When you fail an interview
```
Within 1 hour of finishing: write every question you were asked.
Within 24 hours: identify which questions you stumbled on.
Within 48 hours: study those specific gaps. Not general review — targeted.
Week after: do a mock on those exact topics.
```

### When you feel like giving up
```
This is normal. It happens around Week 3-4 (pre-application anxiety)
and around Week 8-9 (interview fatigue).

What actually helps:
  → Run: prep status — see your progress bars. You ARE moving forward.
  → Do 1 Easy LeetCode problem. Just one. The momentum returns.
  → Read your STAR stories. Remind yourself what you've built.
  → Remember: you're not starting from zero. 5.5 years at GSTN is real.
    You're bridging from government infra to product engineering — that's it.
```

### The compound effect
```
Day 1:    0 problems. 0 applications.
Day 30:   30 problems. 10 applications. 2 interviews done.
Day 60:   70 problems. 25 applications. 8 interviews. 1 offer.
Day 90:   100 problems. 35 applications. 15 interviews. 1-2 offers.
Day 120:  130 problems. 45 applications. FAANG final rounds starting.
Day 180:  150+ problems. 60 applications. Dream offer signed.

The gap between people who crack it and those who don't:
Not talent. Not intelligence. Just showing up every day.
```

---

## QUICK TROUBLESHOOTING

### "I'm not getting callbacks"
- Callback rate < 15% → Resume issue. Fix it before applying more.
- Check: Are keywords matching the job description?
- Check: Do you have impact numbers in every bullet?
- Action: Revise resume → `LINKEDIN_RESUME_GUIDE.md` → apply 5 more immediately.

### "I'm getting calls but failing early rounds (DSA)"
- Diagnosis: DSA needs more work.
- Action: Increase to 2 problems/day. Focus on the failing pattern (trees? graphs? DP?).
- Do NOT delay applications — apply while improving.

### "I'm reaching final rounds but not getting offers"
- Diagnosis: System design OR behavioral is weak.
- Action: Record yourself doing 1 system design. Watch it back. Fix what looks unclear.
- Action: Do your STAR stories aloud with a friend. Vagueness will be obvious.

### "I got an offer but it's below my expectation"
- Never accept same day. "I'm very excited — can I have 48 hours?"
- Research: Glassdoor, Levels.fyi for that exact role.
- Counter with: "I was targeting [X]. Is there flexibility?"
- Even a 10% counter is worth doing — worst they say is no.

---

## VERSION HISTORY
```
v1.0 — March 19, 2026 — System created. Day 1.
```

*Update this after every major milestone: first callback, first offer, first FAANG round, final offer.*

---

> "You don't rise to the level of your goals. You fall to the level of your systems."
> — James Clear, Atomic Habits
>
> Your system is now built. Run it daily.
