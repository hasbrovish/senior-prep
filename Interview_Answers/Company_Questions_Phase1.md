# Phase 1 Company Interview Question Bank
## Target: SDE-2/SDE-3 Backend — Indian Product Companies (2023–2025)

> Sources synthesized: Glassdoor reviews, LeetCode Discuss, Blind, engineering blogs, interview experience posts.
> Last updated: March 2026. Specific LC problem numbers included where verified.

---

## Table of Contents
1. [Razorpay](#1-razorpay)
2. [CRED](#2-cred)
3. [Juspay](#3-juspay)
4. [Meesho](#4-meesho)
5. [Paytm](#5-paytm)
6. [MakeMyTrip](#6-makemytrip)
7. [Atlassian India](#7-atlassian-india)
8. [Groww](#8-groww)
9. [Walmart Global Tech India](#9-walmart-global-tech-india)
10. [Slice](#10-slice)

---

## 1. Razorpay

### Interview Process
- **Rounds:** 4–5 rounds total
- **Round 1:** Online assessment — 2 DSA problems (90 min), HackerRank/HireVue
- **Round 2:** DSA + Data Structures deep dive (60 min, with interviewer)
- **Round 3:** Low-Level Design (LLD) — class diagrams, OOP design (60 min)
- **Round 4:** High-Level Design / System Design (60–75 min)
- **Round 5:** Hiring Manager / Bar Raiser — behavioral + culture fit + past project depth
- **Total duration:** 2–3 weeks end to end
- **Format:** All virtual (Zoom/Google Meet + CoderPad)

### DSA Questions Asked (Specific)
- **LC 146 — LRU Cache** (extremely common, implement from scratch with O(1) get/put)
- **LC 208 — Implement Trie (Prefix Tree)**
- **LC 56 — Merge Intervals** (variant: merge overlapping payment windows)
- **LC 200 — Number of Islands** (graph variant)
- **LC 23 — Merge K Sorted Lists**
- **LC 76 — Minimum Window Substring**
- **LC 42 — Trapping Rain Water**
- **LC 438 — Find All Anagrams in a String**
- **LC 124 — Binary Tree Maximum Path Sum**
- **LC 1 — Two Sum** (used as warm-up, then extended to variants)
- **LC 253 — Meeting Rooms II** (interval scheduling)
- **LC 297 — Serialize and Deserialize Binary Tree**
- **Sliding window problems** — find max sum subarray of size K
- **Custom:** Design a rate limiter data structure with `allow(userId, timestamp)` method

### System Design Questions
- Design Razorpay Payment Gateway (the most common question)
  - How does a payment go from merchant checkout → bank → success callback?
  - How do you handle idempotency? (webhook retries, duplicate charges)
  - How do you handle refunds atomically?
- Design a Notification Service (SMS/email/webhook delivery with retry)
- Design a Webhook Delivery System — at-least-once delivery, ordering guarantees
- Design a Fraud Detection System — real-time transaction scoring
- Design a Ledger System — double-entry bookkeeping, reconciliation
- Design a Rate Limiter — token bucket vs sliding window, Redis-backed
- Design an Order Management System for payments — state machine, idempotency

### Java / Tech Stack Questions
- Explain Java memory model — heap, stack, metaspace. What triggers OutOfMemoryError?
- Difference between `synchronized`, `ReentrantLock`, `StampedLock` — when to use which
- How does `ConcurrentHashMap` work internally? Segment locking vs Node locking (Java 8+)
- What is a `volatile` variable? Does it guarantee atomicity?
- Explain `CompletableFuture` vs `Future` — how do you chain async operations?
- What is the difference between `@Transactional(propagation=REQUIRES_NEW)` and `NESTED`?
- How does Spring handle circular dependencies? `@Lazy` injection explanation
- What is connection pooling? How does HikariCP work? Key config parameters
- Explain Kafka consumer group rebalancing. What triggers it? How do you minimize rebalance impact?
- How does Redis handle atomicity? When to use Lua scripts vs transactions (`MULTI/EXEC`)?
- Explain idempotency key design for payment APIs
- What is optimistic vs pessimistic locking? When would you use each in a payments context?
- How does database row locking work with `SELECT FOR UPDATE`?

### Behavioral Questions
- Tell me about a time you handled a production incident — what was your process?
- Describe the most complex system you've built. What were the hardest trade-offs?
- Tell me about a disagreement with a senior engineer — how did you resolve it?
- How do you ensure code quality in a fast-moving team?
- Describe a time you had to learn a new technology quickly under pressure
- What's the biggest performance optimization you've done? How did you measure impact?

### Key Focus Areas
1. **Payments domain depth** — idempotency, retries, reconciliation, double-entry ledger
2. **Java concurrency** — this is tested heavily in DSA AND design rounds
3. **LLD quality** — clean OOP, SOLID principles, extensibility
4. **System reliability** — how you handle failure, retries, at-least-once vs exactly-once
5. **Production debugging mindset** — they want engineers who think about failure modes

### Tips for Razorpay
- When solving DSA, explain your reasoning aloud before coding — they value process
- In system design, always bring up idempotency keys and webhook retry strategies unprompted — this signals payments domain expertise
- For LLD round, practice Payment Gateway, Rate Limiter, and Notification Service designs
- Know your Kafka offset management well — they will ask about consumer lag and DLQ
- The bar raiser round will ask "why Razorpay specifically?" — have a detailed answer about their payments infra stack or eng blog posts
- Prepare 2–3 war stories from GSTN production incidents with clear STAR structure

---

## 2. CRED

### Interview Process
- **Rounds:** 4–5 rounds
- **Round 1:** Online assessment — 2–3 DSA problems (Medium difficulty), 90 min
- **Round 2:** Technical Phone Screen — DSA + Java discussion (45 min)
- **Round 3:** System Design (60–75 min) — very architecture-heavy
- **Round 4:** LLD + code quality (60 min)
- **Round 5:** Culture + values fit with engineering manager or VP Eng
- **Total duration:** 3–4 weeks
- **Format:** Virtual, CoderPad for coding

### DSA Questions Asked (Specific)
- **LC 146 — LRU Cache** (implement with HashMap + DoublyLinkedList)
- **LC 295 — Find Median from Data Stream**
- **LC 23 — Merge K Sorted Lists**
- **LC 239 — Sliding Window Maximum**
- **LC 42 — Trapping Rain Water**
- **LC 460 — LFU Cache** (harder variant of LRU)
- **LC 84 — Largest Rectangle in Histogram**
- **LC 127 — Word Ladder** (BFS)
- **LC 300 — Longest Increasing Subsequence** (with O(n log n) solution)
- **LC 772 — Basic Calculator III** (expression parsing)
- **LC 45 — Jump Game II**
- **Custom:** Design an in-memory key-value store with TTL support
- **Custom:** Given a stream of credit card transactions, find the top-K merchants by spend in the last 1 hour (sliding window + heap)

### System Design Questions
- Design CRED's credit card payment system — bill fetch, payment scheduling, reminder system
- Design a Credit Score Calculation Engine — batch vs real-time, explainability
- Design a Rewards and Cashback Engine — rule evaluation, idempotency, rollback
- Design a Notification System at 10M+ users scale — push, SMS, email, in-app
- Design a Feed/Home Screen for CRED app — personalization, caching strategy
- Design a Search system for credit card offers — relevance, filters, latency
- Design a Fraud Detection pipeline — feature engineering, real-time scoring
- Design an AB Testing platform — experiment assignment, metrics tracking

### Java / Tech Stack Questions
- CRED uses Kotlin heavily — do you know Kotlin? (be honest; say you can learn quickly)
- Explain coroutines vs threads — how does Kotlin's coroutines work conceptually?
- What are sealed classes? How would you use them in a payment state machine?
- Explain Spring Boot auto-configuration — how does `@EnableAutoConfiguration` work?
- Deep dive into JVM GC — G1GC vs ZGC vs Shenandoah. When would you tune each?
- How do you do zero-downtime deployments in a Spring Boot microservices environment?
- Explain the outbox pattern for reliable event publishing
- How do you implement distributed tracing across microservices? (Jaeger, Zipkin, OpenTelemetry)
- What is a circuit breaker? How does Resilience4j implement it?
- Explain eventual consistency — give a real example from your work where you accepted it

### Behavioral Questions
- CRED has a "high bar for quality" culture — expect questions about craft and standards
- Tell me about a time you pushed back on a deadline to ensure quality
- Describe your biggest technical failure and what you learned
- How do you decide when to refactor vs add new functionality?
- Tell me about a system you're proud of architecturally — why?
- What's your process when you receive a poorly-specified requirement?
- Describe a time when you mentored a junior engineer — what was your approach?

### Key Focus Areas
1. **Engineering craftsmanship** — clean code, good abstractions, zero shortcuts
2. **Product thinking** — they want engineers who think about user impact, not just implementation
3. **Architecture maturity** — CRED's systems are complex; they test depth, not breadth
4. **Reliability engineering** — circuit breakers, bulkheads, graceful degradation
5. **Data correctness** — especially for financial data (credits, cashback, payments)

### Tips for CRED
- CRED explicitly values "opinionated engineers" — don't give generic answers, have strong technical opinions
- Research CRED's engineering blog (cred.club/blog) — they sometimes ask about their own design decisions
- In system design, don't just describe the happy path — spend significant time on failure scenarios
- CRED's culture round is genuinely a bar — they reject candidates who don't align with "craft over speed"
- If you don't know Kotlin, say so but demonstrate you've read about it and understand its advantages over Java — shows learning agility
- The LLD round values extensibility highly: ask about future requirements before designing

---

## 3. Juspay

### Interview Process
- **Rounds:** 4–5 rounds
- **Round 1:** Online assessment — algorithmic problems, sometimes Haskell-related (but Java/Go accepted)
- **Round 2:** DSA / Problem Solving (heavy on logic, not just coding)
- **Round 3:** System Design — payments routing and distributed systems
- **Round 4:** Technical depth — language internals, functional programming concepts
- **Round 5:** Hiring manager / culture
- **Total duration:** 2–3 weeks
- **Format:** Virtual; they may use their own platform or CoderPad

### DSA Questions Asked (Specific)
- **LC 42 — Trapping Rain Water**
- **LC 1 — Two Sum** (then extended to variants)
- **LC 236 — Lowest Common Ancestor of a Binary Tree**
- **LC 124 — Binary Tree Maximum Path Sum**
- **LC 200 — Number of Islands**
- **LC 297 — Serialize and Deserialize Binary Tree**
- **LC 51 — N-Queens** (backtracking)
- **LC 32 — Longest Valid Parentheses**
- **LC 329 — Longest Increasing Path in a Matrix** (DFS + memoization)
- **Custom:** Implement a payment routing algorithm — given a list of payment gateways with success rates and fees, route a transaction to maximize success probability while minimizing cost (graph/DP)
- **Custom:** Given transaction logs, detect circular payment chains (graph cycle detection)
- **Functional programming concept questions:** Write a `flatMap` implementation. Explain monads intuitively. What is referential transparency?

### System Design Questions
- Design a Payment Routing Engine — multi-gateway routing, fallback, success rate tracking
- Design Juspay's Smart Router — A/B routing, gateway health monitoring, retry logic
- Design a Transaction Orchestration System — multi-step payment flow with compensating transactions
- Design a Merchant Dashboard — real-time transaction analytics, chargebacks, settlements
- Design a Retry Manager for failed payments — exponential backoff, idempotency
- Design a Reconciliation System — matching bank settlements with internal records
- Distributed consensus: how would you implement a distributed lock?

### Java / Tech Stack Questions
- Juspay values functional thinking — even if you write Java, they want functional style
- What is immutability? How do you design immutable objects in Java? (`Record` classes in Java 16+)
- Explain `Optional` in Java — when should you use it? When is it an antipattern?
- What are functional interfaces? Explain `Function<T,R>`, `Predicate<T>`, `Consumer<T>`
- How does `Stream.collect()` work internally? What is a `Collector`?
- Explain monadic design in Java — `CompletableFuture` chaining as a monad
- What is tail recursion? Does Java support it? (No — JVM doesn't optimize tail calls. Workaround: trampoline)
- Explain event sourcing — how does it differ from CQRS?
- What is the saga pattern? Choreography vs orchestration?

### Behavioral Questions
- Why are you interested in payments infrastructure specifically?
- Describe a time you had to understand a complex legacy codebase — how did you approach it?
- Tell me about a bug that was extremely hard to reproduce — how did you find it?
- What is the most creative engineering solution you've implemented?
- How do you approach learning a completely new paradigm (like functional programming)?

### Key Focus Areas
1. **Payments routing logic** — deep understanding of gateway health, fallback strategies
2. **Functional programming mindset** — even in Java/Go, they value immutability and pure functions
3. **Distributed systems correctness** — exactly-once semantics, idempotency, saga
4. **Problem solving approach** — they care about HOW you think, not just the answer
5. **Production reliability** — how do you ensure a payment never gets lost?

### Tips for Juspay
- Even if you won't write Haskell, read the basics of functional programming concepts — they will probe this
- For payment routing design, study real-world gateway failover strategies (primary/secondary, round-robin with health checks, success rate based)
- Juspay interviewers are very senior — don't try to fake knowledge; they will dig until they find your actual depth
- Saga pattern (orchestration vs choreography) is almost guaranteed to come up in system design
- Prepare a strong answer on how you handle partial failures in distributed transactions — this maps directly to your XA/Atomikos work at GSTN

---

## 4. Meesho

### Interview Process
- **Rounds:** 4 rounds
- **Round 1:** Online assessment — 2 DSA problems (Medium), 90 min on HackerEarth
- **Round 2:** Technical Round 1 — DSA + Java concepts (60 min)
- **Round 3:** Technical Round 2 — System Design (60 min)
- **Round 4:** Hiring Manager — behavioral + project depth + culture
- **Total duration:** 2–3 weeks
- **Format:** Virtual

### DSA Questions Asked (Specific)
- **LC 3 — Longest Substring Without Repeating Characters**
- **LC 15 — 3Sum**
- **LC 56 — Merge Intervals**
- **LC 146 — LRU Cache**
- **LC 200 — Number of Islands**
- **LC 207 — Course Schedule** (topological sort / cycle detection)
- **LC 621 — Task Scheduler**
- **LC 347 — Top K Frequent Elements**
- **LC 215 — Kth Largest Element in an Array**
- **LC 973 — K Closest Points to Origin**
- **LC 49 — Group Anagrams**
- **LC 102 — Binary Tree Level Order Traversal**
- **LC 739 — Daily Temperatures** (monotonic stack)
- **Custom:** Given order data (orderId, timestamp, supplierId, amount), find the top-3 suppliers by revenue in the last 7 days — design the data structure

### System Design Questions
- Design Meesho's Product Catalog System — multi-supplier, attribute management, search
- Design an Order Management System for social commerce — order placement, supplier notification, tracking
- Design a Supplier Onboarding System — document verification, catalog upload at scale
- Design Meesho's Logistics Tracking System — real-time package status, last-mile
- Design a Notification System for resellers — 50M+ users, WhatsApp/SMS/push
- Design a Returns and Refund Processing system
- Design a Flash Sale / Inventory Management system — overselling prevention
- Design a Recommendation Engine for Meesho resellers

### Java / Tech Stack Questions
- Explain Spring Boot's bean lifecycle — `@PostConstruct`, `InitializingBean`, `BeanFactoryPostProcessor`
- How does Spring's `@Async` work? What thread pool does it use?
- Explain `@Transactional` pitfalls — self-invocation, checked vs unchecked exceptions
- Difference between `HashMap` and `LinkedHashMap` — when to use each
- How does garbage collection work in Java? Explain minor GC vs major GC
- What is the purpose of `finalize()`? Why is it deprecated?
- How does Hibernate's first-level and second-level cache work?
- Explain N+1 problem in Hibernate — how do you fix it? (`@BatchSize`, `JOIN FETCH`, `EntityGraph`)
- How does Kafka handle message ordering? How do you ensure ordering within a category?
- What is MySQL's MVCC? How does it relate to isolation levels?

### Behavioral Questions
- Meesho has a flat culture — they test for ownership and autonomy
- Tell me about a time you owned a project end-to-end — from design to delivery
- Describe a time you had to work with incomplete requirements — what did you do?
- Tell me about a production incident you led the resolution of
- How do you handle technical debt in a fast-growing codebase?
- Describe a time you had a disagreement with a product manager

### Key Focus Areas
1. **E-commerce domain understanding** — supply chain, catalog, orders, logistics
2. **Java fundamentals and Spring Boot depth** — they go deep on internals
3. **Scale thinking** — Meesho has 140M+ users; every design must handle real scale
4. **Ownership mindset** — they strongly value engineers who drive features independently
5. **Database optimization** — query optimization, indexing, connection pooling

### Tips for Meesho
- Meesho uses HackerEarth for OA — practice on that platform for the UI familiarity
- In system design, always mention how you'd handle a flash sale scenario (inventory atomicity)
- Meesho is very Java-heavy — brush up on Spring Boot internals, not just usage
- The HM round at Meesho is genuinely behavioral — prepare 5 strong STAR stories
- They value "builder" mindset — in every behavioral answer, emphasize ownership over collaboration

---

## 5. Paytm

### Interview Process
- **Rounds:** 4–5 rounds
- **Round 1:** Online assessment — 3 problems (Easy + Medium + Medium/Hard), 90 min
- **Round 2:** Technical Round — DSA + Java internals (60 min)
- **Round 3:** Technical Round — System Design (60 min)
- **Round 4:** Technical/Architecture — deep dive into past projects, architecture decisions
- **Round 5:** HR + CTO/VP level (senior roles)
- **Total duration:** 3–4 weeks
- **Format:** Virtual; older rounds may have been in-person

### DSA Questions Asked (Specific)
- **LC 1 — Two Sum** (always a warm-up)
- **LC 146 — LRU Cache**
- **LC 20 — Valid Parentheses**
- **LC 42 — Trapping Rain Water**
- **LC 141 — Linked List Cycle**
- **LC 206 — Reverse Linked List**
- **LC 102 — Binary Tree Level Order Traversal**
- **LC 56 — Merge Intervals**
- **LC 347 — Top K Frequent Elements**
- **LC 621 — Task Scheduler**
- **LC 23 — Merge K Sorted Lists**
- **LC 76 — Minimum Window Substring**
- **Custom:** Design a system that processes payment refunds — model as a state machine, implement transitions
- **Custom:** Given a list of transactions with timestamps, detect duplicate transactions within a 60-second window per user

### System Design Questions
- Design Paytm Wallet — top-up, transfer, pay merchant, transaction history
- Design a UPI Payment System — VPA resolution, bank adapter, NPCI integration
- Design a Bill Payment System — biller integration, scheduled payments, reminder
- Design Paytm's Transaction Ledger — high-throughput write, audit trail
- Design Paytm's Cashback/Offer Engine — rule evaluation, user targeting
- Design a Real-time Fraud Detection System
- Design Paytm's QR Code Payment System — generation, scan, settlement

### Java / Tech Stack Questions
- Paytm is very Java-heavy — expect deep Java questions
- Explain Java ClassLoader hierarchy. What is the parent delegation model?
- What is the difference between `==` and `.equals()` in Java? How does `String.intern()` work?
- Explain Java's String pool and why String is immutable
- How does `HashMap` handle hash collisions? What is the threshold for tree conversion (8 nodes)?
- Explain the Fork/Join framework — what problem does it solve?
- What is a `ThreadLocal` variable? When is it useful? What are the memory leak risks?
- Explain `synchronized` block vs method — what is the lock object?
- What is the Java Memory Model (JMM)? Explain happens-before relationship
- Explain ACID properties — how does MySQL InnoDB implement them?
- What is a deadlock? Write a code example. How do you detect and prevent it?
- Explain Kafka's `acks=all` vs `acks=1` — when do you use each?
- How does Redis `SETNX` work? How is it used for distributed locking?

### Behavioral Questions
- Tell me about your experience with high-throughput systems
- Describe a time you improved system performance significantly
- How do you handle a situation where your tech lead disagrees with your approach?
- Tell me about a time you had to debug a critical production issue under time pressure

### Key Focus Areas
1. **Java internals** — Paytm goes very deep on JVM, memory, concurrency
2. **Kafka and Redis** — they use both heavily and will test operational knowledge
3. **Financial system design** — idempotency, ledger, double-entry
4. **MySQL optimization** — indexing strategies, query plans, partitioning
5. **Payments domain** — UPI, wallet, reconciliation

### Tips for Paytm
- Paytm's DSA bar is slightly lower than CRED/Razorpay — Medium problems, not Hard
- Java internals are critical here — go deeper than just usage (ClassLoader, JMM, GC algorithms)
- In system design, always bring up the idempotency key pattern for payment APIs
- They have a large legacy codebase — show you can work with legacy systems and improve them incrementally
- Salary negotiation: Paytm has historically offered lower than market — have competing offers ready

---

## 6. MakeMyTrip

### Interview Process
- **Rounds:** 4–5 rounds
- **Round 1:** Online assessment — 2 DSA problems + 20 MCQs (Java concepts), 90 min
- **Round 2:** Technical Round 1 — DSA deep dive (60 min)
- **Round 3:** Technical Round 2 — System Design (60–75 min)
- **Round 4:** Technical Round 3 — LLD or deeper system design
- **Round 5:** HR / hiring manager
- **Total duration:** 3–4 weeks
- **Format:** Virtual

### DSA Questions Asked (Specific)
- **LC 1 — Two Sum**
- **LC 3 — Longest Substring Without Repeating Characters**
- **LC 56 — Merge Intervals** (booking time overlap detection)
- **LC 253 — Meeting Rooms II** (seat/room availability variant)
- **LC 146 — LRU Cache**
- **LC 200 — Number of Islands**
- **LC 207 — Course Schedule**
- **LC 322 — Coin Change**
- **LC 152 — Maximum Product Subarray**
- **LC 1143 — Longest Common Subsequence**
- **LC 79 — Word Search**
- **Custom:** Given a list of flights (source, destination, departure, arrival), find the cheapest path from city A to city B with at most K stops (BFS/DP — similar to LC 787)
- **Custom:** Hotel search: given hotel availability intervals and a booking request, find available hotels (interval overlap)
- **LC 787 — Cheapest Flights Within K Stops** (extremely relevant, very commonly asked)

### System Design Questions
- Design MakeMyTrip's Flight Search System — aggregation from multiple airlines, filters, sorting
- Design a Hotel Booking System — inventory, hold-and-book, overbooking prevention
- Design a Seat Selection System for flights — real-time lock, release after timeout
- Design a Price Alert System — user subscriptions, price change detection, notification
- Design a Travel Itinerary Planner — multi-city, multi-modal (flight + hotel + cab)
- Design a Review and Rating System for hotels
- Design a Search Autocomplete system for city/airport names
- Design a Dynamic Pricing Engine for flights/hotels

### Java / Tech Stack Questions
- Explain how you'd implement a distributed cache with TTL — use cases in travel search
- How does connection pool exhaustion happen? How do you debug it?
- What is the CAP theorem? Where does MySQL fall? Where does Redis fall?
- Explain the difference between `@RestController` and `@Controller` in Spring
- How does Spring MVC handle a request? (DispatcherServlet flow)
- What is the difference between eager and lazy loading in Hibernate?
- How do you handle database transactions spanning multiple microservices?
- Explain retry logic with exponential backoff — implement it
- What is bulkhead pattern? How do you implement it with Resilience4j?

### Behavioral Questions
- Tell me about a time you had to deliver under a tight deadline
- Describe the most complex integration you've built
- How do you ensure your code is maintainable 2 years from now?
- Tell me about a time you identified and fixed a major bug before it hit production

### Key Focus Areas
1. **Travel domain** — bookings, availability, inventory management, pricing
2. **Search and aggregation** — how to search across multiple inventory sources efficiently
3. **Interval/scheduling problems in DSA** — highly domain-relevant
4. **Microservices integration patterns** — circuit breaker, bulkhead, retry
5. **Caching strategy** — travel search results have complex cache invalidation requirements

### Tips for MakeMyTrip
- LC 787 (Cheapest Flights Within K Stops) is almost guaranteed — master it completely
- All interval problems (LC 56, 253, 252) are directly relevant to their booking domain — practice these
- In system design, discuss the seat hold problem carefully (distributed lock with TTL)
- MMT has a large legacy Java codebase — they appreciate engineers who can navigate and improve it
- The MCQ section in OA tests Java knowledge — study Collections API, exceptions, threading basics
- Research MMT's microservices blog posts — they've published about their travel aggregation architecture

---

## 7. Atlassian India

### Interview Process
- **Rounds:** 5–6 rounds (one of the most thorough processes)
- **Round 1:** Recruiter Screen — 30 min, resume discussion
- **Round 2:** Online assessment — 2 DSA problems + system design question (written), 90 min
- **Round 3:** Technical Interview — DSA (45–60 min)
- **Round 4:** Technical Interview — System Design (60 min)
- **Round 5:** Technical Interview — Values / behavioral (using Atlassian values framework)
- **Round 6:** Hiring Manager or Skip-level
- **Total duration:** 3–5 weeks
- **Format:** Virtual; uses their own interviewing platform + Zoom

### DSA Questions Asked (Specific)
- **LC 146 — LRU Cache**
- **LC 236 — Lowest Common Ancestor of Binary Tree**
- **LC 102 — Binary Tree Level Order Traversal**
- **LC 297 — Serialize/Deserialize Binary Tree**
- **LC 23 — Merge K Sorted Lists**
- **LC 347 — Top K Frequent Elements**
- **LC 79 — Word Search**
- **LC 695 — Max Area of Island**
- **LC 200 — Number of Islands**
- **LC 207 — Course Schedule** (dependency graph for JIRA issues)
- **LC 210 — Course Schedule II** (topological sort)
- **LC 560 — Subarray Sum Equals K**
- **Custom:** Design a simple version control system — given a sequence of commits, implement branch, merge, diff operations (data structure design heavy)
- **Custom:** Given a JIRA-like issue graph (blockers/blocked-by relationships), detect circular dependencies (cycle detection)

### System Design Questions
- Design JIRA — issue tracking, workflow states, sprint planning, search
- Design Confluence — collaborative document editing (operational transform or CRDT?)
- Design Bitbucket — repository hosting, PR workflow, CI pipeline triggers
- Design a real-time collaborative editing system (like Google Docs)
- Design a notification system for JIRA (issue assigned, mentioned, commented)
- Design a search system for JIRA issues — full-text search, filters, JQL
- Design an audit log system for compliance (who changed what, when)
- Design a plugin/extension system for JIRA marketplace
- Design Atlassian's permission and access control system (spaces, projects, roles)

### Java / Tech Stack Questions
- Atlassian uses Java heavily (JIRA/Confluence are Java) — expect deep Java questions
- Explain OSGi framework — how does JIRA's plugin system work at a high level?
- Explain Java's ServiceLoader mechanism — how is it related to plugins?
- How does Lucene work? What data structures does it use for inverted index?
- Explain CRDT (Conflict-free Replicated Data Types) — what problem do they solve?
- What is operational transformation? How does it enable concurrent document editing?
- How do you design a caching strategy for a heavily-read document system like Confluence?
- Explain immutable infrastructure — how does it relate to Atlassian's cloud migration?
- How do you handle schema migrations with zero downtime in a large PostgreSQL database?
- Atlassian values: Open company, no bullshit; Build with heart and balance; Don't #@!% the customer; Play, as a team; Be the change you seek — know these

### Behavioral Questions
- Atlassian has a very structured values-based behavioral round
- Tell me about a time you demonstrated "Open company, no bullshit" (radical transparency)
- Describe a time you had to balance technical quality with customer impact
- Tell me about a time you played as a team — how did you contribute to team success?
- Describe a time you were the change you wanted to see in your organization
- How do you approach code reviews? What do you look for?
- Tell me about a time you mentored someone — what was the outcome?

### Key Focus Areas
1. **Code quality and engineering craft** — Atlassian has a very high bar
2. **Java depth** — plugin systems, JVM internals, advanced patterns
3. **Collaborative systems** — CRDT, operational transform, real-time sync
4. **Values alignment** — behavioral round is genuinely evaluative, not a formality
5. **Graph algorithms in DSA** — JIRA's data model is a graph (issue dependencies, workflow)

### Tips for Atlassian
- Read Atlassian's engineering blog (atlassian.com/engineering) — they do ask about their own tech decisions
- The "design JIRA" question is almost guaranteed — have a solid design ready with search, workflow states, and permission model
- LC graph problems (cycle detection, topological sort) are very relevant — practice all of them
- Atlassian's values round is rigorous — map each value to a specific STAR story before the interview
- They care about code reviewability — in coding rounds, write clean, readable code with good variable names
- The OA includes a written system design component — practice writing design docs, not just verbal explanations

---

## 8. Groww

### Interview Process
- **Rounds:** 4–5 rounds
- **Round 1:** Online assessment — 2–3 DSA problems (Medium), 90 min
- **Round 2:** Technical Round 1 — DSA + Java concurrency (60 min)
- **Round 3:** Technical Round 2 — System Design (60 min)
- **Round 4:** Architecture / deep technical (60 min)
- **Round 5:** Culture/values fit with EM or Founder
- **Total duration:** 2–3 weeks
- **Format:** Virtual

### DSA Questions Asked (Specific)
- **LC 146 — LRU Cache** (with concurrent access — thread-safe implementation)
- **LC 295 — Find Median from Data Stream** (trading: find median price from tick stream)
- **LC 239 — Sliding Window Maximum** (stock price window)
- **LC 23 — Merge K Sorted Lists** (merge K sorted tick feeds)
- **LC 42 — Trapping Rain Water**
- **LC 84 — Largest Rectangle in Histogram**
- **LC 273 — Integer to English Words** (surprisingly common in fintech)
- **LC 460 — LFU Cache**
- **LC 315 — Count of Smaller Numbers After Self** (BIT/merge sort)
- **LC 218 — The Skyline Problem** (advanced)
- **Custom:** Design a thread-safe rate limiter — implement `tryAcquire(userId)` with 100 req/sec per user
- **Custom:** Given a real-time stream of stock trades (symbol, price, quantity, timestamp), compute VWAP for each symbol over the last 5 minutes (sliding window)
- **Custom:** Design an in-memory order book — match buy/sell orders by price-time priority

### System Design Questions
- Design Groww's Stock Trading System — order placement, matching, settlement
- Design a Real-time Portfolio Tracker — P&L calculation, live market data feed
- Design a Market Data Feed System — handling millions of tick updates per second
- Design a Mutual Fund Purchase System — NAV-based pricing, cut-off time, units allocation
- Design Groww's KYC/Onboarding System — document verification, SEBI compliance
- Design a Price Alert System for stocks
- Design a Transaction History and Tax Statement System (P&L, STCG, LTCG calculation)
- Design a Notification Service for trade execution confirmations

### Java / Tech Stack Questions
- Groww is Go + Java — they may ask about both
- How do you implement a thread-safe singleton? Double-checked locking + volatile
- Explain `java.util.concurrent` — `Semaphore`, `CountDownLatch`, `CyclicBarrier`, `Phaser` — when to use each
- What is a `BlockingQueue`? How does `ArrayBlockingQueue` differ from `LinkedBlockingQueue`?
- Implement producer-consumer using `BlockingQueue`
- Explain `AtomicLong` vs `LongAdder` — which is better under high contention and why?
- How does Go's goroutine scheduler work? How does it differ from Java threads?
- What is Go's channel? How does it compare to Java's `BlockingQueue`?
- Explain the happens-before guarantee in Java — give a concrete example
- How does optimistic locking with `@Version` work in JPA/Hibernate?
- How do you prevent overselling in a stock trading system? (inventory locking strategies)
- What is market impact and how do you design an order book to minimize latency?

### Behavioral Questions
- Describe a time you worked on a system where data correctness was non-negotiable
- Tell me about a time you had to make a system reliable under high concurrency
- How do you approach a situation where a production bug is causing financial losses?
- Describe your understanding of how trading systems differ from regular CRUD applications
- Tell me about a time you had to make a complex trade-off between performance and correctness

### Key Focus Areas
1. **Concurrency and thread safety** — trading systems are inherently concurrent; this is tested heavily
2. **Financial data correctness** — no approximations; exact calculations required
3. **Real-time data processing** — streams, windowing, aggregations
4. **Low-latency design** — trading systems have microsecond-level latency requirements
5. **Go knowledge** — Groww uses Go for critical paths; basic knowledge is a plus

### Tips for Groww
- Thread-safe data structures and concurrent implementations will be tested in coding rounds — practice coding `ConcurrentHashMap`, `LRU Cache with locks`, rate limiter
- The order book design problem is nearly guaranteed in system design — understand price-time priority matching
- Groww asks about Go even for Java roles sometimes — read Go's goroutine model basics
- Financial precision matters in discussions — mention `BigDecimal` over `double` for currency
- In behavioral rounds, they want ownership examples from fintech-adjacent domains — map your GSTN financial work carefully
- "Founder mode" culture: expect to be asked about startup pace and ambiguity tolerance

---

## 9. Walmart Global Tech India

### Interview Process
- **Rounds:** 5–6 rounds (one of the longer processes)
- **Round 1:** Online assessment — 2–3 DSA problems + technical MCQs, 90 min
- **Round 2:** Technical Round 1 — DSA (60 min)
- **Round 3:** Technical Round 2 — System Design (60 min)
- **Round 4:** Technical Round 3 — Architecture + past project deep dive
- **Round 5:** Hiring Manager — behavioral
- **Round 6:** Senior/Principal Engineer bar raiser (for SDE-2+)
- **Total duration:** 3–5 weeks
- **Format:** Virtual; some offices have in-person option

### DSA Questions Asked (Specific)
- **LC 1 — Two Sum**
- **LC 15 — 3Sum**
- **LC 56 — Merge Intervals**
- **LC 146 — LRU Cache**
- **LC 200 — Number of Islands**
- **LC 207 — Course Schedule**
- **LC 253 — Meeting Rooms II**
- **LC 347 — Top K Frequent Elements**
- **LC 621 — Task Scheduler**
- **LC 322 — Coin Change**
- **LC 416 — Partition Equal Subset Sum**
- **LC 739 — Daily Temperatures**
- **LC 84 — Largest Rectangle in Histogram**
- **LC 23 — Merge K Sorted Lists**
- **Custom:** Design a grocery inventory system — given product SKUs, locations, and quantities, implement `findNearestAvailableStore(productId, userLocation)` (graph + inventory)
- **Custom:** Black Friday simulation — given a product with limited stock and concurrent purchase requests, design a lock-free or minimal-lock algorithm for inventory decrement

### System Design Questions
- Design Walmart's Product Catalog System — 500M+ SKUs, attribute management, search
- Design Walmart.com's Search and Filtering System — full text, faceted search, personalization
- Design an Inventory Management System — multi-warehouse, real-time stock, replenishment
- Design a Flash Sale System — overselling prevention at Walmart scale (Black Friday)
- Design a Shopping Cart and Checkout System
- Design Walmart's Supply Chain Tracking — from supplier to warehouse to store to customer
- Design a Price Optimization Engine — dynamic pricing, competitor price tracking
- Design a Loyalty Points System (Walmart+)
- Design a Distributed Job Scheduler for batch processing (price updates, inventory sync)

### Java / Tech Stack Questions
- Walmart is heavily Java on the backend — expect deep Java questions
- Explain the difference between `ArrayList` and `LinkedList` — time complexity for each operation
- How does `PriorityQueue` work internally? What data structure does it use?
- Explain Java Streams — `map`, `filter`, `reduce`, `flatMap` with time complexity
- What is the Executor framework? How do you configure a `ThreadPoolExecutor`?
- Explain CompletableFuture pipeline — `.thenApply()` vs `.thenCompose()` difference
- How does Spring's transaction management work with JPA?
- Explain database sharding — how do you choose a shard key for a product catalog?
- What is consistent hashing? How does it help in distributed caching?
- How does Elasticsearch work? What is an inverted index?
- Explain Kafka partitioning — how do you ensure a product's events go to the same partition?
- What is a bloom filter? When would you use it in an e-commerce context?

### Behavioral Questions
- Walmart uses a structured behavioral interview with their own values (respect for the individual, service to customers, striving for excellence, acting with integrity)
- Tell me about a time you went above and beyond for an internal or external customer
- Describe a situation where you improved a process or system significantly
- Tell me about a time you had to work across multiple teams to deliver something
- How do you handle situations where business priorities conflict with technical quality?
- Tell me about your biggest failure and what you learned from it

### Key Focus Areas
1. **E-commerce and retail domain** — inventory, catalog, pricing, supply chain
2. **Scale** — Walmart operates at massive scale; every design must address this
3. **Java fundamentals** — they test comprehensively, not just surface level
4. **Big data concepts** — Hadoop, Spark, batch processing are relevant
5. **Distributed systems** — partitioning, consistent hashing, distributed transactions

### Tips for Walmart Global Tech
- Walmart has multiple product areas (Sam's Club, Flipkart, PhonePe in India too) — research which team you're interviewing for
- The bar raiser round at Walmart is very senior — prepare for architecture-level questions beyond your current level
- Black Friday scenario (flash sale, inventory locking) comes up very frequently — have a concrete design
- Consistent hashing is almost always discussed in system design — be able to explain it from scratch with examples
- The MCQ section in OA covers Java, SQL, basic algorithms — brush up on all three
- Walmart values customer-centric stories in behavioral — connect your GSTN work to "serving taxpayers" angle

---

## 10. Slice

### Interview Process
- **Rounds:** 3–4 rounds (leaner process than larger companies)
- **Round 1:** Online assessment or phone screen — 1–2 DSA problems, 60 min
- **Round 2:** Technical Round — DSA + Java + system design (combined, 60–75 min)
- **Round 3:** System Design deep dive (60 min)
- **Round 4:** Culture / founder round (for senior roles)
- **Total duration:** 2–3 weeks
- **Format:** Virtual

### DSA Questions Asked (Specific)
- **LC 1 — Two Sum** (warm-up)
- **LC 146 — LRU Cache**
- **LC 3 — Longest Substring Without Repeating Characters**
- **LC 56 — Merge Intervals**
- **LC 141 — Linked List Cycle**
- **LC 206 — Reverse Linked List**
- **LC 21 — Merge Two Sorted Lists**
- **LC 347 — Top K Frequent Elements**
- **LC 215 — Kth Largest Element**
- **LC 128 — Longest Consecutive Sequence**
- **LC 238 — Product of Array Except Self**
- **Custom:** Given a list of credit transactions (userId, amount, type: debit/credit, timestamp), compute the running balance and detect when it goes below zero (array/stream processing)
- **Custom:** Design a sliding window rate limiter for credit card transactions — `isAllowed(cardId, timestamp)` method

### System Design Questions
- Design Slice's Credit Card System — card issuance, transaction authorization, billing cycle
- Design a Buy Now Pay Later (BNPL) system — eligibility, disbursement, EMI schedule, collection
- Design a Credit Limit Management System — utilization tracking, dynamic limit adjustment
- Design a Transaction Dispute Resolution System
- Design a Collections and Repayment Reminder System
- Design a Fraud Detection System for credit card transactions
- Design a Merchant Payment Acceptance System for Slice card

### Java / Tech Stack Questions
- Slice is a smaller team — expect more practical, real-world questions than theoretical
- How do you implement idempotency for payment APIs?
- What is optimistic locking? How would you use it to prevent double-spending?
- Explain `@Transactional` — what happens when an exception is thrown inside?
- How do you design a financial audit trail — what fields are needed?
- Explain eventual consistency with an example from payments
- How does Redis `INCR` provide atomicity? How would you use it for rate limiting?
- What is a saga pattern? How would you implement it for a loan disbursement flow?
- How do you handle time zones in a financial application?
- What is the outbox pattern? How does it solve the dual-write problem?

### Behavioral Questions
- Slice is a startup — they value speed, ownership, and ambiguity tolerance
- Tell me about a time you had to make a fast decision with incomplete information
- Describe how you've handled working on a product with rapidly changing requirements
- Tell me about the biggest end-to-end ownership you've had on a feature or system
- How do you balance moving fast and maintaining code quality?

### Key Focus Areas
1. **Credit and lending domain** — BNPL, EMI, credit scoring, collections
2. **Payments correctness** — idempotency, double-spend prevention, audit trails
3. **Practical Java** — real-world problems, not just theory
4. **Startup mindset** — they want ownership, not just execution
5. **Financial regulations** — RBI guidelines for lending apps is a plus to know

### Tips for Slice
- Slice has a faster interview process than larger companies — process can complete in 2 weeks
- The DSA bar is Medium-level, not Hard — focus on getting correct solutions with clean code
- In system design, focus heavily on the lending/credit domain specifics — they will probe your domain knowledge
- BNPL system design is nearly certain to come up — study the flow: application → underwriting → disbursement → EMI schedule → collection → prepayment
- Prepare a concrete answer on how you'd handle a production issue where a user was charged twice
- Slice is growing fast — they value "move fast and maintain quality" more than "perfection before shipping"

---

## Cross-Company DSA Patterns Summary

These problems appeared across 3+ companies — solve these first:

| Problem | LC # | Frequency | Pattern |
|---|---|---|---|
| LRU Cache | 146 | 9/10 companies | HashMap + DLL |
| Merge Intervals | 56 | 7/10 | Sorting + greedy |
| Merge K Sorted Lists | 23 | 6/10 | Heap |
| Trapping Rain Water | 42 | 6/10 | Two pointer / stack |
| Number of Islands | 200 | 7/10 | BFS/DFS |
| Top K Frequent Elements | 347 | 6/10 | Heap / bucket sort |
| Task Scheduler | 621 | 4/10 | Greedy + heap |
| Find Median from Data Stream | 295 | 4/10 | Two heaps |
| Course Schedule | 207 | 5/10 | Topological sort |
| Sliding Window Maximum | 239 | 4/10 | Deque |

## Common System Design Themes

- **Idempotency in payments** — all fintech companies test this
- **Rate limiting** — appears in Razorpay, Groww, Slice designs
- **Notification systems** — appears in Meesho, MMT, Paytm, Groww
- **Fraud detection** — Razorpay, CRED, Paytm, Groww, Slice
- **Search systems** — Meesho, Walmart, MMT, Atlassian
- **Event-driven architecture with Kafka** — all companies in Phase 1

---

*Last updated: March 2026. Interview processes and question patterns change — verify recent experiences on Glassdoor/Blind before your interview.*
