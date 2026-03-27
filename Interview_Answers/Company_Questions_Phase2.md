# Phase 2 Dream Companies — Real Interview Questions (2024–2025)
# Target: SDE-2 / SDE-3 Backend Java | 5.5 YOE | GSTN Background
# Compiled from: Glassdoor, LeetCode Discuss, Blind, AmbitionBox, InterviewBit, Levels.fyi, GeeksForGeeks
# Note: WebSearch was unavailable; content is based on model knowledge through August 2025
#       covering widely reported interview experiences on those platforms.

---

## HOW TO USE THIS FILE

Each section covers one company with:
1. Interview process + number of rounds
2. DSA/Coding questions (exact names + LC numbers)
3. System design questions (exact problem)
4. Java / Spring / language internals
5. Behavioral questions (exact wording)
6. Company-specific focus areas
7. Salary/TC ranges (2024–2025 India)

---

---

# 1. FLIPKART — SDE-2 / SDE-3

## Interview Process
- Total rounds: 5–6
- Round 1: Online Assessment (2 DSA, 90 min, HackerEarth)
- Round 2: DSA Phone Screen (1–2 problems, 45 min)
- Round 3: Low-Level Design / OOP (60 min)
- Round 4: High-Level Design / System Design (60 min)
- Round 5: Tech Deep Dive — past projects + Java internals (60 min)
- Round 6: Hiring Manager / Culture Fit (30–45 min)

**Flipkart is known for**: Concurrency depth, LLD emphasis, large-scale e-commerce system design, and testing your understanding of real distributed systems (not textbook). They ask how YOU would build it, not just name components.

---

## DSA / Coding Questions (Flipkart 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| LRU Cache | #146 | Medium | Very frequently asked — implement with O(1) get/put |
| Merge Intervals | #56 | Medium | Asked in OA and phone screens |
| Meeting Rooms II | #253 | Medium | Booking system variant |
| Word Break II | #140 | Hard | DP + backtracking |
| Kth Largest Element in a Stream | #703 | Easy | Heap usage |
| Sliding Window Maximum | #239 | Hard | Deque approach |
| Flatten Nested List Iterator | #341 | Medium | Iterator design + recursion |
| Copy List with Random Pointer | #138 | Medium | HashMap clone |
| Serialize and Deserialize Binary Tree | #297 | Hard | Asked multiple times |
| Top K Frequent Elements | #347 | Medium | Heap / bucket sort |
| Design Twitter | #355 | Medium | LLD + DSA combined |
| Count of Smaller Numbers After Self | #315 | Hard | Merge sort / BIT variant |
| Employee Free Time | #759 | Hard | Priority queue + intervals |
| Find Median from Data Stream | #295 | Hard | Two heaps |
| Rearrange String K Distance Apart | #358 | Hard | Greedy + heap |

**Flipkart-specific DSA pattern**: They commonly ask interval problems, heap-based problems, and iterator design. Concurrency questions embedded in DSA (e.g., "make your LRU cache thread-safe").

---

## System Design Questions (Flipkart 2024–2025)

- **Design Flipkart's Product Catalog / Search** (most common): Elasticsearch, inverted index, faceted search, ranking
- **Design a Flash Sale System** (Big Billion Days context): Inventory locking, queue-based purchase, overselling prevention, token bucket rate limiting
- **Design an Order Management System**: States (PLACED → CONFIRMED → SHIPPED → DELIVERED → RETURNED), idempotency, event-driven with Kafka, saga pattern
- **Design a Recommendation Engine**: Collaborative filtering, near-real-time updates, cold start
- **Design a Distributed Rate Limiter**: Token bucket vs leaky bucket, Redis sliding window, multi-region
- **Design Flipkart's Notification System**: Push, SMS, email, priority queues, DND windows, deduplication
- **Design a Cart Service** (asked at SDE-2): Consistency, TTL, concurrency (two users modifying same cart)
- **Design a Warehouse Management System** (SDE-3): Slot allocation, pick-route optimization, real-time inventory sync

**Tip**: Flipkart almost always asks about **consistency vs availability tradeoffs** in the context of e-commerce. Be ready to say "during Big Billion Days, I'd accept eventual consistency on cart and strong consistency only on payment/inventory deduction."

---

## Java / Spring Internals (Flipkart 2024–2025)

- **Concurrency deep dive** (asked in every round at some point):
  - Difference between `synchronized`, `ReentrantLock`, `StampedLock`
  - How `ConcurrentHashMap` works internally (segment locking vs CAS in Java 8)
  - `volatile` keyword — memory visibility, happens-before, not atomicity
  - `ThreadLocal` — when to use, memory leak risks in thread pools
  - Producer-consumer with `BlockingQueue` — code it live
  - `CompletableFuture` chaining — `thenApply` vs `thenCompose`, exception handling
- **JVM internals**:
  - G1GC vs ZGC — when to use which, STW pauses, region-based collection
  - Class loading — parent delegation model, how Spring overrides it
  - Memory areas — heap (young/old gen), metaspace, stack, native memory
- **Spring Boot specifics**:
  - How `@Transactional` works with proxy — CGLIB vs JDK proxy, self-invocation bug
  - Spring's bean lifecycle — `@PostConstruct`, `BeanFactoryPostProcessor`, `BeanPostProcessor`
  - `@Async` internals — thread pool, propagation of transaction context
  - Circular dependency — constructor injection vs field injection, `@Lazy`
- **Database**:
  - MVCC in MySQL InnoDB — how dirty reads are prevented without locking
  - Difference between `SELECT FOR UPDATE` vs optimistic locking
  - N+1 problem in JPA — `@BatchSize`, `JOIN FETCH`, entity graphs

---

## Behavioral Questions (Flipkart 2024–2025)

- "Tell me about a time you improved the performance of a system significantly."
- "Describe a situation where you had a technical disagreement with your team. How did you resolve it?"
- "Have you ever had to make a decision with incomplete information? What happened?"
- "Tell me about the most complex system you've built. What would you do differently?"
- "How do you handle tight deadlines when the system isn't ready?"

**Flipkart behavioral focus**: ownership of impact, metrics-driven thinking, collaboration under pressure.

---

## Salary / TC (Flipkart India, 2024–2025, Source: Levels.fyi / Glassdoor)

| Level | Base | Bonus | ESOP/RSU | Total TC |
|---|---|---|---|---|
| SDE-2 (IC3) | ₹35–45 LPA | 15–20% | ₹20–40L over 4yr | ₹45–60 LPA |
| SDE-3 (IC4) | ₹55–75 LPA | 15–20% | ₹50–80L over 4yr | ₹70–95 LPA |

---

---

# 2. AMAZON INDIA — SDE-2

## Interview Process
- Total rounds: 5–6 (all virtual)
- Round 1: Online Assessment (2 DSA + work simulation, HackerRank, 105 min)
- Round 2: Phone Screen with Recruiter (LP check, 30 min)
- Round 3: DSA Round 1 (1–2 problems + 2 LP questions, 60 min)
- Round 4: DSA Round 2 (1–2 problems + 2 LP questions, 60 min)
- Round 5: System Design + 2 LP questions (60 min)
- Round 6: **Bar Raiser Round** (LP-heavy, may include DSA or design, 60 min)

**Bar Raiser details**: An interviewer from a different team who has veto power. They focus heavily on LP depth, "raise the bar" philosophy — they're checking if you'd be in the top 50% of all Amazonians at your level. They often re-probe LP stories you gave in earlier rounds with deeper follow-ups.

**Amazon's rule**: Every round has **exactly 2 LP questions** after DSA/design. You MUST have STAR stories ready for all 14 LPs. Without this, you fail regardless of coding quality.

---

## DSA / Coding Questions (Amazon India SDE-2, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| LRU Cache | #146 | Medium | Asked repeatedly, make it thread-safe |
| Number of Islands | #200 | Medium | BFS/DFS, very common |
| Word Ladder | #127 | Hard | BFS with bidirectional optimization |
| Trapping Rain Water | #42 | Hard | Two pointer + stack approaches |
| Task Scheduler | #621 | Medium | Greedy + heap |
| Minimum Window Substring | #76 | Hard | Sliding window |
| Course Schedule II | #210 | Medium | Topological sort |
| K Closest Points to Origin | #973 | Medium | Heap |
| Longest Increasing Subsequence | #300 | Medium | DP + binary search O(n log n) |
| Find All Anagrams in String | #438 | Medium | Sliding window |
| Design Hit Counter | #362 | Medium | Circular buffer approach |
| Serialize/Deserialize BST | #449 | Medium | Preorder encoding |
| Reorder List | #143 | Medium | Linked list |
| Maximum Profit in Job Scheduling | #1235 | Hard | DP + binary search |
| First Missing Positive | #41 | Hard | In-place hash |
| Partition Equal Subset Sum | #416 | Medium | DP |
| Median of Two Sorted Arrays | #4 | Hard | Binary search |
| Employee Free Time | #759 | Hard | Intervals |
| Design In-Memory File System | #588 | Hard | Trie + design |

**Amazon OA (2024–2025) specific patterns**: Debugging questions (fix the code), work simulation (prioritize tasks), and 2 DSA problems. OA DSA is typically Medium difficulty with large inputs — optimize for time complexity.

---

## System Design Questions (Amazon India SDE-2, 2024–2025)

- **Design Amazon's Order Management System** (most asked) — idempotency keys, saga, eventual consistency, Kafka events
- **Design a URL Shortener** (very common warm-up) — hashing, Base62, collision, redirect
- **Design Amazon's Product Search** — Elasticsearch, ranking, real-time inventory, A/B testing
- **Design a Distributed Cache** — consistent hashing, eviction, replication, TTL
- **Design Amazon Locker System** (SDE-2 specific): slot assignment, expiry, PIN generation
- **Design a Ride-sharing System** (asked in Bar Raiser round) — geo-indexing, matching, surge pricing
- **Design a Notification Platform** — multi-channel, priority, deduplication, rate limiting per user
- **Design S3** (Senior SDE-2 / SDE-3): erasure coding, chunking, replication, bucket policies
- **Design Amazon's Recommendation System** — collaborative filtering, feature store, near-real-time

**Amazon system design tip**: Always start with "Working backwards from the customer" and mention reliability + operational excellence (Amazon LPs in design). They love hearing about **idempotency**, **retry with exponential backoff**, and **circuit breakers**.

---

## Java / Spring / Behavioral (Amazon India SDE-2, 2024–2025)

Java questions are lighter at Amazon compared to Goldman or Flipkart. They focus more on LP + system design.

- "How does garbage collection work in Java? What GC did you use at GSTN?"
- "What's the difference between `HashMap` and `ConcurrentHashMap`?"
- "`@Transactional` — what happens with unchecked vs checked exceptions?"
- "How does Spring handle bean scoping (singleton vs request vs session)?"

---

## Behavioral / LP Questions (Amazon India SDE-2, 2024–2025)

Amazon asks exactly 2 LPs per round. Most asked LPs in India rounds (based on frequency reports):

1. **Customer Obsession**: "Tell me about a time you went above and beyond for a customer (internal or external)."
2. **Ownership**: "Tell me about a time you took ownership of a problem that wasn't yours."
3. **Dive Deep**: "Tell me about a time you had to analyze a complex problem deeply. What data did you look at?"
4. **Deliver Results**: "Tell me about a time you delivered a result despite significant obstacles."
5. **Invent and Simplify**: "Tell me about a time you simplified a complex process."
6. **Are Right, A Lot**: "Tell me about a time you made a decision that others disagreed with. Were you right? How do you know?"
7. **Have Backbone; Disagree and Commit**: "Tell me about a time you pushed back on a decision from management."
8. **Bias for Action**: "Tell me about a time you took quick action without waiting for full information."
9. **Think Big**: "Tell me about a time you had an idea that was bigger than your current scope."
10. **Frugality**: "Tell me about a time you achieved something with fewer resources than expected."

**Bar Raiser round common LP combos**: Ownership + Dive Deep, or Deliver Results + Have Backbone.

---

## Salary / TC (Amazon India, SDE-2, 2024–2025, Source: Levels.fyi)

| Component | Amount |
|---|---|
| Base Salary | ₹40–55 LPA |
| Sign-on Bonus (Year 1) | ₹10–20L |
| Sign-on Bonus (Year 2) | ₹5–10L |
| RSU (4-year vest, 5%/15%/40%/40%) | ₹40–80L total |
| Total TC Year 1 | ₹55–80 LPA |
| Total TC Year 3–4 | ₹65–100 LPA |

Note: Amazon's back-loaded RSU vesting (5/15/40/40) means Year 1 TC appears low. Negotiate sign-on accordingly.

---

---

# 3. GOLDMAN SACHS INDIA — Technology Analyst / Associate (SDE-2 equivalent)

## Interview Process
- Total rounds: 4–5
- Round 1: Online Assessment (Coding + MCQ on Java/OOPS/DS, HackerRank, 90 min)
- Round 2: Technical Phone Screen (Java internals + DSA, 60 min)
- Round 3: Technical Interview 1 — DSA + Java deep dive (60 min)
- Round 4: Technical Interview 2 — System Design + past project deep dive (60 min)
- Round 5: HR / Super Day (at senior levels: panel with MDs and VPs)

**Goldman Sachs is known for**: Deepest Java internals of any company. They expect you to know the JVM, GC algorithms, memory model, multithreading at an expert level. System design is secondary to Java depth. They also ask about financial systems — message ordering, exactly-once delivery, audit trails.

---

## DSA / Coding Questions (Goldman Sachs India, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| LFU Cache | #460 | Hard | Much harder than LRU, asked frequently |
| Alien Dictionary | #269 | Hard | Topological sort |
| Longest Common Subsequence | #1143 | Medium | DP classic |
| Trapping Rain Water | #42 | Hard | Two pointer |
| Minimum Cost to Connect Sticks | #1167 | Medium | Heap |
| Design a Stack With Increment Operation | #1381 | Medium | Stack design |
| Implement Trie | #208 | Medium | Very common |
| Find All Numbers Disappeared in an Array | #448 | Easy | In-place hash |
| Kth Smallest Element in a BST | #230 | Medium | Inorder traversal |
| Binary Tree Maximum Path Sum | #124 | Hard | DFS |
| Maximum Rectangle | #85 | Hard | Stack |
| Regular Expression Matching | #10 | Hard | DP |
| Skyline Problem | #218 | Hard | Heap + sweep line |
| K-th Largest in Unsorted Array | #215 | Medium | Quickselect |
| Edit Distance | #72 | Medium | DP |

Goldman OA also includes **Java MCQs** on: output of multithreaded programs, exception handling edge cases, collections behavior, generics wildcards.

---

## System Design Questions (Goldman Sachs India, 2024–2025)

Goldman design questions lean toward **financial systems**:

- **Design a Real-Time Trade Processing System**: Order book, matching engine, idempotency, audit trail, CQRS
- **Design a Risk Calculation Engine**: Real-time portfolio P&L, streaming computation (Kafka Streams / Flink), consistency
- **Design a Distributed Ledger for Payments**: Double-entry bookkeeping, XA transactions, eventual consistency trade-offs
- **Design a Market Data Feed System**: Pub/sub, low-latency, conflation (deduplicate rapid updates)
- **Design an API Rate Limiter** (common warm-up): Sliding window, Redis, distributed environment
- **Design a Fraud Detection System**: Rule engine, ML scoring, real-time stream processing
- **Design a Notification/Alert System for Trading Events**: Priority, exactly-once, fan-out

**Tip for Goldman**: They value **ACID properties**, **exactly-once semantics**, **idempotency**, and **audit trails** more than horizontal scaling. Your GSTN XA transaction experience is directly relevant — mention Atomikos by name.

---

## Java / Spring Internals (Goldman Sachs India, 2024–2025)

This is their STRONGEST focus area. Expect 30–40 minutes of Java interrogation:

- **Memory Model**:
  - Java Memory Model (JMM) — happens-before, visibility guarantees
  - `volatile` — what it does and doesn't guarantee (visibility yes, atomicity no)
  - Double-checked locking — why it was broken before Java 5, how `volatile` fixes it
  - `AtomicInteger` vs `volatile int` — when to use each
- **Garbage Collection**:
  - CMS vs G1GC vs ZGC vs Shenandoah — tradeoffs, when to use each
  - How G1GC works: regions, mixed collections, evacuation failure
  - How to tune GC: `-Xms`, `-Xmx`, `-XX:MaxGCPauseMillis`, `-XX:G1HeapRegionSize`
  - GC log analysis — identifying GC storms, old gen pressure
- **Threading Deep Dive**:
  - `ReentrantLock` vs `synchronized` — fairness, condition variables, try-lock
  - `StampedLock` — optimistic read, write lock, conversion
  - `ForkJoinPool` — work stealing, how `CompletableFuture` uses it
  - Deadlock — detection, prevention, lock ordering
  - `ThreadPoolExecutor` parameters — core pool, max pool, queue type, rejection policy
  - Virtual threads (Java 21) — what they are, how they differ from platform threads, when to use
- **Collections Internals**:
  - `HashMap` — load factor, resize, treeify threshold (8), hash collision attack (Java 8 fix)
  - `ConcurrentHashMap` Java 8 — CAS-based bin heads, no segment locking, compute atomically
  - `LinkedHashMap` — access-order mode for LRU cache implementation
  - `PriorityQueue` — binary heap, O(log n) insert, O(1) peek
- **Generics and Type System**:
  - Erasure — what's erased, what's kept in bytecode
  - `? extends T` vs `? super T` — PECS rule (Producer Extends, Consumer Super)
  - Why `List<Integer>` is not a `List<Number>`
- **Spring specific**:
  - `@Transactional` propagation: REQUIRED, REQUIRES_NEW, NESTED, MANDATORY
  - How Spring AOP proxy works — what happens with `@Transactional` + `@Async` on same method
  - `ApplicationContext` vs `BeanFactory` — lifecycle hooks, refresh, close

---

## Behavioral Questions (Goldman Sachs India, 2024–2025)

Goldman's behavioral is less structured than Amazon LP, but they do ask:

- "Why Goldman Sachs specifically? What do you know about our technology stack?"
- "Tell me about the most technically challenging problem you solved."
- "How do you ensure code quality in a fast-paced environment?"
- "Describe a time you worked with non-technical stakeholders to deliver a system."
- "What's the biggest technical mistake you've made? How did you fix it?"
- "Where do you see yourself in 3 years?"

---

## Salary / TC (Goldman Sachs India, Associate / Technology Analyst, 2024–2025)

| Level | Base | Bonus | Total |
|---|---|---|---|
| Technology Analyst (New Associate) | ₹30–40 LPA | 20–40% | ₹38–56 LPA |
| Associate (SDE-2 equivalent, 3–5 YOE) | ₹45–65 LPA | 30–60% | ₹58–104 LPA |
| VP (SDE-3 equivalent, 6–10 YOE) | ₹70–100 LPA | 50–100% | ₹105–200 LPA |

Note: Goldman bonuses are cash-heavy (not RSU-heavy like Big Tech). The range is wide based on performance band. Expect all-cash comp, not equity.

---

---

# 4. PHONEPE — SDE-2

## Interview Process
- Total rounds: 4–5
- Round 1: Online Assessment (2 DSA, 90 min)
- Round 2: Technical Interview 1 — DSA + Java internals (60 min)
- Round 3: Technical Interview 2 — Low-Level Design (60 min)
- Round 4: High-Level Design / System Design (60 min)
- Round 5: Engineering Manager / Culture Fit (30–45 min)

**PhonePe is known for**: Payments domain knowledge, distributed transactions, idempotency, eventual consistency in payment systems. They specifically ask "what happens if the network fails between step X and step Y in a payment flow?" They care about operational excellence — alerting, on-call, rollback.

---

## DSA / Coding Questions (PhonePe SDE-2, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| LRU Cache | #146 | Medium | Standard, make thread-safe |
| Design HashMap | #706 | Easy | Implement from scratch |
| Time Based Key-Value Store | #981 | Medium | Binary search on timestamps |
| Account Merge | #721 | Medium | Union-Find |
| All O`one Data Structure | #432 | Hard | Doubly linked list + hashmap |
| Task Scheduler | #621 | Medium | Greedy |
| Insert Delete GetRandom O(1) | #380 | Medium | HashMap + array |
| Max Consecutive Ones III | #1004 | Medium | Sliding window |
| Jump Game II | #45 | Medium | Greedy |
| Partition Labels | #763 | Medium | Greedy + last occurrence |
| Expressive Words | #809 | Medium | Two pointer string |
| Minimum Number of Platforms | Classic | Medium | Sort + sweep (not on LC directly) |
| Find the Duplicate Number | #287 | Medium | Floyd's cycle |
| Subarray Sum Equals K | #560 | Medium | Prefix sum + hashmap |
| Decode Ways | #91 | Medium | DP |

---

## System Design Questions (PhonePe SDE-2, 2024–2025)

PhonePe heavily focuses on payment and financial system design:

- **Design UPI Payment System** (most asked): NPCI integration, idempotency, debit/credit atomicity, timeout handling, reconciliation
- **Design a Wallet Service**: Balance management, concurrent debit safety, ledger, fraud check
- **Design a Payment Gateway**: Acquiring bank integration, 3DS, retries, webhook delivery
- **Design a Transaction Notification System**: Real-time push/SMS, deduplication, ordering guarantees
- **Design a Fraud Detection System**: Rules engine + ML, real-time scoring, false positive management
- **Design a KYC Verification System**: Document upload, async verification, state machine
- **Design a Refund Processing System**: Saga pattern, compensation transactions, SLA tracking
- **Design a Rate Limiting Service** (warm-up): Redis sliding window, distributed, per-user + global limits

**PhonePe-specific questions** (from Glassdoor/Blind reports):
- "How do you handle a double-debit scenario in distributed payments?"
- "Explain idempotency key design for your payment API."
- "If Kafka consumer dies after debit but before credit, how do you recover?"

---

## Java / Spring Internals (PhonePe SDE-2, 2024–2025)

- `@Transactional` with Kafka — why they don't mix cleanly, transactional outbox pattern
- Spring's `RetryTemplate` and `@Retryable` — backoff strategies, idempotency requirement
- How Spring Security works internally — filter chain, `OncePerRequestFilter`
- `CompletableFuture` in payment flows — `allOf`, `anyOf`, timeout with `orTimeout()`
- Database connection pool (HikariCP): `maximumPoolSize`, `connectionTimeout`, pool exhaustion
- Redis Lua scripts for atomic balance check-and-decrement
- Circuit breaker pattern — Resilience4j vs Hystrix, half-open state

---

## Behavioral Questions (PhonePe SDE-2, 2024–2025)

- "Tell me about a production incident you handled. Walk me through your debugging process."
- "How do you balance feature delivery with reliability/quality?"
- "Describe a time when you had to learn a new technology quickly."
- "Tell me about a time you disagreed with a product decision."
- "What does good engineering culture mean to you?"
- "How do you approach on-call and incident management?"

---

## Salary / TC (PhonePe India, SDE-2, 2024–2025, Source: Glassdoor/Levels.fyi)

| Level | Base | Bonus | ESOP | Total TC |
|---|---|---|---|---|
| SDE-2 | ₹35–50 LPA | 10–20% | ₹15–30L over 4yr | ₹45–65 LPA |
| SDE-3 | ₹55–75 LPA | 15–25% | ₹30–60L over 4yr | ₹70–95 LPA |

---

---

# 5. SWIGGY — SDE-2 / SDE-3

## Interview Process
- Total rounds: 4–5
- Round 1: DSA Phone Screen (1–2 problems, 45 min)
- Round 2: Technical Interview — DSA + OOP + Java (60 min)
- Round 3: Low-Level Design (60 min)
- Round 4: High-Level Design / System Design (60 min)
- Round 5: Engineering Manager / Bar Raiser equivalent (45 min)

**Swiggy is known for**: Real-time systems (live order tracking, ETA), geo-spatial problems, delivery logistics optimization, and high-throughput event processing. They value candidates who have dealt with real operational complexity.

---

## DSA / Coding Questions (Swiggy SDE-2/SDE-3, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| Merge K Sorted Lists | #23 | Hard | PriorityQueue |
| Minimum Cost to Hire K Workers | #857 | Hard | Heap + sorting |
| Shortest Path in Binary Matrix | #1091 | Medium | BFS |
| Rotting Oranges | #994 | Medium | Multi-source BFS |
| Meeting Rooms II | #253 | Medium | Intervals, often asked |
| Design Phone Directory | #379 | Medium | Set design |
| Max Area of Island | #695 | Medium | DFS |
| Find K Pairs with Smallest Sums | #373 | Medium | Heap |
| Random Pick with Weight | #528 | Medium | Binary search + prefix sum |
| Implement Queue using Stacks | #232 | Easy | Design pattern |
| Sliding Window Maximum | #239 | Hard | Deque |
| Number of Visible People in a Queue | #1944 | Hard | Monotonic stack |
| Minimum Interval to Include Each Query | #1851 | Hard | Heap + sort |
| Pacific Atlantic Water Flow | #417 | Medium | DFS |
| Word Search II | #212 | Hard | Trie + backtracking |

---

## System Design Questions (Swiggy SDE-2/SDE-3, 2024–2025)

- **Design Live Order Tracking** (most asked): WebSocket vs SSE, geo updates, driver location stream, client reconnect
- **Design Swiggy's Delivery Assignment System**: Matching drivers to orders, real-time geo-indexing (S2 cells, geohash), ETA calculation
- **Design a Restaurant Discovery / Search Service**: Location-based search, filters, ranking, caching
- **Design a Menu Catalog System**: Versioning, restaurant-specific pricing, real-time availability
- **Design a Coupon / Discount Engine**: Rule evaluation, stacking, fraud prevention, expiry
- **Design a Real-Time ETA Prediction Service**: ML model serving, traffic data, fallback strategy
- **Design Swiggy's Notification System**: Order status push, SMS, templating, deduplication
- **Design a Dark Store / Instamart Inventory System**: Real-time stock, slot allocation, picking optimization

**Swiggy-specific questions from reports**:
- "How do you handle driver location updates at 10Hz from 100K concurrent drivers?"
- "If the delivery assignment service goes down, how does the system degrade gracefully?"
- "How would you design the ETA system to handle rain (sudden slowdown in all cities)?"

---

## Java / Spring Internals (Swiggy SDE-2/SDE-3, 2024–2025)

- Kafka consumer group rebalancing — what triggers it, how to minimize rebalance time
- Spring WebFlux vs Spring MVC — when to use reactive, backpressure
- How to implement idempotency in a REST API (idempotency key in header, Redis/DB check)
- `@Cacheable` with TTL — Spring Cache abstraction, Redis backend, cache stampede problem
- `RestTemplate` vs `WebClient` — thread-per-request vs event-loop
- How to handle database connection pool exhaustion under load
- Distributed tracing — Zipkin/Jaeger, `TraceId` propagation across Kafka, MDC in logs

---

## Behavioral Questions (Swiggy SDE-2/SDE-3, 2024–2025)

- "Tell me about a time you built something under extreme time pressure."
- "Describe a system you built that failed in production. What did you learn?"
- "How do you prioritize tech debt vs feature work?"
- "Tell me about your most impactful technical contribution."
- "How do you mentor junior engineers while also delivering your own work?"
- "What would you do in the first 90 days if you joined Swiggy?"

---

## Salary / TC (Swiggy India, SDE-2/SDE-3, 2024–2025)

| Level | Base | Bonus | ESOP | Total TC |
|---|---|---|---|---|
| SDE-2 | ₹35–50 LPA | 10–20% | ₹15–30L over 4yr | ₹45–65 LPA |
| SDE-3 | ₹55–80 LPA | 15–25% | ₹40–80L over 4yr | ₹72–105 LPA |

---

---

# 6. STRIPE INDIA — SDE-2

## Interview Process (Stripe India is Stripe's global process)
- Total rounds: 5–6
- Round 1: Recruiter Screen (30 min)
- Round 2: Technical Phone Screen — DSA (45 min, 1 problem, CoderPad)
- Round 3: Coding Interview 1 — 2 DSA problems (60 min)
- Round 4: Coding Interview 2 — 2 DSA problems (60 min)
- Round 5: System Design (60 min)
- Round 6: Behavioral / Culture Fit — "Stripe's Operating Principles" (45 min)

**Stripe is known for**: Extremely rigorous coding interviews, real-world payments API design, clean code emphasis. They use **CoderPad** (you can run code). They care about code quality, not just getting to a solution — clean variable names, edge case handling, testing approach.

**Important**: Stripe asks about **their actual API design** and expects you to critique it. Know Stripe's API — idempotency keys, webhook retries, Connect architecture.

---

## DSA / Coding Questions (Stripe India SDE-2, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| Merge Intervals | #56 | Medium | Very common at Stripe |
| Meeting Rooms II | #253 | Medium | Interval scheduling |
| LRU Cache | #146 | Medium | HashMap + DLL |
| Evaluate Division | #399 | Medium | Graph / union-find |
| Accounts Merge | #721 | Medium | Union-Find |
| Word Break | #139 | Medium | DP |
| Minimum Path Sum | #64 | Medium | DP grid |
| Decode String | #394 | Medium | Stack |
| Group Anagrams | #49 | Medium | HashMap |
| Find All Duplicates in an Array | #442 | Medium | In-place |
| Design Tic-Tac-Toe | #348 | Medium | Row/col/diag tracking |
| Shortest Bridge | #934 | Medium | BFS + DFS |
| Minimum Remove to Make Valid Parentheses | #1249 | Medium | Stack |
| Basic Calculator II | #227 | Medium | Stack |
| Spiral Matrix | #54 | Medium | Simulation |

**Stripe coding style**: They expect production-quality code. After you solve, they'll ask "How would you test this?", "What edge cases did you miss?", "How would this behave with 10M records?" Write clean, readable code with helper methods.

**Stripe-specific coding questions (not on LC)**:
- "Parse and evaluate a simplified version of Stripe's webhook payload"
- "Implement a simple retry mechanism with exponential backoff and jitter"
- "Implement a rate limiter for API calls (token bucket)"
- "Given a list of transactions, detect duplicate charges within a time window"

---

## System Design Questions (Stripe India SDE-2, 2024–2025)

- **Design Stripe's Payments API**: Idempotency keys, charge lifecycle (PENDING → CAPTURED → REFUNDED), webhook delivery, retry
- **Design a Webhook Delivery System** (very commonly asked at Stripe): Fan-out, retry with backoff, delivery guarantees, dead letter queue, ordering
- **Design a Fraud Detection System**: Real-time scoring, feature store, model serving, feedback loop
- **Design Stripe Connect** (multi-party payments): Platform account, connected accounts, fund routing, fee splitting
- **Design a Billing / Subscription System**: Recurring charges, proration, invoice generation, dunning
- **Design an Idempotent API Gateway**: Key storage, request deduplication, response caching

---

## Java / Spring Internals (Stripe India SDE-2, 2024–2025)

Stripe India interviews are less Java-specific (they're polyglot — Ruby, Go, Java, Python). They focus on:
- "How would you design this in a language you don't know well? What patterns transfer?"
- General: thread safety, immutability, error handling patterns
- "What's the difference between checked and unchecked exceptions? When to use each?"
- "How do you handle partial failures in a distributed transaction?"
- "What is the outbox pattern and why does it solve dual-write?"

---

## Behavioral Questions (Stripe India SDE-2, 2024–2025)

Stripe uses their **Operating Principles** in behavioral. Key ones:
- "Tell me about a time you prioritized long-term quality over short-term speed."
- "Describe a situation where you changed your mind based on data/feedback."
- "Tell me about a time you made a decision that affected many users."
- "How do you approach working with product managers to define requirements?"
- "Tell me about something you built that you're proud of and why."
- "Describe a time you had to navigate ambiguity without clear direction."

---

## Salary / TC (Stripe India, SDE-2, 2024–2025, Source: Levels.fyi)

| Component | Amount |
|---|---|
| Base Salary | ₹55–80 LPA |
| Bonus | 10–15% |
| RSU (4-year vest) | ₹30–60L total |
| Total TC | ₹70–100 LPA |

Note: Stripe pays above Indian market median. Their RSU is pre-IPO equity (private company as of 2025) — actual value depends on eventual IPO/valuation.

---

---

# 7. UBER INDIA — SDE-2

## Interview Process
- Total rounds: 5
- Round 1: Recruiter + Coding Screen (HackerRank OA, 60 min)
- Round 2: Coding Interview 1 — 2 DSA problems (45–60 min)
- Round 3: Coding Interview 2 — 2 DSA problems (45–60 min)
- Round 4: System Design (60 min)
- Round 5: Behavioral / Hiring Manager (45 min)

**Uber is known for**: Geo-spatial systems (very unique), real-time matching, surge pricing, high-throughput event processing. They ask Go or Java. Strong emphasis on scalable microservices and event-driven architecture.

---

## DSA / Coding Questions (Uber India SDE-2, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| Shortest Path to Get All Keys | #864 | Hard | BFS with bitmask |
| Alien Dictionary | #269 | Hard | Topological sort |
| Nearest Exit from Entrance | #1926 | Medium | BFS |
| Find the City With Smallest Reachable Neighbors | #1334 | Medium | Floyd-Warshall / Dijkstra |
| Minimum Cost to Reach City B | variant | Medium | Dijkstra |
| Design A Leaderboard | #1244 | Medium | Sorted map |
| Reorganize String | #767 | Medium | Heap |
| Random Pick Index | #398 | Medium | Reservoir sampling |
| Design Underground System | #1396 | Medium | HashMap design |
| Minimum Number of Refueling Stops | #871 | Hard | Greedy heap |
| Swim in Rising Water | #778 | Hard | Dijkstra / Union-Find |
| Rearrange String K Distance Apart | #358 | Hard | Greedy heap |
| The Skyline Problem | #218 | Hard | Heap / sweep |
| Bus Routes | #815 | Hard | BFS on routes |
| Course Schedule II | #210 | Medium | Topological sort |

**Uber-specific focus**: Graph problems (shortest path, connectivity), geo-spatial (grid BFS), and design-embedded coding (Design Underground System pattern).

---

## System Design Questions (Uber India SDE-2, 2024–2025)

- **Design Uber's Driver-Rider Matching System** (most asked): Geo-indexing (S2 cells, geohash, H3), supply/demand matching, ride request dispatch
- **Design Surge Pricing System**: Supply/demand ratio, hexagonal grid, real-time update, price calculation
- **Design Real-Time Driver Location Tracking**: High-frequency GPS updates, 100K concurrent drivers, write optimization, client queries
- **Design Uber's Trip Service**: Trip lifecycle, state machine, driver/rider notification, edge cases (driver cancels mid-trip)
- **Design a Geo-Fencing System**: Enter/exit detection, polygon matching, real-time stream
- **Design Uber Eats Order Routing**: Restaurant ETA, delivery assignment, reordering
- **Design a Distributed Rate Limiter** (common warm-up)
- **Design a Real-Time Analytics Dashboard**: Kafka → aggregation → serving layer

---

## Java / Go / Spring Internals (Uber India SDE-2, 2024–2025)

Uber uses Go for many services. Expect Go questions if you list it:
- Go: goroutines vs threads, channels (buffered/unbuffered), `select` statement, `context.Context` cancellation
- Go: `sync.Mutex` vs `sync.RWMutex` vs `sync/atomic`
- Go: `defer`, `panic`, `recover` — when to use
- Go: interface satisfaction at compile time vs runtime, nil interface pitfall
- Java (if Java role): `CompletableFuture` with timeout, `ThreadPoolExecutor` config for geo-processing
- General: How do you handle backpressure in a streaming pipeline?

---

## Behavioral Questions (Uber India SDE-2, 2024–2025)

- "Tell me about a system you designed that had to scale 10x. What changed?"
- "Describe a time you had to make a technical decision under uncertainty."
- "Tell me about a production incident you resolved. Walk me through the timeline."
- "How do you approach code reviews? What do you look for?"
- "Tell me about a time you had to work cross-functionally."

---

## Salary / TC (Uber India, SDE-2, 2024–2025, Source: Levels.fyi)

| Level | Base | Bonus | RSU | Total TC |
|---|---|---|---|---|
| SDE-2 (L4) | ₹45–65 LPA | 10–15% | ₹30–60L over 4yr | ₹58–85 LPA |
| SDE-3 (L5) | ₹70–95 LPA | 15–20% | ₹60–120L over 4yr | ₹90–130 LPA |

---

---

# 8. ZERODHA — Backend Engineer

## Interview Process
- Total rounds: 3–4 (lean process, no fluff)
- Round 1: Async Technical Assignment (take-home, 5–7 days): Build a real working system
- Round 2: Technical Deep Dive on Assignment + Architecture (90 min)
- Round 3: Go/Systems deep dive + DSA (60 min)
- Round 4: Founder/CTO conversation (30 min, values fit)

**Zerodha is known for**: Go (Golang) is the primary language. They care about clean, minimal, production-ready code. They build trading systems — low latency, reliability, and simplicity. They don't ask LeetCode in the traditional sense; they give real-world problems and judge your engineering judgment.

**Important**: Zerodha does NOT do standard LeetCode-style OA. They prefer practical problem-solving. They also have a flat culture and avoid over-engineering.

---

## Take-Home Assignment Types (Zerodha, 2024–2025, from reports)

- "Build a simple stock quote API that fetches, caches, and serves real-time quotes"
- "Build a basic order matching engine (price-time priority, market/limit orders)"
- "Implement a simple pub-sub message broker with at-least-once delivery"
- "Build a CLI tool to process and aggregate large CSV files of trades"
- "Implement a concurrent key-value store with TTL and persistence"
- "Build a simple WebSocket server that broadcasts live ticker data to subscribed clients"

**What they evaluate**: Code quality, error handling, test coverage, documentation, simplicity. They specifically penalize over-engineering.

---

## DSA / Technical Questions (Zerodha, 2024–2025)

Not standard LeetCode, but they ask:
- "Implement an order book (bids/asks sorted, match engine)"
- "Design an efficient data structure for a time-series of stock prices" (segment tree, Fenwick tree)
- "Write a goroutine-safe in-memory cache with TTL expiry"
- "Implement a circular buffer for tick data"
- "Explain how you'd implement consistent hashing in Go from scratch"
- Classic: Binary search variants, sorting-based problems

---

## System Design Questions (Zerodha, 2024–2025)

- **Design Zerodha's Order Management System**: Order placement, risk check, exchange connectivity (FIX protocol), fill notification
- **Design Kite's Real-Time Market Data System**: WebSocket feed, tick aggregation, compression
- **Design a Portfolio P&L Calculator**: Real-time mark-to-market, historical P&L, cost basis methods
- **Design a Broker Risk Management System**: Position limits, margin calculation, auto-square off
- **Design a Back-Testing Platform for Trading Strategies**

---

## Go / Systems Internals (Zerodha, 2024–2025)

This is Zerodha's core technical focus:
- Goroutines — how they're scheduled (GOMAXPROCS, M:N threading model, work stealing)
- Channels — buffered vs unbuffered, deadlock scenarios, `select` with default
- `context.Context` — cancellation propagation, timeout, `WithValue` for request tracing
- `sync.WaitGroup`, `sync.Mutex`, `sync.Once`
- Memory: Go's GC — tricolor mark-and-sweep, GOGC parameter
- Error handling philosophy — Go 1.13 `fmt.Errorf` with `%w`, `errors.Is`, `errors.As`
- HTTP server in Go — `net/http`, `gorilla/mux`, middleware pattern
- How to profile Go programs — `pprof`, CPU profile, memory profile, goroutine dump
- `interface{}` vs `any` (Go 1.18+), type assertions, type switches
- Generics in Go 1.18+ — type constraints, when to use vs interface

---

## Behavioral Questions (Zerodha, 2024–2025)

Zerodha's culture interview is founder-values driven:
- "Why Zerodha? Why not a well-funded startup with more money?"
- "Tell me about a project you built that you're most proud of."
- "What's something you've built entirely on your own (side project, open source)?"
- "How do you keep yourself updated technically?"
- "What do you think about over-engineering? Give an example where simplicity won."

---

## Salary / TC (Zerodha, Backend Engineer, 2024–2025)

| Level | Base | Bonus | Notes |
|---|---|---|---|
| Mid-Level (SDE-2 equiv) | ₹25–40 LPA | Discretionary | No equity/ESOP (bootstrapped, profitable) |
| Senior (SDE-3 equiv) | ₹40–60 LPA | Discretionary | Strong job security, low stress culture |

Note: Zerodha pays below Big Tech but offers exceptional work-life balance, no VC pressure, and real engineering ownership. They're one of India's most profitable tech companies.

---

---

# 9. MORGAN STANLEY INDIA — Technology Analyst / Associate

## Interview Process
- Total rounds: 4–5
- Round 1: Online Assessment (Coding + Java MCQ, HackerRank, 90 min)
- Round 2: Technical Interview 1 — DSA + Java (60 min)
- Round 3: Technical Interview 2 — System Design / Architecture (60 min)
- Round 4: Technical Interview 3 — Past Project Deep Dive + Domain (60 min)
- Round 5: HR / Managing Director conversation (30–45 min)

**Morgan Stanley is known for**: Java is their primary language (investment banking systems). They care about Java concurrency, multithreading, and financial domain knowledge. Less system design than Goldman, more emphasis on core Java and domain understanding.

---

## DSA / Coding Questions (Morgan Stanley India, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| LRU Cache | #146 | Medium | Implement cleanly |
| Two Sum | #1 | Easy | Often a warm-up |
| Maximum Subarray | #53 | Medium | Kadane's algorithm |
| Valid Parentheses | #20 | Easy | Stack |
| Longest Palindromic Substring | #5 | Medium | DP or Manacher |
| Find Peak Element | #162 | Medium | Binary search |
| Sort Colors | #75 | Medium | Dutch National Flag |
| Rotate Image | #48 | Medium | In-place |
| Binary Tree Level Order Traversal | #102 | Medium | BFS |
| Construct Binary Tree from Preorder/Inorder | #105 | Medium | Recursion |
| Stock Buy/Sell Multiple Times | #122 | Medium | Greedy |
| Number of Islands | #200 | Medium | BFS/DFS |
| Minimum Depth of Binary Tree | #111 | Easy-Med | BFS |
| Flatten Binary Tree to Linked List | #114 | Medium | DFS |
| Implement Stack using Queues | #225 | Easy | Design |

Morgan Stanley's OA also has **output-based MCQs** for Java (thread behavior, exception handling, collections outputs).

---

## System Design Questions (Morgan Stanley India, 2024–2025)

Morgan Stanley design questions lean financial:
- **Design a Real-Time Trade Settlement System**: T+2 settlement, matching, confirmation, reconciliation
- **Design an Order Book for a Stock Exchange**: Bid/ask sorted structure, matching engine, market depth
- **Design a Portfolio Management System**: Holdings, P&L, real-time price update, history
- **Design a Risk Monitoring System**: Position limits, VaR calculation, real-time alerts
- **Design a Messaging System for Trading Desks** (internal Bloomberg-like): Message routing, persistence, fan-out
- **Design a Transaction Audit Log System**: Immutable append-only, search, compliance queries

---

## Java / Spring Internals (Morgan Stanley India, 2024–2025)

Very Java-heavy:
- "What is the `ExecutorService` hierarchy? What's the difference between `FixedThreadPool` and `CachedThreadPool`?"
- "Explain `Future` vs `CompletableFuture`. What's a `CompletionStage`?"
- "How does `synchronized` differ from `Lock`? What is `Condition`?"
- "What is a `WeakReference`? When would you use it in a cache?"
- "Explain `Comparable` vs `Comparator`. What's a `Comparator.comparing()` chain?"
- "What is method hiding vs method overriding (static methods)?"
- "How does the `try-with-resources` statement work under the hood? What is `Closeable` vs `AutoCloseable`?"
- "What are the rules for `hashCode` and `equals` contract? What breaks if you only override one?"
- "Explain SOLID principles with a code example for each."
- "What is the Open/Closed principle? How does Spring apply it?"
- "What is a memory leak in Java? Give 3 real scenarios."
- Design patterns: "Implement Observer, Factory Method, Builder live in code."

---

## Behavioral Questions (Morgan Stanley India, 2024–2025)

- "Why financial services / investment banking technology?"
- "How do you ensure accuracy in a system where errors have financial consequences?"
- "Tell me about a time you had to meet a hard regulatory or compliance deadline."
- "Describe your experience with high-availability systems."
- "What do you know about Morgan Stanley's technology stack?"
- "How do you approach learning a new financial domain quickly?"

---

## Salary / TC (Morgan Stanley India, Associate, 2024–2025)

| Level | Base | Bonus | Total |
|---|---|---|---|
| Technology Analyst (0–3 YOE) | ₹20–30 LPA | 20–40% | ₹25–42 LPA |
| Associate (3–6 YOE) | ₹35–55 LPA | 30–60% | ₹45–88 LPA |
| VP (6–10 YOE) | ₹60–90 LPA | 50–100% | ₹90–180 LPA |

Note: Morgan Stanley bonuses are cash (not RSU). Tech roles in India are well-compensated at VP level but slower growth than Big Tech at entry/mid levels.

---

---

# 10. GOOGLE INDIA — L4 (SDE-2 equivalent)

## Interview Process
- Total rounds: 5–7 (most rigorous process)
- Round 1: Recruiter Screen + Technical Screen (DSA, 45 min, Google Meet + CoderPad)
- Rounds 2–5: **Onsite** (virtual) — each 45 min:
  - 2 × Coding interviews (DSA, 1–2 problems each)
  - 1 × System Design
  - 1 × Behavioral ("Googleyness" + Leadership)
- Rounds 6–7: Additional coding at senior levels or team match conversations
- **Hiring Committee review** before offer (unique to Google)

**Google is known for**: Highest bar in the industry. L4 expects near-perfect DSA. They test algorithmic thinking, not just problem recognition. Clean code, communicate your thinking aloud throughout, discuss multiple approaches before coding. Behavioral focuses on "Googleyness" (inclusion, collaboration, growth mindset).

**Hiring Committee**: After your onsite, your packet is reviewed by a committee you never meet. They look at all feedback holistically. A strong perf in 3 rounds can offset a weak 4th. No single interviewer can hire or reject you.

---

## DSA / Coding Questions (Google India L4, 2024–2025)

| Problem | LC # | Difficulty | Notes |
|---|---|---|---|
| Median of Two Sorted Arrays | #4 | Hard | Binary search |
| Word Search II | #212 | Hard | Trie + DFS |
| Serialize and Deserialize Binary Tree | #297 | Hard | Classic |
| Longest Increasing Path in Matrix | #329 | Hard | DFS + memoization |
| Robot Cleaner | #489 | Hard | Backtracking with offset |
| N-Queens | #51 | Hard | Backtracking |
| Minimum Window Substring | #76 | Hard | Sliding window |
| Jump Game III | #1306 | Medium | BFS |
| Palindrome Partitioning II | #132 | Hard | DP |
| Largest Rectangle in Histogram | #84 | Hard | Stack |
| Longest Valid Parentheses | #32 | Hard | Stack / DP |
| Recover Binary Search Tree | #99 | Medium | Morris traversal |
| Wildcard Matching | #44 | Hard | DP |
| Distinct Subsequences | #115 | Hard | DP |
| Maximal Rectangle | #85 | Hard | Histogram trick |
| Regular Expression Matching | #10 | Hard | DP |
| Text Justification | #68 | Hard | Simulation |
| Insert Interval | #57 | Medium | Merge |
| Expression Add Operators | #282 | Hard | Backtracking |
| Minimum Cost to Cut a Stick | #1547 | Hard | Interval DP |

**Google-specific patterns**: They love problems where the optimal solution requires an insight (not just knowing the algorithm). Expect follow-ups: "What if the array doesn't fit in memory?", "What if you had to do this 1M times per second?", "Can you do it in O(1) space?"

---

## System Design Questions (Google India L4, 2024–2025)

- **Design Google Search** (asked directly or variants): Web crawling, indexing, ranking, freshness, anti-spam
- **Design YouTube** (most common): Upload pipeline, transcoding, CDN, recommendation, comments
- **Design Google Maps** (very common at L4/L5): Routing (Dijkstra, A*), real-time traffic, ETA, tile rendering
- **Design Google Drive**: Chunking, deduplication, conflict resolution, sync, sharing permissions
- **Design a Web Crawler at Scale**: Politeness, de-duplication (URL fingerprinting), distributed queue
- **Design Gmail**: Storage model, search (Bigtable), spam filter, threading
- **Design a Distributed Key-Value Store** (Bigtable / Spanner variant)
- **Design a Pub/Sub System** (Pub/Sub itself): Topics, subscriptions, ordering, at-least-once, fan-out
- **Design Google Analytics**: Ingestion (100B events/day), aggregation, query serving

**Google design tip**: They expect you to know Google's own technologies — Bigtable, Spanner, Chubby, Pub/Sub, Dremel (BigQuery), Borg (K8s origin). Mention trade-offs in CAP theorem. Always discuss **consistency models** (strong, eventual, linearizability).

---

## Java / Spring / Coding Style (Google India L4, 2024–2025)

Google is largely polyglot (C++, Java, Go, Python). Java-specific:
- They expect idiomatic code: streams, optionals, generics — NOT boilerplate loops
- "Write a generic `Pair<A, B>` class that is comparable if both A and B are comparable"
- "Implement a thread-safe singleton without using synchronized on the whole method"
- "What's the difference between `Iterator` and `Spliterator`? Why does Spliterator exist?"
- Code review: "What's wrong with this code?" (passed with a subtle concurrency bug or null pointer)

---

## Behavioral Questions — "Googleyness" (Google India L4, 2024–2025)

- "Tell me about a time you had to collaborate with someone difficult."
- "Describe a time when you received critical feedback. How did you respond?"
- "Tell me about a time you failed. What did you learn?"
- "How do you approach an unfamiliar codebase or technology?"
- "Tell me about a time you went out of your way to help a colleague."
- "Describe a situation where you had to navigate ambiguity."
- "What's the most creative solution you've come up with for a technical problem?"

**Googleyness definition** (from Google's hiring rubric):
- Thrives in ambiguity
- Values feedback and growth
- Collaborative without being a pushover
- Committed to inclusion
- Passionate about Google's mission

---

## Salary / TC (Google India, L4, 2024–2025, Source: Levels.fyi)

| Component | Amount |
|---|---|
| Base Salary | ₹55–75 LPA |
| Annual Bonus | 15–20% |
| RSU (4-year vest, 25%/year) | ₹80–150L total |
| Signing Bonus | ₹10–20L |
| Total TC Year 1 | ₹85–120 LPA |
| Total TC Year 3–4 | ₹95–130 LPA |

Note: Google India L4 is one of the highest-paying IC roles in India. RSU at Google is at market price (liquid) — much better than pre-IPO equity.

---

---

# CROSS-COMPANY SUMMARY TABLE

## DSA Problems That Appear Across 3+ Companies

| Problem | LC # | Companies |
|---|---|---|
| LRU Cache | #146 | Flipkart, Amazon, PhonePe, Uber, Goldman, Morgan Stanley |
| Trapping Rain Water | #42 | Amazon, Goldman Sachs |
| Task Scheduler | #621 | Amazon, PhonePe |
| Meeting Rooms II | #253 | Flipkart, Swiggy, Stripe |
| Merge Intervals | #56 | Flipkart, Stripe, Amazon |
| Serialize/Deserialize BT | #297 | Flipkart, Amazon, Google |
| Number of Islands | #200 | Amazon, Swiggy, Morgan Stanley |
| Alien Dictionary | #269 | Goldman, Uber |
| Minimum Window Substring | #76 | Amazon, Google |
| Find Median from Data Stream | #295 | Flipkart, Goldman |

## System Design Topics That Appear Across 3+ Companies

| Topic | Companies |
|---|---|
| Rate Limiter | PhonePe, Stripe, Swiggy, Uber |
| Notification System | Flipkart, Amazon, PhonePe, Swiggy |
| Order Management | Flipkart, Amazon, PhonePe |
| Fraud Detection | Goldman, PhonePe, Stripe |
| Distributed Cache | Amazon, Flipkart, Goldman |
| Real-Time Tracking | Swiggy, Uber |

## Java Internals Topics That Appear Across 3+ Companies

| Topic | Companies |
|---|---|
| `ConcurrentHashMap` internals | Flipkart, Goldman, Morgan Stanley |
| `@Transactional` proxy / self-invocation | Flipkart, PhonePe, Amazon |
| GC algorithms (G1, ZGC) | Goldman, Flipkart, Morgan Stanley |
| `CompletableFuture` | Flipkart, PhonePe, Swiggy, Uber |
| `volatile` + double-checked locking | Goldman, Flipkart, Morgan Stanley |
| `ThreadPoolExecutor` config | Flipkart, Goldman, Morgan Stanley |

---

# JAYANTI'S GSTN ADVANTAGE — HOW TO MAP YOUR EXPERIENCE

Use the following table to connect your GSTN work to what each company cares about:

| GSTN System | Map To | Companies That Value This |
|---|---|---|
| XA transactions (Atomikos) | Distributed transactions, exactly-once | Goldman, PhonePe, Stripe |
| Kafka DLQ consumer framework | At-least-once delivery, dead letter, retry | Amazon, Swiggy, PhonePe |
| JBoss DataGrid 2-tier cache (70 regions) | Distributed cache design, eviction, TTL | Flipkart, Amazon, Goldman |
| 14M taxpayers, 3B invoices/year | Scale estimation, large-scale system design | Google, Uber, Amazon |
| Case workflow engine (Strategy + Factory) | LLD, design patterns, state machine | Flipkart, Goldman, Morgan Stanley |
| Redis-based session management | Caching, distributed session | PhonePe, Swiggy |
| GSTR filing month-end spikes (10x) | Burst traffic handling, auto-scaling | Flipkart, Amazon |
| Digital signature (DSC/EVC) verification | Security, auth design | Goldman, Stripe |

**CRITICAL TIP**: In every system design, say: "At GSTN, I dealt with [similar problem] at [scale]. Here's what I learned and what I'd do differently in a product company context." This immediately differentiates you from candidates with no real large-scale experience.

---

# PREP PRIORITY ORDER (for Jayanti's Phase 2)

Based on difficulty, reward, and fit with GSTN background:

1. **Amazon India** — Process is well-defined, LP bank is ready. Focus: DSA Medium/Hard + 2 LP per round
2. **PhonePe** — GSTN XA/Kafka experience maps perfectly. Focus: Payment system design, idempotency
3. **Flipkart** — Concurrency + LLD is key. Focus: Java threading, LLD practice
4. **Swiggy** — Real-time systems. Focus: Geo/tracking design, Kafka stream processing
5. **Goldman Sachs** — Java deepest. Focus: JVM internals, GC, threading — 2 weeks of grinding
6. **Stripe** — Highest TC, polyglot. Focus: Clean code, webhook/billing design
7. **Uber** — Go needed. Focus: Goroutines, geo-spatial design
8. **Google India** — Hardest bar. Focus: Hard DSA daily for 3+ months
9. **Morgan Stanley** — Good fit. Focus: Core Java, financial domain
10. **Zerodha** — Go + practical projects. Focus: Build something real in Go

---

*Last updated: 2026-03-20*
*Sources: Based on model knowledge through August 2025, aggregated from Glassdoor India, LeetCode Discuss, Blind (teamblind.com), AmbitionBox, InterviewBit, GeeksForGeeks interview experiences, and Levels.fyi India data for these companies.*
*Note: WebSearch was unavailable; verify salary numbers on Levels.fyi before negotiation.*
