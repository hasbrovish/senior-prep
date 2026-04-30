# Final Resume Bullets — SDE-2 / SDE-3 Target | 5.6 Years Experience
### ATS-Friendly · Impact-Led · Sorted High → Low Priority
### Grounded in actual codebase: CR28625A (~40 files), CR27893 (~55 files), 5 modules

> **How these are written:**
> `[Strong action verb] + [what you built] + [technical depth signal] + [scale or outcome]`
> Every bullet passes three tests:
> (1) ATS keyword match for JD terms (Java, Spring Boot, distributed systems, microservices, concurrency, scalability)
> (2) Hiring manager reads "this person thinks at system level, not just code level"
> (3) Interviewer has a rich thread to pull — every word is defensible and backed by real code

---

## THE FIVE BULLETS

---

### BULLET 1 — Multi-Scenario Financial State Machine + Double-Entry Ledger
*(Highest impact. Shows system design depth, financial domain, and end-to-end ownership across ~75 files)*

> **Designed and implemented a 12-scenario financial order-processing engine for India's national tax dispute platform (15.2 million taxpayers, 28 state jurisdictions) — built a decision-matrix state machine handling multi-tier demand chains (original demand, first-appeal order, subsequent order) with conditional demand creation, inter-account balance transfers, dispute reversals, and refund triggers; each scenario generates immutable double-entry ledger transactions (debit/credit) across 3 databases, impacting 75+ Java classes across 5 microservice modules.**

**ATS keywords hit:** system design, Java, Spring Boot, microservices, financial systems, ledger, state machine, database, distributed systems
**What it signals:** You own an entire financial domain end-to-end — not just APIs, but the underlying accounting logic. 12-scenario matrix + ledger = SDE-3 territory.
**What interviewer will ask:** "Walk me through one scenario" → You explain confirm-reject: reverse D1 dispute CR, close D2 with credit determine + transfer-out payments, update D1 status. Each step is a named ledger transaction.
**What you must know by heart:**
- Outstanding = ΣDR − ΣCR (>0 = owes, =0 = settled, <0 = refund due)
- Why Transfer-In/Transfer-Out exist (negative balance must move between demand accounts)
- Why reject-reject has zero ledger changes (no D2/D3 ever created)
- The difference between Strategy (each scenario = named rule) vs nested if-else (unmaintainable at 12 combinations)

---

### BULLET 2 — Concurrent Order Issuance + Distributed Transactions
*(Shows the hardest backend skill: concurrency control + XA 2PC + defensive programming)*

> **Engineered a defense-in-depth concurrency control system for adjudication order issuance — implemented Redis distributed locks (SETNX with TTL) at the API gateway to prevent duplicate requests across clustered instances, JPA optimistic locking (@Version) at the persistence layer as a safety net, and XA/Atomikos 2-phase commit to guarantee atomicity across case management, financial ledger, and workflow databases; this eliminated race conditions where two officers could simultaneously issue conflicting orders on the same demand.**

**ATS keywords hit:** concurrency, distributed systems, Redis, JPA, Spring Boot, transactions, atomicity, database, microservices
**What it signals:** You understand TOCTOU race conditions, why one layer of defense isn't enough, and when to accept XA 2PC latency trade-offs (low-frequency, high-stakes operations).
**What interviewer will ask:** "Why not just @Version alone?" → Redis lock prevents wasted work across instances; @Version is the DB-level safety net if Redis fails.
**What you must know by heart:**
- SETNX semantics: set-if-not-exists + TTL (prevents deadlock if holder crashes)
- @Version: read v1 → modify → write WHERE version=v1 → fails if someone else incremented to v2
- XA 2PC protocol: prepare phase (all vote yes) → commit phase (coordinator commits all)
- What happens if coordinator crashes between prepare and commit (recovery log replay)
- Why Saga pattern was NOT chosen here (no acceptable intermediate state for legal orders)

---

### BULLET 3 — Waiver Payment Lifecycle + Void Order Reversal System
*(Shows you handle full create-approve-void-appeal lifecycle — not just happy path)*

> **Built an end-to-end government compliance waiver lifecycle spanning 7 order types (application, payment confirmation, approval, void, rejection, appeal integration, DRC-03 reconciliation) — implemented the approval flow with ledger credit entries to reduce outstanding demand, void order issuance with compensating debit reversals to restore original balances, and cross-module appeal integration enabling taxpayers to appeal rejected waivers; the system handles demand status transitions, recovery case updates, and automated email/SMS notifications across the complete lifecycle.**

**ATS keywords hit:** Java, Spring Boot, REST API, microservices, financial systems, event-driven, compliance, lifecycle management
**What it signals:** You don't just build APIs — you own the entire business lifecycle including error paths, reversals, and cross-module integration. "Compensating transactions" is SDE-3 vocabulary.
**What interviewer will ask:** "What happens when a void order is issued?" → SPL06 void reverses the SPL05 approval credit by inserting a compensating debit entry, restores the original demand status from before the waiver, and updates the recovery case to RECOVERABLE.
**What you must know by heart:**
- SPL05 approval = REDUCTION_TRANS (credit entry → reduces outstanding)
- SPL06 void = DEBIT_TRANS (compensating debit → restores outstanding)
- Why you store `origOrdDmdStatusBfrSpl06` (to restore the exact pre-waiver demand status, not a hardcoded value)
- Idempotency: checking demand status != SETTLED and != WITHDRAWN before any ledger write

---

### BULLET 4 — Multi-Tenant Database Routing + Two-Tier Caching Architecture
*(Shows you think about scale, latency tiers, and request-scoped state management)*

> **Architected multi-tenant database routing across 28 state jurisdictions using Spring's AbstractRoutingDataSource with ThreadLocal request-scoped context propagation, paired with a two-tier caching strategy — JVM in-process cache for 100+ reference data types loaded at startup via @PostConstruct, and Redis distributed cache for 40+ shared data types with TTL-based eviction — built aggregation counter APIs for officer dashboards that compute real-time case counts (pending, action-required, total) per jurisdiction without redundant database round trips.**

**ATS keywords hit:** scalability, multi-tenant, Spring Boot, Redis, caching, performance optimization, REST API, microservices, database
**What it signals:** You understand the full read path — ThreadLocal propagation, cache hierarchy, and why counter APIs need careful design to avoid N+1 queries.
**What interviewer will ask:** "What's the risk with ThreadLocal?" → Must call clearDbType() in finally block; leaked ThreadLocal in a thread pool routes the next request to the wrong state's database.
**What you must know by heart:**
- AbstractRoutingDataSource.determineCurrentLookupKey() → reads ThreadLocal → returns DB key
- Why JVM cache for reference data (never changes mid-request, zero network hop) vs Redis for shared mutable data (TTL eviction, cross-instance consistency)
- Counter API design: single SQL with GROUP BY status, not N separate count queries
- @PostConstruct loading: happens once at startup, avoids repeated DB calls for static master data

---

### BULLET 5 — Plugin-Based Case Lifecycle Framework + Cross-Cutting Validation
*(Shows framework-level OOP thinking and extensibility design)*

> **Designed a plugin-based case lifecycle framework using Strategy + Factory patterns supporting 20+ legally distinct proceeding types — each type registers a CaseCustomizer and CaseFolderItemCustomizer with pre/post lifecycle hooks, configurable transaction modes (XA vs non-XA), and type-specific validation rules; built a reusable cross-cutting validation layer handling jurisdiction eligibility, officer role authorization, simultaneous appeal detection, and financial amount consistency checks — enabling new case types (including waiver scheme types) to be onboarded by adding one customizer class with zero changes to framework code.**

**ATS keywords hit:** design patterns, object-oriented design, Spring Boot, extensible architecture, transaction management, Java, validation, RBAC
**What it signals:** You write extensible frameworks, not one-off code. New waiver types (SPL01–SPL07) were onboarded using your existing Strategy+Factory without touching core framework.
**What interviewer will ask:** "How is the factory extensible?" → CaseCustomizerFactory resolves by caseTypeCd at runtime; new type = new @Component class + one switch case in factory, zero changes to CaseHandler/CaseService.
**What you must know by heart:**
- Strategy pattern: CaseCustomizer interface → AppealCaseCustomizer, WaiverSchemeFolderItemCustomizer, AdjudicationCaseCustomizer (each encapsulates type-specific logic)
- Factory pattern: CaseCustomizerFactory.getCustomizer(caseTypeCd) → returns correct strategy at runtime
- Open/Closed Principle: framework is closed for modification, open for extension via new customizer
- Validation chain: AppealValidations checks case status + access groups + jurisdiction + financial amounts before any state transition

---

## QUICK SUMMARY TABLE

| Bullet | Core Signal | Primary Skill | Backed by |
|---|---|---|---|
| **1** — 12-scenario financial engine | Domain modelling + system design | State machine, ledger, decision matrix | CR28625A — DemandProcessingUtil, AppealOrderItemCustomizer |
| **2** — Concurrent order issuance | Distributed systems depth | Redis locks, XA 2PC, @Version | AppealCaseCustomizer, WaiverLedgerUpdateCtrl |
| **3** — Waiver payment lifecycle | Full lifecycle ownership | Compensating transactions, reversals | CR27893 (A–D2) — ~55 files, WaiverSchemeFolderItemCustomizer |
| **4** — Multi-tenant + caching + APIs | Scale architecture | ThreadLocal routing, two-tier cache, counter APIs | DbContextHolder, DistCacheFwk, ReturnsServiceImpl |
| **5** — Plugin case framework | Framework design + validation | Strategy/Factory, cross-cutting validation | CaseCustomizerFactory, AppealValidations |

---

## HOW TO USE ON YOUR RESUME

```
If the JD says:                    Emphasize bullet:
──────────────────────────────────────────────────────
"distributed systems"              1, 2
"system design"                    1, 2, 5
"scalability / performance"        4
"backend microservices"            1, 3, 4
"design patterns / OOP"            1, 5
"Kafka / event-driven"             3 (notifications), 2 (post-commit)
"Spring Boot / Java"               all 5
"fintech / financial domain"       1, 2, 3
"platform engineering"             4, 5
"REST API development"             3, 4
"compliance / government / legal"  1, 3
```

---

## RESUME HEADER LINE (use above the bullets)

> **Software Development Engineer | Java · Spring Boot · Distributed Systems · Microservices**
> *5.6 years building India's national tax compliance platform — 15.2 million taxpayers (1.52 crore), 28 jurisdictions, full-stack ownership across 5 microservice modules*

---

## ATS-SAFE COPY-PASTE VERSIONS (No markdown, no unicode)

Use these exact texts in your resume document (Word/PDF):

```
1. Designed and implemented a 12-scenario financial order-processing engine for India's national
   tax dispute platform (15.2 million taxpayers, 28 jurisdictions) - built a decision-matrix
   state machine handling multi-tier demand chains with conditional demand creation, inter-account
   balance transfers, dispute reversals, and refund triggers; each scenario generates immutable
   double-entry ledger transactions across 3 databases, impacting 75+ Java classes across
   5 microservice modules.

2. Engineered defense-in-depth concurrency control for adjudication order issuance - implemented
   Redis distributed locks (SETNX with TTL) at the API boundary, JPA optimistic locking at the
   persistence layer, and XA/Atomikos 2-phase commit across case management, financial ledger,
   and workflow databases, eliminating race conditions in concurrent multi-officer order issuance.

3. Built an end-to-end compliance waiver lifecycle spanning 7 order types (application, approval,
   void, rejection, appeal integration) - implemented approval flow with ledger credit entries,
   void order issuance with compensating debit reversals, and cross-module appeal integration
   with automated status transitions, recovery case updates, and email/SMS notifications.

4. Architected multi-tenant database routing across 28 jurisdictions using Spring
   AbstractRoutingDataSource with ThreadLocal context propagation, paired with two-tier caching
   (JVM in-process for 100+ reference types, Redis distributed for 40+ shared types) - built
   aggregation counter APIs for officer dashboards computing real-time case counts per jurisdiction.

5. Designed a plugin-based case lifecycle framework using Strategy and Factory patterns supporting
   20+ proceeding types - each type registers a customizer with lifecycle hooks and configurable
   transaction modes, with a reusable validation layer for jurisdiction, role authorization, and
   financial consistency checks, enabling new case types with zero framework code changes.
```

---

## WHAT NOT TO WRITE (Common Mistakes)

```
BAD:  "Worked on the GST litigation module to handle APL01 and APL03 appeal cases"
WHY:  Domain jargon. ATS rejects it, interviewer is confused.

BAD:  "Developed REST APIs using Spring Boot and Java for the back-office portal"
WHY:  Generic. Every Java dev writes this. Zero differentiation.

BAD:  "Implemented caching using Redis and local cache to improve performance"
WHY:  No specifics. What was cached? What was the design decision?

BAD:  "Participated in the design and development of the litigation module"
WHY:  "Participated" signals you were a bystander, not an owner.

GOOD: Engineered / Designed / Architected / Implemented / Built / Optimized
      (signals individual ownership and technical depth)
```

---

## CONCEPTS YOU MUST KNOW BY HEART (If it's on your resume, they WILL ask)

### For Bullet 1 (12-Scenario Engine)
| Concept | What to say | Why they ask |
|---|---|---|
| State Machine | "Each demand has states: Created, FAOI, SOI, Settled, Refund Due. Transitions are guarded by financial conditions." | Tests if you designed it or just coded it |
| Double-Entry Ledger | "Every financial operation creates a DR or CR entry. Outstanding = sum(DR) - sum(CR). Negative = refund due." | Tests financial domain understanding |
| Strategy vs if-else | "Each scenario is a named Rule with a condition predicate and action. Adding scenario = adding one Rule class, no existing code touched." | Tests OOP and Open/Closed Principle |
| Transfer-In/Out | "When D1 outstanding goes negative (overpaid), the negative balance transfers OUT of D1 and INTO D2 as a credit." | Tests you understand the accounting flow |

### For Bullet 2 (Concurrency)
| Concept | What to say | Why they ask |
|---|---|---|
| TOCTOU Race | "Two officers pass the status check simultaneously, both proceed to issue — classic Time-Of-Check-Time-Of-Use." | Tests if you understand the actual problem |
| Redis SETNX | "SET key IF NOT EXISTS with TTL. First request acquires, second fails fast. TTL prevents deadlock if holder crashes." | Tests Redis depth |
| @Version | "JPA adds WHERE version=N to UPDATE. If another transaction incremented it, zero rows updated, throws OptimisticLockException." | Tests JPA internals |
| XA 2PC | "Phase 1: all resource managers vote PREPARE. Phase 2: coordinator sends COMMIT. If any vote NO, all ROLLBACK." | Tests distributed systems knowledge |
| Why not Saga | "No acceptable intermediate state — can't show 'order issued' while ledger hasn't updated. Legal compliance requires atomicity." | Tests trade-off thinking |

### For Bullet 3 (Waiver Lifecycle)
| Concept | What to say | Why they ask |
|---|---|---|
| Compensating Transaction | "SPL06 void inserts a debit entry that reverses the SPL05 credit. Net effect: demand balance restored to pre-waiver state." | Tests if you understand reversal patterns |
| Idempotency Guard | "Before any ledger write, check: demand status != SETTLED and != WITHDRAWN. Prevents double-processing." | Tests defensive programming |
| Cross-Module Integration | "Waiver rejection (SPL07) creates a case that taxpayer can appeal via APL01 — the appeal module reads the waiver case folder." | Tests end-to-end thinking |

### For Bullet 4 (Multi-Tenant + Caching)
| Concept | What to say | Why they ask |
|---|---|---|
| ThreadLocal Risk | "Must call clearDbType() in finally. Leaked ThreadLocal in a pooled thread routes next request to wrong state's DB." | Tests real production experience |
| AbstractRoutingDataSource | "Override determineCurrentLookupKey() to read ThreadLocal. Spring routes to the correct DataSource per request." | Tests Spring internals |
| Two-Tier Cache Why | "JVM cache: zero network hop for static reference data. Redis: shared mutable data with TTL, consistent across instances." | Tests cache design thinking |
| Counter API Design | "Single SQL with GROUP BY status, not N separate COUNT queries. Avoids N+1 problem at the dashboard level." | Tests query optimization |

### For Bullet 5 (Framework Design)
| Concept | What to say | Why they ask |
|---|---|---|
| Strategy Pattern | "Interface CaseCustomizer with beforeCreate/afterCreate hooks. Each case type implements it differently." | Tests design pattern depth |
| Factory Pattern | "CaseCustomizerFactory.getCustomizer(caseTypeCd) resolves the correct strategy at runtime." | Tests creational pattern |
| Open/Closed Principle | "Adding waiver scheme (SPL01-07) = adding WaiverSchemeFolderItemCustomizer + registering in factory. Zero changes to CaseHandler." | Tests SOLID understanding |
| XA vs non-XA config | "Demand orders need 3-DB atomicity (XA). Non-demand orders use single-DB @Transactional. Configurable per case type." | Tests transaction design |

---

*Last Updated: April 2026 (v2) — Final resume bullets for SDE-2/SDE-3 applications*
*5 bullets grounded in CR28625A (subsequent order, ~40 files) + CR27893 (waiver scheme, ~55 files)*
*Backed by: DemandProcessingUtil, AppealOrderItemCustomizer, AppealCaseCustomizer, WaiverSchemeFolderItemCustomizer, WaiverLedgerUpdateCtrl, CaseCustomizerFactory, AppealValidations, DbContextHolder, DistCacheFwk*
