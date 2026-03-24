# Jayanti Vishnoi — 6-Month SDE-2/SDE-3 Offer Programme
# Start Date: March 2026 | Phase 1 Deadline: June 2026 | Phase 2 Deadline: September 2026
# Profile: 5.5 YOE | GSTN | Java, Spring Boot, Kafka, Redis, MySQL, Golang, Docker, K8s

---

## THE TWO-PHASE STRATEGY

```
PHASE 1 (Month 1–3):  First Offer
  ↳ Target: Mid-tier product companies (Razorpay, Juspay, CRED, Meesho,
            Paytm, Slice, MakeMyTrip, Atlassian, ThoughtWorks SDE-2)
  ↳ Goal:   Get an offer on the table. Real interview experience.
            Build confidence. Get financially safe.

PHASE 2 (Month 4–6): Dream Offer
  ↳ Target: Flipkart, Amazon, Google, Goldman Sachs, PhonePe, Swiggy,
            Zerodha, Stripe (India), Microsoft, Uber India
  ↳ Goal:   Armed with Phase 1 offer, negotiate hard. No desperation.
            Crack top-tier with full prep.
```

**The Logic:** Phase 1 offer removes financial pressure and gives you
real interview data. Phase 2 is where you go for the kill.

---

## DAILY TIME COMMITMENT

```
Weekdays:  2.5 hours minimum
  - 6:00–7:00 AM  → DSA (LeetCode — non-negotiable daily)
  - 7:00–7:30 AM  → Flashcard review (Java/Spring/concepts)
  - Evening 8:00–9:00 PM → Topic deep dive (Java, System Design, LLD)

Weekends:  5–6 hours
  - Morning 3 hrs → System Design or Mock Interview
  - Afternoon 2 hrs → Topic completion + notes
  - Evening 1 hr → Week review, next week planning
```

---

# ═══════════════════════════════════════════════════════════════
# PHASE 1 — MONTH 1: FOUNDATION & POSITIONING
# March 19 – April 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 1 GOAL
Resume is battle-ready. LinkedIn is optimized. Java/Spring internals are
solid. First applications are out. 20 LeetCode Easy problems done.

---

## WEEK 1 (Mar 19–25): Resume + Profile

### Deliverables
- [ ] Final resume (1 page, impact-driven, ATS-optimized)
- [ ] LinkedIn: Headline updated, About section, 3 project descriptions
- [ ] GitHub: At least 1 project with README (use existing project ideas from Part 10)

### Resume — Top 6 Bullets (already drafted in GSTN_Complete guide — Part 2)
Pull from there. Key formula: **[Action Verb] [What You Did] → [Metric Impact]**

Example bullet (already written):
> "Designed distributed cache layer (JBoss DataGrid + EhCache) reducing DB load by
> 40% across 45+ microservices serving 14M taxpayers"

### LinkedIn Optimization
- Headline: "Backend Engineer | Java · Spring Boot · Kafka · Redis | 5.5 YOE | Open to SDE-2/SDE-3"
- Open to Work: ON (visible to recruiters only)
- Add: All GSTN projects, tech stack keywords in skills section

### GitHub — Start Project 3 (Kafka Event Pipeline with DLQ)
This is the highest signal project. Tech: Spring Boot 3, Kafka, Docker Compose.
Reference: Part 10 → Project 3 in GSTN_Complete guide.
Even a skeleton with good README is fine this week.

### DSA — Week 1
- LeetCode target: 7 Easy problems
- Topics: Arrays, Strings (Two Sum, Valid Anagram, Contains Duplicate, etc.)
- Platform tip: NeetCode.io — follow their roadmap
- ⚠️ **SWITCH TO JAVA NOW**: You have 155 problems done but 151 in C++, only 4 in Java.
  Apple/Oracle/Amazon/DoorDash all ask Java-specific questions in the same rounds.
  From Week 1 onwards — solve ALL LeetCode problems in Java only.

### Priority P0 Problems (from Real Interview Data — do these first)
These appeared in actual Apple/Oracle/Amazon/DoorDash interviews:
- LRU Cache (LC #146) — Apple Screening. Must know by heart.
- Trapping Rain Water (LC #42) — Amazon Round 4
- Task Scheduler (LC #621) — Oracle Round 2
- First Missing Positive (LC #41) — Amazon Round 3
- Evaluate Reverse Polish Notation (LC #150) — Amazon Round 3
- Container With Most Water (LC #11) — Oracle Screening
- Longest Common Prefix (LC #14) — Apple Round 1
- BFS grid problems (multi-source BFS) — DoorDash Round 3

---

## WEEK 2 (Mar 26–Apr 1): Java Core Internals

### Study Material
→ `Interview_Answers/Section_01_Java_Core.md` — Read fully, mark gaps
→ `GSTN_Interview_QuestionBank_296Q.md` — Q1–Q25

### Must-Master This Week
- HashMap internals (treeify at 8, untreeify at 6, load factor 0.75)
- ConcurrentHashMap segments → CAS in Java 8
- Thread lifecycle, ThreadPool types, ExecutorService
- CompletableFuture — thenApply, thenCompose, allOf, exceptionally
- GC types: G1GC vs ZGC vs Serial/Parallel — which for low-latency?
- JVM memory: Young Gen / Old Gen / Metaspace / Stack
- Java 8+ features: Streams, Optional, Functional interfaces

### Practice
- Write code for: Custom ThreadPool, CompletableFuture parallel API calls
- Explain your Kafka consumer code from GSTN in terms of Java concurrency

### DSA — Week 2
- LeetCode target: 7 Easy problems
- Topics: Two Pointers, Sliding Window basics
- ⚠️ **Read first**: `Interview_Answers/Section_DSA_Java_Patterns.md` — Section 1 (C++ → Java translation) + Section 2 (Pattern Templates for Two Pointers + Sliding Window)
- Reference this every time you start a new problem pattern in Java

---

## WEEK 3 (Apr 2–8): Spring Boot + Hibernate + LLD Introduction

### Study Material
→ `Interview_Answers/Section_02_Spring_Boot.md` — Full read
→ `Interview_Answers/Section_03_Hibernate_JPA.md` — Full read
→ `GSTN_Interview_QuestionBank_296Q.md` — Q26–Q80

### Must-Master This Week

**Spring Boot:**
- Auto-configuration: @ConditionalOnClass, spring.factories, @EnableAutoConfiguration
- Bean lifecycle: @PostConstruct, @PreDestroy, init-method
- @Transactional internals: proxy, propagation (REQUIRED, REQUIRES_NEW, NESTED)
- @Async: how it works, ThreadPoolTaskExecutor config
- Spring Security filter chain (if asked)
- Actuator endpoints, custom health indicators

**Hibernate:**
- N+1 problem — how it happens, how to fix (JOIN FETCH, @BatchSize)
- 1st level cache (Session) vs 2nd level cache (EhCache) — you used this at GSTN
- Dirty checking, flush modes
- @Transactional rollback rules
- Connection pool (HikariCP) — maxPoolSize, connectionTimeout

### Your GSTN Angle
→ Reference `GSTN_Complete guide Part 1` — AppealTranCaseCustomizer, WFServiceImpl
→ Be able to explain: "In GSTN we used @Transactional(propagation=REQUIRES_NEW) for
   ledger operations because..." — this is gold in interviews

### LLD — Week 3 (Introduction — DO NOT SKIP)
⚠️ Phase 1 companies (Razorpay, CRED, Juspay) have LLD in Round 1 or 2. Starting now, not Week 6.

→ `Interview_Answers/Section_LLD_Complete.md` — Read Section 1 (45-min framework) + Section 2 (SOLID with code)
- Learn the LLD interview framework: Requirements → Entities → Interfaces → Core Classes → Edge Cases
- Do 1 SOLID principle per day (5 days, one each)
- **LLD Problem 1 this week**: Design a Parking Lot — full solution with Java code (Section_LLD_Complete.md Problem 1)

### DSA — Week 3
- LeetCode target: 7 Easy problems
- Topics: HashMap problems, Linked Lists

---

## WEEK 4 (Apr 9–15): Microservices + System Design Basics + First Applications

### Study Material
→ `Interview_Answers/Section_04_05_06_Microservices_Kafka_Redis.md` — Full read
→ `Interview_Answers/GSTN_Architecture_Reference.md` — Sections 1–7

### Must-Master This Week

**Microservices:**
- Service discovery (Eureka), API Gateway patterns
- Circuit breaker (Resilience4j) — states: CLOSED/OPEN/HALF-OPEN
- Saga pattern (Choreography vs Orchestration) — how GSTN appeal flow maps to this
- **CQRS pattern** — Command Query Responsibility Segregation, read/write model separation
  → Apple screening asked this directly. Frame using GSTN GSTR-2A query optimization as example.
- Distributed tracing (Sleuth + Zipkin)
- Idempotency — why it matters, how you implemented it

**Kafka:**
- Producer: acks=all, idempotent producer, retries
- Consumer: offset commit (auto vs manual), consumer groups, rebalancing
- Partitioning strategy — key-based vs round-robin
- Exactly-once: transactional API (you have a deep dive doc for this)
- DLQ pattern — your Consumer.java implements this

**Redis:**
- Data structures: String, Hash, List, Set, ZSet — use cases for each
- Cache-aside vs write-through vs write-behind
- Redis Cluster vs Sentinel
- Distributed locking: SET key value NX EX (vs Redisson)
- Your DistCacheUtil — explain its internal design

### First Applications — Start Now
- Apply to 5–10 companies this week (Razorpay, Juspay, CRED, MakeMyTrip, ThoughtWorks)
- Use LinkedIn Easy Apply + company career pages
- Target: roles with Java + Spring Boot + Microservices

### LLD — Week 4
→ `Interview_Answers/Section_LLD_Complete.md`
- **LLD Problem 2**: Design a Vending Machine (State pattern — Section_LLD_Complete.md Problem 2)
- **LLD Problem 3**: Design Elevator System (Section_LLD_Complete.md Problem 3)
- Practice: code both from memory after reading solution once

### DP — Week 4 (Moved EARLY — Phase 1 companies ask DP)
⚠️ DP was in Week 7/Phase 2 before — that was too late. CRED, Meesho, Swiggy ask DP in Phase 1.
→ `Interview_Answers/Section_DSA_Java_Patterns.md` — Section 3 (DP Complete Guide)
- Read: DP Recognition Framework + "4 questions before writing any DP"
- Solve: Climbing Stairs, Coin Change (minimum), House Robber — all in Java
- Template to internalize: top-down memoization skeleton in Java

### DSA — Week 4
- LeetCode target: 7 Easy problems
- Topics: Stack, Queue, Binary Search

---

## WEEK 5 (Apr 16–19): Review + Mock Interview 1 + Momentum

### Deliverables
- [ ] 28 LeetCode Easy problems done (4 weeks × 7)
- [ ] 5–10 applications out
- [ ] GitHub project has skeleton + README
- [ ] Can speak for 45 mins on GSTN architecture without notes

### Mock Interview 1 (Self or with a friend)
Do Round 4 from the mock interview section in GSTN_Complete guide:
"Past Work Deep Dive" — explain your top 3 contributions from GSTN.
Time yourself. Record if possible.

---

# ═══════════════════════════════════════════════════════════════
# PHASE 1 — MONTH 2: INTERVIEW MODE
# April 19 – May 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 2 GOAL
Active interviewing. 20+ applications. Real feedback from 3–5 interviews.
LLD basics solid. System Design: can handle mid-tier company problems.
30 more LeetCode done (mix Easy/Medium).

---

## WEEK 6 (Apr 19–25): LLD Deep Practice + Design Patterns

### You've Already Done
- Parking Lot (Week 3), Vending Machine + Elevator (Week 4)
- SOLID principles (Week 3)
This week is about fluency — doing problems from scratch without looking at solutions.

### LLD Practice (Do 2 this week — blind, no reference)
1. **BookMyShow Ticket Booking** — concurrency, seat locking, race conditions (Section_LLD_Complete.md Problem 4)
2. **LRU Cache** — LinkedHashMap approach + doubly linked list approach, thread-safe version (Section_LLD_Complete.md Problem 5)

### Design Patterns Deep Dive
→ `Interview_Answers/Section_LLD_Complete.md` — Section 4 (Patterns Quick Reference)
- Strategy (your GSTN CaseCustomizerFactory — your best story)
- Factory / Abstract Factory
- Observer / Event-Driven (your Kafka consumers)
- Builder, Singleton, Decorator, Template Method, Command, Proxy
- For each: know the trigger phrase ("When interviewer says X, I use Y pattern")

### SDE-3 LLD Bar
→ `Interview_Answers/Section_LLD_Complete.md` — Section 5
- What extra is expected at SDE-3: extensibility reasoning, SOLID violation detection, trade-off discussion
- Practice: explain *why* you chose each pattern, not just what you chose

### DSA — Week 6
- LeetCode: 7 problems (mix Easy/Medium)
- Topics: Trees (Inorder, Preorder, Level-order BFS)

---

## WEEK 7 (Apr 26–May 2): System Design — Mid-Tier Level

### What Mid-Tier Companies Ask
- URL Shortener, Rate Limiter, Notification System, Job Scheduler
- They do NOT expect Google-scale. They want clean thinking + trade-offs.

### Study Material
→ `Interview_Answers/Section_21_SystemDesign_DeepDive_With_Answers.md`
→ `Interview_Answers/GSTN_Architecture_Reference.md` — Sections 8–20
→ GSTN_Complete guide Part 9 — Design 1 (GST Filing System) — your strongest design

### Framework for Every System Design Answer
```
1. Clarify requirements (functional + non-functional) — 5 min
2. Estimate scale (users, RPS, storage) — 3 min
3. High-level components — 5 min
4. Deep dive on 2-3 critical components — 20 min
5. Address: scaling, failure, monitoring — 5 min
```

### Must-Know Designs (Mid-Tier Level)
1. Rate Limiter (token bucket vs sliding window)
2. Notification System (your strongest — you built this at GSTN)
3. URL Shortener (hashing, redirection, analytics)
4. Job/Task Scheduler (distributed, retry, DLQ)
5. Key-Value Store (consistent hashing, replication)

### Consumer Product System Designs (NEW — Phase 2 gap closed early)
→ `Interview_Answers/Section_SD_Consumer_Products.md`
- Read: Twitter/Instagram Feed design (fan-out on write vs read, celebrity problem)
- Read: The "Which DB?" and "Which messaging system?" decision trees — memorize these
- Practice: draw Twitter Feed design end-to-end on paper, explain aloud in 45 min

### DSA — Week 7
- LeetCode: 7 problems (Medium)
- Topics: DP Medium — LCS, 0/1 Knapsack, Word Break
- → `Interview_Answers/Section_DSA_Java_Patterns.md` Section 3 — follow the DP problem list

---

## WEEK 8 (May 3–9): Databases + Distributed Systems (Deep)

### Study Material
→ `Interview_Answers/Section_07_08_Database_DistributedSystems.md` — Full read
→ `Interview_Answers/Section_Behavioral_DB_Golang.md` — Part 2 (DB Deep Dive — NEW)
→ `GSTN_Interview_QuestionBank_296Q.md` — Q136–Q200

### Must-Master This Week

**Database (SDE-3 depth — from Section_Behavioral_DB_Golang.md Part 2):**
- EXPLAIN / EXPLAIN ANALYZE — how to read query execution plans
- Index design: B-tree internals, composite index leftmost prefix rule, covering index
- Isolation levels deep: what each prevents (dirty read, non-repeatable read, phantom read)
- MySQL MVCC — how InnoDB achieves non-blocking reads
- Window functions: ROW_NUMBER, RANK, LAG, LEAD — practical examples
- Deadlock detection and how to resolve

**Distributed Systems:**
- Consistency models: Strong, Eventual, Causal
- Consensus: Raft vs Paxos (conceptual level)
- Leader election, split brain problem
- Distributed locking — Redlock, ZooKeeper
- Clock synchronization — Lamport timestamps

**Your GSTN Angle:**
- HBase row key design (GSTIN|Period|ReturnType) — this is a great example
- MySQL for ACID ledger vs HBase for petabyte-scale filing data — trade-off explained
- XA transactions with Atomikos — how distributed transactions work (you built this)

### Modern Java + Observability (NEW — 2025-2026 Hiring Trend)
→ `Interview_Answers/Section_Modern_Java_Observability_CQRS.md` — Part 1 + Part 2
- Java 17-21: Records, Sealed Classes, Pattern Matching, Virtual Threads (Project Loom)
- Spring Boot 3.x: Micrometer, Observability, Security 6
- These questions are now asked at Flipkart, Swiggy, Stripe even at SDE-2 level

### CQRS + Event Sourcing (Apple asked this — still open gap)
→ `Interview_Answers/Section_Modern_Java_Observability_CQRS.md` — Part 4
- Read CQRS section + Event Sourcing section
- Map to GSTN: "GSTR-2A query optimization as CQRS read model"

### DSA — Week 8
- LeetCode: 7 problems (Medium)
- Topics: Graphs (BFS/DFS), basic traversal
- → `Interview_Answers/Section_DSA_Java_Patterns.md` Section 4 — Graph algorithms in Java

---

## WEEK 9 (May 10–16): Cloud + Docker/K8s + Testing + Observability

### Study Material
→ `Interview_Answers/Section_09_10_11_Patterns_Docker_CICD.md`
→ `Interview_Answers/Section_12_13_14_15_Cloud_Network_Design_Go.md`
→ `Interview_Answers/Section_16_17_18_19_Testing_Behavioral_Scenarios.md`
→ `Interview_Answers/Section_Modern_Java_Observability_CQRS.md` — Part 3 (Observability)

### Must-Master This Week
- Docker: image vs container, layers, multi-stage builds
- Kubernetes: Pod, Deployment, Service, ConfigMap, HPA
- CI/CD pipeline stages: build → test → dockerize → deploy
- AWS core: EC2, S3, RDS, ElasticCache, SQS/SNS, Lambda
- Testing: Unit (JUnit + Mockito), Integration, Contract (Pact)
- **Observability (NEW — asked at SDE-3)**: SLIs/SLOs/SLAs, RED method, distributed tracing, OpenTelemetry
  - Must be able to answer: "Your API is slow. Walk me through how you'd diagnose it."
  - Structured answer: Metrics → Traces → Logs → EXPLAIN query → Thread dump
- Golang basics: goroutines, channels, context package
  → `Interview_Answers/Section_Behavioral_DB_Golang.md` — Part 3 (Go section)

### DSA — Week 9
- LeetCode: 7 problems (Medium)
- Topics: Heap / Priority Queue

---

## WEEK 10 (May 17–19): Behavioral + Interview Acceleration

### Behavioral Prep
→ `Interview_Answers/Section_16_17_18_19_Testing_Behavioral_Scenarios.md`
→ `Interview_Answers/Section_Behavioral_DB_Golang.md` — Part 1 (Non-Amazon behavioral)
→ `Interview_Answers/Amazon_LP_STAR_Bank.md` — Amazon LP format

### Must-Have STAR Stories (prepare all of these — use STARL format)
1. **Most complex problem you solved** → XA transaction / ledger consistency at GSTN
2. **Disagreed with team/manager** → technical decision you pushed back on
3. **Worked under pressure** → deadline during GST peak filing season
4. **Led without authority** → drove adoption of a new pattern across teams
5. **Failed and learned** → a production incident, what you did
6. **Mentored someone** → even if informal

### SDE-3 Behavioral Questions (Prepare These Too)
→ `Interview_Answers/Section_Behavioral_DB_Golang.md` — Section: SDE-3 Behavioral Questions
- "How have you mentored junior engineers?"
- "Describe a system you designed that influenced the whole org"
- "When did you push back on a leadership/product decision?"
- "How do you handle tech debt vs feature velocity?"

### Company-Specific "Why this company?" Answers
→ `Interview_Answers/Section_Behavioral_DB_Golang.md` — Section: Company-Specific Angles
- Prepare one genuine answer per company you're interviewing at this week

### Applications Push
- By end of Week 10: 25+ applications out
- Follow up on all applications from Month 1
- If you have any referrals — use them now

---

# ═══════════════════════════════════════════════════════════════
# PHASE 1 — MONTH 3: CLOSE FIRST OFFER
# May 19 – June 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 3 GOAL
At least 1 offer in hand by June 19. Use real interview feedback to sharpen.
Target: 3–5 final round interviews happening this month.

---

## WEEK 11 (May 19–25): Full Mock Interview Week

### Do All 5 Rounds from GSTN_Complete Guide Part 3
1. Round 1: Java Deep Dive — time it (45 min)
2. Round 2: Spring Boot + Microservices — time it
3. Round 3: System Design — pick one from your must-know list
4. Round 4: Past Work Deep Dive — your GSTN stories
5. Round 5: Behavioral + Managerial — STAR stories

**Do these with someone if possible.** If not, record yourself on camera.
Review and identify the 3 weakest areas. Fix them this week.

### DSA — Week 11
- LeetCode: 7 problems (Medium/Hard)
- Topics: Backtracking, recursion

---

## WEEK 12–13 (May 26–Jun 8): Interview Blitz + Refinement

### Focus
- You should be in active interviews now
- After each interview: write down every question asked within 1 hour
- Identify patterns — what are you being asked repeatedly?
- Shore up any gaps immediately

### Common Feedback at This Stage (and how to fix)
| Feedback | Fix |
|---|---|
| "DSA was weak" | Add 30 min more daily, focus NeetCode Blind 75 |
| "System design unclear" | Use the framework religiously, practice drawing on paper |
| "Java not deep enough" | Review JVM internals, practice explaining GC verbally |
| "Didn't ask good questions" | Prepare 5 smart questions for every company |

### Offer Negotiation Prep (Start Now, Don't Wait)
- Know your target CTC: Base, Variable, Equity, Joining Bonus
- Research: Glassdoor, Levels.fyi, LinkedIn Salary for SDE-2/SDE-3 roles
- Never accept on the spot. Always say: "I'm very excited. Can I have 48 hours?"
- Counter-offer is always appropriate at this level

---

## WEEK 14 (Jun 9–15): Offer Close

### If No Offer Yet
- Expand target list: add service companies (Thoughtworks, Walmart Global Tech,
  Publicis Sapient, Nagarro) — they pay well and have good engineering culture
- Check: Is your resume getting callbacks? (If <20% → fix resume)
  OR: Are you getting to rounds but failing? (If yes → identify which round)

### If Offer Received
- Evaluate: CTC, tech stack, team, product, growth potential
- Negotiate — even 10–15% is reasonable to ask for
- Accept only if it meets your minimum bar
- **Do NOT stop Phase 2 prep after accepting**

---

# ═══════════════════════════════════════════════════════════════
# PHASE 2 — MONTH 4: BRIDGE & ELEVATE
# June 19 – July 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 4 GOAL
Phase 1 offer accepted (or in hand). Shift gear completely.
Now prep for FAANG/top-product. DSA goes hard. System Design goes deep.

---

## WEEK 15–16 (Jun 19–Jul 2): DSA Serious Mode

### From this point: 2 hours DSA daily (not 1 hour)
- Morning: 1 problem (timed, 35 min, then review)
- Evening: 1 problem (blind, no hints)

### NeetCode Blind 75 — Track Progress
By end of Phase 2 you must have done all 75 + NeetCode 150 additions.

### Week 15: Arrays, Strings, Sliding Window, Two Pointers
### Week 16: Binary Search, Linked List, Trees

### System Design Deep Dive — FAANG Level
→ `Interview_Answers/Section_21_SystemDesign_DeepDive_With_Answers.md`
→ `Interview_Answers/Section_20_FAANG_SDE2_SDE3_Advanced.md`

FAANG-level designs to master (all 4 are now fully written out):
→ `Interview_Answers/Section_SD_Consumer_Products.md` — full answers for all 4
1. Design Twitter / Instagram Feed (fan-out on write vs read, celebrity problem, ranking)
2. Design Google Drive / Dropbox (chunked upload, deduplication, sync conflict)
3. Design WhatsApp (WebSocket, message delivery guarantees, group chat, E2E encryption)
4. Design Uber / OLA (geospatial indexing — QuadTree vs Geohash, driver matching, surge)
5. Design your own: GST Return Filing System (you can nail this — already in Section_21)

Also reference the decision trees in Section_SD_Consumer_Products.md:
- "Which DB?" decision tree (SQL vs NoSQL, Cassandra vs MongoDB vs Redis)
- "Which messaging system?" (Kafka vs RabbitMQ vs SQS vs Redis Pub/Sub)
- "Which cache strategy?" (read-through vs write-through vs cache-aside)

---

## WEEK 17–18 (Jul 3–19): LLD Serious Mode + Golang

### LLD Practice (By now you've done 5 problems in Phase 1 — these are Phase 2 additions)
→ `Interview_Answers/Section_LLD_Complete.md` for reference if needed
1. Design a Chess Game (from scratch, 45-min timer)
2. Design Food Delivery App — Swiggy/Zomato LLD
3. Design Pub-Sub system (your Kafka knowledge shines here)
4. Design a Rate Limiter (token bucket implementation in Java)
5. Design Hotel Booking (Booking.com LLD — concurrency + availability)

### Golang Deep Dive (Important for Google/Uber/Swiggy/Zerodha)
→ `Interview_Answers/Section_Behavioral_DB_Golang.md` — Part 3 (Golang full section)
- Goroutines vs OS threads — the fundamental difference
- Channels: buffered vs unbuffered, select multiplexing
- Context package: WithCancel, WithTimeout, WithDeadline — propagation pattern
- sync package: Mutex, RWMutex, WaitGroup, Once, atomic
- Error handling: errors.Is, errors.As, %w wrapping, custom error types
- HTTP service in Go — middleware pattern, simple CRUD API
- Goroutine leak prevention — the most common Go interview trap
- Go Memory Model + race detector (-race flag)

---

# ═══════════════════════════════════════════════════════════════
# PHASE 2 — MONTH 5: FAANG FULL PREP
# July 19 – August 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 5 GOAL
Can clear DSA round at Amazon/Flipkart (Medium-Hard problems).
System Design at FAANG level. Behavioral: 10 STAR stories ready.

---

## WEEK 19–20 (Jul 19–Aug 2): DSA Hard Mode

### NeetCode 150 — Remaining Topics
- Graphs: Dijkstra, Topological Sort, Union-Find
- DP: 0/1 Knapsack, Longest Common Subsequence, Edit Distance
- Heap: Top-K, Merge K sorted lists
- String: KMP, Rabin-Karp (conceptual — rarely asked to implement)

### Daily Cadence
- 1 hard problem (45 min, then review answer)
- 1 medium problem (25 min, no hints)
- Weekly contest on LeetCode (Saturday)

---

## WEEK 21–22 (Aug 3–19): Company-Specific Prep

### Amazon
→ `Interview_Answers/Amazon_LP_STAR_Bank.md` — **USE THIS** (22 GSTN STAR stories, all 14 LPs covered)
- ⚠️ EVERY Amazon round has 2 LP questions. Bar Raiser = dedicated behavioral round.
- Practice: 2 stories per LP out loud with a timer (2 min each)
- Focus LPs: Customer Obsession, Ownership, Deliver Results, Dive Deep, Invent & Simplify
- Real DSA asked: Trapping Rain Water, First Missing Positive, Evaluate RPN, BFS file path
- Real System Design asked: Multi-broker portfolio platform (schema + JSON design)
- Each round ends with 2 LP questions — prepare them as warmup, not afterthought

### Flipkart
- Java heavy — they will go very deep on concurrency, GC tuning
- System Design: Product catalog, inventory management, flash sale system
- Behavioral: How do you handle scale? Product mindset questions.

### Goldman Sachs / Morgan Stanley
→ `GSTN_Complete guide Part 5.4`
- Java deepest — expect JVM internals, lock internals, GC tuning
- No system design. 3–4 coding rounds.
- Financial domain: you have GSTN ledger experience — USE IT
- Concurrency: they love asking about thread-safe data structures

### PhonePe / Razorpay (Fintech)
- Payments domain aligns perfectly with your GSTN tax/ledger experience
- Idempotency, distributed transactions, audit trails — you built all this
- Ask about their tech stack before interview, tailor your answers

### Swiggy / Zomato / Meesho (Product)
- Product thinking expected: "How would you improve X?"
- System design: real-time order tracking, surge pricing, recommendation engine
- Culture: fast-paced, startup mentality questions

---

# ═══════════════════════════════════════════════════════════════
# PHASE 2 — MONTH 6: CLOSE DREAM OFFER
# August 19 – September 19, 2026
# ═══════════════════════════════════════════════════════════════

## MONTH 6 GOAL
3+ final rounds at dream companies. 1 offer from FAANG/top-product by Sep 19.

---

## WEEK 23–24 (Aug 19–Sep 2): Final Polish + Applications

### Applications Push (Dream Companies)
- Apply to: Amazon, Flipkart, Goldman Sachs, PhonePe, Swiggy, Google, Microsoft
- Use employee referrals wherever possible (LinkedIn → find GSTN alumni)
- Referrals double callback rates — spend 1 week getting them

### Final Polish Areas
- [ ] DSA: NeetCode 150 completion check — redo all failed problems
- [ ] System Design: Draw each design on paper (3 full designs end-to-end)
- [ ] Behavioral: Practice all 10 STAR stories aloud — not just in your head
- [ ] Java: Reread JVM internals + concurrency (Section 20 FAANG doc)
- [ ] GitHub: Kafka Pipeline project should be complete and polished

---

## WEEK 25–26 (Sep 3–19): Dream Offer Close

### Negotiation at FAANG/Top-Product Level
- FAANG offers are: Base + RSU (vesting over 4 years) + Annual Bonus + Joining Bonus
- Reference: Levels.fyi for exact ranges for your YOE
- Negotiate RSU cliff, joining bonus, and title (SDE-2 vs SDE-3 matters)
- Get competing offers — even if you don't want the role, the offer adds leverage
- Never reveal your current CTC first. Say: "I'm targeting market rate for this role."

---

# ═══════════════════════════════════════════════════════════════
# WEEKLY TRACKING TEMPLATE
# Copy this each week, fill in Sunday evening
# ═══════════════════════════════════════════════════════════════

```
Week: ___  |  Phase: ___  |  Date: ___

DSA:
  Problems done this week: ___
  Easy/Medium/Hard split: ___/___/___
  Total cumulative: ___
  Hardest problem cracked: ___

Study:
  Topic covered: ___
  File studied: ___
  Concepts still shaky: ___

Applications:
  Applied this week: ___
  Total applied: ___
  Callbacks received: ___
  Interviews scheduled: ___

Interviews Done:
  Company + Round: ___
  How it went (1-5): ___
  Questions I stumbled on: ___
  What to fix next week: ___

GitHub:
  Commits this week: ___
  Project status: ___

Energy/Focus (1-5): ___
What went well: ___
What to fix next week: ___
```

---

# ═══════════════════════════════════════════════════════════════
# DSA PROGRESS TRACKER
# ═══════════════════════════════════════════════════════════════

## NeetCode Blind 75 — Track Here

| # | Problem | Difficulty | Status | Date |
|---|---|---|---|---|
| 1 | Two Sum | Easy | | |
| 2 | Valid Anagram | Easy | | |
| 3 | Contains Duplicate | Easy | | |
| 4 | Group Anagrams | Medium | | |
| 5 | Top K Frequent Elements | Medium | | |
| 6 | Product of Array Except Self | Medium | | |
| 7 | Valid Sudoku | Medium | | |
| 8 | Longest Consecutive Sequence | Medium | | |
| 9 | Valid Palindrome | Easy | | |
| 10 | Two Sum II | Medium | | |
| 11 | 3Sum | Medium | | |
| 12 | Container With Most Water | Medium | | |
| 13 | Trapping Rain Water | Hard | | |
| 14 | Best Time to Buy/Sell Stock | Easy | | |
| 15 | Longest Substring Without Repeating | Medium | | |
| 16 | Longest Repeating Char Replacement | Medium | | |
| 17 | Permutation in String | Medium | | |
| 18 | Minimum Window Substring | Hard | | |
| 19 | Sliding Window Maximum | Hard | | |
| 20 | Valid Parentheses | Easy | | |
| 21 | Min Stack | Medium | | |
| 22 | Evaluate Reverse Polish Notation | Medium | | |
| 23 | Generate Parentheses | Medium | | |
| 24 | Daily Temperatures | Medium | | |
| 25 | Car Fleet | Medium | | |
| 26 | Largest Rectangle in Histogram | Hard | | |
| 27 | Binary Search | Easy | | |
| 28 | Search a 2D Matrix | Medium | | |
| 29 | Koko Eating Bananas | Medium | | |
| 30 | Find Min in Rotated Sorted Array | Medium | | |
| 31 | Search in Rotated Sorted Array | Medium | | |
| 32 | Time Based Key-Value Store | Medium | | |
| 33 | Median of Two Sorted Arrays | Hard | | |
| 34 | Reverse Linked List | Easy | | |
| 35 | Merge Two Sorted Lists | Easy | | |
| 36 | Reorder List | Medium | | |
| 37 | Remove Nth Node From End | Medium | | |
| 38 | Copy List with Random Pointer | Medium | | |
| 39 | Add Two Numbers | Medium | | |
| 40 | LRU Cache | Medium | | |
| 41 | Merge K Sorted Lists | Hard | | |
| 42 | Reverse Nodes in K-Group | Hard | | |
| 43 | Invert Binary Tree | Easy | | |
| 44 | Max Depth of Binary Tree | Easy | | |
| 45 | Diameter of Binary Tree | Easy | | |
| 46 | Balanced Binary Tree | Easy | | |
| 47 | Same Tree | Easy | | |
| 48 | Subtree of Another Tree | Easy | | |
| 49 | LCA of Binary Tree | Medium | | |
| 50 | Binary Tree Level Order Traversal | Medium | | |
| 51 | Binary Tree Right Side View | Medium | | |
| 52 | Count Good Nodes in Binary Tree | Medium | | |
| 53 | Validate Binary Search Tree | Medium | | |
| 54 | Kth Smallest in BST | Medium | | |
| 55 | Construct BT from Pre+Inorder | Medium | | |
| 56 | Binary Tree Max Path Sum | Hard | | |
| 57 | Serialize/Deserialize Binary Tree | Hard | | |
| 58 | Implement Trie | Medium | | |
| 59 | Design Add/Search Words DS | Medium | | |
| 60 | Word Search II | Hard | | |
| 61 | Combination Sum | Medium | | |
| 62 | Word Search | Medium | | |
| 63 | Subsets | Medium | | |
| 64 | Subsets II | Medium | | |
| 65 | Permutations | Medium | | |
| 66 | Combination Sum II | Medium | | |
| 67 | Palindrome Partitioning | Medium | | |
| 68 | Letter Combinations of Phone Number | Medium | | |
| 69 | N-Queens | Hard | | |
| 70 | Number of Islands | Medium | | |
| 71 | Clone Graph | Medium | | |
| 72 | Max Area of Island | Medium | | |
| 73 | Pacific Atlantic Water Flow | Medium | | |
| 74 | Surrounded Regions | Medium | | |
| 75 | Rotting Oranges | Medium | | |
(Continue with NeetCode 150 additions after completing Blind 75)

---

# ═══════════════════════════════════════════════════════════════
# COMPANY APPLICATION TRACKER
# ═══════════════════════════════════════════════════════════════

## Phase 1 Targets (First Offer)

| Company | Role | Applied | Status | Round | Notes |
|---|---|---|---|---|---|
| Razorpay | SDE-2 Backend | | | | |
| Juspay | SDE-2 | | | | |
| CRED | SDE-2 Backend | | | | |
| MakeMyTrip | SDE-2 | | | | |
| Meesho | SDE-2 Backend | | | | |
| Paytm | SDE-2 | | | | |
| Slice | SDE-2 Backend | | | | |
| ThoughtWorks | Application Developer | | | | |
| Atlassian | SDE-2 | | | | |
| Walmart Global Tech | SDE-2 | | | | |
| Publicis Sapient | SDE-2 | | | | |
| Nagarro | SDE-2 Java | | | | |

## Phase 2 Targets (Dream Role)

| Company | Role | Applied | Status | Round | Notes |
|---|---|---|---|---|---|
| Amazon | SDE-2 | | | | |
| Flipkart | SDE-2 | | | | |
| Goldman Sachs | SDE-2 Java | | | | |
| Morgan Stanley | SDE-2 | | | | |
| Google | L4/SWE | | | | |
| Microsoft | SDE-2 | | | | |
| PhonePe | SDE-2 Backend | | | | |
| Swiggy | SDE-2 Backend | | | | |
| Zerodha | Backend Dev | | | | |
| Uber India | SDE-2 | | | | |
| Stripe India | SDE-2 | | | | |

---

# ═══════════════════════════════════════════════════════════════
# QUICK REFERENCE: STUDY MATERIAL MAP
# ═══════════════════════════════════════════════════════════════

| Topic | Primary File | When to Use |
|---|---|---|
| Java Core | Section_01_Java_Core.md | Week 2 |
| Spring Boot | Section_02_Spring_Boot.md | Week 3 |
| Hibernate/JPA | Section_03_Hibernate_JPA.md | Week 3 |
| Microservices + Kafka + Redis | Section_04_05_06_Microservices_Kafka_Redis.md | Week 4 |
| Database + Distributed | Section_07_08_Database_DistributedSystems.md | Week 8 |
| Patterns + Docker + CI/CD | Section_09_10_11_Patterns_Docker_CICD.md | Week 9 |
| Cloud + Network + Go | Section_12_13_14_15_Cloud_Network_Design_Go.md | Week 9 |
| Testing + Behavioral | Section_16_17_18_19_Testing_Behavioral_Scenarios.md | Week 10 |
| FAANG Advanced Java | Section_20_FAANG_SDE2_SDE3_Advanced.md | Week 2 onwards |
| System Design (GSTN) | Section_21_SystemDesign_DeepDive_With_Answers.md | Week 7 |
| GSTN Architecture | GSTN_Architecture_Reference.md | All rounds |
| GSTN Code Walkthroughs | GSTN_Complete_SDE2_SDE3_InterviewPrep.md | All rounds |
| **[NEW] LLD Complete** | **Section_LLD_Complete.md** | **Week 3 onwards** |
| **[NEW] DSA Java Patterns** | **Section_DSA_Java_Patterns.md** | **Week 1 onwards** |
| **[NEW] Consumer Product SD** | **Section_SD_Consumer_Products.md** | **Week 7, Phase 2** |
| **[NEW] Modern Java + CQRS** | **Section_Modern_Java_Observability_CQRS.md** | **Week 8 onwards** |
| **[NEW] Behavioral + DB + Go** | **Section_Behavioral_DB_Golang.md** | **Week 8 onwards** |
| Amazon LP Stories | Amazon_LP_STAR_Bank.md | Week 10, Phase 2 |

---

# ═══════════════════════════════════════════════════════════════
# MONTHLY MILESTONES CHECKLIST
# ═══════════════════════════════════════════════════════════════

## Month 1 (April 19)
- [ ] Resume final version done
- [ ] LinkedIn optimized + Open to Work
- [ ] GitHub project started
- [ ] Java Core + Spring Boot + Hibernate studied
- [ ] **LLD framework learned + Parking Lot + Vending Machine done in Java** (NEW)
- [ ] **DP basics: Climbing Stairs, Coin Change, House Robber done in Java** (NEW)
- [ ] DSA Java Patterns cheat sheet read — Two Pointers, Sliding Window templates (NEW)
- [ ] 28 LeetCode Easy problems done (ALL in Java)
- [ ] 10+ applications out

## Month 2 (May 19)
- [ ] **LLD: 5 full problems done with Java code** (Parking Lot, Vending Machine, Elevator, BookMyShow, LRU Cache)
- [ ] **All design patterns memorized with trigger phrases** (Section_LLD_Complete.md Section 4)
- [ ] System Design framework internalized — 3 designs practiced end-to-end
- [ ] **Consumer product SD: Twitter Feed design practiced** (Section_SD_Consumer_Products.md)
- [ ] **Modern Java: Records, Sealed Classes, Virtual Threads — can explain all** (NEW)
- [ ] **CQRS + Event Sourcing: can explain with GSTN example** (NEW)
- [ ] **DB deep dive: EXPLAIN plans, isolation levels, index design** (NEW)
- [ ] Microservices + Kafka + Redis deep dive done
- [ ] 30+ LeetCode (mix Easy/Medium) done — all Java
- [ ] 25+ applications out
- [ ] 3+ real interviews completed

## Month 3 — Phase 1 Target (June 19)
- [ ] **FIRST OFFER IN HAND**
- [ ] 50 LeetCode total done — all Java
- [ ] **Behavioral: STARL format for 6+ stories; SDE-3 questions ready** (NEW)
- [ ] All 5 mock interview rounds done at least once
- [ ] Offer negotiated
- [ ] **Observability: can answer "API is slow — diagnose it" with full structure** (NEW)

## Month 4 (July 19)
- [ ] Phase 1 offer accepted
- [ ] NeetCode Blind 75: 50% done
- [ ] **FAANG-level consumer product SDs: all 4 practiced** (Twitter, Drive, WhatsApp, Uber)
- [ ] **LLD: 5 more problems (Chess, Food Delivery, Pub-Sub, Rate Limiter, Hotel Booking)**
- [ ] Applications to dream companies started

## Month 5 (August 19)
- [ ] NeetCode Blind 75: 100% done
- [ ] NeetCode 150 additions: started (25+ done)
- [ ] Company-specific prep: Amazon LPs, Goldman Java depth
- [ ] **Golang deep dive done: goroutines, channels, context, sync, HTTP service** (NEW)
- [ ] **DDD concepts: Bounded Context, Aggregates, Value Objects — for Stripe/Goldman** (NEW)
- [ ] 3+ dream company interviews in pipeline

## Month 6 — Phase 2 Target (September 19)
- [ ] **DREAM OFFER IN HAND**
- [ ] 150+ LeetCode total done — all Java
- [ ] Offer negotiated to maximum (use Section_Behavioral_DB_Golang.md Negotiation Playbook)
- [ ] Start date + onboarding planned

---

*Programme created: March 2026 | Based on GSTN codebase + 5.5 YOE context*
*Review and update this file weekly. It is your single source of truth.*
