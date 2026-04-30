# SDE-2 INTERVIEW SIMULATION — Project Architecture & Feature Deep Dive
## Full Mock Interview: Questions, Expected Answers, Vocabulary, and Traps

---

# HOW THIS INTERVIEW ROUND WORKS

**Format:** 45-60 minutes. Interviewer says: "Walk me through a technically challenging project you've worked on."
**What they're evaluating:**
1. Can you explain complex systems simply? (Communication)
2. Did you make real engineering decisions, or just follow instructions? (Ownership)
3. Do you understand WHY things are built a certain way? (Depth)
4. Can you see what's wrong with your own design? (Self-awareness / maturity)
5. Do you use correct engineering vocabulary? (Calibration)

**Golden rule:** Talk like an architect, not a task-executor. Say "I designed" not "I was asked to build."

---

# PART 1 — THE OPENING (How to introduce your project)

## Q1: "Tell me about your current project and your role."

### BAD answer (task-executor mode):
> "I work on GSTN. I build features in AngularJS. I work on appeal module. I make API calls and show data."

### GOOD answer (architect mode):

> "I work on India's national GST portal — it's a large-scale government platform serving millions of registered taxpayers and thousands of back-office tax officers across all Indian states.
>
> The system is a distributed web application with a Java backend and an AngularJS frontend that we're incrementally migrating to Angular. The back-office module I work on handles the full appeal litigation lifecycle — from when a taxpayer or the department files an appeal against a tax demand, through case assignment to adjudicating officers, hearing notices, order issuance, and appeal effect.
>
> I've been the primary developer on the appeal case management subsystem. My most significant contribution was designing a **case-graph traversal engine** with a **compliance rule engine** — essentially a system that walks through a directed graph of related legal cases, deduplicates API calls using session-scoped idempotency keys, and evaluates 10+ statutory conditions to determine whether an officer is legally permitted to issue an order. If not, it surfaces a contextual warning modal.
>
> I also built the RBAC module as an Angular micro-library in a monorepo, contributed to the BO revamp dashboard counters, and worked on simultaneous/combined order processing — where two appeals against the same tax demand need to be adjudicated together."

### What the interviewer heard:
- "large-scale" — you understand the blast radius of your work
- "directed graph" — you think in data structures, not just UI widgets
- "idempotency keys" — you know distributed systems vocabulary
- "compliance rule engine" — you think in domain abstractions
- "incrementally migrating" — you've dealt with real-world legacy constraints
- "monorepo" — you understand modern architecture patterns

---

# PART 2 — ARCHITECTURE DEEP DIVE

## Q2: "Draw me the high-level architecture of this system."

### Expected answer (draw this mentally or on whiteboard):

```
┌──────────────────────────────────────────────────────────┐
│                     BROWSER (SPA)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ AngularJS   │  │ Angular      │  │ gstn-apps      │  │
│  │ Controllers │  │ (BO-Revamp)  │  │ (21 micro-libs)│  │
│  │ + Services  │  │ Components   │  │ TypeScript     │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│         └────────┬───────┴───────────────────┘           │
│                  │                                       │
│          HTTP Interceptor (auth token, error handling)   │
└──────────────────┬───────────────────────────────────────┘
                   │ REST API (JSON)
                   ▼
┌──────────────────────────────────────────────────────────┐
│              API GATEWAY / NGINX                         │
│         (routing, SSL termination, static serve)         │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│              JAVA BACKEND (Spring)                       │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  │
│  │ Appeal APIs  │  │ Case Folder   │  │ Auth / RBAC  │  │
│  │ /getCaseItem │  │ Service       │  │ Service      │  │
│  │ /getByArn    │  │               │  │              │  │
│  └──────┬───────┘  └───────┬───────┘  └──────┬───────┘  │
│         └────────┬─────────┘                  │          │
│                  ▼                            │          │
│         ┌────────────────┐                   │          │
│         │   Database     │◄──────────────────┘          │
│         │   (Oracle/     │                              │
│         │    PostgreSQL) │                              │
│         └────────────────┘                              │
└──────────────────────────────────────────────────────────┘
```

### Key talking points when drawing:

1. **"The frontend is a hybrid."** Explain: "We have a legacy AngularJS SPA that serves the majority of back-office modules. In parallel, we have a modern Angular application (BO-Revamp) and a monorepo of 21 micro-libraries. New features are built as Angular libraries and bridged into the AngularJS host using Angular's `downgradeComponent` API — this is the Strangler Fig migration pattern."

2. **"All HTTP traffic passes through a single interceptor."** Explain: "We implemented the Chain of Responsibility pattern at the transport layer — every outgoing request gets auth token injection, content-type negotiation, and BlockUI integration. Every incoming error response gets normalized centrally. No individual service needs to handle auth or loading states."

3. **"The appeal module has its own service layer."** Explain: "I extracted business rule evaluation into a dedicated `AppealCaseService` — a singleton AngularJS service that acts as a Facade over the case traversal and rule engine logic. Controllers don't know about the graph traversal or compliance rules. They call `processAppealData()` and get a processed scope."

### Follow-up the interviewer WILL ask:

> **"Why didn't you use a microservice architecture?"**

**Your answer:** "This is a government portal with strict deployment constraints — the deployment unit is a WAR/EAR file deployed to application servers across multiple state data centers. The team doesn't have autonomous deployment capabilities. Given those constraints, a modular monolith with clearly separated modules (appeal, recovery, refund, enforcement) was the pragmatic choice. The frontend monorepo with 21 independent libraries gives us module-level independence at the UI layer without the operational overhead of microservices."

**What this signals:** You understand that architecture is driven by organizational and operational constraints, not just technical ideals. This is a very senior answer.

---

# PART 3 — FEATURE DEEP DIVE: THE CASE GRAPH TRAVERSAL

## Q3: "Walk me through the most technically complex feature you built."

### Your structured answer (use this flow):

**1. The Problem (30 seconds)**
> "When an officer opens an appeal case, we need to determine all related legal proceedings — waiver applications, departmental appeals, rejection orders, appellate orders — because the officer cannot issue an adjudication order if certain parallel proceedings are active. These related cases form a graph: a case references an appeal number, that appeal contains case items, those items reference other appeals, and so on. The naive approach of sequential API calls would lead to infinite loops and redundant network requests."

**2. The Solution (60 seconds)**
> "I designed a graph traversal engine using mutual recursion. Two functions — `getCaseItemDetails` and `getItemDetailsFromARN` — call each other. `getCaseItemDetails` takes a case reference ID, fetches all items for that case, and for each item that contains an appeal reference, calls `getItemDetailsFromARN`. That function fetches the appeal's case folder, and if it finds a nested case reference, calls back to `getCaseItemDetails`.
>
> To prevent infinite loops, I used session-scoped deduplication with ES6 Sets. Before every API call, I check a composite key — `sessionId + scopeId + entityId` — against a Set. If it exists, we skip. This gives O(1) lookup and prevents cycles in the case graph.
>
> The session ID is regenerated on every new case load via `resetState()`, which prevents stale state from a previously viewed case from contaminating the next one — critical because the service is a singleton that lives for the lifetime of the SPA."

**3. The Result (15 seconds)**
> "This eliminated all redundant API calls, prevented infinite recursion in production, and gave us a reliable base to layer the compliance rule engine on top of."

---

## Q4: "Why did you use mutual recursion instead of [alternative]?"

### Expected follow-ups and your answers:

**"Why not BFS with a queue?"**
> "The case graph has variable depth and heterogeneous node types — case items and appeal folders have different API endpoints and different response schemas. Mutual recursion naturally maps to this: one function handles case items, the other handles appeal folders. BFS would require a discriminated union in the queue and type-switching logic in the dequeue loop. Mutual recursion was more readable and maintainable for this specific domain."

**"What's the worst-case depth of this recursion?"**
> "In practice, the case graph is shallow — typically 2-3 levels deep. A tax demand leads to at most one waiver application, one rejection order, and one appeal against that rejection. Theoretically, the depth is bounded by the number of distinct legal proceedings on a single demand, which legal constraints cap at around 5-6. So stack overflow is not a practical risk. If it were, I'd convert to an iterative approach with an explicit stack."

**"What happens if an API call fails mid-traversal?"**
> "I used a soft-failure pattern — every `.catch()` handler calls `resolve()` instead of `reject()`. This means a failure in one branch of the graph doesn't abort the entire traversal. The other branches continue, and we get a best-effort view of the case state. I log the error for debugging. This is a deliberate tradeoff: partial data is more useful to the officer than a blank error screen."

**What this signals:** Fault-tolerant design thinking. You didn't just make it work — you decided what should happen when it partially fails.

---

## Q5: "Tell me about the composite key design. Why three parts?"

### Your answer:

> "The key has three components: `sessionId`, `scopeId`, and `entityId` (either a refId or an ARN).
>
> - **`entityId`** is obvious — it's the thing we're deduplicating.
> - **`scopeId`** (Angular's `$scope.$id`) is needed because the same service serves multiple UI components simultaneously. Without it, if an officer has two appeal views open in tabs or sections, Case A's refId would incorrectly suppress the lookup for Case B's identical refId.
> - **`sessionId`** is a timestamp + random value generated on every `resetState()` call. Without it, after an officer views Case A and then opens Case B, the Set still contains Case A's entries. If Case B happens to share any refIds with Case A, those lookups would be skipped — returning stale state from the wrong case.
>
> The three-part key guarantees that deduplication is **scoped to one case, in one UI component, in one logical session** — and nothing leaks across boundaries."

### Trap question the interviewer might ask:

> **"Isn't this over-engineered? Why not just clear the Set before each new case?"**

**Your answer:** "Clearing the Set is what `resetState()` does — but clearance alone isn't sufficient. The `sessionId` handles a race condition: if the user clicks a new case while the previous case's async chain is still resolving, the in-flight promises from Case A would add entries to the freshly cleared Set, contaminating Case B's processing. The sessionId ensures that entries from the old session are never recognized as valid in the new session, even if they arrive late."

**What this signals:** You think about race conditions and async timing — not just the happy path.

---

# PART 4 — THE RULE ENGINE

## Q6: "Tell me about the compliance rule engine."

### Your answer:

> "After the graph traversal completes and we know the full state of all related proceedings, we evaluate a set of compliance rules to determine if the officer should be warned or blocked from issuing an order.
>
> The rule engine evaluates conditions like:
> - Is there an active waiver application? If so, the order is blocked until the waiver is resolved.
> - Has a rejection order been issued? If so, was it within the last 4 months? (Statutory lockout period)
> - Has someone filed an appeal against the rejection? If so, is that appeal's order still pending?
> - Is this a multi-finance-year demand? If so, different rules apply — the officer gets a warning instead of a block.
>
> I modeled this as a decision tree with approximately 10 distinct states and 12 guarded transitions. The state is defined by a combination of boolean flags: `isWaiverCasePresent`, `spl07issued`, `spl07aplissued`, `spl07spl06issued`, `spl07FourMonthsPassed`, etc."

## Q7: "You said 'finite state machine.' Can you draw the state diagram?"

### Your answer (simplified):

```
                ┌──────────────┐
                │  INITIAL     │ (no related proceedings)
                │  → Allow     │
                └──────┬───────┘
                       │ waiver filed?
                       ▼
                ┌──────────────┐
                │  WAIVER      │
                │  PENDING     │──── No order issued → BLOCK
                └──────┬───────┘
                       │ waiver decided?
                ┌──────┴──────┐
                ▼             ▼
        ┌──────────┐  ┌──────────────┐
        │ WAIVER   │  │ WAIVER       │
        │ APPROVED │  │ REJECTED     │
        │ (SPL-05) │  │ (SPL-07)     │
        │ → Warn   │  └──────┬───────┘
        └──────────┘         │ < 4 months?
                       ┌─────┴─────┐
                       ▼           ▼
               ┌──────────┐ ┌──────────────┐
               │ LOCKOUT  │ │ LOCKOUT      │
               │ ACTIVE   │ │ EXPIRED      │
               │ → BLOCK  │ │ → Allow      │
               └──────────┘ └──────┬───────┘
                                   │ appeal filed against SPL-07?
                                   ▼
                            ┌──────────────┐
                            │ APPEAL       │
                            │ PENDING      │──→ BLOCK until decided
                            └──────┬───────┘
                                   │ appeal decided?
                            ┌──────┴──────┐
                            ▼             ▼
                    ┌──────────┐  ┌──────────────┐
                    │ APPEAL   │  │ VOID ORDER   │
                    │ ORDER    │  │ ISSUED       │
                    │ ISSUED   │  │ → Allow      │
                    │ → Allow  │  └──────────────┘
                    └──────────┘
```

### Follow-up question:

> **"Why didn't you use a proper state machine library like XState?"**

**Your answer:** "Two reasons. First, the AngularJS codebase doesn't have a build system that supports npm-installed libraries easily — it uses script tags and a concatenation-based build. Adding XState would require a build pipeline change that was out of scope. Second, the state space is small enough (10 states) that an explicit condition chain is readable and auditable by domain experts — the legal team reviews these rules. A formal FSM definition would be more maintainable at scale, but for this size, the condition chain was the pragmatic choice.

If I were building this from scratch today in the Angular codebase, I would absolutely use XState — it gives you visualization of the state diagram, guards as first-class concepts, and prevents illegal state transitions by construction."

**What this signals:** You know the ideal solution AND you know when pragmatism trumps purity.

---

## Q8: "You mentioned APLTD uses if/else-if but APPEL uses sequential if/if. Why the asymmetry?"

### Your answer:

> "In the APLTD module (departmental appeal), the conditions are mutually exclusive — at any given point, exactly one of the warning conditions can be true. A waiver-pending state and a waiver-rejected state cannot coexist. So `if/else if` naturally models this: first match wins, and we stop evaluating.
>
> In the APPEL module (taxpayer appeal), multiple conditions can be simultaneously true. A taxpayer might have an active waiver application AND a departmental appeal pending AND a prior appeal that hasn't been withdrawn. Each condition adds important context. The sequential `if/if/if` pattern means the last matching condition overwrites the warning message — effectively implementing a **priority system where later conditions are higher priority**.
>
> I'll be transparent: this implicit priority via execution order is fragile. If someone adds a new condition at the wrong position, it silently changes the priority of existing conditions. A more robust design would be an explicit priority map — each rule has a numeric priority, all matching rules are collected, and the highest-priority one is displayed. That's what I'd refactor toward if the rule count grows beyond 15."

**What this signals:** You can critique your own code constructively. This is the #1 thing senior interviewers look for. Juniors defend everything they wrote. Seniors say "here's what I'd improve."

---

# PART 5 — ENGINEERING DECISIONS

## Q9: "Why is the service a singleton? What problems does that cause?"

### Your answer:

> "In AngularJS, services registered with `.service()` are singletons by design — the framework instantiates them once and injects the same instance everywhere. This is generally desirable: it gives us a single source of truth for state.
>
> The problem is that the singleton outlives any individual case. When an officer opens Case A, processes it, then navigates to Case B — the singleton still holds Case A's state. Boolean flags like `isWaiverCasePresent` from Case A would incorrectly apply to Case B.
>
> I solved this with an explicit lifecycle method: `resetState()`. It clears all Sets, resets all flags, and generates a new `sessionId`. The caller (the controller) is responsible for calling `resetState()` before initiating a new case. This is the **manual lifecycle management** pattern — the service doesn't know when a new case starts, so the consumer tells it.
>
> The downside is coupling: every consumer must remember to call `resetState()`. If a new developer adds a controller and forgets, they get stale state. To mitigate this, `processAppealData()` checks a `completedCases` Set and skips if the same session+ARN has already been processed — a defensive guard.
>
> In a modern Angular app, I'd use a different pattern: a `BehaviorSubject` that emits the current case state, and each component subscribes. When the case changes, you push a new initial state to the subject. Subscribers automatically get the reset. No manual `resetState()` needed."

## Q10: "How do you handle auth across all these API calls?"

### Your answer:

> "Auth is handled at the transport layer using the Chain of Responsibility pattern — specifically an Angular HTTP interceptor. Every outgoing request passes through the interceptor, which:
>
> 1. Reads the auth token from a session service
> 2. Clones the request with the `Authorization` header attached
> 3. Sets `Content-Type` to `application/json` unless the request is a file upload
> 4. Activates BlockUI (loading overlay) before the request
> 5. Deactivates BlockUI on response
> 6. On error, normalizes the error response into a consistent format
>
> This means no individual service or API call needs to think about auth, loading states, or error formats. It's a cross-cutting concern handled once. This is analogous to a servlet filter in Java, or middleware in Express.js."

## Q11: "How do you share state between components?"

### Your answer:

> "We use three patterns depending on the context:
>
> 1. **ShareData service (AngularJS):** A simple singleton service with getter/setter methods. Controllers write data to it, and other controllers read from it. This is the AngularJS equivalent of a context or a simple store. It works for parent-child communication within the same page.
>
> 2. **BehaviorSubject (Angular):** For the BO-Revamp dashboard, I used a `BehaviorSubject` in `AppealEffectService`. Components subscribe to the observable and get the latest value. Late subscribers automatically receive the cached value. This is the reactive pattern — it decouples the producer from consumers.
>
> 3. **LocalStorage (role caching):** For data that must survive page refreshes — like the officer's role assignment — we serialize to LocalStorage. On page load, we hydrate the role from LocalStorage before making an API call. This gives instant UI rendering while the API call confirms the role is still valid. This is the **stale-while-revalidate** pattern.
>
> In a greenfield project, I'd use NgRx or a lightweight state management library for all three cases. But in a hybrid AngularJS/Angular codebase, each pattern fits its context."

---

# PART 6 — SCALE, FAILURE, AND PRODUCTION

## Q12: "What's the scale of this system?"

### Your answer:

> "India has approximately 1.4 crore (14 million) registered GST taxpayers. The portal handles return filing for all of them — the peak load during return filing deadlines is significant.
>
> The back-office module I work on serves thousands of tax officers across all Indian states. On the appeal module specifically, at any given time there are lakhs of active appeal cases being processed. Each case load triggers the graph traversal I described — typically 2-5 API calls per case depending on depth.
>
> The frontend is a single-page application served via CDN. The backend is deployed across multiple data centers. API responses are in the low hundreds of milliseconds for most calls."

## Q13: "What happens if the graph traversal takes too long? Have you seen timeout issues?"

### Your answer:

> "Good question. The traversal involves sequential API calls because each call's response determines the next call. For a 3-level deep case graph, that's 3 sequential round-trips — roughly 300-900ms depending on backend load.
>
> We haven't hit timeout issues because:
> 1. The graph is shallow (bounded by legal constraints to ~5 levels max)
> 2. The deduplication ensures we never make the same call twice
> 3. Within a single level, I use `Promise.all` to parallelize sibling lookups
>
> If this became a problem, the optimization path would be:
> - **Backend aggregation:** Create a single API that returns the full case graph in one call, instead of requiring the frontend to walk it incrementally. This is the BFF (Backend for Frontend) pattern.
> - **Caching:** Cache case graph snapshots with a short TTL, since the graph changes infrequently (only when a new order is issued).
> - **Prefetching:** When the officer opens the case list, start prefetching case graphs in the background for the top N cases."

## Q14: "Have you encountered any production bugs in this system?"

### Your answer (be honest — interviewers respect this):

> "Yes. The most significant one was the stale state bug I mentioned — before I added the session-scoped deduplication, an officer who viewed two cases in succession would sometimes see warnings from the first case appear on the second. This was because the singleton service's boolean flags weren't being reset between cases.
>
> The root cause was that the original implementation used a simple `isProcessing` boolean and didn't scope state to a logical session. I fixed it by introducing the `resetState()` method with a new `sessionId` on each call, and adding the three-part composite key to the deduplication Sets.
>
> The fix was zero-downtime — it was a frontend-only change. I deployed it, verified it in staging with a multi-case test scenario, and confirmed in production via console logs."

---

# PART 7 — DESIGN PATTERN QUESTIONS

## Q15: "What design patterns did you use in this system?"

### Your answer (map each to the textbook pattern):

| What I Built | Design Pattern |
|---|---|
| `AppealCaseService.processAppealData()` hides graph traversal from controllers | **Facade** |
| Graph traversal → getCaseItemDetails ↔ getItemDetailsFromARN | **Visitor / DFS traversal** (not a GoF pattern, but graph algorithm) |
| HTTP Interceptor for auth, error handling, loading state | **Chain of Responsibility** |
| Service is instantiated once, injected everywhere | **Singleton** |
| `checkAndShowWarningPopups` — behavior changes based on state flags | **State Pattern** (informal FSM) |
| `$compile` → Bootstrap modal → `alert()` fallback | **Graceful Degradation / Strategy** (fallback strategies) |
| `createAjaxGetPromise` wraps `$q.defer()` around native ajax | **Adapter** (adapting one async interface to another) |
| `BehaviorSubject` in AppealEffectService — components subscribe | **Observer** |
| Multiple modules (APPEL, APLTD) with different rule sets | **Strategy** (each module is a different strategy for rule evaluation) |

## Q16: "If you could redesign this system from scratch, what would you change?"

### Your answer (shows maturity):

> "Three things:
>
> **1. Replace the condition chain with a declarative rule engine.**
> Instead of imperative `if/else` chains, I'd define rules as data — a JSON or TypeScript array of `{ condition, priority, message, action }` objects. A generic evaluator iterates the rules, collects all matching ones, sorts by priority, and displays the highest. This is the **Specification Pattern** — it makes rules auditable, testable, and externally configurable without code changes.
>
> **2. Move the graph traversal to the backend.**
> The frontend shouldn't be making 3-5 sequential API calls to assemble the case graph. A single backend API should return the full graph with all related proceedings. This reduces latency, simplifies the frontend, and lets the backend do the compliance evaluation server-side — which is more secure because the rules can't be bypassed by a tampered frontend.
>
> **3. Use proper state management.**
> Replace the manual `resetState()` lifecycle with an NgRx-style store or at minimum a `BehaviorSubject`-based service where the state is immutable and changes are explicit actions. This eliminates the stale-state bug class entirely."

---

# PART 8 — CURVEBALL QUESTIONS (the hard ones)

## Q17: "Your deduplication uses a Set. What's the time and space complexity?"

**Answer:** "Set lookup and insertion are both O(1) amortized — they're hash-based. Space is O(n) where n is the number of distinct entities in the case graph. In practice, n is under 20 for the deepest cases, so the space cost is negligible."

## Q18: "What if two officers view the same case simultaneously? Any race conditions?"

**Answer:** "No, because the state is entirely client-side. Each officer's browser has its own instance of the AngularJS app, its own singleton service, and its own Sets. There's no shared mutable state between browsers. The server APIs are stateless and idempotent — they return the same case data regardless of who calls them.

The only shared state is the database, and that's managed by the backend with proper transaction isolation. If Officer A issues an order while Officer B is still reviewing the case, Officer B would see the stale pre-order state until they refresh. That's acceptable because order issuance is a rare, deliberate action — not a concurrent hot path."

## Q19: "You mentioned Promise.all for parallel sub-operations. What if one of the parallel promises fails?"

**Answer:** "Standard `Promise.all` is fail-fast — if any promise rejects, the entire `Promise.all` rejects and the other promises' results are lost. In my implementation, each individual promise uses the soft-failure pattern (catches errors and resolves with undefined instead of rejecting). So by the time they reach `Promise.all`, none of them will reject. `Promise.all` always resolves, and the aggregate result contains whatever data each branch successfully retrieved.

If I wanted even more granularity, I'd use `Promise.allSettled` (ES2020), which returns the status of each promise individually — `fulfilled` or `rejected` — and never short-circuits. But since my promises already never reject, `Promise.all` is equivalent."

## Q20: "How would you unit test the rule engine?"

**Answer:** "The rule engine is a pure function of scope state — given a set of boolean flags (`isWaiverCasePresent`, `spl07issued`, etc.), it deterministically produces a warning message (or none). This makes it highly testable.

I'd write a test for each state combination:

```javascript
describe('checkAndShowWarningPopups', function() {
  it('should block when waiver is pending and no order issued', function() {
    scope.isWaiverCasePresent = true;
    scope.spl05OrderIssued = false;
    scope.spl07issued = false;
    scope.moduleName = 'APLTD';
    scope.dataProcessingComplete = true;

    service.checkAndShowWarningPopups(scope, shareData, false);

    expect(scope.splpopup).toBe(true);
    expect(dialogueMessage).toContain('waiver');
  });

  it('should allow when 4-month lockout has expired', function() {
    scope.spl07issued = true;
    scope.spl07FourMonthsPassed = true;
    // ... assert no popup
  });
});
```

The challenge is that the current implementation has side effects — it manipulates the DOM via `$compile` and shows Bootstrap modals. To make it properly testable, I'd separate the **rule evaluation** (pure function that returns a decision) from the **UI rendering** (shows the modal). The rule evaluation becomes a pure, easily testable function. The UI rendering is tested separately with DOM assertions."

**What this signals:** You understand the difference between testable and untestable code, and you know how to refactor toward testability.

---

# PART 9 — VOCABULARY CHEAT SHEET

*Use these exact phrases in your interview — they signal senior-level thinking*

| Instead of saying... | Say this... |
|---|---|
| "I made API calls in a loop" | "I implemented a graph traversal over the case hierarchy" |
| "I checked if we already called this API" | "I used session-scoped idempotency keys with O(1) Set-based deduplication" |
| "I had a lot of if/else conditions" | "I implemented a compliance rule engine modeled as a finite state machine with guarded transitions" |
| "I showed a popup" | "I orchestrated an async modal pipeline with graceful degradation to native alerts" |
| "The service remembers data" | "The service uses closure-scoped singleton state with explicit lifecycle management" |
| "I added auth headers to every request" | "I centralized cross-cutting concerns via the Chain of Responsibility pattern in an HTTP interceptor" |
| "We're rewriting the app" | "We're incrementally migrating using the Strangler Fig pattern — extracting features into Angular micro-libraries" |
| "I stored data so we don't call the API again" | "I implemented a memoized reactive singleton with a BehaviorSubject" |
| "The error doesn't crash the whole page" | "I used fault-tolerant orchestration with soft-failure semantics — resolve instead of reject in catch handlers" |
| "I made separate Angular libraries" | "I built features as independently versioned micro-libraries in a monorepo architecture" |
| "Both appeals need to be handled together" | "I implemented distributed state synchronization across simultaneous proceedings" |
| "I made the button disabled based on role" | "I implemented presentation-layer RBAC with dynamic capability toggling" |

---

# PART 10 — RED FLAGS TO AVOID

Things that will cost you points if you say them in an interview:

| Red Flag | Why It's Bad | What to Say Instead |
|---|---|---|
| "I was asked to build this" | Sounds like you don't own decisions | "I designed and implemented this" |
| "It's a government project so we can't use X" | Sounds like excuse-making | "Given the deployment constraints, I chose X because..." |
| "I don't know why it's done this way" | Signals you don't understand the code | "The tradeoff here is between X and Y. We chose Y because Z." |
| "We use AngularJS" (and stop) | Sounds dated | "We have a legacy AngularJS layer that we're incrementally migrating to Angular using the Strangler Fig pattern" |
| "The file is 16,000 lines" (with no comment) | Sounds like you tolerate bad code | "The file grew to 16K LOC due to feature accumulation. I extracted shared logic into a dedicated service to reduce controller coupling." |
| "I didn't write tests because..." | No excuse is acceptable | "Testing is challenging due to DOM side effects. I'd refactor the rule evaluation into a pure function for testability." |
| Using internal project names (DRC-07, APL-04) | Outsider can't understand | "Tax demand notice", "adjudication order" |

---

# PART 11 — THE 2-MINUTE CLOSING

When the interviewer says "Do you have any questions for me?", always ask:

1. **"What does the tech stack look like, and are you doing any major migrations?"** (Shows you care about architecture)
2. **"How does your team handle technical debt — is it formally tracked?"** (Shows maturity)
3. **"What does a typical feature lifecycle look like — from design doc to production?"** (Shows process awareness)

Never ask about salary, WFH policy, or benefits in the technical round.

---

# QUICK REFERENCE: THE 60-SECOND PROJECT PITCH

Memorize this and use it verbatim when the interviewer says "Tell me about your project":

> "I work on India's national GST portal — a large-scale government platform serving 14 million taxpayers and thousands of back-office officers. I'm the primary developer on the appeal litigation subsystem, which handles the full lifecycle from appeal filing through adjudication.
>
> My most impactful contribution was a case-graph traversal engine that walks a directed graph of related legal proceedings using mutual recursion, with session-scoped idempotency keys for deduplication. On top of this, I built a compliance rule engine — essentially a finite state machine with 10 states and 12 guarded transitions — that determines whether an officer is legally permitted to issue an order based on active waivers, statutory time windows, and parallel proceedings.
>
> I also built RBAC as an Angular micro-library in a 21-library monorepo, contributed dashboard counter components, and implemented simultaneous/combined order processing where two appeals on the same demand are adjudicated together.
>
> The stack is a hybrid — legacy AngularJS incrementally migrating to Angular via the Strangler Fig pattern, with a Java backend."

**Time yourself. This should be under 60 seconds.**
