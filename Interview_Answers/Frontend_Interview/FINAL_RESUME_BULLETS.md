# FINAL RESUME BULLETS — SDE-2 / SDE-3 Target
### 5.6 Years Experience | Java Full-Stack | India's National GST Portal

---

## HOW TO USE THIS

- Copy the **Resume-Ready** version directly into your resume under your current role
- Use the **Extended** version for cover letters or LinkedIn descriptions
- The **Interview Hook** tells you what the interviewer will ask — be ready
- Bullets are sorted **high → low priority** — if space is tight, drop from the bottom

---

## RESUME FORMATTING GUIDELINES

| Rule | Why |
|---|---|
| Start every bullet with a **strong past-tense verb** (Designed, Built, Drove, Owned) | ATS parsers and recruiters scan the first word |
| Keep each bullet to **1–2 lines** on a standard resume (max ~25 words per line) | Hiring managers spend 6–8 seconds per resume |
| Include **one quantifiable metric** per bullet (10+ rules, 21 libraries, 70K+ LOC, 11K+ LOC) | Numbers break the wall of text and prove scale |
| End with **impact** (what changed because of your work) | Shows you think beyond code |
| No jargon without context — say "GST portal serving millions" not just "GST portal" | Reader may not know your domain |
| No filler words — remove "Responsible for", "Worked on", "Helped with" | These signal a task-executor, not an owner |

---

## BULLET 1 — Case-Graph Traversal + Compliance Rule Engine

### Resume-Ready (copy this)
> Designed and implemented a recursive case-graph traversal engine with session-scoped deduplication (ES6 Set) and a multi-condition compliance rule engine evaluating 10+ statutory business rules — enabling real-time legal-validity checks for adjudicating officers on India's national GST portal serving millions of taxpayers.

### Extended (for cover letter / LinkedIn)
> Built the core case-validation subsystem for India's national GST dispute-management portal. The system traverses a directed graph of related legal proceedings using mutual recursion across two API-driven functions, with composite-key deduplication (Set-based) to eliminate redundant network calls and prevent infinite loops. A downstream rule engine evaluates 10+ statutory conditions — active waivers, 4-month lockout windows, order lifecycle states — and surfaces contextual warnings to officers before they issue legally binding orders. Handles single-year and multi-year tax demand scenarios across 3 module contexts.

### What Makes This Impressive
- **Graph traversal** and **mutual recursion** are DSA concepts most frontend engineers never touch
- **Session-scoped idempotency** is a distributed-systems concept applied on the frontend
- **Rule engine** shows domain modeling ability — not just CRUD
- **"Serving millions"** establishes blast radius

### Interview Hook
> "Tell me more about this graph traversal — what does the graph look like?"
>
> Be ready to draw: Case Item → references ARN → Appeal Folder → references RefId → Case Item → ...  
> Explain DFS, cycle detection via visited Set, O(V+E) complexity, soft-failure on partial errors.

---

## BULLET 2 — AngularJS-to-Angular Migration at Scale

### Resume-Ready (copy this)
> Drove incremental migration of a 70,000+ LOC AngularJS application to Angular by architecting new features as standalone TypeScript micro-libraries in a monorepo (21 libraries), reducing coupling and enabling parallel team delivery without a full rewrite.

### Extended
> Led the frontend modernization strategy for a large-scale government back-office application. Instead of a risky big-bang rewrite, adopted the Strangler Fig pattern — new features were built as self-contained Angular libraries in a monorepo (21 libraries under gstn-apps/libs/back-office/), each with its own module, routing, tests, and barrel exports. Angular components are bridged into the AngularJS host via downgradeComponent. This enabled multiple teams to ship independently while the legacy system continued serving production traffic.

### What Makes This Impressive
- **70K+ LOC migration** — shows you've dealt with real legacy at scale, not toy apps
- **Strangler Fig** — named architectural pattern that senior engineers recognize instantly
- **21 micro-libraries** — proves you think in modular, composable units
- **"Without a full rewrite"** — shows pragmatism over perfectionism (a senior trait)

### Interview Hook
> "How did you decide what to migrate first?"
>
> Answer: New features were built in Angular. Existing features were migrated when they needed significant changes. We prioritized by change frequency — modules that changed often were migrated first (higher ROI).

---

## BULLET 3 — RBAC Micro-Library with Reactive State

### Resume-Ready (copy this)
> Built a reusable Angular RBAC micro-library with smart/dumb component separation, reactive state management (RxJS BehaviorSubject), and Excel report export — enforcing least-privilege access control for thousands of back-office tax officers across multiple modules.

### Extended
> Designed and built an end-to-end role-based access control module as a standalone Angular library in the gstn-apps monorepo. The library uses a container/presentational component architecture — the container component handles API communication and state management via RxJS BehaviorSubject, while presentational components receive data through @Input and emit events through @Output. Includes toggle-based permission management, audit history tracking, and styled Excel export via ExcelJS. Consumed by multiple back-office modules without duplication.

### What Makes This Impressive
- **RBAC** — security is always a plus on a resume
- **Smart/dumb components** — shows you follow established frontend architecture patterns
- **RxJS BehaviorSubject** — shows reactive programming fluency
- **"Reusable across multiple modules"** — proves you build platform-level code, not one-off features
- **"Least-privilege"** — security vocabulary that senior roles are expected to know

### Interview Hook
> "Why RBAC on the frontend if the backend also enforces it?"
>
> Answer: Defense in depth. Frontend RBAC is a UX concern — prevent the user from even seeing actions they can't perform. Backend RBAC is the security boundary — reject unauthorized API calls with 403. Both are needed.

---

## BULLET 4 — End-to-End Appeal Module Ownership

### Resume-Ready (copy this)
> Owned end-to-end development of the appeal litigation module — covering case assignment, simultaneous/combined order processing, and real-time dashboard counters — extracting shared business logic into a dedicated service layer that eliminated duplication across 4 controller files totaling 11,000+ LOC.

### Extended
> Served as the primary developer for the appeal litigation subsystem — the full lifecycle from case filing through assignment, hearing, order issuance, and appeal effect. Built the case assignment workflow (role-based distribution to adjudicating officers), simultaneous order processing (two related appeals adjudicated side-by-side), combined order processing (single order covering multiple appeals with cross-case amount propagation), and real-time dashboard counters (Angular components with BehaviorSubject-based state). Identified and eliminated business-logic duplication by extracting a shared AppealCaseService consumed by 4 controllers, reducing maintenance surface and improving consistency.

### What Makes This Impressive
- **"Owned end-to-end"** — signals ownership, not just ticket execution
- **"Simultaneous/combined orders"** — domain complexity that shows you handle non-trivial business logic
- **"Extracted shared service layer"** — refactoring discipline (cleaning up, not just adding)
- **"Eliminated duplication across 4 controllers"** — measurable impact on code quality
- **"11,000+ LOC"** — scale context

### Interview Hook
> "How did you handle state sharing between simultaneous orders?"
>
> Answer: Both cases' data is loaded into the same AngularJS scope. Dispute amounts from Case A's application are loaded alongside Case B's. The combined order is saved as a single API call so the backend writes atomically. Concurrency conflicts are prevented upstream — only one officer is assigned per case.

---

## ATS KEYWORD CHECKLIST

These terms appear naturally in your bullets. ATS systems and recruiters at product companies filter for them:

| Category | Keywords Hit |
|---|---|
| **Languages / Frameworks** | Java, JavaScript, TypeScript, Angular, AngularJS, RxJS, Spring |
| **Architecture** | Monorepo, micro-library, service layer, migration, RBAC, interceptor |
| **CS Fundamentals** | Recursive, graph traversal, deduplication, rule engine, state management |
| **Practices** | Smart/dumb components, reactive programming, BehaviorSubject, least-privilege |
| **Scale Signals** | 70,000+ LOC, 21 libraries, 10+ rules, 11,000+ LOC, millions of users |
| **Ownership Signals** | Designed, Drove, Built, Owned, end-to-end |

---

## QUICK COPY — ALL 4 BULLETS (paste into resume)

```
• Designed and implemented a recursive case-graph traversal engine with session-scoped
  deduplication (ES6 Set) and a multi-condition compliance rule engine evaluating 10+
  statutory business rules — enabling real-time legal-validity checks for adjudicating
  officers on India's national GST portal serving millions of taxpayers.

• Drove incremental migration of a 70,000+ LOC AngularJS application to Angular by
  architecting new features as standalone TypeScript micro-libraries in a monorepo
  (21 libraries), reducing coupling and enabling parallel team delivery without a
  full rewrite.

• Built a reusable Angular RBAC micro-library with smart/dumb component separation,
  reactive state management (RxJS BehaviorSubject), and Excel report export — enforcing
  least-privilege access control for thousands of back-office tax officers across
  multiple modules.

• Owned end-to-end development of the appeal litigation module — covering case assignment,
  simultaneous/combined order processing, and real-time dashboard counters — extracting
  shared business logic into a dedicated service layer that eliminated duplication across
  4 controller files totaling 11,000+ LOC.
```

---

## WHAT TO REMOVE FROM YOUR CURRENT RESUME

If you have any of these, **delete them** — they weaken your profile:

- ~~Responsible for developing and maintaining frontend modules~~
- ~~Worked on AngularJS and Angular projects~~
- ~~Created UI components as per requirements~~
- ~~Fixed bugs and resolved production issues~~
- ~~Participated in code reviews and sprint ceremonies~~

These say nothing. Your 4 bullets above say everything.
