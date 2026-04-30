# Final Resume — Full-Stack | SDE-2 / SDE-3 Target | 5.6 Years
### ATS-Friendly · Action + Impact Format · Backend + Frontend
### Jayanti Vishnoi

---

## COPY-PASTE RESUME BLOCK

```
JAYANTI VISHNOI
Software Development Engineer | 5.6 Years
Java · Spring Boot · Angular · Distributed Systems · Microservices
Email: [email] | Phone: [phone] | LinkedIn: [link] | GitHub: [link]

────────────────────────────────────────────────────────────
PROFESSIONAL SUMMARY
────────────────────────────────────────────────────────────

Full-stack engineer with 5.6 years of experience building India's national
tax compliance platform serving 15.2 million taxpayers across 28 state
jurisdictions. End-to-end ownership across 5 Java microservice modules and
a 70,000+ LOC frontend application. Specializing in distributed transactions,
financial state machines, and large-scale Angular migration.

────────────────────────────────────────────────────────────
SKILLS
────────────────────────────────────────────────────────────

Languages:    Java, TypeScript, JavaScript (ES6+), SQL
Backend:      Spring Boot, Spring MVC, JPA/Hibernate, REST APIs, Kafka,
              Redis, Atomikos (XA 2PC), Maven
Frontend:     Angular, AngularJS, RxJS, PrimeNG, ngx-bootstrap, ExcelJS
Database:     Oracle, PostgreSQL, multi-tenant sharding
Architecture: Microservices, monorepo (Nx), design patterns (Strategy,
              Factory, Facade, Observer, Chain of Responsibility)
Tools:        Git, Jenkins, SonarQube, JIRA

────────────────────────────────────────────────────────────
EXPERIENCE
────────────────────────────────────────────────────────────

INFOSYS LIMITED — Software Development Engineer          [Start Date] – Present
Project: GSTN (Goods and Services Tax Network)
Client:  Government of India — National Tax Platform

Tech Stack: Java 8+, Spring Boot, Spring MVC, JPA/Hibernate, Oracle,
            PostgreSQL, Redis, Kafka, Atomikos (XA), Angular, AngularJS,
            TypeScript, RxJS, PrimeNG, ExcelJS, Maven, Git, Jenkins

Platform Scale: 15.2M registered taxpayers | 28 state jurisdictions |
                5 Java microservice modules | 70K+ LOC frontend | 21 Angular
                micro-libraries in monorepo

• Designed and implemented a 12-scenario financial order-processing state
  machine using Java, Spring Boot, and JPA/Hibernate — handling multi-tier
  demand chains with conditional demand creation, inter-account balance
  transfers, dispute reversals, and refund triggers across 3 databases;
  reduced manual demand-processing errors by automating all 12 first-appeal
  outcome combinations for 15.2M taxpayer accounts across 28 jurisdictions.

• Engineered defense-in-depth concurrency control using Redis SETNX
  distributed locks, JPA @Version optimistic locking, and XA/Atomikos
  2-phase commit — eliminated race conditions in concurrent multi-officer
  order issuance, ensuring zero duplicate financial entries across case
  management, ledger, and workflow databases.

• Built an end-to-end GST waiver lifecycle (7 order types) in Java/Spring
  Boot with double-entry ledger integration — implemented approval flows
  with ledger credit entries, void orders with compensating debit reversals,
  and cross-module appeal integration; enabled processing of 4.8 lakh
  backlogged waiver applications with automated status transitions and
  email/SMS notifications.

• Architected multi-tenant database routing for 28 jurisdictions using Spring
  AbstractRoutingDataSource and ThreadLocal context propagation, paired with
  two-tier caching (JVM in-process + Redis distributed) — reduced average
  API response time by eliminating redundant DB lookups for 100+ reference
  types and 40+ shared configuration types across all microservices.

• Designed a recursive async case-graph traversal engine in JavaScript/
  AngularJS with session-scoped ES6 Set deduplication and a 10+ rule
  compliance engine — eliminated redundant API calls and prevented infinite
  loops in deeply nested appeal chains, enabling real-time legal-validity
  checks for adjudicating officers before order issuance.

• Drove incremental migration of a 70,000+ LOC AngularJS application to
  Angular/TypeScript by architecting 21 standalone micro-libraries in an Nx
  monorepo using the Strangler Fig pattern — enabled parallel team delivery,
  eliminated cross-module coupling, and removed the need for a risky full
  rewrite while maintaining zero downtime for 15.2M taxpayer-facing services.

• Built a reusable Angular RBAC micro-library with RxJS BehaviorSubject state
  management, smart/dumb component separation, and ExcelJS audit export;
  implemented an HTTP interceptor centralizing auth token injection and error
  handling — enforced least-privilege access for thousands of back-office
  officers and eliminated per-service auth boilerplate across 21 modules.

• Owned end-to-end appeal litigation frontend (4 controllers, 11K+ LOC)
  covering case assignment, simultaneous/combined order processing, and
  real-time dashboard counters — extracted shared business logic into a
  dedicated AngularJS service layer (AppealCaseService), reducing code
  duplication by ~800 lines and improving maintainability for a module
  handling 43 appeal controllers and ~78K LOC.

────────────────────────────────────────────────────────────
EDUCATION
────────────────────────────────────────────────────────────

[Your Degree] — [University] — [Year]
```

---

## IF SPACE-LIMITED: PICK 5-6 BULLETS BASED ON JD

| If the JD emphasizes... | Use bullets |
|---|---|
| Backend / distributed systems / Java | 1, 2, 3, 4, 5 |
| Full-stack / Java + Angular | 1, 3, 4, 5, 6, 8 |
| Frontend-heavy / Angular / TypeScript | 5, 6, 7, 8, 1 |
| System design / architecture | 1, 2, 4, 5, 6 |
| Fintech / financial domain | 1, 2, 3, 5 |
| Platform / infrastructure / scale | 2, 4, 6, 7 |
| Government / compliance / legal tech | 1, 3, 5, 8 |

---

## BULLET-BY-BULLET: WHAT I DID → IMPACT

---

### BULLET 1 — 12-Scenario Financial State Machine
**Tech used:** Java, Spring Boot, JPA/Hibernate, Oracle, Atomikos XA
**What I did:** Built 12 first-appeal-outcome × subsequent-outcome scenario handlers in DemandProcessingUtil.java (lines 1733-4796). Each scenario creates/updates demands, posts double-entry ledger entries, triggers transfers.
**Impact:** Automated all appeal-order financial outcomes — officers no longer manually compute demand adjustments for 15.2M taxpayer accounts. One code path per scenario instead of ad-hoc SQL scripts.
**Hook question:** "Walk me through one scenario"
→ Confirm-reject: reverse D1 dispute, close D2 with credit determine + transfer-out, update D1 status

---

### BULLET 2 — Concurrency + Distributed Transactions
**Tech used:** Redis (SETNX), JPA @Version, Atomikos XA 2PC, Spring Boot
**What I did:** Added Redis SETNX lock at API entry, @Version on entity, XA 2PC across 3 databases. Three layers: prevent, detect, recover.
**Impact:** Eliminated duplicate financial entries when multiple officers issue orders on the same case simultaneously. Zero data-corruption incidents post-deployment.
**Hook question:** "Why not just @Version alone?"
→ Redis prevents wasted work; @Version is DB-level safety net if Redis fails

---

### BULLET 3 — Waiver Lifecycle (7 Order Types)
**Tech used:** Java, Spring Boot, JPA/Hibernate, Kafka, Oracle
**What I did:** Built SPL01-SPL07 lifecycle — approval with ledger credits, void with compensating debits, appeal-integration with status transitions. Created WaiverSchemeFolderItemCustomizer from scratch (~55 files).
**Impact:** Enabled processing of 4.8 lakh backlogged waiver applications under Section 128A amnesty scheme. Void-order reversal restores exact pre-waiver state from snapshot, preserving audit trail.
**Hook question:** "What happens on void order?"
→ SPL06 inserts compensating debit, restores pre-waiver status from origOrdDmdStatusBfrSpl06 snapshot, sets case to RECOVERABLE

---

### BULLET 4 — Multi-Tenant Routing + Caching + Plugin Framework
**Tech used:** Spring AbstractRoutingDataSource, ThreadLocal, Redis, JVM cache, Strategy + Factory patterns
**What I did:** Implemented jurisdiction-aware DB routing (28 shards), two-tier cache (JVM for 100+ reference types, Redis for 40+ shared), and plugin framework (CaseCustomizerFactory → 20+ CaseCustomizer implementations).
**Impact:** New proceeding type = new class, zero framework changes. Cache eliminated redundant DB lookups across all microservices. ThreadLocal routing serves correct jurisdiction data for every request.
**Hook question:** "ThreadLocal risk?"
→ Must clearDbType() in finally; leaked ThreadLocal routes next request to wrong DB

---

### BULLET 5 — Case-Graph Traversal + Compliance Rule Engine
**Tech used:** JavaScript (ES6), AngularJS, Promise.all, ES6 Set
**What I did:** Built recursive DFS traversal (getCaseItemDetails ↔ getItemDetailsFromARN) with composite-key deduplication (sessionId + scopeId + refId). Built 10+ condition rule engine checking waiver status, 4-month statutory windows, order lifecycle states.
**Impact:** Officers see real-time compliance warnings before issuing orders — prevents legally invalid orders. Cycle detection eliminates infinite API loops in nested appeal chains. Soft-failure ensures partial data still renders.
**Hook question:** "What's the graph structure?"
→ Case Item → ARN → Appeal Folder → RefId → Case Item (mutual recursion, Set for visited tracking)

---

### BULLET 6 — AngularJS-to-Angular Migration (70K+ LOC)
**Tech used:** Angular, TypeScript, Nx monorepo, downgradeComponent, RxJS
**What I did:** Architected 21 standalone micro-libraries in gstn-apps/libs/back-office/. New features built in Angular, bridged into AngularJS host via downgradeComponent.
**Impact:** Enabled parallel team delivery — 5+ BO modules share libraries. No risky full rewrite. Each library independently buildable and testable. Zero downtime during migration.
**Hook question:** "How did you decide what to migrate first?"
→ New features in Angular; existing features migrated when needing major changes; prioritized by change frequency

---

### BULLET 7 — RBAC Micro-Library + HTTP Interceptor
**Tech used:** Angular, TypeScript, RxJS BehaviorSubject, ExcelJS, HTTP Interceptor
**What I did:** Built enable-disable-access-role library (21 TS files) with smart/dumb components and BehaviorSubject state. Built HTTP interceptor centralizing auth token injection, Content-Type, BlockUI, error handling.
**Impact:** Enforced least-privilege access for thousands of officers — unauthorized actions hidden at UI level. Interceptor eliminated per-service auth boilerplate across all 21 modules. Excel export replaced manual audit reporting.
**Hook question:** "Why RBAC on frontend if backend also enforces?"
→ Defense in depth. Frontend = UX. Backend = security boundary (403). Both needed.

---

### BULLET 8 — Appeal Frontend Module Ownership (11K+ LOC)
**Tech used:** AngularJS, JavaScript, Bootstrap modals, $compile, ShareData service
**What I did:** Owned 4 controllers (appealorderctrl 16K LOC, appealorderctrltd 13K, appealAssignmentCtrl, appealcasemgmtctrl). Built simultaneous/combined order processing. Extracted shared logic into AppealCaseService.
**Impact:** Reduced ~800 lines of duplicated validation code across 4 controllers to 1 service call. Simultaneous-order feature enables single adjudication for related appeals. Dashboard counters give officers real-time workload visibility.

---

## ATS KEYWORD COVERAGE

| Category | Keywords in Bullets |
|---|---|
| **Languages** | Java, JavaScript (ES6), TypeScript, SQL |
| **Backend Frameworks** | Spring Boot, Spring MVC, JPA/Hibernate, Atomikos (XA 2PC) |
| **Frontend Frameworks** | Angular, AngularJS, RxJS, PrimeNG, ngx-bootstrap |
| **Databases** | Oracle, PostgreSQL, multi-tenant sharding |
| **Caching / Messaging** | Redis (SETNX, distributed cache), Kafka, JVM in-process cache |
| **Architecture** | microservices, distributed systems, monorepo, multi-tenant, REST API |
| **Patterns** | Strategy, Factory, Facade, Observer, Chain of Responsibility, Strangler Fig |
| **Security** | RBAC, HTTP interceptor, distributed locks, defense-in-depth |
| **CS Fundamentals** | graph traversal, recursion, cycle detection, deduplication, state machine, rule engine |
| **Transactions** | XA 2PC, optimistic locking (@Version), compensating transactions, double-entry ledger |
| **Scale Numbers** | 15.2M taxpayers, 28 jurisdictions, 70K+ LOC, 21 libraries, 75+ classes, 4.8 lakh backlog |
| **Action Verbs** | Designed, Engineered, Built, Drove, Architected, Owned, Implemented |
| **CS Fundamentals** | graph traversal, recursion, deduplication, cycle detection, rule engine |
| **Patterns** | Strategy, Factory, Facade, Observer, Chain of Responsibility, Strangler Fig |
| **Transactions** | XA 2PC, optimistic locking, compensating transactions, double-entry ledger |
| **Scale** | 15.2M taxpayers, 28 jurisdictions, 70K+ LOC, 21 libraries, 75+ classes |
| **Ownership** | Designed, Engineered, Built, Drove, Owned, Architected |

---

## JD-TO-BULLET MAPPING

```
JD says "Java / Spring Boot"              → Bullets 1, 2, 3, 4
JD says "Angular / TypeScript / RxJS"      → Bullets 5, 6, 7, 8
JD says "distributed systems"              → Bullets 1, 2, 4
JD says "system design"                    → Bullets 1, 2, 4, 5, 6
JD says "scalability / performance"        → Bullets 4, 6
JD says "design patterns / OOP"            → Bullets 4, 5, 7
JD says "full-stack"                       → Pick 2 backend (1,3) + 2 frontend (5,6) + 1 mixed (4)
JD says "fintech / financial"              → Bullets 1, 2, 3
JD says "migration / legacy modernization" → Bullet 6
JD says "security / RBAC"                  → Bullets 2, 7
JD says "frontend architecture"            → Bullets 5, 6, 7, 8
JD says "REST API development"             → Bullets 3, 4
JD says "graph / algorithms"               → Bullet 5
```

---

## CONCEPTS-TO-KNOW-BY-HEART TABLE

### Backend Concepts (Bullets 1-4)

| Concept | One-line answer | Which bullet |
|---|---|---|
| Double-entry ledger | Outstanding = Σ(DR) - Σ(CR). Negative = refund due. | 1 |
| Transfer-In/Out | Negative outstanding in D1 moves to D2 via transfer entries | 1 |
| SETNX + TTL | Set-if-not-exists with auto-expiry. Prevents deadlock if holder crashes. | 2 |
| @Version | JPA adds WHERE version=N to UPDATE. Fails if someone else incremented. | 2 |
| XA 2PC | Phase 1: PREPARE. Phase 2: COMMIT. All-or-nothing across 3 DBs. | 2 |
| Compensating transaction | SPL06 void inserts debit to reverse SPL05 credit. Audit trail preserved. | 3 |
| origOrdDmdStatusBfrSpl06 | Snapshot of pre-waiver status. Exact restore on void, not hardcoded. | 3 |
| ThreadLocal + clearDbType() | Must clear in finally. Leaked ThreadLocal = wrong DB on next request. | 4 |
| Strategy + Factory | CaseCustomizerFactory resolves by caseTypeCd. New type = new class, zero framework changes. | 4 |

### Frontend Concepts (Bullets 5-8)

| Concept | One-line answer | Which bullet |
|---|---|---|
| Mutual recursion | getCaseItemDetails ↔ getItemDetailsFromARN. DFS on directed graph. | 5 |
| ES6 Set dedup | O(1) has() + add(). Composite key = sessionId + scopeId + refId. | 5 |
| Session isolation | resetState() clears Sets + new sessionId. Prevents Case A leaking to Case B. | 5 |
| Soft failure | resolve() not reject() in catch. Partial failure doesn't kill traversal. | 5 |
| FSM (informal) | Boolean flags = states. if/else = guards. dialogueMessage = action. | 5 |
| Strangler Fig | New features in Angular. Old stays AngularJS. Gradual replacement. | 6 |
| downgradeComponent | Angular component wrapped for AngularJS host. Bridge for migration. | 6 |
| BehaviorSubject | Stores latest value. New subscribers get it immediately. = Observer pattern. | 7, 8 |
| Smart/dumb components | Container = API + state. Presentational = rendering + events. | 7 |
| Chain of Responsibility | HTTP interceptor: auth → content-type → BlockUI → error handling. | 7 |
| Service layer extraction | 4 controllers × 200 lines duplicated → 1 AppealCaseService = Facade + DRY. | 8 |

---

## WHAT NOT TO WRITE

```
BAD:  "Worked on both frontend and backend of the GST portal"
WHY:  No tech stack, no impact. Every full-stack dev says this.

BAD:  "Developed AngularJS controllers for appeal module"
WHY:  No what/impact. Doesn't say what the controllers DO or WHY they matter.

BAD:  "Used RxJS for state management in Angular components"
WHY:  Too generic. No impact. Say WHAT state, WHY reactive, WHAT changed.

BAD:  "Migrated code from AngularJS to Angular"
WHY:  No HOW (Strangler Fig, monorepo, 21 libraries) or IMPACT (parallel delivery, zero downtime).

FORMAT: [Action Verb] + [What I Built] + [Tech Stack Used] + [Measurable Impact / Business Outcome]
```

---

*Last Updated: April 2026*
*Full-stack resume combining:*
*Backend: Java/Spring Boot — CR28625A (~40 files), CR27893 (~55 files), 5 microservice modules*
*Frontend: Angular/AngularJS — AppealCaseService, gstn-apps (21 libraries), 70K+ LOC migration, RBAC library*
