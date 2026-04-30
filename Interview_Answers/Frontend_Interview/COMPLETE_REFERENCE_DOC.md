# COMPLETE REFERENCE DOCUMENT — GSTN Appeal System
## Resume, Architecture, Interview Prep & Learning Roadmap
**Generated:** April 27, 2026 | **Profile:** 5.6 yr Java Full-Stack | **Target:** SDE-2/SDE-3

---

# TABLE OF CONTENTS

1. [Profile & Goals](#1-profile--goals)
2. [Domain Glossary](#2-domain-glossary)
3. [Codebase Scale & Architecture](#3-codebase-scale--architecture)
4. [Features Built](#4-features-built)
5. [Resume Bullets](#5-resume-bullets)
6. [Power Bullets](#6-power-bullets)
7. [Interview Talking Points](#7-interview-talking-points)
8. [Additional Resume Signals](#8-additional-resume-signals)
9. [Architecture Patterns Quick Reference](#9-architecture-patterns-quick-reference)
10. [Self-Study Roadmap (What to Learn)](#10-self-study-roadmap)
11. [Senior Interview Prep — DSA](#11-dsa)
12. [Senior Interview Prep — Java Deep Dive](#12-java-deep-dive)
13. [Senior Interview Prep — System Design (HLD)](#13-system-design-hld)
14. [Senior Interview Prep — Low-Level Design (LLD)](#14-low-level-design-lld)
15. [Senior Interview Prep — Frontend (Angular + RxJS)](#15-frontend-angular--rxjs)
16. [Senior Interview Prep — Databases](#16-databases)
17. [Senior Interview Prep — Your Codebase Mapped to Interview Vocabulary](#17-your-codebase-mapped)
18. [Senior Interview Prep — Behavioral](#18-behavioral)
19. [12-Week Study Schedule](#19-study-schedule)
20. [Resources](#20-resources)

---

# 1. PROFILE & GOALS

- 5.6 years of experience as a Java full-stack engineer
- Currently working on **GSTN** (Goods and Services Tax Network) — India's national GST portal
- Targeting **SDE-2 / SDE-3** roles at product companies and startups
- Works primarily in AngularJS (legacy) and Angular (modern revamp), with Java backend
- Has built features across: appeal case management, order processing, RBAC, BO revamp
- Prefers resume bullets in **XYZ format** with generic, domain-agnostic language

---

# 2. DOMAIN GLOSSARY

*Internal name → what it actually is (use the plain-English version on your resume)*

| Internal Term | Plain English |
|---|---|
| DRC-07 | Tax demand notice issued by the department |
| APL-01 | Taxpayer's appeal application against a tax demand |
| APL-03 | Departmental appeal application |
| APL-04 | Adjudication order (final order on an appeal) |
| SPL-02 | Waiver application (under GST amnesty scheme, Section 128A) |
| SPL-05 | Waiver approval order |
| SPL-06 | Appeal order issued by first appellate authority |
| SPL-07 | Rejection order for waiver application |
| ARN | Appeal Reference Number (unique case identifier) |
| APLTD | Departmental appeal module (department is appellant) |
| APPEL | Taxpayer appeal module (taxpayer is appellant) |
| MFY | Multi-Finance Year (single demand spanning multiple tax years) |
| BO | Back Office (officer-facing portal) |
| FO | Front Office (taxpayer-facing portal) |
| GSTN | GST Network — the organization running India's GST IT infrastructure |

---

# 3. CODEBASE SCALE & ARCHITECTURE

## Scale

| Metric | Value |
|---|---|
| Total JS/TS files | 11,652 |
| Appeal module controllers | 43 |
| Appeal module LOC | ~77,986 |
| Largest file | appealorderctrl.js — 16,090 LOC |
| Second largest | appealorderctrltd.js — 13,191 LOC |
| gstn-apps micro-libraries | 21 |

## Key Modules

- **`BO-Home-Lit`** — legacy AngularJS back-office application
- **`BO-Revamp`** — modern Angular rewrite (RxJS, ngx-bootstrap, PrimeNG)
- **`gstn-apps/libs/back-office/`** — 21 TypeScript micro-libraries

## Architecture Patterns Found

- **HTTP Interceptor:** `http-error.interceptor.ts` — auth token injection, BlockUI, error mapping
- **RBAC micro-library:** `enable-disable-access-role/` — Angular + RxJS BehaviorSubject + ExcelJS export
- **AppealEffectService:** BehaviorSubject singleton with `isDataLoaded` guard (prevent duplicate API calls)
- **CacheService:** simple getter/setter cache for appeal effect counts
- **ShareData service:** cross-component communication in AngularJS layer
- **LocalStorage role caching:** `appellateAuthorityRole`, `assitantToAppellateRole`

## Simultaneous / Combined Order Feature

- `$scope.simulAppeals` array — related appeal cases
- `$scope.isSimulCombinedOrd` flag — combined proceeding status
- Dispute amount propagation across simultaneous cases
- Counter appeal tracking: `latestApltdCase` vs `latestAppelCase`
- Lives in appealorderctrl.js (16K LOC)

## Micro-library List (gstn-apps/libs/back-office/)

auth, bao-device-access, bi-feedback, bo-address, constants, core,
enable-disable-access-role, goods-transport-agencies, models, offline-rfn-gen,
payment, reassign-arn, registration, returns, router, state-actions,
state-jurisd-admin, tp-jurisdiction-update, transfer-of-charge, utils, welcome-letter

---

# 4. FEATURES BUILT

## 4A. AppealCaseService — Recursive Case Graph Traversal & Compliance Rule Engine

**File:** `appealcasemgmtctrl.js`

**What it does:**
- Traverses a case hierarchy graph: starting from a case refId → fetches case items → for each item fetches ARN details → which may trigger more refId lookups (mutual recursion between `getCaseItemDetails` and `getItemDetailsFromARN`)
- Session-scoped `Set`-based deduplication prevents infinite loops and redundant API calls
- 10+ condition compliance rule engine in `checkAndShowWarningPopups` evaluates waiver status, 4-month statutory windows, order lifecycle states, and module context (APLTD / APPEL / APPEL+MFY) before surfacing contextual warnings
- Dynamic AngularJS `$compile` + Bootstrap modal pipeline with graceful fallback to `alert()`

**Technical patterns:**
- Mutual recursion (graph traversal)
- ES6 `Set` for O(1) idempotency check
- Composite key design: `sessionId + scopeId + refId`
- Soft-failure async (resolve-not-reject) for resilience
- `Promise.all` for parallel sub-operations
- Closure-scoped singleton state in AngularJS service

---

## 4B. Appeal Assignment Controller

**File:** `appealAssignmentCtrl.js` (~968 LOC)

**What it does:**
- Role-based case distribution to adjudicating officers
- LocalStorage-based role caching (`appellateAuthorityRole`, `assitantToAppellateRole`)
- ShareData service for cross-component communication
- State-aware UI rendering based on case status
- NgTable pagination for assignment history

---

## 4C. Appeal Order Controllers — Simultaneous & Combined Orders

**Files:** `appealorderctrl.js` (16,090 LOC), `appealorderctrltd.js` (13,191 LOC)

**What it does:**
- End-to-end order creation, processing, and adjudication
- Simultaneous proceedings: `$scope.simulAppeals` array tracks related appeals
- Combined orders: `$scope.isSimulCombinedOrd` flag, dispute amount propagation across cases
- Counter appeal tracking: `latestApltdCase` vs `latestAppelCase`
- Separate TD (Tax Department) variant with its own business rules

---

## 4D. Enable/Disable Access Role (gstn-apps micro-library)

**Location:** `gstn-apps/libs/back-office/enable-disable-access-role/` (21 TypeScript files)

**What it does:**
- Angular micro-library for RBAC management
- Smart/dumb component separation
- RxJS `BehaviorSubject` for state management
- ExcelJS-based styled Excel export of role access data
- Audit trail via `getCaseFldrItemAccessHist()` API

---

## 4E. BO Revamp Dashboard Counters

**Location:** `BO-Revamp/` Angular application

**What it does:**
- Real-time case volume metric components for appeal queues
- `AppealEffectService` — BehaviorSubject singleton with `isDataLoaded` guard to prevent duplicate API calls
- `CacheService` — simple getter/setter cache for appeal effect counts

---

# 5. RESUME BULLETS

## Primary Bullets (use these)

- **Engineered a recursive async case-graph traversal engine** for India's national GST dispute-management portal, using mutual recursion across appeal-reference and case-item lookup APIs with session-scoped `Set`-based deduplication — eliminating redundant API calls, preventing infinite loops in deeply nested appeal chains, and ensuring idempotent execution per officer session.

- **Designed a multi-condition compliance rule engine** with 10+ branching decision paths that evaluates active waiver applications, statutory 4-month time windows, and order lifecycle states (pending / approved / voided / withdrawn) across single-year and multi-year tax demand scenarios, surfacing real-time contextual warnings to adjudicating officers before they issue adjudication orders.

- **Built end-to-end appeal order processing workflows** — covering assignment, order creation, simultaneous orders, and combined orders — with a dedicated AngularJS service layer that decoupled business-rule evaluation from controller logic, reducing duplication across four controller files and improving maintainability.

- **Implemented UI-level role-based access control** across appeal management modules in a national-scale government portal, dynamically enabling and disabling officer actions based on assigned roles — enforcing least-privilege access for thousands of daily users.

- **Delivered real-time dashboard counter components** as part of a back-office revamp, providing tax administrators with live case-volume metrics across appeal queues — improving situational awareness and workload distribution visibility.

- **Architected a resilient async modal orchestration pipeline** by chaining AngularJS `$compile`, Bootstrap modal initialization, and DOM-readiness verification with progressive fallback to native browser alerts — ensuring officers always receive statutory compliance warnings regardless of UI framework state.

## Migration / Architecture Bullet (once you can speak to it)

- **Contributed to incremental migration of a 77,000+ LOC AngularJS application to Angular** by building new features as standalone TypeScript micro-libraries in a monorepo (21 libraries), enabling adoption without a full rewrite and ensuring reusability across 5+ back-office application modules.

## Additional Bullets (from codebase exploration)

- **Implemented an Angular HTTP interceptor** applying the Chain of Responsibility pattern to centralize auth token injection, content-type negotiation, and error response normalization — eliminating per-service boilerplate across 21 micro-library modules.

- **Built an enterprise Excel report export** for role-access audit data using ExcelJS, generating dynamically styled multi-row workbooks from live API data — replacing manual audit processes for compliance administrators.

---

# 6. POWER BULLETS

## Standard Power Bullet (single sentence, space-limited resume)

> Architected a recursive, session-idempotent appeal-case validation system for India's GST portal — implementing a graph-traversal engine with `Set`-based cycle detection, a 10+ condition statutory rule engine enforcing time-window and waiver-scheme constraints, dynamic AngularJS modal compilation, and role-based access control across the full appeal lifecycle from assignment through adjudication.

## Extended Power Bullet (after learning the roadmap topics)

> Architected and delivered a recursive appeal-case validation engine, a 10-state compliance FSM with guarded transitions, simultaneous-order state propagation, and an RBAC micro-library with reactive state management — across a 77K-LOC AngularJS-to-Angular incremental migration serving India's national GST portal with millions of registered taxpayers.

## Migration Power Bullet

> Drove incremental migration of a 77K+ LOC AngularJS government portal to Angular by extracting cross-cutting features into 21 independently versioned TypeScript micro-libraries — applying reactive state management (RxJS BehaviorSubject), HTTP interceptor-based auth injection, and finite-state-machine-modeled business rules, reducing per-feature code duplication by consolidating logic previously scattered across 4 controllers.

---

# 7. INTERVIEW TALKING POINTS

## On the Recursive Traversal (Graph Traversal + Deduplication)

- `getCaseItemDetails` and `getItemDetailsFromARN` call each other — mutual recursion on a real case graph
- Infinite loop risk: a case item references an ARN, that ARN contains a case item that references back
- **Fix:** composite key `sessionId + scopeId + refId` stored in `Set`. O(1) lookup before every API call
- **Why `scopeId`?** Multiple cases can be open in the same Angular singleton service session — without it, Case A's refId would skip lookup when Case B has the same refId
- **Why new `sessionId` on `resetState()`?** The service is a singleton. Without a new session token, the Set from the previous case would still be populated and would incorrectly short-circuit lookups for the next case

## On the Rule Engine (State Machine Thinking)

- `checkAndShowWarningPopups` is an informal finite state machine with ~10 states
- **APLTD module:** uses `if/else if` — first match wins, mutually exclusive conditions
- **APPEL module:** uses sequential `if/if/if` — last match overwrites `dialogueMessage`. This is intentional: multiple conditions can be simultaneously true (pending appeal AND waiver filed), and the last one is the most critical
- Be ready to critique: this sequential overwrite is fragile — a proper priority queue or state machine with explicit priority would be more maintainable at scale
- **Time-window enforcement:** 4-month statutory lockout computed with `moment.diff(date, 'months', true)` — the `true` param gives fractional months, so 3.9 months correctly evaluates as not-yet-4

## On Session-Based vs Global State

- A simple boolean `isProcessing = true` breaks when an officer opens Case B while Case A's async chain is still resolving
- The service is a closure-scoped singleton — state persists for the lifetime of the app
- `resetState()` is the only safe boundary — it clears all Sets AND generates a new sessionId
- Real-world consequence: without this, an officer reviewing a second appeal after a first would see stale waiver/order flags from the previous case, potentially leading to incorrect compliance warnings

## On Simultaneous / Combined Orders

- Two appeals on the same underlying demand can be in "simultaneous proceedings" — a legal status where both must be resolved together
- `simulAppeals` array holds all related cases; dispute amounts are propagated across them
- Counter appeals: department files APL-03 against the taxpayer's APL-01 on the same demand — both must be adjudicated in one order. `latestApltdCase` vs `latestAppelCase` tracks which side the logged-in officer represents

## On BehaviorSubject + isDataLoaded Guard (Reactive State)

"I used a BehaviorSubject to share appeal count state across components without prop-drilling or repeated API calls. The `isDataLoaded` flag acts as a memoization guard — once loaded, any new subscriber gets the cached value immediately."

---

# 8. ADDITIONAL RESUME SIGNALS

## HTTP Interceptor — Cross-cutting Auth & Error Handling
**File:** `http-error.interceptor.ts` (59 LOC)

Implements the **Chain of Responsibility** pattern at the transport layer:
- Injects auth token into every outgoing request
- Negotiates Content-Type (skips for file uploads)
- Integrates BlockUI for loading state
- Normalizes error responses centrally

## ExcelJS Report Generation
**File:** `enable-disable-access-role` library

Dynamic styled Excel export for role access audit reports. Enterprise reporting, dynamic cell styling, date formatting.

## BehaviorSubject + isDataLoaded Guard (Reactive State)
**File:** `AppealEffectService.ts`

Singleton observable service with a boolean guard preventing duplicate HTTP calls — the Angular equivalent of a memoized selector.

---

# 9. ARCHITECTURE PATTERNS QUICK REFERENCE

| Pattern | Where in Codebase | Interview Term |
|---|---|---|
| Mutual recursion (graph traversal) | getCaseItemDetails ↔ getItemDetailsFromARN | DFS on a directed graph |
| Session-scoped deduplication | processingState Set with composite key | Memoization / idempotency key |
| Compliance rule evaluation | checkAndShowWarningPopups | Finite State Machine / Decision Table |
| Cross-cutting auth injection | http-error.interceptor.ts | Chain of Responsibility |
| Singleton observable with guard | AppealEffectService BehaviorSubject | Reactive singleton / memoized selector |
| Micro-library extraction | gstn-apps 21 libraries | Monorepo + micro-frontend |
| AngularJS → Angular bridge | gstn-apps downgrade pattern | Incremental migration / strangler fig |
| Multi-case state propagation | simulAppeals + dispute amount sync | Distributed state synchronization |
| Progressive fallback | $compile → Bootstrap modal → alert() | Graceful degradation |
| Soft-failure async | resolve() instead of reject() in catch | Fault-tolerant orchestration |

---

# 10. SELF-STUDY ROADMAP

*Ranked by ROI — things to learn from YOUR OWN codebase that will be impressive in interviews*

## 1. RxJS Reactive Programming — HIGHEST ROI

You already use `BehaviorSubject` in the codebase. Deepen to:
- `Subject` vs `BehaviorSubject` vs `ReplaySubject` — when each is appropriate
- `switchMap` vs `mergeMap` vs `exhaustMap` vs `concatMap` — classic interview trap, each has a distinct cancellation behavior
- `combineLatest` vs `forkJoin` — parallel vs sequential stream combination
- The `isDataLoaded` guard you use is a manual memoization — learn how `shareReplay(1)` does this automatically

**Why it matters:** Every Angular SDE-2 interview asks at least one RxJS operator question. Knowing the cancellation semantics of `switchMap` alone puts you ahead of 70% of candidates.

## 2. Finite State Machine (FSM) Vocabulary — MEDIUM ROI, HIGH IMPRESSION

Your `checkAndShowWarningPopups` is an FSM. Learn to:
- Draw a state transition diagram for it (states: waiver_pending, spl07_issued, appeal_filed, order_issued, void_issued...)
- Know the vocabulary: states, transitions, guards, actions
- Reference XState (JavaScript FSM library) — even just knowing it exists signals seniority

**Why it matters:** Saying "I modeled this as a finite state machine with 8 states and 12 guarded transitions" sounds dramatically more senior than "I had a lot of if/else conditions." The underlying code is the same.

## 3. HTTP Interceptor + Chain of Responsibility Pattern — LOW EFFORT, HIGH VALUE

Read `http-error.interceptor.ts` end to end (59 lines). Understand:
- Why auth token injection belongs at the transport layer, not per-service
- How Angular's `HttpInterceptor` interface implements Chain of Responsibility
- The difference between request interceptors and response interceptors

**Why it matters:** A common SDE-2 design question is "how would you add auth headers to all API calls?" The interceptor answer signals you think in cross-cutting concerns, not copy-paste.

## 4. AngularJS $q vs Native Promise — Bridges the Legacy/Modern Gap

Your `createAjaxGetPromise` wraps a native Promise in `$q.defer()`. Understand exactly why:
- AngularJS's digest cycle is the UI update mechanism — it doesn't know about native `Promise` resolution
- When a native Promise resolves outside a digest cycle, the UI doesn't update
- `$q` hooks into the digest cycle, so `$q.defer().resolve()` triggers a UI refresh
- This is why AngularJS code that uses `Promise.all` sometimes needs an explicit `scope.$apply()` call afterward

**Why it matters:** Understanding framework internals (digest cycle, zone.js in Angular) separates engineers who use a framework from engineers who understand it.

## 5. Monorepo + Micro-library Architecture — MEDIUM EFFORT, STRONG SIGNAL

The `gstn-apps` structure is an Nx-style monorepo with 21 publishable libraries. Learn:
- What a monorepo is and why it's used (single source of truth, atomic cross-library changes)
- `nx affected` — only build/test what changed (key selling point)
- Difference between `publishable`, `buildable`, and `regular` libraries in Nx
- How `downgradeComponent` / `downgradeInjectable` bridges Angular libraries into AngularJS hosts

**Why it matters:** Most product companies at scale (Google, Meta, Shopify) run monorepos. Being able to say "I contributed to a 21-library monorepo with incremental migration from AngularJS to Angular" is a strong SDE-3 signal.

---

# 11. DSA

## How Senior Interviews Differ

At SDE-2/SDE-3 level, interviewers are not checking if you can code.
They are checking:
- Can you **design** something at scale without being told what to do?
- Can you **justify** your decisions with tradeoffs?
- Can you **see failure modes** before they happen?
- Do you think about **maintainability**, not just correctness?

For every answer: **What → Why → Tradeoffs → What I'd do differently at scale.**

## Core Patterns to Master (in this order)

### 1. Hashing & Two Pointers
- HashMap internals (collision, load factor, rehash)
- Two-pointer on sorted arrays
- Sliding window (fixed and variable size)
- Frequency count problems

**Hands-on:** LeetCode #1, #3, #11, #15, #42, #76, #567

### 2. Recursion & Backtracking
- This is directly relevant — you built a recursive graph traversal
- Understand the call stack, base case, recurrence relation
- Subsets, permutations, N-Queens, Sudoku solver

**Hands-on:** LeetCode #46, #78, #79, #131, #39

### 3. Trees
- BFS (level order) and DFS (pre/in/post)
- Lowest Common Ancestor
- Binary Search Tree operations
- Diameter, height, path sum

**Hands-on:** LeetCode #102, #104, #112, #236, #543, #98

### 4. Graphs — HIGH PRIORITY (you already built one)
Your `getCaseItemDetails ↔ getItemDetailsFromARN` is literally DFS on a directed graph with cycle detection.
Learn the formal vocabulary:
- BFS, DFS (iterative and recursive)
- Cycle detection (visited + recursion stack)
- Topological sort (Kahn's algorithm)
- Connected components
- Dijkstra (shortest path)
- Union-Find (disjoint sets)

**Hands-on:** LeetCode #200, #207, #210, #417, #743, #547, #684

### 5. Dynamic Programming
- Start with memoization (top-down recursion + cache) — easier to reason about
- Then tabulation (bottom-up)
- Patterns: 0/1 knapsack, longest common subsequence, coin change, edit distance

**Hands-on:** LeetCode #70, #322, #1143, #300, #416, #72

### 6. Heaps & Priority Queues
- Min-heap, max-heap
- Top-K problems
- Merge K sorted lists

**Hands-on:** LeetCode #347, #23, #295, #378

### 7. Binary Search
- Not just on sorted arrays — on the answer space
- Search in rotated array, find peak, capacity problems

**Hands-on:** LeetCode #33, #153, #162, #875, #1011

## Senior DSA Interview Expectations
- Write clean, compilable code (not pseudocode)
- State time and space complexity upfront — don't wait to be asked
- Mention edge cases before coding: empty input, single element, negative numbers, overflow
- If brute force is O(n²), say "brute force is X, but we can do better with Y"
- Say "let me walk through this with a small example" before coding

## Minimum LeetCode Target
- Easy: fluent (under 5 minutes)
- Medium: consistent (20-30 minutes)
- Hard: attempt + explain approach (you don't need to fully solve)
- Total: ~100-150 mediums across the patterns above

---

# 12. JAVA DEEP DIVE

## 12A. JVM Internals

### Memory Model
- Heap: Young Generation (Eden + Survivor S0/S1) + Old Generation (Tenured) + Metaspace
- Stack: per-thread, stores stack frames (local vars + method calls)
- Minor GC (young gen) vs Major/Full GC (old gen + metaspace)

**Interview question:** "What is a memory leak in Java, and how would you detect one?"
**Answer:** Objects referenced but never used (listener not deregistered, static collections growing). Detect with heap dump + VisualVM or jmap.

### Garbage Collection
- Mark and Sweep → Mark Compact → Generational GC
- GC algorithms: Serial, Parallel, G1 (default Java 9+), ZGC (Java 15+, low latency)
- Stop-the-world pauses — why they happen and how G1 minimizes them

**Hands-on:** Run a Java app with `-verbose:gc` and read the output.

### Class Loading
- Bootstrap → Extension → Application classloader (parent delegation model)
- Why this prevents duplicate class definitions
- Hot reloading in frameworks (Spring DevTools) — how it breaks parent delegation

## 12B. Concurrency — CRITICAL TOPIC

### Core Concepts
- `Thread`, `Runnable`, `Callable`, `Future`
- `synchronized` keyword: method-level vs block-level, intrinsic lock
- `volatile`: visibility guarantee (no CPU cache), not atomicity
- `AtomicInteger`, `AtomicReference` — CAS (Compare-And-Swap) operations
- Happens-before relationship in Java Memory Model

### java.util.concurrent Package
- `ReentrantLock` vs `synchronized`: tryLock(), fairness, interruptible
- `ReadWriteLock`: multiple readers, exclusive writer
- `CountDownLatch`: wait for N events (one-time)
- `CyclicBarrier`: N threads wait for each other (reusable)
- `Semaphore`: limit concurrent access to a resource
- `BlockingQueue`: `LinkedBlockingQueue`, `ArrayBlockingQueue`, `PriorityBlockingQueue`

### ExecutorService & Thread Pools
- `newFixedThreadPool`, `newCachedThreadPool`, `newSingleThreadExecutor`
- `ThreadPoolExecutor` params: corePoolSize, maxPoolSize, keepAliveTime, workQueue, RejectedExecutionHandler
- When does a thread pool reject tasks? Queue full + maxPoolSize reached
- `CompletableFuture`: thenApply, thenCompose, thenCombine, exceptionally, allOf, anyOf
- `CompletableFuture` vs `Future`: non-blocking, chainable, callback-based

**Interview question:** "Design a rate limiter using Java concurrency primitives."
**Answer:** `Semaphore` with a fixed number of permits. Acquire permit → process request → release. For sliding window, use `ScheduledExecutorService` to refill permits.

### Common Concurrency Bugs
- Race condition: two threads read-modify-write without sync
- Deadlock: two threads hold lock A/B and wait for B/A — draw the cycle
- Livelock: threads keep responding to each other without making progress
- Thread starvation: low-priority thread never gets CPU

**Hands-on:** Write a thread-safe bounded blocking queue from scratch using `ReentrantLock` + `Condition`.

## 12C. Collections Internals

### HashMap
- Array of buckets, each bucket is a linked list (Java 8+: treeified to red-black tree when bucket size > 8)
- `hashCode()` → index calculation: `(n-1) & hash`
- Collision resolution: chaining
- Load factor default 0.75, resize at 75% capacity → doubles bucket array, rehashes all entries
- Why default capacity is 16 (power of 2): bitwise AND is faster than modulo

**Interview question:** "Two objects are equal (`equals()` returns true). What must be true about their `hashCode()`?"
**Answer:** Must return the same value. The reverse is not required (hash collision is allowed).

### ConcurrentHashMap
- Java 7: segment locks (16 segments by default)
- Java 8+: bucket-level locking using `synchronized` on first node + CAS for empty buckets
- `computeIfAbsent`, `merge`, `forEach` — thread-safe atomic operations
- Does NOT allow null keys or values (unlike HashMap)

### Other Collections
- **LinkedHashMap**: insertion-order iteration, used for LRU cache
- **TreeMap**: sorted by key, Red-Black tree, O(log n) operations
- **PriorityQueue**: min-heap, O(log n) offer/poll

## 12D. Java 8+ Features

- **Lambda:** `(a, b) -> a + b` — syntactic sugar for functional interface
- **Stream API:** `filter`, `map`, `flatMap`, `reduce`, `collect`, `groupingBy`, `partitioningBy`
- **Optional:** avoid null checks, use `map`, `flatMap`, `orElse`, `orElseThrow`
- **Method references:** `String::valueOf`, `list::add`
- **Functional interfaces:** `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T,U,R>`
- **Default methods in interfaces:** allows interface evolution without breaking implementations
- **CompletableFuture:** async programming (covered above)

**Hands-on:** Given a list of employees, group by department, find the highest-paid employee per department, return as `Map<String, Employee>` — write it with streams.

## 12E. Spring Boot Internals

- **Auto-configuration:** `@SpringBootApplication` triggers `@EnableAutoConfiguration` which scans `spring.factories` for `@Configuration` classes
- **Bean lifecycle:** instantiation → dependency injection → `@PostConstruct` → use → `@PreDestroy`
- **`@Transactional`:** proxied via AOP, only works on public methods, self-invocation bypasses proxy
- **`@Async`:** creates a new thread from a `TaskExecutor` — doesn't work in same class (AOP proxy)
- **AOP:** `@Around`, `@Before`, `@After` — used for logging, transactions, security
- **Bean scopes:** Singleton (default), Prototype, Request, Session

**Interview question:** "Why doesn't `@Transactional` work when you call one method from another in the same class?"
**Answer:** Spring's transaction management uses a JDK proxy or CGLIB proxy. When you call `this.method()`, you're bypassing the proxy, so the transaction advice never fires.

---

# 13. SYSTEM DESIGN (HLD)

*Most important phase for SDE-2/SDE-3. Every senior loop has at least one system design round.*

## The Framework (use this every time)

1. **Clarify requirements** (5 min): functional requirements, non-functional (scale, latency, availability), out of scope
2. **Estimate scale** (3 min): DAU, QPS, storage, bandwidth
3. **High-level design** (10 min): draw boxes — client, API gateway, services, DB, cache, queue
4. **Deep dive** (20 min): the interviewer will ask you to go deep on one component
5. **Tradeoffs** (5 min): what did you sacrifice and why?

## Non-Functional Concepts You Must Know Cold

### CAP Theorem
- Consistency, Availability, Partition Tolerance — pick 2 when network partition occurs
- CP systems: ZooKeeper, HBase (consistent but may be unavailable during partition)
- AP systems: Cassandra, DynamoDB (available but may return stale data)
- Most real systems choose between CP and AP — know which your database is

### Caching
- Cache-aside (lazy loading): app checks cache, on miss loads from DB, populates cache
- Write-through: write to cache and DB together (consistent, slower writes)
- Write-behind (write-back): write to cache, async flush to DB (fast writes, risk of data loss)
- Eviction policies: LRU (most common), LFU, TTL-based
- Cache stampede: many requests hit DB simultaneously on cold cache — solution: mutex lock or probabilistic early expiration
- Tools: Redis (with persistence), Memcached (pure cache)

### Database Scaling
- Read replica: async replication, serve reads from replica, writes to primary
- Sharding (horizontal partitioning): split rows across multiple DB instances by shard key
  - Range sharding: user IDs 1-1M on shard 1 (hotspot risk)
  - Hash sharding: `hash(userId) % N` (even distribution, hard to range query)
  - Directory sharding: lookup table maps key to shard (flexible, lookup overhead)
- Connection pooling: reuse DB connections (HikariCP in Spring Boot)

### Message Queues
- Use cases: async processing, decoupling producers and consumers, backpressure, retry
- Kafka: log-based, ordered per partition, consumer groups, replay, high throughput
- RabbitMQ: message broker, push model, routing via exchanges, good for task queues
- At-least-once vs exactly-once delivery — idempotency is the consumer's responsibility
- Dead letter queue: messages that fail N times go here for inspection

### Load Balancing
- Layer 4 (transport): route by IP/port — fast, no content inspection
- Layer 7 (application): route by URL, headers, cookies — smarter, used for A/B testing
- Algorithms: round robin, weighted round robin, least connections, consistent hashing
- Consistent hashing: when a node is added/removed, only K/n keys remap (K = keys, n = nodes)
  - Used by: Cassandra, DynamoDB, CDNs, Redis Cluster

### API Design
- REST principles: stateless, resource-based URIs, HTTP verbs (GET/POST/PUT/PATCH/DELETE)
- Idempotency: GET, PUT, DELETE are idempotent. POST is not.
- Pagination: cursor-based (stable, scalable) vs offset-based (simple, unstable under inserts)
- Rate limiting: token bucket (allows burst), leaky bucket (smooth), sliding window
- Versioning: URL versioning (`/v1/`), header versioning, content negotiation

### Distributed System Concepts
- Eventual consistency vs strong consistency
- Two-phase commit (2PC): coordinator + participants, blocking protocol
- Saga pattern: distributed transactions via compensating transactions (preferred in microservices)
- Idempotency keys: client sends unique key, server deduplicates retries
- Circuit breaker: after N failures, open circuit (fail fast), then half-open to test recovery
- Retry with exponential backoff + jitter: avoids thundering herd on retry storms

## Must-Practice System Design Questions

| Question | Key Concepts Tested |
|---|---|
| Design URL Shortener (bit.ly) | Hashing, DB choice, caching, 302 redirect |
| Design Rate Limiter | Token bucket, Redis, distributed rate limit |
| Design Notification System | Message queue, fan-out, push vs pull |
| Design Search Autocomplete | Trie, caching, ranking |
| Design Twitter Feed | Fan-out on write vs read, timeline generation |
| Design Payment System | Idempotency, ACID, distributed transactions, saga |
| Design File Storage (S3) | Chunking, metadata DB, object storage |
| Design WhatsApp/Chat | WebSocket, message ordering, offline delivery |
| Design Job Scheduler (like cron) | Distributed lock, at-least-once delivery, priority queue |
| Design API Gateway | Auth, rate limiting, routing, circuit breaker |

**Your Advantage:** You can map GSTN to system design. The appeal validation service you built IS a distributed workflow engine — talk about it in terms of CAP, idempotency, and state management.

---

# 14. LOW-LEVEL DESIGN (LLD)

*LLD round: design a class structure for a real-world system in 45 minutes.*

## SOLID Principles

- **S — Single Responsibility:** A class should have one reason to change.
  Your `AppealCaseService` partially violates this — it handles traversal, deduplication, AND modal display. In an LLD interview, split these.
- **O — Open/Closed:** Open for extension, closed for modification.
  Use strategy pattern instead of if/else chains.
- **L — Liskov Substitution:** Subtypes must be substitutable for their base types.
  A `Square` that extends `Rectangle` and overrides `setWidth` to also set `setHeight` violates this.
- **I — Interface Segregation:** Don't force clients to implement methods they don't use.
  Fat interfaces → split into role-specific interfaces.
- **D — Dependency Inversion:** Depend on abstractions, not concretions.
  Inject `PaymentGateway` interface, not `RazorpayClient` directly.

## Design Patterns You Must Know Cold

### Creational
- **Singleton:** one instance per JVM. Thread-safe: double-checked locking with `volatile`, or enum singleton.
- **Factory Method:** subclass decides which object to create. Used in: JDBC DriverManager, Spring BeanFactory.
- **Abstract Factory:** family of related objects. Used in: UI toolkit (Windows vs Mac widgets).
- **Builder:** construct complex objects step by step. Used in: `StringBuilder`, Lombok `@Builder`.

### Structural
- **Decorator:** add behavior without subclassing. Used in: Java I/O streams (`BufferedReader` wraps `FileReader`).
- **Adapter:** convert one interface to another. Used in: `Arrays.asList()` wrapping array in List.
- **Proxy:** control access to an object. Used in: Spring AOP `@Transactional`, JDK dynamic proxy.
- **Facade:** simplify a complex subsystem. Your `AppealCaseService.processAppealData()` IS a facade.
- **Composite:** tree structure of uniform objects. Used in: file system (file and directory both implement Component).

### Behavioral
- **Strategy:** encapsulate algorithms, swap at runtime. Instead of if/else on `moduleName`, inject `AppelStrategy` or `ApltdStrategy`.
- **Observer:** subject notifies observers on change. Used in: AngularJS `$watch`, RxJS Observable.
- **State:** object changes behavior when state changes. Your rule engine IS a state machine.
- **Chain of Responsibility:** pass request along a chain. Used in: HTTP Interceptors, servlet filters.
- **Command:** encapsulate a request as an object. Used in: undo/redo systems, job queues.
- **Template Method:** define skeleton, subclasses fill in steps. Used in: Spring's `JdbcTemplate`.
- **Iterator:** traverse collection without exposing structure. Used in: Java `Iterator`.

## Must-Practice LLD Questions

| Question | Key Patterns |
|---|---|
| Design a Parking Lot | Strategy (pricing), State (slot), Factory (vehicle type) |
| Design an ATM | State machine (card inserted → PIN → transaction) |
| Design a Library Management System | Repository pattern, Observer (due date alert) |
| Design a Ride-Sharing App (Uber basic) | Strategy (matching), Observer (driver location update) |
| Design a Chess Game | Composite, State, Template Method |
| Design a Rate Limiter (class level) | Strategy (algorithm), Singleton (per endpoint instance) |
| Design a Notification Service | Strategy (SMS/Email/Push), Factory, Observer |
| Design a Vending Machine | State machine |
| Design a Logger Framework | Singleton, Chain of Responsibility, Observer |
| Design an In-Memory Cache (LRU) | LinkedHashMap or HashMap + DoublyLinkedList |

**Hands-on for LRU Cache:**
```java
class LRUCache {
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final DoublyLinkedList list = new DoublyLinkedList();

    public int get(int key) { ... }     // O(1)
    public void put(int key, int val) { ... }  // O(1)
}
```
This question appears in almost every senior Java interview. Know it by heart.

---

# 15. FRONTEND (Angular + RxJS)

## 15A. RxJS — The Most Important Frontend Topic

### The 4 Subjects
- `Subject`: no initial value, only future emissions
- `BehaviorSubject`: stores last value, new subscribers get it immediately — **you use this in AppealEffectService**
- `ReplaySubject(n)`: replays last n values to new subscribers
- `AsyncSubject`: only emits the last value, and only on completion

### The Operator Trap — switchMap vs mergeMap vs concatMap vs exhaustMap

| Operator | When new emission arrives while inner is active | Use case |
|---|---|---|
| `switchMap` | **Cancels** the previous inner observable | Search autocomplete (cancel previous search) |
| `mergeMap` | Runs **both** concurrently | Parallel HTTP requests |
| `concatMap` | **Queues** — waits for previous to complete | Sequential operations (upload files one by one) |
| `exhaustMap` | **Ignores** new emissions while inner is active | Submit button (ignore double-clicks) |

**Interview question:** "A user types in a search box. Each keystroke fires an API call. How do you prevent stale results?"
**Answer:** `switchMap` — when a new keystroke arrives, it cancels the in-flight request.

**Interview question:** "A user clicks Submit. You fire an API call. If they click again before response, what do you do?"
**Answer:** `exhaustMap` — ignore subsequent clicks until the first request completes.

### Common Operators
- `map`: transform value
- `filter`: pass through conditionally
- `tap`: side effect without transformation (logging)
- `catchError`: handle error, return fallback observable
- `retry(n)`: resubscribe on error, N times
- `debounceTime(ms)`: wait for silence before emitting (search input)
- `distinctUntilChanged`: skip duplicate consecutive values
- `takeUntil(subject$)`: unsubscribe when another observable emits (component destroy)
- `combineLatest([a$, b$])`: emit when ANY source emits, with latest from all
- `forkJoin([a$, b$])`: emit once when ALL sources complete (like Promise.all)
- `shareReplay(1)`: multicast + cache last value for late subscribers (replaces your manual `isDataLoaded` flag)

**Hands-on:** Build a search box with debounceTime → distinctUntilChanged → switchMap → catchError → startWith

## 15B. Angular Change Detection

- Default: checks entire component tree on every event/timer/HTTP response
- `OnPush`: only checks when `@Input` reference changes or `async` pipe resolves
- `markForCheck()`: manually tell Angular to check an OnPush component
- `detectChanges()`: run CD for this component and children right now
- Zone.js: patches browser APIs (setTimeout, fetch, DOM events) to trigger CD
- `NgZone.runOutsideAngular()`: run code without triggering CD (e.g., animation frames)

**Interview question:** "Your Angular app is slow. How do you diagnose and fix performance?"
**Answer:** Enable OnPush strategy on all leaf components. Use trackBy in ngFor. Use async pipe instead of manual subscriptions. Profile with Chrome DevTools → Performance tab.

## 15C. Angular Lifecycle Hooks

Order: `constructor` → `ngOnChanges` → `ngOnInit` → `ngDoCheck` → `ngAfterContentInit` → `ngAfterContentChecked` → `ngAfterViewInit` → `ngAfterViewChecked` → `ngOnDestroy`

Key ones:
- `ngOnInit`: safe to call services/HTTP (view not yet rendered)
- `ngAfterViewInit`: safe to access `@ViewChild` (DOM is ready)
- `ngOnChanges`: fires when `@Input` changes (receives `SimpleChanges`)
- `ngOnDestroy`: unsubscribe all observables here (memory leak prevention)

## 15D. AngularJS Internals (your current codebase)

- **Digest cycle:** `$scope.$apply()` triggers `$digest()` which runs all watchers (`$watch`) until the model stabilizes (dirty checking loop, max 10 iterations)
- **$q vs native Promise:** `$q` resolves inside the digest cycle → triggers UI update automatically. Native Promise resolves outside → need `$scope.$apply()` manually. **This is exactly why your code has `if (scope.$apply && !scope.$$phase) { scope.$apply(); }`**
- **`$$phase`:** prevents `$apply already in progress` error
- **Dependency injection:** `$inject` array or minification-safe array syntax `['dep1', 'dep2', fn]`
- **Services vs Factories vs Providers:** all singletons. Service: instantiated with `new`. Factory: returns an object. Provider: configurable before bootstrap.

## 15E. Performance Optimization

- Lazy loading: `loadChildren: () => import(...)` in routing
- `trackBy` in `*ngFor`: prevents full DOM re-render when list changes
- Preloading strategy: `PreloadAllModules` or custom
- Bundle analysis: `ng build --stats-json` + webpack-bundle-analyzer
- Tree shaking: unused exports removed by Webpack
- AOT compilation (default in prod): templates compiled at build time, not runtime

---

# 16. DATABASES

## 16A. SQL Internals

### Indexes
- B-Tree index (default): balanced tree, O(log n) lookup, supports range queries and ORDER BY
- Hash index: O(1) exact lookup, no range queries
- Composite index: index on (col_a, col_b) — usable for col_a alone, or col_a + col_b. Not col_b alone. (Leftmost prefix rule)
- Covering index: index contains all columns the query needs — no table row fetch needed
- When NOT to index: high write frequency tables, low cardinality columns (boolean), small tables

### Transactions & ACID
- Atomicity: all or nothing
- Consistency: DB constraints always hold
- Isolation: concurrent transactions don't interfere
- Durability: committed data survives crashes (WAL — Write Ahead Log)

### Isolation Levels (from weakest to strongest)
- Read Uncommitted: sees uncommitted data (dirty reads)
- Read Committed (PostgreSQL default): sees only committed data
- Repeatable Read (MySQL InnoDB default): same row returns same value within transaction
- Serializable: full isolation, transactions appear sequential (slowest)

### Locking
- Shared lock (S): multiple readers allowed, no writers
- Exclusive lock (X): one writer, no readers
- Optimistic locking: no lock taken, check version on write (good for low contention)
- Pessimistic locking: `SELECT ... FOR UPDATE` (good for high contention, like inventory)
- Deadlock: DB detects cycle and kills one transaction

## 16B. NoSQL

### When to use NoSQL over SQL
- Schema flexibility (document DB: MongoDB)
- Massive scale with simple access patterns (key-value: Redis, DynamoDB)
- Time-series or IoT (InfluxDB, Cassandra)
- Graph relationships (Neo4j)
- NOT for: complex joins, strong ACID transactions across multiple entities

### MongoDB
- Document store: BSON documents in collections
- `_id` is indexed by default
- Aggregation pipeline: `$match`, `$group`, `$project`, `$sort`, `$lookup` (join)
- When to embed vs reference: embed for data always queried together (1:few), reference for 1:many or frequently updated subdocs

### Redis
- In-memory key-value store with persistence options (RDB snapshots, AOF log)
- Data types: String, List, Set, Sorted Set (ZSet), Hash, Stream
- Use cases: session cache, rate limiting (INCR + EXPIRE), leaderboard (ZSet), pub/sub, distributed lock (SETNX)
- Distributed lock: `SET key value NX PX 30000` — Redlock for multi-node

### Cassandra
- Wide-column store, AP system (available + partition tolerant)
- Design around queries, not entities — partition key determines physical location
- Replication factor + consistency level: `QUORUM` = majority of replicas must agree
- No JOINs, no foreign keys, no transactions across partitions

---

# 17. YOUR CODEBASE MAPPED

*Things you've already built → formal interview vocabulary*

### Graph Traversal (DFS with cycle detection)
**What you built:** `getCaseItemDetails ↔ getItemDetailsFromARN` mutual recursion with Set-based deduplication
**Formal name:** Depth-First Search on a directed graph with visited-set cycle detection
**Interview question:** "How would you detect a cycle in a directed graph?"
**Your answer:** Use DFS with two sets — `visited` (permanently done) and `recursionStack` (currently in path). Your `processedRefIds` Set serves the same purpose.

### Idempotency
**What you built:** Session-scoped composite keys prevent duplicate processing
**Formal name:** Idempotent operations via idempotency keys
**Interview question:** "How do you make an API call idempotent?"
**Your answer:** Client includes a unique idempotency key per logical request. Server stores key + result. On retry, return stored result. Your `sessionId + scopeId + refId` is exactly this pattern.

### Finite State Machine
**What you built:** `checkAndShowWarningPopups` with 10+ conditions across 3 modules
**Formal name:** Finite State Machine (FSM) / State Pattern
**Interview question:** "How would you model a complex workflow with many states?"
**Your answer:** Define states as an enum, transitions as a map of (state, event) → (newState, action). Each state has defined valid transitions.

### Circuit Breaker (soft version)
**What you built:** `processingState.isProcessing` flag + queue with setTimeout retry
**Formal name:** Basic circuit breaker / backpressure mechanism
**Real circuit breaker:** Closed (normal) → Open (too many failures, fail fast) → Half-Open (test one request) → Closed. Libraries: Resilience4j (Java).

### Reactive Singleton with Guard
**What you built:** `AppealEffectService` BehaviorSubject + `isDataLoaded`
**Formal name:** Memoized observable / `shareReplay(1)` pattern

### Micro-library / Micro-frontend
**What you built:** `enable-disable-access-role` as a standalone Angular library in gstn-apps
**Formal name:** Micro-frontend architecture / library-based monorepo
**Interview question:** "How do you share code between multiple Angular applications?"
**Your answer:** Extract shared features as independently buildable libraries in an Nx monorepo.

### HTTP Interceptor / Chain of Responsibility
**What you built:** `http-error.interceptor.ts` for auth, content-type, error normalization
**Formal name:** Chain of Responsibility pattern at the transport layer
**Interview question:** "How would you add auth headers to every API call without modifying each service?"
**Your answer:** HTTP interceptor that implements `HttpInterceptor` interface. Multiple interceptors form a chain.

---

# 18. BEHAVIORAL

## STAR Format
- **S**ituation: context (1 sentence)
- **T**ask: your responsibility (1 sentence)
- **A**ction: what YOU specifically did (3-4 sentences, most detail here)
- **R**esult: measurable outcome (1-2 sentences)

## Questions + How to Answer from Your Experience

**"Tell me about a technically complex problem you solved."**
Use the recursive graph traversal story: the appeal case hierarchy had cycles, redundant API calls were causing UI inconsistencies, you designed a session-scoped deduplication system using composite keys. Result: eliminated duplicate processing, ensured officers always saw accurate case state.

**"Tell me about a time you had to make a design decision with incomplete information."**
Use the APPEL rule engine: statutory rules were evolving mid-development (legal team kept adding cases). You chose a condition-chain design over a hardcoded lookup table so business logic could be changed without schema migrations.

**"Tell me about a time you improved a system's performance or reliability."**
Use the `isProcessing` + session state story: the service was a singleton, so state leaked between cases. You redesigned to session-scoped state with an explicit `resetState()` boundary.

**"Tell me about a time you disagreed with a technical decision."**
Be ready with one honest example. Format: "I disagreed because X. I raised it by Y. The team decided Z. In retrospect, A."

**"How do you mentor junior engineers?"**
"When a junior engineer was adding duplicate API calls in a new controller, I didn't just fix it — I walked them through the existing `AppealCaseService` pattern and explained why centralized state management prevents race conditions. Then I asked them to refactor their code using the pattern."

**"How do you handle technical debt?"**
"I distinguish between debt that is accruing interest (will block future work) and debt that is stable (old but working). For the former, I raise it explicitly in sprint planning with a concrete cost estimate — 'this will take 2 days now vs 2 weeks if we wait.'"

---

# 19. STUDY SCHEDULE

| Week | Focus | Daily Time |
|---|---|---|
| 1-2 | DSA: Arrays, Hashing, Two Pointers, Sliding Window | 2 hrs |
| 3-4 | DSA: Trees, Graphs, Recursion, Backtracking | 2 hrs |
| 5 | DSA: DP, Heaps, Binary Search | 2 hrs |
| 6 | Java: Concurrency, JVM, Collections internals | 2 hrs |
| 7 | System Design: fundamentals (CAP, caching, DB scaling, queues) | 2 hrs |
| 8 | System Design: practice 3 full designs (URL shortener, rate limiter, notification) | 2 hrs |
| 9 | LLD: SOLID + patterns + practice 2 LLD questions | 2 hrs |
| 10 | Angular/RxJS: operators, change detection, lifecycle | 2 hrs |
| 11 | Databases: SQL internals, NoSQL, transactions | 1.5 hrs |
| 12 | Full mock interviews: DSA (1hr) + System Design (1hr) + Behavioral (30min) | — |

---

# 20. RESOURCES

### DSA
- **Neetcode.io** — best structured LeetCode roadmap
- **"Grokking Algorithms"** book — visual, beginner-friendly
- **Striver's SDE Sheet** — popular in India, exhaustive

### System Design
- **"Designing Data-Intensive Applications"** (Kleppmann) — the bible
- **ByteByteGo** (Alex Xu) — visual system design cards
- **Gaurav Sen YouTube** — excellent for Indian product companies

### Java Concurrency
- **"Java Concurrency in Practice"** (Goetz) — still the definitive reference
- **Jenkov.com** — free, exhaustive tutorials

### LLD
- **"Refactoring"** (Fowler) + **"Head First Design Patterns"**
- **Concept&&Coding YouTube** (Shrayansh) — best LLD content in Hindi/English

### RxJS
- **rxmarbles.com** — visual marble diagrams for every operator
- **learnrxjs.io** — practical examples
- **Angular official docs** — change detection deep dive

---

# QUICK REFERENCE: What to Say When You Don't Know

- "I haven't used that specific tool, but the problem it solves is X. In my work I solved that with Y, which works on the same principle."
- "I'd approach this by first understanding the constraints — what's the read/write ratio, what's the scale, what are the consistency requirements."
- "The tradeoff I see is between X and Y. In this scenario, I'd choose X because Z."

**Never say "I don't know" and stop. Always say what you DO know that's adjacent.**
