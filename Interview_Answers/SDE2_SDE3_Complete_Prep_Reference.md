# SDE-2 / SDE-3 Complete Interview Preparation Reference
## Jayanti Vishnoi | 5.6 Years Experience | GSTN Litigation & Appeal Module
### Target: SDE-2/SDE-3 at Product Companies / Good Startups
**Last Updated: April 2026 (v3 — ATS fixes + Learn & Impress section added)**

---

## TABLE OF CONTENTS

1. [Resume Bullets — What to Put & How](#1-resume-bullets)
2. [Your GSTN Technical Deep Dive](#2-gstn-technical-deep-dive)
3. [What You Must Know by Heart](#3-what-you-must-know-by-heart)
4. [LLD Questions — Easy to Advanced (with GSTN Mapping)](#4-lld-questions)
5. [HLD Questions — Easy to Advanced (with GSTN Mapping)](#5-hld-questions)
6. [Progressive 90-Day Study Plan](#6-progressive-90-day-study-plan)
7. [Projects to Build](#7-projects-to-build)
8. [Platform-Level Learning Resources](#8-platform-level-learning-resources)
9. [Interview Answer Templates](#9-interview-answer-templates)
10. [GSTN → Standard Interview Problem Cheat Sheet](#10-gstn-to-standard-problem-cheat-sheet)
11. [ATS-Friendly Bullet Rewrites](#11-ats-friendly-bullet-rewrites)
12. [What Else to Learn from This Codebase — Impressive Resume Additions](#12-what-else-to-learn)

---

## 1. RESUME BULLETS

### Headline Project Line
```
Tax Litigation & Appeal Order Management — Full-Stack Feature Owner
National GST Platform (15.2 Million Taxpayers, 1.52 Crore Active GST Registrations) | Java/Spring Boot · Angular · MySQL · Redis · Kafka
```

---

### GSTN Terminology → Generic Resume Language (Translation Table)

| GSTN-Specific Term | Generic Resume / LinkedIn Language |
|---|---|
| DRC07 | "Tax demand notice" / "original demand order" |
| APL01 | "Taxpayer appeal application" |
| APL03 | "Department-initiated appeal" |
| APL04 | "Appeal order" / "adjudication order" |
| DCR Entries | "Double-entry ledger transactions" / "financial audit trail entries" |
| Transfer In / Transfer Out | "Inter-account balance transfer" / "demand account reconciliation" |
| Dispute(A) amount | "Disputed liability amount" |
| Predeposit / Admitted amount | "Mandatory pre-deposit / admitted liability" |
| Refund Due | "Government-owed refund trigger" |
| Simultaneous Combine Order | "Concurrent multi-party appeal processing" |
| Subsequent Order | "Higher appellate court order processing" |
| CaseMgmtFwk | "Case lifecycle management framework" |
| LedgerUtilFwk | "Distributed financial ledger engine" |
| WorkFlowFwk | "Workflow orchestration engine" |
| DistCacheFwk | "Distributed caching layer (Redis)" |
| BOLitigationWeb | "Back-office litigation management portal (Angular)" |
| LitigationAPI / LitigationAPI2 | "Litigation microservice REST API" |
| D1 / D2 / D3 demand chain | "Multi-tier demand account chain" |
| stateCd jurisdiction | "Multi-tenant state-wise jurisdiction routing" |
| Model-1 / Model-2 states | "Central vs State adjudication model" |
| ARN generation | "Unique appeal reference number generation" |
| GSTIN | "Taxpayer unique identifier" |
| 1.52 Cr taxpayers | "15.2 million registered taxpayers" |
| Back-office officer | "Tax adjudication officer" |

---

### Resume Bullets — Generic Language (Use These on Resume / LinkedIn)

- **Designed a 12-scenario appellate order processing engine** for a national tax litigation
  platform by implementing a decision-matrix state machine across a 3-tier demand account chain
  (original demand → first appeal order → subsequent order), handling conditional demand
  creation, inter-account balance transfers, dispute reversals, and refund-due triggers —
  eliminating ad-hoc conditional branching and making each legal outcome a named,
  independently testable rule

- **Engineered a double-entry financial ledger engine** tracking debit (liability), credit
  (payment / dispute / inter-account transfer), and net outstanding per demand account —
  automating status transitions to `Settled` (balance = 0) or `Refund Due` (balance < 0) and
  ensuring pre-deposit amounts are credited to successor accounts in multi-tier appellate chains

- **Built concurrent multi-party appeal processing** where both taxpayer and department
  appeals on the same demand are resolved via a single unified adjudication order — designed
  payload transformation logic so issuance from either party's side transparently writes into
  the canonical case record, enforcing the legal constraint of one order per demand across
  15.2 million taxpayer accounts

- **Implemented XA distributed transactions (Atomikos 2PC)** to guarantee atomicity across
  three independent databases (case management, financial ledger, workflow engine) during
  adjudication order issuance — preventing partial-commit scenarios in legally binding financial
  operations where any inconsistency is a compliance violation

- **Architected a plugin-based case lifecycle framework** using Strategy + Factory design
  patterns to support 20+ legally distinct proceeding types (appeals, adjudication, demand
  recovery, waiver) — each type encapsulates its own initialization and order-effect logic as
  an isolated customizer, allowing new proceeding types to be onboarded without modifying
  core framework code

- **Delivered full-stack appeal management module** on Spring Boot microservices (REST APIs,
  XA transactions, Kafka async notifications) with Angular dynamic forms for back-office
  adjudication officers — covering order issuance, multi-tier cascading closures, and
  real-time demand balance display across 28 state jurisdictions

- **Reduced repeated database lookups by 60-80%** during peak filing windows by implementing
  a Redis-backed distributed cache (TTL-based) for jurisdiction and master data across a
  platform serving 15.2 million registered taxpayers

---

### Frontend Resume Bullets

- **Built adjudication order issuance UI** (Angular) — dynamic forms with auto-populated
  disputed amounts and user-input determined amounts, conditional rendering based on order
  outcome type (Modified / Confirmed / Rejected), and real-time outstanding balance display

- **Implemented concurrent multi-party appeal UI** — surfacing order issuance on both
  taxpayer and department appeal sides while enforcing single-order constraint, constructing
  correct request payloads per issuance side, and syncing order visibility across both
  case views post-issuance

- **Designed multi-tier order status screens** with cascading state display across 3-level
  demand account chain, showing live status (`Order Issued - Demand Closed`, `Refund Due`,
  `New Demand Created`) and payment transfer summaries per scenario

---

### Power Bullet (Single sentence for space-limited resume)

> **Owned end-to-end design and delivery of a tax appellate order management system** on
> India's national GST platform (15.2 million taxpayers) — implemented a 12-scenario demand state
> machine with double-entry ledger engine, XA distributed transactions across 3 databases,
> and concurrent multi-party appeal processing using Strategy + Factory patterns on a
> Java/Spring Boot + Angular stack

---

### Interview Deep-Dive Talking Points (Prepare These Cold)

**Talking Point 1 — "Walk me through the 12-scenario matrix — how did you avoid making it unmaintainable?"**

> The matrix is driven by two inputs: first-appeal outcome (Modified / Confirmed / Rejected) and
> subsequent order outcome (same three). Rather than nested if-else, I modelled each combination
> as a named Rule with a condition predicate (checks both outcomes) and an action (executes the
> correct ledger operations). The engine evaluates the matching rule and fires it. Adding a new
> scenario = adding one rule, not touching existing code — this is the Open/Closed Principle in
> practice. Each rule is independently unit-testable with a specific financial scenario.

**Talking Point 2 — "Why XA transactions? Why not Saga pattern?"**

> The order issuance must be atomic across case DB, ledger DB, and workflow DB — there is no
> acceptable intermediate state. A Saga with compensating transactions would mean a window where
> the case shows "order issued" but the ledger hasn't updated — legally unacceptable in a
> government tax system. XA 2PC holds locks across all three resources and either commits all or
> rolls back all. The trade-off is latency and DB lock contention, which we accepted because order
> issuance is a low-frequency, high-stakes operation — not a high-throughput path.

**Talking Point 3 — "How did you handle the concurrent order issuance problem?"**

> Two officers could simultaneously pass the state-validity check and both proceed to issue an
> order on the same demand — a classic TOCTOU (Time-Of-Check-Time-Of-Use) race. I solved it
> with two layers: `@Version` optimistic locking on the case entity (the second writer gets
> `OptimisticLockException` at commit time), and a Redis distributed lock (`SETNX demandId EX 30`)
> acquired at the start of the issuance flow — so across multiple API server instances, only one
> request proceeds past the lock. Optimistic lock is the safety net; Redis lock is the performance
> gate.

---

### Resume Language Rules
| ❌ Avoid | ✅ Use Instead |
|---|---|
| "worked on" | "owned end-to-end" |
| "involved in" | "designed and implemented" |
| "contributed to" | "built / engineered / delivered" |
| "helped with" | "led / drove / architected" |
| Domain jargon (DRC07, APL01) | Generic equivalent (tax demand notice, taxpayer appeal) |

---

## 2. GSTN TECHNICAL DEEP DIVE

### 2.1 Architecture You Must Explain

```
REST Controller (LitigationAPI2)
    → CaseHandler          (Input validation, routing — Facade pattern)
        → CaseService      (Interface — contract — ISP, OCP)
            → CaseServiceImpl  (Business logic)
                → DAO              (DB operations — MySQL)
                → WorkFlowFwk      (Task lifecycle)
                → LedgerUtilFwk    (DCR entries — demand ledger)
                → DistCacheFwk     (Redis — jurisdiction/master cache)
                → KafkaConsumerFwk (Async events post-commit)
```

---

### 2.2 CaseMgmtFwk — Key Classes

| Class | Role | Pattern Used |
|---|---|---|
| `CaseHandler` | Validates input, routes to service | Facade |
| `CaseService` | Interface contract | ISP, OCP |
| `CaseServiceImpl` | All business logic | Template Method |
| `CaseFolderHandler` | Manages case folders (containers) | Facade |
| `TaskServiceImpl` | Creates/updates tasks on state change | Command |
| `CaseAssignTaskServiceImpl` | Jurisdiction-based officer assignment | Strategy |
| `AppealTranCaseCustomizer` | Appeal-specific init logic | Strategy |
| `CaseCustomizerFactory` | Resolves customizer by case type | Factory |
| `GenericCaseHandler` | Base handler, overrideable steps | Template Method |

**Key VO Fields on `Case.java`:**
- `caseId`, `caseTypeCd`, `gstid`, `stateCd`, `arn`
- `caseCreationDate`, `aplAdmCaseStatus`, `draftId`
- `stateJursdCd`, `cntrJursdCd` — for jurisdiction routing

---

### 2.3 Ledger / DCR Mental Model

```
Every demand = a ledger account
DR (Debit)  = Amount Added   → money owed TO government
CR (Credit) = Amount Reduced → money paid / settled / disputed

Outstanding Balance = ΣDR - ΣCR
  > 0  →  Outstanding (taxpayer still owes)
  = 0  →  Demand Settled
  < 0  →  Refund Due (government owes taxpayer)
```

**DCR Operations — Trigger & Effect:**

| Operation | Triggered When | Financial Effect |
|---|---|---|
| `createDemand` (DR) | New DRC07 or APL04 created | Opens demand with debit |
| Dispute(A) CR | APL04 issued | Reduces D1 outstanding by disputed amt |
| Payment CR | Taxpayer pays admitted+predeposit | Reduces D1 outstanding |
| Transfer Out | D1 outstanding goes negative | Moves negative balance OUT of D1 |
| Transfer In | Into D2/D3 | Brings negative balance INTO new demand |
| Determine DR | New D2/D3 demand created | Sets opening balance of new demand |
| Admitted Amount CR | Subsequent Order with Confirm/Modify | Credits APL01 predeposit into D3 |
| Refund Due trigger | Outstanding < 0 after all CRs | System marks Refund Due |

---

### 2.4 Appeal Order — 6 Scenario Matrix

| APL Type | APL04 Outcome | D1 Status | D2 Created? | D2 Status |
|---|---|---|---|---|
| APL01 | Modified | First Appeal Order Issued | Yes | FAOI Demand Created |
| APL01 | Confirmed | First Appeal Order Issued | Yes (cancelled) | Refund Due |
| APL01 | Rejected | First Appeal Rejected | No | — |
| APL03 | Modified | FAOI | Yes | FAOI Demand Created |
| APL03 | Confirmed | FAOI | Yes (cancelled) | Refund Due |
| APL03 | Rejected | First Appeal Rejected | No | — |

**Key difference: APL01 vs APL03**
```
APL01 (taxpayer appeal):
  Outstanding = always negative (predeposit + admitted paid) → Transfer always happens

APL03 (department appeal):
  Outstanding = positive, zero, or negative
  - Positive  → amount remains as-is
  - Zero      → Demand Settled
  - Negative  → Refund Due transferred
```

---

### 2.5 Subsequent Order — 12 Scenario Decision Tree

```
INPUT: (firstAppealOutcome, subsequentOutcome)

if firstAppealOutcome IN [Confirmed, Modified]:
    if subsequentOutcome == Rejected:
        → Reverse D1 dispute amount
        → Close D2: credit determined amt, transfer payments back D2→D1
        → D1 status: Subsequent Order Rejected
        → D2 status: Subsequent Order Issued - Demand Closed

    if subsequentOutcome == Confirmed:
        → Create D3 (new demand with dispute amt)
        → Close D2: credit determined amt, transfer payments D2→D3
        → Credit admitted amount into D3
        → D2 status: SOI Demand Closed
        → D3 status: SOI Demand Created

    if subsequentOutcome == Modified:
        → Create D3 (new demand with DETERMINED amt, not dispute)
        → Close D2: credit determined amt, transfer payments D2→D3
        → Credit admitted amount into D3
        → D2 status: SOI Demand Closed
        → D3 status: SOI Demand Created

if firstAppealOutcome == Rejected:
    // D1 (DRC07) was never closed — close it now

    if subsequentOutcome == Rejected:
        → No financial transactions
        → D1 status: Subsequent Order Rejected

    if subsequentOutcome IN [Confirmed, Modified]:
        → Create D3
        → Close D1: transfer payments D1→D3
        → Credit admitted amount into D3
        → D1 status: SOI Demand Closed
        → D3 status: SOI Demand Created
```

**For APL03 first appeal (Flow 2):** All above applies BUT with extra step:
- **Reverse APL03 dispute amount from D1 first**
- Then execute equivalent APL01 flow for D3 creation

---

### 2.6 Simultaneous Combine Order — Core Logic

```
Condition: APL01 (Admitted, not withdrawn) + APL03 (Admitted, not withdrawn) on same DRC07
           → Eligible for Simultaneous Combine Order

Rule: Single APL04 order, visible at BOTH APL01 and APL03 sides

Issuance from APL01 side:
  payload: { isSimulCombineOrd: true, dispt: apl01Dispute, dtmr: determine,
             apl03dispAmt: (apl03Dispute - apl04Dispute), srcModule: "APPEL" }

Issuance from APL03 side (transformation required):
  → In DB: stored as APL01 case entry (APPEL_ORDRS_APLOD), NOT APLTD
  → Payload transformed: swap current_dispt → apl01Dispute
  payload: { isSimulCombineOrd: true, dispt: apl01Dispute [swapped],
             dtmr: determine, apl03dispAmt: ..., srcModule: "APLTD" }

Ledger (same as APL01):
  D1 (DRC07):
    DR: 1000 (original demand)
    CR: 280  (APL01 payment: 200 admitted + 80 predeposit)
    CR: 800  (APL01 dispute)
    DR: 80   (Transfer Out of negative balance)

  D2 (APL04):
    DR: 1400 (Determine)
    CR: 80   (Transfer In)
    CR: 200  (Credit Admitted Amount)
```

---

### 2.7 Design Patterns In Your Code — Name Them

| Pattern | Where in GSTN | Describe It |
|---|---|---|
| **Strategy** | `AppealTranCaseCustomizer`, `DCRCustomizer` etc. | Each case type has its own customizer implementing same interface |
| **Factory** | `CaseCustomizerFactory` | Resolves which customizer to use at runtime based on `caseTypeCd` |
| **Template Method** | `GenericCaseHandler` → `CaseHandler` | Base flow defined, specific steps overridden |
| **Facade** | `CaseHandler` | Hides complexity of `CaseService` + `WorkFlowFwk` from REST controller |
| **Observer** | Kafka post-commit events | `ORDER_ISSUED` event → notification consumer, audit consumer |
| **Decorator** | `GstAopFwk` AOP aspects | Adds logging/security around methods without changing them |
| **Singleton** | `DistCacheFwk` Redis connection | Single shared cache manager instance |
| **Saga (Orchestration)** | Subsequent Order processing | Coordinator drives D1/D2/D3 closure sequence |

---

## 3. WHAT YOU MUST KNOW BY HEART

### Tier 1 — MUST (Every Round)

#### Java Internals
- `HashMap` internals: hash collision, treeification at bucket size 8, load factor 0.75, resize at 75%
- `ConcurrentHashMap`: segment locking (Java 7) → CAS + synchronized per bucket (Java 8+)
- `volatile` = visibility guarantee (not atomicity); `synchronized` = both visibility + atomicity
- `ThreadLocal` — request-scoped user context (audit user in your GSTN code)
- `equals()` + `hashCode()` contract — must override both together
- Checked (`GSTLogicalException`) vs Unchecked (`GSTRuntimeException`) — your real code uses this
- `@Transactional` propagation:
  - `REQUIRED` — joins existing or creates new (default)
  - `REQUIRES_NEW` — always new transaction (use for D3 creation so it doesn't roll back D2 closure)
  - `NESTED` — savepoint within existing

#### Spring Boot
- Bean lifecycle: `@PostConstruct` → `afterPropertiesSet` → bean ready
- Singleton vs Prototype scope
- `@Async` — works via Spring proxy; needs `@EnableAsync`; runs in thread pool
- `@Autowired` — field injection vs constructor injection (constructor = preferred, testable)
- AOP: `@Before`, `@After`, `@Around` — how `GstAopFwk` works

#### Database
- B-Tree index: balanced tree, O(log n) lookup, good for range queries
- Composite index: order matters — `(stateCd, caseTypeCd)` helps query on `stateCd` alone but not `caseTypeCd` alone
- `EXPLAIN` plan: look for "full table scan" → add index
- **Optimistic Locking** (`@Version`): read + version check on write — no lock held; fails if version mismatch
- **Pessimistic Locking** (`SELECT FOR UPDATE`): lock row immediately — use for APL04 issuance
- N+1 problem: `findAllCases()` then `case.getFolders()` × N → fix with `JOIN FETCH`
- Transaction isolation: `READ COMMITTED` (default MySQL) vs `REPEATABLE READ` vs `SERIALIZABLE`

#### Distributed Systems
- CAP theorem: your GSTN = **CP** (legal orders must be consistent; brief unavailability OK)
- Idempotency: `draftId` on `Case.java` = idempotency key (same draft = don't create duplicate case)
- Exactly-once vs at-least-once Kafka: GSTN uses at-least-once + idempotent consumer check

---

### Tier 2 — IMPORTANT (Deep Dive Rounds)

#### REST API Design
- Idempotency: GET, PUT, DELETE are idempotent; POST is not (use idempotency key header)
- HTTP codes to know: `200`, `201`, `204`, `400`, `401`, `403`, `404`, `409` (conflict), `422`, `500`
- Versioning: `/v1/` vs `/v2/` — your `LitigationAPI` vs `LitigationAPI2` is real versioning

#### Kafka
- Producer → Topic (partitioned) → Consumer Group
- Offset = position in partition; consumer commits offset after processing
- Exactly-once: `enable.idempotence=true` on producer + transactional consumer
- DLQ (Dead Letter Queue): failed messages → retry topic → DLQ after max retries

#### Redis
- `SETNX key value EX ttl` = distributed lock (set if not exists + TTL)
- Cache invalidation: TTL-based (your case), event-based, write-through
- Data structures: String, Hash, List, Set, SortedSet — know when to use each

---

## 4. LLD QUESTIONS

### EASY (Weeks 1-2)

| # | Question | GSTN Hook | Key Concept |
|---|---|---|---|
| L1 | What is LLD? Why does it matter? | CaseMgmtFwk = LLD artifact | Blueprint before coding |
| L2 | Explain SOLID principles | `CaseService` interface = SRP+ISP; Customizers = OCP | 5 principles, one example each |
| L3 | What is a Design Pattern? Types? | Strategy+Factory+Observer all in your code | Creational/Behavioral/Structural |
| L4 | Explain Singleton pattern | Redis connection manager in `DistCacheFwk` | One instance, global access |
| L5 | Explain Factory pattern | `CaseCustomizerFactory` by `caseTypeCd` | Deferred instantiation |
| L6 | Explain Strategy pattern | 20+ customizers, one interface | Algorithm family, runtime selection |
| L7 | Explain Observer pattern | Kafka after APL04 order issuance | One-to-many, event-driven |
| L8 | What is a State Machine? Draw one | Appeal: `FILED→ADMITTED→ORDER_ISSUED→SETTLED` | States + transitions + guards |
| L9 | How does DB indexing work? | `demandId`, `gstin`, `caseTypeCd` indexed | B-Tree, trade-off: read vs write |
| L10 | Why is concurrency control needed? | Two officers issuing APL04 on same DRC07 | Race condition → @Version |

**Interview Answer — State Machine (memorize this):**
```
Appeal Case States:
  APL01_FILED
      ↓ [Officer admits]
  ADMITTED
      ↓ [APL04 issued - Modified]          ↓ [APL04 issued - Confirmed]     ↓ [APL04 issued - Rejected]
  FIRST_APPEAL_ORDER_ISSUED            FIRST_APPEAL_ORDER_ISSUED         FIRST_APPEAL_REJECTED
      ↓ [D1 outstanding = 0]               ↓ [D2 outstanding < 0]
  DEMAND_SETTLED                       REFUND_DUE
```

---

### MEDIUM (Weeks 3-5) — Machine Coding Problems

| # | Machine Coding Problem | Time | GSTN Equivalent | Key Design |
|---|---|---|---|---|
| L11 | Design Parking Lot | 90 min | Case = slot, Officer = car, Task = ticket | State machine + observer |
| L12 | Design Library System | 90 min | CaseMgmtFwk itself | CRUD + search + state |
| L13 | Design Notification System | 90 min | Kafka post-order events | Observer + async |
| L14 | Design Elevator System | 90 min | WorkFlowFwk task queue | Strategy (scheduling algo) |
| L15 | Design Food Ordering System | 90 min | Appeal filing = order | State machine + factory |
| L16 | Design LRU Cache | 60 min | DistCacheFwk Redis TTL | HashMap + DoublyLinkedList |
| L17 | Design Rate Limiter | 60 min | APL01 filing throttle per GSTIN | Token bucket / sliding window |
| L18 | Design ATM System | 90 min | Demand payment flow | Template method + state |
| L19 | Design Splitwise | 90 min | DCR Transfer In/Out between demands | Double-entry bookkeeping |
| L20 | Design Logger | 45 min | `GstAopFwk` + SLF4J | Singleton + Observer + Strategy |

**How to approach any machine coding problem in 90 minutes:**
```
0-10 min:  Clarify requirements. Functional (what) + Non-functional (scale, concurrent users)
10-25 min: Identify entities/classes. Draw class diagram on paper.
25-45 min: Define interfaces. Write skeleton code with method signatures.
45-75 min: Implement core logic. Get one happy path working end-to-end.
75-90 min: Add edge cases. Thread safety. Brief walkthrough.
```

---

### ADVANCED (Weeks 6-8) — SDE-3 Level

| # | Question | Your GSTN Answer | Key Concepts |
|---|---|---|---|
| L21 | Design a Workflow Engine | WorkFlowFwk — task lifecycle, assignee routing, escalation | DAG, state machine, event-driven |
| L22 | Design a Double-Entry Ledger | LedgerUtilFwk — DR/CR, Transfer In/Out, balance computation | Immutable events, projection |
| L23 | Design a Case Management Framework | CaseMgmtFwk — 20+ case types, Strategy+Factory | Plugin architecture, extensibility |
| L24 | Design Distributed Transaction | XA Atomikos 2PC across 3 DBs | 2PC, Saga, compensating transactions |
| L25 | Optimistic vs Pessimistic Locking | @Version for case, SELECT FOR UPDATE for APL04 | MVCC, lock granularity |
| L26 | Design Audit Trail System | AuditMstrDetlEntity, AuditFormJsonEntity | Append-only log, event sourcing |
| L27 | Design Multi-Tenant System | GSTN by stateCd — Model-1 vs Model-2 states | Tenant isolation, shared schema |
| L28 | Design Rule Engine | 12-scenario Subsequent Order matrix | Decision table, interpreter pattern |
| L29 | Design Event Sourcing System | DCR entries = event sourcing (each DR/CR = immutable event) | CQRS, projections, replay |
| L30 | Design Idempotent API | `draftId` on Case, `isSimulCombineOrd` flag | Idempotency key, deduplication |

---

## 5. HLD QUESTIONS

### EASY (Weeks 1-2)

| # | Question | GSTN Hook | Answer Framework |
|---|---|---|---|
| H1 | What is HLD? Components? | API→Framework→DB→Cache→Queue layers | Architecture, tech stack, scalability |
| H2 | Monolith vs Microservices? | LitigationAPI→LitigationAPI2 split = you witnessed this | Trade-offs: complexity vs scalability |
| H3 | What is Load Balancing? | Multiple LitigationAPI2 instances at deadline peaks | Round robin, least connections |
| H4 | What is Caching? Types? | DistCacheFwk Redis — jurisdiction cache, TTL-based | L1/L2/CDN/App cache layers |
| H5 | SQL vs NoSQL — when to use? | MySQL (ACID for demands), HBase (scale for returns) | Structured vs flexible, ACID vs BASE |
| H6 | What is an API Gateway? | GSTN gateway: auth token validation, rate limiting | Single entry point, cross-cutting |
| H7 | What is CAP Theorem? | GSTN = CP — legal orders must be consistent | C+A+P, can only guarantee 2 of 3 |
| H8 | What is eventual consistency? | Kafka notification — order issued, SMS eventually | BASE vs ACID, use cases |
| H9 | Horizontal vs Vertical scaling? | GSTN API scales horizontally at filing deadline | Stateless services for horizontal |
| H10 | What is a Message Broker? | KafkaConsumerFwk — high throughput, ordered partitions | Kafka vs RabbitMQ trade-offs |

---

### MEDIUM (Weeks 3-5) — System Design Problems

**Framework for ANY HLD problem:**
```
Step 1 (5 min):  Clarify requirements
  → Functional: what does the system do?
  → Non-functional: scale, latency, availability, consistency

Step 2 (5 min):  Capacity estimation
  → DAU, requests/sec, storage/day, bandwidth

Step 3 (10 min): High-level design
  → Draw: Client → API Gateway → Services → DB → Cache → Queue

Step 4 (20 min): Deep dive into critical components
  → DB schema, API contracts, key algorithms

Step 5 (10 min): Address bottlenecks
  → Scaling, caching strategy, failure handling
```

| # | HLD Problem | GSTN Mapping | Key Design Decisions |
|---|---|---|---|
| H11 | Design URL Shortener | ARN generation = short unique ID | Hash + collision handling, redirect |
| H12 | Design Notification System | Async Kafka after APL04 issuance | Fan-out, rate limiting, retry |
| H13 | Design Rate Limiter | APL01 filing throttle per GSTIN/day | Token bucket, Redis sliding window |
| H14 | Design Job Scheduler | Demand expiry batch, DCR reconciliation | Distributed cron, leader election |
| H15 | Design Search System | Solr in GSTN — case search by GSTIN+period | Inverted index, ranking |
| H16 | Design Distributed Cache | DistCacheFwk Redis layer | Eviction policies, consistency |
| H17 | Design Auth System | AuthenticationFwk + AuthFwk + JWT | OAuth2, JWT, session management |
| H18 | Design Chat System | Communication in GSTN between officers | WebSocket, message ordering |
| H19 | Design File Storage | Audit documents in CaseMgmtFwk | Object storage, metadata index |
| H20 | Design Payment System | DCR demand payment flow | Idempotency, double-spend prevention |

---

### ADVANCED (Weeks 6-8) — SDE-3 Level

| # | HLD Problem | Your GSTN Angle | Key Concepts to Cover |
|---|---|---|---|
| H21 | Design GST Litigation Platform | **THIS IS YOUR SYSTEM** — describe it as case study | Microservices, CaseMgmtFwk, workflow, ledger |
| H22 | Design Distributed Ledger | LedgerUtilFwk — immutable DCR entries | Event sourcing, CQRS, eventual consistency |
| H23 | Design Workflow Orchestration | WorkFlowFwk — task lifecycle, SLA, escalation | Saga orchestration, state machine |
| H24 | Design for 10M Concurrent Users | GSTN scale — 1.52 Cr taxpayers, deadline spikes | Sharding by stateCd, Redis hot data |
| H25 | Design Distributed Transaction | XA 2PC vs Saga for D1→D2→D3 order chain | 2PC trade-offs, compensating transactions |
| H26 | Design CQRS System | GSTN read (case list view) vs write (case creation) | Command bus, event store, read model |
| H27 | Design Multi-Region DR | GSTN primary + DR site for legal data | RPO, RTO, geo-replication, failover |
| H28 | Saga Pattern — which variant? | Subsequent Order = **orchestration** saga | Choreography (Kafka events) vs Orchestration (coordinator) |
| H29 | Design Audit System at Scale | AuditMstrDetlEntity → centralized audit service | Append-only, Kafka ingestion, search |
| H30 | Design Distributed Lock | Redis SETNX to prevent duplicate APL04 issuance | SETNX+TTL, Redlock algorithm |

---

### Your Flagship HLD Answer — GST Litigation Platform

**Use this when asked: "Design a Case Management System" / "Design a Workflow System" / "Tell me about a complex system you built"**

```
SYSTEM: GST Litigation & Appeal Management Platform
SCALE:  1.52 Cr active GST registrations | ~4-4.8 lakh first-appeal backlog (GSTAT) | ~2M total cases/year | 28 states | Deadline traffic spikes

ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│                     API GATEWAY                              │
│              (Auth JWT + Rate Limiting)                      │
└─────────────────────┬───────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────────┐
         ▼             ▼                 ▼
  LitigationAPI2  BOLitigationAPI   BOLitigationWeb
  (Taxpayer-facing) (Back-office)   (Angular UI)
         │             │
         └──────┬───────┘
                ▼
         CaseMgmtFwk
    (Strategy+Factory pattern)
    ┌──────────────────────────┐
    │ CaseHandler (Facade)     │
    │ CaseServiceImpl          │
    │ CaseCustomizerFactory    │
    │ AppealTranCaseCustomizer │
    └──────┬───────────────────┘
           │
    ┌──────┼──────────────────────────┐
    ▼      ▼                          ▼
  MySQL  WorkFlowFwk              LedgerUtilFwk
(Cases)  (Task lifecycle)         (DCR entries)
           │                          │
           ▼                          ▼
        Redis                      MySQL
  (Jurisdiction cache)          (Demand table)
           │
           ▼
        Kafka
  (ORDER_ISSUED event)
           │
    ┌──────┴──────┐
    ▼             ▼
Notification   Audit
 Consumer     Consumer

KEY DESIGN DECISIONS:
1. Strategy+Factory: 20+ case types, extensible without if-else
2. XA Atomikos 2PC: atomic across 3 DBs for order issuance
3. @Version optimistic locking: concurrent officer access
4. Redis TTL cache: jurisdiction master, 60-80% DB load reduction at peaks
5. Kafka async: decouple legal order from notification failures
6. Horizontal scaling: stateless API + external session (Redis)
7. Sharding approach: by stateCd — 28 partitions, natural domain boundary
```

---

## 6. PROGRESSIVE 90-DAY STUDY PLAN

### Phase 0: Before You Start (1 Week)
**Goal: Baseline audit — know what you already know vs gaps**

```
Day 1: Read through this entire document. Mark what you can explain confidently (✅) vs not (❌)
Day 2: Write CaseMgmtFwk architecture from memory (no looking). Compare with real code.
Day 3: Draw the 12-scenario Subsequent Order decision tree from memory.
Day 4: Explain the DCR ledger model to yourself out loud for 10 minutes.
Day 5: Set up a blank Spring Boot project — your playground for the next 90 days.
Day 6-7: Review Java 8+ features: Streams, Optional, CompletableFuture, Lambdas.
```

---

### Phase 1: LLD Foundations (Weeks 1-3)
**Goal: Master all design patterns + implement them in code**

**Week 1 — Behavioral Patterns**
```
Day 1-2:  Strategy Pattern
  Theory:  What is it? When to use? Open/Closed Principle connection?
  Code:    CaseCustomizer interface + AppealCustomizer + AdjudicationCustomizer + Factory
  Test:    Unit test each customizer independently

Day 3-4:  Observer Pattern
  Theory:  Push vs pull model. EventListener vs Kafka.
  Code:    OrderEventPublisher + NotificationListener + AuditListener
  Test:    Verify both listeners called on single event

Day 5-6:  Template Method Pattern
  Theory:  Base class defines algorithm, subclasses override steps
  Code:    AbstractCaseCreationFlow → AppealCreationFlow + DCRCreationFlow
  Test:    Verify base steps always run, custom steps override correctly

Day 7:    State Machine Pattern
  Theory:  States, transitions, guards, actions
  Code:    AppealStateMachine (5 states, 8 transitions) — use enum + switch
  Test:    Verify illegal transitions throw exception
```

**Week 2 — Creational + Structural Patterns**
```
Day 1-2:  Factory + Abstract Factory
  Code:    CaseCustomizerFactory + DemandFactory (creates DRC07 vs APL04 demand)

Day 3-4:  Decorator + AOP
  Code:    @LogExecution aspect + @AuditTrail aspect (like GstAopFwk)
  Learn:   Spring AOP proxy mechanism, @Around, JoinPoint, ProceedingJoinPoint

Day 5-6:  Facade + Builder
  Code:    LitigationFacade (wraps CaseService + LedgerService + WorkflowService)
           CaseRequestBuilder (builds complex Case VO with validation)

Day 7:    Singleton + Object Pool
  Code:    Thread-safe Singleton (double-checked locking + volatile)
           Connection pool concept (why DistCacheFwk uses pool)
```

**Week 3 — SOLID Principles Deep Dive**
```
Day 1:  Single Responsibility — refactor a God class into focused services
Day 2:  Open/Closed — add new case type WITHOUT modifying existing code (Strategy proves this)
Day 3:  Liskov Substitution — verify customizer subclasses are substitutable for interface
Day 4:  Interface Segregation — CaseService splits into CaseFolderService, TaskService etc.
Day 5:  Dependency Inversion — constructor inject CaseService (not new CaseServiceImpl())
Day 6-7: Code review your own projects against SOLID — fix violations
```

---

### Phase 2: Machine Coding Practice (Weeks 4-6)
**Goal: Solve any LLD problem in 90 minutes with clean, working, tested Java code**

**Rules for practice:**
- No IDE autocomplete during first 45 minutes
- Must write at least 3 unit tests per problem
- Record yourself explaining the design for 5 minutes after each

**Week 4 — Warm Up Problems**
```
Problem 1: Parking Lot (Day 1-2)
  Entities: ParkingLot, Floor, Slot (Compact/Large/Handicapped), Ticket, Vehicle
  Features: Enter → assign nearest slot; Exit → compute fee; Find available
  Pattern:  Strategy (fee calculation), Factory (slot types), Singleton (lot)
  GSTN Map: Case(lot) + Task(ticket) + Officer(vehicle)

Problem 2: Library System (Day 3-4)
  Entities: Library, Book, BookCopy, Member, Loan, Reservation
  Features: Search, borrow, return, reserve, fine calculation
  Pattern:  Observer (availability notification), Strategy (search)
  GSTN Map: Directly mirrors CaseMgmtFwk — getCaseList, createCase, updateCase

Problem 3: Elevator (Day 5-6)
  Entities: ElevatorSystem, Elevator, Floor, Request, Direction
  Features: Add request, dispatch nearest elevator, optimize direction
  Pattern:  Strategy (scheduling: FCFS / SCAN / LOOK), Observer (floor arrival)
  GSTN Map: WorkFlowFwk task queue — tasks arrive, get assigned, processed

Day 7: Review all 3. Write a 1-page design document for each.
```

**Week 5 — Domain-Adjacent Problems**
```
Problem 4: Demand Ledger Engine (Day 1-3) ← YOUR STRONGEST
  Entities: Demand, DCREntry (type: DR/CR), EntryCategory, Transfer
  Features: createDemand, addCredit, transferOut/In, computeBalance, getStatus
  Schema:
    demand_master: demand_id, gstin, demand_type, created_at
    dcr_entries:   id, demand_id, entry_type(DR/CR), category, amount, ref_demand_id

  Core logic:
    computeOutstanding(demandId) = Σ(DR entries) - Σ(CR entries)
    getStatus:
      outstanding > 0  → PENDING
      outstanding == 0 → SETTLED
      outstanding < 0  → REFUND_DUE

  Pattern:  Immutable event log (event sourcing lite)
  Test:     All 6 appeal scenarios as integration tests

Problem 5: Notification System (Day 4-5)
  Entities: NotificationService, Channel(EMAIL/SMS/PUSH), Template, Message, User
  Features: Send, retry failed, bulk, user preference (channel priority)
  Pattern:  Strategy (channel), Observer, Chain of Responsibility (retry)
  GSTN Map: SendEmailSMSReq VO + Kafka consumer

Problem 6: Workflow Engine (Day 6-7)
  Entities: Workflow, Step, Task, Assignment, Status, Transition
  Features: Create workflow, assign task, complete task, auto-escalate on SLA breach
  Pattern:  State machine, Strategy (assignment algorithm), Observer (escalation trigger)
  GSTN Map: WorkFlowFwk — directly mirrors this
```

**Week 6 — Advanced Problems**
```
Problem 7: Rule Engine (Day 1-2)
  Input: Map<String, Object> facts
  Rules: List<Rule> where Rule has condition (Predicate) + action (Consumer)
  Engine: evaluate all rules, fire matching ones
  GSTN Map: 12-scenario Subsequent Order matrix IS a rule engine:
    Rule("D2=Confirmed AND D3=Rejected") → action: reverseDisputeAmt + closeD2 + transferToD1

Problem 8: Audit Trail System (Day 3-4)
  Features: Log every state change with: who, what, when, from-state, to-state, payload
  Design:   Append-only table + async Kafka ingestion + search API
  GSTN Map: AuditMstrDetlEntity + AuditFormJsonEntity

Problem 9: Idempotent API (Day 5-6)
  Design:   Idempotency key in header → check Redis → if exists return cached response
             If not exists → process → store in Redis with TTL → return response
  GSTN Map: draftId on Case.java, duplicate APL04 prevention

Day 7: Full mock — pick random problem, 90 minutes, no help.
```

---

### Phase 3: HLD System Design (Weeks 7-9)
**Goal: Confidently design any system from scratch in 45 minutes**

**Week 7 — Core HLD Building Blocks**

Learn each component deeply before using in system designs:

```
Day 1: Load Balancer
  Types: L4 (TCP) vs L7 (HTTP/HTTPS)
  Algorithms: Round Robin, Weighted, Least Connections, IP Hash (sticky sessions)
  Tools: Nginx, HAProxy, AWS ALB
  Practice: Draw LB in front of LitigationAPI cluster

Day 2: Caching Deep Dive
  Strategies: Cache-aside (your Redis pattern), Write-through, Write-behind, Refresh-ahead
  Eviction: LRU, LFU, TTL
  Consistency: Cache invalidation on update — how does DistCacheFwk handle it?
  Redis data structures: String, Hash (use for Case metadata), SortedSet (leaderboard/priority)

Day 3: Database Scaling
  Read replicas: Write to primary, read from replicas — for case list queries
  Sharding: By stateCd (your GSTN natural partition) — shard key choice matters
  Partitioning: Range (by date), Hash (by GSTIN), List (by state)

Day 4: Message Queue Deep Dive
  Kafka internals: Topic → Partition → Offset, Consumer Group, Rebalancing
  Guarantees: at-most-once, at-least-once, exactly-once
  Use cases: ORDER_ISSUED event (at-least-once + idempotent consumer = effectively exactly-once)

Day 5: Distributed Systems Concepts
  Consistent hashing: for distributing load across Redis cluster nodes
  Quorum: N=3, W=2, R=2 → strong consistency
  Vector clocks: conflict resolution in concurrent updates

Day 6: API Design
  REST best practices, idempotency, pagination (cursor vs offset — your GSTN uses offset)
  Versioning strategy: URI (/v1/ vs /v2/) — your LitigationAPI versioning

Day 7: Observability
  Metrics: Prometheus + Grafana
  Tracing: Zipkin/Jaeger — correlation IDs (your GSTN uses this for request tracing)
  Logging: ELK stack — centralized, structured JSON logs
```

**Week 8 — Domain Systems (Your Area)**

```
Day 1-2: Design GST Litigation Platform (Your Case Study)
  Follow the full framework:
  1. Requirements: 1.4Cr users, 2M cases/year, legal compliance, ACID for financial
  2. Capacity: 2M cases/year = ~5500/day = ~230/hour = ~4/min (low but spiky at deadline)
  3. Architecture: See flagship answer in Section 5 above
  4. Deep dive: DB schema, Kafka topics, Redis keys, API contracts
  5. Bottlenecks: How to handle March 31 / GST filing deadline traffic spikes?

Day 3-4: Design Distributed Ledger System
  Core insight: DCR entries = append-only event log = Event Sourcing
  Read model: Materialized view of outstanding amount per demand
  CQRS: Write (addDCREntry) → separate read (getDemandBalance)
  Consistency: Strong for financial entries (XA or Saga)

Day 5-6: Design Workflow Orchestration
  Patterns: Saga orchestration (your Subsequent Order coordinator)
  vs Saga choreography (Kafka events between services)
  Your example: Subsequent Order is orchestration — single coordinator drives D1/D2/D3

Day 7: Mock HLD — 45 min — "Design a Legal Case Management Platform"
```

**Week 9 — General High-Scale Systems**

```
Day 1-2: Design Twitter/Instagram Feed
  Concepts: Fan-out on write vs fan-out on read, celebrity problem
  Components: Post service, Timeline service, Feed cache (Redis sorted set)

Day 3-4: Design Uber/Ola
  Concepts: Geospatial index (geohash, S2), matching algorithm, surge pricing
  Components: Location service, matching service, trip service

Day 5-6: Design WhatsApp
  Concepts: WebSocket, message ordering, delivery receipts, end-to-end encryption
  Components: Connection manager, message store, notification service

Day 7: Mock — 45 min — any random HLD
```

---

### Phase 4: Finalization (Weeks 10-12)

**Week 10 — Mock Interviews**
```
Day 1-2:  LLD mock × 2 (Pramp.com / Interviewing.io / friend)
Day 3-4:  HLD mock × 2
Day 5:    Java deep dive mock (HashMap internals, GC, concurrency)
Day 6-7:  Behavioral + Past Work deep dive mock
```

**Week 11 — Gap Filling**
```
Review every ❌ from Phase 0 audit
Target: 0 remaining ❌ marks
DSA: 3 LeetCode mediums/day — Trees, Graphs, DP, Sliding Window
```

**Week 12 — Polish**
```
Day 1-2:  Resume final review — 5 people outside GSTN read it, collect feedback
Day 3-4:  Prepare 5 behavioral stories (STAR format)
Day 5-7:  Apply to target companies
```

---

## 7. PROJECTS TO BUILD

### Project 1 — Mini Case Management System (mirrors CaseMgmtFwk)
**Tech:** Spring Boot + MySQL + JPA + Redis
**Time:** 2 weekends
```
APIs:
  POST /cases              → create case (APPEAL / ADJUDICATION / DCR)
  PUT  /cases/{id}/status  → state transition with validation
  GET  /cases/{id}/folders → list folders
  POST /cases/{id}/orders  → issue order (triggers ledger entry)

Key implementations:
  - State machine: illegal transitions throw CaseStateException
  - Strategy pattern: AppealCaseCustomizer, AdjudicationCaseCustomizer
  - @Version optimistic locking on Case entity
  - Redis cache for case type master data
  - @Transactional(propagation=REQUIRES_NEW) for ledger entries
```

### Project 2 — Demand Ledger Engine (mirrors LedgerUtilFwk)
**Tech:** Spring Boot + MySQL
**Time:** 1 weekend
```
APIs:
  POST /demands                → createDemand (DR entry)
  POST /demands/{id}/credit    → add credit (payment/dispute/transfer)
  POST /demands/{id}/transfer  → transferOut → transferIn
  GET  /demands/{id}/balance   → outstanding amount
  GET  /demands/{id}/status    → PENDING / SETTLED / REFUND_DUE

Schema:
  CREATE TABLE demands (
    id VARCHAR(50) PRIMARY KEY,
    gstin VARCHAR(15),
    demand_type VARCHAR(20),
    created_at TIMESTAMP
  );

  CREATE TABLE dcr_entries (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    demand_id VARCHAR(50),
    entry_type ENUM('DR','CR'),
    category ENUM('DEMAND','PAYMENT','DISPUTE','TRANSFER_IN','TRANSFER_OUT'),
    amount DECIMAL(15,2),
    ref_demand_id VARCHAR(50),
    idempotency_key VARCHAR(100) UNIQUE,  ← prevents duplicate entries
    created_at TIMESTAMP
  );

Tests: Write all 12 Subsequent Order scenarios as integration tests.
```

### Project 3 — Appeal Order Workflow API (Your Resume Project)
**Tech:** Spring Boot + Kafka + Redis + MySQL
**Time:** 3 weekends
```
APIs:
  POST /appeals/{caseId}/issue-order      → issue APL04 (Modified/Confirmed/Rejected)
  POST /appeals/{caseId}/subsequent-order → D1→D2→D3 chain

Flow for issue-order:
  1. Validate state (case must be ADMITTED)
  2. Acquire distributed lock (Redis SETNX) — prevent concurrent issuance
  3. Compute DCR entries based on outcome type
  4. @Transactional: update demand statuses + create DCR entries
  5. Publish Kafka event: ORDER_ISSUED
  6. Release lock
  7. @Async Kafka consumer: send notification

Tests: 12 integration test cases (one per scenario in decision matrix)
```

---

## 8. PLATFORM-LEVEL LEARNING RESOURCES

### For LLD

| Resource | What to Learn | Priority |
|---|---|---|
| **Refactoring Guru** (refactoring.guru/design-patterns) | All 23 GoF patterns with Java examples | HIGH |
| **Head First Design Patterns** (book) | Best visual explanation of patterns | HIGH |
| **LeetCode Explore — OOP** | Machine coding style problems | MEDIUM |
| **Workat.tech** | Machine coding problems with editorial | HIGH |
| **GitHub: ashishps1/awesome-low-level-design** | 50+ LLD problems with Java solutions | HIGH |

### For HLD

| Resource | What to Learn | Priority |
|---|---|---|
| **System Design Primer** (github.com/donnemartin/system-design-primer) | Complete HLD reference | HIGH |
| **Designing Data-Intensive Applications** (book by Martin Kleppmann) | Kafka, databases, distributed systems | MUST READ |
| **ByteByteGo** (YouTube + newsletter) | Visual system design explanations | HIGH |
| **Gaurav Sen** (YouTube) | HLD from scratch, very clear | HIGH |
| **High Scalability Blog** (highscalability.com) | Real architectures from top companies | MEDIUM |
| **AWS Architecture Center** | Cloud-native patterns | MEDIUM |

### For Java Deep Dive

| Resource | What to Learn | Priority |
|---|---|---|
| **Java Concurrency in Practice** (book by Brian Goetz) | Threading, locks, concurrent collections | HIGH |
| **Baeldung.com** | Spring Boot, JPA, Security tutorials | HIGH |
| **Vlad Mihalcea Blog** | Hibernate/JPA internals, N+1, locking | HIGH |
| **JVM Internals** (blog.jamesdbloom.com) | JVM architecture, GC, classloading | MEDIUM |

### For DSA

| Resource | Platform | Focus |
|---|---|---|
| **NeetCode 150** | LeetCode | Curated 150 problems covering all patterns |
| **Striver's SDE Sheet** | takeuforward.org | Systematic by topic |
| **LeetCode Company Tags** | LeetCode | Filter by target company (Flipkart, Razorpay, etc.) |

### Weekly Schedule Template
```
Monday:    Java/Spring deep dive (2 hrs theory + code)
Tuesday:   LLD machine coding practice (90 min)
Wednesday: HLD system design (45 min problem + 30 min review)
Thursday:  DSA (2 LeetCode mediums)
Friday:    Build/extend your projects (2 hrs)
Saturday:  Mock interview (LLD or HLD, 45 min) + review
Sunday:    Review week notes + plan next week
```

---

## 9. INTERVIEW ANSWER TEMPLATES

### "Tell me about yourself" (30 seconds)

> "I'm Jayanti, with 5.6 years of backend and full-stack experience at GSTN — India's national
> GST infrastructure platform serving 1.52 crore taxpayers. I've worked in the Litigation and
> Appeal module, where I owned complex financial workflows end-to-end — from system design to
> production delivery. I'm now targeting SDE-2/SDE-3 roles at product companies where I can work
> on high-scale, high-complexity systems."

---

### "Walk me through a complex feature you built" (3-4 minutes)

> "At GSTN, I owned the Simultaneous Appeal and Subsequent Order feature in the litigation module.
>
> **The problem:** When a taxpayer files APL01 (their appeal) AND the tax department files APL03
> on the same demand simultaneously, we needed to issue a single combined order — but the
> issuance could come from either side. Additionally, when a higher court issues a Subsequent
> Order on top of an existing appeal order, the financial impact cascades across multiple demand
> accounts.
>
> **The complexity:** I had to handle a 12-scenario decision matrix — based on whether the first
> appeal was Modified, Confirmed, or Rejected, and whether the Subsequent Order was Modified,
> Confirmed, or Rejected, different financial operations had to happen. For example, Confirm-Reject
> means reversing the first appeal dispute amount, crediting the determined amount back to D2, and
> transferring payments from D2 back to D1. Whereas Confirm-Confirm means creating a brand new
> D3 demand, closing D2, and crediting the predeposit/admitted amount into D3.
>
> **Key design decisions:**
> 1. **Rule Engine pattern** — the 12-scenario matrix as a decision table, not hardcoded if-else
> 2. **XA distributed transaction** — issuing an order must atomically update 3 DBs: litigation case,
>    demand ledger, and workflow tasks
> 3. **Simultaneous Combine payload transformation** — when APL03-side issues the order, we
>    transform the payload and store it in the APL01 case folder, because legally only one order
>    can exist per demand
> 4. **Optimistic locking** — `@Version` on the case entity to prevent two officers issuing the
>    same order concurrently
>
> **Result:** The feature went live supporting lakhs of taxpayers with active appeals, with zero
> financial discrepancy incidents reported."

---

### "Why do you want to leave GSTN?" (Be honest, positive framing)

> "GSTN gave me incredible exposure to complex, high-scale systems and real business domain
> depth. However, it's a government-contracted system with a slow release cycle and limited
> exposure to cloud-native, modern tech stacks. I want to work in an environment with faster
> iteration, exposure to distributed systems at internet scale, and engineering culture that
> values technical excellence — which is what I see at [target company]."

---

### "What's your biggest technical challenge?" (From your GSTN work)

> "The hardest problem I solved was the concurrent order issuance race condition. Two back-office
> officers could simultaneously try to issue an APL04 order on the same DRC07 demand. Without
> proper handling, both would pass the validation check, and we'd have two orders in the system —
> which is legally invalid for a government tax system.
>
> I solved it with two layers: first, optimistic locking (`@Version` on the Case entity in JPA) which
> causes one of the concurrent requests to fail with an `OptimisticLockException`. Second, a Redis
> distributed lock (`SETNX demandId EX 30`) acquired at the beginning of order issuance, ensuring
> only one request proceeds even across multiple API server instances.
>
> This taught me to always think about concurrency at both the application layer and the database
> layer for critical financial operations."

---

### STAR Behavioral Stories (Have 5 ready)

**Story 1: Technical Leadership**
```
S: GSTN needed to handle 12-scenario Subsequent Order financial logic without creating
   unmaintainable spaghetti code
T: Design an extensible, testable solution for the branching financial logic
A: Proposed and implemented a rule engine pattern — each scenario as a named rule with
   a condition predicate and an action consumer. Wrote 12 integration tests, one per scenario.
R: Code is readable (any new developer can follow), fully tested, and adding a new scenario
   requires adding one rule — not modifying existing code.
```

**Story 2: Problem Solving Under Pressure**
```
S: During GST filing deadline, production found that Transfer-Out was being calculated
   incorrectly for APL03 cases with partial payments — affecting real taxpayer balances
T: Fix critical production bug in the financial calculation with zero tolerance for error
A: Reproduced the issue locally with exact test data. Traced to APL01 vs APL03 outstanding
   amount calculation difference (APL01 always negative, APL03 can be positive/zero/negative).
   Added the conditional branch. Wrote regression tests covering all 3 APL03 outstanding states.
R: Hotfix deployed in 4 hours. Zero further financial discrepancies. Added scenario to test suite.
```

---

## 10. GSTN TO STANDARD PROBLEM CHEAT SHEET

| Asked in Interview | Your Real GSTN Equivalent | How to Open Your Answer |
|---|---|---|
| Design Parking Lot | Case Management (cases=slots, tasks=tickets) | "I've built a more complex version — CaseMgmtFwk..." |
| Design Vending Machine | Appeal State Machine (5 states, 8 transitions) | "Same FSM pattern — let me show with my appeal case states..." |
| Design Chess / Game Engine | Subsequent Order rule engine (12 scenarios) | "I designed a rule engine for legal orders — input is (D2_outcome, D3_outcome)..." |
| Design LRU Cache | DistCacheFwk Redis layer with TTL | "In production I used Redis with TTL-based eviction..." |
| Design Rate Limiter | APL01 filing throttle per GSTIN per day | "In GST portal, each GSTIN is rate-limited..." |
| Design Notification | Kafka post-APL04 order issuance | "Post-commit Kafka event, decouple legal order from notification..." |
| Design ATM | Demand payment flow (check balance → debit → receipt) | "Same flow — DCR debit/credit entry system..." |
| Design Splitwise | DCR Transfer In/Out between demand accounts | "Exact double-entry bookkeeping pattern — debit one account, credit another..." |
| Design Logger | GstAopFwk + SLF4J + correlation IDs | "Used AOP-based structured logging with request correlation IDs..." |
| Design Distributed Lock | Redis SETNX for concurrent APL04 prevention | "SETNX demandId EX 30 — in production for order issuance..." |
| Design Event Sourcing | DCR entries = immutable event log | "Our demand ledger IS event sourcing — each DR/CR is an immutable event..." |
| Design Workflow Engine | WorkFlowFwk — task lifecycle, SLA, escalation | "I built on top of a workflow engine — here's its architecture..." |
| Design a Rule Engine | 12-scenario Subsequent Order decision tree | "I built this — condition predicate + action consumer pattern..." |
| Design Audit Trail | AuditMstrDetlEntity + AuditFormJsonEntity | "Append-only audit log — same pattern I've implemented in production..." |

---

## QUICK REFERENCE CARD (Print and Keep)

### Design Pattern in One Line Each
```
Singleton    → One instance globally (Redis manager)
Factory      → Create object by type at runtime (CaseCustomizerFactory)
Abstract Factory → Family of related objects
Builder      → Complex object step-by-step (CaseRequestBuilder)
Prototype    → Clone existing object

Strategy     → Swap algorithm at runtime (CaseCustomizer per case type)
Observer     → Notify multiple on change (Kafka events)
Template Method → Base algo, override steps (GenericCaseHandler)
Command      → Encapsulate request as object (Task in WorkFlowFwk)
Chain of Responsibility → Pass through handlers (Spring Security filter chain)
State        → Behavior changes with state (Appeal state machine)
Facade       → Simple interface over complex subsystem (CaseHandler)
Decorator    → Add behavior without changing class (AOP)
Adapter      → Convert interface (LitigationAPI1 → API2 migration)
Composite    → Tree structure (Case → Folders → Items)
```

### CAP Theorem Quick Ref
```
C = Consistency   (all nodes see same data)
A = Availability  (system always responds)
P = Partition Tolerance (survives network splits — ALWAYS required in distributed)

CP → MySQL, MongoDB, ZooKeeper → Choose for: banking, legal, GSTN
AP → Cassandra, DynamoDB, CouchDB → Choose for: social feeds, analytics, IoT
```

### Transaction Propagation Quick Ref
```
REQUIRED      → Join existing OR create new (default)
REQUIRES_NEW  → Always new (D3 demand creation — don't roll back on D2 failure)
NESTED        → Savepoint inside existing
SUPPORTS      → Use existing if present, else non-transactional
NOT_SUPPORTED → Suspend existing, run non-transactionally
NEVER         → Fail if transaction exists
MANDATORY     → Fail if NO transaction exists
```

### HTTP Status Codes Quick Ref
```
200 OK           → GET success
201 Created      → POST success (case created)
204 No Content   → DELETE success
400 Bad Request  → Invalid input
401 Unauthorized → Not authenticated
403 Forbidden    → Authenticated but not authorized (wrong jurisdiction)
404 Not Found    → Case/demand doesn't exist
409 Conflict     → Optimistic lock failure / duplicate case
422 Unprocessable → Semantic validation failed (invalid state transition)
500 Server Error → Bug / unhandled exception
```

---

## 11. ATS-FRIENDLY BULLET REWRITES

### What ATS Systems Scan For
- Exact keyword matches against the job description
- Action verbs at the start of each bullet
- Quantified numbers (`15.2 million`, `3 databases`, `20+ types`)
- No markdown formatting characters (`**`, `—`, `→`, `•`) in the resume document itself

### ATS Problems in Markdown — Fix Before Pasting to Resume

| Problem | Why ATS Fails | Fix |
|---|---|---|
| `**Bold text**` inside bullet | `**` symbols appear as literal characters | Remove all bold from bullet text |
| Em dash `—` (unicode) | Many parsers read as garbled character | Replace with `: ` or ` - ` |
| `→` arrows | Unicode, not ASCII | Remove or replace with `->` |
| `15.2M` | Write as `15.2 million` or `1.52 crore` — avoid abbreviated M notation | Write `15.2 million` |
| Two-column layout (Word/PDF) | ATS reads left column, skips right | Use single column only |
| Contact info in header/footer | ATS skips headers/footers | Put contact in body |
| Tables for skills section | Parsed as garbled text | Use plain comma-separated list |

### ATS-Safe Versions of Your Top Bullets (Copy-Paste Ready)

```
Designed a 12-scenario appellate order processing engine for a national tax
litigation platform using a decision-matrix state machine across a 3-tier demand
account chain, handling conditional demand creation, inter-account balance
transfers, dispute reversals, and refund-due triggers in Java and Spring Boot

Engineered a double-entry financial ledger engine tracking debit and credit entries
per demand account, automating status transitions to Settled or Refund Due using
JPA and MySQL transactions on a platform serving 140 million registered taxpayers

Implemented XA distributed transactions using Atomikos 2-phase commit to guarantee
atomicity across three independent databases during adjudication order issuance in
a legally binding tax compliance system serving 140 million taxpayers

Architected a plugin-based case lifecycle framework using Strategy and Factory
design patterns supporting 20 legally distinct proceeding types, enabling new case
types to be added without modifying core framework code (Open-Closed Principle)

Built concurrent multi-party appeal processing where taxpayer and department
appeals on the same demand are resolved via a single unified adjudication order
using payload transformation logic and distributed locking with Redis

Reduced repeated database lookups by 60 to 80 percent during peak filing windows
by implementing a Redis distributed cache with TTL-based eviction for jurisdiction
and master data across a platform serving 140 million registered taxpayers
```

### ATS-Safe Power Bullet
```
Owned end-to-end design and delivery of a tax appellate order management system on
India's national GST platform serving 140 million taxpayers: implemented a
12-scenario demand state machine with double-entry ledger engine, XA distributed
transactions across 3 databases, and concurrent multi-party appeal processing using
Strategy and Factory design patterns on a Java, Spring Boot, and Angular stack
```

### Keywords to Add to Your Resume Skills Section (ATS Match)
```
Java, Spring Boot, Spring MVC, Spring Security, Microservices, REST API, JPA,
Hibernate, MySQL, Redis, Apache Kafka, Angular, TypeScript, Distributed Systems,
Design Patterns, OOP, SOLID Principles, Multithreading, Concurrency, SQL,
Transactions, System Design, Git, Maven, Agile, Unit Testing, Integration Testing,
High Availability, Scalability, Event-Driven Architecture, XA Transactions,
Aspect-Oriented Programming, Workflow Orchestration
```

### Free ATS Checker Tools
- **Jobscan.co** - paste your resume + JD, shows percentage match and missing keywords
- **Resume Worded** (resumeworded.com) - line-by-line ATS feedback
- **LinkedIn Easy Apply preview** - see how LinkedIn ATS parses your resume

---

## 12. WHAT ELSE TO LEARN FROM THIS CODEBASE

> These are real, production-grade patterns inside your GSTN frameworks.
> You have worked around them or on top of them every day.
> For each one: (1) read the actual code in the repo, (2) understand WHY it was designed that way,
> (3) build a small project, (4) add the bullet to your resume and the talking point to your memory.

### Master Priority Table

| # | Pattern | Repo Class | Learn In | Rarity on Resumes | SDE-2/3 Signal |
|---|---|---|---|---|---|
| 12.1 | Spring AOP + Kafka Audit | GstAopFwk / BoApiAuditAspect | 1 week | Rare | Framework thinking |
| 12.2 | ThreadLocal + AbstractRoutingDataSource (multi-tenant DB routing) | WorkFlowFwk / DbContextHolder + RoutingDataSource | 3 days | Very rare | Senior-level infra |
| 12.3 | HBase + custom functional API (GSTFunction/GSTPredicate) | HbaseAccessFwk / layer1 | 1 week | Rare | NoSQL + FP |
| 12.4 | XA Workflow with jurisdiction routing | WorkFlowFwk / WFXAService | 1 week | Very rare | Distributed TX |
| 12.5 | 40+ type distributed cache with Factory | DistCacheFwk | 1 week | Medium | Cache mastery |
| 12.6 | Kafka Protobuf + manual ack + DLQ | KafkaConsumerFwk | 1 week | Rare | Production Kafka |
| 12.7 | 100+ master type in-memory local cache | LocalCacheFwk / RefDataService | 3 days | Medium | Performance thinking |
| 12.8 | Multi-auth: OTP, DSC, G2G, Risk-Based Auth | AuthenticationFwk | 1 week | Very rare | Security depth |
| 12.9 | Custom Spring Boot Starter | springboot-starter-gstn | 3 days | Rare | Platform engineering |

---

### 12.1 Aspect-Oriented Programming (AOP) — GstAopFwk
**What exists in your code:**
```
GstAopFwk/
  aspects/
    BoApiAuditAspect.java   - @Around advice: captures HTTP request+response,
                              reads audit config from DB, publishes to Kafka
    LoggingAspect.java      - @Before/@AfterReturning/@AfterThrowing: structured
                              method entry/exit/exception logging
  annotations/
    @BoApiAudit             - custom annotation to trigger audit on any controller
    @Loggable               - custom annotation to trigger structured logging
    @NonLoggable            - opt-out annotation
```
**What is impressive here:**
- `BoApiAuditAspect` reads DB-driven audit config at runtime (toggle per API without redeploy)
- Publishes audit logs to Kafka asynchronously — zero impact on main request thread
- `@NonLoggable` on sensitive fields prevents PII from leaking into logs

**What to learn:**
- How Spring AOP proxy works (JDK dynamic proxy vs CGLIB)
- Pointcut expressions: `@within`, `@annotation`, `execution(* *(..))`
- `ProceedingJoinPoint` — how `proceed()` executes the actual method
- Why AOP can't intercept `private` or `final` methods (proxy limitation)

**Resume bullet (after learning):**
```
Implemented a database-driven API audit framework using Spring AOP @Around advice
that captures HTTP request and response payloads, loads per-API audit configuration
at runtime from a config table, and publishes structured audit logs asynchronously
to Kafka - enabling audit toggling per API without any redeployment
```

**Build project:**
Spring Boot app with custom `@Auditable` annotation. When placed on any controller
method, captures: user, endpoint, request body, response body, latency, timestamp.
Store in DB + publish to Kafka. Support runtime toggle via DB flag.

---

### 12.2 ThreadLocal + AbstractRoutingDataSource — Dynamic Multi-Tenant DB Routing

**What exists in your code (WorkFlowFwk):**
```java
// DbContextHolder.java — ThreadLocal holds current DB key per request thread
public class DbContextHolder {
    private static final ThreadLocal<DbType> CONTEXTHOLDER = new ThreadLocal<>();

    public static void setDbType(DbType dbType) { CONTEXTHOLDER.set(dbType); }
    public static DbType getDbType()             { return CONTEXTHOLDER.get(); }
    public static void clearDbType()             { CONTEXTHOLDER.remove(); }
}

// RoutingDataSource.java — Spring picks datasource based on ThreadLocal value
public class RoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DbContextHolder.getDbType();  // returns R1, R2, R3 etc (regions)
    }
}

// Usage — before any DB call, set the region key on the thread
private void setDbRouting(String stateCd) {
    String stRegion = gstProperty.getProperty("STAT_" + stateCd + "_CORE");
    DbContextHolder.setDbType(DbType.valueOf(stRegion));  // e.g. R1, R2
}
```

**What is impressive here:**
- GSTN shards its database by state code (28 Indian states = multiple DB regions)
- `ThreadLocal` stores the DB key scoped to the current request thread — zero contention
- `AbstractRoutingDataSource` is Spring's routing hook — picks correct datasource from a map
- The pattern enables one application to talk to N databases transparently via the same DAO code
- `clearDbType()` must be called after request — else the thread (from pool) carries stale state

**The mental model:**
```
Request for stateCd="07" (Delhi)
    → setDbRouting("07") → property lookup → "R1"
    → DbContextHolder.setDbType(R1)   [stored in ThreadLocal]
    → DAO executes query
    → RoutingDataSource.determineCurrentLookupKey() → returns "R1"
    → Spring selects datasource R1 from map
    → query hits Region-1 DB
    → DbContextHolder.clearDbType()   [MUST clean up]
```

**Why this is an SDE-2/3 signal:**
Most developers know basic Spring datasource config. Very few know how to implement
runtime datasource routing with ThreadLocal. This pattern is used at Flipkart, Zomato,
PayTM for database sharding without code-level if-else per region.

**What to learn:**
- `ThreadLocal` lifecycle: created per thread, never shared, must be cleaned up
- `ThreadLocal` memory leak: if not cleaned in finally block, stays in thread pool thread forever
- `AbstractRoutingDataSource.setTargetDataSources(Map)` — how you configure the datasource map
- `InheritableThreadLocal` — child threads inherit parent's value (use for async tasks)
- Comparison to `@Transactional(readOnly=true)` routing — less flexible, only read vs write

**Interview answer — "How did your system route database calls to the right shard?"**
> "We used Spring's AbstractRoutingDataSource with ThreadLocal. Before any DB call,
> we resolve the state code from the request to a region key (R1, R2, R3) and store it
> in a ThreadLocal via DbContextHolder. RoutingDataSource overrides determineCurrentLookupKey()
> to return that value, and Spring picks the matching datasource from a pre-configured map.
> After the call, we always clear the ThreadLocal in a finally block to prevent state
> leaking to the next request on the same pooled thread."

**Resume bullet (after learning):**
```
Implemented runtime database sharding using Spring AbstractRoutingDataSource and
ThreadLocal-based context holder, dynamically routing all DAO calls to the correct
regional database based on state code from the request — enabling a single codebase
to serve 28 state-wise database partitions transparently without DAO-level branching
```

**Build project:**
Spring Boot app with 2 H2 datasources (db-north, db-south). `@RestController` accepts
`region=NORTH/SOUTH` header. `DbContextHolder` stores it in ThreadLocal. RoutingDataSource
routes to correct H2. Write test: NORTH requests → db-north, SOUTH → db-south.
Add a leak test: omit clearDbType(), verify next request gets wrong DB.

---

### 12.3 HBase Framework with Custom Functional API — GSTFunction / GSTPredicate

**What exists in your code (HbaseAccessFwk):**
```java
// GSTFunction.java — custom Function<T,R> with Model validation
public interface GSTFunction<T, R> {
    R apply(T t) throws HBaseFwkIllegalArgumentException;
    Model applicableModel();  // which HBase table/model this operates on

    // composable: f.compose(g) = x -> f(g(x))
    default <V> GSTFunction<V, R> compose(GSTFunction<? super V, ? extends T> before) {
        // validates both functions target same HBase model
        Model model = GstUtil.validateAndReturnModel(this.applicableModel(), before.applicableModel());
        ...
    }
}

// GSTPredicate.java — custom Predicate<T> with Model validation
public interface GSTPredicate<T> {
    boolean test(T t);
    Model applicableModel();
    default GSTPredicate<T> and(GSTPredicate<? super T> other) { ... }
    default GSTPredicate<T> or(GSTPredicate<? super T> other)  { ... }
    default GSTPredicate<T> negate()                           { ... }
}

// Model.java — describes HBase table: row key format, column families,
//              dynamic columns, const columns, column-CF mapping
public final class Model {
    private final String HBaseTableName;
    private final RowKey rowKeyFormat;
    private final Map<String, List<Column>> dynamicColumns;
    private final Map<String, List<Column>> constColumns;
    private final Map<String, Column> nameColumnMap;
    private final Map<String, byte[]> nameCFBytesMap;
    private final boolean isSimilarColumnModel;
    private final boolean modelHasFullyDynamicColumn;
}
```

**What is impressive here:**
- GSTN built its own type-safe HBase ORM — like JPA but for HBase column families
- `GSTFunction` extends Java `Function<T,R>` with Model-aware composition — prevents
  cross-table operation bugs at compile time
- `GSTPredicate` adds composable, chainable HBase row filters (and/or/negate)
- `Model` encodes row key format + column family structure — entire schema in code
- `Mutator.java`, `Reader.java`, `Loader.java` — full read/write abstraction over HBase client

**What to learn:**
- HBase data model: namespace → table → row key → column family → column qualifier → cell
- Row key design is everything: bad row key = hot spot = all traffic hits one region server
- Column families: physical separation on disk; keep related columns in same CF
- Scan vs Get: `Get` = single row by key O(1), `Scan` = range of rows by key prefix
- Why HBase for GSTN: return filing data (GSTR1, GSTR3B) is massive and sparse — HBase handles this better than MySQL
- Java `Function.compose()` vs `andThen()`: `f.compose(g)` = f(g(x)), `f.andThen(g)` = g(f(x))

**Interview answer — "Why HBase over MySQL for return data?"**
> "Return filing data is sparse and massive — millions of taxpayers file monthly with
> hundreds of line items each. With MySQL you'd need wide tables with many nullable columns
> or complex normalization with expensive joins. HBase's column family model stores only
> the columns that exist for each row — sparse rows don't waste space. Row key design by
> GSTIN+period gives O(1) Get for any taxpayer's return. And HBase scales horizontally
> across RegionServers as data grows — MySQL would need sharding with application-level
> routing for the same scale."

**Resume bullet (after learning):**
```
Worked with a custom HBase access framework implementing a type-safe functional API
(GSTFunction/GSTPredicate with model-aware composition) for reading and writing
GST return filing data — enabling composable, schema-validated HBase operations
with row key design optimized for per-taxpayer-per-period access patterns at scale
```

**Build project:**
Spring Boot + HBase (Docker) + custom `HBaseTemplate<T>`. Define a `Model` for a user
table (row key: userId, CF: personal, CF: prefs). Write `GSTFunction<UserId, UserRow>`
and `GSTPredicate<UserRow>` for age filter. Compose them: find all active premium users.

---

### 12.4 Multi-Authentication Framework — AuthenticationFwk

**What exists in your code:**
```java
// Authentication2Service.java — multiple auth strategies in one interface:
authenticateUser(userName, credential, role, accessMode, request)  // password
authenticateTrnUser(id, mbno, email, applnType, stateCd, trn,
                    lgnmbz, inputOtp, request)                      // OTP
authenticateBoUserOtp(username, credential, accessMode, request)   // BO OTP
getBoDscUserDetails(userName, role, ip, accessMode)                // DSC (Digital Signature Cert)
authenticateG2GUser(userName, password)                            // G2G (govt-to-govt)
authenticateCommUser(userName, password)                           // common user
generateAuthTokenForUIDLogin(uid, role, refNum, userIP, request)   // UID (Aadhaar)
generateAuthTokenForARLogin(arId, role, arRefId, userIP, request)  // Authorised Rep
getRiskCategory(rbaAuthVo)                                         // Risk-Based Auth (RBA)
getPostRBAuthResult(userName, riskDeviceID, otpAuth, callerId)     // RBA post-auth
```

**What is impressive here:**
- 10+ distinct authentication strategies in one unified service interface = Strategy pattern
- **Risk-Based Authentication (RBA)**: system assesses device fingerprint + user behaviour
  to compute risk category → low risk → password only; high risk → force OTP
- **DSC (Digital Signature Certificate)**: hardware-based auth for tax officers
- **G2G authentication**: government-to-government API authentication with audit trail
- `Authentication2AuditService` — every auth attempt separately audited

**The authentication strategy tree:**
```
Incoming Request
    ├── Taxpayer (FO)
    │     ├── Password login             → authenticateUser()
    │     ├── OTP login (mobile/email)   → authenticateTrnUser()
    │     └── Aadhaar (UID) login        → generateAuthTokenForUIDLogin()
    ├── Back-Office (BO) Officer
    │     ├── Password + OTP             → authenticateBoUserOtp()
    │     └── DSC (Digital Signature)    → getBoDscUserDetails()
    ├── Authorised Representative (CA)   → generateAuthTokenForARLogin()
    └── Government API (G2G)             → authenticateG2GUser()
    
Cross-cutting:
    Risk-Based Auth: every login → getRiskCategory() → escalate if high risk
```

**What to learn:**
- OAuth 2.0 flows: Authorization Code, Client Credentials, PKCE — how tokens are issued
- JWT structure: header.payload.signature, claims (sub, exp, iat, roles), verification
- Risk-Based Authentication: device fingerprinting, IP reputation, behavioural analytics
- DSC: PKI basics — public/private key, certificate chain, signing and verification
- Session vs token: GSTN uses token-based (stateless) — why this scales better
- `UserSession` vs `BOUserSession` — different session models for different user types

**Resume bullet (after learning):**
```
Worked with a multi-strategy authentication framework supporting 10+ login flows
(password, OTP, Aadhaar UID, Digital Signature Certificate, G2G, Risk-Based
Authentication) built as a Strategy pattern with unified interface — with
Risk-Based Auth dynamically escalating authentication strength based on
device fingerprint and behavioural risk score
```

---

### 12.5 In-Memory Local Cache with 100+ Master Types — LocalCacheFwk

**What exists in your code (LocalCacheFwk / RefDataService.java):**
```
RefDataService caches 100+ reference data types at application startup:
  getCaseTypeMstr()         - all case types (APPEAL, DCR, ADJUDICATION...)
  getCaseStatusMstr()       - all case statuses
  getDemandStatusMstr()     - demand status transitions
  getHearingMstr()          - hearing types and schedules
  getCommTemplateMstr()     - communication templates
  getBankMstr()             - bank master data
  getDistrictMstr()         - district and state data
  getReturnFormDetails()    - GST return form metadata
  getReturnsDateConfig()    - filing deadline dates
  getHldyMstrEntity()       - holiday calendar
  getAccessGrpMstr()        - access group permissions
  getDocTypeMstr()          - document type master
  ... (100+ types total)
```

**What is impressive here:**
- All master/reference data loaded at startup into JVM heap — zero DB hits per lookup
- `LocalCacheFwk` (JVM in-memory) vs `DistCacheFwk` (Redis distributed) — two-tier caching
- Cache refresh strategy: startup load + scheduled refresh + manual invalidation endpoint
- `CaseToTaxOfclsMap` — case-to-officer map cached locally for instant task assignment

**Two-tier cache architecture:**
```
Request arrives
    ↓
Local Cache (JVM, nanosecond access)
    ↓ MISS (rare — only on first load or refresh)
Distributed Cache (Redis, millisecond access)
    ↓ MISS (very rare — TTL expired)
Database (millisecond to second, avoid at all costs during peak)
```

**What to learn:**
- JVM heap caching: why `ConcurrentHashMap` is better than `HashMap` for cache
- Cache warm-up: `@PostConstruct` to load all master data before first request
- Cache refresh: `@Scheduled(cron="0 0 1 * * *")` — nightly refresh for master data
- Stale data risk: local cache has no automatic invalidation — updates need manual refresh
- Cache size estimation: 100 types × avg 1000 entries × avg 500 bytes = ~50MB — acceptable
- `Guava Cache` or `Caffeine` — production alternatives with built-in size limits and stats

**Resume bullet (after learning):**
```
Leveraged a two-tier caching architecture combining JVM in-memory cache (100+
reference data types loaded at startup via @PostConstruct) with Redis distributed
cache for session data, eliminating database calls for all master data lookups and
reducing average API response latency during peak filing windows
```

---

### 12.6 Event-Driven System with State-Based DB Routing — EventMgmt

**What exists in your code (EventMgmt):**
```java
// EventProcessorHandler.java — creates events routed to correct regional DB
public Object createEvent(EventDetailRequestVO eventDetailRequestVO) {
    setDbRouting(eventDetailRequestVO.getStateCd());  // route by state
    response = eventProcessor.createEvent(eventDetailRequestVO);
}

// AuditServiceImpl.java — async event audit with DB routing + @Transactional
@EnableAsync
@Transactional
public void auditEvent(EventDtlEntity toBeCreatedEntity) {
    setDbRouting(toBeCreatedEntity.getStateCd());
    // persists to region-specific audit table
}
```

**What is impressive here:**
- Event creation + audit are two separate concerns — separated into `EventProcessor` + `AuditService`
- `@EnableAsync` on `AuditServiceImpl` — audit writes don't block main event thread
- DB routing per event based on `stateCd` — each state's events go to its own regional DB
- This is a lightweight Event Sourcing pattern: every state change creates an immutable event record

**What to learn:**
- Event vs Command: Command = "do this", Event = "this happened" (immutable)
- Event Sourcing: state = replay of all events (your DCR entries ARE event sourcing)
- `@Async` + `@Transactional` interaction: `@Async` runs in new thread — can't share parent TX
- `@EnableAsync` on class vs `@EnableAsync` in config class — scope difference
- Outbox pattern: store event in same DB transaction as business data, then publish async

---

### 12.7 What to Say for Each in an Interview

**ThreadLocal + AbstractRoutingDataSource:**
> "Our system serves 28 Indian states, each with its own database region. Instead of
> if-else routing in every DAO, we used Spring's AbstractRoutingDataSource. A ThreadLocal
> stores the region key for each request thread. The RoutingDataSource calls
> determineCurrentLookupKey() and Spring picks the correct datasource from a pre-configured
> map. We always clear the ThreadLocal after the request in a finally block to prevent
> stale state in pooled threads."

**HBase custom functional API:**
> "Return filing data is sparse and massive — unsuitable for MySQL. We used HBase with
> a custom functional API — GSTFunction and GSTPredicate — that enforces HBase Model
> validation at compile time. You can compose predicates: find all rows where period=2024-03
> AND status=FILED, and map them to a VO — but the composition validates both predicates
> operate on the same HBase table, preventing runtime cross-table errors."

**Risk-Based Authentication:**
> "Our authentication service supports 10+ strategies — from simple password to Digital
> Signature Certificates for tax officers. Every login also goes through Risk-Based
> Authentication: we assess device fingerprint, IP, and behaviour pattern to assign a risk
> category. Low risk = password only. High risk = forced OTP escalation. This is the same
> pattern used by banks and large fintech platforms."

**Local Cache (100+ types):**
> "We have two cache layers. LocalCacheFwk is a JVM in-memory cache loaded at startup
> with 100+ reference data types — case statuses, hearing masters, document types, return
> deadlines. These never hit the database. DistCacheFwk is Redis for session and transactional
> data. The two-tier approach means most requests are fully served from nanosecond-access
> JVM memory, with Redis as fallback, and DB only as last resort."

---

### 12.8 Summary — What to Learn + Expected Timeline

| Topic | Repo Source | Learn In | Impressive Because |
|---|---|---|---|
| Spring AOP (custom annotations, @Around, Kafka publish) | GstAopFwk | 1 week | Production AOP is rare on most resumes |
| ThreadLocal + AbstractRoutingDataSource (multi-tenant DB routing) | WorkFlowFwk / DbContextHolder + RoutingDataSource | 3 days | Very few devs have done real DB sharding routing |
| HBase + custom GSTFunction/GSTPredicate functional API | HbaseAccessFwk / layer1 | 1 week | NoSQL + functional composition = senior signal |
| Multi-strategy authentication (OTP, DSC, G2G, RBA) | AuthenticationFwk | 1 week | Security depth beyond JWT basics |
| XA Transactions + Atomikos 2PC | WorkFlowFwk / WFXAService | 1 week | Very few devs have hands-on XA experience |
| Redis Architecture (40+ cached types, Factory, stampede protection) | DistCacheFwk | 1 week | Goes beyond basic caching |
| Kafka (Protobuf, manual ack, DLQ, health check) | KafkaConsumerFwk, GstAopFwk | 1 week | Production Kafka patterns — not tutorial Kafka |
| JVM In-Memory Local Cache (100+ master types, startup warm-up) | LocalCacheFwk | 3 days | Performance-first thinking |
| Event-driven audit with async DB routing | EventMgmt | 3 days | Event sourcing lite |
| Custom Spring Boot Starter | springboot-starter-gstn | 3 days | Framework-level platform thinking |

**Priority order for SDE-2/3 resume impact:**
```
1. ThreadLocal + AbstractRoutingDataSource  ← HIGHEST — very rare, immediately impressive
2. Spring AOP (@BoApiAudit, Kafka publish)  ← HIGH — framework-level thinking
3. HBase GSTFunction/GSTPredicate           ← HIGH — functional + NoSQL combination
4. Risk-Based Authentication                ← HIGH — security depth
5. Redis deep dive (stampede, Factory)      ← MEDIUM-HIGH — beyond basics
6. Kafka Protobuf + manual ack              ← MEDIUM-HIGH — production patterns
7. Local Cache 100+ types + warm-up         ← MEDIUM — perf awareness
8. Custom Spring Boot Starter               ← MEDIUM — platform engineering
```

---

### 12.9 The "Hidden Gems" Interview Answer

**When asked: "What's the most technically interesting thing in your codebase?"**

> "Three things stand out. First, our multi-region database routing: we use Spring's
> AbstractRoutingDataSource with ThreadLocal to transparently route every DAO call to
> the correct regional database based on the state code in the request. The entire DAO
> layer is unaware of which database it's hitting — the routing is purely infrastructural.
>
> Second, our AOP audit framework: any controller method annotated with @BoApiAudit
> gets intercepted, its request and response captured, audit configuration loaded from
> a database at runtime (so we can toggle per-API auditing without redeployment), and
> the audit event published to Kafka as Protobuf. The main thread never blocks.
>
> Third, our HBase access layer has a custom functional API — GSTFunction and
> GSTPredicate — that are composable and model-aware. You can write a predicate
> to filter HBase rows, compose it with another predicate, and the framework validates
> at composition time that both predicates target the same HBase table — preventing
> cross-table operation bugs entirely at the type level."

---
**What exists in your code:**
```
WorkFlowFwk/
  service/
    WFService.java          - standard workflow operations
    WFXAService.java        - XA-aware workflow: addWfProcess, addWfTask,
                              getLatestTaskAssignedToTaxOfficial,
                              getWfProcessByARN
    WorkFlowARNReassignmentService.java - reassign workflow by ARN
  model/
    ProcessDetails          - workflow process (maps to a case lifecycle)
    TaskDetails             - individual task (assigned to officer, with deadline)
```
**What is impressive here:**
- `WFXAService` — workflow operations participate in XA transactions alongside case and ledger updates
- Jurisdiction-based officer assignment: `getLatestTaskAssignedToTaxOfficial(stJurdsCd, stCd, tasktypId)`
- ARN-based process lookup: entire workflow is traceable by appeal reference number

**What to learn:**
- How XA transaction manager (Atomikos) enrolls multiple resources into one transaction
- 2-phase commit protocol: Prepare phase (all vote yes/no) → Commit phase
- Difference between `WFService` (single DB) and `WFXAService` (multi-DB XA)
- Task assignment algorithms: round-robin, least-load, jurisdiction-based routing

**Resume bullet (after learning):**
```
Built workflow orchestration with XA transaction participation ensuring task
creation, case updates, and ledger entries commit atomically across 3 independent
databases using Atomikos 2-phase commit - with jurisdiction-based officer
assignment routing tasks to the correct adjudicating authority by state code
```

**Build project:**
Workflow engine where: creating a task also creates an audit entry and a ledger
debit entry - all in one XA transaction. If any step fails, all three roll back.
Use H2 + a mock second datasource to simulate multi-DB XA locally.

---

### 12.3 Distributed Cache Architecture — DistCacheFwk
**What exists in your code:**
```
DistCacheFwk/
  service/
    DistDataService.java    - 40+ cached data types:
                              getBankEncrptn(), getJursdOffclMap(),
                              getReturnDueDtls(), getApiTxnVO(),
                              getCaseToTaxOfclsMap()
  factory/                  - factory pattern for cache store selection
  store/                    - pluggable cache store abstraction
  model/
    JursdOffclMap           - jurisdiction to officer mapping (critical for routing)
    ReturnDueDtls           - return filing deadlines (hot data at month-end)
    ApiTxnVO                - API transaction tracking
```
**What is impressive here:**
- 40+ distinct data types cached — from bank encryption keys to jurisdiction maps
- Factory pattern selects cache store (Redis vs local vs HBase) at runtime
- `CaseToTaxOfclsMap` — caches case-to-officer mapping, eliminates repeated DB joins
- `ReturnDueDtls` — pre-loaded deadline data serves millions of lookups during filing peaks

**What to learn:**
- Redis data structures: String (simple value), Hash (object), SortedSet (leaderboard/priority)
- Cache-aside vs write-through vs write-behind patterns
- Cache stampede problem: what happens when TTL expires for hot key simultaneously for 1000 threads
- Solution: probabilistic early expiration, Redis `SETNX` lock on refresh
- Consistent hashing: how Redis Cluster distributes keys across nodes

**Resume bullet (after learning):**
```
Designed a pluggable distributed cache layer using Factory pattern with Redis,
caching 40 distinct data types (jurisdiction maps, filing deadlines, officer
mappings) with TTL-based eviction - eliminating repeated database joins and
reducing backend load by 60 to 80 percent during peak GST filing windows
```

**Build project:**
Spring Boot + Redis. Cache-aside pattern: on cache miss, load from DB and store
with TTL. Implement cache stampede protection using Redis distributed lock on
cache refresh. Add metrics: hit rate, miss rate, eviction count.

---

### 12.4 Event-Driven Audit System — GstAopFwk + KafkaConsumerFwk
**What exists in your code:**
```
KafkaConsumerFwk/
  producer/     - Kafka producers
  consumer/     - Kafka consumers with acknowledgement handling
  ack/          - acknowledgement strategies
  config/       - Kafka connection, topic, consumer group config
  health/       - Kafka health check endpoint

GstAopFwk:
  KafkaAuditProducer - publishes ApiAuditLog to Kafka topic
  ApiAuditLog (proto) - Protobuf-serialized audit event
```
**What is impressive here:**
- Audit events use **Protobuf** serialization (not JSON) — smaller payload, schema-enforced
- `BoApiAuditAspect` captures BOTH request and response bodies with field-level control
- Kafka health endpoint — production-grade observability built in
- Acknowledgement strategies in `ack/` — at-least-once delivery with manual commit

**What to learn:**
- Protobuf vs JSON: schema evolution, binary encoding, backward compatibility
- Kafka consumer groups: each consumer group gets all messages independently
- Manual offset commit: when to use `ack.acknowledge()` vs auto-commit
- Dead Letter Queue pattern: failed messages → retry topic → DLQ after max retries
- Kafka Connect vs custom consumer for data pipeline use cases

**Resume bullet (after learning):**
```
Implemented an event-driven API audit pipeline using Spring AOP and Apache Kafka
with Protobuf serialization - capturing structured audit events (user, endpoint,
request/response payload, latency) at method interception level and streaming to
a centralized audit topic with manual offset acknowledgement for at-least-once
delivery guarantees
```

**Build project:**
Audit pipeline: Spring Boot API with `@Auditable` AOP aspect → Kafka producer
(Protobuf messages) → Kafka consumer → store in MySQL audit table. Add DLQ:
failed audit writes → retry topic → alert after 3 failures.

---

### 12.5 Custom Spring Boot Starter — springboot-starter-gstn
**What exists in your code:**
```
springboot-starter-gstn/      - custom auto-configuration starter
gst-spring-boot2-parent/      - parent POM with dependency management
gst-spring-boot2-starter/     - Spring Boot 2 compatible starter
```
**What is impressive here:**
- GSTN built its own Spring Boot starter — all common configuration (datasource,
  Redis, Kafka, security, AOP) auto-configured for any new microservice
- This is exactly what Netflix OSS, Zalando, and large engineering orgs do

**What to learn:**
- `spring.factories` / `AutoConfiguration.imports` — how Spring Boot discovers auto-config
- `@ConditionalOnProperty`, `@ConditionalOnMissingBean` — conditional bean creation
- `@ConfigurationProperties` — type-safe property binding
- How to package a starter: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`

**Resume bullet (after learning):**
```
Developed a custom Spring Boot auto-configuration starter consolidating shared
configuration (datasource pooling, Redis, Kafka, AOP audit) across 15 microservices
using @ConditionalOnProperty and @ConfigurationProperties - reducing boilerplate
configuration per service by 80 percent and standardizing cross-cutting concerns
```

**Build project:**
Create a `my-audit-starter` Maven module. Auto-configures: `@Auditable` AOP aspect
+ Kafka producer when `audit.enabled=true` in any consuming Spring Boot app.
Publish to local Maven repo and consume from another app with zero config.

---

### 12.6 Multi-Datasource + Connection Pool Management
**What exists in your code:**
- `LitigationAPI2` talks to: MySQL (case data) + HBase (archive) + Redis (cache) + Kafka
- XA datasource configuration for multi-DB atomicity
- `gst-spring-boot2-starter` configures connection pools centrally

**What to learn:**
- HikariCP: `maximumPoolSize`, `minimumIdle`, `connectionTimeout` tuning
- Why connection pool exhaustion causes cascading failures at traffic spikes
- XA datasource wrapping: `AtomikosDataSourceBean` wraps regular datasource for XA
- HBase client: column families, row key design, scan vs get
- Read replica routing: `@Transactional(readOnly=true)` → slave datasource

**Resume bullet (after learning):**
```
Configured multi-datasource connection pool management across MySQL, HBase, and
Redis using HikariCP and Atomikos XA datasource wrappers - tuned pool parameters
to prevent connection exhaustion during filing deadline traffic spikes on a platform
serving 140 million taxpayers
```

---

### 12.7 Summary — What to Learn + Expected Timeline

| Topic | Repo Source | Learn In | Impressive Because |
|---|---|---|---|
| Spring AOP (custom annotations, @Around, Kafka publish) | GstAopFwk | 1 week | Production AOP is rare on most resumes |
| XA Transactions + Atomikos | WorkFlowFwk, LitigationAPI2 | 1 week | Very few devs have hands-on XA experience |
| Redis Architecture (40+ cached types, Factory pattern, stampede protection) | DistCacheFwk | 1 week | Goes beyond basic caching |
| Kafka (Protobuf, manual ack, DLQ, health check) | KafkaConsumerFwk, GstAopFwk | 1 week | Most devs know basic Kafka; you know production patterns |
| Custom Spring Boot Starter | springboot-starter-gstn | 3-4 days | Shows framework-level thinking |
| HBase + multi-datasource + connection pool tuning | HbaseAccessFwk | 3-4 days | Signals senior-level infra awareness |

**Priority order:** AOP → Redis deep dive → Kafka production patterns → Custom starter → XA deep dive → HBase

---

### 12.8 The "Hidden Gems" Interview Answer

**When asked: "What's the most technically interesting thing in your codebase?"**

> "Beyond the business logic, our platform has a custom AOP-based audit framework
> that intercepts any controller method annotated with `@BoApiAudit`. It reads per-API
> audit configuration from a database at runtime - so you can toggle which fields to
> log without redeployment - and publishes structured Protobuf-encoded audit events
> to Kafka asynchronously. This means the main request thread is never blocked by
> audit logging, and audit configuration is fully dynamic.
>
> We also built a custom Spring Boot starter that auto-configures Redis, Kafka, XA
> datasource, and this AOP audit framework for any new microservice joining the
> platform. What took 200+ lines of boilerplate per service became zero config.
>
> These two things together - dynamic AOP audit + auto-configured starter - are
> exactly the kind of platform engineering problems I want to work on at scale."

---

*Reference compiled from GSTN litigation module work and SDE-2/SDE-3 interview preparation.*
*Focus areas: CaseMgmtFwk, LedgerUtilFwk, WorkFlowFwk, DistCacheFwk, KafkaConsumerFwk, GstAopFwk.*
*Target: SDE-2/SDE-3 at Flipkart, Razorpay, PhonePe, Meesho, Zerodha, Cred, Swiggy, Uber, Goldman Sachs*

---

# Section 13 — Complete Concepts Master Checklist: Learn + Hands-On + Interview Readiness

> This section is your single reference for EVERYTHING you need to know and practice
> to answer any SDE-2/SDE-3 interview question confidently. Each topic has:
> - Concepts to know (mark off as you learn)
> - A hands-on mini-project (30 min to 2 hours)
> - The exact interview question you must be ready to answer

**How to use:** Go topic by topic. For each concept, (1) read/watch, (2) write code from scratch, (3) speak the answer out loud without looking.

---

## 13.1 Java Core — Internals That SDE-2/3 Are Expected to Know

### Concepts to Master

**Collections Internals:**
- [ ] HashMap: array of buckets + linked list, hash collision chaining, load factor 0.75, resize to 2x
- [ ] HashMap: why capacity must be power-of-2 (bitwise AND for index = hash & (n-1))
- [ ] HashMap in Java 8+: bucket converts to Red-Black Tree when size > 8 (treeifyBin)
- [ ] ConcurrentHashMap: 16 segments (Java 7) vs CAS + synchronized per-bucket (Java 8)
- [ ] LinkedHashMap: doubly-linked list on top of HashMap for insertion/access order — how LRU cache is built
- [ ] TreeMap: Red-Black Tree, O(log n) for all ops, sorted by key natural order or Comparator
- [ ] PriorityQueue: binary min-heap, offer/poll O(log n), peek O(1)
- [ ] ArrayDeque vs LinkedList: ArrayDeque is faster (no node allocation), prefer as Stack/Queue

**Java Memory Model:**
- [ ] Stack vs Heap: primitives + references on stack, objects on heap
- [ ] String pool: `"abc" == "abc"` is true (same pool reference), `new String("abc") == new String("abc")` is false
- [ ] `volatile`: ensures visibility (no CPU cache), NOT atomicity
- [ ] `synchronized`: mutual exclusion + visibility, monitor lock on object
- [ ] `AtomicInteger` / `AtomicReference`: CAS (compare-and-swap) under the hood, lock-free
- [ ] Happens-before: write to `volatile` happens-before subsequent reads of same variable

**Concurrency:**
- [ ] `ExecutorService`: thread pool, submit vs execute, Future vs CompletableFuture
- [ ] `CompletableFuture`: supplyAsync, thenApply, thenCompose, thenCombine, exceptionally, allOf
- [ ] `CountDownLatch` vs `CyclicBarrier`: latch is one-time countdown, barrier is reusable meeting point
- [ ] `Semaphore`: permits, acquire/release — controls concurrent access to limited resource
- [ ] Deadlock: 4 conditions (mutual exclusion, hold-and-wait, no preemption, circular wait). Prevention: always lock in same order
- [ ] `ReentrantLock` vs `synchronized`: ReentrantLock has tryLock, lockInterruptibly, fairness option
- [ ] `ThreadLocal`: per-thread storage, must call remove() to prevent memory leak in thread pools
- [ ] `ForkJoinPool`: work-stealing, used by parallel streams and CompletableFuture

**JVM / GC:**
- [ ] JVM memory: Heap (Young/Old), Metaspace (not in heap), Stack (per-thread)
- [ ] GC generations: Young (Eden + S0 + S1), Old, Metaspace. Minor GC (Young), Major/Full GC (Old)
- [ ] GC algorithms: Serial, Parallel, CMS (deprecated), G1 (default Java 9+), ZGC (low latency)
- [ ] G1GC: region-based, aims to keep GC pauses under 200ms target
- [ ] GC tuning flags: `-Xms`, `-Xmx`, `-XX:+UseG1GC`, `-XX:MaxGCPauseMillis`
- [ ] Memory leak: static references holding objects, unclosed streams, ThreadLocal not cleared
- [ ] Class loading: Bootstrap → Extension → Application classloader, parent-delegation model

**Java 8-17 Features:**
- [ ] Lambda and functional interfaces: `Function<T,R>`, `Predicate<T>`, `Supplier<T>`, `Consumer<T>`
- [ ] Streams: lazy evaluation, intermediate (filter/map/flatMap) vs terminal (collect/reduce/forEach)
- [ ] Stream parallel: uses ForkJoinPool, not always faster (overhead for small collections)
- [ ] Optional: avoid null checks, orElse vs orElseGet (orElseGet is lazy — use for expensive calls)
- [ ] Records (Java 16): immutable data classes, auto-generates equals/hashCode/toString
- [ ] Sealed classes (Java 17): restrict which classes can extend — exhaustive pattern matching

### Hands-On Exercises

**Exercise 1 — Build LRU Cache from scratch (30 min):**
```java
// Implement using LinkedHashMap
class LRUCache {
    private final int capacity;
    private final LinkedHashMap<Integer, Integer> map;
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new LinkedHashMap<>(capacity, 0.75f, true) {
            protected boolean removeEldestEntry(Map.Entry<Integer,Integer> e) {
                return size() > capacity;
            }
        };
    }
    public int get(int key) { return map.getOrDefault(key, -1); }
    public void put(int key, int value) { map.put(key, value); }
}
```
Then implement it from scratch using HashMap + doubly-linked list (no LinkedHashMap).

**Exercise 2 — Producer-Consumer with BlockingQueue (20 min):**
```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
ExecutorService pool = Executors.newFixedThreadPool(4);
// 2 producers, 2 consumers, run for 10 seconds, then shutdown gracefully
```

**Exercise 3 — CompletableFuture pipeline (20 min):**
```java
// Simulate: fetch user (200ms) → fetch orders (300ms) → fetch payment info (250ms)
// First try sequential (750ms total), then parallel (500ms total using allOf/thenCombine)
// Handle exceptions with exceptionally()
```

### Interview Questions to Answer Out Loud

1. "How does HashMap work internally? What happens during a collision? When does it become a tree?"
2. "What is the difference between volatile and synchronized?"
3. "How would you implement a thread-safe singleton?"
4. "What is a deadlock? How do you prevent it?"
5. "What is CompletableFuture and how is it different from Future?"
6. "Explain G1GC. How does it differ from CMS?"
7. "What are the 4 functional interfaces in Java 8? Give an example of each."
8. "What is ThreadLocal? What is its memory leak risk?"

---

## 13.2 Spring Boot — Framework Internals + Production Patterns

### Concepts to Master

**Auto-Configuration:**
- [ ] `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`
- [ ] Auto-config mechanism: `spring.factories` (Boot 2) / `AutoConfiguration.imports` (Boot 3) — lists config classes
- [ ] `@Conditional`: `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` — when beans are created
- [ ] How to write a custom Spring Boot starter: auto-config class + META-INF/spring.factories entry

**Bean Lifecycle:**
- [ ] Bean scopes: Singleton (default), Prototype, Request, Session, Application
- [ ] Lifecycle hooks: `@PostConstruct` (after injection), `@PreDestroy` (before shutdown), `InitializingBean`, `DisposableBean`
- [ ] `BeanFactoryPostProcessor` vs `BeanPostProcessor`: factory PP runs before bean creation, bean PP wraps each bean
- [ ] Circular dependency: constructor injection fails (correct), field injection silently breaks — always use constructor injection

**Spring AOP:**
- [ ] Proxy types: JDK dynamic proxy (interface-based) vs CGLIB proxy (class-based, default in Spring Boot)
- [ ] Advice types: `@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`, `@Around`
- [ ] `@Around` is most powerful: controls whether method executes, can change return value
- [ ] Pointcut expressions: `execution(* com.example.service.*.*(..))`, `@annotation(MyAnnotation)`
- [ ] AOP limitation: self-invocation doesn't trigger proxy (calling method from same class bypasses AOP)

**Transactions:**
- [ ] `@Transactional` isolation levels: READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE
- [ ] Transaction propagation: REQUIRED (join/create), REQUIRES_NEW (always new), SUPPORTS, NOT_SUPPORTED, NEVER, MANDATORY, NESTED
- [ ] `@Transactional` + `@Async`: async runs in new thread = new transaction (parent TX not shared)
- [ ] Checked vs unchecked exception rollback: default rollback only on RuntimeException, use `rollbackFor=Exception.class` for checked
- [ ] Optimistic locking: `@Version` field, throws `OptimisticLockException` on conflict — no DB lock, retry on conflict
- [ ] Pessimistic locking: `@Lock(LockModeType.PESSIMISTIC_WRITE)` — DB row lock, use for high-contention

**Spring Security (basics for SDE-2):**
- [ ] Filter chain: `SecurityFilterChain` processes every request, order matters
- [ ] Authentication vs Authorization: who are you vs what can you do
- [ ] JWT flow: login → server issues JWT → client sends in `Authorization: Bearer <token>` header → server validates signature
- [ ] `UserDetailsService.loadUserByUsername()` — where you plug in your user store
- [ ] Password encoding: `BCryptPasswordEncoder` — never store plain text

**Spring Actuator:**
- [ ] `/actuator/health`, `/actuator/info`, `/actuator/metrics`, `/actuator/env`
- [ ] Custom health indicator: implement `HealthIndicator`, check DB/Redis/Kafka connectivity
- [ ] Micrometer: metrics library under Actuator, integrates with Prometheus/Grafana

### Hands-On Exercises

**Exercise 1 — Write a custom Spring Boot starter (1 hour):**
```
1. Create library project: my-audit-starter
2. Write MyAuditAutoConfiguration.java with @ConditionalOnProperty("audit.enabled=true")
3. Bean creates AuditInterceptor that logs all incoming requests
4. Add META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
5. In a separate Spring Boot app, add your starter as dependency
6. Verify: with audit.enabled=true all requests are logged, with false nothing is logged
```

**Exercise 2 — AOP annotation that times any method (30 min):**
```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Timed {}

@Aspect @Component
public class TimingAspect {
    @Around("@annotation(Timed)")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        Object result = pjp.proceed();
        System.out.println(pjp.getSignature() + " took " + (System.currentTimeMillis()-start) + "ms");
        return result;
    }
}
```
Then extend it: capture method name, class, params, and publish to a list in memory. Add endpoint to view timings.

**Exercise 3 — Transaction propagation experiment (20 min):**
Create ServiceA calling ServiceB. Annotate A with REQUIRED, B with REQUIRES_NEW.
Throw exception in A after B completes. Verify B's changes are committed, A's are rolled back.
Then try: annotate B with REQUIRED, verify everything rolls back together.

### Interview Questions to Answer Out Loud

1. "How does Spring Boot auto-configuration work? Walk me through what happens when the app starts."
2. "What is the difference between @Component, @Service, @Repository, @Controller?"
3. "Explain AOP proxy mechanism. What is self-invocation problem?"
4. "What is the difference between REQUIRES_NEW and REQUIRED transaction propagation?"
5. "How does JWT-based authentication work in a Spring Security filter chain?"
6. "What happens if you annotate a method with @Async and @Transactional — what are the pitfalls?"
7. "How would you write a custom Spring Boot starter?"

---

## 13.3 Database — SQL, JPA/Hibernate, Transactions, Sharding

### Concepts to Master

**SQL Advanced:**
- [ ] Window functions: `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`
- [ ] CTEs: `WITH cte AS (SELECT ...)` — readable, reusable, recursive CTEs for hierarchies
- [ ] Subquery vs JOIN: subquery for existence check (`EXISTS`), JOIN for filtering and projection
- [ ] Index types: B-Tree (default, range queries), Hash (equality only), Composite (column order matters)
- [ ] Index usage: leading column rule — composite index on (A,B,C) helps A, A+B, A+B+C but NOT B alone
- [ ] EXPLAIN / EXPLAIN ANALYZE: read query plan, identify seq scan vs index scan, identify bottlenecks
- [ ] Covering index: index includes all columns the query needs — no table lookup (index-only scan)
- [ ] NULL handling: `IS NULL`, `IS NOT NULL`, NULL in aggregates (COUNT ignores NULL, SUM treats as 0)

**Transaction Isolation:**
- [ ] READ UNCOMMITTED: dirty reads possible (read uncommitted data of another TX)
- [ ] READ COMMITTED (PostgreSQL default): no dirty reads, but non-repeatable reads possible
- [ ] REPEATABLE READ (MySQL InnoDB default): same row reads same value, but phantom reads possible
- [ ] SERIALIZABLE: full isolation, like serial execution, highest overhead
- [ ] Phantom read: same range query returns different rows in same TX (new row inserted by other TX)
- [ ] MVCC (Multi-Version Concurrency Control): readers don't block writers — snapshot isolation

**JPA / Hibernate Internals:**
- [ ] `EntityManager` vs `Session`: JPA standard vs Hibernate-specific
- [ ] First-level cache (session cache): within same session, same entity loaded once, held in cache
- [ ] Second-level cache (shared): across sessions, needs explicit config (`@Cacheable`, `@Cache`)
- [ ] N+1 problem: fetching 100 orders then fetching each order's items = 101 queries. Fix: `JOIN FETCH` or `@BatchSize`
- [ ] Lazy vs Eager loading: LAZY = load on access (N+1 risk), EAGER = always load (cartesian product risk)
- [ ] `@OneToMany(fetch=LAZY, cascade=ALL, orphanRemoval=true)` — most common safe config
- [ ] Dirty checking: Hibernate compares entity state at flush time with snapshot at load — auto generates UPDATE
- [ ] `@Modifying + @Query`: required for bulk UPDATE/DELETE with JPQL/HQL — bypasses dirty checking

**Database Design:**
- [ ] Normalization: 1NF (atomic), 2NF (no partial dependency), 3NF (no transitive dependency)
- [ ] When to denormalize: read-heavy system, aggregation is expensive, reporting queries
- [ ] Partitioning: horizontal (by row range/hash) vs vertical (by column group)
- [ ] Sharding: application-level routing to different databases — your GSTN ThreadLocal pattern
- [ ] Read replicas: write to primary, read from replica — synchronous vs asynchronous replication lag
- [ ] Connection pooling: HikariCP (default in Spring Boot) — pool size tuning: min-idle, max-pool-size

### Hands-On Exercises

**Exercise 1 — N+1 diagnosis and fix (30 min):**
```
Create: Author (1) → Books (many) → Reviews (many)
Load all authors + their books + review count
First: trigger N+1, use Hibernate show_sql=true to count queries
Then: fix with JOIN FETCH, fix with @BatchSize(size=20)
Measure query count before and after
```

**Exercise 2 — Window function practice (20 min):**
```sql
-- Given: orders(order_id, customer_id, amount, order_date)
-- Write queries for:
-- 1. Rank customers by total spend (RANK OVER)
-- 2. Find running total of daily revenue (SUM OVER ORDER BY date)
-- 3. Find each customer's previous order amount (LAG)
-- 4. Find top 3 orders per customer (ROW_NUMBER OVER PARTITION BY)
```

**Exercise 3 — Index tuning (20 min):**
```sql
-- Table: case_master (case_id, gstin, state_cd, status, created_date, officer_id)
-- Queries to optimize:
-- Q1: WHERE gstin = ? AND state_cd = ?  (equality on both)
-- Q2: WHERE officer_id = ? AND status = 'OPEN' ORDER BY created_date
-- Q3: WHERE state_cd = ? AND created_date BETWEEN ? AND ?
-- For each: decide which index to create, explain why
```

### Interview Questions to Answer Out Loud

1. "What is the N+1 problem? How do you detect and fix it?"
2. "Explain the difference between optimistic and pessimistic locking."
3. "What is a covering index? When would you use one?"
4. "What is MVCC? Why do reads not block writes in PostgreSQL?"
5. "Explain dirty checking in Hibernate. When does an UPDATE happen automatically?"
6. "What are window functions? Give a real example."
7. "How would you scale a database that has grown to 100M rows?"

---

## 13.4 Redis — Beyond Basic Caching

### Concepts to Master

**Data Structures:**
- [ ] String: most basic, get/set/incr/decr — counters, rate limiting, simple cache
- [ ] Hash: `HSET key field value` — store object fields, user sessions, config maps
- [ ] List: push/pop from head or tail — message queue, recent items list
- [ ] Set: unique members, SADD/SISMEMBER — deduplication, tags, permissions
- [ ] Sorted Set (ZSet): members with scores, ZADD/ZRANGE/ZRANGEBYSCORE — leaderboard, time-series queries
- [ ] Bitmap: store boolean per offset — track daily active users (1 bit per userId per day)
- [ ] HyperLogLog: approximate cardinality count with tiny memory — count unique visitors
- [ ] Streams: append-only log with consumer groups — lightweight Kafka alternative

**Eviction Policies:**
- [ ] `noeviction`: return error when memory full (default — bad for cache)
- [ ] `allkeys-lru`: evict least recently used from all keys — best for general cache
- [ ] `volatile-lru`: evict LRU but only from keys with TTL set
- [ ] `allkeys-random`, `volatile-ttl`: less common
- [ ] TTL: `EXPIRE key seconds` — always set TTL on cache entries to prevent unbounded growth

**Distributed Patterns:**
- [ ] Cache-aside (lazy loading): app checks cache, on miss loads from DB and sets cache
- [ ] Write-through: app writes to cache + DB together
- [ ] Write-behind (write-back): write to cache, async flush to DB — risk of data loss
- [ ] Cache stampede (thundering herd): TTL expires, 1000 requests all hit DB at same time
  - Fix 1: probabilistic early refresh (refresh before TTL expires with probability)
  - Fix 2: mutex lock — only one thread refreshes, others wait
  - Fix 3: stale-while-revalidate — serve stale data, refresh async
- [ ] Distributed lock: `SET key value NX PX 30000` — atomic acquire, Redisson for production
- [ ] Redis Cluster: 16384 hash slots distributed across nodes, automatic sharding
- [ ] Redis Sentinel: high availability, automatic failover — NOT sharding

**Redis in Production:**
- [ ] Persistence: RDB (snapshot) vs AOF (append-only log), RDB faster restart, AOF more durable
- [ ] Pipelining: batch multiple commands in single TCP roundtrip — 10x throughput for bulk ops
- [ ] Lua scripting: atomic multi-command operations — use for check-then-set patterns
- [ ] Pub/Sub: fire-and-forget messaging — no persistence, no consumer groups

### Hands-On Exercises

**Exercise 1 — Rate limiter using Redis (30 min):**
```java
// Implement token bucket or sliding window rate limiter
// GSTN use case: max 100 API calls per minute per GSTIN
// Use INCR + EXPIRE: each minute key = "ratelimit:{gstin}:{minute}", INCR, if > 100 reject
// Lua script version: atomic increment + check in single command
String key = "ratelimit:" + gstin + ":" + Instant.now().truncatedTo(ChronoUnit.MINUTES);
Long count = redisTemplate.opsForValue().increment(key);
if (count == 1) redisTemplate.expire(key, 60, TimeUnit.SECONDS);
if (count > 100) throw new RateLimitException();
```

**Exercise 2 — Leaderboard with Sorted Set (20 min):**
```java
// Add players with scores
redisTemplate.opsForZSet().add("leaderboard", "player1", 1500.0);
// Get top 10
redisTemplate.opsForZSet().reverseRangeWithScores("leaderboard", 0, 9);
// Get rank of a player
redisTemplate.opsForZSet().reverseRank("leaderboard", "player1");
// Increment score
redisTemplate.opsForZSet().incrementScore("leaderboard", "player1", 100.0);
```

**Exercise 3 — Distributed lock (20 min):**
```java
// Implement: only one instance processes a scheduled job at a time
// Using SET key value NX PX milliseconds
Boolean acquired = redisTemplate.opsForValue()
    .setIfAbsent("lock:job:daily-report", instanceId, 30, TimeUnit.SECONDS);
if (Boolean.TRUE.equals(acquired)) {
    try { runDailyReport(); }
    finally { redisTemplate.delete("lock:job:daily-report"); }
}
```

### Interview Questions to Answer Out Loud

1. "What is a cache stampede? How do you prevent it?"
2. "How would you implement a rate limiter using Redis?"
3. "What is the difference between Redis Cluster and Redis Sentinel?"
4. "How would you implement a distributed lock? What are the failure modes?"
5. "What Redis data structure would you use for a leaderboard? A daily active users count? A session store?"
6. "What eviction policy would you choose for a cache and why?"

---

## 13.5 Kafka — Production Patterns Beyond Basics

### Concepts to Master

**Core Concepts:**
- [ ] Topic → Partition → Offset: each message has a unique (partition, offset) address
- [ ] Producer → Partition selection: hash(key) % numPartitions (key-based), round-robin (no key)
- [ ] Consumer group: each partition assigned to exactly one consumer in the group — parallelism
- [ ] `__consumer_offsets`: internal Kafka topic storing committed offsets per group
- [ ] Replication factor: each partition replicated to N brokers, leader serves reads/writes, followers sync
- [ ] ISR (In-Sync Replicas): replicas caught up to leader. `acks=all` waits for all ISR to commit

**Delivery Guarantees:**
- [ ] At-most-once: auto-commit offset before processing — on crash, message lost
- [ ] At-least-once: manual commit after processing — on crash, message reprocessed (idempotent consumer required)
- [ ] Exactly-once: Kafka Transactions + idempotent producer — `enable.idempotence=true`, `transactional.id`
- [ ] Idempotency: processing same message N times = same result as processing once (use deduplication key)

**Consumer Patterns:**
- [ ] Auto-commit: `enable.auto.commit=true` — risky (commits before processing)
- [ ] Manual commit: `commitSync()` after processing — blocks, but safe. `commitAsync()` — non-blocking, retry on next poll
- [ ] `max.poll.records`: how many records per poll() call — tune for batch processing
- [ ] `max.poll.interval.ms`: if consumer doesn't call poll() within this time — kicked out of group, rebalance triggered
- [ ] Rebalance: partition reassignment on consumer join/leave — pause processing, resume after assignment
- [ ] Dead Letter Queue (DLQ): on processing failure after N retries, publish to `topic.DLT` for manual inspection

**Producer Patterns:**
- [ ] `acks=0`: fire-and-forget (no guarantee), `acks=1`: leader acked, `acks=all`/`acks=-1`: all ISR acked
- [ ] `retries` + `retry.backoff.ms`: retry on transient failures, set `max.in.flight.requests.per.connection=1` to maintain order
- [ ] Batching: `linger.ms` (wait for batch) + `batch.size` — improves throughput, increases latency
- [ ] Compression: `compression.type=snappy` — reduce network + disk IO for large messages
- [ ] Protobuf vs JSON: Protobuf is 5-10x smaller, 2x faster to serialize, schema-enforced — GSTN uses this

**Schema Registry (Avro/Protobuf):**
- [ ] Schema Registry: central store for schemas, assigns schema ID, producers/consumers use ID in message
- [ ] Backward/Forward/Full compatibility — how schemas can evolve without breaking consumers

### Hands-On Exercises

**Exercise 1 — Manual ack consumer (30 min):**
```java
@KafkaListener(topics = "orders", groupId = "order-processor",
               containerFactory = "manualAckFactory")
public void consume(ConsumerRecord<String, String> record, Acknowledgment ack) {
    try {
        processOrder(record.value());
        ack.acknowledge();  // commit only on success
    } catch (Exception e) {
        // don't ack — message will be redelivered
        // after N retries, publish to DLQ
        kafkaTemplate.send("orders.DLT", record.key(), record.value());
        ack.acknowledge();  // ack after DLQ send to prevent infinite loop
    }
}
```

**Exercise 2 — Exactly-once producer (20 min):**
```java
// Configure producer for exactly-once
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "order-producer-1");
// Send in transaction
producer.initTransactions();
producer.beginTransaction();
producer.send(new ProducerRecord<>("output-topic", key, value));
producer.commitTransaction();  // or producer.abortTransaction() on error
```

**Exercise 3 — Implement retry + DLQ with Spring Kafka (30 min):**
Configure `SeekToCurrentErrorHandler` (or `DefaultErrorHandler` in Spring Kafka 2.8+)
with `FixedBackOff(1000L, 3)` — 3 retries, 1 second apart, then publish to DLQ.
Write test: producer sends message → consumer fails intentionally → verify DLQ receives it.

### Interview Questions to Answer Out Loud

1. "Explain the difference between at-least-once and exactly-once delivery in Kafka."
2. "What happens when a consumer crashes after reading but before processing a message?"
3. "How does Kafka guarantee message ordering within a partition?"
4. "What is a consumer group rebalance? When does it happen?"
5. "Why would you use Protobuf instead of JSON for Kafka messages?"
6. "How would you implement a Dead Letter Queue pattern in Kafka?"
7. "What is ISR? What does acks=all mean?"

---

## 13.6 Microservices — Patterns That SDE-2/3 Must Know

### Concepts to Master

**Service Communication:**
- [ ] Synchronous: REST (HTTP/1.1), gRPC (HTTP/2, Protobuf, streaming) — request-response
- [ ] Asynchronous: Kafka, RabbitMQ — fire-and-forget, pub-sub, event-driven
- [ ] When to choose async: long-running tasks, cross-service workflows, decoupling services
- [ ] Service discovery: Eureka (Netflix), Consul — services register, clients look up by name not IP
- [ ] API Gateway: single entry point, handles routing, rate limiting, auth, SSL termination, logging

**Resilience Patterns:**
- [ ] Circuit Breaker: CLOSED (normal) → OPEN (after N failures, block calls) → HALF-OPEN (probe) → CLOSED
  - Resilience4j: `@CircuitBreaker(name="service", fallbackMethod="fallback")`
- [ ] Retry: exponential backoff with jitter — avoid thundering herd on recovery
- [ ] Bulkhead: isolate failures — separate thread pools per downstream service
- [ ] Timeout: every external call must have a timeout — no indefinite waits
- [ ] Rate Limiting: token bucket or sliding window — protect your service from overload

**Distributed Transactions:**
- [ ] 2PC (Two-Phase Commit): coordinator + participants, `prepare` then `commit/rollback`. Synchronous, blocking, coordinator SPOF
  - XA: 2PC over JDBC datasources — your GSTN WFXAService uses this
- [ ] Saga Pattern: sequence of local transactions, each publishes event for next step
  - Choreography Saga: services react to events from each other (no central coordinator)
  - Orchestration Saga: central orchestrator calls each service and handles rollback
  - Compensating transaction: reverse a completed step (e.g., un-reserve inventory)
- [ ] When to use: 2PC for same-organization, short-lived, same-tech transactions. Saga for cross-service, long-running, polyglot

**Observability:**
- [ ] Distributed tracing: trace ID propagated through all services — Jaeger, Zipkin, OpenTelemetry
- [ ] Correlation ID: unique ID per request, logged by every service — enables log stitching
- [ ] Structured logging: JSON format, consistent fields (traceId, service, level, timestamp, message)
- [ ] RED metrics: Rate (requests/sec), Errors (error rate), Duration (latency P50/P95/P99)
- [ ] USE metrics: Utilization, Saturation, Errors — for infrastructure (CPU, memory, disk)

**Service Mesh:**
- [ ] Sidecar proxy: Envoy runs alongside each service, handles mTLS, retries, circuit breaking, tracing
- [ ] Control plane: Istio Pilot configures all sidecars — you define policies, mesh enforces them
- [ ] mTLS: mutual TLS between services — service-to-service authentication with certificates

### Hands-On Exercises

**Exercise 1 — Circuit breaker with Resilience4j (30 min):**
```java
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
@Retry(name = "paymentService")
@TimeLimiter(name = "paymentService")
public CompletableFuture<PaymentResponse> callPaymentService(PaymentRequest req) {
    return CompletableFuture.supplyAsync(() -> paymentClient.process(req));
}

public CompletableFuture<PaymentResponse> paymentFallback(PaymentRequest req, Exception e) {
    return CompletableFuture.completedFuture(PaymentResponse.queued(req.getId()));
}
```
Configure in `application.yml`: slidingWindowSize=10, failureRateThreshold=50, waitDurationInOpenState=30s.
Test: kill downstream service → circuit opens → fallback called → restart service → circuit recovers.

**Exercise 2 — Saga orchestration (45 min):**
```
Order Service → creates order
    → calls Inventory Service (reserve items)
    → calls Payment Service (charge card)
    → calls Notification Service (send confirmation)
If Payment fails:
    → compensate Inventory Service (unreserve items)
    → compensate Order Service (mark order FAILED)
```
Implement with Spring Kafka: each step publishes success/failure event, orchestrator handles flow.

**Exercise 3 — Distributed tracing (20 min):**
Add Micrometer + Zipkin to two Spring Boot services that call each other.
Verify same `traceId` appears in logs of both services. See the trace in Zipkin UI.

### Interview Questions to Answer Out Loud

1. "What is the difference between Saga and 2PC? When would you use each?"
2. "Explain the circuit breaker states. What is the half-open state for?"
3. "How does a service mesh handle mTLS between microservices?"
4. "What is distributed tracing? How does trace ID propagation work?"
5. "How would you handle a failure partway through a multi-service order flow?"
6. "What is a bulkhead pattern? Why does it prevent cascading failures?"

---

## 13.7 System Design / HLD — Framework for Every Question

### Concepts to Master

**Always Cover These 8 Pillars in HLD:**
```
1. Requirements Clarification
   - Functional: what does it do?
   - Non-Functional: scale (users, requests/sec, data size), latency SLA, availability (99.9% = 8.7 hrs/year downtime)
   
2. Capacity Estimation
   - Reads/sec, Writes/sec, Storage/year, Bandwidth
   - Rule of thumb: 100M users, 10% DAU = 10M DAU, 1 req/user/day = 10M req/day = 115 RPS
   
3. High-Level Design
   - Client → CDN → Load Balancer → API Gateway → Services → DB/Cache/Queue
   
4. Data Model
   - Which DB? SQL (ACID, relations), NoSQL (scale, flexible schema), Blob store (files)
   - Schema design: primary key, indexes, partitioning key
   
5. Deep Dive on Critical Components
   - The interviewer will probe 2-3 components — be ready with internals
   
6. Scalability
   - Horizontal scaling, DB read replicas, caching layers, CDN for static
   - How does your design handle 10x traffic tomorrow?
   
7. Reliability / Availability
   - Single points of failure, redundancy, failover, data replication
   
8. Trade-offs
   - CAP theorem: in network partition, choose CP or AP?
   - Consistency vs Availability: what does your system prioritize?
```

**DB Selection Guide:**
| Use Case | Database |
|---|---|
| User accounts, orders, financial transactions | PostgreSQL / MySQL (relational, ACID) |
| Session data, cache, rate limiting | Redis |
| Product catalog, flexible schema, write-heavy | MongoDB |
| Time series metrics | InfluxDB / TimescaleDB |
| Search / autocomplete | Elasticsearch |
| Large-scale sparse data (return filings) | HBase / Cassandra |
| Files, images, videos | S3 / Blob store |
| Audit logs, append-only events | Kafka / Cassandra |

**CAP Theorem:**
- [ ] CAP: Consistency, Availability, Partition tolerance — can only guarantee 2 of 3 during network partition
- [ ] CA (no partition tolerance): single-node databases — impossible in distributed systems
- [ ] CP: Choose consistency over availability — ZooKeeper, HBase, Cassandra (tunable), MongoDB
- [ ] AP: Choose availability over consistency — Cassandra (default), DynamoDB, CouchDB
- [ ] PACELC extends CAP: even without partitions, choose latency vs consistency

**Consistent Hashing:**
- [ ] Why: when you add/remove nodes in a cluster, minimize key redistribution
- [ ] Virtual nodes: each physical node has K virtual positions on ring — improves balance
- [ ] Used by: Cassandra, DynamoDB, Redis Cluster (different variant)

**Rate Limiting Algorithms:**
- [ ] Token bucket: tokens added at fixed rate, request consumes token, burst allowed up to bucket size
- [ ] Leaky bucket: requests queue, processed at fixed rate — smooths traffic, no burst
- [ ] Fixed window: count per window (minute), sharp reset — boundary spike problem
- [ ] Sliding window log: store each request timestamp — accurate, memory-heavy
- [ ] Sliding window counter: combination of fixed windows with interpolation — practical

### Hands-On Practice

**Design These Systems (talk through out loud, draw on paper):**
```
1. URL Shortener (bit.ly)
   Key: base62 encoding, 7-char short URL = 62^7 = 3.5 trillion URLs
   Storage: key-value store (Redis or Cassandra), 1 write per URL creation, 100x reads
   Redirect: 301 (permanent, browser caches) vs 302 (temporary, always hits server) — use 302 for tracking
   
2. Design GSTN's Case Management System (your experience!)
   140M taxpayers, 2M cases/year, 28 states, peak traffic on filing deadlines
   Talk about: CaseMgmtFwk strategy+factory, multi-region DB routing, Redis cache, Kafka audit
   
3. Design a Rate Limiter (for GSTN APIs)
   100 req/min per GSTIN. Redis sliding window. Lua script for atomicity. Distributed deployment.
   
4. Design Notification Service (like GSTN's CommunicationAPI)
   SMS/Email/In-app. Kafka-based async delivery. Template service. Retry with backoff. DLQ.
   
5. Design a Ledger System (like GSTN's LedgerUtilFwk)
   Double-entry bookkeeping. Immutable entries. ACID transactions. Balance = ΣCredit - ΣDebit.
```

### Interview Questions to Answer Out Loud

1. "Design a URL shortener. Walk me through your complete design."
2. "How would you design GSTN's case management system to handle 140M taxpayers?"
3. "What is CAP theorem? If your system prioritizes consistency, which database patterns support that?"
4. "How does consistent hashing help when scaling a distributed cache?"
5. "Design a rate limiter. What algorithm would you use? How does it work at scale?"
6. "How would you make your system handle 10x traffic? What breaks first?"

---

## 13.8 LLD — Object-Oriented Design + Design Patterns

### Core Design Patterns to Know Cold

**Creational:**
- [ ] **Singleton**: one instance, thread-safe via `volatile + double-checked locking` or enum
- [ ] **Factory Method**: subclass decides which object to create — `CaseCustomizerFactory` in your code
- [ ] **Builder**: construct complex objects step by step — `CaseRequest.builder().type().status().build()`
- [ ] **Prototype**: clone existing object instead of creating new — useful for expensive initialization

**Structural:**
- [ ] **Facade**: simplified interface to complex subsystem — `CaseHandler` wrapping `CaseService + TaskService`
- [ ] **Decorator**: add behavior to objects dynamically without changing class — `InputStream` → `BufferedInputStream`
- [ ] **Proxy**: placeholder for another object — Spring AOP proxies, lazy-loading proxies in Hibernate
- [ ] **Adapter**: make incompatible interfaces work together — wrapping legacy API with modern interface
- [ ] **Composite**: treat individual objects and composites uniformly — file/directory hierarchy

**Behavioral:**
- [ ] **Strategy**: algorithm family, encapsulate each one, make them interchangeable — `CaseCustomizer` variants
- [ ] **Template Method**: skeleton algorithm in parent, steps overridden in subclass — `GenericCaseHandler`
- [ ] **Observer**: notify multiple subscribers on state change — event listeners, Spring events
- [ ] **Command**: encapsulate request as object — undo/redo, job queues, transactional operations
- [ ] **Chain of Responsibility**: pass request along chain until handled — Spring Security filter chain
- [ ] **State**: object behavior changes based on its state — case status transitions

### LLD Interview — How to Structure Your Answer

```
Step 1 (2 min) — Clarify requirements
  "Is this for a single machine or distributed? How many concurrent users?
   What are the most important operations? Any special consistency requirements?"

Step 2 (3 min) — Identify entities / nouns
  "I see these main entities: [list them]. Their relationships are: [describe]."

Step 3 (5 min) — Define interfaces and key classes
  "I'll define an interface for [X] so we can swap implementations.
   The core classes are: [list with responsibilities]."

Step 4 (5 min) — Apply patterns
  "I'll use Strategy for [X] because the algorithm needs to vary.
   I'll use Factory for [Y] to encapsulate creation logic.
   I'll use Observer for [Z] to decouple state changes from reactions."

Step 5 (5 min) — Write core code
  Write the main interfaces and the most important class.
  Show one method fully implemented. Don't try to write everything.

Step 6 (2 min) — Trade-offs
  "This design is extensible for [X] but less optimized for [Y].
   If we needed [Y], I would instead..."
```

### LLD Practice Problems (Do Each Once on Paper/IDE)

```
1. Parking Lot: ParkingLot, ParkingFloor, ParkingSpot, Vehicle, Ticket, FeeCalculator
   Patterns: Strategy (fee), Factory (vehicle type), Singleton (lot entry)
   GSTN hook: CaseMgmt = same patterns (case type, fee = demand amount)

2. Rate Limiter: RateLimiter interface, TokenBucketRateLimiter, SlidingWindowRateLimiter
   Patterns: Strategy (algorithm), Decorator (per-user limits)

3. Notification Service: Notifier interface, EmailNotifier, SMSNotifier, PushNotifier
   Patterns: Strategy, Builder (notification), Observer (trigger on event)

4. Snake and Ladder Game: Board, Cell, Player, Snake, Ladder, Dice, Game
   Patterns: Template Method (game loop), Command (moves), Observer (game events)

5. Elevator System: ElevatorController, Elevator, Request, SchedulingStrategy
   Patterns: Strategy (scheduling: FCFS, SCAN), Observer (floor arrival), State (IDLE/MOVING/DOOR_OPEN)

6. Design CaseMgmtFwk (your code!): CaseHandler, CaseCustomizer, CaseCustomizerFactory, TaskService
   Patterns: Strategy + Factory + Template Method + Facade — you have real production example
```

### Interview Questions to Answer Out Loud

1. "Design a parking lot. Walk me through your classes and the patterns you'd use."
2. "What is the difference between Strategy and Template Method patterns?"
3. "How would you design a notification system that supports email, SMS, and push?"
4. "When would you use a Facade pattern? Give a real example from your experience."
5. "How is the Proxy pattern used in Spring? Give two examples."
6. "Design an elevator system. What design patterns apply?"

---

## 13.9 Security — What Every SDE-2/3 Should Know

### Concepts to Master

**JWT + OAuth 2.0:**
- [ ] JWT structure: `base64(header).base64(payload).HMACSHA256(header+payload, secret)`
- [ ] JWT claims: `sub` (subject=userId), `exp` (expiry), `iat` (issued-at), `iss` (issuer), `roles`
- [ ] JWT validation: decode without secret = read claims, VERIFY = check signature with secret
- [ ] Refresh token flow: access token (short-lived, 15min), refresh token (long-lived, 30 days)
- [ ] OAuth 2.0 flows:
  - Authorization Code: for web apps with server-side — most secure
  - Client Credentials: for service-to-service (M2M) — no user involved
  - PKCE: for SPAs and mobile — code challenge instead of client secret
- [ ] Token storage: Never in localStorage (XSS risk). Use HttpOnly cookie (XSS safe) + SameSite=Strict (CSRF safe)

**OWASP Top 10 — Know All 10:**
- [ ] A01 — Broken Access Control: user can access other users' data. Fix: verify ownership on every request
- [ ] A02 — Cryptographic Failures: weak encryption, MD5 passwords. Fix: bcrypt, AES-256, TLS 1.3
- [ ] A03 — Injection (SQL, Command): user input executed as code. Fix: parameterized queries, NEVER string concat
- [ ] A04 — Insecure Design: no rate limiting, no business logic validation
- [ ] A05 — Security Misconfiguration: default credentials, debug mode in prod, unnecessary ports open
- [ ] A06 — Vulnerable Components: outdated dependencies with CVEs. Fix: dependency scanning (Snyk, Dependabot)
- [ ] A07 — Identification and Authentication Failures: no MFA, weak passwords, no account lockout
- [ ] A08 — Software and Data Integrity Failures: unsigned software updates, insecure deserialization
- [ ] A09 — Logging and Monitoring Failures: no audit trail, no alerting on suspicious activity
- [ ] A10 — Server-Side Request Forgery (SSRF): server makes requests to internal services via user input

**Common Attack Vectors:**
- [ ] SQL Injection: `SELECT * FROM users WHERE name = '` + input — always use PreparedStatement
- [ ] XSS (Cross-Site Scripting): injecting JS into pages — sanitize all output, Content-Security-Policy header
- [ ] CSRF (Cross-Site Request Forgery): malicious site triggers authenticated user's request — CSRF token or SameSite cookie
- [ ] IDOR (Insecure Direct Object Reference): `/api/cases/12345` — verify 12345 belongs to calling user
- [ ] Path Traversal: `../../etc/passwd` in file path — validate and sanitize file paths

### Hands-On Exercises

**Exercise 1 — Secure a Spring Boot REST API (30 min):**
```
1. Add Spring Security
2. JWT filter: extract token from header, validate, set SecurityContext
3. Protected endpoint: @PreAuthorize("hasRole('ADMIN')") 
4. Test: valid token → 200, expired token → 401, wrong role → 403, no token → 401
```

**Exercise 2 — Fix SQL injection vulnerability (15 min):**
```java
// VULNERABLE - never do this
String query = "SELECT * FROM users WHERE username = '" + username + "'";

// FIX - always parameterized
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE username = ?");
ps.setString(1, username);

// With JPA - always use @Query with parameters, never string concatenation
@Query("SELECT u FROM User u WHERE u.username = :username")
User findByUsername(@Param("username") String username);
```

### Interview Questions to Answer Out Loud

1. "What is the OWASP Top 10? Name at least 5 and how to fix them."
2. "How does JWT work? How do you validate a JWT?"
3. "What is the difference between authorization code flow and client credentials flow in OAuth2?"
4. "How would you prevent SQL injection in your application?"
5. "What is CSRF? How do you prevent it?"
6. "If a user can access another user's case data by changing the ID in the URL, what vulnerability is that?"

---

## 13.10 Docker + Kubernetes — SDE-2/3 Minimum Knowledge

### Concepts to Master

**Docker:**
- [ ] Image vs Container: image is read-only template, container is running instance
- [ ] `Dockerfile`: FROM, RUN, COPY, EXPOSE, CMD, ENTRYPOINT
- [ ] Multi-stage build: build in large JDK image, copy artifact to slim JRE image — smaller final image
- [ ] Layer caching: each RUN/COPY creates a layer, unchanged layers are cached
- [ ] `docker-compose`: define multi-container applications, networks, volumes

**Kubernetes:**
- [ ] Pod: smallest unit, 1+ containers, shared network and storage
- [ ] Deployment: manages pod replicas, rolling updates, rollback
- [ ] Service: stable network endpoint for pods — ClusterIP (internal), NodePort, LoadBalancer
- [ ] ConfigMap + Secret: externalize configuration from container image
- [ ] Horizontal Pod Autoscaler (HPA): scale replicas based on CPU/memory metrics
- [ ] Liveness probe: is container alive? (restart if fails). Readiness probe: is container ready for traffic? (remove from LB if fails)
- [ ] Resource limits: `requests` (guaranteed), `limits` (maximum) — always set both

### Hands-On Exercise

**Exercise — Dockerize a Spring Boot app with Redis (30 min):**
```dockerfile
# Dockerfile
FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN ./mvnw package -DskipTests

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```
```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports: ["8080:8080"]
    environment:
      SPRING_REDIS_HOST: redis
    depends_on: [redis]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

### Interview Questions to Answer Out Loud

1. "What is the difference between a Docker image and a container?"
2. "What is a liveness probe vs readiness probe in Kubernetes?"
3. "How does a Kubernetes Deployment handle rolling updates?"
4. "What is the difference between a ConfigMap and a Secret?"

---

## 13.11 Master Timeline — What to Learn in What Order

```
WEEK 1-2 (Foundation — things you already know, deepen them):
  - Java: HashMap internals, ConcurrentHashMap, CompletableFuture, ThreadLocal leak
  - Spring Boot: auto-config internals, AOP (write @Timed), Transaction propagation
  - Hands-on: LRU cache, AOP timing annotation, TX propagation experiment

WEEK 3-4 (Your GSTN Patterns — learn deeply what you already USE):
  - AbstractRoutingDataSource + ThreadLocal — read your WorkFlowFwk code, then build from scratch
  - HBase Model + GSTFunction — understand the pattern, then implement a simpler version
  - AOP audit + Kafka publish — your GstAopFwk — extend it with a new annotation
  
WEEK 5-6 (Distributed Systems — Redis + Kafka production):
  - Redis: rate limiter, distributed lock, leaderboard, cache stampede fix
  - Kafka: manual ack, DLQ, retry, Protobuf setup
  - Hands-on: full pipeline: API → Kafka → consumer → Redis → DB

WEEK 7-8 (Security + Microservices):
  - JWT + OAuth2: implement secure Spring Boot API, all 4 OWASP injection fixes
  - Circuit breaker with Resilience4j, Saga orchestration
  - Distributed tracing with Zipkin

WEEK 9-10 (System Design + LLD intensive):
  - HLD: design 5 systems (URL shortener, rate limiter, notification, ledger, case mgmt)
  - LLD: code 6 problems (parking lot, elevator, rate limiter, notification, snake-ladder, case mgmt)
  - Mock interviews: speak answers out loud for every question in this file

WEEK 11-12 (Mock + Apply):
  - Full mock interviews (HLD 45 min + LLD 45 min + coding 45 min)
  - Resume final version
  - Apply to companies
```

---

## 13.12 Quick Self-Test — Before Any Interview

Run through this checklist. If you can answer verbally (without notes), you are ready.

**Java:**
- [ ] Explain HashMap collision handling and tree conversion
- [ ] Difference between volatile and synchronized
- [ ] What is CompletableFuture, write a parallel fetch example
- [ ] ThreadLocal memory leak — when and why

**Spring:**
- [ ] How does auto-configuration work (spring.factories)
- [ ] AOP self-invocation problem
- [ ] REQUIRES_NEW vs REQUIRED — what happens on exception

**Database:**
- [ ] Explain N+1, show the fix
- [ ] READ_COMMITTED vs REPEATABLE_READ — what phantom read is
- [ ] Optimistic vs pessimistic locking — @Version annotation

**Redis:**
- [ ] Cache stampede and 3 ways to prevent it
- [ ] Distributed lock with SET NX PX
- [ ] Rate limiter implementation with Redis

**Kafka:**
- [ ] At-least-once vs exactly-once delivery
- [ ] Manual commit after processing pattern
- [ ] DLQ pattern — why and how

**Microservices:**
- [ ] Circuit breaker states and what each means
- [ ] Saga vs 2PC — when to use each
- [ ] What is distributed tracing, what does trace ID look like

**System Design:**
- [ ] CAP theorem — which two properties your system prioritizes
- [ ] How to estimate capacity (users → DAU → RPS → storage)
- [ ] Design URL shortener in 10 minutes

**LLD:**
- [ ] Strategy vs Template Method — when to use each
- [ ] Code a thread-safe Singleton
- [ ] Design Parking Lot — classes, interfaces, patterns

**Security:**
- [ ] How JWT validation works
- [ ] SQL injection — show vulnerable and fixed code
- [ ] What is IDOR vulnerability

**GSTN Patterns (your differentiators):**
- [ ] ThreadLocal + AbstractRoutingDataSource — explain the full flow
- [ ] @BoApiAudit — how AOP reads config and publishes to Kafka
- [ ] CaseCustomizerFactory — Strategy + Factory + Template Method combined
- [ ] DCR ledger — DR vs CR, outstanding calculation, transfer condition

---

# Section 14 — DSA / Coding Round: Patterns for SDE-2/3

> Product companies (Flipkart, Razorpay, PhonePe, Meesho, Goldman Sachs) have 1-2 coding
> rounds even for SDE-2/3. The bar is NOT competitive programming — it is "can you solve
> medium problems cleanly under pressure". This section maps the 12 most common patterns
> to problems you will actually see, with the mental model for each.

---

## 14.1 The 12 Patterns That Cover 90% of Coding Interviews

### Pattern 1 — Sliding Window

**When to use:** Contiguous subarray/substring problems. "Maximum/minimum of something in a window of size K."

**Template:**
```java
int left = 0, maxSum = 0, windowSum = 0;
for (int right = 0; right < nums.length; right++) {
    windowSum += nums[right];
    if (right - left + 1 > k) {        // window too large, shrink from left
        windowSum -= nums[left++];
    }
    maxSum = Math.max(maxSum, windowSum);
}
```

**Variable-size window (shrink when condition violated):**
```java
int left = 0;
Map<Character, Integer> freq = new HashMap<>();
int maxLen = 0;
for (int right = 0; right < s.length(); right++) {
    freq.merge(s.charAt(right), 1, Integer::sum);
    while (freq.size() > k) {                     // condition violated: shrink
        char leftChar = s.charAt(left++);
        freq.merge(leftChar, -1, Integer::sum);
        if (freq.get(leftChar) == 0) freq.remove(leftChar);
    }
    maxLen = Math.max(maxLen, right - left + 1);
}
```

**GSTN connection:** Rate limiting — "maximum requests in any 60-second window" is a sliding window problem.

**Practice problems:**
- Maximum sum subarray of size K (fixed window)
- Longest substring with K distinct characters (variable window)
- Minimum window substring (LeetCode 76)
- Longest substring without repeating characters (LeetCode 3)

---

### Pattern 2 — Two Pointers

**When to use:** Sorted array, pairs with target sum, partitioning, palindrome check.

**Template — find pair with target sum:**
```java
int left = 0, right = arr.length - 1;
while (left < right) {
    int sum = arr[left] + arr[right];
    if (sum == target) return new int[]{left, right};
    else if (sum < target) left++;
    else right--;
}
```

**Template — remove duplicates in-place:**
```java
int slow = 0;
for (int fast = 1; fast < nums.length; fast++) {
    if (nums[fast] != nums[slow]) {
        nums[++slow] = nums[fast];
    }
}
return slow + 1;
```

**Practice problems:**
- Two Sum II (sorted array) — two pointers
- Three Sum — sort + two pointers for each element
- Container with most water (LeetCode 11)
- Trapping Rain Water (LeetCode 42) — two pointers or stack

---

### Pattern 3 — Fast and Slow Pointers (Floyd's Cycle)

**When to use:** Linked list cycle, middle of list, kth from end.

```java
// Detect cycle
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) return true;   // cycle found
}
return false;

// Find middle of linked list
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
}
// slow is now at middle
```

**Practice problems:**
- Linked List Cycle (LeetCode 141)
- Find middle of linked list
- Palindrome Linked List (LeetCode 234)
- Reorder List (LeetCode 143)

---

### Pattern 4 — Binary Search (Beyond Basic)

**When to use:** Sorted array, "find minimum/maximum X such that condition(X) is true."

**Template — search in rotated sorted array:**
```java
int left = 0, right = nums.length - 1;
while (left <= right) {
    int mid = left + (right - left) / 2;    // avoid integer overflow
    if (nums[mid] == target) return mid;
    if (nums[left] <= nums[mid]) {          // left half is sorted
        if (nums[left] <= target && target < nums[mid]) right = mid - 1;
        else left = mid + 1;
    } else {                                 // right half is sorted
        if (nums[mid] < target && target <= nums[right]) left = mid + 1;
        else right = mid - 1;
    }
}
```

**Template — binary search on ANSWER (most powerful):**
```java
// "Find minimum capacity to ship packages in D days"
// Binary search on the answer: left=max(weight), right=sum(weights)
int left = Arrays.stream(weights).max().getAsInt();
int right = Arrays.stream(weights).sum();
while (left < right) {
    int mid = left + (right - left) / 2;
    if (canShip(weights, mid, days)) right = mid;  // mid is feasible, try smaller
    else left = mid + 1;
}
return left;
```

**Practice problems:**
- Binary Search (LeetCode 704) — baseline
- Search in Rotated Sorted Array (LeetCode 33)
- Find Minimum in Rotated Sorted Array (LeetCode 153)
- Capacity to Ship Packages (LeetCode 1011) — binary search on answer
- Koko Eating Bananas (LeetCode 875) — binary search on answer

---

### Pattern 5 — BFS / DFS on Graphs and Trees

**When to use:** BFS = shortest path, level-by-level, minimum steps. DFS = all paths, cycle detection, topological sort.

**BFS template:**
```java
Queue<Integer> queue = new LinkedList<>();
Set<Integer> visited = new HashSet<>();
queue.offer(start);
visited.add(start);
int steps = 0;
while (!queue.isEmpty()) {
    int size = queue.size();              // process level by level
    for (int i = 0; i < size; i++) {
        int node = queue.poll();
        if (node == target) return steps;
        for (int neighbor : graph.get(node)) {
            if (!visited.contains(neighbor)) {
                visited.add(neighbor);
                queue.offer(neighbor);
            }
        }
    }
    steps++;
}
```

**DFS template (iterative with stack):**
```java
Stack<Integer> stack = new Stack<>();
Set<Integer> visited = new HashSet<>();
stack.push(start);
while (!stack.isEmpty()) {
    int node = stack.pop();
    if (visited.contains(node)) continue;
    visited.add(node);
    // process node
    for (int neighbor : graph.get(node)) stack.push(neighbor);
}
```

**Topological sort (Kahn's algorithm — BFS-based):**
```java
int[] inDegree = new int[n];
for (int[] edge : edges) inDegree[edge[1]]++;
Queue<Integer> queue = new LinkedList<>();
for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.offer(i);
List<Integer> order = new ArrayList<>();
while (!queue.isEmpty()) {
    int node = queue.poll();
    order.add(node);
    for (int neighbor : graph.get(node)) {
        if (--inDegree[neighbor] == 0) queue.offer(neighbor);
    }
}
// if order.size() != n: cycle exists
```

**Practice problems:**
- Number of Islands (LeetCode 200) — DFS/BFS on grid
- Course Schedule (LeetCode 207) — cycle detection / topological sort
- Word Ladder (LeetCode 127) — BFS shortest path
- Clone Graph (LeetCode 133)
- Rotting Oranges (LeetCode 994) — multi-source BFS

---

### Pattern 6 — Dynamic Programming

**The 5-step DP framework:**
```
1. Define subproblem: dp[i] = "answer for first i elements"
2. Find recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
3. Base case: dp[0] = ?, dp[1] = ?
4. Fill order: left to right, or define memo map
5. Extract answer: dp[n], max(dp), etc.
```

**DP templates:**

**1D DP — House Robber:**
```java
int prev2 = 0, prev1 = 0;
for (int num : nums) {
    int curr = Math.max(prev1, prev2 + num);
    prev2 = prev1;
    prev1 = curr;
}
return prev1;
```

**2D DP — Longest Common Subsequence:**
```java
int[][] dp = new int[m+1][n+1];
for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
        if (s1.charAt(i-1) == s2.charAt(j-1)) dp[i][j] = dp[i-1][j-1] + 1;
        else dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
    }
}
return dp[m][n];
```

**0/1 Knapsack:**
```java
int[] dp = new int[capacity + 1];
for (int[] item : items) {        // item[0]=weight, item[1]=value
    for (int w = capacity; w >= item[0]; w--) {   // traverse RIGHT to LEFT for 0/1
        dp[w] = Math.max(dp[w], dp[w - item[0]] + item[1]);
    }
}
return dp[capacity];
```

**Practice problems:**
- Climbing Stairs / Fibonacci — 1D DP warm-up
- House Robber I, II (LeetCode 198, 213)
- Longest Common Subsequence (LeetCode 1143)
- Coin Change (LeetCode 322) — unbounded knapsack
- 0/1 Knapsack — classic
- Longest Increasing Subsequence (LeetCode 300)
- Word Break (LeetCode 139)

---

### Pattern 7 — Heap / Priority Queue

**When to use:** "Top K", "Kth largest/smallest", "merge K sorted", "sliding window maximum."

**Min-heap for Top K largest:**
```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>(k);
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll();  // remove smallest, keep top K
}
return new ArrayList<>(minHeap);
```

**K-way merge (merge K sorted arrays):**
```java
// PriorityQueue<int[]> where int[] = {value, arrayIndex, elementIndex}
PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[0] - b[0]);
for (int i = 0; i < lists.length; i++) {
    if (lists[i] != null) heap.offer(new int[]{lists[i].val, i, 0});
}
while (!heap.isEmpty()) {
    int[] curr = heap.poll();
    // add curr[0] to result
    // add next element from same array if exists
}
```

**Practice problems:**
- Kth Largest Element in an Array (LeetCode 215)
- Top K Frequent Elements (LeetCode 347)
- Merge K Sorted Lists (LeetCode 23)
- Find Median from Data Stream (LeetCode 295) — two heaps
- Task Scheduler (LeetCode 621)

---

### Pattern 8 — Backtracking

**When to use:** Generate all combinations, permutations, subsets. "Find all solutions."

**Template:**
```java
void backtrack(int start, List<Integer> current, List<List<Integer>> result, int[] nums) {
    result.add(new ArrayList<>(current));    // add snapshot, not reference
    for (int i = start; i < nums.length; i++) {
        if (i > start && nums[i] == nums[i-1]) continue;  // skip duplicates
        current.add(nums[i]);
        backtrack(i + 1, current, result, nums);           // recurse
        current.remove(current.size() - 1);                // undo choice
    }
}
```

**Practice problems:**
- Subsets I, II (LeetCode 78, 90)
- Permutations I, II (LeetCode 46, 47)
- Combination Sum I, II (LeetCode 39, 40)
- Word Search (LeetCode 79) — backtracking on grid
- N-Queens (LeetCode 51) — classic

---

### Pattern 9 — Stack (Monotonic Stack)

**When to use:** "Next greater element", "previous smaller element", histogram area.

**Template — next greater element:**
```java
int[] result = new int[nums.length];
Arrays.fill(result, -1);
Stack<Integer> stack = new Stack<>();  // stores indices
for (int i = 0; i < nums.length; i++) {
    while (!stack.isEmpty() && nums[i] > nums[stack.peek()]) {
        result[stack.pop()] = nums[i];  // nums[i] is the next greater for stack.peek()
    }
    stack.push(i);
}
```

**Practice problems:**
- Next Greater Element I, II (LeetCode 496, 503)
- Largest Rectangle in Histogram (LeetCode 84) — classic monotonic stack
- Daily Temperatures (LeetCode 739)
- Valid Parentheses (LeetCode 20) — basic stack
- Min Stack (LeetCode 155)

---

### Pattern 10 — Trie (Prefix Tree)

**When to use:** Autocomplete, prefix search, word dictionary.

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEnd;
}
class Trie {
    TrieNode root = new TrieNode();
    void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.isEnd = true;
    }
    boolean startsWith(String prefix) {
        TrieNode node = root;
        for (char c : prefix.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return true;
    }
}
```

**Practice problems:**
- Implement Trie (LeetCode 208) — build it from scratch
- Word Search II (LeetCode 212) — Trie + backtracking
- Design Search Autocomplete (LeetCode 642)

---

### Pattern 11 — Union Find (Disjoint Set)

**When to use:** Connected components, cycle detection in undirected graph, "are these two nodes connected?"

```java
int[] parent, rank;
void init(int n) {
    parent = new int[n];
    rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
}
int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);  // path compression
    return parent[x];
}
void union(int x, int y) {
    int px = find(x), py = find(y);
    if (px == py) return;
    if (rank[px] < rank[py]) { int t = px; px = py; py = t; }
    parent[py] = px;
    if (rank[px] == rank[py]) rank[px]++;
}
```

**Practice problems:**
- Number of Connected Components (LeetCode 323)
- Redundant Connection (LeetCode 684) — cycle detection
- Accounts Merge (LeetCode 721)
- Number of Islands II (LeetCode 305)

---

### Pattern 12 — Intervals

**When to use:** Overlapping intervals, meeting rooms, merge intervals.

**Merge intervals:**
```java
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);  // sort by start
List<int[]> result = new ArrayList<>();
result.add(intervals[0]);
for (int i = 1; i < intervals.length; i++) {
    int[] last = result.get(result.size() - 1);
    if (intervals[i][0] <= last[1]) {            // overlap
        last[1] = Math.max(last[1], intervals[i][1]);
    } else {
        result.add(intervals[i]);
    }
}
```

**Meeting Rooms II (minimum rooms needed):**
```java
int[] starts = Arrays.stream(intervals).mapToInt(i -> i[0]).sorted().toArray();
int[] ends   = Arrays.stream(intervals).mapToInt(i -> i[1]).sorted().toArray();
int rooms = 0, maxRooms = 0, end = 0;
for (int start : starts) {
    if (start < ends[end]) rooms++;   // new meeting starts before previous ends
    else end++;                        // a meeting ended, reuse that room
    maxRooms = Math.max(maxRooms, rooms);
}
return maxRooms;
```

**Practice problems:**
- Merge Intervals (LeetCode 56)
- Insert Interval (LeetCode 57)
- Meeting Rooms II (LeetCode 253)
- Non-overlapping Intervals (LeetCode 435)

---

## 14.2 Coding Interview — How to Behave in the Room

```
Step 1 (2 min) — Read and clarify
  "Can the array have negative numbers? Can elements repeat? What is the expected time complexity?"
  Never start coding without clarifying.

Step 2 (3 min) — State your approach before coding
  "I'll use a sliding window approach. Here's my thinking: [explain].
   This will be O(n) time and O(1) space."
  Wait for interviewer to say "yes, go ahead."

Step 3 (10-15 min) — Code clearly
  - Write method signature first, then fill
  - Name variables meaningfully (left/right, not i/j for two pointers)
  - Add one-line comment per block of logic
  - Don't erase — cross out and rewrite to the side

Step 4 (3 min) — Trace through with example
  "Let me trace through nums=[2,7,11,15], target=9..."
  Walk each iteration. Fix bugs you find — interviewers respect self-correction.

Step 5 (2 min) — Complexity analysis
  "Time: O(n) because we visit each element once. Space: O(1) — no extra data structure."

Step 6 — Handle follow-ups
  "How would you optimize for space?" / "What if the array is sorted?" / "What if we have duplicates?"
  Think out loud. It's fine to say "I'd need a moment to think about that."
```

---

## 14.3 20 Problems to Practice Before Any Interview

Practice these in this order — each builds on the previous pattern:

| # | Problem | LeetCode | Pattern | Difficulty |
|---|---|---|---|---|
| 1 | Two Sum | 1 | HashMap | Easy |
| 2 | Best Time to Buy and Sell Stock | 121 | Sliding Window | Easy |
| 3 | Longest Substring Without Repeating Characters | 3 | Variable Window | Medium |
| 4 | Binary Search | 704 | Binary Search | Easy |
| 5 | Search in Rotated Sorted Array | 33 | Binary Search | Medium |
| 6 | Merge Intervals | 56 | Intervals | Medium |
| 7 | Number of Islands | 200 | BFS/DFS | Medium |
| 8 | Course Schedule | 207 | Topological Sort | Medium |
| 9 | Kth Largest Element | 215 | Heap | Medium |
| 10 | Top K Frequent Elements | 347 | Heap + HashMap | Medium |
| 11 | House Robber | 198 | DP | Medium |
| 12 | Coin Change | 322 | DP | Medium |
| 13 | Longest Common Subsequence | 1143 | 2D DP | Medium |
| 14 | Subsets II | 90 | Backtracking | Medium |
| 15 | Combination Sum | 39 | Backtracking | Medium |
| 16 | Daily Temperatures | 739 | Monotonic Stack | Medium |
| 17 | Largest Rectangle in Histogram | 84 | Monotonic Stack | Hard |
| 18 | Implement Trie | 208 | Trie | Medium |
| 19 | Word Ladder | 127 | BFS | Hard |
| 20 | Trapping Rain Water | 42 | Two Pointers | Hard |

**Note:** You don't need LeetCode Hard mastery for SDE-2/3 at most companies.
Solve Medium problems in under 20 minutes cleanly. That is the bar.

---

## 14.4 GSTN-Mapped Coding Problems

These are problems that map directly to algorithms inside your codebase:

| Your GSTN Feature | Maps to Algorithm | LeetCode Equivalent |
|---|---|---|
| DCR outstanding calculation (ΣDR - ΣCR) | Running sum / prefix sum | Running sum array |
| Transfer condition: find min(outstanding, amount) | Max/min in sequence | Array manipulation |
| Case status transitions (OPEN→CLOSED→DISPOSED) | Graph DFS (state machine) | Course Schedule (207) |
| Task assignment to officers | Matching / interval scheduling | Meeting Rooms II (253) |
| 12-scenario matrix (D2 × D3 states) | Multi-dimensional DP | Unique Paths II (63) |
| Holiday calendar skip logic | Interval/calendar problems | Non-overlapping Intervals (435) |
| Redis rate limiter (sliding window) | Sliding window | Minimum Window Substring (76) |
| Cache eviction (LRU) | LinkedHashMap trick | LRU Cache (146) |
| CaseMgmtFwk: select customizer by type | Factory / strategy decision | — |
| Fetch top K pending cases | Top-K heap | Kth Largest (215) |

---

# Section 15 — Behavioral Interview: Complete Prep with GSTN STAR Stories

> Product companies (Razorpay, Meesho, Flipkart, PhonePe) dedicate 30-45 minutes to
> behavioral questions. GSTN is a PERFECT source of STAR stories — high complexity,
> high stakes, government-scale, real business impact. This section gives you
> ready-to-speak answers for every major behavioral question.

---

## 15.1 The STAR Framework (Your Template for Every Answer)

```
S — Situation: context, team size, project, what was at stake
T — Task:      what was YOUR specific responsibility (not "we")
A — Action:    what you specifically did — technical decisions, trade-offs, leadership
R — Result:    measurable outcome — time saved, errors reduced, performance improved
```

**Rules:**
- Always say "I" not "we" for the Action — interviewer is evaluating YOU
- Every answer: 90 seconds to 2 minutes. Practice timing.
- End with a "learning" or "what I'd do differently" — shows growth mindset
- Prepare 8-10 STAR stories and map them to multiple questions

---

## 15.2 Your Core STAR Stories from GSTN Work

### Story 1 — "Most complex technical problem you solved"

**Use for:** "Tell me about a challenging problem", "Describe a time you solved a hard technical problem"

**STAR:**
> **Situation:** I was responsible for implementing the appeal order financial flow in GSTN's litigation platform — a system used by 140 million taxpayers. When a tax officer issues a court-ordered outcome (APL04), the system must compute whether a taxpayer gets a refund, still owes money, or is settled — based on the original demand, the first appeal outcome, and potentially a subsequent court order, across 12 possible scenario combinations.
>
> **Task:** My task was to design and implement the demand-credit-recovery (DCR) ledger calculation logic that correctly handles all 12 scenarios, including edge cases where a later court order modifies a decision that was already partially actioned — without corrupting the financial records.
>
> **Action:** I first documented all 12 scenarios as a decision matrix (original demand × first order outcome × subsequent order outcome). I implemented it using a strategy-based approach — each scenario has its own calculation path — instead of deeply nested if-else. I added explicit guards for the simultaneous-combine case where two appeal branches affect the same taxpayer at the same time, requiring atomic ledger updates with XA transactions to prevent race conditions.
>
> **Result:** The system correctly handles all 12 financial scenarios with zero data integrity incidents since launch. The decision matrix documentation I created became the reference for QA, legal compliance review, and onboarding of new engineers.
>
> **Learning:** The most valuable thing I built was not the code — it was the decision matrix. Complex business logic needs to be made explicit and visual before implementation, or you will always miss edge cases.

---

### Story 2 — "Improved system performance"

**Use for:** "Tell me about a time you improved performance", "How did you handle a scaling problem?"

**STAR:**
> **Situation:** GSTN's back-office litigation system processes millions of case operations. Many APIs were hitting the database for reference data (case types, status masters, officer maps) on every single request — data that changes at most once a day.
>
> **Task:** I needed to reduce unnecessary database load on the reference data tables without breaking consistency, especially during peak periods like GST return filing deadlines when traffic spikes dramatically.
>
> **Action:** I worked with the LocalCacheFwk framework — an in-JVM cache — and mapped over 100 reference data types that were safe to cache at startup. I added @PostConstruct loading so all master data is in JVM memory before the first request arrives. For data that changes during the day (like officer assignments), I configured TTL-based refresh via Redis in DistCacheFwk, with a scheduled refresh job every few hours. I also profiled the most-called APIs to identify which were hitting the DB unnecessarily.
>
> **Result:** Reference data lookups dropped from database queries to sub-millisecond JVM HashMap lookups. API response times for case status queries improved significantly. During the next GST filing deadline, we saw no database overload on reference data tables.
>
> **Learning:** Caching is not one-size-fits-all. Master data (100+ types, changes once a day) goes in JVM cache. Session data goes in Redis. Transactional data stays in DB. Mapping data to the right tier is the skill.

---

### Story 3 — "Worked under pressure / met a deadline"

**Use for:** "Tell me about a time you delivered under pressure", "How do you handle tight deadlines?"

**STAR:**
> **Situation:** GST return filing deadlines are fixed by government regulation — they cannot move. Our litigation module had a hard deadline to deploy the simultaneous-combine order feature before the end of the financial year. Two separate appeal processes (APL01 and APL03) can run in parallel for the same taxpayer, and when orders are issued simultaneously, the financial impacts must be combined correctly without double-counting.
>
> **Task:** I had to design, implement, and test the simultaneous-combine logic end-to-end — including the edge case where the APL03 branch's outcome needs to be stored in the APL01 case folder with a transformed payload — in a compressed timeline.
>
> **Action:** I broke the work into the most critical path first: the payload transformation and storage logic (APL03 order into APL01 APPEL_ORDRS_APLOD). I wrote the transformation code in a way that was independently testable without needing the full system. I paired with the QA team daily instead of waiting for a handoff, writing test cases alongside code. I also documented the logic as I went so there was no documentation debt after deployment.
>
> **Result:** Feature deployed on schedule. Post-deployment, the QA-alongside-development approach caught three edge cases before production that would have been hard to debug post-deployment.
>
> **Learning:** In deadline-driven work, "done means tested and documented." Leaving documentation for later always means it never happens — and the next person who touches that code will build the wrong mental model.

---

### Story 4 — "Disagreed with a technical decision"

**Use for:** "Tell me about a time you disagreed with your team", "How do you handle technical conflict?"

**STAR:**
> **Situation:** During design of the appeal order workflow, the team was considering using a shared mutable state object passed between multiple service layers to track the running financial calculation — so each layer could update it without reloading from DB.
>
> **Task:** I was responsible for the service layer implementation and had concerns about this approach's safety under concurrent requests.
>
> **Action:** I raised the concern that shared mutable state passed between service layers creates implicit coupling and is dangerous under concurrent conditions — two requests for the same taxpayer could corrupt each other's calculation. I proposed instead that each service call be stateless — load what it needs from cache/DB, compute, return a result. I prepared a simple example showing how the shared-object approach would fail with two concurrent requests. I presented this in a team review, not as a criticism but as a risk analysis with a proposed alternative.
>
> **Result:** The team agreed to switch to the stateless approach. The implementation is simpler, easier to test, and each request is fully isolated. No concurrency bugs were reported in the financial calculation layer.
>
> **Learning:** Technical disagreements are won with data, not opinion. Show the failure mode with a concrete example. Propose an alternative, not just a criticism.

---

### Story 5 — "Took ownership beyond your role"

**Use for:** "Tell me about a time you went above and beyond", "Describe a time you showed ownership"

**STAR:**
> **Situation:** Our litigation module had complex domain logic — the appeal financial flow — that existed only in the heads of 2-3 engineers who had originally built it. New team members were taking weeks to get productive on this module.
>
> **Task:** My primary task was feature implementation, but I recognized the knowledge transfer risk.
>
> **Action:** I took it upon myself to document the entire appeal order financial flow — the 12-scenario matrix, the simultaneous-combine logic, the DCR ledger model, the case folder structure — in structured markdown documents that anyone could read. I also created the decision trees and flow diagrams. This was not asked of me and was done alongside my feature work.
>
> **Result:** The documents are now the primary onboarding material for engineers joining the litigation module. Two new engineers ramped up in their first week using these docs instead of relying on ad-hoc knowledge transfer. The documents also became reference material for compliance and QA reviews.
>
> **Learning:** Documentation is a force multiplier. One hour of writing saves ten hours of answering the same questions.

---

### Story 6 — "Learned a new technology quickly"

**Use for:** "Tell me about a time you had to learn something new fast", "How do you approach learning?"

**STAR:**
> **Situation:** GSTN's platform uses HBase for return filing data storage — a NoSQL database I had not worked with before. I was asked to work on a feature that read and wrote HBase data via the internal HbaseAccessFwk framework.
>
> **Task:** I needed to understand HBase data modeling (row keys, column families, column qualifiers) and the custom functional API (GSTFunction, GSTPredicate, Model) well enough to implement correct and performant data access.
>
> **Action:** I started by reading the HbaseAccessFwk source code — specifically Model.java (schema definition), GSTFunction.java (read operations), and Mutator.java (write operations) — to understand the framework's design before looking at usage examples. I then read HBase documentation on row key design to understand why bad row keys cause hot spots on RegionServers. Within a week I had implemented the feature, and I documented the HBase access patterns I learned for future reference.
>
> **Result:** Feature implemented correctly. More importantly, I built a mental model of HBase that helped me understand the broader GSTN platform architecture and why HBase was chosen for sparse, high-volume return data over MySQL.
>
> **Learning:** When learning a new framework, read the framework source code first, not the usage examples. Usage examples show you what to do — source code shows you why it works.

---

## 15.3 Common Behavioral Questions — Mapped to Your Stories

| Question | Best Story to Use |
|---|---|
| Tell me about yourself | Your 2-minute intro (see 15.4) |
| Most challenging technical problem? | Story 1 (12-scenario matrix) |
| Improved performance? | Story 2 (caching) |
| Delivered under pressure? | Story 3 (simultaneous-combine deadline) |
| Disagreed with a decision? | Story 4 (shared mutable state) |
| Went above and beyond? | Story 5 (documentation) |
| Learned something new quickly? | Story 6 (HBase) |
| Tell me about a failure / mistake | See 15.5 |
| Why are you leaving GSTN? | See 15.6 |
| Where do you want to be in 5 years? | See 15.7 |
| Why do you want to join us? | Research company, tie to your interests |
| What is your biggest strength? | Story 1 + "I turn complex business logic into clean, testable code" |
| What is your biggest weakness? | Honest + growth plan (see 15.5) |

---

## 15.4 Your 2-Minute "Tell Me About Yourself"

> Speak this out loud 10 times until it flows naturally.

"I'm a Java backend engineer with 5.6 years of experience, currently at GSTN — India's national tax compliance platform serving 140 million taxpayers. I specialize in building high-stakes, high-scale systems where correctness is non-negotiable — things like financial ledger engines, multi-step workflow orchestration, and distributed caching.

At GSTN I've worked primarily on the litigation module — the system that manages tax disputes and appeal orders. The most technically interesting part was designing the financial computation logic for appeal outcomes: the system has to correctly calculate whether a taxpayer gets a refund, still owes tax, or is settled, across 12 scenario combinations, with edge cases for concurrent orders, all while maintaining double-entry ledger integrity under XA transactions.

Beyond business logic, I've worked closely with our shared platform frameworks — an AOP-based audit system that publishes Protobuf events to Kafka, a ThreadLocal-based multi-region database router, and a distributed Redis cache with 40+ cached data types.

I'm now looking for an SDE-2 role at a product company where I can work on systems at consumer scale — where design decisions have direct user impact. I'm particularly interested in [company name] because [one specific thing about their tech/product/culture]."

---

## 15.5 Weakness + Failure Question

**Weakness (honest, with growth plan):**
> "I sometimes over-engineer at the design stage — I'll think through more scenarios than
> actually needed and that can slow initial implementation. I've been working on this by
> forcing myself to scope to the MVP first and document the 'what if' scenarios separately,
> so they're captured but don't block shipping. The appeal order decision matrix was actually
> born from this — I documented all 12 scenarios so the edge cases were visible and
> resolved before I started coding."

**Failure (real, with learning):**
> "Early in my career I delivered a feature without considering the concurrent access scenario
> — two tax officers updating the same case simultaneously caused a data conflict. It wasn't
> caught in single-threaded testing. After that incident, I added concurrent access scenarios
> as a mandatory item in my personal review checklist for every service I build. I also
> introduced optimistic locking on case state transitions so conflicts are detected and
> surfaced rather than silently overwriting each other."

---

## 15.6 Why Are You Leaving GSTN?

> Do NOT say: negative things about GSTN, your manager, your team, money.
> DO say: growth, scope, tech stack, consumer scale.

**Template:**
> "GSTN has been a great place to build deep backend engineering skills — I've worked on
> complex domain problems and production systems at real scale. What I'm looking for now
> is a product company environment where I can work on systems that directly impact
> end-user experience, iterate faster, and work with more modern technology choices.
> I want to be in an engineering culture where there's strong emphasis on code quality
> and technical growth, and I think [company] offers exactly that."

---

## 15.7 Where Do You Want to Be in 5 Years?

> Avoid: "I want to be a manager" (unless truly) or "I don't know."

**Template:**
> "In 5 years, I want to be a senior engineer who is a go-to person for distributed systems
> and backend platform design — someone who can design a new system end-to-end, mentor
> junior engineers, and drive technical decisions. I'm less focused on titles and more
> focused on the quality of problems I'm solving. If I look back in 5 years and have
> built systems that handle serious scale with high reliability, and helped others grow
> technically, I'll consider that a success."

---

## 15.8 Company Research Template

Fill this for each company before the interview:

```
Company: _________________
Product I use / know: _______________
Why their tech is interesting to me: _______________
A recent engineering blog post I read: _______________
One technical challenge they must solve at scale: _______________

My opening line for "Why do you want to join us?":
"I read your [blog post / talk] about [X], and the way you solved [Y] using [Z] is exactly
the kind of problem I want to be working on. Combined with [product I use / impact at scale],
this feels like the right next step for me."
```

**Target companies' engineering blogs:**
- Flipkart: tech.flipkart.com
- Razorpay: engineering.razorpay.com
- PhonePe: tech.phonepe.com
- Meesho: tech.meesho.com
- Zerodha: zerodha.tech
- Zomato: engineering.zomato.com
- Swiggy: bytes.swiggy.com
- Goldman Sachs: developer.gs.com/blog

---

## 15.9 Questions to Ask the Interviewer

> Always have 3 questions ready. Asking good questions = showing preparation and seniority.

**Technical questions:**
- "What does the on-call rotation look like for the team? How are production incidents handled?"
- "What is the biggest technical challenge the team is facing right now?"
- "How is the decision made between building vs buying a platform component?"
- "What does the deployment pipeline look like? How often does the team ship to production?"

**Team and culture:**
- "How does the team handle technical disagreements about architecture?"
- "What would success look like for me in the first 3 months?"
- "What is the biggest thing you'd want a new engineer to know before joining?"

**Growth:**
- "How does the team approach technical learning and growth? Do engineers have dedicated time for it?"

---

# Section 16 — DDIA Deep Dive: Concepts That Separate SDE-2 from SDE-3

> "Designing Data-Intensive Applications" by Martin Kleppmann is the most cited book
> in senior backend interviews. This section maps every key DDIA concept to:
> (1) what it means, (2) the interview question it answers, (3) your GSTN equivalent.
> If you can speak to these with your GSTN experience, you will sound like SDE-3.

---

## 16.1 Storage Engines — B-Tree vs LSM-Tree

**Why this matters in interviews:** "What happens inside a database when you write a row?"
This is asked at Razorpay, Goldman Sachs, Flipkart for SDE-3.

### B-Tree (MySQL InnoDB, PostgreSQL)

```
Structure: balanced tree of pages (typically 4KB each)
           each page = array of sorted key-value pairs

Write path:
  1. Find correct leaf page (tree traversal, O(log n))
  2. Update page in-place
  3. Write to WAL (Write-Ahead Log) first for crash recovery
  4. If page full → split page into two (expensive — random write)

Read path:
  O(log n) tree traversal — predictable, fast for point queries

Write-Ahead Log (WAL):
  Before modifying any page, write the intent to a sequential log file
  On crash recovery: replay WAL to restore consistent state
  This is why MySQL is crash-safe even if the OS kills the process mid-write
```

**GSTN connection:** MySQL is your primary case/ledger store. Every `UPDATE case SET status=?`
goes through InnoDB's B-Tree + WAL. Your `@Version` optimistic locking works because
InnoDB holds row-level locks during the UPDATE on the B-Tree leaf page.

### LSM-Tree (HBase, Cassandra, RocksDB)

```
Structure: memtable (in-memory sorted buffer) + SSTables (immutable sorted files on disk)

Write path:
  1. Append to WAL (for crash recovery)
  2. Write to memtable (in-memory, O(log n) sorted insert)
  3. When memtable full → flush to disk as SSTable (sorted, immutable)
  4. Background compaction: merge SSTables, remove tombstones
  → All writes are SEQUENTIAL (fast for write-heavy workloads)

Read path:
  1. Check memtable
  2. Check bloom filter (is key in this SSTable? saves disk reads)
  3. Scan SSTables from newest to oldest
  → Reads are SLOWER than B-Tree (must check multiple files)
  → Bloom filter makes this practical

Compaction strategies:
  Size-tiered: merge SSTables of similar size — good for write-heavy
  Leveled: compact into levels with size limits — better read performance (Cassandra default)
```

**GSTN connection:** HBase uses LSM-Tree internally (backed by HFile = SSTable).
This is WHY HBase is write-optimized for return filing data — millions of taxpayers
writing GSTR1 entries concurrently. All writes are sequential appends to memtable.

### Interview Answer — "When would you choose LSM-Tree over B-Tree?"

> "B-Tree is better for read-heavy, mixed workloads — MySQL, PostgreSQL. Reads are O(log n)
> with predictable performance. LSM-Tree is better for write-heavy workloads — HBase,
> Cassandra. Writes are always sequential (memtable → SSTable flush), so write throughput
> is much higher. The trade-off is read amplification: LSM-Tree reads may check multiple
> SSTables, mitigated by bloom filters. Compaction also causes write amplification — each
> byte written once may be rewritten multiple times during compaction. At GSTN, we use
> MySQL (B-Tree) for transactional case/ledger data and HBase (LSM-Tree) for write-heavy
> return filing data — exactly the right tool for each workload."

---

## 16.2 Replication — Single-Leader, Multi-Leader, Leaderless

**Why this matters:** "How would you ensure high availability for your database?"
"What is replication lag? When does it cause problems?"

### Single-Leader Replication (MySQL, PostgreSQL)

```
Leader:   accepts all writes, replicates to followers
Followers: serve reads only, apply leader's replication log

Replication log formats:
  Statement-based:  replicate the SQL statement — risky (NOW(), RAND() are non-deterministic)
  WAL shipping:     ship the binary WAL to follower — tightly coupled to storage engine version
  Row-based (logical): replicate the actual rows changed — most common (MySQL binlog default)

Synchronous replication:
  Leader waits for follower to confirm before ack'ing write
  Guarantees: no data loss if leader crashes
  Cost: one slow follower slows all writes

Asynchronous replication (MySQL default):
  Leader ack's write immediately, replicates in background
  Risk: follower may lag behind — replication lag
  Risk: if leader crashes before follower catches up → data loss

Replication Lag Problems:
  Read-your-writes: user writes, then reads from lagging follower → sees old data
    Fix: read from leader for 1 min after write, or route by userId
  Monotonic reads: user makes multiple reads, hits different followers at different lag
    Fix: always route same user to same replica (sticky sessions on replica)
  Consistent prefix reads: user sees events out of order (B happened before A in their view)
    Fix: causally related writes go to same partition
```

**GSTN connection:** Your MySQL primary (case writes) + read replicas (case list queries).
Replication lag means a just-issued APL04 order might not immediately appear on the
list view if it reads from a lagging replica. Fix: route post-issuance reads to primary
for the next 5 seconds (read-your-writes guarantee).

### Multi-Leader Replication (CouchDB, Google Docs, multi-datacenter)

```
Multiple nodes accept writes independently
Problem: write conflicts — two users edit same row on different leaders
Conflict resolution strategies:
  Last-Write-Wins (LWW): highest timestamp wins — data loss risk
  Merge: custom application logic merges conflicting versions
  CRDT (Conflict-free Replicated Data Type): data structure that auto-merges

When to use: multi-datacenter active-active, offline clients (mobile apps)
When NOT: when you need strong consistency (financial systems like GSTN)
```

### Leaderless Replication (Cassandra, DynamoDB — Dynamo-style)

```
Any node accepts writes and reads
Quorum: N replicas, W write quorum, R read quorum
  W + R > N → read sees at least one node with latest write (overlap)
  
Common: N=3, W=2, R=2 → strong consistency
         N=3, W=1, R=1 → eventual consistency, maximum availability

Sloppy quorum: during network partition, write to non-designated nodes temporarily
Hinted handoff: temporary nodes forward writes to original node when it recovers

Read repair: when reading, compare versions across replicas → write back newest
Anti-entropy: background process that syncs replicas for missed writes

Version vectors: each node maintains version per replica, merges on read
  [A:2, B:3] = A wrote 2 times, B wrote 3 times → can detect conflicts
```

**Interview Answer — "What is quorum? How does N=3,W=2,R=2 guarantee consistency?"**

> "In a leaderless system with N=3 replicas, W=2 means a write is confirmed when 2 of 3
> replicas ack. R=2 means a read queries 2 of 3 replicas and takes the latest version.
> Since W+R=4 > N=3, there is always at least 1 replica overlap between any write set
> and any read set — so the read will always see at least one copy of the latest write.
> Cassandra uses this. For GSTN's financial operations, we'd need W=3 (all replicas must
> confirm) to guarantee no data loss, which is why we use XA with synchronous replication
> rather than eventual consistency."

---

## 16.3 Partitioning (Sharding) — Strategies and Trade-offs

**Why this matters:** "How would you partition a database with 100M users?"

### Partitioning by Key Range

```
Example: partition by GSTIN first character (A-E = partition 1, F-J = partition 2...)
Pro:  range queries are efficient (give me all GSTINs starting with 27... = Maharashtra)
Con:  hot spots — all Maharashtra filings hit one partition at deadline
GSTN: partitions by stateCd (natural range boundary) — you use this!
```

### Partitioning by Hash

```
Example: hash(GSTIN) % 100 → partition number
Pro:  evenly distributed, no hot spots
Con:  range queries impossible (all GSTINs between X and Y requires full scan)
Used by: Cassandra, MongoDB (hashed sharding), Redis Cluster

Consistent hashing:
  Problem with hash % N: when N changes (add/remove node), most keys remap
  Solution: hash ring with virtual nodes
    - hash space = 0 to 2^32, arranged in a ring
    - each node owns an arc of the ring
    - key maps to clockwise next node on ring
    - adding a node: only keys between new node and its predecessor move
    - virtual nodes: each physical node has K positions on ring → better balance
```

### Secondary Index Partitioning

```
Document-based (local index): each partition has its own secondary index
  Write: update only local partition's index — fast
  Read: scatter-gather query (must query ALL partitions, merge results) — slow
  Used by: MongoDB, Cassandra

Term-based (global index): index itself is partitioned, covers all partitions
  Write: must update index partition (may be on different node) — can be async
  Read: single index partition query — fast
  Used by: DynamoDB (GSI), Elasticsearch
```

**GSTN connection:** Your sharding is range-based by `stateCd`. Query "all cases in state 27"
hits exactly one shard. Query "all cases for GSTIN XYZ across all years" may need to
know the state first. Your `DbContextHolder` implements the shard routing layer.

**Interview Answer — "How does consistent hashing help when you add a cache node?"**

> "With regular hash % N, adding one node to a 10-node cluster remaps 90% of keys —
> every cache miss on rebalancing. Consistent hashing puts nodes on a ring. Adding
> a node only takes keys from its predecessor on the ring — roughly 10% of keys
> remapped for a 10-node cluster. Virtual nodes (each physical node gets K positions)
> smooth out uneven distribution caused by hash collisions at the ring positions."

---

## 16.4 Transactions — Beyond ACID

**Why this matters:** These are SDE-3 interview questions. Most candidates stop at "ACID."

### Write Skew and Phantom Reads

```
Write Skew (not prevented by READ_COMMITTED or REPEATABLE_READ):
  Two transactions read the same data, make decisions based on it, then both write
  — but each write invalidates the other's premise.

  Example from GSTN:
    TX1: reads case count for officer = 5 (under max 10)
         assigns case to officer
    TX2: reads case count for officer = 5 (under max 10)  ← reads before TX1 commits
         assigns case to officer
    Result: officer has 12 cases — both transactions were "correct" individually
    Fix: SELECT FOR UPDATE on the count row, or use SERIALIZABLE isolation

  Another example: "On-call doctor"
    Two doctors check if anyone is on call — both see the other is available
    Both mark themselves as off-call → nobody is on call
    Fix: SERIALIZABLE isolation or explicit locking

Phantom Read (not prevented by REPEATABLE_READ):
  TX1 reads a range, TX2 inserts a new row in that range, TX1 reads range again — sees new row
  Fix: SERIALIZABLE isolation (uses predicate locks or next-key locks)

Serializable Snapshot Isolation (SSI):
  Optimistic concurrency control — allow transactions to run in parallel
  At commit: detect if any premise was violated (another TX committed a conflicting write)
  If conflict: abort and retry one of them
  Used by: PostgreSQL (SERIALIZABLE isolation level), FoundationDB
  Better than 2PL (Two-Phase Locking): no blocking, high concurrency, only abort on actual conflict
```

### Two-Phase Locking (2PL) vs MVCC

```
Two-Phase Locking (2PL):
  Growing phase: acquire locks (shared for read, exclusive for write)
  Shrinking phase: release locks (after commit/rollback)
  Guarantees: serializability
  Problem: deadlocks (both TX1 and TX2 waiting for each other's lock)
  Problem: long-running reads block all writes (shared lock held for duration)
  Used by: MySQL SERIALIZABLE, many legacy DBs

MVCC (Multi-Version Concurrency Control):
  Readers don't block writers, writers don't block readers
  Each transaction sees a snapshot of the DB at its start time
  Old versions kept until no transaction needs them (vacuum/purge process)
  Writers can conflict only with other writers, not readers
  Used by: PostgreSQL, MySQL InnoDB (default), Oracle

Your GSTN code:
  @Version optimistic locking = application-level MVCC concept
  If two officers issue APL04 simultaneously:
    TX1: reads Case version=5, TX2: reads Case version=5
    TX1 commits: UPDATE case SET version=6 WHERE version=5 → succeeds
    TX2 commits: UPDATE case SET version=6 WHERE version=5 → 0 rows affected → OptimisticLockException
    TX2 retries → reads version=6 → sees TX1's committed order → fails state validation → returns error
```

### Distributed Transactions — 2PC Deep Dive

```
Two-Phase Commit (2PC):
  Phase 1 (Prepare):
    Coordinator sends "prepare" to all participants
    Each participant writes prepare record to its WAL, sends "yes" or "no"
    If any participant sends "no" → coordinator sends "abort" to all

  Phase 2 (Commit):
    If all "yes" → coordinator writes commit record to its WAL
    Coordinator sends "commit" to all participants
    Each participant commits and releases locks

Problems with 2PC:
  Coordinator SPOF: if coordinator crashes after Phase 1 but before Phase 2
    → participants are in "prepared" state, holding locks, can't proceed or abort
    → they are "in doubt" until coordinator recovers
  Blocking protocol: participants hold locks from Phase 1 until Phase 2 completes
  Performance: 2 network round trips minimum, more for large participant sets

XA (eXtended Architecture):
  Standard interface for 2PC across different resource managers (JDBC, JMS)
  Atomikos: Java XA transaction manager you use in GSTN
  XADataSource: wraps regular datasource to participate in XA TX
  javax.transaction.UserTransaction: programmatic TX demarcation

Your GSTN advantage:
  You can say "I used XA transactions in production for appeal order issuance,
  coordinating case DB, ledger DB, and workflow DB. I understand the coordinator
  SPOF problem and why we mitigated it by making the operation low-frequency and
  accepting the latency trade-off for correctness."
```

---

## 16.5 Consistency Models — The Full Spectrum

**Why this matters:** "What is linearizability? How is it different from serializability?"
This is a classic SDE-3 question that trips up most candidates.

```
Spectrum from strongest to weakest:

1. LINEARIZABILITY (Strongest)
   "Once a write is confirmed, all subsequent reads from ANY node see that write"
   = real-time ordering guarantee
   = single-copy illusion (behaves as if there's one copy of data)
   Example: after APL04 order is committed, any officer on any server sees it immediately
   Cost: high — requires synchronous replication or consensus protocol
   CAP: CP systems provide this (sacrifice availability)

2. SEQUENTIAL CONSISTENCY
   All operations appear to execute in some sequential order
   That order is consistent with each process's own operations
   Weaker than linearizability: no real-time guarantee (can see old data for a while)

3. CAUSAL CONSISTENCY
   If A happened before B (A caused B), everyone sees A before B
   Concurrent events may be seen in different orders by different nodes
   "Comment on a post only visible after the post" — causal dependency respected
   Stronger than eventual, weaker than sequential

4. EVENTUAL CONSISTENCY (Weakest)
   Eventually all replicas will converge to the same value if no new writes
   No timing guarantee — could take seconds or minutes
   Example: DNS propagation, Cassandra with W=1,R=1

DIFFERENCE between Linearizability and Serializability:
  Linearizability: about single-object, single-operation recency guarantee
  Serializability: about multi-object transactions executing as if serial
  STRICT SERIALIZABILITY = both = gold standard (what GSTN's XA provides)

Why this is hard in distributed systems:
  Network delays mean you can't know if a message arrived
  Clocks on different machines drift (can't use timestamps for ordering)
  Solution: consensus algorithms (Raft, Paxos) achieve linearizability
```

### Consensus and Leader Election — Raft Basics

```
Consensus problem: multiple nodes must agree on a single value, even if some nodes crash

Raft algorithm (easier to understand than Paxos):
  Nodes have 3 roles: Leader, Follower, Candidate

  Leader election:
    All nodes start as Followers with election timeout (150-300ms random)
    If no heartbeat from leader → become Candidate, increment term, request votes
    If majority votes received → become Leader
    Random timeouts prevent split votes (two candidates simultaneously)

  Log replication:
    Leader receives writes, appends to its log
    Leader sends log entries to all Followers (AppendEntries RPC)
    When majority confirm → entry is "committed" → leader applies to state machine → responds to client
    Followers apply committed entries

  Safety guarantee: only nodes with up-to-date logs can win election
    → committed entries are never lost even if leader crashes

ZooKeeper uses ZAB (similar to Raft) for coordination:
  GSTN could use ZooKeeper for: distributed lock, leader election for batch jobs
  But Redis SETNX is simpler for single-value distributed locks

Interview Answer — "How does Raft ensure a leader with stale data can't be elected?"
  "Raft requires a candidate to have a log at least as up-to-date as any node
   it's requesting a vote from. Follower votes 'no' if its log is more up-to-date.
   Since committed entries are on a majority of nodes, and any majority overlaps with
   the committed majority, at least one node in any election majority has all committed entries."
```

---

## 16.6 Data Encoding and Schema Evolution

**Why this matters:** "How does your system handle schema changes without downtime?"
Directly relevant to your GSTN Protobuf + Kafka work.

### Encoding Formats Compared

```
JSON:
  Human-readable, no schema required, widely supported
  Problems: no type safety (number vs string), field names repeated in every message
  Size: field names add overhead ({"demandId": 12345} vs just 12345)
  Schema evolution: add fields freely, consumers ignore unknown fields (if lenient parser)

XML:
  Verbose, namespace complexity, heavy for machine-to-machine
  
Avro:
  Schema embedded in file or stored in schema registry
  No field names in binary encoding — schema required to decode
  Schema evolution: add/remove fields with defaults — reader and writer schemas can differ
  Compact binary encoding
  
Protobuf (Protocol Buffers — what GSTN uses):
  Schema in .proto file, compiled to language-specific classes
  Each field has a number tag (not name) — used in binary encoding
  Schema evolution rules:
    BACKWARD COMPATIBLE (new code reads old data):
      Add new optional field — old data just doesn't have it (treated as default)
      Remove optional field — new code ignores it
    FORWARD COMPATIBLE (old code reads new data):
      Old code sees unknown field tags — ignores them (must not remove old field tags)
    BREAKING (avoid):
      Changing field tag numbers — old/new code reads wrong fields
      Changing field type — encoding may be incompatible

  Your GSTN GstAopFwk:
    ApiAuditLog.proto → compiled to ApiAuditLog.java
    KafkaAuditProducer serializes with Protobuf (not JSON) — 5-10x smaller message
    Consumer can be deployed independently with different proto version if fields follow rules
```

### Schema Registry Pattern

```
Problem: producers and consumers must agree on schema
         if producer changes schema, how does consumer know?

Schema Registry (Confluent Schema Registry):
  Central store of all schema versions, with compatibility checks
  Producer: registers schema, gets schema ID (e.g., 42)
  Message: [magic byte][schema ID (4 bytes)][protobuf/avro payload]
  Consumer: reads schema ID from message, fetches schema from registry, decodes

Compatibility types:
  BACKWARD:  new schema can read data written with old schema (add fields with defaults)
  FORWARD:   old schema can read data written with new schema (remove fields)
  FULL:      both backward and forward (only add/remove optional fields with defaults)
  NONE:      no compatibility checks — dangerous in production

Your GSTN Kafka:
  Even without a formal schema registry, using Protobuf enforces field tag discipline
  which achieves FULL compatibility as long as you follow Protobuf evolution rules
```

---

## 16.7 Stream Processing — Event Time vs Processing Time

**Why this matters:** "How would you build a real-time dashboard for case filings per minute?"

```
Two types of time:
  Event time:      when the event actually occurred (in the source system)
  Processing time: when the event was processed by the stream processor

The difference matters:
  Mobile user files GST return at 11:58 PM (event time)
  Network delay → Kafka receives it at 12:02 AM (processing time)
  Filing deadline was midnight — is it on time?
  → Must use EVENT TIME for correct deadline calculation

Windowing:
  Tumbling window: fixed non-overlapping (0:00-0:01, 0:01-0:02...)
  Sliding window:  overlapping with stride (0:00-0:05, 0:01-0:06...)
  Session window:  gap-based (group events with <30min gap into one session)

Watermarks:
  "All events with timestamp ≤ T have arrived"
  When stream processor sees watermark T → it can emit results for windows up to T
  Watermark T = max(event_time) - allowed_lateness (e.g., 10 seconds)
  Trade-off: larger allowed_lateness = more correct but higher output latency

Exactly-once in stream processing:
  Idempotent producer + transactional consumer = exactly-once
  Apache Flink: checkpointing + barriers in stream = exactly-once stateful processing
  Kafka Streams: built-in exactly-once with Kafka transactions

GSTN connection:
  Your Kafka consumers process audit events — at-least-once delivery is fine
  (duplicate audit log = acceptable, missed audit log = not acceptable)
  For deadline calculation (was GSTR3B filed before 11:59 PM?) → must use event time
  For case assignment SLA (case not actioned in 30 days → escalate) → processing time OK
```

---

## 16.8 Batch Processing and the Unix Philosophy

**Why this matters:** "How would you process 140 million taxpayer records nightly?"

```
MapReduce mental model:
  Map:    for each input record, emit (key, value) pairs
  Shuffle: group all values by key
  Reduce: for each key, aggregate its values into output

  Example: find total outstanding per state
    Map:    (caseId, state, outstanding) → emit (state, outstanding)
    Reduce: sum all outstandings per state

Limitations of MapReduce:
  Each MapReduce job writes output to disk → next job reads from disk
  Multi-step pipelines = many disk reads/writes
  Fix: Spark (in-memory, lazy evaluation, DAG of transformations)

Modern batch processing (Spark):
  RDD (Resilient Distributed Dataset): immutable, partitioned collection
  Transformations: map, filter, groupBy, join — LAZY (not executed immediately)
  Actions: count, collect, save — trigger execution
  DAG scheduler: computes optimal execution plan, avoids unnecessary shuffles

GSTN batch jobs likely include:
  Demand expiry batch: mark unpaid demands past due date as overdue
  DCR reconciliation: verify all DR entries have matching CR or outstanding balance
  Audit log archival: move audit records older than 7 years to cold storage
  Notification batch: send pending hearing reminders
  
For these, you would use:
  Spring Batch (what GSTN probably uses): Job → Steps → ItemReader/ItemProcessor/ItemWriter
  Each step reads chunks (commit-interval=100), processes, writes — crash-safe with job restarts
  JobRepository: stores job execution state in DB (restart from last checkpoint on failure)
```

---

## 16.9 Change Data Capture (CDC) — The Outbox Pattern Done Right

**Why this matters:** "How do you ensure a Kafka event is published if and only if the DB transaction commits?"

```
The Dual Write Problem:
  // WRONG — not atomic:
  dbRepository.save(order);           // step 1: save to DB
  kafkaTemplate.send("orders", order) // step 2: send to Kafka
  // If process crashes between step 1 and 2:
  //   DB has the order, Kafka does not → downstream systems never get the event

Outbox Pattern (DDIA solution):
  // RIGHT — atomic with DB:
  @Transactional
  public void createOrder(Order order) {
      orderRepo.save(order);                          // save business entity
      outboxRepo.save(new OutboxEvent("ORDER_CREATED", toJson(order)));  // same TX
  }
  // Separate process polls outbox table and publishes to Kafka
  // On success: delete from outbox
  // On failure: retry (at-least-once delivery)

  Why this works:
    Both DB save and outbox insert are in ONE transaction — either both commit or both rollback
    Kafka publish is outside the transaction — but if it fails, the outbox row is still there
    Polling/retry guarantees eventual delivery

CDC (Change Data Capture) — better than polling:
  Database replication log (MySQL binlog, PostgreSQL WAL) captures every change
  Debezium reads the binlog and publishes change events to Kafka — zero polling latency
  The DB commit IS the Kafka publish trigger — no outbox table needed
  
  Debezium → Kafka event format:
    {before: {...}, after: {...}, op: "u"} // op: c=create, u=update, d=delete

GSTN connection:
  Your KafkaAuditProducer in GstAopFwk publishes AFTER the method completes
  If the DB transaction commits but the Kafka publish fails → audit event lost
  Outbox pattern would fix this: write audit event to DB outbox in same TX,
  separate async process publishes to Kafka, deletes on success
```

---

## 16.10 DDIA-Informed System Design Checklist

**Use this mental checklist for every HLD problem in interviews:**

### Storage Layer Questions
```
[ ] What is the read/write ratio? (read-heavy → B-Tree+replica, write-heavy → LSM/Cassandra)
[ ] Does it need ACID transactions? (financial = yes → PostgreSQL/MySQL)
[ ] Is the data schema flexible or structured? (flexible → MongoDB, structured → SQL)
[ ] What is the data size and growth rate? (10TB+ → consider partitioning from day 1)
[ ] Are there time-series patterns? (metrics, logs → InfluxDB, TimescaleDB)
[ ] Does it need full-text search? (→ Elasticsearch, separate from main DB)
```

### Replication Questions
```
[ ] What is the RTO (Recovery Time Objective)? (minutes → synchronous replica)
[ ] What is the RPO (Recovery Point Objective)? (0 data loss → synchronous write)
[ ] Can reads be slightly stale? (yes for most → async replica + read-your-writes fix)
[ ] Multi-datacenter? (yes → multi-leader or leaderless with conflict resolution)
```

### Consistency Questions
```
[ ] Is this a financial/legal system? (yes → linearizability, ACID, XA or Saga)
[ ] Can you tolerate read-your-writes violations? (no for user-facing → route post-write reads to leader)
[ ] Is eventual consistency acceptable? (yes for notifications, dashboards, analytics)
[ ] Are there concurrent write conflicts? (yes → optimistic locking @Version or application-level CRDT)
```

### Partition/Scale Questions
```
[ ] What is the natural partition key? (user_id, tenant_id, state_cd in GSTN)
[ ] Are there hot spots? (celebrity user, filing deadline → shard relief or rate limiting)
[ ] Do you need secondary index queries? (yes → global secondary index, or scatter-gather)
[ ] Can you use consistent hashing? (yes for cache clusters and stateless services)
```

### Event/Messaging Questions
```
[ ] Is the event publish atomic with the DB write? (must be → Outbox pattern or CDC)
[ ] At-least-once or exactly-once? (exactly-once is expensive — is idempotent consumer OK?)
[ ] What is the message retention requirement? (audit = 7 years → don't delete from Kafka)
[ ] Need event time vs processing time? (deadline-sensitive → event time + watermarks)
```

---

## 16.11 DDIA Interview Questions — With Your Answers

| Question | Key Concept | Your Answer Angle |
|---|---|---|
| "Explain the WAL. Why does every serious database have one?" | Crash recovery, durability | MySQL InnoDB WAL = why your GSTN case writes survive crashes |
| "What is the difference between B-Tree and LSM-Tree? When to use each?" | Storage engines | MySQL (B-Tree) for cases, HBase (LSM) for return data |
| "What is replication lag? Give a real example of a bug it causes." | Async replication | APL04 order invisible on list view — read-your-writes fix |
| "Explain write skew. How do you prevent it?" | Transaction anomalies | Case assignment over-quota — SELECT FOR UPDATE or SERIALIZABLE |
| "What is linearizability? How is it different from serializability?" | Consistency models | Both are needed for GSTN (strict serializability via XA) |
| "What is the Outbox pattern? Why is it better than dual-write?" | Atomicity across systems | Audit event loss if Kafka publish fails after DB commit |
| "How does Raft achieve leader election?" | Consensus | ZooKeeper/etcd uses this for distributed lock coordination |
| "What is consistent hashing? What problem does it solve?" | Partitioning | Redis Cluster key distribution when nodes are added |
| "When would you choose Cassandra over MySQL?" | Trade-offs | Write-heavy, wide-column sparse data (like HBase for returns) |
| "What is a bloom filter? Where is it used?" | Performance optimization | LSM-Tree uses it to avoid disk reads for absent keys |
| "Explain CDC and Debezium. How does it compare to the Outbox pattern?" | Event streaming | Both solve dual-write problem, CDC is zero-latency |
| "What is SSI (Serializable Snapshot Isolation)?" | Advanced transactions | PostgreSQL SERIALIZABLE level — optimistic, high concurrency |

---

## 16.12 Bloom Filter — The Data Structure Every Senior Should Know

```
Problem: "Is this key in this SSTable (disk file)?"
  Checking disk is expensive. Do this millions of times = performance catastrophe.

Bloom Filter:
  Probabilistic data structure: answers "is element X in set S?"
  Answers:
    "NO"  → definitely not in set (100% accurate)
    "YES" → probably in set (false positives possible, false negatives impossible)

  How it works:
    Bit array of size m, k different hash functions
    Insert X: compute h1(X), h2(X)...hk(X) → set those bits to 1
    Query X: compute h1(X)...hk(X) → if ALL bits are 1 → "probably yes"; if ANY bit is 0 → "definitely no"
    
  False positive rate depends on: m (array size), k (hash functions), n (elements inserted)
  Larger array = lower false positive rate = more memory

  Delete: NOT SUPPORTED (clearing a bit may affect other elements sharing that bit)
  Counting bloom filter: replace bits with counters → supports delete but uses more memory

Where used:
  HBase: bloom filter per HFile (SSTable) — before reading disk, check bloom filter
  Cassandra: bloom filter per SSTable
  Redis: RedisBloom module
  Google Bigtable: original paper describes bloom filter per SSTable
  Chrome browser: uses bloom filter to check malicious URLs (compact local store)

Interview answer — "How does HBase use bloom filters for performance?"
  "HBase maintains a bloom filter for each HFile. When reading a row key,
   before doing a disk seek on an HFile, HBase checks its bloom filter.
   If the filter says 'definitely not here', skip the file entirely.
   This reduces the number of disk reads dramatically for random-access patterns.
   False positives mean occasionally reading a file unnecessarily — acceptable trade-off
   for the eliminated unnecessary reads."
```

---

## 16.13 The DDIA "Chapter to Interview Question" Map

| DDIA Chapter | Core Concept | Interview Question |
|---|---|---|
| Ch 3 — Storage Engines | B-Tree vs LSM-Tree, WAL, SSTables, compaction | "What happens when you write a row to MySQL?" |
| Ch 4 — Encoding | Protobuf, Avro, schema evolution, backward/forward compat | "How do you evolve a Kafka message schema without breaking consumers?" |
| Ch 5 — Replication | Leader/follower, replication lag, read-your-writes, quorum | "How do you ensure users always see their own writes?" |
| Ch 6 — Partitioning | Key-range vs hash, consistent hashing, secondary indexes | "How would you shard a 100M user database?" |
| Ch 7 — Transactions | ACID, 2PL, MVCC, write skew, SSI | "What is the difference between optimistic and pessimistic locking?" |
| Ch 8 — Distributed Problems | Partial failures, clocks, ordering | "Why can't you use timestamps to order distributed events?" |
| Ch 9 — Consistency & Consensus | Linearizability, Raft, total order broadcast | "What is linearizability vs serializability?" |
| Ch 10 — Batch Processing | MapReduce, Spark, joins in batch | "How would you aggregate 140M records nightly?" |
| Ch 11 — Stream Processing | Kafka, event time, watermarks, CDC, Outbox | "How do you ensure a DB write and Kafka publish are atomic?" |
| Ch 12 — Future of Data | CQRS, event sourcing, Lambda/Kappa architecture | "When would you use event sourcing?" |

---

# Section 17 — One-Stop Resource Guide + Mock Interview Bank

> This section makes the document fully self-contained.
> Every resource is hand-picked for SDE-2/SDE-3 Java backend interviews.
> Every mock question is the type actually asked at Flipkart, Razorpay, PhonePe, Meesho,
> Zerodha, Goldman Sachs, Swiggy, Zomato, Uber India for this level.

---

## 17.1 Must-Read Books (Priority Order)

### Tier 1 — Read Before Any Interview

| Book | Author | Why | Read This Part First |
|---|---|---|---|
| **Designing Data-Intensive Applications** | Martin Kleppmann | Best distributed systems book ever written. Every concept in Section 16 is from here. | Ch 5 (Replication), Ch 7 (Transactions), Ch 9 (Consistency) |
| **Effective Java (3rd Edition)** | Joshua Bloch | Java best practices that interviewers expect — equals/hashCode, generics, concurrency, lambdas | Item 1-17 (creating/destroying objects), Item 66-84 (concurrency) |
| **Clean Code** | Robert C. Martin | Code quality questions in interviews — naming, functions, classes, boundaries | Ch 1-5, Ch 9-10 |
| **Head First Design Patterns** | Freeman & Freeman | Visual, memorable pattern explanations — Strategy, Observer, Factory are in your code | Ch 1 (Strategy), Ch 2 (Observer), Ch 4 (Factory) |

### Tier 2 — Read During Deep Dive Phase

| Book | Author | Why | Best Chapters |
|---|---|---|---|
| **Java Concurrency in Practice** | Brian Goetz | The definitive Java threading book — ThreadLocal, locks, executor framework | Ch 2-5 (thread safety, sharing, composition), Ch 12 (testing concurrent programs) |
| **Spring in Action (6th Edition)** | Craig Walls | Spring Boot internals, security, data, messaging in one book | Ch 4 (Spring Security), Ch 8 (Reactive), Ch 10 (Kafka integration) |
| **Release It! (2nd Edition)** | Michael Nygard | Stability patterns: circuit breaker, bulkhead, timeout — concepts behind Resilience4j | Ch 4 (Stability Patterns) — read this one chapter |
| **System Design Interview Vol 1 & 2** | Alex Xu | Structured HLD walkthroughs for all common systems | Vol 1 Ch 1 (framework), then any chapter matching your target company's domain |

### Tier 3 — Reference (Dip In as Needed)

| Book | Why |
|---|---|
| **High Performance MySQL** | If asked about DB tuning — index internals, query optimization, replication setup |
| **Redis in Action** | Redis data structures and patterns in depth |
| **Kafka: The Definitive Guide** | Kafka internals, producer/consumer tuning, exactly-once |

---

## 17.2 Must-Watch Videos (YouTube — Free)

### System Design

| Channel / Video | Topic | Duration | When to Watch |
|---|---|---|---|
| **ByteByteGo — System Design Fundamentals** (playlist) | Covers every HLD building block with visuals | 10-15 min each | Week 7 of study plan |
| **Gaurav Sen — Consistent Hashing** | Best visual explanation of the concept | 12 min | Before any sharding question |
| **Gaurav Sen — Message Queues** | Kafka vs RabbitMQ, when to use what | 18 min | Before any async system design |
| **Gaurav Sen — Microservices vs Monolith** | Trade-offs, migration strategy | 15 min | Before any architecture question |
| **TechDummies — Design WhatsApp** | End-to-end real-time messaging design | 45 min | Week 9 |
| **Exponent — Design a Rate Limiter** | Full mock with interviewer interaction | 35 min | Week 7 |
| **Exponent — Design Twitter** | Fan-out on write vs read, timeline generation | 40 min | Week 9 |
| **Jordan has no life — DDIA series** | Chapter-by-chapter DDIA walkthrough | 20-30 min each | Alongside reading DDIA |
| **Hussein Nasser — Postgres Internals** | B-Tree, MVCC, WAL, vacuum explained visually | 45 min | Before any DB internals question |
| **Hussein Nasser — Kafka internals** | Partitions, consumer groups, exactly-once | 30 min | Week 5 |

### LLD / Machine Coding

| Channel / Video | Topic | When to Watch |
|---|---|---|
| **Soumyajit Bhattacharyya (YouTube)** | Live machine coding — Parking Lot, Snake-Ladder | Week 4 |
| **Udit Agarwal — LLD playlist** | 10+ machine coding problems with walkthrough | Week 4-6 |
| **Code With Mosh — Design Patterns** | All 23 GoF patterns with Java examples | Week 1-2 |
| **in28minutes — Spring Boot Master Class** | Spring Boot + JPA + Security + Actuator | Before Spring questions |

### Java / Concurrency

| Channel / Video | Topic |
|---|---|
| **Venkat Subramaniam — Functional Java** | Lambdas, streams, CompletableFuture — modern Java |
| **Jacob Jenkov — Java Concurrency** | ThreadLocal, ExecutorService, ReentrantLock, CountDownLatch |
| **Defog Tech — Java Memory Model** | volatile, happens-before, race conditions explained |

---

## 17.3 Must-Bookmark Websites

### System Design
| Site | Best For |
|---|---|
| **github.com/donnemartin/system-design-primer** | Most comprehensive free HLD reference. Read the intro + pick 3 systems to deep dive |
| **highscalability.com** | Real architecture posts from Netflix, Airbnb, Twitter, Uber — read 2-3 before each interview |
| **architecturenotes.co** | Visual system design breakdowns — short, clean, shareable |
| **bytebytego.com/newsletter** | Weekly system design visual digest — subscribe, read every Sunday |

### Engineering Blogs (target companies)
| Company | Blog URL | Best Articles to Read |
|---|---|---|
| Flipkart | tech.flipkart.com | Flik — search architecture, payment system, supply chain |
| Razorpay | engineering.razorpay.com | Payments at scale, Kafka usage, ledger system |
| PhonePe | tech.phonepe.com | UPI at scale, distributed transactions, Redis usage |
| Meesho | tech.meesho.com | Catalog search, order management, supply chain |
| Zerodha | zerodha.tech | Trading platform, Kite API, WebSocket at scale |
| Zomato | engineering.zomato.com | Delivery ETA, hyperlocal search, driver matching |
| Swiggy | bytes.swiggy.com | Surge pricing, delivery optimization, restaurant search |
| Goldman Sachs | developer.gs.com/blog | Financial systems, low-latency, data platforms |
| Uber | eng.uber.com | Geospatial, matching, surge pricing, driver tracking |

### Java / Spring
| Site | Best For |
|---|---|
| **baeldung.com** | Spring Boot, JPA, Security — every concept explained with working code |
| **vladmihalcea.com** | Hibernate internals, N+1, locking, MVCC — the best JPA deep dive blog |
| **thorben-janssen.com** | JPA advanced patterns, criteria API, performance |
| **spring.io/guides** | Official Spring Boot guides — build and run, not just theory |

### DSA Practice
| Site | Best For |
|---|---|
| **leetcode.com** | Primary practice platform. Use company tag filters for target companies |
| **neetcode.io** | Curated 150 problems + video solutions + roadmap by pattern |
| **workat.tech** | Machine coding (LLD) problems with editorials — unique to this platform |
| **interviewing.io** | Anonymous mock interviews with real engineers — free tier available |
| **pramp.com** | Free peer mock interviews — pair up with other candidates |

---

## 17.4 Full Mock Interview Bank

> These are the actual questions asked at target companies for SDE-2/SDE-3 Java backend roles.
> Format: simulate the interview — speak the answer out loud, time yourself.

---

### Round 1 — Java + Spring Deep Dive (45 min mock)

**Set the timer. Answer each question as if talking to an interviewer. Target: 3-5 min each.**

```
Q1.  Walk me through what happens from the moment a request hits your Spring Boot
     application to the moment a response is returned. Be as detailed as possible.
     [Tests: DispatcherServlet, filters, interceptors, AOP proxies, @Transactional]

Q2.  How does HashMap work internally? What is a hash collision?
     What optimization was added in Java 8 and why?
     [Tests: bucket → linked list → Red-Black Tree at size 8, load factor 0.75]

Q3.  What is the difference between ConcurrentHashMap and Collections.synchronizedMap()?
     When would you use each?
     [Tests: CAS + per-bucket sync (Java 8) vs global lock]

Q4.  I have a Spring Boot service annotated @Transactional(propagation=REQUIRED).
     It calls another method in the SAME class annotated @Transactional(propagation=REQUIRES_NEW).
     What happens? Does a new transaction start?
     [Tests: self-invocation AOP bypass — answer: NO, proxy is not called for same-class calls]

Q5.  Your service method is annotated @Transactional and @Async. What happens to
     the transaction when the async execution starts?
     [Tests: @Async runs in new thread = new transaction context, parent TX not shared]

Q6.  I have two threads both trying to increment a counter. Thread A reads 5, Thread B reads 5.
     Both increment to 6. Both write 6. Counter should be 7 but it's 6. How do you fix this?
     Name 3 different ways.
     [Tests: synchronized, AtomicInteger.incrementAndGet(), volatile (WRONG answer — explain why)]

Q7.  What is the difference between @RestController and @Controller?
     What does @ResponseBody do?
     When would you still use @Controller without @RestController?
     [Tests: view resolver vs JSON response, Thymeleaf templates]

Q8.  Walk me through @SpringBootApplication. What 3 annotations does it combine?
     How does auto-configuration actually work — what file does Spring Boot read?
     [Tests: @Configuration + @EnableAutoConfiguration + @ComponentScan, spring.factories / AutoConfiguration.imports]

Q9.  What is a BeanPostProcessor? Give a real example of where Spring uses it.
     [Tests: AutowiredAnnotationBeanPostProcessor, AOP ProxyCreator]

Q10. Explain ThreadLocal. Where did you use it in your GSTN work?
     What is the risk of not calling remove()?
     [Tests: DbContextHolder, thread pool reuse → stale state → routing to wrong DB]
```

---

### Round 2 — Database + JPA (45 min mock)

```
Q1.  I run a query: SELECT * FROM cases WHERE state_cd = 'MH' AND status = 'OPEN'
     ORDER BY created_date DESC.
     I have an index on (state_cd). Is this index being used fully? What would you add?
     [Tests: composite index (state_cd, status, created_date) — leading column rule + sort direction]

Q2.  Explain the N+1 problem. Write a JPQL query that causes it.
     Write the fix using JOIN FETCH. What is the risk of JOIN FETCH with collections?
     [Tests: Cartesian product with multiple collections — use @BatchSize or separate queries]

Q3.  What is optimistic locking? Show the @Version annotation.
     What exception is thrown on conflict? How does your caller handle it?
     [Tests: OptimisticLockException, ObjectOptimisticLockingFailureException (Spring), retry]

Q4.  Difference between TRUNCATE and DELETE. Which one can be rolled back?
     Which one resets auto-increment? Why?
     [Tests: TRUNCATE = DDL, no row-level lock, no rollback (in most DBs), resets AI;
             DELETE = DML, row-level, rollbackable, does not reset AI]

Q5.  What is a covering index? Write a query where it would eliminate a table lookup.
     [Tests: index includes all projected columns, InnoDB index-only scan]

Q6.  I have a table with 500 million rows. My query takes 30 seconds.
     Walk me through your optimization process step by step.
     [Tests: EXPLAIN plan, index analysis, partition by date, read replica, query rewrite, pagination]

Q7.  What is MVCC? How does it allow reads and writes to not block each other?
     [Tests: version snapshots, each TX sees snapshot at start time, old versions kept for active TX]

Q8.  What is the difference between REPEATABLE READ and SERIALIZABLE isolation?
     What problem does SERIALIZABLE prevent that REPEATABLE READ does not?
     [Tests: phantom reads + write skew — SERIALIZABLE prevents both]

Q9.  In GSTN, two officers could try to assign the same case to themselves simultaneously.
     How would you prevent this using database features only (no Redis)?
     [Tests: SELECT ... FOR UPDATE, or UNIQUE constraint on (case_id, assigned_officer_id)]

Q10. What is connection pool exhaustion? How do you detect it and prevent it?
     What HikariCP settings would you tune for a high-traffic API?
     [Tests: maximumPoolSize, connectionTimeout, leakDetectionThreshold, monitoring pool metrics]
```

---

### Round 3 — Distributed Systems + Kafka + Redis (45 min mock)

```
Q1.  Explain CAP theorem with a real example for each: CP system and AP system.
     Where does your GSTN system fall and why?
     [Tests: CP = MySQL/GSTN (legal correctness over availability), AP = Cassandra/DNS]

Q2.  What is a cache stampede? Walk me through exactly how it happens.
     Give 3 different ways to prevent it.
     [Tests: TTL expires → N threads miss → N DB queries; fix: mutex lock, probabilistic early refresh, stale-while-revalidate]

Q3.  You have a distributed rate limiter: max 100 requests per minute per user.
     Your API runs on 5 servers. How do you implement this correctly?
     Write the Redis commands.
     [Tests: INCR key → EXPIRE if count==1 → check > limit; Lua script for atomicity;
             key = "rate:{userId}:{minute_epoch}"]

Q4.  What is Kafka consumer group rebalancing? When does it happen?
     Why is it a problem and what can you do to minimize it?
     [Tests: triggers: consumer joins/leaves/crashes/max.poll.interval exceeded;
             minimize: heartbeat tuning, session.timeout.ms, static membership (group.instance.id)]

Q5.  Explain the difference between at-least-once and exactly-once in Kafka.
     Is exactly-once always better? When would at-least-once with an idempotent consumer be preferred?
     [Tests: exactly-once has overhead (transactions), at-least-once + dedup key is simpler and faster]

Q6.  In your GSTN AOP audit system, the DB transaction commits but the Kafka publish fails.
     What happens? How would you fix it?
     [Tests: audit event lost — dual write problem; fix: Outbox pattern or CDC with Debezium]

Q7.  Explain how Redis Cluster distributes keys. What is a hash slot?
     What happens to writes when a node fails?
     [Tests: 16384 hash slots, hash(key) % 16384, failover to replica, CLUSTERDOWN if primary+replica both fail]

Q8.  Implement a distributed lock using Redis. What are the failure scenarios?
     What is Redlock and when would you use it?
     [Tests: SET key value NX PX 30000; failures: lock holder crashes, clock skew;
             Redlock: acquire from N/2+1 nodes independently — Antirez vs Martin Kleppmann debate]

Q9.  Your Redis cache is hit by 10,000 requests per second. One key expires.
     All 10,000 threads miss and hit your DB. Walk me through what happens to your system.
     How do you prevent this at the architecture level?
     [Tests: DB connection pool exhaustion → timeouts → cascading failure;
             fix: circuit breaker in front of DB, mutex on cache refresh, key pre-warming]

Q10. What is consistent hashing? Draw a ring with 3 nodes.
     Now add a 4th node. Which keys move?
     [Tests: only keys between new node and its predecessor on the ring move — ~25% for 4 nodes]
```

---

### Round 4 — LLD Machine Coding (90 min mock)

**Pick ONE problem. Set 90-minute timer. Code in IDE. Must produce compiling, running code.**

```
Problem A — Design a Task Scheduler (closest to your WorkFlowFwk experience)
  Requirements:
  - Tasks have: id, name, priority (HIGH/MEDIUM/LOW), status, assigned_to, due_date
  - TaskService: createTask, assignTask, completeTask, escalateOverdueTasks
  - Priority queue: HIGH tasks always processed before MEDIUM before LOW
  - Escalation: tasks overdue by > 24hrs → reassign to supervisor
  - Thread-safe: multiple threads creating and completing tasks concurrently
  - Unit tests for: assignment, priority ordering, escalation logic

  GSTN hook: This is exactly WorkFlowFwk's task lifecycle — describe after you finish

Problem B — Design a Double-Entry Ledger (your strongest)
  Requirements:
  - Accounts: DEMAND, PAYMENT, DISPUTE, REFUND
  - Operations: createDebit(accountId, amount, description), createCredit(accountId, amount, description)
  - Balance: getBalance(accountId) = sum(debits) - sum(credits)
  - Transfer: transfer(fromAccountId, toAccountId, amount) — atomic, both or neither
  - Status: getStatus(accountId) → PENDING (balance > 0) / SETTLED (= 0) / REFUND_DUE (< 0)
  - Audit trail: every operation logged with timestamp, user, reason
  - Tests: all 3 status transitions, concurrent transfer atomicity

  GSTN hook: This IS LedgerUtilFwk — you built the real version

Problem C — Design a Cache with TTL and LRU Eviction
  Requirements:
  - Cache<K,V>: put(key, value, ttlMillis), get(key), delete(key)
  - LRU eviction: when capacity exceeded, evict least recently used
  - TTL eviction: expired entries return null and are cleaned up
  - Thread-safe: concurrent reads and writes
  - Stats: hitRate(), missRate(), evictionCount()
  - Tests: LRU eviction order, TTL expiry, concurrent access

Problem D — Design a Notification Service
  Requirements:
  - Channels: EMAIL, SMS, PUSH (each has different rate limits)
  - NotificationService.send(userId, message, channels)
  - Rate limiting: max 10 emails/hour, 5 SMS/hour, 50 push/hour per user
  - Retry: if delivery fails, retry 3 times with exponential backoff
  - Template: messages have a template with variable substitution
  - Observer: on case status change → notify relevant parties
  - Tests: rate limit enforcement, retry logic, template substitution
```

---

### Round 5 — HLD System Design (45 min mock)

**For each problem: 5 min requirements, 5 min capacity, 10 min design, 10 min deep dive, 10 min trade-offs, 5 min wrap-up.**

```
Problem A — Design GSTN Case Management System (USE YOUR REAL EXPERIENCE)
  Scale: 140M taxpayers, 2M new cases/year, 28 states, peak = GST filing deadlines
  Must cover:
  - How do you partition the data? (answer: by stateCd — your DbContextHolder)
  - How do you handle concurrent order issuance? (answer: @Version + Redis lock)
  - How do you keep the system available during deadline spikes? (answer: cache + circuit breaker)
  - How does the workflow engine work? (answer: WorkFlowFwk task lifecycle)
  - How do you audit every API call? (answer: GstAopFwk @BoApiAudit → Kafka)
  This is your home ground. You should nail this.

Problem B — Design a Payment Ledger System (maps to your LedgerUtilFwk)
  Scale: 10M transactions/day, each transaction = debit one account, credit another
  Must cover:
  - Data model: double-entry bookkeeping, immutable entries
  - Consistency: how do you ensure debit + credit are atomic?
  - Scale: how do you partition the ledger? by accountId? by date?
  - Idempotency: same transaction retried twice must not double-charge
  - Reporting: how do you run balance queries without locking the transaction table?
  - Audit: every change logged with who, what, when

Problem C — Design a Real-Time Notification System
  Scale: 10M users, 100M notifications/day, SMS + Email + Push
  Must cover:
  - How do you fan-out one event to multiple users? (topic-based vs user-preference filtering)
  - Rate limiting per user per channel
  - Delivery guarantee: at-least-once with deduplication key
  - Retry with exponential backoff + DLQ
  - Template service: parameterized message templates by event type
  - How do you handle a sudden spike (e.g., all users notified at once)?

Problem D — Design a Distributed Rate Limiter
  Scale: 50M API calls/min, 100+ microservices, per-user + per-API limits
  Must cover:
  - Algorithm choice: token bucket vs sliding window (and why)
  - Distributed: rate limiter state shared across 10 API servers
  - Storage: Redis (why? atomicity with Lua, TTL, in-memory speed)
  - Edge cases: Redis down → fail open or fail closed? (discuss trade-off)
  - Config: limits configurable per API, per tier (free/pro/enterprise)

Problem E — Design Google Drive / File Storage
  Scale: 1B users, 10 exabytes of data, files up to 5GB
  Must cover:
  - Chunking: split large files into 4MB chunks, upload parallel
  - Deduplication: hash-based chunk deduplication (content-addressable storage)
  - Metadata DB: files, folders, versions, sharing permissions (SQL or NoSQL?)
  - Sync: how does the desktop client detect and sync changes?
  - CDN: how are frequently accessed files served fast globally?
  - Versioning: how do you support file version history without full copies?
```

---

### Round 6 — Behavioral (30 min mock)

**For each: speak your answer out loud. Time: 90 seconds to 2 minutes. Record yourself once.**

```
B1.  Tell me about yourself. (2 min — use Section 15.4 script)

B2.  What is the most technically complex problem you have solved?
     Walk me through it — problem, constraints, your solution, result.
     [Use Story 1: 12-scenario decision matrix]

B3.  Tell me about a time you disagreed with a technical decision.
     What happened, what did you do, and what was the outcome?
     [Use Story 4: shared mutable state design disagreement]

B4.  Describe a situation where you had to deliver something under a very tight deadline.
     What did you prioritize? What did you cut?
     [Use Story 3: simultaneous-combine deadline delivery]

B5.  Tell me about a time you improved the performance of a system.
     What was the problem? What did you do? What was the result?
     [Use Story 2: two-tier caching, 60-80% DB load reduction]

B6.  Tell me about a time you took ownership of something outside your defined role.
     [Use Story 5: documentation of appeal order flow for team onboarding]

B7.  Tell me about a time you had to learn a new technology or concept quickly.
     How did you approach it?
     [Use Story 6: learning HBase by reading framework source code]

B8.  Describe a production incident you were involved in.
     What went wrong, what was your role, what did you do?
     [Use Story from Section 9: Transfer-Out calculation bug for APL03 cases]

B9.  Why are you leaving your current company?
     [Use Section 15.6 answer — growth, product scale, tech stack]

B10. Where do you want to be in 5 years?
     [Use Section 15.7 answer — senior engineer, distributed systems, technical depth]

B11. Why do you want to join [specific company]?
     [Research company blog, pick one specific tech problem they solve, tie to your interest]

B12. What is your biggest weakness? Give an example of how you've worked on it.
     [Use Section 15.5 weakness answer — over-engineering + how you fixed it]
```

---

### Round 7 — DSA Coding (45 min mock)

**These are the actual patterns asked at target companies for SDE-2/3 level.**

```
WEEK 1 — Do these 5 (warm up, build pattern recognition):
  1. Two Sum (LeetCode 1) — HashMap, O(n)
  2. Best Time to Buy and Sell Stock (LC 121) — one pass, track min so far
  3. Valid Parentheses (LC 20) — Stack
  4. Merge Intervals (LC 56) — sort + merge
  5. Reverse Linked List (LC 206) — iterative and recursive

WEEK 2 — Do these 5 (core patterns):
  6. Longest Substring Without Repeating Characters (LC 3) — sliding window + set
  7. Search in Rotated Sorted Array (LC 33) — binary search, identify sorted half
  8. Number of Islands (LC 200) — DFS/BFS on grid
  9. House Robber (LC 198) — 1D DP
  10. Kth Largest Element (LC 215) — min-heap of size k

WEEK 3 — Do these 5 (medium-hard):
  11. Product of Array Except Self (LC 238) — prefix + suffix product, no division
  12. Coin Change (LC 322) — unbounded knapsack DP
  13. LRU Cache (LC 146) — LinkedHashMap or HashMap + doubly-linked list
  14. Subsets II (LC 90) — backtracking with duplicate skip
  15. Course Schedule (LC 207) — topological sort, cycle detection

WEEK 4 — Do these 5 (company favorites):
  16. Trapping Rain Water (LC 42) — two pointers
  17. Word Break (LC 139) — DP or BFS
  18. Top K Frequent Elements (LC 347) — heap or bucket sort
  19. Lowest Common Ancestor of BST (LC 235) — BST property
  20. Spiral Matrix (LC 54) — boundary simulation

WEEK 5-8 — 3 problems per day (maintain momentum):
  Priority: NeetCode 150 roadmap — Arrays, Two Pointers, Sliding Window, Binary Search,
            Trees, Graphs, DP, Heap, Backtracking — in that order
  
  Time yourself: Easy ≤ 10 min, Medium ≤ 20 min, Hard ≤ 35 min
  If stuck after 20 min on Medium: look at hint, code it, understand it, redo from scratch 2 days later
```

---

## 17.5 Company-Specific Interview Patterns

> Read 1-2 engineering blog posts per company BEFORE the interview.
> Mentioning their blog in the "why us" answer = immediately noticed.

### Flipkart
```
Focus: Large-scale search, supply chain, payment, catalog
Strong on: HLD (design Instagram / Uber / WhatsApp), Java concurrency, Kafka
Blog to read: "Flik — Flipkart's in-house stream processing" (search tech.flipkart.com)
Tip: They like GSTN-scale numbers. Emphasize 140M taxpayers, 28-state sharding.
Typical rounds: 1 DSA + 1 LLD + 1 HLD + 1 Managerial
```

### Razorpay
```
Focus: Payments, ledger, idempotency, financial consistency
Strong on: Double-entry bookkeeping, XA vs Saga, idempotency keys, Kafka exactly-once
Blog to read: "Razorpay's Ledger System" on engineering.razorpay.com
Tip: Your LedgerUtilFwk and XA Transactions ARE their core problems. This is your best fit.
Typical rounds: 1 DSA + 1 LLD (design payment ledger) + 1 HLD + 1 Behavioral
```

### PhonePe
```
Focus: UPI at scale, digital wallet, merchant payments, real-time
Strong on: Distributed transactions, Redis, Kafka, concurrent requests
Blog to read: "Building PhonePe's payment switch" on tech.phonepe.com
Tip: Rate limiting, distributed lock, idempotency — these are daily problems there.
Typical rounds: 1 DSA + 1 LLD + 1 System Design + 1 Bar Raiser
```

### Meesho
```
Focus: Social commerce, catalog, orders, supply chain
Strong on: LLD, Spring Boot internals, basic HLD
Blog to read: "Meesho's catalog search" on tech.meesho.com
Tip: Less intense on DDIA-level depth. Strong code quality and OOP expected.
Typical rounds: 1 DSA + 1 LLD (machine coding) + 1 HLD + 1 Behavioral
```

### Zerodha
```
Focus: Trading platform, real-time data, WebSocket, financial accuracy
Strong on: Low-latency, concurrency, Java performance, correctness
Blog to read: zerodha.tech — Kite API, Kite Connect internals
Tip: Smaller team, expect to discuss code quality and operational simplicity.
Typical rounds: 1 take-home + 1 technical deep dive + 1 culture fit
```

### Goldman Sachs / JP Morgan (SDE-2/SDE-3)
```
Focus: Financial systems, correctness, security, compliance, Java internals
Strong on: Java deep dive (JVM, GC, concurrency), design patterns, financial domain
Blog to read: developer.gs.com/blog
Tip: They value correctness > cleverness. Your GSTN financial work is perfect background.
Typical rounds: 1 DSA + 1 Java deep dive + 1 LLD + 1 HLD + 1 Design (60 min)
```

### Zomato / Swiggy
```
Focus: Hyperlocal, real-time delivery, restaurant search, ETA
Strong on: Geospatial queries, real-time streaming, HLD for delivery systems
Blog to read: engineering.zomato.com, bytes.swiggy.com
Tip: System design favors delivery ETA, driver matching, surge pricing.
Typical rounds: 1 DSA + 1 LLD + 1 HLD + 1 Hiring Manager
```

---

## 17.6 Interview Day Checklist

### One Week Before
```
[ ] Read 1-2 engineering blog posts from the target company
[ ] Do one full HLD mock (45 min, speak out loud, draw on paper)
[ ] Do one full LLD mock (90 min, code it end to end)
[ ] Do 5 LeetCode mediums on random topics — maintain sharpness
[ ] Prepare "why this company" answer with specific company reference
[ ] Rehearse "tell me about yourself" (2 min, timed)
[ ] Review your 6 STAR stories — speak each one out loud
[ ] Re-read Sections 2, 9, 13.12 (Quick Self-Test) of this document
```

### Night Before
```
[ ] Read Section 13.12 Quick Self-Test — if you can answer all, you are ready
[ ] Review your STAR stories one more time
[ ] Check: water, quiet room, stable internet (for virtual), IDE open, paper and pen ready
[ ] Sleep 7+ hours — tired brain = slow pattern recognition
```

### Interview Day (Virtual)
```
[ ] Log in 5 min early — test audio/video/screen share
[ ] Pen and paper on desk — draw diagrams while explaining (visible to interviewer)
[ ] For coding: IDE open with a blank Java file, input/output methods ready
[ ] Browser tab: LeetCode or your preferred coding environment as backup
[ ] Read the problem statement twice before saying anything
[ ] Ask clarifying questions BEFORE writing code (interviewer is evaluating this)
[ ] Think out loud — silence is bad, even "let me think..." is better than silence
[ ] If stuck: state what you know, state what you're trying, ask for a hint — don't go silent
```

### After the Interview
```
[ ] Write down every question asked within 30 minutes (memory fades fast)
[ ] Note: what you answered well, what you stumbled on
[ ] Add any gaps to a "fix list" and study those before next interview
[ ] If company uses same rounds for multiple interviews: the prep carries over
```

---

## 17.7 90-Day Resource Usage Calendar

```
WEEK 1-2 (Java + Spring):
  Read:    Effective Java Items 1-17, 66-84
  Watch:   Defog Tech Java Memory Model, Jacob Jenkov ThreadLocal video
  Code:    LRU cache, AOP timing annotation, Transaction propagation experiment
  DSA:     LeetCode 1, 121, 20, 56, 206 (5 problems)

WEEK 3-4 (Design Patterns + LLD):
  Read:    Head First Design Patterns Ch 1-4
  Watch:   Code With Mosh Design Patterns, Udit Agarwal LLD playlist
  Code:    Parking Lot, Library System, Elevator (90 min each)
  DSA:     LC 3, 33, 200, 198, 215 (5 problems)

WEEK 5-6 (Database + JPA):
  Read:    vladmihalcea.com — N+1, MVCC, locking (top 5 posts)
  Watch:   Hussein Nasser Postgres Internals
  Code:    N+1 diagnosis + fix, Window function practice, Index tuning
  DSA:     LC 238, 322, 146, 90, 207 (5 problems)

WEEK 7 (Redis + Kafka):
  Read:    Redis commands reference (redis.io/commands)
  Watch:   Hussein Nasser Kafka Internals, Gaurav Sen Message Queues
  Code:    Rate limiter, distributed lock, leaderboard (Redis); manual ack consumer, DLQ (Kafka)
  DSA:     LC 42, 139, 347, 235, 54 (5 problems)
  
WEEK 8 (HLD Building Blocks):
  Read:    System Design Primer intro + caching + messaging sections
  Watch:   ByteByteGo System Design Fundamentals playlist (1 video/day)
  Practice: Draw architecture diagrams for: URL shortener, Rate Limiter, Notification Service
  DSA:     NeetCode 150 — Trees section (5 problems/day)

WEEK 9 (Full System Designs):
  Read:    Alex Xu System Design Interview Vol 1 — Ch 1 (framework) + 3 chapters of choice
  Watch:   Exponent rate limiter mock, TechDummies WhatsApp design
  Practice: Full 45-min mocks: GSTN case mgmt, Razorpay ledger, notification system
  DSA:     NeetCode 150 — Graphs section (5 problems/day)

WEEK 10 (DDIA):
  Read:    DDIA Ch 5 (Replication), Ch 7 (Transactions), Ch 9 (Consistency) — these 3 chapters
  Watch:   Jordan has no life DDIA series — Ch 5, 7, 9 episodes
  Review:  Section 16 of this document — test yourself on each concept
  DSA:     NeetCode 150 — DP section (5 problems/day)

WEEK 11 (Mock Interviews):
  Do:      2 full LLD mocks (workat.tech or with a friend)
  Do:      2 full HLD mocks (interviewing.io or pramp.com)
  Do:      1 full behavioral mock (record yourself, watch it back)
  DSA:     Mixed review — 3 problems/day from weak areas

WEEK 12 (Apply + Polish):
  Do:      Resume final pass — run through Jobscan against each JD
  Read:    1 engineering blog post per target company
  Prepare: "Why this company" answer for each target
  Apply:   Referrals first, then direct apply through company career pages
```

---

## 17.8 Referral Strategy — How to Get Into Target Companies

```
Why referrals matter: referred candidates get 2-4x higher callback rate at most product companies
Referred candidates often skip first screening call

Step 1 — Find people at target companies:
  LinkedIn: search "[Company] [Java/Backend Engineer]"
  Filter: 2nd degree connections (mutual connections are warm outreach)
  Alumni: GSTN → check if ex-colleagues moved to target companies
  College alumni: search LinkedIn for your college + target company

Step 2 — Craft the outreach message (keep it short):
  "Hi [Name], I'm a Java backend engineer at GSTN (India's GST platform, 140M users).
   I'm exploring SDE-2/SDE-3 opportunities at [Company] and would love a referral if
   you feel my background is a fit. I have 5.6 years in distributed systems, Kafka, Redis,
   and Spring Boot. Happy to share my resume. No pressure at all if you don't know me well
   enough — completely understand."

Step 3 — Make it easy to refer:
  Attach your resume in the first message
  Include your LinkedIn profile link
  2-3 bullet points of your strongest GSTN work (use ATS-safe bullets from Section 11)

Step 4 — Follow up once after 5 days if no reply, then move on

Target companies with strong referral programs:
  Flipkart, Razorpay, PhonePe, Meesho — all have internal referral bonuses
  → the person referring you is motivated (cash incentive)
```

---

## 17.9 The Final "Am I Ready?" Test

> Do this test 2 days before your first interview.
> If you can score 80%+, you are ready to interview.

```
JAVA (10 questions — 1 min each):
  [ ] Explain HashMap treeification in one sentence
  [ ] What does volatile guarantee that synchronized does not?
  [ ] When does CompletableFuture use ForkJoinPool vs a provided Executor?
  [ ] Name the 4 functional interfaces in Java 8 with one example each
  [ ] What is the difference between Runnable and Callable?
  [ ] What is G1GC? How does it differ from CMS?
  [ ] What is the happens-before relationship in Java Memory Model?
  [ ] How does ConcurrentHashMap achieve thread safety in Java 8?
  [ ] What is a WeakReference? When would you use it?
  [ ] What is the double-checked locking pattern for Singleton? Write it from memory.

SPRING (10 questions — 1 min each):
  [ ] How does Spring Boot auto-configuration work? What file does it read?
  [ ] What is the CGLIB proxy? When does Spring use JDK dynamic proxy instead?
  [ ] What happens when you call a @Transactional method from within the same class?
  [ ] What is @ConditionalOnMissingBean? Give a real use case.
  [ ] What is BeanFactoryPostProcessor vs BeanPostProcessor?
  [ ] What does @Async do under the hood? What thread pool does it use?
  [ ] What is the difference between @RequestParam and @PathVariable?
  [ ] How does Spring Security filter chain work? What order do filters run?
  [ ] What is actuator? Name 4 endpoints and what each shows.
  [ ] What is Spring's @Transactional rollbackFor default behavior for checked exceptions?

DATABASE (10 questions — 1 min each):
  [ ] What is a phantom read? Which isolation level prevents it?
  [ ] Explain MVCC in one paragraph.
  [ ] What is write skew? Give an example.
  [ ] What is a covering index? When does it eliminate a table lookup?
  [ ] What is HikariCP? Name 3 pool settings you would tune.
  [ ] What is the N+1 problem? How do you fix it with JPQL?
  [ ] What is optimistic locking? What exception does it throw?
  [ ] When is a composite index (A,B,C) used for a query on column B alone?
  [ ] What is connection pool exhaustion? What metrics would alert you?
  [ ] What is WAL? Why does every serious database have one?

DISTRIBUTED SYSTEMS (10 questions — 1 min each):
  [ ] What is CAP theorem? Where does GSTN sit and why?
  [ ] What is a cache stampede? Name 3 ways to prevent it.
  [ ] How does Kafka ensure ordering within a partition?
  [ ] What is at-least-once vs exactly-once Kafka delivery?
  [ ] What is a distributed lock? How do you implement it with Redis?
  [ ] What is the Outbox pattern and why is it needed?
  [ ] What is consistent hashing? Why does it minimize key remapping?
  [ ] What is replication lag? What is the read-your-writes fix?
  [ ] What is linearizability? How is it different from serializability?
  [ ] What is the 2PC coordinator SPOF problem?

SYSTEM DESIGN — GSTN ANCHORS (5 questions — 3 min each):
  [ ] In one minute: how does GSTN route DB calls to the correct regional shard?
  [ ] In one minute: how does the AOP audit framework work end-to-end?
  [ ] In one minute: walk through the 12-scenario Subsequent Order matrix
  [ ] In one minute: how does the two-tier cache (JVM + Redis) work?
  [ ] In one minute: how does XA 2PC guarantee atomicity across 3 databases?
```

**Score yourself:**
- 90-100% → You are ready. Apply now.
- 75-89%  → 1 more week of targeted study on weak areas. You are close.
- 60-74%  → 2-3 weeks. Focus on the sections you missed most.
- Below 60% → Follow the 12-week plan from Section 13.11. Don't rush.

---

# Section 18 — Simulated SDE-2 Interview: Project Architecture + Feature Deep Dive

> This section is a full simulation of how an SDE-2 interviewer at a product company
> (Razorpay, Flipkart, PhonePe, Goldman Sachs) will probe your GSTN project.
>
> For each question:
> - What the interviewer is ACTUALLY testing (not obvious from the question)
> - The vocabulary and framing to use (generic software engineering language)
> - The model answer at SDE-2 level
> - The follow-up question that comes next
> - What a WEAK answer looks like (so you avoid it)
>
> Read this section like a script. Practice speaking each answer out loud.

---

## 18.1 The Interview Opening — How They Set the Stage

**Interviewer:** "So, tell me about the most complex feature you've worked on at GSTN.
Give me a 3-minute walkthrough — what was the problem, what was your role,
and what were the key technical decisions you made."

---

### What the Interviewer Is Testing
- Can you explain complex work to someone who has zero domain knowledge?
- Do you distinguish between YOUR decisions vs team decisions?
- Do you talk in terms of trade-offs, or just describe what you built?
- Is your vocabulary software engineering vocabulary, or domain jargon?

---

### The Vocabulary Upgrade Table — Before You Answer Anything

| If You're About to Say... | Say This Instead |
|---|---|
| "DRC07 demand" | "the original tax demand — think of it as a financial liability record" |
| "APL01, APL03, APL04" | "taxpayer appeal, department appeal, adjudication order — the three actors in the dispute workflow" |
| "DCR entries" | "double-entry ledger transactions — a debit when liability is created, a credit when it is settled" |
| "simultaneous combine order" | "concurrent multi-party resolution — two independent appeal threads converging on a single authoritative outcome" |
| "subsequent order" | "higher appellate court override — a superseding decision that cascades financial corrections down the chain" |
| "stateCd routing" | "tenant-based database routing — each of 28 state jurisdictions has its own isolated data partition" |
| "CaseMgmtFwk" | "a case lifecycle management framework — plugin-based, with Strategy + Factory patterns for 20+ case types" |
| "LedgerUtilFwk" | "a double-entry financial ledger engine — immutable audit trail with balance projection" |
| "WorkFlowFwk" | "a workflow orchestration engine — manages task assignment, escalation, and SLA enforcement" |
| "GstAopFwk" | "an AOP-based API audit framework — cross-cutting concern for compliance logging" |
| "DistCacheFwk" | "a distributed caching layer — Redis-backed, 40+ data types, TTL-based eviction" |
| "140M taxpayers" | "140 million registered entities — roughly the scale of the entire population of Germany or Mexico" |
| "28 states" | "28 independent tenants — each with physical database isolation, jurisdiction-specific business rules" |

---

### Model Opening Answer (Speak This Out Loud — Practice Until Natural)

> "The most technically complex feature I built was the **appellate order financial
> processing engine** — a system that handles the financial consequences of court-ordered
> outcomes in a tax dispute workflow.
>
> Here is the context: when a taxpayer disputes a tax demand, it creates a multi-party
> appeal process. A taxpayer can file their own appeal, the tax department can file a
> counter-appeal, and eventually an adjudicating authority issues a binding order.
> That order can modify, confirm, or reject the original demand — and each combination
> produces different financial obligations.
>
> My role was to design and own the calculation engine end-to-end — from the data model
> to the service layer to the API. The core complexity was a **12-scenario decision matrix**:
> the original demand outcome crossed with the appellate order outcome produces 12 distinct
> financial states, each requiring different ledger operations. Nested if-else would have
> been unmaintainable and untestable. I modelled it as a **rule engine** — each scenario is
> an explicit, named rule with a condition predicate and an action. Rules are independently
> unit-testable, and adding a new scenario requires adding one rule without touching existing code.
>
> Three technical decisions I'm proud of: first, using **XA distributed transactions** across
> three databases — case management, financial ledger, workflow — to guarantee atomicity on
> every order issuance. Second, **optimistic locking with a version field** on the case entity
> plus a **Redis distributed lock** at the application layer to prevent two concurrent officers
> from issuing orders on the same case. Third, a **Kafka-based async audit pipeline** using
> AOP interception, so the main request thread is never blocked by compliance logging."

---

## 18.2 Architecture Questions — The Interviewer Drills In

### Question 1

**Interviewer:** "You mentioned three databases. Walk me through why you have three
separate databases. Why not one?"

**What they're testing:** Do you understand separation of concerns at the data layer?
Can you articulate the trade-off between schema isolation vs join complexity?

**Weak answer to avoid:**
> "That's just how it was designed when I joined. We had separate DBs for each module."
*(Passes ownership to history. Zero credit.)*

**Model Answer:**

> "The three databases reflect three distinct bounded contexts with different
> transactional patterns and ownership.
>
> The **case management database** holds the lifecycle state of disputes — who filed what,
> what stage it is in, task assignments, hearing schedules. It is write-heavy during
> initiation and read-heavy during case resolution. The schema is normalized and heavily
> indexed on case identifiers and jurisdiction codes.
>
> The **financial ledger database** is append-only. Every debit and credit entry is
> immutable — we never UPDATE a ledger row, only INSERT. This is the event sourcing
> pattern: the account balance is a projection of all entries, not a stored value.
> Keeping it separate means we can apply different durability guarantees — synchronous
> replication here, whereas case data can tolerate slightly async replication for reads.
>
> The **workflow database** tracks task state — what is assigned to whom, what is pending,
> what is overdue. This has the most frequent writes during peak periods because every
> action on a case creates or updates a task.
>
> If these were in one schema, a slow query in case management could hold locks that
> block ledger writes — which is unacceptable for financial operations. Schema isolation
> also means each team can evolve their schema independently without a migration risk
> to the others. The trade-off is that you lose cross-database joins — we handle that
> by denormalizing a minimal set of identifiers across schemas and using application-level
> aggregation for queries that span contexts."

**Follow-up:** "You said the ledger is append-only. How do you query the current balance
then? Doesn't that get expensive?"

**Model Answer:**

> "Balance is calculated as a projection: `SELECT SUM(amount) FROM entries WHERE
> account_id = ? AND entry_type = 'DEBIT'` minus the same for CREDIT. With proper
> indexing on (account_id, entry_type), this is fast for accounts with a bounded
> number of entries.
>
> For accounts that accumulate entries over years — like a long-running dispute — we
> maintain a **snapshot balance** that is periodically materialized and stored. New
> balance = snapshot + sum of entries since snapshot timestamp. This is the same
> pattern used by event sourcing systems to avoid full log replay on every read.
>
> The deeper reason to prefer append-only over UPDATE is auditability. In a government
> tax system, every change to a financial record must have an immutable trail. If we
> allowed UPDATEs, a corrupt or erroneous update could silently change financial history.
> With append-only, the audit trail IS the data — there is nothing to reconstruct."

---

### Question 2

**Interviewer:** "You mentioned optimistic locking AND a Redis distributed lock.
Why do you need both? Isn't one enough?"

**What they're testing:** This is a classic defense question. They want to see if you
understand the failure modes of each mechanism independently.

**Weak answer to avoid:**
> "We added Redis lock as an extra safety layer just to be sure."
*(No understanding of why each mechanism is needed.)*

**Model Answer:**

> "They protect against different failure modes, and neither alone is sufficient.
>
> **The optimistic lock** (a `@Version` field on the case entity, enforced by JPA)
> protects against **intra-database concurrent writes**. When two transactions both
> read the case at version 5 and both try to commit, the first commit sets it to
> version 6. The second commit runs `UPDATE case SET ... WHERE version = 5` — finds
> zero rows — and throws `OptimisticLockException`. This is reliable but it acts
> **at the database commit boundary** — meaning both requests have already done all
> their work: validation, calculation, ledger preparation — before one of them fails.
> That wasted work must be retried.
>
> **The Redis distributed lock** protects at the **application entry boundary**.
> The moment a request enters the order issuance flow, it attempts
> `SET lock:case:{caseId} {requestId} NX PX 30000`. Only one request across all
> API server instances holds this lock. The second request sees the lock is taken and
> fails fast — before doing any work, before any DB round trips.
>
> The Redis lock is a **performance gate** — it prevents wasteful parallel execution.
> The optimistic lock is the **correctness safety net** — it ensures that even if the
> Redis lock fails (Redis down, TTL expires early, network glitch), the database level
> still enforces single-write. Defense in depth for a financially critical operation."

**Follow-up:** "What happens if the process holding the Redis lock crashes after
acquiring it but before releasing it?"

**Model Answer:**

> "The lock has a TTL — 30 seconds in our case — set atomically with the acquisition
> using `SET key value NX PX 30000`. If the process crashes, the lock expires
> automatically after 30 seconds. No manual cleanup needed.
>
> The risk is: 30 seconds may be longer than needed, and during that window, no other
> request can issue an order on that case. We tuned TTL to be 2x the 99th percentile
> latency of the issuance flow, so a legitimate request will always complete well
> within TTL, while a crashed process releases within a bounded time window.
>
> The more subtle risk is **lock extension**: what if the process is slow (GC pause,
> network delay) and its work takes longer than TTL? The lock expires while it's still
> working, a second process acquires the lock, and now two processes are in the issuance
> flow simultaneously — the Redis lock's protection is lost. This is the core of the
> Redlock controversy. For our use case, we mitigate it by keeping the locked section
> as short as possible (only the state validation and initial DB write, not the full
> flow), and relying on the optimistic lock as the backstop for the rare case where
> TTL is violated."

---

### Question 3

**Interviewer:** "You used XA transactions. Walk me through exactly how a 2-phase
commit works in your system. What is the coordinator? What happens if it crashes?"

**What they're testing:** SDE-2 level understanding of distributed transactions,
not just "I used Atomikos." They want to know if you understand the protocol.

**Model Answer:**

> "In our system, **Atomikos** is the XA transaction manager — the coordinator.
> The three participants are the three JDBC datasources: case DB, ledger DB, workflow DB.
> Each datasource implements the `XAResource` interface, which exposes `prepare()`,
> `commit()`, and `rollback()` methods.
>
> When our service code calls `@Transactional` (with XA), the flow is:
>
> **Phase 1 — Prepare:**
> Atomikos calls `prepare()` on each XAResource. Each database writes a prepare record
> to its own Write-Ahead Log — it is saying: 'I have the resources locked, I can commit,
> but I am waiting for the coordinator's decision.' If any resource votes 'no'
> (constraint violation, deadlock, out of space), Atomikos sends `rollback()` to all.
>
> **Phase 2 — Commit:**
> If all three voted 'yes', Atomikos writes a commit record to its own durable log,
> then sends `commit()` to each resource. Each DB applies the changes and releases locks.
>
> **Coordinator crash scenario:**
> If Atomikos crashes after Phase 1 but before Phase 2, all three databases are in an
> 'in-doubt' state — they have prepared but not committed. They hold locks and cannot
> proceed unilaterally. This is the **coordinator single point of failure** problem.
> When Atomikos restarts, it reads its durable log: if it had written 'commit' before
> crashing, it re-sends commit to all participants. If the log shows 'prepared' but no
> 'commit', it sends rollback.
>
> The practical implication: during the window between Phase 1 and coordinator recovery,
> those three DB rows are locked. For our use case — order issuance is a low-frequency,
> high-stakes operation — we accepted this risk. We would NOT use XA for a
> high-throughput path like reading case lists. XA is reserved for the write path
> where atomicity is non-negotiable."

---

### Question 4

**Interviewer:** "You said you routed every request to a specific database based on
a state code. How does that work architecturally? Walk me through the code path."

**What they're testing:** Do you understand Spring's datasource abstraction?
Do you understand ThreadLocal scoping? Can you explain it clearly?

**Model Answer:**

> "The pattern is called **dynamic datasource routing** using Spring's
> `AbstractRoutingDataSource`.
>
> Here is the flow:
>
> 1. Every incoming request carries a `stateCd` — a two-character jurisdiction code
>    identifying which of the 28 state partitions owns this data.
>
> 2. Before any database call, we resolve the state code to a region key — for example,
>    Maharashtra (state 27) maps to region R2. We call:
>    `DbContextHolder.setDbType(DbType.R2)` which stores R2 in a `ThreadLocal`.
>    ThreadLocal is per-thread storage — the value is scoped to the current request
>    thread and invisible to all other threads. Zero synchronization needed.
>
> 3. Our `RoutingDataSource` extends `AbstractRoutingDataSource` and overrides one method:
>    `determineCurrentLookupKey()` — which simply returns `DbContextHolder.getDbType()`.
>    Spring's datasource routing calls this method every time a connection is needed and
>    selects the matching physical datasource from a pre-configured map.
>
> 4. The entire DAO layer is completely unaware of this. Every JPA repository call,
>    every JDBC template call — they all just ask Spring for a connection, and the
>    routing layer transparently hands them the correct regional datasource.
>
> 5. After the request completes — in a `finally` block — we call
>    `DbContextHolder.clearDbType()`. This is critical: our threads come from a pool.
>    If we don't clean up, the next request reusing this thread inherits the previous
>    request's region key and hits the wrong database. That is a silent data corruption
>    bug that is very hard to debug.
>
> The pattern is essentially the same as what multi-tenant SaaS products use — except
> instead of tenant ID, we use jurisdiction code."

---

### Question 5

**Interviewer:** "Tell me about your caching strategy. How did you decide what to cache,
where to cache it, and for how long?"

**What they're testing:** Cache-aside vs write-through, TTL reasoning, two-tier thinking,
and whether you understand staleness trade-offs.

**Model Answer:**

> "We used a **two-tier caching strategy** — JVM in-memory cache for reference data,
> Redis for session and transactional data.
>
> **Tier 1 — JVM in-memory cache (LocalCacheFwk):**
> This holds reference/master data: case type definitions, status code mappings, district
> masters, filing deadline calendars, document type lists — over 100 distinct data types.
> These are loaded at application startup via `@PostConstruct` and held in `ConcurrentHashMap`
> in the JVM heap. Access is nanosecond — no network round trip.
>
> Decision criteria for JVM cache:
> - Change frequency: once a day at most (nightly batch updates)
> - Size: bounded — ~50MB estimated total across all types
> - Consistency tolerance: slightly stale is fine — if a case type name changes, users see
>   the old name for a few hours. That is acceptable for reference data.
>
> **Tier 2 — Redis distributed cache (DistCacheFwk):**
> This holds data that changes more frequently or needs to be shared across
> multiple application instances: jurisdiction-to-officer maps, session data,
> rate limiting counters, distributed locks.
>
> Decision criteria for Redis:
> - Must be consistent across all API server instances (JVM cache is per-instance)
> - TTL-based eviction: jurisdiction maps refresh every few hours, sessions expire on logout
>
> **What we explicitly did NOT cache:**
> Case status and ledger balances — these change with every officer action. Caching them
> risks showing a stale order status. Serving stale financial data in a legal system is
> a compliance violation. The rule: cache data whose staleness has bounded business impact.
>
> **Cache stampede prevention:**
> During GST filing deadlines, traffic spikes 10-20x. If a Redis key expires at peak,
> hundreds of threads simultaneously miss and hit the database. We mitigate this with
> a mutex lock on cache refresh: the first thread to miss acquires `SETNX refresh_lock:key`,
> fetches from DB, populates cache, releases lock. All other threads that missed wait
> briefly and then read from the now-warm cache."

---

### Question 6

**Interviewer:** "Your system has a Kafka-based audit pipeline. Walk me through the
full flow — from an API call arriving, to the audit event being stored."

**What they're testing:** AOP proxy understanding, Kafka producer/consumer flow, async
decoupling, and awareness of failure modes (the dual-write problem).

**Model Answer:**

> "The audit pipeline uses **aspect-oriented programming** to intercept any controller
> method annotated with `@BoApiAudit` — without the method itself knowing it is being audited.
>
> Here is the flow:
>
> 1. **Request arrives** at the Spring controller. The controller method is not called
>    directly — instead, a CGLIB proxy intercepts the call because `BoApiAuditAspect`
>    uses `@Around` advice on `@BoApiAudit` annotations.
>
> 2. **Audit config lookup:** The aspect checks a database-backed config table: 'For this
>    specific API endpoint, which fields should be logged? Is auditing even enabled for
>    this API?' This makes audit configuration **runtime-toggleable** — we can enable or
>    disable logging per API without redeployment. The config is cached in Redis so this
>    lookup is fast.
>
> 3. **Method execution:** The aspect calls `proceedingJoinPoint.proceed()` — the actual
>    controller method runs. The aspect captures: the request payload, the response payload,
>    the response status, and the end-to-end latency.
>
> 4. **Kafka publish (async):** The audit event is serialized to **Protobuf** —
>    not JSON — and published to a Kafka topic asynchronously. The main request thread
>    returns the response to the client immediately. The Kafka publish does not block it.
>
> 5. **Kafka consumer:** A separate microservice consumes from the audit topic and persists
>    the events to the audit database.
>
> **The failure mode I am aware of:**
> If the controller method's DB transaction commits but the Kafka publish fails, the
> audit event is silently lost — this is the **dual-write problem**. In our current
> implementation, we accept this risk for non-financial audit events. For a higher
> guarantee, the correct fix is the **Outbox pattern**: write the audit event to an
> outbox table in the same transaction as the business data, then a separate poller
> publishes from the outbox to Kafka and deletes on success. I've identified this as
> a technical debt item."

**Follow-up:** "Why Protobuf instead of JSON?"

**Model Answer:**

> "Three reasons:
>
> 1. **Size:** Protobuf binary encoding does not include field names — fields are
>    identified by compact integer tags in the schema. A typical audit event that would
>    be 500 bytes as JSON is 80-100 bytes as Protobuf. At millions of audit events per
>    day, this reduces Kafka storage and network bandwidth significantly.
>
> 2. **Schema enforcement:** The `.proto` file is the contract. If a producer tries to
>    publish an event missing a required field, it fails at serialization time — not at
>    consumer processing time. JSON has no such guarantee.
>
> 3. **Schema evolution with backward compatibility:** Protobuf fields are identified
>    by number tags, not names. Adding a new optional field with a new tag number is
>    fully backward compatible — old consumers ignore unknown tags, new consumers
>    handle absent fields with defaults. As long as we never reuse a tag number, old
>    and new versions of the schema can coexist across a rolling deployment."

---

### Question 7

**Interviewer:** "Tell me about a design decision you made that you would change today
if you were building this from scratch."

**What they're testing:** Engineering maturity. The best SDE-2 candidates see gaps in
their own work. This is NOT a trap — it is an opportunity to show depth.

**Weak answer to avoid:**
> "I think the design is pretty solid. Maybe I would add more unit tests."
*(Shows no critical thinking about architecture.)*

**Model Answer:**

> "Two things I would do differently.
>
> **First: replace XA transactions with the Saga pattern for most flows.**
> We chose XA 2-phase commit because it gives us strict atomicity across three
> databases. In practice, XA has two costs we underestimated. First, it holds database
> locks for the entire duration of the 2PC protocol — if the network is slow, all three
> databases have rows locked. Second, the coordinator (Atomikos) is a single point of
> failure during the commit window — if it crashes between Phase 1 and Phase 2, all
> three databases are in-doubt and blocked.
>
> For most of our flows, a **Saga with compensating transactions** would be sufficient.
> The case update is the first step; on failure, we reverse it. Only the financial ledger
> entry — the most critical correctness requirement — actually needs synchronous commitment.
> I would use a hybrid: synchronous 2PC for the ledger step alone, and async Saga with
> compensation for the case and workflow steps. This reduces the scope of locked rows
> dramatically.
>
> **Second: introduce the Outbox pattern for Kafka audit events.**
> Currently, if the controller DB transaction commits but the Kafka publish fails,
> the audit event is lost. In a legal compliance system, that is a silent gap. The
> Outbox pattern — writing the event to a DB table in the same transaction, then
> publishing separately — would give us exactly-once delivery semantics without
> requiring Kafka transactions. I did not implement this originally because it was
> not in the requirements, but now that I understand the failure mode, I would
> build it in from day one."

---

### Question 8

**Interviewer:** "Your system serves 140 million taxpayers across 28 states.
Walk me through how it handles a sudden spike — like a GST filing deadline
where everyone files in the last 30 minutes."

**What they're testing:** Traffic spike handling, caching, horizontal scaling,
circuit breakers, and whether you've actually thought about production load.

**Model Answer:**

> "Let me walk through each layer.
>
> **API layer — horizontal scaling:**
> Our microservices are stateless — all session state is in Redis. So we can
> add application instances horizontally behind a load balancer with no coordination.
> For deadline spikes, we pre-scale: based on historical traffic patterns, we provision
> 2x instances 30 minutes before the known deadline. Kubernetes HPA handles this with
> CPU-based autoscaling as a backstop.
>
> **Cache layer — deflect DB traffic:**
> The two-tier cache is the primary defense. Master data — case types, filing deadlines,
> jurisdiction maps — is in JVM memory. Every API call that reads reference data
> hits nanosecond JVM cache, not the database. During peak, this deflects 60-80% of
> what would otherwise be DB reads.
>
> **Database layer — the real bottleneck:**
> Writes are the challenge. Every case creation and status update is a write.
> Our database is sharded by state code — Maharashtra's filings only hit Maharashtra's
> shard. This means 28 shards absorb the load independently rather than concentrating
> it on one database.
> We also use **read replicas** for list queries — case search, dashboard — so the
> write primary only handles actual mutations.
>
> **Resilience — circuit breakers:**
> If the case DB shard for one state is overwhelmed, we do not want that failure to
> cascade to all states. Each shard has an independent circuit breaker. If State-X
> shard is throwing timeout errors, the breaker opens for that shard, returns a
> 'system busy, try again' response for State-X users, while all other states continue
> serving normally.
>
> **Kafka — async decoupling:**
> Post-submission notifications (confirmation SMS, email) go through Kafka. They do not
> block the submission API response. Even if the notification consumer is backlogged,
> taxpayers still get their submission confirmation immediately. The notification arrives
> a few minutes late — which is acceptable.
>
> **What I would add today:**
> A request queue in front of the case creation API. Under extreme load, accept the
> request, return a `202 Accepted` with a job ID, process asynchronously. Taxpayer
> polls for status. This is more user-friendly than a 503 under overload."

---

## 18.3 Feature-Level Questions — The Technical Drill

### Question 9

**Interviewer:** "You mentioned a 12-scenario decision matrix. How did you model it
in code? Why not just write nested if-else?"

**Model Answer:**

> "Nested if-else for 12 scenarios has three problems: it is hard to read, impossible to
> unit-test each scenario independently, and adding a 13th scenario requires modifying
> code that was already tested — violating the Open-Closed Principle.
>
> I modelled it as a **rule engine** using three constructs:
>
> ```java
> interface SubsequentOrderRule {
>     // Condition: does this rule apply to this combination of outcomes?
>     boolean matches(FirstAppealOutcome firstOutcome, SubsequentOutcome subOutcome);
>     // Action: execute the financial operations for this scenario
>     void execute(OrderContext context);
>     // Identity: readable name for logging and debugging
>     String name();
> }
> ```
>
> Each of the 12 scenarios is a separate class implementing this interface. For example:
>
> ```java
> class ConfirmThenRejectRule implements SubsequentOrderRule {
>     public boolean matches(FirstAppealOutcome f, SubsequentOutcome s) {
>         return f == CONFIRMED && s == REJECTED;
>     }
>     public void execute(OrderContext ctx) {
>         // reverse APL03 dispute from D1
>         // credit determined amount to D2
>         // transfer payment from D2 back to D1
>         // mark D2 status as SUBSEQUENT_REJECTED
>     }
>     public String name() { return "CONFIRM_THEN_REJECT"; }
> }
> ```
>
> The engine holds a list of all 12 rules. On execution:
> ```java
> rules.stream()
>      .filter(r -> r.matches(firstOutcome, subOutcome))
>      .findFirst()
>      .orElseThrow(() -> new UnhandledScenarioException(firstOutcome, subOutcome))
>      .execute(context);
> ```
>
> Benefits I experienced in practice:
> - Each rule has its own unit test with a specific financial scenario as input and
>   expected ledger entries as output — 12 tests, one per rule, fully isolated
> - When the business added a 13th edge case, I added one rule class and one test —
>   zero changes to existing rules
> - The `UnhandledScenarioException` means any uncovered combination fails loudly —
>   not silently with wrong behavior
>
> This is the **Command pattern** for the actions and the **Chain of Responsibility**
> for the matching — the request passes through rules until one handles it."

---

### Question 10

**Interviewer:** "You mentioned the system is used by 20+ different case types.
How do you make sure new case types can be added without breaking existing ones?"

**Model Answer:**

> "This is exactly the **Open-Closed Principle** applied at the framework level.
>
> The core framework — case creation, task assignment, status transitions, folder management
> — is in a base layer. It defines abstractions but contains no case-type-specific logic.
>
> Each case type provides a **customizer** — a plugin that implements a `CaseCustomizer`
> interface with lifecycle hooks:
>
> ```java
> interface CaseCustomizer {
>     void onCaseCreate(Case newCase, CaseContext ctx);
>     void onStateTransition(Case c, CaseStatus from, CaseStatus to, CaseContext ctx);
>     void onOrderIssuance(Case c, OrderPayload order, CaseContext ctx);
>     CaseTypeCd supportedCaseType();
> }
> ```
>
> A `CaseCustomizerFactory` resolves the correct customizer at runtime:
> ```java
> CaseCustomizer customizer = factory.getCustomizer(caseTypeCd);
> customizer.onCaseCreate(newCase, context);
> ```
>
> Adding a new case type = create a new class implementing `CaseCustomizer`, annotate
> it with `@Component`, and Spring auto-registers it. Zero changes to the factory,
> zero changes to the framework code.
>
> **Testing isolation:** each customizer is tested in isolation with mock `CaseContext`.
> The framework's tests do not need to know about specific customizers. Customizer tests
> do not need to boot the full application.
>
> **The runtime safety net:** if someone adds a case type but forgets to register a
> customizer, the factory throws `UnknownCaseTypeException` with the type code — not
> a NullPointerException somewhere deep in the call stack.
>
> This is the **Strategy + Factory** combination. Strategy for the algorithm variation,
> Factory for the runtime resolution. It scales linearly — 20 case types, 20 strategy
> classes, zero case-type-specific code in the framework core."

---

## 18.4 Architecture Vocabulary Cheat Sheet

> Use these phrases naturally. They signal SDE-2/3 maturity.

### On Design Decisions
```
"The trade-off we made was..."              (shows you weighed options)
"We chose X over Y because..."              (shows reasoning, not just outcome)
"The failure mode of this approach is..."   (shows production awareness)
"What I would change today is..."           (shows engineering growth)
"The constraint that drove this decision was..." (shows context awareness)
```

### On Data + Storage
```
"bounded context with its own data ownership"  (DDD vocabulary)
"append-only event log with projection"        (event sourcing pattern)
"read model separated from write model"        (CQRS vocabulary)
"optimistic concurrency via version field"     (precise locking language)
"schema evolution with backward compatibility" (Protobuf/Avro language)
"single-writer per partition"                  (Kafka/sharding principle)
```

### On Scale + Resilience
```
"horizontal scaling of stateless services"     (vs vertical scaling)
"cascade failure prevention via circuit breaker" (Resilience4j vocabulary)
"bulkhead isolation between partitions"        (failure isolation pattern)
"idempotency key for exactly-once semantics"   (duplicate prevention)
"at-least-once delivery with idempotent consumer" (Kafka pattern)
"graceful degradation under load"              (vs hard failure)
```

### On Transactions + Consistency
```
"strict atomicity across multiple resources"   (XA/2PC context)
"compensating transaction for rollback"        (Saga vocabulary)
"linearizable reads from primary"              (vs eventual from replica)
"write skew prevented by SELECT FOR UPDATE"    (advanced isolation)
"dual-write problem solved via Outbox pattern" (CDC/event consistency)
```

### On Observability
```
"distributed trace ID propagated across services" (OpenTelemetry vocabulary)
"structured JSON logging with correlation ID"     (log aggregation)
"RED metrics: rate, errors, duration"             (SRE vocabulary)
"health check endpoint for readiness probe"       (Kubernetes vocabulary)
"alert on P99 latency, not average"               (SRE maturity signal)
```

---

## 18.5 The Interviewer's Internal Scorecard

> Understanding how you are evaluated helps you calibrate your answers.

| Dimension | SDE-1 Answer | SDE-2 Answer (Target) | SDE-3 Answer |
|---|---|---|---|
| **Problem framing** | Describes what they built | Explains WHY they built it that way + trade-offs | Proactively questions whether the problem was framed correctly |
| **Design vocabulary** | Domain jargon (DRC07, APL01) | Generic software patterns (double-entry ledger, state machine) | System design vocabulary (bounded context, CQRS, saga) |
| **Failure awareness** | "It works" | "Here is the failure mode and how we mitigate it" | "Here is the failure mode, our mitigation, and the residual risk we accepted" |
| **Trade-off discussion** | "We used X" | "We chose X over Y because of constraint Z" | "We chose X, but in hindsight Y would have been better because..." |
| **Code quality signals** | SOLID mentioned | Strategy + Factory + AOP shown with real code | Also discusses testing strategy, extensibility, and how new developers onboard |
| **Scale awareness** | "It works under load" | "We sharded by stateCd, cached master data in JVM, pre-scaled for deadline spikes" | Also discusses: database connection pool limits, GC pressure under load, JVM heap sizing |
| **Self-awareness** | "Everything was well-designed" | "I would change X if I rebuilt it today" | "The specific technical debt items and why we consciously deferred them" |

---

## 18.6 One-Page Cheat Sheet — Say This, Not That

```
TOPIC: Your project at GSTN
  SAY:  "I owned end-to-end delivery of an appellate order processing engine for a
         government tax compliance platform serving 140 million registered entities
         across 28 jurisdictions."
  NOT:  "I worked on the GST appeal module which handles APL01, APL03, APL04 orders."

TOPIC: The complexity
  SAY:  "The core challenge was a 12-scenario decision matrix — the combination of
         two independent court outcomes produces 12 distinct financial obligation states,
         each requiring different ledger operations."
  NOT:  "It was complex because there are many cases like confirmed-rejected,
         modified-modified, etc."

TOPIC: Your solution
  SAY:  "I modelled it as a rule engine — each scenario is an explicit Rule object
         with a condition predicate and an action handler. The engine evaluates rules
         until one matches. Each rule is independently testable."
  NOT:  "I wrote all the logic inside a service method and used if-else to handle
         the different scenarios."

TOPIC: Concurrency
  SAY:  "We used two layers of concurrency control: optimistic locking via a @Version
         field on the entity for database-level protection, and a Redis distributed
         lock at the application boundary for early rejection of concurrent requests
         before they do any expensive work."
  NOT:  "We used @Version and also Redis SET NX to prevent two people issuing at once."

TOPIC: Caching
  SAY:  "A two-tier caching architecture: JVM in-memory for bounded, low-change reference
         data loaded at startup, and Redis for session and transactional data shared
         across instances. The decision criterion was change frequency and cross-instance
         consistency requirements."
  NOT:  "We cached things in LocalCacheFwk and DistCacheFwk for performance."

TOPIC: What you'd change
  SAY:  "I would replace XA 2-phase commit with a Saga pattern for the case and
         workflow steps, reserving 2PC only for the financial ledger entry where
         strict atomicity is non-negotiable. This reduces the scope of row-level
         locks significantly."
  NOT:  "The design is good. Maybe I'd write more tests."

TOPIC: Scale
  SAY:  "The system is sharded by jurisdiction code — 28 independent data partitions —
         with dynamic datasource routing implemented via Spring's AbstractRoutingDataSource
         and a ThreadLocal-based context holder. Each partition scales independently."
  NOT:  "We have different databases for each state, and the code picks the right one
         based on which state the request is for."
```

---

*Last Updated: April 2026 (v8 — SDE-2 Interview Simulation added — Section 18: Architecture Questions, Feature Deep Dive, Vocabulary Upgrade, Interviewer Scorecard)*
