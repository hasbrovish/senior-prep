# Interview Preparation Master Guide
### Based on Real Interview Experiences — Apple, Oracle, Amazon, DoorDash

---

## PART 1: TOPICS DEEP DIVE

---

### 1. DATA STRUCTURES & ALGORITHMS (DSA)

#### A. Arrays & Strings
- Two Pointers (Container with Most Water, Trapping Rain Water)
- Sliding Window (Longest Substring, Max Sum Subarray)
- Prefix techniques (Longest Common Prefix)
- Sorting & Searching within arrays

**Must-solve problems from the interviews:**
- [LRU Cache](https://leetcode.com/problems/lru-cache/) — Apple
- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) — Apple
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) — Oracle
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — Amazon
- [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) — Amazon

#### B. Stacks & Queues
- Monotonic Stack
- Expression Evaluation
- [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) — Amazon

#### C. Graphs & Trees
- BFS / DFS traversal
- Shortest path (BFS on unweighted graphs)
- Tree path problems (max path sum between nodes)
- Graph construction from real-world data (file system → graph)
- Manhattan distance, coordinate-based graph problems

**Must-solve problems from the interviews:**
- File system shortest path using BFS with HashMap<String, List<String>> — Amazon
- DashMart grid BFS (multi-source BFS) — DoorDash
- Binary tree max path sum between alive nodes — DoorDash
- Nearest city sharing coordinates (Manhattan distance) — DoorDash

#### D. Greedy & Scheduling
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) — Oracle
- Interval-based problems
- Greedy allocation (circle segments problem — Oracle)

#### E. Binary Search
- Binary search on answer (Oracle's circle segments problem uses this)
- Search in rotated arrays
- Median of two sorted arrays

#### F. Design-Oriented DSA
- LRU Cache (HashMap + Doubly Linked List)
- LFU Cache
- Trie for prefix problems
- Consistent Hashing implementation

**Resources:**
| Resource | What It Covers | Link |
|----------|---------------|------|
| NeetCode 150 | Curated pattern-based problem list | https://neetcode.io/practice |
| NeetCode YouTube | Video explanations for every pattern | https://youtube.com/@NeetCode |
| Blind 75 | The classic 75 must-do problems | https://leetcode.com/discuss/general-discussion/460599 |
| LeetCode Patterns | Problems grouped by pattern | https://seanprashad.com/leetcode-patterns/ |
| Striver's A2Z DSA Sheet | Comprehensive topic-wise list | https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2 |
| AlgoExpert | 160 hand-picked problems with video | https://www.algoexpert.io |

---

### 2. SYSTEM DESIGN

#### A. Fundamentals You Must Know

**Networking & Communication:**
- REST vs gRPC vs GraphQL
- WebSockets vs Long Polling vs SSE
- Load Balancers: L4 vs L7, Round Robin, Least Connections, Consistent Hashing
- Sticky Sessions vs Stateless Sessions (asked at Apple)
- CDN design and placement
- API Gateway pattern

**Databases:**
- SQL vs NoSQL — when to use which
- Database sharding (horizontal vs vertical)
- Replication (leader-follower, multi-leader)
- Indexing strategies (B-tree, LSM tree, hash index)
- CAP Theorem — CP vs AP systems
- ACID vs BASE
- Schema design and normalization vs denormalization

**Caching:**
- Caching strategies: Write-through, Write-back, Write-around, Read-through (Oracle)
- Cache eviction policies: LRU, LFU, FIFO
- Distributed caching (Redis, Memcached)
- Cache invalidation strategies
- Cache-aside pattern

**Distributed Systems Concepts:**
- Consistent Hashing (Oracle, asked explicitly)
- Quorum: Read Quorum, Write Quorum (Oracle)
- Bloom Filters (Oracle)
- Eventual Consistency (Apple)
- Leader Election
- Heartbeat / Failure Detection (Apple)
- Distributed Locks
- Vector Clocks / Lamport Timestamps
- Gossip Protocol

**Message Queues & Event Systems:**
- Kafka, RabbitMQ, SQS — when to use which
- Event-driven architecture
- Pub/Sub pattern
- CQRS pattern (Apple)
- SAGA pattern (Apple)
- Exactly-once, At-least-once, At-most-once delivery

**Patterns:**
- Monolithic vs Microservices (Apple)
- API Gateway
- Circuit Breaker
- Bulkhead
- Sidecar
- Strangler Fig (for migration)
- Rate Limiting (Token Bucket, Leaky Bucket, Sliding Window)

#### B. System Design Problems From These Interviews

| Problem | Company | Key Focus Areas |
|---------|---------|----------------|
| Design Apple Music | Apple | Streaming, bitrate adaptation, CDN, music metadata DB |
| Design URL Shortener | Apple | Hashing, base62, read-heavy, analytics |
| Design Amazon Order Management | Apple | State machine, saga pattern, eventual consistency |
| Design Distributed Caching | Oracle | Consistent hashing, replication, eviction, quorum |
| Design Key-Value Store | Oracle | LSM tree, compaction, replication, partitioning |
| Design Multi-Broker Portfolio Platform | Amazon | Multi-tenancy, aggregation, real-time data, schema design |
| Design Application Monitoring/Alerting | DoorDash | Event ingestion, pipeline, custom rules, SLA |

#### C. Resources

| Resource | What It Covers | Link |
|----------|---------------|------|
| **Designing Data-Intensive Applications (DDIA)** | THE book. Replication, partitioning, consistency, batch/stream processing | Book by Martin Kleppmann |
| **System Design Interview Vol 1 — Alex Xu** | 13 system designs with step-by-step walkthrough | Book |
| **System Design Interview Vol 2 — Alex Xu** | Advanced: proximity service, stock exchange, hotel reservation | Book |
| **ByteByteGo YouTube** | Alex Xu's video versions of the book content | https://youtube.com/@ByteByteGo |
| **Gaurav Sen YouTube** | Deep dives on distributed system concepts | https://youtube.com/@gaborsen |
| **System Design Primer (GitHub)** | Free, comprehensive, covers everything | https://github.com/donnemartin/system-design-primer |
| **HelloInterview** | Practice system design with AI feedback | https://www.hellointerview.com |
| **Exponent** | Mock system design interviews with solutions | https://www.tryexponent.com |
| **Jordan Has No Life YouTube** | Goes through DDIA chapter by chapter | https://youtube.com/@jordanhasnolife5163 |

---

### 3. JAVA & SPRING BOOT (Backend Focus)

#### A. Core Java

**Multithreading & Concurrency (heavily tested at Apple):**
- Thread lifecycle, Runnable vs Callable
- synchronized keyword, volatile
- ReentrantLock, ReadWriteLock
- Double-checked locking mechanism (Apple)
- Race conditions — detection and resolution (Apple)
- Deadlock — detection, prevention, avoidance (Apple)
- ThreadPool, ExecutorService, CompletableFuture
- ConcurrentHashMap, CopyOnWriteArrayList
- CountDownLatch, CyclicBarrier, Semaphore
- Producer-Consumer problem

**Design Patterns:**
- Singleton (Lazy, Eager, Thread-safe with double-checked locking) — Apple asked specifically
- Factory, Abstract Factory
- Builder
- Observer
- Strategy
- Decorator
- Proxy

**JVM Internals:**
- Garbage Collection (G1GC, ZGC, CMS)
- Heap vs Stack memory
- Memory leak detection
- JVM tuning flags (-Xmx, -Xms, -XX:+UseG1GC)
- Class loading mechanism
- JIT compilation

**Performance Monitoring & Optimization (Apple Round 2):**
- How to monitor a Java application: JMX, Micrometer, Prometheus + Grafana
- Key metrics: throughput, latency (p50, p95, p99), error rate, GC pauses
- Thread dumps and heap dumps analysis
- Profiling tools: VisualVM, JProfiler, async-profiler
- How to fix low-performing APIs: identify bottleneck → DB query? N+1? Thread contention? GC?
- Connection pool tuning (HikariCP)

#### B. Spring Boot

- Bean lifecycle and scopes (singleton, prototype, request, session)
- @Bean annotation — having multiple beans, @Qualifier, @Primary (Apple)
- Dependency Injection — constructor vs setter vs field
- Spring AOP (Aspect Oriented Programming)
- Spring Security basics
- Spring Data JPA — repositories, queries, pagination
- @Transactional — propagation levels, isolation levels
- Exception handling — @ControllerAdvice, @ExceptionHandler
- Actuator for monitoring
- Profiles and configuration management

#### C. SQL

- Joins (INNER, LEFT, RIGHT, FULL, CROSS, SELF)
- Subqueries, CTEs (Common Table Expressions)
- Window functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)
- GROUP BY, HAVING, aggregation
- Indexing — B-tree, composite index, covering index
- Query optimization — EXPLAIN ANALYZE
- Transactions and isolation levels

#### D. Resources

| Resource | What It Covers | Link |
|----------|---------------|------|
| **Java Concurrency in Practice** | THE concurrency book (Brian Goetz) | Book |
| **Effective Java (3rd ed)** | Best practices, patterns, idioms | Book by Joshua Bloch |
| **Baeldung** | Spring Boot tutorials for everything | https://www.baeldung.com |
| **Java Brains YouTube** | Spring Boot, Microservices, Java concepts | https://youtube.com/@Java.Brains |
| **Spring.io Guides** | Official Spring Boot guides | https://spring.io/guides |
| **Mode SQL Tutorial** | Intermediate-to-advanced SQL | https://mode.com/sql-tutorial |
| **StrataScratch** | SQL interview questions by company | https://www.stratascratch.com |
| **LeetCode Database** | SQL practice problems | https://leetcode.com/problemset/database/ |
| **VisualVM** | Free profiling tool — practice using it | https://visualvm.github.io |

---

### 4. DISTRIBUTED SYSTEMS (Deeper Theory)

This overlaps with system design but these concepts were asked as standalone questions at Apple and Oracle.

#### Topics to Master:
- Eventual Consistency vs Strong Consistency vs Causal Consistency
- Failure Detection: Heartbeat, Phi Accrual Failure Detector, Gossip-based
- Consensus: Raft, Paxos (at a high level)
- Conflict Resolution: Last-Write-Wins, CRDT, application-level
- Partitioning strategies: Hash, Range, Consistent Hashing
- Replication: Single leader, Multi-leader, Leaderless (Dynamo-style)
- Quorum: W + R > N for strong consistency
- Bloom Filters: Probabilistic data structure, false positives, no false negatives
- Merkle Trees: Anti-entropy, data synchronization
- Rate Limiting: Token Bucket, Leaky Bucket, Fixed/Sliding Window

#### Resources:
| Resource | What It Covers | Link |
|----------|---------------|------|
| **DDIA Chapters 5-9** | Replication, Partitioning, Transactions, Consistency | Book |
| **MIT 6.824 Lectures** | Distributed systems graduate course (free) | https://pdos.csail.mit.edu/6.824/ |
| **Martin Fowler's Blog** | Microservices, CQRS, Event Sourcing patterns | https://martinfowler.com |
| **Jepsen.io** | Real-world distributed system failure analysis | https://jepsen.io |
| **The Morning Paper** | Summaries of distributed systems papers | https://blog.acolyer.org |

---

### 5. BEHAVIORAL / LEADERSHIP PRINCIPLES

#### Amazon LP Questions (2 per round, so ~8 total):

Prepare 10-12 STAR stories covering:
- **Ownership**: A time you went beyond your role
- **Dive Deep**: A time you dug into data/metrics to find the root cause
- **Bias for Action**: A time you made a decision with incomplete information
- **Disagree and Commit**: A time you disagreed but still committed
- **Customer Obsession**: A time you prioritized the customer
- **Deliver Results**: A time you met a tight deadline
- **Earn Trust**: A time you admitted a mistake or built trust
- **Invent and Simplify**: A time you simplified a complex process
- **Think Big**: A time you proposed something ambitious
- **Have Backbone**: A time you pushed back on leadership

#### For All Companies (Managerial Rounds):
- Conflict resolution with teammates
- How you handled a production incident
- Project you're most proud of — and why
- A failure and what you learned
- How you mentor junior engineers
- How you prioritize when everything is urgent
- How you handle ambiguous requirements

#### Resources:
| Resource | What It Covers | Link |
|----------|---------------|------|
| **Amazon LP List** | All 16 Leadership Principles explained | https://amazon.jobs/content/en/our-workplace/leadership-principles |
| **Exponent Behavioral** | Structured behavioral prep with mock interviews | https://www.tryexponent.com |
| **Blind** | Real LP questions asked at Amazon by round | https://www.teamblind.com |
| **Dan Croitor YouTube** | Amazon LP interview prep, 100+ videos | https://youtube.com/@DanCroitor |

---

## PART 2: 8-WEEK STUDY PLAN

---

### Week 1-2: DSA Foundations
**Daily: 3-4 problems, 2-3 hours**

| Day | Focus | Problems |
|-----|-------|----------|
| 1 | Arrays + Two Pointers | Container With Most Water, Trapping Rain Water, 3Sum |
| 2 | Sliding Window | Longest Substring Without Repeating, Min Window Substring |
| 3 | Stacks | Evaluate Reverse Polish Notation, Valid Parentheses, Daily Temperatures |
| 4 | Linked Lists | LRU Cache, Reverse Linked List, Merge K Sorted Lists |
| 5 | Binary Search | Search in Rotated Array, Binary Search on Answer problems |
| 6 | Strings | Longest Common Prefix, Group Anagrams |
| 7 | Review + Revisit unsolved problems |
| 8-14 | Repeat above cycle with harder variants from NeetCode 150 |

**Also start**: Read DDIA Chapter 1-2 (30 min/day)

---

### Week 3-4: Graphs, Trees & Advanced DSA
**Daily: 3-4 problems, 2-3 hours**

| Day | Focus | Problems |
|-----|-------|----------|
| 1 | BFS basics | Rotten Oranges, Multi-source BFS (DashMart-style) |
| 2 | Graph construction | File system → graph (Amazon), Nearest city (DoorDash) |
| 3 | Tree DFS | Max Path Sum, Diameter of Binary Tree |
| 4 | Tree variants | Max path between alive nodes, Lowest Common Ancestor |
| 5 | Greedy/Scheduling | Task Scheduler, Meeting Rooms II |
| 6 | Binary Search on Answer | Oracle's circle segments, Koko Eating Bananas |
| 7 | Review all weak areas |
| 8-14 | Hard variants + timed practice (25 min per medium, 40 min per hard) |

**Also start**: DDIA Chapters 3-5 + start System Design Primer on GitHub

---

### Week 3-5: System Design Foundations (Overlap with DSA)
**Daily: 1 hour system design reading + 1 design per 2 days**

| Week | Focus | Practice Design |
|------|-------|----------------|
| 3 | Databases, Indexing, Sharding (DDIA Ch 3, 5, 6) | Design URL Shortener |
| 4 | Caching, CDNs, Load Balancing | Design Distributed Cache (Oracle) |
| 5 | Message Queues, Event Driven, CQRS/SAGA | Design Order Management System |

**How to practice**: For each design, write out on paper or whiteboard:
1. Functional requirements (3-5)
2. Non-functional requirements (3-5)
3. API design
4. Data model
5. High-level architecture
6. Deep dives (2-3 components)
7. Bottlenecks and tradeoffs

---

### Week 5-6: Java, Spring Boot & SQL
**Daily: 1.5 hours**

| Topic | Time | What to Do |
|-------|------|-----------|
| Multithreading | 3 days | Write code for: Thread pool, Producer-Consumer, Deadlock simulation, Double-checked locking singleton |
| Spring Boot | 2 days | Build a small REST API with @Bean, @Qualifier, @Transactional, exception handling |
| Design Patterns | 2 days | Implement Singleton (all variants), Factory, Observer, Strategy in Java |
| SQL | 3 days | 30 LeetCode SQL problems (Medium+Hard), practice window functions and CTEs |
| Performance | 2 days | Set up VisualVM, practice taking thread dumps, learn to read GC logs |
| JVM | 2 days | Study GC algorithms, practice JVM tuning flags |

---

### Week 6-7: Advanced System Design
**Daily: 1 full design per day, present out loud**

| Day | Design Problem |
|-----|---------------|
| 1 | Design Apple Music (streaming, bitrate, CDN) |
| 2 | Design Key-Value Store (Oracle — LSM tree, compaction) |
| 3 | Design Multi-Broker Portfolio Platform (Amazon) |
| 4 | Design Application Monitoring & Alerting System (DoorDash) |
| 5 | Design Notification System |
| 6 | Design Chat/Messaging System |
| 7 | Design Rate Limiter |

**For each**: Practice explaining out loud for 35-40 minutes. Record yourself. Watch it back.

---

### Week 7-8: Behavioral Prep + Mock Interviews
**Daily: 1 mock per day**

| Day | Activity |
|-----|---------|
| 1-2 | Write all 10-12 STAR stories, map to Amazon LPs |
| 3 | Mock DSA interview (Pramp or Interviewing.io) |
| 4 | Mock System Design interview (with a friend or Exponent) |
| 5 | Mock Behavioral interview (record yourself) |
| 6 | Mock DSA interview |
| 7 | Mock System Design interview |
| 8-14 | Alternate: DSA mock → System Design mock → Behavioral mock |

---

## PART 3: WHERE TO FIND REAL INTERVIEW EXPERIENCES

| Source | Best For | Link |
|--------|----------|------|
| **Blind (TeamBlind)** | Detailed round-by-round breakdowns, compensation data | https://www.teamblind.com |
| **LeetCode Discuss** | Company-tagged DSA problems + interview experiences | https://leetcode.com/discuss/interview-experience |
| **Glassdoor** | Interview process overview, behavioral questions | https://www.glassdoor.com |
| **1point3acres** | Extremely detailed reports (Chinese + English) | https://www.1point3acres.com |
| **Reddit** | r/cscareerquestions, r/leetcode, r/experienceddevs | https://www.reddit.com |
| **Levels.fyi** | Compensation data + some interview experiences | https://www.levels.fyi |
| **GitHub repos** | Search "company interview questions" for curated lists | https://github.com |
| **YouTube** | Mock interview recordings from real engineers | NeetCode, Exponent, Clément Mihailescu |

**Pro tip**: On Blind, search "[Company] interview experience 2024" or "[Company] onsite". Sort by recent. People often share exact LeetCode problem numbers.

---

## PART 4: DAILY ROUTINE TEMPLATE

```
Morning (2 hours)    → DSA: 2-3 problems, focus on one pattern
Afternoon (1.5 hours) → System Design reading OR Java deep dive
Evening (1 hour)      → System Design practice OR SQL problems
Before bed (30 min)   → Behavioral story prep OR review notes
Weekend (3-4 hours)   → Full mock interview + review weak areas
```

---

## PART 5: KEY BOOKS (Priority Order)

1. **Designing Data-Intensive Applications** — Martin Kleppmann *(System Design + Distributed Systems)*
2. **System Design Interview Vol 1** — Alex Xu *(Structured system designs)*
3. **System Design Interview Vol 2** — Alex Xu *(Advanced designs)*
4. **Java Concurrency in Practice** — Brian Goetz *(Threading + Concurrency)*
5. **Effective Java** — Joshua Bloch *(Clean Java patterns)*
6. **Cracking the Coding Interview** — Gayle McDowell *(DSA fundamentals if needed)*

---

## QUICK REFERENCE: Company-Specific Focus

| Company | Primary Focus | Unique Emphasis |
|---------|--------------|----------------|
| **Apple** | Spring Boot + DSA + System Design | Deep Java internals, multithreading, monitoring, performance optimization |
| **Oracle** | DSA (harder) + System Design | Distributed systems theory (quorum, bloom filters, consistent hashing) |
| **Amazon** | DSA + System Design + LPs | Leadership Principles are make-or-break, 2 LP questions per round |
| **DoorDash** | DSA (graph-heavy) + System Design | Real-world modeling (grid BFS, tree path problems), event systems |
