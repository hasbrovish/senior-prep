# 6-Month Advanced Backend Engineering Mastery
### The Complete Roadmap to Becoming a Demanded, Competent, Thriving Developer
### For someone with 5 YOE who wants to go from "knows how" to "knows why and beyond"

---

## THE MISSION

You are not starting from zero. You have 5 years of experience. What you need is not beginner knowledge — you need to **fill the gaps that separate a "working developer" from an "engineer companies fight to hire."**

This roadmap covers EVERYTHING:
- Advanced Backend Engineering (Java deep, Go, Python)
- JVM Internals, Memory Management, Performance Tuning
- Clean Code, SOLID, Design Patterns (practical, not textbook)
- Machine Coding / Low-Level Design (LLD) Rounds
- CS Fundamentals: OS, Networking, Databases (the parts that matter)
- DSA (interview-focused, pattern-based)
- AI-Augmented Engineering (using AI as a force multiplier)
- Communication, Requirement Gathering, Decision Making
- Building a profile that attracts recruiters

---

## MONTH 1: CS FUNDAMENTALS THAT ACTUALLY MATTER
### Theme: Rebuild the foundation — but this time, understand WHY everything works

Most developers learned OS, Networking, and DB in college and forgot 90% of it. In interviews at Apple, Oracle, Amazon — these fundamentals come up constantly. You need them not for theory, but to make better engineering decisions.

---

### Week 1: Operating System Essentials (What Every Backend Dev Must Know)

**Why this matters:** When Apple asks about deadlocks, when Amazon asks about thread contention, when DoorDash asks why their service is slow — the answer is always OS concepts.

**Topics to master:**

Process & Thread Management:
- Process vs Thread — memory sharing, context switching cost
- Thread lifecycle: New → Runnable → Running → Waiting → Terminated
- Context switching — why it is expensive, how to minimize it
- User threads vs Kernel threads
- Green threads / Virtual threads (Java 21+ Project Loom)

Concurrency & Synchronization:
- Race condition — what it is, real examples, how to detect
- Mutex vs Semaphore vs Monitor — when to use which
- Deadlock — 4 conditions (Coffman), detection, prevention, avoidance
- Livelock and Starvation
- Producer-Consumer problem
- Readers-Writers problem
- Dining Philosophers problem

Memory Management:
- Virtual memory — page tables, TLB, page faults
- Stack vs Heap memory — what goes where and why
- Memory leak — how it happens in Java (even with GC)
- Memory-mapped files (mmap)
- How the OS allocates memory to a process

I/O and File Systems:
- Blocking vs Non-blocking I/O
- I/O multiplexing: select, poll, epoll (Linux), kqueue (macOS)
- Why Nginx is fast (event-driven, non-blocking I/O)
- File descriptors
- Disk I/O: Sequential vs Random access — why this matters for databases

**Resources:**
| Resource | Link |
|----------|------|
| Operating Systems: Three Easy Pieces (FREE online book) | https://pages.cs.wisc.edu/~remzi/OSTEP/ |
| Neso Academy — OS playlist (YouTube) | https://youtube.com/@nesoacademy |
| Hussein Nasser — "Processes vs Threads" | YouTube |
| ByteByteGo — "Blocking vs Non-blocking I/O" | YouTube |

**Deliverable:** Explain to yourself: "When a Java application creates 1000 threads vs using a thread pool of 50, what happens at the OS level? Why is the thread pool better? What are the tradeoffs?"

---

### Week 2: Computer Networking for Backend Engineers

**Why this matters:** Every system design discussion involves networking. Every performance bottleneck might be a network issue. Apple asked about sticky sessions. Amazon asked about load balancers. Oracle asked about distributed systems — all networking.

**Topics to master:**

Network Layers (practical focus):
- TCP vs UDP — when to use each, handshake, reliability
- TCP connection lifecycle — 3-way handshake, TIME_WAIT, connection pooling
- HTTP/1.1 vs HTTP/2 vs HTTP/3 (QUIC) — what changed and why
- TLS/SSL — how HTTPS works, certificate chain, handshake
- DNS resolution — recursive, iterative, caching, TTL

Backend-Relevant Networking:
- Keep-alive connections and connection pooling
- Head-of-line blocking (HTTP/1.1 vs HTTP/2)
- WebSocket — full duplex, when to use (real-time features)
- Server-Sent Events (SSE) — one-way, when to use
- Long polling — how it works, why WebSocket is usually better
- gRPC — HTTP/2 based, protobuf, bidirectional streaming
- REST vs gRPC vs GraphQL — decision framework

Network Performance:
- Latency vs Bandwidth vs Throughput
- TCP slow start and congestion control
- Network partitions — what happens when networks split
- CDN — how it reduces latency, anycast routing
- Load balancer networking — L4 (TCP level) vs L7 (HTTP level)

**Resources:**
| Resource | Link |
|----------|------|
| Computer Networking: A Top-Down Approach (Kurose & Ross) | Book (Chapters 1-3 is enough) |
| ByteByteGo — "HTTP/1 vs HTTP/2 vs HTTP/3" | YouTube |
| Hussein Nasser — Networking playlist | YouTube |
| Julia Evans — Networking Zines | https://jvns.ca |
| High Performance Browser Networking (FREE online) | https://hpbn.co |

**Deliverable:** Draw the complete network journey of an HTTPS request from browser to server, including DNS, TCP handshake, TLS handshake, HTTP request, load balancer, and response. Know every step.

---

### Week 3: Database Internals — Beyond SQL Queries

**Why this matters:** Oracle asked about LSM trees, B-trees, caching strategies. Apple asked about query optimization. Amazon asked about schema design. Every system design needs database decisions.

**Topics to master:**

Storage Engines:
- B-tree (read-optimized) — how pages split, why indexes use B-trees
- LSM tree (write-optimized) — memtable, WAL, SSTables, compaction
- When to choose B-tree vs LSM tree
- Row-oriented vs Column-oriented storage — OLTP vs OLAP

Indexing Deep Dive:
- Primary index vs Secondary index
- Composite index — column order matters (leftmost prefix rule)
- Covering index — when the index has all the data you need
- Hash index — O(1) lookup, no range queries
- Full-text index / Inverted index (Elasticsearch)
- Index anti-patterns: over-indexing, unused indexes, index bloat

Query Optimization:
- EXPLAIN / EXPLAIN ANALYZE — how to read query plans
- N+1 query problem — detection and solutions (JOIN, batch loading)
- Slow query identification and optimization
- Connection pooling (HikariCP, PgBouncer)
- Query caching vs Result caching

Transactions Deep Dive:
- ACID properties — what each really means
- Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable
- MVCC (Multi-Version Concurrency Control) — how PostgreSQL handles concurrent reads/writes
- Optimistic vs Pessimistic locking
- Distributed transactions: 2PC (Two-Phase Commit), SAGA pattern

Advanced SQL (Interview Must-Knows):
- Window functions: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD(), NTILE()
- CTEs (Common Table Expressions) — recursive CTEs
- Self-joins
- Pivoting data
- Handling NULL properly

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapters 2, 3, 7 | Book |
| Use The Index, Luke (FREE online) | https://use-the-index-luke.com |
| Mode SQL Tutorial (intermediate-advanced) | https://mode.com/sql-tutorial |
| StrataScratch — SQL by company | https://www.stratascratch.com |
| LeetCode Database problems | https://leetcode.com/problemset/database/ |
| Hussein Nasser — "B-tree vs LSM tree" | YouTube |

**Deliverable:** Solve 20 Medium/Hard SQL problems on LeetCode. Be able to explain B-tree vs LSM tree internals with diagrams.

---

### Week 4: DSA — The Patterns That Actually Appear in Interviews

**Why this matters:** Every company in your interview data had DSA rounds. But you don't need 500 problems — you need pattern recognition.

**The 12 patterns that cover 90% of interview problems:**

| # | Pattern | Key Problems | When to Use |
|---|---------|-------------|-------------|
| 1 | Two Pointers | Container With Most Water, 3Sum, Trapping Rain Water | Sorted array, find pair, squeeze from both ends |
| 2 | Sliding Window | Longest Substring Without Repeating, Min Window Substring | Contiguous subarray/substring, fixed or variable window |
| 3 | Binary Search | Search Rotated Array, Koko Eating Bananas, Oracle circle segments | Sorted data, binary search on answer |
| 4 | BFS/DFS on Graphs | Rotten Oranges, DashMart grid, File system path (Amazon) | Grid traversal, shortest path, multi-source BFS |
| 5 | Tree DFS | Max Path Sum, Diameter, LCA | Tree traversal, path problems |
| 6 | Stack | Evaluate RPN, Daily Temperatures, Valid Parentheses | Nested structures, next greater element, evaluation |
| 7 | Heap / Priority Queue | Top K elements, Merge K Sorted Lists, Meeting Rooms II | Top/bottom K, scheduling, merging sorted data |
| 8 | HashMap / Set | Two Sum, Group Anagrams, LRU Cache | Fast lookup, grouping, counting |
| 9 | Dynamic Programming | Longest Common Subsequence, Coin Change, Edit Distance | Optimal substructure + overlapping subproblems |
| 10 | Greedy | Task Scheduler, Jump Game, Interval Scheduling | Local optimal leads to global optimal |
| 11 | Linked List | LRU Cache, Reverse, Merge | In-place modification, pointer manipulation |
| 12 | Trie | Longest Common Prefix, Autocomplete, Word Search II | Prefix-based problems |

**Strategy:** Solve 3-4 problems per pattern. Total: ~40-50 problems. That is enough if you deeply understand each pattern.

**Resources:**
| Resource | Link |
|----------|------|
| NeetCode 150 (pattern-organized) | https://neetcode.io/practice |
| NeetCode YouTube (video solutions) | https://youtube.com/@NeetCode |
| Blind 75 | https://leetcode.com/discuss/general-discussion/460599 |
| LeetCode Patterns | https://seanprashad.com/leetcode-patterns/ |
| Striver's A2Z DSA Sheet | https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2 |

**Daily:** Solve 2 problems per day throughout all 6 months. Never stop. This is your ongoing practice, not a one-time thing.

---

## MONTH 2: JAVA DEEP DIVE — INTERNALS, CONCURRENCY, PERFORMANCE
### Theme: Know Java the way the JVM knows it

This is what separates a "Java developer" from a "Java engineer." Apple tested this heavily in Round 2. Oracle tests it. Senior roles everywhere test it.

---

### Week 5: JVM Architecture & Memory Model

**Topics:**

JVM Architecture:
- Class Loader subsystem — Loading, Linking (Verify, Prepare, Resolve), Initialization
- Bootstrap, Extension, Application class loaders
- Runtime Data Areas: Method Area, Heap, Stack, PC Register, Native Method Stack
- Which areas are shared across threads vs per-thread
- Execution Engine: Interpreter, JIT Compiler, HotSpot optimization

Java Memory Model (JMM):
- Heap: Young Generation (Eden, Survivor S0, S1), Old Generation, Metaspace
- Stack: frames, local variables, operand stack
- String Pool — where it lives, intern()
- How object creation works: new keyword → memory allocation → constructor → reference
- Object header: mark word, klass pointer
- Escape Analysis — when JVM puts objects on stack instead of heap

Memory Issues:
- Memory leak in Java — common causes (static collections, listeners not removed, ThreadLocal not cleaned, unclosed resources)
- OutOfMemoryError types: heap, metaspace, stack, GC overhead
- How to detect: heap dump analysis (Eclipse MAT, VisualVM)
- Soft Reference, Weak Reference, Phantom Reference — when to use each

**Resources:**
| Resource | Link |
|----------|------|
| Java Concurrency in Practice — Brian Goetz | Book (Chapters 1-5, 16) |
| JVM Internals Medium article by Dalibor Plavcic | Medium |
| Baeldung — JVM Memory Model | https://www.baeldung.com |
| VisualVM (practice using it) | https://visualvm.github.io |
| Java Performance — Scott Oaks | Book |

**Deliverable:** Draw the complete JVM architecture from memory. Explain what happens when you type `new Object()` at every level.

---

### Week 6: Concurrency & Multithreading (Apple's Favorite Topic)

**Topics:**

Core Concurrency:
- Thread creation: Thread class, Runnable, Callable + Future
- synchronized keyword — method level, block level, class level
- volatile keyword — visibility guarantee, happens-before
- wait(), notify(), notifyAll() — and why you should use higher-level alternatives
- Thread states: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED

Locks & Advanced Synchronization:
- ReentrantLock — tryLock, fairness, interruptible locking
- ReadWriteLock — when reads >> writes
- StampedLock (Java 8+) — optimistic reads
- Double-checked locking — why naive singleton breaks, how to fix with volatile (Apple asked this!)
- Lock-free programming: AtomicInteger, AtomicReference, CAS (Compare-And-Swap)
- java.util.concurrent: ConcurrentHashMap, CopyOnWriteArrayList, BlockingQueue

Thread Pools & Async:
- ExecutorService, ThreadPoolExecutor — core pool, max pool, queue, rejection policies
- CompletableFuture — thenApply, thenCompose, thenCombine, exceptionally
- Fork/Join Framework
- Virtual Threads (Java 21+ Project Loom) — what they change, when to use

Concurrency Problems:
- Deadlock — write code that creates one, then fix it
- Race condition — write code that demonstrates one, then fix with synchronized/lock
- Livelock, Starvation, Priority Inversion
- Producer-Consumer with BlockingQueue
- Thread-safe Singleton — all 5 ways (eager, lazy unsafe, synchronized, double-checked, enum, holder class)

**Hands-on exercises (actually code these):**
1. Implement a thread-safe LRU Cache
2. Implement Producer-Consumer with BlockingQueue
3. Implement a custom Thread Pool
4. Create a deadlock, detect it with jstack, fix it
5. Implement the Double-Checked Locking Singleton (the Apple question)

**Resources:**
| Resource | Link |
|----------|------|
| Java Concurrency in Practice — Brian Goetz | Book (THE reference) |
| Baeldung — Concurrency tutorials | https://www.baeldung.com/java-concurrency |
| Jakob Jenkov — Concurrency tutorial | https://jenkov.com/tutorials/java-concurrency/ |
| Defog Tech YouTube — Java concurrency | YouTube |

---

### Week 7: Garbage Collection & Performance Tuning

**Topics:**

Garbage Collection (GC) Deep Dive:
- GC roots and reachability analysis
- Young GC (Minor GC) vs Full GC (Major GC)
- Garbage collectors:
  - Serial GC — single-threaded, small heaps
  - Parallel GC — multi-threaded, throughput-focused
  - CMS (Concurrent Mark Sweep) — low pause, deprecated
  - G1GC — default since Java 9, region-based, predictable pauses
  - ZGC — sub-millisecond pauses, scalable to terabytes
  - Shenandoah — similar to ZGC, Red Hat
- GC tuning parameters: -Xmx, -Xms, -XX:+UseG1GC, -XX:MaxGCPauseMillis, -XX:NewRatio
- How to read GC logs — enable with -Xlog:gc or -verbose:gc
- GC pauses and stop-the-world events

Performance Monitoring & Profiling:
- Key metrics every backend engineer must know:
  - Throughput (requests/second)
  - Latency: p50, p95, p99 (and why p99 matters more than average)
  - Error rate
  - CPU usage, Memory usage, GC pauses
  - Thread count, connection pool utilization
- Monitoring stack: Prometheus (metrics) + Grafana (visualization)
- Application-level: Micrometer (Spring Boot), JMX MBeans
- Profiling tools: VisualVM, JProfiler, async-profiler, JFR (Java Flight Recorder)
- Thread dump analysis: jstack, how to identify deadlocks and thread contention
- Heap dump analysis: Eclipse MAT, jmap

Performance Optimization Playbook (Apple Round 2):
- Step 1: Measure — establish baseline with metrics
- Step 2: Identify bottleneck — is it CPU, memory, I/O, network, database?
- Step 3: Common fixes:
  - DB query slow? → Check EXPLAIN, add index, fix N+1
  - High GC pauses? → Tune heap, check for memory leak, use G1/ZGC
  - Thread contention? → Thread dump, reduce synchronized scope, use concurrent collections
  - Connection exhaustion? → Tune HikariCP pool size, add timeouts
  - Slow external API? → Add timeout, circuit breaker, cache response
  - High latency? → Add caching layer, use async processing
- Step 4: Validate — load test with JMeter/Gatling, compare metrics

**Hands-on exercises:**
1. Set up VisualVM, connect to a running Java app, take a heap dump, analyze it
2. Enable GC logging on a Java app, generate load, read the GC logs
3. Take a thread dump with jstack, identify a blocked thread
4. Use JMeter to load test a Spring Boot API, measure p95 latency
5. Tune a HikariCP connection pool — experiment with different sizes

**Resources:**
| Resource | Link |
|----------|------|
| Java Performance — Scott Oaks | Book |
| Baeldung — GC tuning | https://www.baeldung.com |
| JFR + JMC documentation (Oracle) | Oracle docs |
| Brendan Gregg's performance tools | https://www.brendangregg.com |

---

### Week 8: Spring Boot Deep Dive + Design Patterns in Practice

**Spring Boot (what interviews actually ask):**

Bean Management (Apple Round 1):
- Bean lifecycle: instantiation → populate properties → setBeanName → setBeanFactory → pre-init → afterPropertiesSet → custom init → post-init → ready → pre-destroy → destroy
- Bean scopes: singleton (default), prototype, request, session
- @Bean annotation — can you have 2 beans of same type? Yes → use @Qualifier or @Primary
- @Autowired — constructor injection (preferred) vs setter vs field
- Circular dependencies — how to detect, how to fix (redesign, @Lazy, setter injection)

Transaction Management:
- @Transactional — how it works (Spring AOP proxy)
- Propagation: REQUIRED (default), REQUIRES_NEW, NESTED, SUPPORTS, MANDATORY, NEVER, NOT_SUPPORTED
- Isolation levels: READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE
- Common mistakes: @Transactional on private method (won't work), self-invocation (proxy bypass)

Error Handling:
- @ControllerAdvice + @ExceptionHandler — global exception handling
- Custom exception hierarchy: BusinessException → OrderNotFoundException, PaymentFailedException
- Problem Details (RFC 7807) — standardized error response format

Observability:
- Spring Boot Actuator — health, metrics, info endpoints
- Micrometer — metrics facade, Prometheus integration
- Distributed tracing — Spring Cloud Sleuth / Micrometer Tracing
- Structured logging with correlation IDs

**Design Patterns (code these in Java):**

| Pattern | When to Use | Interview Context |
|---------|-------------|-------------------|
| Singleton | Single instance needed (Logger, Config, Connection Pool) | Apple asked specifically — know all 5 implementations |
| Factory | Object creation without exposing logic | PaymentProcessor: CreditCard, UPI, Wallet |
| Abstract Factory | Family of related objects | UI component families for different platforms |
| Builder | Complex object construction, many optional parameters | QueryBuilder, NotificationBuilder |
| Strategy | Interchangeable algorithms | Pricing strategies, Sorting algorithms, Payment methods |
| Observer | Event notification, pub-sub within app | Event listeners, notification system |
| Decorator | Add behavior dynamically | InputStream → BufferedInputStream → DataInputStream |
| Proxy | Control access, lazy loading, caching | Spring AOP, Hibernate lazy loading |
| Template Method | Define algorithm skeleton, let subclasses fill steps | ETL pipeline, report generation |
| Chain of Responsibility | Pass request through handler chain | Middleware, validation pipeline, filter chains |
| State | Object behavior changes based on state | Order states: Created → Confirmed → Shipped → Delivered |
| Command | Encapsulate request as object | Undo/redo, task queuing |

**Resources:**
| Resource | Link |
|----------|------|
| Effective Java 3rd ed — Joshua Bloch | Book |
| Head First Design Patterns | Book |
| Refactoring Guru — Design Patterns | https://refactoring.guru/design-patterns |
| Baeldung — Spring tutorials | https://www.baeldung.com |
| Java Brains YouTube | https://youtube.com/@Java.Brains |

---

## MONTH 3: CLEAN CODE, LLD, AND MACHINE CODING
### Theme: Write code that other engineers respect

This is where you prove you can build real software, not just solve algorithmic puzzles.

---

### Week 9: Clean Code — Principles and Practice

**Why this matters:** Clean code is what separates someone who "writes code" from someone who "engineers software." Interviewers can see it in your machine coding round within 5 minutes.

**Core Principles:**

Naming:
- Variables: describe WHAT it holds — `remainingRetries` not `r`, `userEmail` not `e`
- Methods: describe WHAT it does — `calculateTotalPrice()` not `calc()`, `isEligibleForDiscount()` not `check()`
- Classes: noun that describes the entity — `PaymentProcessor` not `PaymentHelper` or `PaymentUtils`
- Constants: ALL_CAPS — `MAX_RETRY_ATTEMPTS`, `DEFAULT_PAGE_SIZE`
- Boolean variables: `isActive`, `hasPermission`, `canProceed` — always read like English

Functions:
- Do ONE thing (Single Responsibility)
- Max 20-25 lines (if longer, extract)
- Max 3 parameters (if more, create a parameter object)
- No side effects — if named `getUser()`, it should not also update the user
- Command-Query Separation: either DO something or RETURN something, not both
- Early return / Guard clauses — avoid deep nesting

Classes:
- Small and focused — one reason to change
- High cohesion — everything in the class is related
- Low coupling — minimal dependencies on other classes
- Composition over Inheritance — prefer "has-a" over "is-a"
- Program to interfaces, not implementations

Error Handling:
- Use exceptions, not return codes
- Create specific exception classes — `InsufficientBalanceException` not generic `RuntimeException`
- Never catch and swallow (empty catch block)
- Fail fast — validate inputs at the boundary
- Use try-with-resources for closeable resources

**SOLID Principles (know these cold — they come up in every LLD round):**

| Principle | Meaning | Example |
|-----------|---------|---------|
| S — Single Responsibility | A class has ONE reason to change | `OrderService` handles orders, `EmailService` handles emails — not one class doing both |
| O — Open/Closed | Open for extension, closed for modification | Add new payment type by implementing `PaymentStrategy` interface, not modifying `PaymentProcessor` |
| L — Liskov Substitution | Subclass must be usable wherever parent is used | `Square extends Rectangle` breaks this — redesign needed |
| I — Interface Segregation | No client should depend on methods it does not use | Split `Animal` into `Flyable`, `Swimmable` instead of one fat interface |
| D — Dependency Inversion | High-level modules depend on abstractions, not concrete classes | `OrderService` depends on `NotificationSender` interface, not `EmailSender` directly |

**Resources:**
| Resource | Link |
|----------|------|
| Clean Code — Robert C. Martin | Book (Chapters 1-10) |
| Clean Architecture — Robert C. Martin | Book |
| Refactoring Guru — SOLID | https://refactoring.guru/design-patterns |
| Code Complete — Steve McConnell | Book (reference) |

**Deliverable:** Take any old code you have written. Refactor it applying these principles. The difference should be visible.

---

### Week 10-11: Low-Level Design (LLD) / Machine Coding Round Mastery

**What the interview expects:** You are given a problem (design a parking lot, design a vending machine). In 60-90 minutes, you must:
1. Gather requirements (5 min)
2. Identify entities/classes (5 min)
3. Define relationships and responsibilities (10 min)
4. Write clean, working code with SOLID principles and design patterns (40-50 min)
5. Explain tradeoffs (5-10 min)

**The LLD Framework:**

Step 1: Requirements
- Ask clarifying questions
- List functional requirements (what the system does)
- List non-functional requirements (extensibility, thread safety)

Step 2: Identify Core Entities
- Nouns in requirements → potential classes
- Example: "Parking Lot" → ParkingLot, Floor, ParkingSpot, Vehicle, Ticket, Payment

Step 3: Define Relationships
- IS-A (inheritance): Car IS-A Vehicle, Bike IS-A Vehicle
- HAS-A (composition): ParkingLot HAS-A list of Floors, Floor HAS-A list of ParkingSpots
- USES (dependency): ParkingService USES ParkingSpot, PaymentService

Step 4: Apply Design Patterns
- Strategy → for interchangeable algorithms (pricing, payment methods)
- Factory → for object creation (VehicleFactory, SpotFactory)
- Observer → for notifications (notify when spot available)
- State → for state machines (order status, ticket status)
- Singleton → for global managers (ParkingLotManager)

Step 5: Write Code
- Use interfaces/abstract classes for extensibility
- Apply SOLID principles
- Handle edge cases
- Add enums for fixed types (VehicleType, SpotType, PaymentMode)

**Must-Practice LLD Problems (these appear in interviews repeatedly):**

| # | Problem | Key Patterns | Companies |
|---|---------|-------------|-----------|
| 1 | Parking Lot | Strategy (pricing), Factory (vehicles), State (spot status) | Amazon, Flipkart, Uber |
| 2 | Elevator System | State (elevator states), Strategy (scheduling algorithm), Observer | Google, Microsoft, Flipkart |
| 3 | BookMyShow / Movie Ticket Booking | Observer (notifications), State (seat status), Concurrency (seat locking) | Flipkart, Swiggy, Paytm |
| 4 | Chess Game | State (game state), Strategy (piece movement), Factory (piece creation) | Amazon, Google |
| 5 | Vending Machine | State (idle, accepting, dispensing), Strategy (payment) | Oracle, Amazon |
| 6 | LRU Cache | HashMap + Doubly Linked List, Thread safety | Apple, Amazon, everyone |
| 7 | Snake and Ladder | State, Strategy, Board as graph | Flipkart, PhonePe |
| 8 | Library Management | CRUD + Domain modeling, Observer (due date notifications) | Common screening |
| 9 | Splitwise / Expense Sharing | Strategy (split types), Observer, Graph (debt simplification) | Google, Flipkart |
| 10 | Rate Limiter | Strategy (token bucket, sliding window), Thread safety | Amazon, DoorDash |
| 11 | In-Memory Key-Value Store | HashMap, TTL expiry, Thread safety | Oracle, Amazon |
| 12 | Task Scheduler | Priority Queue, Strategy, Thread Pool | Oracle, Apple |
| 13 | File System (in-memory) | Composite pattern, Tree structure | Amazon, Google |
| 14 | Logging Framework | Singleton, Observer, Strategy (log levels, outputs) | Common |
| 15 | Pub-Sub Messaging System | Observer, Thread safety, Queue management | Common |

**Resources:**
| Resource | Link |
|----------|------|
| workat.tech — Machine Coding | https://workat.tech/machine-coding |
| GitHub: ashishps1/awesome-low-level-design | https://github.com/ashishps1/awesome-low-level-design |
| GitHub: prasadgujar/low-level-design-primer | https://github.com/prasadgujar/low-level-design-primer |
| LLDCoding.com | https://www.lldcoding.com |
| codezym.com — LLD practice | https://codezym.com |
| Shreyansh Jain YouTube — LLD playlist | YouTube |
| Concept && Coding YouTube — LLD | YouTube |

**Practice schedule:** Code one complete LLD problem every 2 days. Time yourself to 75 minutes. Write clean, SOLID, pattern-applied code. After finishing, review: "Could I add a new payment method without changing existing code? Could I add a new vehicle type easily?"

---

### Week 12: Advanced Java Features & Modern Java

**Java 8-21 Features You Must Know:**

| Feature | Version | Why It Matters |
|---------|---------|---------------|
| Lambda Expressions | Java 8 | Functional programming, cleaner code, used everywhere in modern Java |
| Streams API | Java 8 | Data processing pipelines, map/filter/reduce, parallel streams |
| Optional | Java 8 | Null safety, cleaner API design |
| CompletableFuture | Java 8 | Async programming without callback hell |
| var (local type inference) | Java 10 | Cleaner code, less boilerplate |
| Records | Java 14 | Immutable data carriers, replace boilerplate POJOs |
| Sealed Classes | Java 17 | Restricted class hierarchies, pattern matching |
| Pattern Matching for instanceof | Java 16 | Cleaner type checks |
| Text Blocks | Java 13 | Multi-line strings, cleaner SQL/JSON |
| Virtual Threads (Project Loom) | Java 21 | Lightweight threads, massive concurrency without thread pool tuning |
| Structured Concurrency | Java 21+ | Managing groups of related tasks |

**Hands-on:** Refactor old-style Java code using modern features. Example: Convert a for-loop with null checks into a stream pipeline with Optional. Write an async pipeline with CompletableFuture.

---

## MONTH 4: GO AND PYTHON + POLYGLOT THINKING
### Theme: Expand your toolkit — understand WHY different languages exist

You don't need to become an expert in Go and Python. You need to understand what they are good at and be able to write production-quality code in them. This makes you a more versatile engineer.

---

### Week 13-14: Go (Golang) — The Systems Language

**Why Go:** Go is used heavily at companies like Google, Uber, DoorDash, Cloudflare, Docker, Kubernetes. It is the language of infrastructure, microservices, and CLI tools. Knowing Go signals "this person understands performance and systems."

**What to learn:**

Core Go:
- Goroutines and channels — Go's concurrency model (CSP: Communicating Sequential Processes)
- How goroutines differ from threads (lightweight, managed by Go runtime, not OS)
- select statement — multiplexing channels
- sync package: Mutex, WaitGroup, Once
- Error handling in Go — no exceptions, explicit error returns
- Interfaces — implicit (duck typing), composition over inheritance
- Structs and methods — Go's approach to OOP
- Defer, Panic, Recover — resource cleanup and error handling
- Pointers in Go — when to use, value vs pointer receivers

Go for Backend:
- net/http package — building APIs
- Gin or Echo framework — lightweight web frameworks
- Context package — cancellation, timeouts, request-scoped values
- Go modules — dependency management
- Testing in Go — table-driven tests, benchmarks
- Go's garbage collector — concurrent, low latency, different from JVM

**Project:** Build a simple URL shortener API in Go. This covers HTTP handling, database interaction, error handling, goroutines for async operations.

**Resources:**
| Resource | Link |
|----------|------|
| A Tour of Go (official interactive tutorial) | https://go.dev/tour |
| Go by Example | https://gobyexample.com |
| Let's Go by Alex Edwards | Book |
| Anthony GG YouTube — Go tutorials | YouTube |
| Effective Go (official) | https://go.dev/doc/effective_go |

---

### Week 15-16: Python — The AI/ML and Scripting Language

**Why Python:** Python is the language of AI/ML, data pipelines, automation, and scripting. Knowing Python means you can work with data scientists, build prototypes fast, and write automation tools. It is increasingly expected for backend roles at companies investing in AI.

**What to learn:**

Core Python (for a Java developer):
- Dynamic typing, duck typing — how it differs from Java
- List comprehensions, generators, decorators
- *args, **kwargs, unpacking
- Context managers (with statement) — resource management
- Type hints (Python 3.5+) — adding static typing feel
- Dataclasses — Python's equivalent of Java Records
- Asyncio — async/await for concurrent I/O

Python for Backend:
- FastAPI — modern, fast, type-safe web framework (recommended)
- SQLAlchemy — ORM, similar to JPA/Hibernate
- Pydantic — data validation and serialization
- Pytest — testing framework
- Virtual environments, pip, requirements.txt

Python for AI-Augmented Engineering:
- LangChain basics — building LLM-powered tools
- OpenAI / Anthropic API — how to call LLMs programmatically
- Prompt engineering basics
- Building a simple RAG (Retrieval Augmented Generation) pipeline

**Project:** Build a CLI tool that takes a system design question and uses an LLM API to generate a structured design outline. This covers Python, API integration, and AI-augmented thinking.

**Resources:**
| Resource | Link |
|----------|------|
| Python Official Tutorial | https://docs.python.org/3/tutorial/ |
| FastAPI Documentation | https://fastapi.tiangolo.com |
| Automate the Boring Stuff (FREE online) | https://automatetheboringstuff.com |
| Corey Schafer YouTube — Python | YouTube |
| LangChain Documentation | https://docs.langchain.com |

---

## MONTH 5: AI-AUGMENTED ENGINEERING + COMMUNICATION + PROFILE BUILDING
### Theme: The skills that make you 10x more effective than raw coding alone

---

### Week 17-18: AI-Augmented Engineering — Your Force Multiplier

**The New Workflow:**
This is not about AI replacing you. This is about you + AI being 5x more productive than you alone.

**Tools to master:**

| Tool | What It Does | How to Use It |
|------|-------------|---------------|
| Claude Code / Cursor | AI-powered coding in the IDE | Code generation, refactoring, debugging, test writing |
| GitHub Copilot | Inline code suggestions | Accept/reject/modify suggestions, learn to prompt in comments |
| Claude / ChatGPT | Thinking partner | System design brainstorming, code review, learning concepts |
| v0.dev (Vercel) | UI generation from prompts | Rapid prototyping of frontend components |

**The AI-Augmented Engineering Mindset:**

1. Problem Definition (YOU do this — AI cannot):
   - What are we building? Why?
   - What are the constraints?
   - What are the success criteria?
   - What are the edge cases?

2. Architecture & Design Decisions (YOU do this — AI assists):
   - Which database? Which communication protocol?
   - How should services be structured?
   - What are the tradeoffs?
   - Use AI to brainstorm alternatives: "What are 3 different approaches to solve X?"

3. Implementation (AI does heavy lifting — YOU review):
   - Generate boilerplate and scaffolding
   - Write first drafts of functions
   - Generate unit tests
   - YOU review every line, understand it, test it, improve it

4. Quality Assurance (YOU drive — AI assists):
   - Ask AI to review your code: "What bugs or issues do you see?"
   - Ask AI to write edge case tests
   - YOU make the final call on what ships

**Practice exercises:**
1. Take a LeetCode problem. Solve it yourself first. Then ask Claude to solve it. Compare approaches. Learn from the differences.
2. Design a system on paper. Then describe it to Claude and ask "What did I miss? What would break at scale?"
3. Write a Spring Boot service. Ask Claude to review it for SOLID violations, performance issues, and security concerns.
4. Use Claude Code or Cursor to build a small project. Track how much you accept vs modify vs reject. The goal: you should be modifying 30-50% of AI-generated code.

---

### Week 19: Communication, Requirement Gathering, and Decision Making

**Why this matters:** The #1 reason experienced engineers fail interviews is not technical knowledge — it is communication. They know the answer but cannot explain it clearly.

**Requirement Gathering Framework (use in system design AND at work):**

Step 1: Understand the Problem
- "What problem are we solving?" — not "What should we build?"
- Who are the users? What are their pain points?
- What does success look like?

Step 2: Ask the Right Questions
- Functional: "Should users be able to ___?"
- Scale: "How many users? How many requests per second?"
- Constraints: "Any technology preferences? Budget constraints?"
- Priority: "If we can only build 3 features, which 3?"
- Edge cases: "What happens when ___?"

Step 3: Document Decisions
- Decision: "We chose PostgreSQL over MongoDB"
- Reason: "Because our data is highly relational and we need ACID transactions"
- Tradeoff: "We sacrifice the write performance of a document store, but gain data integrity"
- Alternative: "If we needed to store unstructured data, we would use MongoDB alongside PostgreSQL"

**How to explain technical decisions (STAR-like framework for tech):**

"We had [SITUATION]. We considered [OPTIONS]. We chose [DECISION] because [REASONING]. The tradeoff was [TRADEOFF]. The result was [OUTCOME]."

Example: "Our API had p99 latency of 800ms. We considered adding a Redis cache, denormalizing the database, or adding a read replica. We chose Redis cache because 80% of reads were for the same 20% of data, making caching high-impact with low complexity. The tradeoff was we needed to handle cache invalidation, which we solved with TTL + event-based invalidation from Kafka. Latency dropped to 120ms at p99."

**Practice:** For every system design you practice, record yourself explaining your decisions. Listen back. Are you clear? Do you explain WHY, not just WHAT?

---

### Week 20: Building a Profile That Attracts Recruiters

**GitHub Profile:**
- Pin 3-5 repositories that showcase different skills
- Minimum projects: one complex backend system (Java/Spring Boot), one Go project, one LLD implementation
- Each repo must have a clear README: what it is, how to run it, what technologies, what design decisions
- Write clean, well-organized code in these repos — recruiters look at code quality

**LinkedIn Optimization:**
- Headline: not just "Software Engineer" → "Backend Engineer | Java, Go, Distributed Systems | System Design"
- About section: tell your story, what you are passionate about, what you are building
- Experience: focus on IMPACT, not tasks. "Reduced API latency by 60% by implementing Redis caching layer" not "Worked on caching"
- Skills: endorse Java, System Design, Distributed Systems, Spring Boot, Go, Python
- Posts: share your learnings weekly — even short posts about "Today I learned how consistent hashing works" attract attention

**Blog / Writing:**
- Start a simple blog (Medium, Hashnode, or dev.to)
- Write about what you learn: "How I designed a Rate Limiter", "Understanding JVM Garbage Collection", "Comparing Redis vs Memcached"
- This does THREE things: solidifies your learning, builds your brand, gives recruiters content to find

**Networking:**
- Join Discord communities: NeetCode, CS Career Hub
- Engage on Blind (TeamBlind) — comment on discussions
- Connect with engineers at target companies on LinkedIn
- Attend virtual meetups on topics you care about

---

## MONTH 6: MOCK INTERVIEWS + INTEGRATION + REFINEMENT
### Theme: Put it all together under pressure

---

### Week 21-22: Integration Practice

By now you have all the knowledge. The challenge is combining it fluidly.

**Daily practice rotation:**

| Day | Activity | Duration |
|-----|---------|----------|
| Monday | 2 DSA problems (timed) + 1 LLD problem | 2.5 hours |
| Tuesday | 1 System Design (full 40-min session, out loud) | 1.5 hours |
| Wednesday | Java deep dive review (pick one topic, explain it from memory) | 1 hour |
| Thursday | 2 DSA problems + 1 Machine Coding problem | 2.5 hours |
| Friday | Mock interview (DSA or System Design with partner/platform) | 1.5 hours |
| Saturday | Full mock loop: 1 DSA + 1 System Design + 1 Behavioral | 3-4 hours |
| Sunday | Review weak areas, read engineering blogs, light study | 1-2 hours |

---

### Week 23-24: Mock Interviews and Final Polish

**Mock interview platforms:**
| Platform | Best For | Link |
|----------|----------|------|
| Pramp | Free peer mocks (DSA + System Design) | https://www.pramp.com |
| Interviewing.io | Mocks with real engineers, anonymous | https://interviewing.io |
| Exponent | System design mocks | https://www.tryexponent.com |
| HelloInterview | AI-powered system design practice | https://www.hellointerview.com |
| IGotAnOffer | Mocks with ex-FAANG | https://igotanoffer.com |

**Behavioral Prep (final 2 weeks):**

Prepare 8-10 STAR stories covering:
- A technical challenge you overcame (debugging, performance issue)
- A time you disagreed with someone and how you resolved it
- A time you took ownership beyond your role
- A failure and what you learned
- A time you worked under ambiguity
- A time you delivered under a tight deadline
- How you mentored someone or helped a teammate grow
- A project you are proud of — and WHY

**The night before any interview:**
- Do NOT study new material
- Review your top 3 system designs
- Review your top 5 STAR stories
- Review the 7-step system design framework
- Sleep 8 hours. Seriously.

---

## WHERE TO FIND REAL INTERVIEW EXPERIENCES (Expanded)

| Source | What You Get | Link |
|--------|-------------|------|
| **TeamBlind** | Round-by-round breakdowns, exact questions, comp data | https://www.teamblind.com |
| **LeetCode Discuss** | Company-tagged problems + interview reports | https://leetcode.com/discuss/interview-experience |
| **Glassdoor** | Interview structure, behavioral questions | https://www.glassdoor.com |
| **1point3acres** | Extremely detailed (Chinese + English) | https://www.1point3acres.com |
| **Reddit** | r/cscareerquestions, r/leetcode, r/experienceddevs | https://www.reddit.com |
| **Levels.fyi** | Compensation + interview experiences | https://www.levels.fyi |
| **interviewing.io Blog** | "A Senior Engineer's Guide to FAANG Interviews" (excellent) | https://interviewing.io/guides/hiring-process |
| **GitHub** | Search "[company] interview questions" repos | https://github.com |
| **YouTube** | NeetCode, Exponent, Clément Mihailescu mock interviews | YouTube |
| **Hacker News** | "Ask HN: Who is hiring?" monthly threads | https://news.ycombinator.com |

---

## COMPLETE BOOK LIST (Priority Order)

| # | Book | What It Gives You | When |
|---|------|------------------|------|
| 1 | Designing Data-Intensive Applications — Kleppmann | System design + distributed systems foundation | Month 1-2 |
| 2 | Java Concurrency in Practice — Goetz | Threading, concurrency, JMM | Month 2 |
| 3 | Clean Code — Robert C. Martin | Code quality, naming, functions, classes | Month 3 |
| 4 | Effective Java 3rd ed — Bloch | Java best practices, patterns, idioms | Month 2-3 |
| 5 | System Design Interview Vol 1 — Alex Xu | Structured designs with framework | Month 1-3 |
| 6 | System Design Interview Vol 2 — Alex Xu | Advanced designs | Month 4-5 |
| 7 | Head First Design Patterns | Design patterns with visual learning | Month 3 |
| 8 | Java Performance — Scott Oaks | JVM tuning, GC, profiling | Month 2 |
| 9 | Operating Systems: Three Easy Pieces (FREE) | OS fundamentals | Month 1 |
| 10 | Clean Architecture — Robert C. Martin | Architecture principles | Month 3-4 |

---

## THE DAILY ROUTINE

```
Morning (2 hours):
  → 2 DSA problems (pattern-based, timed)
  → OR 1 LLD/Machine Coding problem

Afternoon (1.5 hours):
  → Deep dive topic (Java internals / System Design / OS / DB)
  → Read 20-30 pages of current book

Evening (1 hour):
  → System Design practice (explain out loud)
  → OR SQL problems
  → OR Go/Python practice

Before Bed (30 minutes):
  → Review notes from today
  → Write 3 bullet points of what you learned
  → Prep STAR stories

Weekend (3-4 hours):
  → Full mock interview OR complete LLD problem
  → Review weak areas from the week
  → Write a blog post or LinkedIn update about what you learned
```

---

## PROGRESS TRACKER

| Month | Theme | You Can Now... |
|-------|-------|---------------|
| 1 | CS Fundamentals + DSA | Explain OS, networking, DB internals. Recognize DSA patterns. |
| 2 | Java Deep Dive | Discuss JVM internals, debug concurrency issues, tune GC, optimize performance |
| 3 | Clean Code + LLD | Write SOLID code, design classes, ace machine coding rounds |
| 4 | Go + Python + Polyglot | Build services in multiple languages, use AI tools effectively |
| 5 | AI Engineering + Communication + Profile | Gather requirements clearly, make decisions with reasoning, have a strong online presence |
| 6 | Mock Interviews + Integration | Perform under pressure, explain clearly, handle any interview format |

---

## FINAL TRUTH

The developers who thrive are not the ones who know the most. They are the ones who can:
1. Break down any problem into smaller pieces
2. Make decisions and explain WHY
3. Write code that other engineers can read and extend
4. Learn continuously without being told what to learn
5. Communicate their thinking clearly

You have 5 years of experience. You know HOW things work. This 6-month plan teaches you WHY they work, WHEN to use what, and HOW to communicate your decisions.

At the end of these 6 months, you will not just be "someone who can pass interviews." You will be an engineer who understands systems deeply, writes clean code, makes sound architectural decisions, and can clearly explain their reasoning.

That is the kind of developer that every company wants. That is the kind of developer that recruiters reach out to. That is the kind of developer you are becoming.

Start today. One concept. One problem. One page. That is enough for Day 1.
