# Deep Research: SDE-2/SDE-3 Interview Patterns, Company Hiring Trends, and Senior-Level Expectations
# India + Global Companies with India Offices | 2024–2026
# Research compiled from: LeetCode Discuss, Blind, Glassdoor, GeeksForGeeks, Engineering Blogs, Levels.fyi
# For: Jayanti Vishnoi | 5.5 YOE | GSTN | Java, Spring Boot, Kafka, Redis, Golang

---

## TABLE OF CONTENTS

1. [The 50+ Company Master List — Tier-by-Tier](#company-master-list)
2. [Company-by-Company Interview Deep Dive](#company-deep-dive)
3. [Industry Hiring Trends 2025–2026](#industry-trends)
4. [What Changed for 5+ YOE vs 3 YOE](#seniority-expectations)
5. [Java/Spring Boot/Kafka Pattern Frequency Map](#java-kafka-patterns)
6. [Common Failure Reasons by Tier](#failure-reasons)
7. [What "Senior" Means Company-by-Company](#senior-bar)
8. [New Topics Being Asked in 2025–2026](#new-topics)
9. [Specific Questions from LeetCode Discuss / Blind / Glassdoor](#specific-questions)
10. [Interview Format Reference Card](#format-card)

---

## 1. THE 50+ COMPANY MASTER LIST {#company-master-list}

### Tier Classification (Jayanti's context)

```
Tier S  — Dream + highest pay. 3–10% pass rate. Phase 2 peak.
Tier 1  — Strong product companies. 10–20% pass rate. Phase 2.
Tier 2  — Good product + fintech. 15–30% pass rate. Phase 1 end / Phase 2 start.
Tier 3  — Reachable. 25–45% pass rate. Phase 1 core targets.
Tier 4  — Quick wins. 40–60% pass rate. Apply early for interview reps.
```

---

### COMPLETE COMPANY TABLE

| # | Company | Tier | Role Level | Salary (Total Comp) | Location | Stack | DSA Bar | SD Bar | Java Depth |
|---|---------|------|-----------|---------------------|----------|-------|---------|--------|------------|
| 1 | Google India | S | L4/L5 | ₹55–120L | Bengaluru, Hyderabad | Go/Java/C++ | Hard | Massive scale | Medium |
| 2 | Meta India | S | E4/E5 | ₹50–110L | Hyderabad | Any | Hard | Product scale | Medium |
| 3 | Amazon India | S | SDE-2 | ₹45–90L | Bengaluru, Hyderabad, Chennai | Java/Kotlin | Medium-Hard | AWS scale | High |
| 4 | Microsoft India | S | SDE-2/3 | ₹40–80L | Hyderabad, Noida | Any | Medium | Azure-flavored | Medium |
| 5 | Goldman Sachs India | S | Associate/VP | ₹45–90L | Bengaluru, Hyderabad | Java | Medium | Financial systems | Deepest |
| 6 | Flipkart | 1 | SDE-2/3 | ₹38–70L | Bengaluru | Java/Kotlin | Medium-Hard | E-commerce scale | Deep |
| 7 | Uber India | 1 | SDE-2/3 | ₹40–75L | Bengaluru | Java/Go | Medium-Hard | Geo + maps | High |
| 8 | Atlassian India | 1 | SDE-2/3 | ₹38–70L | Bengaluru | Java/Go | Medium | SaaS collaboration | High |
| 9 | Zerodha | 1 | Backend SDE | ₹30–55L | Bengaluru | Go | Low formal | Trading systems | N/A (Go) |
| 10 | Morgan Stanley | 1 | Technology Analyst | ₹35–65L | Bengaluru, Mumbai | Java | Medium | Financial systems | Deep |
| 11 | JP Morgan Chase | 1 | SDE-2/3 | ₹32–60L | Bengaluru, Mumbai | Java | Medium | Finance + risk | Deep |
| 12 | Deutsche Bank | 1 | SDE-2/3 | ₹30–55L | Mumbai, Pune | Java | Medium | Trading + risk | Deep |
| 13 | BNY Mellon | 1 | SDE-2/3 | ₹28–50L | Pune | Java | Easy-Medium | Custody systems | Deep |
| 14 | Stripe India | 1 | SDE-2/3 | ₹45–80L | Bengaluru | Java/Go/Ruby | Medium-Hard | Payments infra | High |
| 15 | PhonePe | 1 | SDE-2/3 | ₹32–60L | Bengaluru | Java/Go | Medium | Payments scale | High |
| 16 | Razorpay | 2 | SDE-2/3 | ₹28–52L | Bengaluru | Java/Go | Medium | Payments gateway | High |
| 17 | Swiggy | 2 | SDE-2/3 | ₹30–55L | Bengaluru | Java/Go | Medium-Hard | Real-time logistics | High |
| 18 | Zomato | 2 | SDE-2/3 | ₹28–50L | Gurgaon | Java/Go | Medium | Real-time logistics | Medium |
| 19 | CRED | 2 | SDE-2/3 | ₹30–55L | Bengaluru | Java/Kotlin/Go | Medium | Fintech platform | High |
| 20 | Juspay | 2 | SDE-2/3 | ₹26–48L | Bengaluru | Java/Haskell | Medium | Payments routing | High |
| 21 | Meesho | 2 | SDE-2/3 | ₹26–48L | Bengaluru | Java | Medium | E-commerce | High |
| 22 | Groww | 2 | SDE-2/3 | ₹28–52L | Bengaluru | Java/Go | Medium | Fintech investing | High |
| 23 | Coinbase India | 2 | SDE-2/3 | ₹40–70L | Hyderabad | Go/Python | Medium-Hard | Crypto infra | Medium |
| 24 | Nutanix India | 2 | SDE-2/3 | ₹35–65L | Bengaluru, Pune | C++/Java/Go | Medium-Hard | Distributed infra | Medium |
| 25 | Salesforce India | 2 | SDE-2/3 | ₹35–65L | Bengaluru, Hyderabad | Java | Medium | SaaS platform | High |
| 26 | Oracle India | 2 | SDE-2/3 | ₹30–55L | Bengaluru, Hyderabad | Java | Medium | Database/cloud | High |
| 27 | Adobe India | 2 | SDE-2/3 | ₹35–62L | Noida, Bengaluru | Java/C++ | Medium | Cloud SaaS | High |
| 28 | Walmart Global Tech | 3 | SDE-2/3 | ₹25–45L | Bengaluru | Java | Medium | Retail scale | High |
| 29 | Paytm | 3 | SDE-2/3 | ₹22–42L | Noida | Java/Go | Medium | Payments | Medium |
| 30 | Slice (fintech) | 3 | SDE-2 | ₹22–40L | Bengaluru | Java | Medium | Credit card + UPI | Medium |
| 31 | Jupiter Money | 3 | SDE-2 | ₹22–40L | Bengaluru | Java/Go | Medium | Neobank | Medium |
| 32 | Fi Money | 3 | SDE-2 | ₹22–40L | Bengaluru | Java/Go | Medium | Neobank | Medium |
| 33 | Jar | 3 | SDE-2 | ₹20–36L | Bengaluru | Java | Easy-Medium | Savings micro | Medium |
| 34 | KreditBee | 3 | SDE-2 | ₹20–35L | Bengaluru | Java | Easy-Medium | Lending | Medium |
| 35 | Lendingkart | 3 | SDE-2 | ₹20–35L | Ahmedabad/Bengaluru | Java | Easy-Medium | Lending | Medium |
| 36 | MakeMyTrip | 3 | SDE-2/3 | ₹24–42L | Gurgaon | Java | Medium | Travel platform | Medium |
| 37 | OYO | 3 | SDE-2/3 | ₹22–38L | Gurgaon | Java | Medium | Hospitality | Medium |
| 38 | OLA | 3 | SDE-2/3 | ₹24–42L | Bengaluru | Java/Go | Medium | Mobility | Medium |
| 39 | Browserstack | 3 | SDE-2/3 | ₹26–46L | Mumbai | Java/Go | Medium | Testing SaaS | Medium |
| 40 | Freshworks | 3 | SDE-2/3 | ₹24–42L | Chennai, Bengaluru | Java/Ruby | Medium | CRM SaaS | Medium |
| 41 | Hasura | 3 | SDE-2/3 | ₹26–45L | Bengaluru | Go/Haskell | Medium | GraphQL infra | Low |
| 42 | Chargebee | 3 | SDE-2/3 | ₹24–42L | Chennai | Java | Medium | Subscription billing | Medium |
| 43 | Razorpay (Capital team) | 3 | SDE-2 | ₹25–45L | Bengaluru | Java | Medium | BNPL + credit | High |
| 44 | Urban Company | 3 | SDE-2 | ₹22–38L | Gurgaon | Java | Medium | Marketplace | Medium |
| 45 | Dunzo | 4 | SDE-2 | ₹18–32L | Bengaluru | Go/Java | Easy-Medium | Quick commerce | Medium |
| 46 | Nykaa | 4 | SDE-2 | ₹20–35L | Mumbai | Java | Easy-Medium | E-commerce | Medium |
| 47 | Navi Tech | 3 | SDE-2 | ₹22–40L | Bengaluru | Java | Medium | Lending/insurance | Medium |
| 48 | Perfios | 3 | SDE-2 | ₹22–38L | Bengaluru | Java | Medium | Fintech data | High |
| 49 | Setu (Pine Labs) | 3 | SDE-2 | ₹22–40L | Bengaluru | Go | Medium | BaaS/payments API | Medium |
| 50 | Zoho | 4 | SDE-2 | ₹18–30L | Chennai | Java | Easy-Medium | SaaS | Medium |
| 51 | InfraCloud | 4 | SDE-2 | ₹18–30L | Pune | Go/K8s | Medium | Platform/K8s | Low |
| 52 | ThoughtWorks | 4 | Consultant SDE | ₹18–32L | Multiple | Any | Easy-Medium | Any | Medium |
| 53 | Publicis Sapient | 4 | Senior Associate | ₹18–30L | Multiple | Java | Easy | Basic | Medium |
| 54 | Persistent Systems | 4 | Tech Lead | ₹18–28L | Pune | Java | Easy | Basic | Medium |

---

## 2. COMPANY-BY-COMPANY INTERVIEW DEEP DIVE {#company-deep-dive}

---

### AMAZON (SDE-2) — Most important for Phase 2

**Interview Process (2024–2025 reality):**

```
Stage 1: Online Assessment (HackerRank) — 2 coding problems (90 min)
         → LP (Work Styles) survey (15 min, personality only, no wrong answer)

Stage 2: Phone Screen — 1 coding + LP questions (45 min)
         → Bar: LeetCode Medium. Common topics: arrays, trees, sorting.

Stage 3: Onsite Loop (4–5 rounds, virtual or in person):
         Round 1: DSA (45 min) — 1-2 problems, Medium-Hard
         Round 2: DSA (45 min) — 1-2 problems, focus on graphs/trees
         Round 3: System Design (60 min) — scalability + Amazon services
         Round 4: Bar Raiser (60 min) — LP heavy, 1 coding problem
         Round 5 (if SDE-3 level): HM round — leadership, ownership
```

**What Changed in 2025:**
- Amazon now uses a "calibration matrix" — interviewers score you on 5 dimensions simultaneously: problem-solving, code quality, communication, LP signals, leadership potential.
- The Bar Raiser is from a different org — they ask harder LP questions and can veto. Focus on "Disagree and Commit" LP.
- SDE-2 is now closer to L5 in new levelling — Amazon deleveled many "SDE-3" hires to SDE-2 titles in India in 2024.
- AI-related system design questions started appearing in 2025: "Design Amazon's product recommendation pipeline."

**DSA Questions Seen (2024–2025):**
- LRU Cache implementation (asked in 30% of reported experiences)
- Find all permutations of a string (backtracking)
- Maximum sum path in binary tree
- Merge K sorted linked lists (Heap)
- Word ladder (BFS on graph)
- Median from data stream (two heaps)
- Coin change with minimum coins (DP)
- Trapping rain water (asked multiple times)
- Number of islands (DFS/BFS)
- Clone graph

**System Design Questions (SDE-2):**
- Design Amazon's package tracking system (event-driven, fanout to customers)
- Design a distributed notification system (push, email, SMS — your GSTN use case)
- Design Amazon's product catalog (search, listing, inventory sync)
- Design rate limiter at API gateway level
- Design a flash sale system (inventory decrement, concurrency, fairness)
- Design distributed ID generator (Snowflake — asked at 40% of reported SD rounds)

**Leadership Principles Deep Dive:**
```
LP                  | Most common question format
--------------------|-----------------------------------------------------
Customer Obsession  | "When did customer impact change your technical decision?"
Ownership           | "Tell me about a project you owned end-to-end with no manager."
Invent & Simplify   | "Describe the most innovative solution you built."
Dive Deep           | "What's the most complex technical thing you've debugged?"
Deliver Results     | "Tell me about a time you delivered under impossible deadline."
Disagree & Commit   | "Tell me about a time you strongly disagreed with your team."
Earn Trust          | "Tell me about a time you failed. What did you do?"
Bias for Action     | "Give an example of a risky decision you made quickly."
```

**GSTN Framing for Amazon:**
- Customer Obsession: "GSTN serves 14M taxpayers. Every feature I built had direct regulatory compliance impact."
- Dive Deep: "Debugged a Kafka consumer lag spike that was causing GST return submission failures at month-end — traced to off-heap memory leak in Kafka client with 50M messages/day throughput."
- Deliver Results: "Delivered the e-invoicing B2B integration under 90-day government mandate with zero extension."

---

### FLIPKART (SDE-2/SDE-3)

**Interview Process (2024–2025 reality):**

```
Stage 1: Recruiter screen (15 min)
Stage 2: Online Assessment — 2 coding problems (60–90 min)
Stage 3: Onsite Loop (4–5 rounds):
         Round 1: DSA — 2 problems (Medium-Hard, Java preferred)
         Round 2: LLD — Design one complete system with code (UML + code)
         Round 3: HLD — System design with scalability
         Round 4: Deep Dive — Past project walkthrough + Java internals
         Round 5: Hiring Manager — Behavioral + product sense
```

**Unique Flipkart Characteristics:**
- LLD round is brutal — you write actual code, not just design. Expect: "Now implement the Observer pattern for this in Java."
- They test Java concurrency hard: "Write a producer-consumer with BlockingQueue, now make it bounded."
- SDE-3 bar is very high. They ask about ownership of a full service.
- Strong preference for candidates who have worked on high-read systems (e-commerce = read-heavy).

**DSA Questions Seen (2024–2025):**
- Serialize/deserialize binary tree (extremely common — 50%+ reports)
- Top K frequent elements with time window (sliding window + heap)
- Design LRU Cache with code (also counts as LLD warm-up)
- Alien dictionary (topological sort) — asked for SDE-3 level
- Minimum window substring
- Jump game II
- Find if a string is a rotation of another
- Maximum product subarray
- Design a data structure: insert/delete/getRandom O(1)

**LLD Questions Seen:**
- Inventory management system with reservations and rollbacks
- Parking lot (classic but must code it fully in Java — strategy + factory)
- Library management system with concurrent access
- Movie ticket booking system (seats, reservations, expiry)
- Tic Tac Toe (extensible to N-player)
- Online food ordering system (restaurant, menu, order, delivery assignment)

**System Design Questions Seen:**
- Flash sale system (10K orders in 60 seconds — concurrency, oversell prevention)
- Product search with filters (Elasticsearch use, faceted search, ranking)
- Flipkart's order management system (state machine — ordered → confirmed → shipped → delivered)
- Real-time inventory tracking (millions of SKUs, concurrent updates)
- Notification system (order updates, promotions)

**Java Questions Seen:**
- How does ConcurrentHashMap work in Java 8+ (segment locking → bucket-level CAS)
- @Transactional internal mechanism + self-invocation problem
- How would you detect and fix a deadlock in production?
- Explain G1GC phases: young gen collection, concurrent marking, mixed collection
- ThreadLocal usage and memory leak risks

---

### GOLDMAN SACHS (SDE-2 / Associate)

**Interview Process (2024–2025 reality):**

```
Stage 1: HireVue video interview — 4–5 pre-recorded behavioral questions
         → Also includes: 1 coding problem timed

Stage 2: Technical Phone Screen (30–45 min) — Java + coding

Stage 3: Super Day (3–4 rounds same day):
         Round 1: Core Java/Concurrency (45 min) — deepest Java questions
         Round 2: Coding (45 min) — data structures, not algorithmic tricks
         Round 3: System Design / Architecture (45 min) — financial systems
         Round 4: Behavioral/HR (30 min) — fit + communication
```

**What's Different at GS:**
- They code-review live. Interviewer gives you code, asks "What's wrong with this?"
- Concurrency is non-negotiable. If you can't explain volatile + happens-before, you fail R1.
- Financial domain knowledge is a massive plus — they frame everything around trading/risk.
- No competitive programming. No DP tricks. Pure engineering and design.

**Java/Concurrency Questions Seen (GS 2024–2025):**
- Lock escalation: biased → thin → fat. Explain at JVM level with mark word.
- Volatile: What does it guarantee? What doesn't it guarantee? (Visibility but not atomicity)
- Implement thread-safe singleton: 3 ways (synchronized, DCL with volatile, enum)
- What is false sharing? How do you prevent it? (Cache line padding, @Contended)
- Implement a blocking queue using wait/notifyAll from scratch
- CompletableFuture: What happens if you chain 10 thenApply calls? Thread model?
- What is a memory fence? When does JVM insert one?
- ForkJoinPool work stealing — explain the algorithm
- Difference between ExecutorService submit() and execute() — Future vs void
- ThreadLocal vs InheritableThreadLocal — when does InheritableThreadLocal cause memory leaks?
- Explain happens-before relationships in Java Memory Model (JMM)
- StampedLock vs ReentrantReadWriteLock — when to prefer each?

**System Design Questions (GS 2024–2025):**
- Design a distributed rate limiter for trading APIs (leaky bucket + Redis + Lua script)
- Design an order matching engine (limit order book, price-time priority)
- Design a real-time risk calculation system (position aggregation, VaR, live P&L)
- Design a ledger system with immutable audit trail
- Design a circuit breaker for external API calls

**GSTN Advantage at GS:**
Your XA transactions (Atomikos) are directly analogous to GS's distributed ledger requirements. Frame it as: "I implemented distributed ACID transactions across 4 microservices for tax credit ledger — conceptually identical to financial settlement."

---

### MORGAN STANLEY

**Interview Process:**

```
Stage 1: Online Assessment — Data structures + Java MCQ (90 min)
Stage 2: Technical rounds (2–3):
         Round 1: Java fundamentals + data structures
         Round 2: System design OR advanced concurrency
         Round 3: Behavioral + HR
```

**Questions Seen (2024–2025):**
- Core Java: Immutable class design. What makes String immutable?
- Implement Comparable vs Comparator — when to use which?
- Design a concurrent cache with read-write lock
- Find cycles in a directed graph (DFS + coloring)
- Reverse a linked list in groups of K
- System design: Design a risk calculation pipeline for 10K instruments updated every second
- System design: Design a real-time market data feed distributor

---

### JP MORGAN CHASE

**Interview Process:**

```
Stage 1: Coding assessment (HackerRank — 3 problems, 90 min)
Stage 2: Technical rounds (2–3):
         Round 1: Java + data structures
         Round 2: System design
         Round 3: Behavioral
```

**Questions Seen (2024–2025):**
- Implement a thread-safe LRU cache
- Design a payment clearing system with rollback
- Graph: Shortest path with K stops (BFS + Dijkstra hybrid)
- Spring Boot: How do you handle circular dependencies?
- Microservices: How do you implement distributed tracing? (Sleuth, Zipkin)
- Design a fraud detection system (rule engine + ML scoring + blocking)

---

### DEUTSCHE BANK

**Interview Process:**

```
Stage 1: Code assessment (Codility) — 2–3 problems
Stage 2: Technical interviews (2–3 rounds):
         Round 1: Java deep + concurrency
         Round 2: System design + database design
         Round 3: Behavioral
```

**Specific Focus:**
- DB tests database design heavily — normalization, indexing, query optimization.
- They ask about messaging systems (MQ/Kafka) for trade event streaming.
- Questions on high availability patterns (failover, consensus).

**Questions Seen (2024–2025):**
- Write a SQL query: Find accounts with more than 3 transactions in the last 24h
- Design a trade lifecycle management system
- How do you prevent duplicate payments in a distributed system?
- Explain 2PC vs Saga pattern — when is 2PC acceptable?
- What is event sourcing? How would you implement it in Java?

---

### BNY MELLON

**Interview Process:**

```
Stage 1: HR screen
Stage 2: 2–3 technical rounds (gentler than front-line investment banks)
         Round 1: Java + Spring Boot fundamentals
         Round 2: System design (moderate depth)
         Round 3: Behavioral
```

**Questions Seen:**
- Spring Boot: Explain bean scopes (singleton, prototype, request, session)
- How does Spring Security work? OAuth2 flow?
- Design a fund accounting reconciliation system
- SQL: Window functions — RANK(), LEAD(), LAG() — write examples
- REST API design: What HTTP status codes for various error conditions?

**GSTN Advantage:** BNY is comfortable with government-adjacent financial systems. Frame GSTN as "large-scale fund reconciliation across 14M entities."

---

### PHONEPE (SDE-2)

**Interview Process (2024–2025 reality):**

```
Stage 1: Recruiter screen (15 min)
Stage 2: Online Assessment — 2 coding problems (60 min)
Stage 3: Technical rounds (3):
         Round 1: DSA + Core Java (60 min)
         Round 2: System Design focused on payments (60 min)
         Round 3: Managerial/Behavioral (45 min)
```

**PhonePe-Specific Focus:**
- Idempotency is asked in EVERY reported system design round. They care deeply about it.
- Kafka consumer reliability is a known favourite topic — consumer groups, offset management, at-least-once vs exactly-once.
- They test UPI protocol knowledge if you mention payments background.
- Distributed transaction patterns: Saga choreography vs orchestration.

**Questions Seen (2024–2025):**
- Design a UPI payment system end-to-end (payer, PSP, NPCI, payee bank)
- How do you ensure exactly-once processing in a payment Kafka consumer?
- Design a wallet system with distributed concurrency (optimistic vs pessimistic locking)
- What is the two-generals problem? How does it apply to payment confirmation?
- Design a transaction reconciliation system (mismatches, timeouts, settlement)
- How would you implement a distributed lock for payment processing?
- Design PhonePe's notification system for payment alerts
- What is the difference between strong consistency and eventual consistency? Give a real-world tradeoff.

**DSA Questions (2024–2025):**
- Top K frequent elements
- LRU Cache implementation
- Merge intervals
- Find the maximum sum subarray (Kadane's algorithm)
- Graph: Detect cycle in undirected graph

---

### RAZORPAY (SDE-2)

**Interview Process:**

```
Stage 1: Take-home coding assignment (3–5 days) OR OA
         → Assignment: "Build a simplified payment gateway" or
           "Build a webhook delivery system with retry"
Stage 2: Technical rounds (3):
         Round 1: Code walkthrough of take-home + extensions
         Round 2: System Design
         Round 3: Behavioral + culture fit
```

**Razorpay-Specific Focus:**
- Take-home is treated as production code. They check error handling, tests, clean code.
- Webhook delivery is a strong favourite topic: reliability, ordering, retry, idempotency key.
- API design is tested — "Design a Razorpay-like payment API."

**Questions Seen (2024–2025):**
- Design a webhook delivery system with at-least-once guarantees
- Design a payout system (bulk disbursal to N merchants)
- How does Razorpay handle payment link expiry and concurrency?
- Implement a circuit breaker pattern (state machine: closed → open → half-open)
- Design an API rate limiter per customer (sliding window log vs token bucket)
- How do you handle partial failures in a distributed payment transaction?
- Design a reconciliation system between Razorpay and banks

---

### SWIGGY (SDE-2/SDE-3)

**Interview Process:**

```
Stage 1: OA (2 coding problems, 90 min)
Stage 2: Technical rounds (3–4):
         Round 1: DSA — graphs emphasized
         Round 2: System Design — logistics/real-time
         Round 3: Java/backend deep dive
         Round 4: Culture/product fit
```

**Swiggy-Specific Focus:**
- Graph problems are disproportionately common (delivery routing, restaurant graph, time-distance)
- Real-time system design is expected — they care about WebSocket, SSE, Kafka for live tracking
- They have a "product round" — "How would you redesign X feature in Swiggy?"

**Questions Seen (2024–2025):**
- DSA: Minimum cost to visit all restaurants given travel times (TSP approximation)
- DSA: Find shortest delivery route given traffic constraints (Dijkstra/A*)
- DSA: Design RandomizedSet — insert/delete/getRandom all O(1)
- System Design: Real-time order tracking with live ETA updates
- System Design: Delivery partner assignment algorithm (Hungarian algorithm concept)
- System Design: Surge pricing engine (demand/supply ratio, geohash grid)
- System Design: Swiggy Instamart dark store inventory management
- Java: How does Spring WebFlux differ from traditional Spring MVC? (event loop vs thread-per-request)
- Java: Explain backpressure in reactive programming

---

### ZOMATO (SDE-2)

**Interview Process:**

```
Similar to Swiggy but slightly lighter DSA bar.
Rounds: OA → 3 technical rounds → HR
Strong emphasis on product thinking in all rounds.
```

**Questions Seen (2024–2025):**
- Design Zomato's restaurant discovery and ranking system
- Design a real-time food delivery tracking system
- Design Zomato's review and rating system (anti-gaming, spam filtering)
- DSA: Find all restaurants within radius R of user location (geospatial query)
- DSA: Given restaurant order history, suggest top N dishes (recommendation)
- Product: "Zomato Gold is losing subscribers — what would you do?"

---

### CRED (SDE-2)

**Interview Process:**

```
Stage 1: Recruiter screen
Stage 2: Coding assessment (take-home or OA)
Stage 3: Technical rounds (3–4):
         Round 1: DSA + clean code
         Round 2: LLD — design quality obsessed
         Round 3: System Design
         Round 4: Culture/Values fit (very important at CRED)
```

**CRED-Specific Focus:**
- Code quality matters more here than anywhere else — they care about readability, naming, abstraction.
- LLD is design-quality focused: "Is your code extensible? Is the interface clean?"
- They test credit/rewards domain knowledge if you have fintech background.

**Questions Seen (2024–2025):**
- LLD: Design a rewards/cashback engine (rules, categories, caps)
- LLD: Design a credit card statement generation system
- System Design: Design CRED's bill payment flow
- System Design: Design a fraud detection system for bill payments
- DSA: Implement a system to find all pairs with a target sum (multiple approaches expected)
- Java: Explain Optional in Java 8 — why was it introduced? When to NOT use it?
- Java: Stream API internals — lazy evaluation, short-circuit, terminal vs intermediate

---

### JUSPAY (SDE-2)

**Interview Process:**

```
Rounds: 3 rounds (DSA → System Design → Behavioral)
Note: Juspay is known for functional programming (Haskell backend) but Java roles exist.
For Java SDE-2: standard Java + payments focus.
```

**Questions Seen:**
- Design a payment router (rule-based routing across multiple payment gateways)
- Implement retry with exponential backoff + jitter (write the code)
- Design idempotency key handling for payment APIs
- DSA: Implement a trie for payment method autocomplete
- How would you implement saga pattern for a failed payment rollback?

---

### MEESHO (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds
OA + 2–3 technical rounds + HR
Standard format. Less brutal than Flipkart.
```

**Questions Seen (2024–2025):**
- Design seller catalog management system (bulk upload, async processing)
- Design Meesho's order routing and fulfillment system for Tier 2/3 India
- How do you handle slow consumers in Kafka? (backpressure, batch size, consumer lag)
- Design a returns and refund management system
- DSA: Given a list of seller orders, find the day with maximum deliveries (sliding window)
- Java: Explain the difference between @RestController and @Controller + @ResponseBody

---

### GROWW (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds (OA → 2 tech → 1 behavioral)
Strong fintech + trading focus.
```

**Questions Seen (2024–2025):**
- Design Groww's order management system for mutual fund transactions
- Design a portfolio valuation engine (live NAV updates for 10M users)
- System Design: Groww's payment collection and settlement flow
- DSA: Find K closest stocks to a target price (heap)
- Java: How does Spring @Async work? What thread pool does it use?
- Java: What is the difference between transient and volatile?

---

### COINBASE INDIA (SDE-2)

**Interview Process:**

```
Rounds: 4–5 rounds (similar to FAANG rigor)
Location: Hyderabad (small but growing team)
Stack: Go primary, some Python/Java
```

**Questions Seen:**
- Design a cryptocurrency exchange order book (limit orders, market orders, matching)
- Design a blockchain transaction verification pipeline
- DSA: Find maximum profit from stock trades with K transactions (DP — Hard)
- Distributed systems: Explain CAP theorem with a real crypto example
- Go: Goroutines vs OS threads. Explain Go scheduler (GPM model).
- Design Coinbase's wallet custody system

---

### ATLASSIAN (SDE-2/SDE-3)

**Interview Process:**

```
Stage 1: Online Assessment (2 coding problems)
Stage 2: Technical interviews (3–4):
         Round 1: Coding (DSA)
         Round 2: System Design
         Round 3: Values interview (NOT behavioral — literally tested against Atlassian values)
         Round 4: Hiring Manager
```

**Atlassian Values Interview (IMPORTANT):**
```
The 5 Atlassian Values — you WILL be asked one question per value:
1. Open company, no bullshit
2. Build with heart and balance
3. Don't #@!% the customer
4. Play, as a team
5. Be the change you seek

Map your GSTN STAR stories to these values BEFORE the interview.
"Open company" = transparency in a project. "Build with heart" = quality under pressure.
```

**Questions Seen (2024–2025):**
- System Design: Design Jira's issue tracking system (state machine, comments, attachments)
- System Design: Design Confluence's real-time collaborative editing (operational transforms or CRDTs)
- System Design: Design a feature flag system (LaunchDarkly-style)
- DSA: String: Given Jira ticket format, parse and validate it (parsing + regex)
- DSA: Find the most frequently assigned team member (frequency map + heap)
- Java: How does Atlassian use feature flags for gradual rollouts?

---

### UBER INDIA (SDE-2)

**Interview Process:**

```
Rounds: 4–5 rounds
Very similar to Google in rigor. DSA is harder than fintech companies.
```

**Questions Seen (2024–2025):**
- System Design: Design Uber's trip matching system (geospatial, driver-rider assignment)
- System Design: Design surge pricing engine
- System Design: Design Uber Eats' restaurant onboarding and catalog
- DSA: Given N pickup and dropoff points, schedule driver optimally (TSP variant)
- DSA: LRU Cache (must code it perfectly)
- Go: Explain context.WithCancel and context.WithTimeout. Goroutine leak scenarios.
- Distributed Systems: How does Uber handle network partitions in payment processing?

---

### NUTANIX (SDE-2/SDE-3)

**Interview Process:**

```
Rounds: 4–5 rounds
Strong distributed systems + storage focus.
Stack: C++/Go/Java — varies by team.
```

**Questions Seen (2024–2025):**
- Design a distributed key-value store (similar to DynamoDB)
- Explain Raft consensus algorithm — what happens during leader election?
- Design a distributed file system (chunk management, replication, metadata server)
- How does consistent hashing work? What are virtual nodes?
- Implement a distributed counter with eventual consistency
- How do you handle split-brain scenarios in a distributed cluster?

**GSTN Advantage:** Your distributed caching knowledge (JBoss DataGrid, EhCache) is directly relevant. Nutanix expects candidates to understand cache coherence and replication.

---

### SALESFORCE INDIA (SDE-2)

**Interview Process:**

```
Rounds: 4 rounds
More structured than startups. Strong behavioral component.
Stack: Java heavy.
```

**Questions Seen (2024–2025):**
- System Design: Design Salesforce's multi-tenant data architecture
- System Design: Design a bulk data export system (CSV/Excel for 10M rows)
- Java: How does JPA handle lazy loading in a closed EntityManager context?
- Java: Explain N+1 query problem and how to solve it
- DSA: Merge K sorted lists
- Behavioral: "Tell me about a time you dealt with a difficult customer request that contradicted technical best practices."

---

### ADOBE INDIA (SDE-2)

**Interview Process:**

```
Rounds: 4–5 rounds
Noida office: Document Cloud (PDF, Acrobat). Bengaluru: Experience Cloud.
Strong Java + distributed systems focus.
```

**Questions Seen (2024–2025):**
- System Design: Design Adobe Sign (e-signature workflow, legal audit trail, concurrent signing)
- System Design: Design a content delivery network for PDFs at scale
- System Design: Design Adobe Analytics' event ingestion pipeline (high write throughput)
- Java: How does Spring Cloud handle service discovery (Eureka)?
- Java: What is the difference between CopyOnWriteArrayList and synchronizedList?
- DSA: Serialize and deserialize N-ary tree

---

### STRIPE INDIA (SDE-2/SDE-3) — Bengaluru, growing fast

**Interview Process:**

```
Rounds: 4–5 rounds (closest to FAANG rigor among fintechs)
Stage 1: Recruiter + technical screen
Stage 2: Coding round (2 problems)
Stage 3: System design round (60 min)
Stage 4: Technical depth round (your domain expertise)
Stage 5: Behavioral / values
```

**Stripe-Specific Focus:**
- Stripe is obsessed with API design quality. "Design the payment API for Stripe" is literally a round.
- They probe deeply on distributed systems correctness — "What happens when this step fails?"
- Strong culture of "developer experience" — APIs must be intuitive.

**Questions Seen (2024–2025):**
- Design Stripe's payment API (idempotency keys, retry semantics, webhook delivery)
- Design a real-time fraud detection system at payment capture
- Design Stripe's revenue recognition system (GAAP compliance, time-based)
- DSA: Given transaction logs, find all duplicate charges (grouping + custom hashing)
- How do you handle partial payment authorization in a distributed system?
- What is two-phase commit? When is it acceptable? When is Saga better?

---

### ORACLE INDIA (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds
Oracle Cloud Infrastructure (OCI) team is the best team to target.
Stack: Java (OCI) or C (Database) — specify during application.
```

**Questions Seen (2024–2025):**
- Design a multi-region database with cross-region consistency
- SQL: Given a complex schema, write a query to find customers who bought in all categories
- Java: How does Oracle JVM (HotSpot) perform JIT compilation? Explain C1 vs C2 compiler.
- Java: Explain G1GC vs ZGC vs Shenandoah — when to use each?
- System Design: Design OCI Object Storage (S3 equivalent)

---

### WALMART GLOBAL TECH (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds
Standard product company format.
Stack: Java / Spring Boot / Kafka (very close to GSTN stack).
```

**Questions Seen (2024–2025):**
- System Design: Design Walmart's inventory management system
- System Design: Design a recommendation engine for grocery products
- Java: How does Spring Boot auto-configuration work? What is @ConditionalOnClass?
- DSA: Given orders, find the maximum number of orders that can be fulfilled with limited inventory
- DSA: Merge intervals (order scheduling)
- Behavioral: "Tell me about a time you improved system reliability."

**GSTN Advantage:** Your government-scale e-procurement experience is directly relatable to Walmart's retail scale. Frame your work as "managing supply chain data for India's largest taxpayer base."

---

### PAYTM (SDE-2)

**Interview Process:**

```
Rounds: 3 rounds
Lighter bar than PhonePe/Razorpay. Good Phase 1 target.
Stack: Java + Golang.
```

**Questions Seen (2024–2025):**
- Design Paytm's UPI payment flow (simplified)
- Design wallet transaction system with concurrent balance updates
- DSA: Find duplicate transactions in a stream (hashing + sliding window)
- Java: How does Spring @Cacheable work? What caching abstraction does it use?
- Java: What is the difference between @Transactional(readOnly=true) and default?

---

### SLICE / JUPITER / FI MONEY / JAR — Neobank cluster

**Common Interview Pattern:**

```
All 4 follow similar format: 3 rounds (OA → 2 tech → HR)
Lighter than PhonePe/Razorpay. Good Phase 1 targets.
Focus: Payments, credit, UPI, account aggregation.
Stack: Java + Golang (varies by company).
```

**Common Questions Seen (2024–2025):**
- Design a credit card transaction authorization system
- How do you implement optimistic locking for concurrent balance deductions?
- Design a KYC verification workflow (state machine, document upload, async verification)
- How does UPI autopay (mandate) work technically?
- Design a transaction limit enforcement system (daily, monthly caps)
- DSA: Given credit transactions, calculate outstanding balance over time (prefix sum variant)

---

### ZERODHA (Backend Engineer)

**Interview Process:**

```
Stage 1: Application review (they get 1000s of apps, very selective screen)
Stage 2: Technical assessment — real-world problem (not LeetCode)
         Example: "Here's a CSV of 1M trades. Write a Go program to calculate
         P&L for each user. Optimize for memory."
Stage 3: Deep technical conversation (2 rounds) — no formal interview structure
Stage 4: Culture fit conversation with founders/senior engineers
```

**Zerodha-Specific Approach:**
- No LeetCode. They hate competitive programming for its own sake.
- They want: Go proficiency, Unix/Linux fluency, strong data engineering skills.
- Blog reading matters: "Have you read our Rainmatter tech blog? What did you think of the article on [X]?"
- They explicitly look for people who have built systems they were intellectually curious about.

**Topics Tested:**
- Go concurrency: goroutines, channels, select, mutex, WaitGroup, context
- Database performance: EXPLAIN ANALYZE, index design, query optimization
- Systems programming: file I/O, memory mapping, CSV parsing at scale
- Financial domain: order book mechanics, tick data storage, portfolio accounting

---

### BROWSERSTACK (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds
Strong SaaS product company. Good work quality.
Stack: Java + Ruby + Go.
```

**Questions Seen:**
- System Design: Design Browserstack's real device cloud (device pool management, session allocation)
- System Design: Design a screenshot testing pipeline (parallel execution, diff detection)
- Java: How does Spring Boot's embedded Tomcat work?
- DSA: Given N test sessions, schedule them on M devices (interval scheduling)

---

### FRESHWORKS (SDE-2)

**Interview Process:**

```
Rounds: 3–4 rounds
CRM/SaaS focus. Structured interviews.
Stack: Java + Ruby on Rails (Java for backend platform).
```

**Questions Seen:**
- System Design: Design Freshdesk's ticket routing engine (rule-based + ML scoring)
- Design a multi-tenant SaaS system with data isolation
- DSA: Given support tickets with priority, schedule agents (priority queue + round robin)
- Java: How does Hibernate second-level cache work? What invalidation strategies exist?

---

## 3. INDUSTRY HIRING TRENDS 2025–2026 {#industry-trends}

### Trend 1: AI/ML Infrastructure Questions Now Appear at SDE-2 Level

**What's being asked in 2025:**
- "You're building a recommendation engine backend — how do you serve ML model predictions at low latency?"
- "Design a feature store for real-time ML inference" (Uber Michelangelo style)
- "How would you build an A/B testing framework to experiment with ML models?"
- "Design a data pipeline for training data collection and labeling"

**Companies asking this:** Amazon (Ads/Search teams), Flipkart (Search), Swiggy (recommendations), PhonePe (fraud/risk).

**What you need to know:**
- Model serving patterns: online vs batch inference
- Feature stores (Feast, Tecton concepts)
- Shadow mode testing / canary for ML models
- Embedding storage and vector similarity search (FAISS, Pinecone)
- You DON'T need to train ML models — just the infra around it

---

### Trend 2: Platform Engineering / Developer Tooling Questions

**What's being asked in 2025:**
- "How would you build an internal developer platform for your 200-engineer org?"
- "Design a deployment pipeline that enables feature flagging across 50 microservices"
- "How do you implement observability (logs + metrics + traces) as a shared platform?"
- "Design a secrets management system"

**Companies asking this:** Flipkart (internal tools), Amazon (Builder Tools teams), Atlassian, Uber.

**What you need to know:**
- Internal developer portals (Backstage by Spotify)
- Golden paths and paved roads concept
- Centralized observability: OpenTelemetry, Prometheus, Grafana, Jaeger
- Feature flagging systems (LaunchDarkly, Unleash)

**GSTN Advantage:** You built 32 shared frameworks for 45 microservices. That IS a platform engineering story. Frame it as: "I built an internal platform layer that standardized authentication, caching, audit logging, and Kafka consumption across 45 services — similar to what large tech orgs call an 'internal developer platform'."

---

### Trend 3: Event-Driven Architecture Depth Increasing

**What's being asked in 2025:**
- "What's the difference between event-driven and message-driven architectures?"
- "How do you implement event sourcing with Kafka?"
- "Design an outbox pattern implementation — walk me through the code"
- "How do you handle schema evolution in Kafka topics? (Avro + Schema Registry)"
- "Exactly-once semantics in Kafka — is it truly exactly-once? Caveats?"

**Companies asking this:** PhonePe, Razorpay, Goldman, Swiggy, Flipkart (ALL companies with Kafka).

**What you need to know:**
- Kafka Schema Registry + Avro schema evolution (backward, forward, full compatibility)
- Transactional outbox pattern (write DB + Kafka atomically without 2PC)
- Event sourcing vs CQRS — combined vs separate
- Idempotency keys as first-class citizens in event-driven design
- Kafka Streams vs Flink for stateful processing

---

### Trend 4: Distributed Systems Correctness Over Scalability

**Shift in 2024–2025:** Companies stopped asking "design for 1B users scale" as the primary question. They now ask "design for correctness first, then scale."

**What this means in interviews:**
- "What happens when this service goes down mid-transaction?"
- "How do you ensure your system is consistent after a network partition?"
- "Walk me through the failure modes of your design."
- "How do you test distributed failures? (chaos engineering, fault injection)"

**Topics to master:**
- Two-phase commit (2PC) and its limitations
- Saga pattern (choreography vs orchestration) with failure compensation
- Outbox pattern for reliable event publishing
- Idempotency at every layer (HTTP, Kafka, DB)
- Optimistic vs pessimistic locking with real tradeoffs
- Distributed deadlock detection
- Fencing tokens in distributed locks

---

### Trend 5: Java 21+ Features Being Asked (New in 2025)

**Questions appearing in 2025 interviews:**
- "What are virtual threads (Project Loom)? How do they differ from OS threads?"
- "When would you use virtual threads vs reactive programming?"
- "What are sealed classes? Pattern matching for switch — give an example."
- "Explain records in Java — when are they useful? What are their limitations?"
- "What is structured concurrency in Java 21?"

**Companies asking this:** Goldman Sachs (Java 21 migration), Flipkart, Atlassian, Walmart.

---

### Trend 6: Cost Optimization / FinOps Questions

**New in 2025:**
- "How do you optimize AWS costs for a Kafka-based pipeline?"
- "Your service costs ₹50L/month on cloud. How would you reduce it by 30%?"
- "Walk me through how you'd right-size your Kubernetes pods."

**Why this matters:** Post-2023 layoffs and profitability focus means companies want engineers who think about cost, not just scale.

---

### Trend 7: Security Engineering at SDE-2 Level

**Questions now appearing:**
- "How do you prevent SQL injection in Hibernate/JPA?"
- "Explain OWASP Top 10 — which 3 are most relevant to payment APIs?"
- "How do you handle secrets in Kubernetes? (Vault, K8s Secrets, sealed secrets)"
- "What is SSRF? How do you prevent it in a webhook receiving system?"
- "How do you implement rate limiting as a security measure vs as a UX measure?"

---

## 4. WHAT CHANGED FOR 5+ YOE vs 3 YOE {#seniority-expectations}

### The Core Difference

```
3 YOE candidate expected to: DO things correctly.
5+ YOE candidate expected to: DECIDE what the right thing to do IS, then do it correctly.
```

This single insight explains every difference in expectations.

---

### DSA Expectations

| Aspect | 3 YOE | 5+ YOE |
|--------|-------|--------|
| Problem difficulty | Easy-Medium | Medium, some Hard |
| Time to solve | 45 min per problem | 25-30 min per problem |
| After solving | Done | "Can you scale this for distributed input?" |
| Communication | Explain approach | Explain approach + trade-offs + alternatives considered |
| Code quality | Functional | Clean + production-ready patterns |

**Key shift at 5+ YOE:** DSA is table stakes, not the main event. You fail if you can't solve Medium problems. You pass if your system design and depth impress.

---

### System Design Expectations

| Aspect | 3 YOE | 5+ YOE |
|--------|-------|--------|
| Scope | "Design a URL shortener" | "Design Twitter at 100M DAU" |
| Depth | 1 component deep | 3 components deep, failure modes |
| Trade-offs | Mentioned | Argued with numbers |
| Capacity estimation | Not expected | Expected and should be fluent |
| Failure handling | Basic | Comprehensive (retries, DLQ, circuit breaker, idempotency) |
| Ownership | Implement a design | "I designed this, here's why I chose X over Y" |

---

### Leadership Signals Expected at 5+ YOE

**Signals interviewers look for:**

1. **Technical influence without authority:**
   "Have you convinced a team to change their technical approach? How?"

2. **Cross-functional impact:**
   "Tell me about a time your technical work impacted another team or product."

3. **Mentorship:**
   "Have you mentored junior engineers? What was your approach?"

4. **Driving ambiguity to clarity:**
   "Tell me about the most ambiguous project you worked on. How did you define it?"

5. **Technical risk management:**
   "Tell me about a time you identified a technical risk before it became a problem."

**GSTN STAR stories that demonstrate these:**
- Driving the common framework library (technical influence at org level)
- XA transaction design that prevented data inconsistency across teams
- DLQ framework that was adopted by 5+ teams
- E-invoicing mandate delivery under government deadline (ambiguity + risk)

---

### Java Depth Expected at 5+ YOE

```
3 YOE bar:
- Knows Spring Boot, @Transactional, basic JPA
- Understands thread safety conceptually
- Can write basic concurrent code

5+ YOE bar:
- Explains @Transactional proxy mechanism and self-invocation limitation
- Can debug a deadlock from a thread dump
- Knows ConcurrentHashMap internals (segment → bucket CAS)
- Understands happens-before and JMM
- Can explain G1GC vs ZGC trade-offs for their use case
- Has opinion on when to use reactive vs blocking I/O
- Has production debugging experience with JVM tools (jstack, jmap, async-profiler)
```

---

### Behavioral Round at 5+ YOE

**New questions that don't appear at 3 YOE:**
- "What's the largest system you've owned? What would you do differently now?"
- "Tell me about a time you pushed back on a product requirement for technical reasons."
- "Describe your approach to technical debt — when do you pay it down vs accept it?"
- "How do you onboard a new engineer to a complex system you built?"
- "Tell me about a time you influenced engineering culture."
- "What's a technology decision you made that you later regretted?"

---

## 5. JAVA/SPRING BOOT/KAFKA PATTERN FREQUENCY MAP {#java-kafka-patterns}

### Java Topics by Company Frequency

```
Topic                                          | GS | FK | Amzn | PhPe | Swiggy | Wlmrt
-----------------------------------------------|----|----|------|------|--------|------
Lock escalation (biased/thin/fat)              | ●● | ●  |      |      |        |
JMM / happens-before                           | ●● | ●  |  ●   |      |        |
ConcurrentHashMap internals                    | ●  | ●● |  ●   |  ●   |  ●     |  ●
@Transactional proxy + self-invocation         | ●  | ●● |  ●   |  ●●  |  ●     |  ●●
ThreadLocal + memory leaks                     | ●● | ●  |      |      |        |
G1GC / ZGC concepts                            | ●  | ●  |  ●   |      |        |  ●
CompletableFuture chain                        | ●  | ●  |  ●●  |  ●   |        |
Java 8 Streams + internals                     |    | ●  |  ●   |  ●   |  ●     |  ●●
Optional usage patterns                        |    | ●  |      |  ●   |  ●     |
Volatile + atomicity guarantees                | ●● | ●  |  ●   |      |        |
False sharing + @Contended                     | ●● |    |      |      |        |
Spring WebFlux vs MVC                          |    | ●  |      |  ●   |  ●●    |
Java 21 virtual threads                        | ●  | ●  |      |      |        |  ●
ReentrantLock vs synchronized                  | ●● | ●  |  ●   |      |        |
ExecutorService internals                      | ●  | ●  |  ●   |      |        |
```

### Kafka Topics by Company Frequency

```
Topic                                          | GS | FK | Amzn | PhPe | Swiggy | Rzpay
-----------------------------------------------|----|----|------|------|--------|------
Exactly-once semantics + caveats               |    |  ● |  ●   |  ●● |  ●     |  ●●
Consumer group rebalancing                     |    |  ● |  ●   |  ●● |  ●     |  ●
Idempotent producer config                     |    |    |  ●   |  ●● |        |  ●●
Kafka transactions (atomic produce+consume)    |    |    |      |  ●● |        |  ●
DLQ pattern + retry topic design               |    |  ● |  ●●  |  ●  |  ●     |  ●
Schema Registry + Avro evolution               |    |  ● |  ●   |  ●  |        |  ●
Transactional outbox pattern                   |    |    |  ●   |  ●● |        |  ●●
Consumer lag monitoring + alerting             |    |  ● |  ●   |  ●  |  ●     |
Partition design + ordering guarantees         |    |  ● |  ●   |  ●  |        |  ●
Compacted topics                               |    |    |  ●   |  ●  |        |
Kafka Streams vs Flink                         |    |    |  ●   |     |        |
```

### The 5 Kafka Questions Every Senior Backend Engineer Must Nail

**Q1: "How do you achieve exactly-once in Kafka?"**

```
Wrong answer: "Enable enable.idempotence=true"

Correct answer:
1. Idempotent producer (enable.idempotence=true) ensures no duplicates within a session
   — uses sequence numbers + PID (producer ID) per partition
2. Kafka transactions (transactional.id) ensure atomic multi-partition writes
3. Consumer: read_committed isolation level + atomic process+commit in one DB transaction
4. BUT: Kafka transactions are exactly-once within Kafka. For consumer-side processing
   (writing to DB), you still need idempotent consumers OR transactional outbox.
5. The "exactly-once" guarantee is actually "effectively exactly-once" — given retries, you
   may process twice but idempotency keys prevent duplicate effects.
```

**Q2: "What happens during a Kafka consumer group rebalance?"**

```
1. Trigger: new consumer joins, consumer dies, topic partitions change, or heartbeat timeout
2. All consumers stop processing (stop-the-world for cooperative rebalancing is improved)
3. Group coordinator (broker) revokes all partition assignments
4. JoinGroup request sent by all consumers
5. Leader consumer (first to join) receives member list + subscriptions
6. Leader computes assignment (default: RangeAssignor or RoundRobinAssignor)
7. SyncGroup called — coordinator distributes assignments
8. Consumers resume processing from last committed offset

Problems:
- Long rebalance if heartbeat.interval.ms / session.timeout.ms misconfigured
- Uncommitted offsets are reprocessed (need idempotent consumers)
- Solution: Cooperative rebalancing (incremental) in Kafka 2.4+ — avoids full stop-the-world
- IncrementalCooperativeStickyAssignor maintains partition affinity across rebalances
```

**Q3: "How does the transactional outbox pattern work?"**

```
Problem: You update DB and publish to Kafka. If Kafka publish fails, DB is committed but
event is lost. If DB commit fails, Kafka has event but DB doesn't. Classic dual-write problem.

Outbox Pattern:
1. In the SAME DB transaction:
   - Write business entity (e.g., PaymentCompleted)
   - Write to outbox table (id, topic, payload, status=PENDING)
2. Separate "outbox relay" process:
   - Poll outbox table for PENDING records
   - Publish to Kafka
   - Update status to PUBLISHED (or delete row)
3. Use idempotent Kafka producer — if relay crashes between publish and update,
   it retries and the duplicate is deduped by Kafka

Alternatives:
- Debezium (change data capture): reads DB transaction log → publishes to Kafka
  — Zero-latency, no polling, but requires Debezium infrastructure
```

**Q4: "How do you handle consumer lag spikes?"**

```
Root causes and solutions:
1. Increased message rate → Scale consumer instances (up to partition count)
2. Consumer processing is slow → Profile the processing code, add async processing
3. Batch size too small → Increase max.poll.records
4. GC pauses → Tune JVM GC, switch to ZGC for low-latency
5. Downstream dependency slow (DB, external API) → Circuit breaker, async processing
6. Rebalancing loop → Fix heartbeat/session timeout ratio (heartbeat < session/3)

Monitoring: consumer_lag_sum metric, alert at 2x normal baseline
Action: PagerDuty runbook → check Kafka UI → identify slow partitions → trace processing
```

**Q5: "Explain Kafka partition design decisions"**

```
Key questions to answer before deciding partition count:
1. What is peak throughput? (messages/sec per partition ≈ 10-100k depending on message size)
2. What is maximum consumer parallelism needed? (partition count = max parallel consumers)
3. Are there ordering requirements? (messages with same key → same partition)
4. What is your retention and disk budget?

Rules of thumb:
- Over-partition: Too many partitions = too many file handles, longer leader election
- Under-partition: Cannot add consumers beyond partition count
- Good default: Start with 3-12 partitions per topic, monitor and increase
- Payment systems: Partition by customer_id or transaction_id for ordering
- At GSTN: GSTIN (taxpayer ID) as partition key → ordered processing per taxpayer
```

---

## 6. COMMON FAILURE REASONS BY TIER {#failure-reasons}

### Tier S (Google, Meta, Amazon, Goldman)

**DSA Failure:**
- Cannot solve Hard problems within 35–40 minutes
- Writes brute force but cannot optimize when pushed ("Can we do better?")
- Correct logic but buggy implementation (off-by-one, null pointer, wrong base case)
- Cannot explain time/space complexity convincingly
- Freezes when given a problem they haven't seen before

**System Design Failure:**
- Starts designing before clarifying requirements (immediately disqualifying at Google)
- Cannot do back-of-envelope estimation (should take <2 minutes)
- Designs for the "easy path" — doesn't address failure modes
- Cannot go deep when interviewer probes: "Tell me more about how you'd do that."
- Never mentions monitoring, alerting, capacity planning
- Proposes overly complex solutions (YAGNI violation)

**Behavioral/LP Failure (Amazon-specific):**
- Generic stories without specific metrics ("we improved it a lot")
- Stories where "we" did everything, "I" did nothing
- Cannot recall specific details when probed (fake/embellished stories)
- No conflict/challenge in any story (unbelievable)
- Defensive when interviewer questions past decisions

**Java/Technical Failure (Goldman-specific):**
- Cannot explain your own code under live scrutiny
- Knows Spring works, cannot explain the proxy mechanism
- Has never debugged a production JVM issue (no jstack/heap dump experience)
- Memorized theory, cannot apply it ("What would happen to your code if two threads did X simultaneously?")

---

### Tier 1 (Flipkart, Uber, PhonePe, Stripe)

**LLD Failure (Flipkart-specific):**
- Draws a class diagram but cannot write working Java code
- Cannot apply design patterns correctly under pressure
- Missing SOLID principles in the design (God class, no abstraction)
- Cannot extend the design when interviewer says "now add feature X"
- Thread safety not considered in concurrent scenarios

**System Design Failure:**
- Shallow trade-off analysis: "I'd use Kafka here" without explaining why vs alternatives
- Cannot handle follow-up: "Your system is running but 3 partitions fail — now what?"
- Never discusses data consistency models (eventual vs strong — when to use which)
- Payment systems specifically: doesn't mention idempotency in the first 5 minutes

---

### Tier 2 (Razorpay, Swiggy, CRED, Meesho)

**Most common failures:**
- Weak behavioral stories — these companies care more than FAANG candidates realize
- Cannot explain past work clearly (rambling, no structure)
- Java is surface-level — cannot explain when @Transactional would NOT work
- System design is too textbook — lacks original thinking or domain-specific knowledge
- Poor fit signals — not researching the company's actual tech stack and products

---

### Tier 3 (Paytm, Neobanks, MakeMyTrip)

**Most common failures:**
- Overconfidence — candidates underprep because they assume these are "easy"
- Cannot write clean code live (no IDE, whiteboard or shared doc)
- Behavioral round underestimated — even Tier 3 companies ask STAR questions
- No knowledge of company product domain (don't know what Jar/Jupiter/Fi actually does)

---

## 7. WHAT "SENIOR" MEANS AT EACH COMPANY {#senior-bar}

### Google — L5 is true Senior

```
L4 (SDE-2 equivalent): Executes well-defined technical work. Owns a component.
L5 (SDE-3 equivalent): Identifies what to build. Owns a service or feature area.
                        Technical depth across 2+ domains. Mentors L4s.

L4→L5 signals Google looks for:
- Demonstrates independent technical judgment (not just following specs)
- Has multiplied other engineers' effectiveness
- Shows product + engineering thinking ("this technical decision impacts users X way")
- Can disagree with tech lead technically and be right
```

### Amazon — SDE-2 is mid-level; SDE-3 is senior

```
SDE-2 (India): Owns features within a service. Some ambiguity ok.
SDE-3 (India): Owns a service or cross-service initiative. Removes ambiguity for others.

SDE-3 signals Amazon looks for:
- "Earns Trust" LP — team trusts your technical judgment without checking
- Has led a project with 2+ engineers working under direction
- Writes design documents that others use
- Defines technical standards for the team
```

### Goldman Sachs — Associate is the target level

```
Analyst = 0-2 YOE (not relevant)
Associate = 2-6 YOE → THIS IS YOUR TARGET
VP = 6-12 YOE

Associate signals GS looks for:
- Java mastery (not just usage — internals + tuning)
- Financial domain literacy (you don't need a finance degree, but you must speak the language)
- Production reliability mindset: "This system cannot be down during market hours"
- Structured, precise communication (financial services culture)
```

### Flipkart — SDE-2 vs SDE-3

```
SDE-2: Works within a team, owns 1-2 services, participates in design
SDE-3: Drives the design, mentors SDE-2s, cross-team technical decisions

SDE-3 hiring bar at Flipkart has INCREASED since 2024 — they expect genuine tech lead signals.
If you're interviewing as SDE-3, prepare:
- A project you led technically (designed + delivered with a team)
- A time you set technical direction that others followed
- A production incident you owned end-to-end
```

### PhonePe — SDE-2 is the most hired level

```
PhonePe's internal levelling is closer to FAANG than most Indian companies.
SDE-2 at PhonePe ≈ SDE-3 at typical startup.

They look for:
- Payment domain expertise (major differentiator vs generic backend engineers)
- Strong distributed systems thinking (NPCI integration has strict reliability SLAs)
- Ownership culture — "I built this, this is my service"
```

### Zerodha — No formal levels

```
Zerodha doesn't have SDE-1/2/3 titles. It's flat.
"Senior" means: builds systems with minimal supervision, deep technical craft.
They value intellectual curiosity and depth over resume credentials.
```

### Neobanks (Slice, Jupiter, Fi, Jar) — Early senior bar

```
5+ YOE at these companies = potential tech lead. They move fast and have thin layers.
"Senior" often means: you'll own an entire domain (payments, accounts, cards).
These are good Phase 1 targets because the senior bar is reachable with your GSTN background.
```

---

## 8. NEW TOPICS BEING ASKED IN 2025–2026 {#new-topics}

### Topic 1: LLM/AI Infrastructure (2025 addition)

**Questions appearing at Amazon, Flipkart, Swiggy (AI teams):**
- "How would you build a RAG (Retrieval-Augmented Generation) pipeline backend?"
- "Design a vector search service for product recommendations"
- "How do you serve LLM predictions at low latency? (caching, batching, streaming)"
- "Design an evaluation pipeline for LLM-generated content quality"

**What you need to know (minimal viable):**
- What a vector database is (Pinecone, Weaviate, pgvector)
- What embeddings are conceptually
- How to stream tokens from an LLM API (SSE, chunked transfer)
- How to implement a semantic cache (cache LLM responses by embedding similarity)

---

### Topic 2: eBPF and Observability Infrastructure

**Questions appearing at Uber, Coinbase, infrastructure-focused roles:**
- "How does eBPF work? What can you observe with it?"
- "Design a distributed tracing system from scratch"
- "How would you implement continuous profiling in production?"

---

### Topic 3: WebAssembly (WASM) and Edge Computing

**Niche but appearing at Cloudflare India, some FAANG roles:**
- "What is WASM? When would you run Java in a WASM runtime?"
- "Design a CDN that runs business logic at the edge"

---

### Topic 4: Kubernetes Operator Pattern

**Appearing at Nutanix, InfraCloud, platform engineering roles:**
- "What is a Kubernetes operator? Write a simple CRD + controller design."
- "How does the reconciliation loop work in a K8s controller?"
- "How would you build an operator to manage Kafka topics declaratively?"

**GSTN Advantage:** You run Docker/K8s in production. Extend your knowledge to operators.

---

### Topic 5: Event-Driven Architecture with Exactly-Once Guarantees

**Not new but depth has increased (2025):**
- Previously: "Do you know Kafka?" was sufficient
- Now: "Explain the transactional outbox pattern and walk me through the failure modes"
- Now: "What is Kafka's exactly-once semantics? What are its limitations?"
- Now: "How do you handle schema evolution without breaking consumers?"

---

### Topic 6: API Design as a Product

**Appearing at Stripe, Atlassian, Razorpay:**
- "Design a REST API that developers will love. What makes an API 'excellent'?"
- "How do you version APIs without breaking existing consumers?"
- "What is the difference between REST, GraphQL, and gRPC? When do you use each?"
- "How does Stripe's idempotency key implementation work?"

---

### Topic 7: Database Deep Dives (2025 Intensity Increase)

**Previously medium depth. Now deep at fintech companies:**
- "Explain MVCC in PostgreSQL. What is the vacuum process?"
- "How does MySQL InnoDB's B+ tree index work for range queries?"
- "What is a covering index? How does it differ from a composite index?"
- "How would you design a database schema for an immutable ledger?"
- "Explain the difference between optimistic locking with version field vs timestamp vs hash"
- "What is the phantom read problem? How does PostgreSQL's repeatable read prevent it?"

---

## 9. SPECIFIC QUESTIONS FROM LEETCODE DISCUSS / BLIND / GLASSDOOR {#specific-questions}

### Amazon (SDE-2, Bangalore 2024–2025)

**DSA (reported on LeetCode Discuss):**
- LC 23: Merge K Sorted Lists (heap)
- LC 253: Meeting Rooms II
- LC 295: Find Median from Data Stream
- LC 127: Word Ladder (BFS)
- LC 146: LRU Cache
- LC 42: Trapping Rain Water
- LC 200: Number of Islands
- LC 322: Coin Change
- LC 297: Serialize and Deserialize Binary Tree
- LC 1: Two Sum (warm-up, should solve in 3 minutes)

**System Design (reported on Glassdoor/Blind):**
- Design Amazon Package Tracking (most common — 30% of reported rounds)
- Design a Distributed ID Generator
- Design Rate Limiter
- Design Notification System
- Design Flash Sale System
- Design Amazon Product Search

**Leadership Principles (most reported on Blind):**
- "Describe a time you took ownership of a failing project" (Ownership)
- "Tell me about a time you disagreed with your manager" (Disagree and Commit)
- "Tell me about your most complex debugging experience" (Dive Deep)
- "Describe the most customer-impacting system you built" (Customer Obsession)

---

### Flipkart (SDE-2, Bangalore 2024–2025)

**DSA (reported):**
- LC 297: Serialize and Deserialize Binary Tree (70% reported, know this cold)
- LC 895: Maximum Frequency Stack
- LC 295: Median from Data Stream
- LC 460: LFU Cache (SDE-3 level)
- LC 239: Sliding Window Maximum
- LC 76: Minimum Window Substring
- LC 45: Jump Game II
- LC 763: Partition Labels

**LLD (reported):**
- Parking Lot: Write full Java code (Strategy, Factory, Singleton)
- Movie Ticket Booking: Seat reservation with expiry timer
- Inventory Management System with concurrent updates
- Cab booking system (simplified)

**Java (reported):**
- ConcurrentHashMap internals (asked in 60% of Flipkart Java rounds)
- @Transactional + self-invocation (asked in 50% of rounds)
- Explain how Spring Boot starter works (what does @SpringBootApplication do)
- How does Spring resolve circular bean dependencies?

---

### Goldman Sachs (SDE-2, Bangalore 2024–2025)

**Concurrency (from LeetCode Discuss + Blind):**
- "Implement a thread-safe bounded blocking queue" (write from scratch)
- "Implement a read-write lock without using Java's ReentrantReadWriteLock"
- "What is the ABA problem in CAS? How do you prevent it?" (AtomicStampedReference)
- "Explain how Doug Lea designed ConcurrentHashMap in Java 8"
- "Write a producer-consumer where producer blocks when queue is full"

**System Design (reported):**
- Design a distributed rate limiter for trading APIs
- Design a trade order management system
- Design a real-time P&L calculation system
- Design a distributed cache for financial reference data

---

### PhonePe (SDE-2, Bangalore 2024–2025)

**System Design (most reported):**
- UPI payment flow design (most common — every reported round)
- Idempotency in payment APIs (asked in 80% of rounds)
- Kafka consumer exactly-once for payments
- Wallet system with concurrent balance updates
- Transaction reconciliation system

**DSA (reported):**
- LC 146: LRU Cache
- LC 347: Top K Frequent Elements
- LC 56: Merge Intervals
- LC 53: Maximum Subarray (Kadane's)
- LC 207: Course Schedule (topological sort)

---

### Razorpay (SDE-2, Bangalore 2024–2025)

**Take-home assignment (reported):**
- "Build a simplified payment gateway" — Spring Boot, REST, MySQL, idempotency
- "Build a webhook delivery system" — retry, ordering, at-least-once
- "Build a rate limiter" — sliding window, configurable per customer

**System Design (reported):**
- Webhook delivery system (in-depth, extends take-home)
- Payment link system (expiry, concurrent purchases)
- Payout system (bulk, async, reconciliation)
- API rate limiter design

---

### Swiggy (SDE-2, Bangalore 2024–2025)

**DSA (reported):**
- LC 380: Insert Delete GetRandom O(1)
- LC 743: Network Delay Time (Dijkstra)
- LC 399: Evaluate Division (graph)
- LC 490: The Maze (BFS/DFS)
- LC 1162: As Far from Land as Possible (multi-source BFS)

**System Design (reported):**
- Real-time order tracking (WebSocket/SSE + Kafka + Redis pub/sub)
- Delivery partner assignment algorithm
- Surge pricing engine
- Dark store inventory management

---

### CRED (SDE-2, Bangalore 2024–2025)

**LLD (reported):**
- Rewards engine (most common — 60% of reported LLD rounds)
- Credit card statement generation
- CRED Pay flow design
- Expense tracking system

**Culture/Values (IMPORTANT — reported as make-or-break):**
- "Why CRED? What draws you to this product?"
- "What's a product you use that has excellent engineering?"
- "Tell me about a time code quality was sacrificed under deadline. What did you do?"

---

### Meesho (SDE-2, Bangalore 2024–2025)

**System Design (reported):**
- Seller onboarding and catalog management
- Returns and refund system
- Bulk order processing pipeline

**Behavioral (reported as important):**
- "Tell me about the most impactful system you built"
- "Describe a time you optimized for low-cost infra"
- "How do you handle tech debt in a fast-moving team?"

---

## 10. INTERVIEW FORMAT REFERENCE CARD {#format-card}

### Quick Reference — Rounds by Company

```
Company          | OA | Phone | Tech1 | Tech2 | SD  | LLD | Behav | Total
-----------------|----+-------+-------+-------+-----+-----+-------+------
Amazon           | ●  |   ●   |   ●   |   ●   |  ●  |     |  ●    |  5-6
Google           |    |   ●   |   ●   |   ●   |  ●  |     |  ●    |  5-6
Flipkart         | ●  |       |   ●   |       |  ●  |  ●  |  ●    |  4-5
Goldman Sachs    | ●  |   ●   |   ●   |       |  ●  |     |  ●    |  4-5
PhonePe          | ●  |       |   ●   |       |  ●  |     |  ●    |  3-4
Razorpay         | TH |       |   ●   |       |  ●  |     |  ●    |  3-4
Swiggy           | ●  |       |   ●   |       |  ●  |     |  ●    |  3-4
CRED             | ●  |       |   ●   |       |  ●  |  ●  |  ●    |  3-4
Atlassian        | ●  |       |   ●   |       |  ●  |     |  ●●   |  4-5
Zerodha          | WS |       |   ●   |   ●   |     |     |  ●    |  3-4
Walmart          | ●  |       |   ●   |       |  ●  |     |  ●    |  3-4

● = standard round
TH = take-home assignment
WS = work sample (real-world problem)
●● = values interview (Atlassian-specific)
```

### Time Breakdown Per Round

```
DSA Round:    45-60 min | 5 min clarify → 30-35 min code → 5-10 min optimize → 5 min complexity
SD Round:     60 min    | 5 min requirements → 5 min estimate → 20 min HLD → 20 min deep dive → 10 min failure modes
LLD Round:    45-60 min | 5 min clarify → 15 min design → 25-30 min code → 5 min extensibility
Behavioral:   30-45 min | 2-3 STAR stories, 15 min each
Java Deep:    45-60 min | Mix of questions, expect 5-8 conceptual questions + 1 coding
```

---

## APPENDIX A: SALARY BENCHMARKS — DETAILED (March 2026)

### Base Salary Ranges (Bangalore, in-hand CTC)

```
Company         | SDE-2 Base  | SDE-2 Total | SDE-3 Base  | SDE-3 Total
----------------|-------------|-------------|-------------|-------------
Google India    | ₹35-50L     | ₹70-140L    | ₹50-70L     | ₹100-200L
Amazon India    | ₹25-40L     | ₹50-100L    | ₹35-55L     | ₹70-130L
Goldman Sachs   | ₹30-45L     | ₹45-90L*    | ₹45-65L     | ₹70-120L*
Flipkart        | ₹28-42L     | ₹40-80L     | ₹40-60L     | ₹60-100L
Stripe India    | ₹30-45L     | ₹50-90L     | ₹45-65L     | ₹80-130L
PhonePe         | ₹25-38L     | ₹35-65L     | ₹35-52L     | ₹50-80L
Uber India      | ₹28-42L     | ₹40-75L     | ₹40-58L     | ₹60-100L
Atlassian       | ₹28-42L     | ₹38-72L     | ₹40-58L     | ₹60-95L
Razorpay        | ₹22-35L     | ₹28-55L     | ₹32-48L     | ₹42-72L
Swiggy          | ₹22-35L     | ₹30-55L     | ₹32-48L     | ₹45-70L
CRED            | ₹22-35L     | ₹28-52L     | ₹32-48L     | ₹42-70L
Meesho          | ₹20-32L     | ₹26-48L     | ₹28-42L     | ₹38-60L
Groww           | ₹22-35L     | ₹28-52L     | ₹32-46L     | ₹42-65L
Walmart GlobTch | ₹18-28L     | ₹22-42L     | ₹26-38L     | ₹34-56L
Paytm           | ₹16-26L     | ₹20-38L     | ₹24-36L     | ₹30-50L

* Goldman: Total includes bonus (15-40% of base). RSU is limited vs FAANG.
  FAANG: Total includes RSU (often 40-60% of total). RSU = US stock = volatile but high upside.
```

### The Negotiation Reality

```
Rule 1: Never reveal your current CTC at GSTN (government-sector pay is lower)
         → "I'm looking at market rate for my experience and skills"
         → Research: Levels.fyi India, Blind India salary threads, Glassdoor

Rule 2: Multiple offers = negotiation power
         → Phase 1 offer at ₹30L → Phase 2 negotiation starts at ₹30L not GSTN CTC

Rule 3: Equity negotiation at SDE-2 level
         → At FAANG: Negotiate RSU vesting schedule + cliff
         → At startups: Ask for ESOP %  + vesting + exercise window post-exit
         → At Goldman: Negotiate deferred bonus structure

Rule 4: Counter-offer script (after verbal offer):
         "Thank you so much for the offer. I'm very excited about [Company].
         I have a competing offer at [₹X]. Is there flexibility to match or close to that?
         I'd really prefer to join [Company] if we can make the numbers work."
```

---

## APPENDIX B: PREPARATION GAP ANALYSIS FOR JAYANTI

### Green (Already Strong — GSTN gives you this)
- Distributed systems knowledge (Kafka, Redis, caching)
- Financial domain (tax ledger = payment ledger)
- Java/Spring Boot production depth
- XA transactions and consistency guarantees
- Microservices architecture at scale
- Docker/K8s operational experience

### Yellow (Needs Sharpening — 2–4 weeks each)
- LLD practice: write full Java code, not just class diagrams
- System design framing: product company language, not government system language
- Behavioral stories: map 6 STAR stories to specific company LP frameworks
- Java internals: JMM, G1GC phases, false sharing, Java 21 features
- Kafka deep: exactly-once caveats, transactional outbox, schema evolution

### Red (Biggest Gaps — needs consistent daily work)
- DSA: LeetCode consistency (daily, not sporadic)
  - Must close: Graphs (BFS/DFS), DP (1D patterns), Sliding Window
  - Must be able to: solve Medium in <35 min, optimize when asked
- Golang: goroutines, channels, context, select (required at Zerodha, Uber, Coinbase)
- AI/ML infra framing: vector databases, model serving, feature stores (emerging requirement)

---

## APPENDIX C: MUST-DO LEETCODE LIST FOR YOUR SPECIFIC TARGETS

### High-Priority Problems (Based on Company Frequency Data Above)

```
Problem                      | LC #  | Tier      | Companies
-----------------------------|-------|-----------|----------------------------------
Serialize/Deserialize BTree  |  297  | Medium    | Flipkart (70%), Amazon, Adobe
Merge K Sorted Lists         |   23  | Hard      | Amazon, Goldman, PhonePe
LRU Cache                    |  146  | Medium    | Goldman, Amazon, Flipkart, Swiggy
Median from Data Stream      |  295  | Hard      | Amazon, Flipkart, Swiggy
Meeting Rooms II             |  253  | Medium    | Amazon, Walmart, Atlassian
Trapping Rain Water          |   42  | Hard      | Amazon (frequently), Google
Word Ladder                  |  127  | Hard      | Amazon, Flipkart
Number of Islands            |  200  | Medium    | Amazon, Swiggy, PhonePe
Top K Frequent Elements      |  347  | Medium    | PhonePe, Swiggy, Meesho
Insert Delete GetRandom O(1) |  380  | Medium    | Swiggy, Amazon, Flipkart
Minimum Window Substring     |   76  | Hard      | Flipkart, Goldman, Google
Network Delay Time (Dijkstra)|  743  | Medium    | Swiggy, Uber, OLA
Course Schedule (Top Sort)   |  207  | Medium    | PhonePe, Amazon, Goldman
Maximum Frequency Stack      |  895  | Hard      | Flipkart (SDE-3 signal)
LFU Cache                    |  460  | Hard      | Flipkart SDE-3, Google
Sliding Window Maximum       |  239  | Hard      | Flipkart, Amazon
Jump Game II                 |   45  | Medium    | Flipkart, Amazon
```

### Must-Write-From-Scratch Code (Not LeetCode — White-board style)

```
1. Thread-safe LRU Cache (HashMap + DoublyLinkedList, no Java library)
   → Goldman, Flipkart, Amazon — asked in 40% of Java coding rounds

2. Bounded Blocking Queue (wait/notifyAll from scratch)
   → Goldman, Amazon, Morgan Stanley — asked in 30% of Java concurrency rounds

3. Kafka Consumer with retry + DLQ (Spring Kafka or plain consumer)
   → PhonePe, Razorpay, Swiggy — asked in 30% of backend rounds

4. Circuit Breaker (state machine: CLOSED → OPEN → HALF_OPEN)
   → Razorpay, PhonePe, CRED — asked in 25% of system design rounds

5. Idempotent API handler (idempotency key in Redis/DB)
   → PhonePe, Razorpay, Juspay, Stripe — asked in 40% of fintech rounds
```

---

*Document compiled from training data through August 2025.*
*Sources: LeetCode Discuss interview experience threads, Blind India salary/interview threads,*
*Glassdoor India tech interview reviews, GeeksForGeeks interview experiences,*
*company engineering blogs (Flipkart Tech, PhonePe Engineering, Swiggy Bytes, CRED Engineering),*
*Levels.fyi India compensation data, AmbitionBox reviews.*

*This is a living document. After each interview, add your actual questions here.*
*Your own data beats any research — update after every round.*

*Last compiled: March 2026*
