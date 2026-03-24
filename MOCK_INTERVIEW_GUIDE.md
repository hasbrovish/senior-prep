# Mock Interview Partner Guide

This guide is for two people: Jayanti (the candidate) and a mock partner (the interviewer). Both sections are written for the person who will use them. Keep this file open during every mock session.

---

## PART 1: For the Mock Interviewer (Your Partner)

---

### How to Run a DSA Mock (45 minutes)

#### Setup
- Pick one problem from the DSA Problem Bank at the end of this guide.
- Do not tell the candidate the problem name or number.
- Have the solution open on your side only.

#### Script — what to say

**Opening (1 min):**
> "I'm going to give you a coding problem. You have about 35 minutes to arrive at a working solution. Please think out loud throughout. I'll interrupt if I have questions. Ready?"

**Problem delivery (1 min):**
Read the problem statement clearly. Wait for the candidate to read it back and ask clarifying questions.

**During (track these checkpoints):**
| Time | What you expect |
|---|---|
| 0–5 min | Candidate asks clarifying questions, states constraints |
| 5–10 min | Brute force approach verbalized before any code |
| 10–15 min | Optimal approach identified and explained |
| 15–30 min | Code written (not pseudo-code, real code in Java) |
| 30–40 min | Dry-run with 2 test cases (including edge case) |
| 40–45 min | Complexity stated (time + space) |

**When to give hints:**
- If stuck for more than 3 minutes on approach: ask "What data structure might help here?"
- If stuck on code for more than 5 minutes: ask "Can you write just the inner loop first?"
- If wrong approach: ask "What's the time complexity of that? Can you do better?"
- Never give the answer directly. Give the smallest nudge possible.

#### DSA Scoring Rubric (1–5)

| Score | What it looks like |
|---|---|
| 1 | Cannot arrive at brute force. Needs heavy leading. No working code. |
| 2 | Brute force with help. Code has bugs not caught by candidate. |
| 3 | Brute force independently. Optimal approach with a hint. Mostly working code. Misses an edge case. |
| 4 | Optimal approach independently. Clean code. Catches edge cases. States complexity correctly. |
| 5 | Optimal approach fast. Multiple approaches considered aloud. Perfect code on first try. Proactively handles edge cases. Mentions follow-up optimizations. |

**Debrief (5 min after):**
Tell the candidate: the score, what they got right, one specific thing to improve.

---

### How to Run an LLD Mock (45 minutes)

#### Setup
- Pick one problem from the LLD Problem Bank below.
- You are evaluating: class design, interface design, extensibility, correct use of patterns.

#### Script

**Opening:**
> "Design the classes and interfaces for [problem]. You have 40 minutes. Start with requirements clarification, then go to the class diagram, then walk me through key methods. You can code whatever you have time for."

**Checkpoints:**
| Time | What you expect |
|---|---|
| 0–5 min | Functional + non-functional requirements asked |
| 5–15 min | Class diagram on paper/whiteboard. Key classes named. |
| 15–25 min | Relationships identified: inheritance vs composition decision explained |
| 25–35 min | At least 2 classes coded fully in Java |
| 35–40 min | "How would you extend this for [new requirement]?" |

**Follow-up questions to always ask:**
- "Why did you choose composition here instead of inheritance?"
- "What if we need to support [new variant] — how does your design handle it?"
- "Which design pattern is this? Why did you choose it over [alternative]?"
- "Where does concurrency become an issue in this design?"

#### LLD Scoring Rubric (1–5)

| Score | What it looks like |
|---|---|
| 1 | No clear class separation. Everything in one class. Cannot name any design pattern. |
| 2 | Some classes identified but relationships wrong. One pattern named but misapplied. |
| 3 | Reasonable class structure. Correct use of one pattern. Cannot extend easily for new requirements. |
| 4 | Clean class hierarchy. Correct use of 2+ patterns. Can explain extensibility. Compiles. |
| 5 | Production-grade design. SOLID principles followed. Multiple patterns correctly applied and justified. Handles concurrency. Immediately identifies how to extend. |

---

### How to Run a System Design Mock (45 minutes)

#### The Curious Interviewer Technique
Your job is not to evaluate passively. You are a skeptical senior engineer. After every statement the candidate makes, ask "why" or probe the decision. This is how real system design interviews work.

#### Script

**Opening:**
> "Let's design [system]. I'm the product manager and you're the tech lead. Walk me through how you'd build this. I'll ask questions as you go."

**Probing questions by phase:**

After requirements: "You said 1M DAU. Where did that number come from? What's the peak QPS?"
After capacity: "You're saying 100 QPS. What's the storage calculation for one year?"
After API design: "REST vs gRPC — why REST here? What are the tradeoffs?"
After DB choice: "You chose MySQL. What if writes become a bottleneck at 10x scale?"
After caching: "What's your cache invalidation strategy? What happens on a write?"
After scaling: "You said horizontal scaling. How do you handle session state?"
After availability: "What's your RTO and RPO? How do you test failover?"

**Topics a good answer always covers (track which ones the candidate hits):**
- [ ] Functional requirements (explicit list)
- [ ] Non-functional requirements (latency, throughput, availability SLA)
- [ ] Back-of-envelope capacity estimation
- [ ] API design (at least 3 endpoints)
- [ ] Database schema (at least 2 tables, justifies SQL vs NoSQL)
- [ ] Read path + write path separately
- [ ] Caching layer (what to cache, eviction policy, TTL)
- [ ] Scalability (what happens at 10x load)
- [ ] Single points of failure identified and addressed

#### System Design Scoring Rubric (1–5)

| Score | What it looks like |
|---|---|
| 1 | No estimation. Jumps to solution. Cannot explain tradeoffs. |
| 2 | Some estimation. One-size-fits-all answer (MySQL + Redis for everything). |
| 3 | Good estimation. Reasonable design. Explains most choices. Misses 2–3 of the checklist items. |
| 4 | Complete design. All checklist items covered. Justifies tradeoffs. Handles at least one failure scenario. |
| 5 | Production-level design. Anticipates bottlenecks before asked. Proposes alternatives. Discusses operational concerns (monitoring, deployment, rollback). |

---

### How to Run a Behavioral Mock (15–20 minutes)

#### Setup
Pick 2 questions from the Behavioral Bank below. Each answer should take 3–4 minutes.

#### Script

**Opening:**
> "I'm going to ask you a couple of behavioral questions. Use the STAR format: Situation, Task, Action, Result. I'll ask follow-ups. Ready?"

**Follow-up questions to always ask (regardless of which question you pick):**
- "What specifically did YOU do, versus what the team did?"
- "What would you do differently now?"
- "How did the other person/team react?"
- "What was the measurable impact?"
- "Have you faced a similar situation since?"

#### Behavioral Scoring Rubric (1–5)

| Score | What it looks like |
|---|---|
| 1 | Vague answer. No specific situation. "We did this as a team." |
| 2 | Has a story but no concrete outcome. Speaks in generalities. |
| 3 | Clear STAR structure. Personal ownership. Outcome stated but not quantified. |
| 4 | Clear STAR. Strong personal ownership. Quantified outcome. Reflection on learning. |
| 5 | Compelling story. Quantified impact. Shows growth. Follow-up answered with ease. Multiple LPs demonstrated in one story. |

---

## PART 2: For the Candidate (Jayanti)

---

### 15 Minutes Before a Mock — Checklist

- [ ] Read your top 3 GSTN stories from `Amazon_LP_STAR_Bank.md` (just the headlines, not full text)
- [ ] Write on paper: 3 numbers you'll use today (14M taxpayers, 3B invoices/year, 40% DB reduction)
- [ ] Open a blank text editor for the DSA/code round — practice typing, not thinking about the IDE
- [ ] Drink water. Close Slack, email, phone.
- [ ] Say this out loud: "I will think out loud before I type anything."

---

### First 2 Minutes of Each Round

**DSA Round:**
> "Before I write any code, let me make sure I understand the problem. [Restate it in your own words]. A few clarifying questions: [ask 2–3]. My initial approach is [brute force], which is O(n^2). I think we can do better with [hint at optimal structure]. Let me code the brute force first and then optimize."

**LLD Round:**
> "Let me start with requirements. Functional: [list 3–4]. Non-functional: the system should support concurrent access, be extensible for new types, and be testable in isolation. I'll start with the main entities and their relationships before writing any code."

**System Design Round:**
> "I'd like to start by understanding scale. Is this a new product or existing? What's the expected DAU? [Get a number]. Let me do a quick back-of-envelope: at [X DAU] with [Y actions/day], we're looking at roughly [Z QPS] at peak. That tells me we need [conclusion about architecture tier]."

**Behavioral Round:**
> "I have a strong example for this from my time at GSTN. [One sentence situation]. My specific role was [your role, not 'we']. Here's what I did: [3 concrete actions]. The result was [specific metric]."

---

### How to Recover When You're Stuck

**In DSA (stuck on approach):**
1. Say it out loud: "I'm stuck on the approach. Let me take 30 seconds to think through a simpler version of this problem."
2. Draw a small example on paper/screen.
3. Ask yourself: "What if the input was size 3? What would I do manually?"
4. If still stuck after 2 minutes: "I'm going to start with the brute force and try to optimize from there."
5. Never sit in silence for more than 60 seconds. Say what you're thinking, even if it's wrong.

**In System Design (interviewer challenges your choice):**
1. Don't immediately cave. Say: "That's a fair point. Let me think about it."
2. Either defend: "I chose MySQL here because the data is relational and consistency matters more than scale at this tier. We can add read replicas if needed."
3. Or update: "You're right, if we're optimizing for write throughput at that scale, I'd switch to Cassandra. Let me revise the write path."
4. Never just agree without explaining why.

**In Behavioral (blank on a story):**
1. Use GSTN. You have 22 stories in `Amazon_LP_STAR_Bank.md`. Pause and say "Let me think of the most relevant example." Then pick one.
2. If the question is about a failure: use the Kafka DLQ incident or the HBase bottleneck story.
3. If asked for a time you disagreed with a manager: use the caching architecture disagreement story.

---

### Self-Assessment Checklist After Each Mock

Fill this in within 10 minutes of finishing the mock.

**DSA:**
- [ ] Did I state my approach before coding?
- [ ] Did I name the time and space complexity?
- [ ] Did I test with at least 2 examples (including an edge case)?
- [ ] Did I catch my own bugs before the interviewer pointed them out?
- Score this round: __/5

**LLD:**
- [ ] Did I start with requirements before drawing anything?
- [ ] Did I name at least one design pattern I used?
- [ ] Could I defend my composition vs inheritance choices?
- [ ] Did I write any actual Java code (not just diagram)?
- Score this round: __/5

**System Design:**
- [ ] Did I estimate QPS and storage before designing?
- [ ] Did I explain both the read path and write path separately?
- [ ] Did I proactively identify at least one bottleneck?
- [ ] Did I handle at least one failure scenario?
- Score this round: __/5

**Behavioral:**
- [ ] Did I use "I" not "we" for my specific actions?
- [ ] Did every answer have a quantified result?
- [ ] Did I stay within 4 minutes per answer?
- Score this round: __/5

**Overall post-mock note (one sentence):**
The one thing I will do differently in the next mock: ___

---

## PART 3: Problem Bank for Mock Interviewers

---

### DSA Problem Bank (10 problems, right level for SDE-2)

**P1 — LRU Cache** (LC #146, Hard)
- Problem: Design a data structure that follows LRU eviction policy with O(1) get and put.
- Expected approach: HashMap + doubly linked list. NOT just using LinkedHashMap.
- Interviewer note: If they jump to LinkedHashMap, ask "what if you couldn't use that built-in?"
- Key test case: capacity=2, put(1,1), put(2,2), get(1), put(3,3) — key 2 should be evicted, not key 1.
- Complexity: O(1) time, O(capacity) space.

**P2 — Task Scheduler** (LC #621, Medium)
- Problem: Given tasks with cooldown n, find minimum intervals to execute all tasks.
- Expected approach: Count frequencies, use max-heap or math (most frequent task determines answer).
- Key insight: idle slots = max(0, (max_freq - 1) * (n + 1) + count_of_max_freq) — total intervals.
- Complexity: O(n) time.

**P3 — Trapping Rain Water** (LC #42, Hard)
- Problem: Given array of heights, compute how much water is trapped.
- Expected approach: Two pointers (O(n) time, O(1) space). Brute force O(n^2) accepted as start.
- Interviewer note: If they do prefix/suffix arrays, that's fine (O(n) space). Ask if they can do O(1).
- Complexity: O(n) time, O(1) space optimal.

**P4 — Word Break II** (LC #140, Hard)
- Problem: Given a string and dictionary, return all possible sentences formed by splitting the string.
- Expected approach: Backtracking + memoization. Without memo it times out.
- Key test case: s="catsanddog", words=["cat","cats","and","sand","dog"].
- Complexity: Exponential worst case due to outputs, but O(n^2) with memo for subproblems.

**P5 — Design Hit Counter** (LC #362, Medium)
- Problem: Count hits in last 300 seconds. Functions: hit(timestamp), getHits(timestamp).
- Expected approach: Circular array of size 300 (seconds). Each slot stores [timestamp, count].
- Interviewer note: Follow up — "What if the system is distributed and timestamps are across machines?"
- Complexity: O(1) per operation.

**P6 — Merge K Sorted Lists** (LC #23, Hard)
- Problem: Merge k sorted linked lists into one sorted list.
- Expected approach: Min-heap of size k. Extract minimum, add next node from same list.
- Key edge case: some lists are empty.
- Complexity: O(N log k) where N = total nodes.

**P7 — Sliding Window Maximum** (LC #239, Hard)
- Problem: Return max element in each sliding window of size k.
- Expected approach: Monotonic deque. Maintain deque with indices in decreasing order of values.
- Complexity: O(n) time, O(k) space.

**P8 — Top K Frequent Elements** (LC #347, Medium)
- Problem: Given array, return k most frequent elements.
- Expected approach: HashMap + bucket sort (O(n)) or HashMap + min-heap (O(n log k)).
- Interviewer note: Push for the bucket sort approach if they stop at heap.
- Complexity: O(n) optimal.

**P9 — Serialize and Deserialize Binary Tree** (LC #297, Hard)
- Problem: Design encode/decode for a binary tree to/from a string.
- Expected approach: BFS or DFS with null markers. Must handle nulls explicitly.
- Key test case: single node, empty tree.
- Complexity: O(n) time and space.

**P10 — Number of Islands** (LC #200, Medium — use as warm-up)
- Problem: Count islands in a 2D grid.
- Expected approach: DFS/BFS with marking visited cells.
- Complexity: O(m*n) time and space.

---

### LLD Problem Bank (5 problems)

**L1 — Parking Lot**
Functional requirements: Multiple floors, spot types (compact, large, motorcycle), entry/exit, ticket with fee calculation.
Key classes to expect: `ParkingLot`, `Floor`, `Spot`, `Ticket`, `Vehicle` (abstract), `Car/Truck/Motorcycle`, `FeeCalculator` (Strategy pattern), `SpotAllocationStrategy`.
Evaluation criteria:
- [ ] Abstract Vehicle class with subclasses
- [ ] Strategy pattern for fee calculation
- [ ] Spot types using enum or class hierarchy
- [ ] Thread safety for spot allocation (synchronized or ReentrantLock)
- [ ] Can explain how to add a new vehicle type without changing existing code (Open/Closed)

**L2 — Library Management System**
Functional requirements: Add/remove books, issue/return, fine calculation, search by title/author/ISBN.
Key classes: `Library`, `Book`, `BookItem` (a physical copy), `Member`, `Librarian`, `Lending`, `Fine`, `Catalog`.
Evaluation criteria:
- [ ] Distinction between Book (metadata) and BookItem (physical copy)
- [ ] Observer pattern for overdue notifications
- [ ] Repository pattern for data access
- [ ] Fine calculation as a separate strategy

**L3 — Chess Game**
Functional requirements: Two-player game, valid moves per piece, check/checkmate detection.
Key classes: `Board`, `Cell`, `Piece` (abstract), `King/Queen/Bishop/etc.`, `Player`, `Game`, `Move`.
Evaluation criteria:
- [ ] Abstract Piece with `getValidMoves()` in subclasses
- [ ] Board uses 8x8 Cell array, not primitive int
- [ ] Move validation is in the Piece, not in Game
- [ ] Check detection without infinite recursion

**L4 — Ride Sharing (Uber lite)**
Functional requirements: Request ride, match driver, track location, calculate fare, complete trip.
Key classes: `Rider`, `Driver`, `Trip`, `Location`, `FareCalculator`, `MatchingService`.
Evaluation criteria:
- [ ] Observer/event pattern for status updates
- [ ] Strategy for fare calculation (surge, standard)
- [ ] State machine for trip lifecycle (REQUESTED → ACCEPTED → IN_PROGRESS → COMPLETED)
- [ ] Concurrency: how do you prevent two riders from getting the same driver?

**L5 — Rate Limiter**
Functional requirements: Allow N requests per user per second. Reject excess requests.
Key classes: `RateLimiter` (interface), `TokenBucketRateLimiter`, `SlidingWindowRateLimiter`, `RequestContext`.
Evaluation criteria:
- [ ] Algorithm choice explained (token bucket vs sliding window — tradeoffs)
- [ ] Thread-safe implementation (AtomicLong or synchronized)
- [ ] Configurable per user/per API
- [ ] Can explain Redis-based distributed rate limiter as follow-up

---

### System Design Problem Bank (5 problems)

**S1 — URL Shortener (bit.ly)**
Good answer covers: hash function, redirect performance (<100ms), analytics, custom aliases, expiry.
Storage: 1B URLs, 100 bytes each = 100GB. Fine for relational DB + Redis cache for hot links.
Critical decision: base62 encoding vs MD5 truncation. Collision handling.
Failure scenario to probe: What if Redis goes down? (DB fallback — discuss cache-aside pattern).

**S2 — Distributed Notification System**
Good answer covers: channel abstraction (email/SMS/push), template rendering, rate limiting, retry, preference management, delivery status tracking.
Key decision: Kafka for async delivery, separate consumers per channel.
Scale concern: 10M notifications/day = ~116/second average, 1000/second peak.
Failure scenario: what if SMS provider is down? (provider fallback, DLQ).

**S3 — Order Management System** (relevant to Jayanti's GSTN background)
Good answer covers: order lifecycle state machine, payment integration, inventory reservation, event sourcing.
Key decision: SAGA pattern vs 2PC for distributed transactions. Discuss tradeoffs.
Scale: 10K orders/day = low write volume. Focus on consistency, not just performance.
Failure scenario: payment succeeds but inventory deduction fails (compensation transaction).

**S4 — Real-Time Leaderboard**
Good answer covers: Redis sorted sets (ZADD/ZRANK), score updates, global vs. friend leaderboard, eventual consistency.
Key insight: Redis sorted set gives O(log n) update and O(log n + k) range query.
Scale: 1M players, updates every game completion (~100/second).
Failure scenario: Redis restart (warm from DB, accept eventual consistency during recovery).

**S5 — Product Search (e-commerce)**
Good answer covers: Elasticsearch for full-text search, MySQL for catalog, denormalized search index, faceted filtering, autocomplete (trie or Elasticsearch).
Key decision: why Elasticsearch over MySQL FULLTEXT? (relevance ranking, distributed, facets).
Scale: 10M products, 1K QPS searches.
Failure scenario: Elasticsearch is down — fall back to MySQL LIKE queries with degraded quality.

---

### Java/Spring Interview Questions Bank (20 questions with expected answers)

**Core Java**

**J1 — What is the difference between HashMap and ConcurrentHashMap? When would you use each?**
Expected: HashMap is not thread-safe (undefined behavior with concurrent modification). ConcurrentHashMap uses segment-level locking (pre-Java 8) or CAS + tree nodes (Java 8+). Use HashMap for single-threaded contexts; ConcurrentHashMap for concurrent read/write. Bonus: mention `Collections.synchronizedMap` vs ConcurrentHashMap (former has coarser lock).

**J2 — Explain volatile vs synchronized. Give a concrete example of each.**
Expected: `volatile` guarantees visibility (all threads see the latest write) but NOT atomicity. `synchronized` guarantees both visibility and atomicity. Example for volatile: a boolean `running` flag checked by multiple threads. Example for synchronized: incrementing a counter (you need read-modify-write atomically). Common mistake: using volatile for compound operations like `i++`.

**J3 — What is double-checked locking? Why does it require volatile?**
Expected: A pattern for lazy initialization with minimal locking. Without `volatile`, the JVM can reorder the `new` operation — another thread can see a non-null but partially initialized object. With `volatile`, the memory barrier prevents this reordering. Show the code: `private volatile Singleton instance;`.

**J4 — What is the difference between Callable and Runnable? When do you use CompletableFuture?**
Expected: Runnable cannot return a result or throw checked exceptions. Callable can do both. CompletableFuture is the modern API for async programming: non-blocking, chainable with thenApply/thenCompose, handles errors with exceptionally. Use it when you need to compose async operations or return futures from service methods.

**J5 — Explain Java memory model: heap vs stack, GC generations.**
Expected: Stack holds method frames and local primitives. Heap holds objects. Young gen (Eden + two Survivor) uses minor GC. Old gen uses major GC. Metaspace (Java 8+) holds class metadata. Common GC tuning: -Xms/-Xmx for heap size, G1GC for low-pause, ZGC/Shenandoah for sub-millisecond pauses.

**J6 — What is a WeakReference? Where would you use it?**
Expected: WeakReference allows the GC to collect the referenced object if no strong references exist. Use cases: caches (so cached objects can be evicted under memory pressure), listener registries (prevent memory leaks when listeners are not explicitly deregistered). WeakHashMap uses weak keys for this reason.

**J7 — Explain the difference between checked and unchecked exceptions. GSTN-context: how do you handle Kafka consumer exceptions?**
Expected: Checked exceptions must be declared or caught (IOException, SQLException). Unchecked (RuntimeException and subclasses) do not. In Kafka consumers, you generally catch RuntimeException and decide: is this transient (retry) or permanent (DLQ)? Never swallow exceptions in a consumer.

**Spring/Spring Boot**

**J8 — Explain Spring Bean scopes. What happens if a singleton bean holds a reference to a prototype bean?**
Expected: Singleton = one instance per ApplicationContext. Prototype = new instance per injection. The problem: a singleton holding a prototype reference captures it at injection time, so it never gets a new prototype. Solutions: inject ApplicationContext and getBean() each time, or use Spring's `@Lookup` method injection, or use `ObjectProvider<T>`.

**J9 — What is @Transactional and what are its common pitfalls?**
Expected: Marks a method to run in a DB transaction. Common pitfalls: (1) self-invocation doesn't work (proxy not used), (2) @Transactional on private methods doesn't work, (3) default propagation is REQUIRED (joins existing transaction), (4) checked exceptions don't rollback by default (only RuntimeException does — use `rollbackFor = Exception.class`), (5) long transactions hold DB locks.

**J10 — How does Spring Boot auto-configuration work?**
Expected: `@SpringBootApplication` includes `@EnableAutoConfiguration`. Spring Boot reads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, finds condition-matching classes (`@ConditionalOnClass`, `@ConditionalOnMissingBean`), and registers beans. You can exclude: `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`.

**J11 — Explain Spring Security filter chain. How would you add JWT authentication?**
Expected: Each HTTP request passes through a chain of `Filter` implementations. For JWT: extend `OncePerRequestFilter`, extract the token from the Authorization header, validate it (signature + expiry), set `SecurityContextHolder.getContext().setAuthentication(...)`. Register the filter before `UsernamePasswordAuthenticationFilter`.

**J12 — What is Spring's event mechanism? Give a use case.**
Expected: `ApplicationEventPublisher` + `@EventListener`. Use case: after order placed, publish `OrderPlacedEvent`. Multiple listeners can react independently (send email, update inventory, log audit). This decouples the order service from downstream actions. Can be made async with `@Async` on the listener.

**Kafka / Distributed Systems**

**J13 — What is consumer group rebalancing in Kafka? How do you minimize its impact?**
Expected: Rebalancing happens when a consumer joins/leaves or partition count changes. During rebalance, all consumers in the group pause. To minimize: (1) tune `session.timeout.ms` and `heartbeat.interval.ms`, (2) use Cooperative Rebalancing (incremental, not stop-the-world), (3) use static group membership (`group.instance.id`) to avoid rebalance on restarts, (4) process records fast to avoid `max.poll.interval.ms` timeout.

**J14 — Explain Kafka at-least-once vs exactly-once. Which did you use at GSTN?**
Expected: At-least-once: manual ack, possible duplicates, handle with idempotency. Exactly-once: Kafka transactions (transactional producer + consumer), adds latency, requires Kafka 0.11+. At GSTN: at-least-once with Redis dedup — same pattern as this kafka-pipeline project. Exactly-once transactions were too expensive for our throughput requirement.

**J15 — How does Redis SET NX work? Is it atomic?**
Expected: SET key value NX EX seconds. NX = only set if key does not exist. EX = set expiry in one atomic command (important — don't do SET + EXPIRE as two separate commands; race condition). The whole operation is atomic because Redis is single-threaded. This is the basis of the distributed lock pattern (Redlock for multi-node).

**Databases**

**J16 — When would you choose NoSQL over SQL? Give a concrete example from your experience.**
Expected: NoSQL for: schema flexibility (HBase at GSTN for invoice data with varying fields), horizontal write scalability (Cassandra), document model (MongoDB for nested objects). SQL for: ACID transactions, complex joins, financial data. At GSTN: MySQL for GST returns (strong consistency needed), HBase for invoice store (high write volume, variable schema).

**J17 — Explain the N+1 query problem in JPA/Hibernate. How do you fix it?**
Expected: Fetching a list of 100 orders then lazily loading each order's items = 1 + 100 = 101 queries. Fix: JOIN FETCH in JPQL (`SELECT o FROM Order o JOIN FETCH o.items`), or `@EntityGraph`, or batch size with `@BatchSize`. Detect with: `spring.jpa.show-sql=true` or Hibernate statistics.

**J18 — What is a database index? When does an index hurt performance?**
Expected: Index = B-tree (default) or Hash structure for fast lookups. Helps: read performance on WHERE, JOIN, ORDER BY columns. Hurts: (1) write performance (every INSERT/UPDATE/DELETE must update the index), (2) wrong index on low-cardinality column (e.g., boolean — not selective enough), (3) covering index not used if SELECT * used instead of SELECT indexed_columns.

**Microservices / Architecture**

**J19 — Explain the Circuit Breaker pattern. When does it open?**
Expected: Wraps a remote call. States: CLOSED (normal), OPEN (failing fast, not calling downstream), HALF_OPEN (probe — try one request). Opens when failure rate exceeds threshold (e.g., 50% failures in 10 second window). Resilience4j is the standard Java library. Benefit: prevents cascade failures when a downstream service is slow/down.

**J20 — What is the SAGA pattern? How does it compare to 2PC?**
Expected: 2PC (Two-Phase Commit): distributed locking, coordinator + participants, all-or-nothing, but blocks on coordinator failure. SAGA: sequence of local transactions, each publishes an event for the next, compensating transactions on failure. Two types: choreography (services react to events) vs orchestration (central orchestrator). SAGA is preferred in microservices because it doesn't require a distributed lock. Trade-off: eventual consistency, no global rollback guarantee.

---

### Behavioral Question Bank with Follow-ups (10 questions)

**B1 — Tell me about a time you had to deliver under a very tight deadline.**
Follow-ups: What specifically did you cut scope on? Who made that call? What would you have done differently given more time? Did you communicate the risk to stakeholders before or after missing something?

**B2 — Describe a time you disagreed with a technical decision made by your team or manager.**
Follow-ups: How did you raise the disagreement? Did you escalate? What was the outcome? Would you have handled it differently? What if the other person had been more senior than a manager?

**B3 — Tell me about the most complex technical problem you've solved.**
Follow-ups: How did you know it was solved? Who else was involved? If you had to explain the solution to a junior engineer, what's the core insight? What would break this solution at 10x scale?

**B4 — Tell me about a time you failed. What did you learn?**
Follow-ups: How did you tell your manager/team? What specifically changed in your behavior after? Have you seen a similar situation since, and how did you handle it?

**B5 — Tell me about a time you had to learn something new very quickly.**
Follow-ups: How did you prioritize what to learn? How did you know you knew enough? What's still a gap from that learning sprint?

**B6 — Describe a time you improved a process or system without being asked.**
Follow-ups: Why did no one else do it? Did you get buy-in before or after? What was the business impact?

**B7 — Tell me about a conflict with a colleague. How did you resolve it?**
Follow-ups: What was the root cause of the disagreement — technical, priority, or personal? Did the relationship improve after? What would you do if the same colleague acted the same way again?

**B8 — Tell me about a time you had to work with very ambiguous requirements.**
Follow-ups: How did you decide what to build? What did you get wrong in your assumptions? How did you validate your approach early?

**B9 — Describe a time you had to prioritize between multiple competing tasks.**
Follow-ups: What framework did you use? What did you deprioritize, and what happened to it? Did your prioritization match what your manager would have done?

**B10 — Tell me about a project you're most proud of.**
Follow-ups: What specifically was YOUR contribution vs the team's? If you could change one technical decision, what would it be? What made it harder than expected?
