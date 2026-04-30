# SDE-2 / SDE-3 Backend + System Design — Complete Skills Map
## What You Must Know, What You Already Know from GSTN, What's Missing

> **How to use this document:**
> - ✅ = You have direct GSTN experience. Talk confidently.
> - ⚠️ = Partial knowledge. Needs reinforcement.
> - ❌ = Gap. Must study before interviews.
>
> **Format for each topic:**
> Concept → What SDE-2 must know → What SDE-3 must know additionally →
> Your GSTN evidence → Interview Q&A → Common wrong answers to avoid

---

## MASTER SKILLS MAP — Overview

```
┌─────────────────────────────────────────────────────────────┐
│  BACKEND + SYSTEM DESIGN — SDE-2/SDE-3 Skills Tree          │
├─────────────────────────────────────────────────────────────┤
│  A. CONCURRENCY & THREAD SAFETY         (your GSTN: ✅✅✅) │
│  B. DATABASE INTERNALS                  (your GSTN: ✅✅⚠️) │
│  C. CACHING                             (your GSTN: ✅✅✅) │
│  D. DISTRIBUTED SYSTEMS FUNDAMENTALS   (your GSTN: ✅✅⚠️) │
│  E. SCALABILITY PATTERNS               (your GSTN: ✅✅⚠️) │
│  F. MESSAGE QUEUES / EVENT STREAMING   (your GSTN: ✅✅⚠️) │
│  G. API DESIGN                         (your GSTN: ✅✅⚠️) │
│  H. MICROSERVICES                      (your GSTN: ✅✅⚠️) │
│  I. JAVA INTERNALS                     (your GSTN: ✅⚠️❌) │
│  J. SPRING BOOT INTERNALS              (your GSTN: ✅✅⚠️) │
│  K. SECURITY                           (your GSTN: ✅⚠️❌) │
│  L. OBSERVABILITY                      (your GSTN: ⚠️❌❌) │
│  M. STORAGE SYSTEMS (NoSQL, HBase)     (your GSTN: ✅⚠️❌) │
│  N. NETWORKING FUNDAMENTALS            (your GSTN: ⚠️❌❌) │
│  O. DESIGN PATTERNS (LLD)              (your GSTN: ✅✅✅) │
│  P. HIGH-LEVEL DESIGN (HLD)            (your GSTN: ✅✅⚠️) │
│  Q. WHAT SDE-3 NEEDS BEYOND SDE-2      (gap section)       │
└─────────────────────────────────────────────────────────────┘
```

---

# SECTION A — CONCURRENCY & THREAD SAFETY ✅

## Why It's Asked
Concurrency bugs are silent, reproducible only under load, and catastrophic in production.
Interviewers test this to distinguish developers who write concurrent code from those who
understand WHY it works and what fails under race conditions.

---

## A1. Java Memory Model (JMM) — What You MUST Know

### The Problem
```java
// Thread 1                  // Thread 2
status = "ACTIVE";           if (status.equals("ACTIVE")) {
                                 process();  // might never see "ACTIVE"!
                             }
```
Without synchronization, Thread 2 may read a stale cached value from its CPU register —
even though Thread 1 wrote "ACTIVE" to main memory. This is a **visibility** problem.

### The Three Pillars of Concurrency Correctness
| Pillar | Problem it prevents | Solution |
|---|---|---|
| **Visibility** | Thread sees stale value from its cache | `volatile`, `synchronized`, `Atomic*` |
| **Atomicity** | Compound operation interrupted mid-way | `synchronized`, `Atomic*`, locks |
| **Ordering** | Compiler reorders instructions unexpectedly | `volatile`, `synchronized`, `happens-before` |

### `volatile` keyword — when to use / when not to
```java
// CORRECT use: flag that one thread writes, others read
private volatile boolean shutdownRequested = false;

void shutdown() { shutdownRequested = true; }
void run() { while (!shutdownRequested) { doWork(); } }

// WRONG use: volatile does NOT make compound operation atomic
private volatile int count = 0;
count++;  // NOT atomic! count++ = read + increment + write = 3 steps
// Use AtomicInteger.incrementAndGet() instead
```

**Rule:** `volatile` solves visibility. It does NOT solve atomicity.

### Your GSTN Connection ✅
`DbContextHolder.setDbType()` / `clearDbType()` uses `ThreadLocal` — a different form of
thread isolation. Not volatile, not synchronized — each thread has its OWN copy of the variable.
```java
// ThreadLocal: each thread has independent storage. Zero contention. Zero synchronization needed.
private static final ThreadLocal<DbType> contextHolder = new ThreadLocal<>();
public static void setDbType(DbType dbType) { contextHolder.set(dbType); }
public static DbType getDbType()            { return contextHolder.get(); }
public static void clearDbType()            { contextHolder.remove(); } // CRITICAL: leak prevention
```

**Interview Q:** Why not use a static HashMap instead of ThreadLocal?
> "A static HashMap shared across threads requires synchronization on every read/write —
> contention bottleneck. ThreadLocal gives each thread its own storage — concurrent reads
> without any locking. The trade-off: each thread must explicitly clean up via `remove()`,
> or thread pool reuse leaks the previous request's value to the next request."

---

## A2. Locks and Synchronization

### `synchronized` — How It Works
```java
// Method-level lock: locks on 'this' object
public synchronized void assignCase(String caseId) { ... }

// Block-level lock: finer granularity
public void assignCase(String caseId) {
    synchronized (this.caseAssignLock) {  // lock on specific object
        ...
    }
}
```
`synchronized` provides both visibility AND atomicity. But it is **blocking** — a thread
waiting for the lock does nothing. For high-contention scenarios, use `ReentrantLock`.

### `ReentrantLock` vs `synchronized`
| Feature | `synchronized` | `ReentrantLock` |
|---|---|---|
| Interruptible wait | ❌ | ✅ `lockInterruptibly()` |
| Timeout on acquire | ❌ | ✅ `tryLock(timeout)` |
| Fair ordering | ❌ | ✅ `new ReentrantLock(true)` |
| Multiple conditions | ❌ (one wait set) | ✅ `newCondition()` |
| Explicit unlock needed | ❌ (auto on exit) | ✅ must `unlock()` in finally |

### Your GSTN Connection ✅
You used **two-layer locking**: Redis `SETNX` (distributed) + JPA `@Version` (optimistic).
```
Layer 1 (Redis SETNX):  Prevents parallel entry to the critical section across JVM instances
Layer 2 (@Version):     Database-level conflict detection if Redis lock fails (defense in depth)
```

### Optimistic vs Pessimistic Locking
```
Optimistic: "Assume no conflict. Detect and retry if conflict happens."
  → @Version field: read version=5, write with WHERE version=5
  → If another writer incremented to 6, your update finds 0 rows → retry
  → Best for: low-conflict scenarios (most cases)

Pessimistic: "Assume conflict. Lock first, then write."
  → SELECT FOR UPDATE: DB row is locked for your transaction
  → Other writers block until you commit/rollback
  → Best for: high-conflict scenarios (account balance updates)
```

**Interview Q:** When would you choose pessimistic over optimistic?
> "Pessimistic when: (1) retry is expensive (order issuance takes 500ms — retrying wastes 500ms
> of work), (2) conflict rate is high (hundreds of concurrent writes to same row),
> (3) you need guaranteed forward progress without retries (financial debit — must succeed
> exactly once). Optimistic when: (1) reads >> writes, (2) conflicts are rare, (3) retry cost is low."

---

## A3. Java Concurrent Collections

### Must Know
```java
ConcurrentHashMap<K,V>       // Thread-safe HashMap. No full-table lock. Segment/bucket locking.
CopyOnWriteArrayList<E>      // Thread-safe List. Writes copy the array. Fast reads, slow writes.
BlockingQueue<E>              // Producer-consumer. ArrayBlockingQueue / LinkedBlockingQueue.
AtomicInteger / AtomicLong   // Lock-free atomic operations using CAS (Compare-And-Swap)
AtomicReference<V>           // Lock-free atomic reference update
```

### Your GSTN Connection ✅
`LocalCacheFwk` uses `ConcurrentHashMap` to store 100+ reference data types:
```java
// CacheUtil internally: ConcurrentHashMap populated at startup, read-only after
private static final ConcurrentHashMap<String, Map<?, ?>> referenceCache = new ConcurrentHashMap<>();
```
Multiple request threads read concurrently — zero lock contention because ConcurrentHashMap
allows concurrent reads on different segments.

### CAS (Compare-And-Swap) — How AtomicInteger works
```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();  // Atomic: read(0) → increment(1) → CAS(expected=0, new=1) → if 0==current, set to 1; else retry
```
CAS is implemented at CPU instruction level — a single atomic hardware operation.
No thread blocking. Used in `AtomicInteger`, `AtomicReference`, `LongAdder`.

---

## A4. Thread Pools — `ExecutorService`

### Why Thread Pools
Creating a new `Thread` per task costs ~1ms and memory for stack.
At 1000 requests/second, that's 1000 new threads — JVM crash.
Thread pools reuse a fixed set of threads.

```java
// Fixed pool: predictable resource usage
ExecutorService pool = Executors.newFixedThreadPool(10);

// Cached pool: grows/shrinks. Risk: unbounded growth under load
ExecutorService pool = Executors.newCachedThreadPool();

// Scheduled: for periodic tasks (like cache refresh)
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.scheduleAtFixedRate(this::refreshCache, 0, 5, TimeUnit.MINUTES);

// The right way in production:
ExecutorService pool = new ThreadPoolExecutor(
    10,           // corePoolSize
    50,           // maximumPoolSize
    60L,          // keepAliveTime
    TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(1000),  // work queue with BOUNDED capacity
    new ThreadPoolExecutor.CallerRunsPolicy()  // backpressure: caller runs if queue full
);
```

**Why bounded queue?** Unbounded queue → memory exhaustion under load. Bounded queue with
`CallerRunsPolicy` → backpressure: slows down the producer (caller runs the task itself).

### Your GSTN Connection ✅
Spring Boot's `@Async` and Kafka consumer threads use `ThreadPoolTaskExecutor` under the hood.
The Kafka consumer group you used spawns one thread per partition.

---

## A5. CompletableFuture (Async Programming)

```java
// Chain async operations — runs in ForkJoinPool.commonPool() by default
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> fetchCaseFromDb(caseId))        // async: DB call
    .thenApply(caseData -> enrichWithOfficerName(caseData))  // transform
    .thenCompose(caseData -> fetchLedgerBalance(caseId))     // flat-map (another async)
    .exceptionally(ex -> handleError(ex));             // error handling

// Combine two independent futures
CompletableFuture<CaseDetails> caseF = fetchCaseAsync(caseId);
CompletableFuture<List<Task>> tasksF = fetchTasksAsync(caseId);
CompletableFuture.allOf(caseF, tasksF).thenRun(() -> {
    CaseDetails c = caseF.join();
    List<Task> t = tasksF.join();
    buildResponse(c, t);
});
```

**Interview Q:** What is the difference between `thenApply` vs `thenCompose`?
> "`thenApply` transforms the result synchronously — like `map` on a stream.
> `thenCompose` is for when your transformation itself returns a `CompletableFuture` —
> like `flatMap`. If you used `thenApply` with a function returning `CompletableFuture`,
> you'd get `CompletableFuture<CompletableFuture<T>>` — nested futures. `thenCompose` flattens it."

---

## A6. Deadlock — Recognition and Prevention

### Four Conditions for Deadlock (Coffman's conditions)
1. **Mutual exclusion** — resource held exclusively
2. **Hold and wait** — holding one lock while waiting for another
3. **No preemption** — lock can't be taken away
4. **Circular wait** — Thread A waits for B, B waits for A

### Prevention Strategy
```java
// DEADLOCK RISK: A acquires lock1 then lock2; B acquires lock2 then lock1
synchronized (lock1) { synchronized (lock2) { ... } }  // Thread A
synchronized (lock2) { synchronized (lock1) { ... } }  // Thread B

// SOLUTION: Always acquire locks in the same order
// Both threads: lock1 THEN lock2 — no circular wait possible
synchronized (lock1) { synchronized (lock2) { ... } }
synchronized (lock1) { synchronized (lock2) { ... } }
```

**Your GSTN context:** XA distributed transactions can cause distributed deadlock —
Transaction A locks case DB row and waits for ledger DB row;
Transaction B locks ledger DB row and waits for case DB row.
**Solution:** Always acquire locks in the same cross-DB order (case → ledger → workflow).

---

# SECTION B — DATABASE INTERNALS ✅⚠️

## B1. Indexing — Deep Knowledge

### B-Tree Index (default in MySQL/PostgreSQL/Oracle)
```
Structure: balanced tree. Root → branch → leaf (leaf holds actual row pointer).
Height: log(N) — for 1M rows, ~3-4 levels.
Cost: O(log N) for point queries, O(log N + K) for range queries.

Good for:
  - Equality: WHERE status = 'ACTIVE'
  - Range: WHERE insert_date BETWEEN '2024-01-01' AND '2024-12-31'
  - Prefix: WHERE arn LIKE 'AB27%'
  - ORDER BY (avoids sort if index matches order)
  
Bad for:
  - Low-cardinality: WHERE gender = 'M' (half the rows — full scan is cheaper)
  - Functions: WHERE UPPER(arn) = 'AB27...' (function defeats index)
```

### Composite Index — Column Order Matters
```sql
-- Index on (STATE_CD, CASETYPE_CD, STATUS)
-- USES index:   WHERE state_cd='27' AND casetype_cd='APL01' AND status='ACTIVE'
-- USES index:   WHERE state_cd='27' AND casetype_cd='APL01'
-- USES index:   WHERE state_cd='27'
-- SKIPS index:  WHERE casetype_cd='APL01'          ← left-prefix rule: must start from left
-- SKIPS index:  WHERE status='ACTIVE'              ← same reason
```
**Rule:** Composite index is useful only when the WHERE clause includes the **leftmost prefix**.
Order columns from most-selective (highest cardinality) to least-selective.

### Covering Index ⚠️
```sql
-- Regular index on (STATE_CD): fetches row pointer → then reads actual row (extra I/O)
-- Covering index on (STATE_CD, STATUS, CASETYPE_CD): all needed columns IN the index
-- Query: SELECT STATUS, CASETYPE_CD FROM cases WHERE STATE_CD='27'
-- → Index-only scan: NEVER touches the actual table. Fastest possible.
```

### Your GSTN Connection ✅
Your query optimization contribution: adding indexes on `(STATE_CD, CASETYPE_CD, STATUS)` for
case list queries, and on `(TAX_OFFCL_ID, STATUS)` for officer workload queries.

---

## B2. Transactions and Isolation Levels

### ACID
| Property | What It Means | Your GSTN Example |
|---|---|---|
| **Atomicity** | All-or-nothing | XA 2PC: case + ledger + workflow all commit or all rollback |
| **Consistency** | DB moves from one valid state to another | Ledger balance invariant: ΣDR - ΣCR must be valid after every write |
| **Isolation** | Concurrent transactions don't see each other's intermediate state | `@Version` prevents dirty reads of in-progress order |
| **Durability** | Committed data survives crash | WAL (Write-Ahead Log) ensures committed entries survive power failure |

### Isolation Levels and What They Prevent ❌ (must study)
```
                    Dirty Read  Non-Repeatable Read  Phantom Read
READ UNCOMMITTED:      ✗              ✗                  ✗
READ COMMITTED:        ✅             ✗                  ✗
REPEATABLE READ:       ✅             ✅                 ✗     ← MySQL InnoDB default
SERIALIZABLE:          ✅             ✅                 ✅

Dirty Read:           Read data written by uncommitted transaction
Non-Repeatable Read:  Read same row twice, get different value (another transaction updated)
Phantom Read:         Read same range twice, get different rows (another transaction inserted)
```

**Interview Q:** What isolation level does your system use and why?
> "Oracle (which GSTN uses) defaults to READ COMMITTED — so we can read committed
> data from other transactions but not uncommitted dirty data. For the order issuance
> flow where we must ensure no other transaction has issued an order on the same case,
> we use `SELECT FOR UPDATE` (pessimistic lock) at READ COMMITTED isolation — this
> serializes access to that specific row without requiring SERIALIZABLE isolation
> for the entire transaction."

### Write Skew ❌ (SDE-3 topic)
```java
// Two doctors both check: "is there at least one doctor on call?"
// Both see: yes, one doctor (not them). Both conclude: safe to take the day off.
// Both go off call. Now: zero doctors on call. Hospital unsafe.
// Neither wrote conflicting data, but their combined effect is a consistency violation.
// This is WRITE SKEW — not prevented by REPEATABLE READ.
// Fix: SELECT FOR UPDATE on the "on-call count" row before deciding.
```
In your domain: two officers simultaneously check case count before bulk assignment.
Both see "30 cases unassigned." Both assign themselves 30 cases. 60 cases assigned to 2 officers,
but there were only 30. Fix: `SELECT COUNT(*) FOR UPDATE` before assignment.

---

## B3. Query Execution Plan ⚠️

```sql
EXPLAIN SELECT c.case_id, c.status, t.tax_offcl_id
FROM CASE_DETL c
JOIN CASE_ASSGN_DTL t ON c.case_id = t.case_id
WHERE c.state_cd = '27' AND c.status = 'ACTIVE';

-- Output columns to read:
-- type: 'ALL' = full scan (bad), 'ref' = index lookup (good), 'const' = single row (best)
-- key: which index is being used (NULL = no index — fix this)
-- rows: estimated rows examined (1M = red flag)
-- Extra: 'Using filesort' (sort not covered by index), 'Using temporary' (temp table created)
```

**Red flags in EXPLAIN:**
- `type = ALL` → full table scan → add index
- `key = NULL` → no index used → add index
- `Extra = Using filesort` → ORDER BY not covered by index → add index matching ORDER BY
- `rows = 5000000` → scanning 5M rows for a query returning 10 → severe missing index

---

## B4. Connection Pooling ⚠️

```
Why: Opening a DB connection costs 20-50ms (TCP + auth + session setup).
At 1000 req/sec, 1000 connections × 50ms = 50 seconds of connection overhead per second.

Pool: maintain N pre-opened connections. Each request borrows one, uses it, returns it.
HikariCP (what Spring Boot uses by default):
  - minimumIdle: connections kept alive when idle
  - maximumPoolSize: max concurrent connections (typically 10-20 per app instance)
  - connectionTimeout: how long to wait for a free connection (default: 30s)
  - maxLifetime: max connection age (prevents stale connections)
```

**Interview Q:** What happens when all pool connections are in use?
> "Requests queue up waiting for a free connection. Once the queue exceeds
> `connectionTimeout` (30 seconds by default in HikariCP), the caller receives
> a `SQLTimeoutException`. At the service level, we should set a shorter
> application-level timeout than the HikariCP timeout, so we can return a
> meaningful '503 Service Temporarily Unavailable' instead of a raw SQL exception."

**Your GSTN Context:** 28 shards × multiple app instances × HikariCP pool per datasource.
`AbstractRoutingDataSource` routes requests to the correct pool. Each shard has its own pool.

---

# SECTION C — CACHING ✅

## C1. Caching Strategies

```
Cache-Aside (Lazy Loading):    Read cache → miss → read DB → write cache → return
  Your GSTN: officer jurisdiction map in Redis

Write-Through:                  Write DB + write cache simultaneously
  Best for: data you always want in cache, low write frequency
  Risk: cache and DB are always in sync but every write is slower

Write-Behind (Write-Back):      Write cache immediately, write DB asynchronously
  Best for: high write frequency, slight durability risk acceptable
  Your GSTN analogy: if batch job processed ARNs in-memory and flushed to DB periodically

Read-Through:                   Cache sits in front of DB, handles miss automatically
  Difference from cache-aside: cache library (like Redis client) handles the miss logic,
  not your application code
```

## C2. Cache Eviction Policies

```
LRU (Least Recently Used):   Evict the item not accessed for the longest time
  Redis default, good for temporal locality (recent data more likely to be reused)

LFU (Least Frequently Used): Evict the item accessed fewest times
  Better when some items are permanently hot (case type master — always needed)

TTL (Time-To-Live):          Evict after N seconds regardless of access
  Your GSTN: Redis keys with TTL — officer maps expire every few hours

FIFO:                         Evict oldest inserted item
  Rarely useful in practice
```

## C3. Cache Consistency Problems ⚠️

```
Problem 1: Stale read
  Thread A writes new value to DB. Doesn't update cache.
  Thread B reads from cache — gets old value.
  Fix: invalidate cache on write, or set short TTL.

Problem 2: Cache stampede / Thundering herd
  1000 threads all miss the same key at the same time.
  All 1000 hit DB simultaneously.
  Fix: mutex lock on cache refresh (SETNX in Redis).

Problem 3: Hot key
  A single cache key receives 100,000 reads/second.
  Redis is single-threaded per slot — one key becomes a bottleneck.
  Fix: replicate hot key across multiple Redis instances with key suffix (_shard1, _shard2)
  and round-robin reads across replicas.

Problem 4: Cache penetration
  Someone queries a key that NEVER exists in DB (bad input / attack).
  Every request misses cache and hits DB (1000 req/sec, all cache miss).
  Fix: cache negative results too — store null/empty with short TTL.
  Or use Bloom Filter: a probabilistic data structure that says "definitely not in DB"
  without a DB query.
```

---

# SECTION D — DISTRIBUTED SYSTEMS FUNDAMENTALS ✅⚠️

## D1. CAP Theorem

```
C = Consistency:  Every read receives the most recent write (or an error)
A = Availability: Every request receives a response (not necessarily most recent)
P = Partition Tolerance: System continues operating despite network partition

Theorem: In presence of a network partition, you must choose C or A.

CA systems (no partition tolerance): single-node RDBMSs — consistent and available
  but can't survive network splits → not suitable for distributed systems

CP systems: choose consistency over availability during partition
  Example: ZooKeeper (leader election), Redis with WAIT, HBase
  "I'd rather return an error than a stale value"

AP systems: choose availability over consistency during partition
  Example: Cassandra, DynamoDB, eventual consistency DNS
  "I'd rather return a possibly stale value than an error"

YOUR GSTN CHOICE: CP for financial data (ledger must be consistent),
  AP acceptable for reference data (case type labels can be slightly stale).
```

## D2. Consistency Models

```
Linearizability (Strict Consistency):
  Operations appear to happen instantaneously at a single point in time.
  Every reader sees the most recent write, globally.
  Cost: high latency (requires consensus protocol)
  Your GSTN: ledger writes must be linearizable — no stale balance reads.

Sequential Consistency:
  All operations appear to happen in some global order, consistent across all nodes.
  Order preserved within each thread, but global order not real-time.

Causal Consistency:
  If A causes B (A happened before B), all nodes see A before B.
  Concurrent events may be seen in different orders.

Eventual Consistency:
  Given no new writes, all replicas eventually converge to the same value.
  No guarantee on HOW LONG "eventually" takes.
  Your GSTN: LocalCache reference data — eventually consistent (loaded at startup, refreshed daily).

READ-YOUR-WRITES:
  After a user writes, they always read their own write.
  (Doesn't apply globally — other users may not see it yet)
  Your GSTN: after submitting an appeal, the officer dashboard must show it. Route
  appeal-submitter's reads to primary DB for 1 minute.
```

## D3. Consensus and Leader Election ❌ (SDE-3 must know)

```
Raft Protocol (simplified):
  Problem: multiple nodes must agree on a single value (who is the leader? what is the next log entry?)
  
  Raft uses: Leader election + Log replication
  
  Leader election:
    - Nodes start as followers. If no heartbeat from leader in timeout, become candidate.
    - Candidate requests votes from all nodes. First to get majority becomes leader.
    - Leader sends heartbeats. Followers reset timeout.
  
  Log replication:
    - Client sends write to leader.
    - Leader appends to its log. Sends AppendEntries RPC to all followers.
    - Once majority acknowledges → leader commits → tells followers to commit.
  
  Safety: Only one leader at a time (split-brain prevention via term numbers).
  
Applications: etcd (Kubernetes), ZooKeeper (Kafka metadata), Consul
```

## D4. Two-Phase Commit (2PC) ✅ — Deep Knowledge

**You already know this from Atomikos/XA. Here is the exact protocol:**

```
Phase 1 — PREPARE:
  Coordinator → "Can you commit?" → Participant1, Participant2, Participant3
  Each participant: writes prepare record to WAL, acquires all needed locks, votes YES/NO
  If ANY participant votes NO → coordinator sends ROLLBACK to all (abort)

Phase 2 — COMMIT:
  Coordinator: writes commit decision to its OWN WAL (DURABLY)
  Coordinator → "COMMIT" → all participants
  Each participant: applies changes, releases locks, writes commit to WAL

Crash scenarios:
  Coordinator crashes BEFORE Phase 2 decision:
    → Participants wait (in-doubt state, holding locks)
    → On coordinator restart: reads WAL → if 'prepare' but no 'commit' → send ROLLBACK
  
  Coordinator crashes AFTER writing commit to WAL but BEFORE sending to participants:
    → On restart: reads WAL → sees 'commit' written → re-sends COMMIT to all participants
  
  Participant crashes during Phase 2:
    → On restart: reads WAL → sees 'prepared' → asks coordinator for decision
    → Coordinator (if alive) responds with commit or rollback

Problem: Coordinator SPOF during the window between Phase 1 and Phase 2.
  In-doubt participants hold locks. Cannot proceed unilaterally.
  Solution: Three-Phase Commit (3PC) or Saga pattern.
```

## D5. Saga Pattern ⚠️ (must know for SDE-3)

```
Problem: XA 2PC locks resources for too long. Coordinator SPOF.
Saga: break distributed transaction into sequence of local transactions.
  Each step has a compensating transaction (rollback action).

Choreography Saga (event-driven):
  OrderService → publishes OrderCreated event
  PaymentService → subscribes, charges payment → publishes PaymentCompleted event
  InventoryService → subscribes, reserves stock → publishes StockReserved event
  If payment fails: publishes PaymentFailed → OrderService cancels order

  Pros: loose coupling, no central coordinator
  Cons: harder to reason about, complex failure debugging

Orchestration Saga (centralized):
  SagaOrchestrator → tells each service what to do → tracks state
  If step N fails → calls compensating transactions for steps N-1, N-2, ...
  
  Pros: single source of truth for saga state, easier debugging
  Cons: orchestrator is stateful, coupling to orchestrator

YOUR GSTN: Order issuance saga (if refactored):
  Step 1: Validate case state → compensate: nothing (read-only)
  Step 2: Update case status to ORDER_PENDING → compensate: revert to ASSIGNED
  Step 3: Insert ledger entries → compensate: insert reversal entries
  Step 4: Create workflow task → compensate: delete task
  Step 5: Publish audit event → compensate: publish cancel event (Kafka)
```

---

# SECTION E — SCALABILITY PATTERNS ✅⚠️

## E1. Horizontal vs Vertical Scaling

```
Vertical Scaling (Scale Up):    Bigger machine. More CPU, RAM, faster disk.
  Limit: single machine has a ceiling. Single point of failure.
  Your GSTN: initial approach — single DB server per state.

Horizontal Scaling (Scale Out): More machines. Distribute load.
  Requirement: stateless services (session in Redis, not in JVM memory)
  Your GSTN: multiple LitigationAPI instances behind load balancer.
  Your GSTN: 28 DB shards = horizontal scaling of the data tier.
```

## E2. Database Sharding ✅

```
Sharding = partitioning data across multiple databases.

Range-based sharding: rows 1-1M on shard 1, 1M-2M on shard 2
  Risk: hot shards (if most writes go to recent range)

Hash-based sharding: shard = hash(key) % N
  Even distribution. But resharding when N changes requires moving all data.

Directory-based sharding: lookup table maps key → shard
  Most flexible. Extra lookup overhead.

YOUR GSTN: Range-based on state code (stateCd 01-10 → shard 1, 11-20 → shard 2, etc.)
  Why: natural administrative isolation. Queries never cross shards.
  Limitation: can't JOIN across state data. Resolved by: application-level aggregation.

Cross-shard query problem:
  "Give me all cases across India" → must query all 28 shards and aggregate.
  Solution: aggregate to a reporting DB (read replica that receives all shards via replication).
```

## E3. Read Replicas ⚠️

```
Setup: one primary (handles writes), N replicas (handle reads).
Reads distributed across replicas → primary handles only writes.
Replication: async (replica may be slightly behind) or sync (replica must confirm before primary commits — slower but consistent).

YOUR GSTN USAGE:
  Primary DB: all writes (case creation, order issuance, assignment)
  Read replica: case list queries, dashboard counts, audit log retrieval
  
  RISK: Read-your-writes inconsistency.
  Scenario: Officer submits order → order goes to primary.
             Officer immediately refreshes case list → reads from replica (may not have it yet).
  Fix: Route writes and immediate reads from the same user to primary for 1-2 seconds after write.
```

## E4. Load Balancing ⚠️

```
Round Robin:      Request 1 → Server A, Request 2 → Server B, Request 3 → Server C, ...
  Simple, good if servers are identical and requests take similar time.

Least Connections: Send to server with fewest active connections.
  Better when requests have variable processing time.
  
IP Hash:          hash(clientIP) % N → always same server for same client.
  Useful for sticky sessions (but your GSTN uses stateless APIs + Redis sessions, so not needed).

Weighted Round Robin: Server A gets 3x requests vs Server B (if A has 3x the capacity).

Layer 4 vs Layer 7:
  L4 (TCP load balancer): operates at transport layer. Faster, no HTTP awareness.
  L7 (HTTP load balancer): can route by URL path, headers, cookies. More intelligent.
  AWS ALB = L7, NLB = L4.
```

## E5. Rate Limiting ⚠️

```
Purpose: prevent API abuse, protect downstream services from overload.

Token Bucket algorithm:
  Bucket holds N tokens. Each request consumes 1 token.
  Tokens refill at rate R per second.
  If bucket empty → request rejected (429 Too Many Requests).
  Allows bursting: bucket fills up during idle → burst of N requests allowed.

Leaky Bucket algorithm:
  Requests enter a queue. Processed at constant rate.
  If queue full → request dropped.
  No bursting — strictly constant outflow.

Sliding Window:
  Count requests in the last 60 seconds (sliding, not fixed window).
  More accurate than fixed window (which can allow 2x rate at window boundary).

Implementation with Redis:
  INCR rate_limit:{userId}:{minute}  → increment counter for this minute
  EXPIRE rate_limit:{userId}:{minute} 60  → auto-delete after 60 seconds
  If count > limit → reject
```

---

# SECTION F — MESSAGE QUEUES / EVENT STREAMING ✅⚠️

## F1. Kafka Deep Knowledge

### Ordering Guarantees
```
Kafka guarantees ordering WITHIN a partition. Not across partitions.

Key-based partitioning:
  producer.send(topic, key=caseId, value=event)
  All events with the same key → same partition → same consumer → ordered processing.
  
  YOUR GSTN: audit events for the same case must be ordered.
  Partition key = caseId → all events for case-123 go to partition-5 → consumer sees them in order.
```

### Consumer Offset Management ✅
```
Each consumer tracks its position (offset) in each partition.
Offsets stored in Kafka itself (_consumer_offsets topic).

Auto-commit: dangerous — commits offset on a timer, not after processing.
  If consumer crashes between auto-commit and processing → message lost.

Manual commit (what KafkaConsumerFwk uses):
  consumer.commitSync() after successfully processing → exactly-at-least-once.
  If commit fails → message re-delivered on restart → consumer must be idempotent.
```

### Dead Letter Queue (DLQ) ✅
```
Some messages can never be processed (poison pill — malformed, dependency unavailable).
Retrying forever blocks the partition.

Pattern:
  consumer fails N times → publish to DLQ topic
  DLQ consumer: human review, alert, or special handling
  Main consumer continues with next message — no partition blocking.
```

### Exactly-Once Semantics ⚠️
```
At-most-once:   May lose messages. Never duplicate.
At-least-once:  Never loses. May duplicate. (Your GSTN uses this + idempotent consumers)
Exactly-once:   Neither lose nor duplicate. Requires:
  1. Idempotent producer (each message has sequence number, broker deduplicates)
  2. Kafka transactions (producer wraps multiple topic writes in transaction)
  3. Consumer reads only committed messages (isolation.level = read_committed)

Cost: overhead of transaction log. Only use when business requires true exactly-once.
```

---

# SECTION G — API DESIGN ✅⚠️

## G1. REST Principles

```
Stateless: each request contains all info server needs. No server-side session.
  Your GSTN: auth token in header, stateCd in payload — server reads both on every request.

Resource-oriented URLs:
  GOOD:  GET /cases/{caseId}
  GOOD:  POST /cases/{caseId}/orders
  BAD:   POST /createOrder?caseId=123
  BAD:   POST /getCaseDetails   ← verb in URL, not RESTful

HTTP methods:
  GET:    read, idempotent, cacheable
  POST:   create, not idempotent
  PUT:    full update (replace entire resource), idempotent
  PATCH:  partial update, not necessarily idempotent
  DELETE: delete, idempotent

Idempotent: calling the same operation N times has same effect as calling once.
  GET /cases/123 called 100 times → same result. Idempotent.
  POST /cases/123/orders called 100 times → 100 orders created. NOT idempotent.
  PUT /cases/123 called 100 times → same final state. Idempotent.
```

## G2. Idempotency Keys

```
Problem: POST is not idempotent. Network retry = duplicate order issuance.

Solution: Idempotency-Key header
  Client sends: POST /cases/123/orders with header Idempotency-Key: uuid-abc-123
  Server: check if uuid-abc-123 already processed.
  If yes: return cached response. If no: process and cache response.

Redis storage:
  SET idempotency:{uuid-abc-123} {responsePayload} EX 86400  (24 hours)
  Next request with same key: return stored response.

Your GSTN application:
  Order issuance should use idempotency key — if officer double-clicks "Issue Order",
  the second request is a no-op returning the first order's reference.
```

## G3. Versioning ⚠️

```
URL versioning:     /v1/cases/{id}  /v2/cases/{id}
Header versioning:  Accept: application/vnd.gstn.v2+json
Query param:        /cases/{id}?version=2

Your GSTN: /v0.1/recovery/updateLedgerEntries — URL versioning.

When to version:
  - Breaking change: removing a field, changing field type, changing response structure
  - Non-breaking: adding optional field (backward compatible — no version needed)
  
Backward compatible changes in JSON: add optional fields (old clients ignore unknowns)
Backward compatible changes in Protobuf: add new field with new tag number
```

## G4. API Gateway Pattern ⚠️

```
API Gateway sits in front of all microservices:
  - Authentication (verify token before hitting service)
  - Rate limiting
  - Request routing (path → microservice)
  - SSL termination
  - Request/response logging
  - Load balancing across service instances

Without gateway: each service must implement auth, rate limiting, logging separately.
With gateway: cross-cutting concerns in one place.

Your GSTN analogy: AdminFilter in BOLitigationAPI validates URL access before
  the request reaches business logic — same concept as gateway filtering but implemented
  per-service rather than centrally.
```

---

# SECTION H — MICROSERVICES ✅⚠️

## H1. Service Discovery ❌

```
Problem: Service B needs to call Service A. What is Service A's IP and port?
  In containerized environments, IP changes on every restart.

Client-side discovery:
  Service B queries a registry (Eureka, Consul) → gets Service A's current IPs
  → load balances among them client-side.

Server-side discovery:
  Service B sends request to load balancer → load balancer queries registry → forwards.
  
Spring Cloud Eureka:
  Every service registers on startup: POST /eureka/apps/{serviceName} with IP:port
  Heartbeat every 30s (deregistered if no heartbeat for 90s)
  Clients fetch registry and cache it locally (refresh every 30s)
```

## H2. Circuit Breaker ✅ (you know this from resilience4j mentions)

```
Problem: Service A calls Service B. Service B is slow/down.
  Service A's threads block waiting. Thread pool exhausted. Service A goes down too.
  Cascade failure.

Circuit Breaker states:
  CLOSED:   Normal operation. Requests pass through. Track failure rate.
  OPEN:     Failure rate exceeded threshold. Requests fail immediately (no waiting).
            Prevents cascade. Returns fallback response.
  HALF-OPEN: After timeout, allow 1 test request. If succeeds → CLOSED. If fails → OPEN.

Implementation with Resilience4j:
  @CircuitBreaker(name = "caseService", fallbackMethod = "getCaseFallback")
  public CaseDetail getCase(String caseId) { ... }
  
  public CaseDetail getCaseFallback(String caseId, Exception ex) {
      return CaseDetail.builder().caseId(caseId).status("UNAVAILABLE").build();
  }

Your GSTN context:
  BOLitigationWeb (frontend) → calls LitigationAPI (backend).
  If LitigationAPI is slow → BOLitigationWeb should circuit-break and show "Service temporarily
  unavailable" rather than hanging all requests.
```

## H3. Service Mesh ❌ (SDE-3 topic)

```
Sidecar proxy (Envoy) deployed alongside each service instance.
All inter-service traffic goes through the sidecar.
Sidecar handles: TLS, retries, circuit breaking, load balancing, metrics collection.
Service code is unaware of all of this — pure business logic.

Examples: Istio (uses Envoy sidecars), Linkerd
Control Plane: configures all sidecars centrally.

When to use: when you have 50+ microservices and need consistent resilience patterns
  without implementing them in every service.
```

## H4. Distributed Tracing ❌ (must know for SDE-2/3)

```
Problem: Request enters API Gateway → Service A → Service B → Service C.
  Which service is slow? Where did the error originate?
  Without tracing: check 3 separate log files, manually correlate.

Solution: propagate a Trace ID across all service calls.
  Service A creates Trace ID: abc-123 (or generates UUID)
  Passes in header: X-Trace-ID: abc-123
  Service B logs with abc-123, Service C logs with abc-123
  Aggregator (Zipkin, Jaeger) collects spans → renders as timeline

Spring Cloud Sleuth: auto-injects trace ID into all outgoing HTTP headers and logs.
OpenTelemetry: vendor-neutral standard for traces, metrics, and logs.

Span: a single operation within a trace (one DB query, one HTTP call)
  span.startTime, span.endTime, span.tags{caseId, stateCd}, span.status

Your GSTN gap: BOLitigationWeb → LitigationAPI calls probably don't propagate trace IDs.
  If implemented, you could find exactly which DB shard query is slow in production.
```

---

# SECTION I — JAVA INTERNALS ✅⚠️❌

## I1. JVM Memory Model ⚠️

```
Heap:
  Young Generation: Eden + S0 (Survivor 0) + S1 (Survivor 1)
    New objects allocated in Eden. Minor GC: Eden + occupied Survivor → empty Survivor.
    Objects surviving N minor GCs → promoted to Old Gen.
  Old Generation (Tenured): Long-lived objects. Major GC is expensive (stop-the-world).
  
Non-Heap:
  Metaspace (Java 8+): Class metadata, method bytecode. Grows dynamically.
  Code Cache: JIT-compiled native code.

GC Algorithms:
  G1GC (default Java 9+): divides heap into regions. Concurrent, low-pause.
    -XX:MaxGCPauseMillis=200 — target pause time
  ZGC / Shenandoah (Java 15+): sub-millisecond pauses. For latency-sensitive apps.
  ParallelGC: throughput-optimized (background batch processing).
```

**Your GSTN context:** LocalCacheFwk with 100+ data types loaded in JVM heap.
If heap is not sized correctly, these maps stay in Old Gen and trigger long major GCs.
Set `-Xmx` appropriately. Monitor with `jstat -gcutil <pid> 1000`.

## I2. Class Loading ❌

```
Bootstrap ClassLoader → loads core Java classes (java.lang.*)
Extension ClassLoader  → loads javax.* and extension jars
Application ClassLoader → loads your application classes

Parent Delegation: ClassLoader asks parent first. Parent handles if it can. 
  Prevents: your code from overriding java.lang.String (Bootstrap handles it first).

Spring's ClassLoader: for each web module, Spring creates a child ClassLoader.
  Allows hot reloading in dev. Beware: static fields in parent loader persist across reloads.
```

## I3. String Pool and Interning ⚠️

```java
String a = "hello";     // stored in String Pool (JVM method area)
String b = "hello";     // same reference as a (pool lookup)
a == b → true           // same object reference

String c = new String("hello");  // heap object, NOT in pool
a == c → false          // different objects
a.equals(c) → true      // same content

// Interning: move heap string to pool
String d = c.intern();
a == d → true           // d is now the pooled reference

// GSTN implication: case type codes like "APL01" appear in millions of objects.
// If stored as new String("APL01") each time → millions of heap objects.
// They're typically string literals or constants → automatically interned → single object.
```

---

# SECTION J — SPRING BOOT INTERNALS ✅⚠️

## J1. Auto-Configuration ✅

```
@SpringBootApplication = @Configuration + @EnableAutoConfiguration + @ComponentScan

Auto-configuration: spring.factories (or spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports)
  lists configuration classes. Each has @ConditionalOn* — only activates if conditions met.

Example: DataSourceAutoConfiguration
  @ConditionalOnClass(DataSource.class)  — activates only if DataSource class on classpath
  @ConditionalOnMissingBean(DataSource.class)  — activates only if no DataSource bean already defined

Your GSTN: springboot-starter-gstn custom starter — packages auto-configuration for GSTN
  common beans (DbContextHolder, DistCacheUtil, etc.) so every microservice gets them
  without manual configuration. Same pattern as Spring Boot itself.
```

## J2. Bean Lifecycle ⚠️

```
1. Bean instantiation (constructor)
2. Dependency injection (@Autowired, setter, constructor)
3. @PostConstruct — your initialization code (LocalCacheFwk loads 100+ master types here)
4. Bean is ready — handles requests
5. @PreDestroy — cleanup before shutdown (close connections, flush buffers)
6. Bean destroyed

BeanPostProcessor: intercept all beans before/after initialization. AOP proxy creation happens here.
  BoApiAuditAspect wraps controllers via BeanPostProcessor → CGLIB proxy.

Scope:
  @Singleton (default): one instance per ApplicationContext. Shared across all requests.
  @Prototype: new instance per request for the bean itself (NOT per HTTP request).
  @RequestScope: new instance per HTTP request.
  @SessionScope: new instance per HTTP session.
```

## J3. AOP Proxy Mechanism ✅

```
@Transactional and @BoApiAudit both work via Spring AOP proxy.

Two proxy mechanisms:
  JDK Dynamic Proxy: requires interface. Creates proxy implementing same interface.
    Used when bean implements an interface.
  CGLIB Proxy: subclasses the class. Used when no interface (or @Transactional on concrete class).
    Limitations: can't proxy final classes or final methods.

Proxy wraps target bean:
  Incoming call → proxy's around advice → actual method → proxy's around advice (after) → return

Self-invocation problem:
  class OrderService {
      @Transactional
      public void issueOrder() {
          this.validateOrder();  // ← calls validateOrder on 'this', NOT the proxy!
          // @Transactional on validateOrder is IGNORED here
      }
      @Transactional(propagation = REQUIRES_NEW)
      public void validateOrder() { ... }
  }
  Fix: inject OrderService into itself, call through the injected proxy reference.
```

## J4. Transaction Propagation ⚠️

```
REQUIRED (default):      Join existing transaction. Create new one if none exists.
REQUIRES_NEW:            Always create new transaction. Suspend current if one exists.
NESTED:                  Create nested transaction (savepoint). If nested rolls back, outer continues.
SUPPORTS:                Use transaction if one exists. Run without if none.
NOT_SUPPORTED:           Run without transaction, suspend existing.
NEVER:                   Throw if a transaction exists.
MANDATORY:               Throw if NO transaction exists.

YOUR GSTN examples:
  Order issuance service: @Transactional(REQUIRED) — joins the XA transaction.
  Audit log writing: @Transactional(REQUIRES_NEW) — separate transaction.
    Even if main transaction rolls back, audit log is committed.
    "Log that the attempt happened, even if it failed."
```

---

# SECTION K — SECURITY ✅⚠️❌

## K1. Authentication vs Authorization ✅

```
Authentication: Who are you? Verify identity.
  Your GSTN: 10+ auth strategies (AuthenticationFwk) — password, OTP, DSC, Aadhaar, RBA

Authorization: What can you do? Verify permission.
  Your GSTN: accessGrpId + accessMapId — RBAC at every API endpoint

JWT (JSON Web Token):
  Header.Payload.Signature
  Header: algorithm (HS256, RS256)
  Payload: claims (userId, roles, exp — expiry)
  Signature: HMAC(header + payload, secret) — verifies token not tampered

  Stateless: server doesn't store session. Verify signature only.
  Risk: can't revoke a JWT before expiry (no server-side state).
  Mitigation: short expiry (15 min) + refresh token (stored server-side, revocable).
```

## K2. OWASP Top 10 — Must Know ⚠️

```
1. Broken Access Control:     Officer A accesses Officer B's cases by guessing caseId.
   Fix: check ownership — is this officer authorized for this case's jurisdiction?

2. Cryptographic Failures:    Sensitive data in plaintext (GSTIN in URL, ARN in logs).
   Fix: TLS everywhere, no sensitive data in logs/URLs.

3. SQL Injection:              WHERE arn = '${input}'  → input = "' OR '1'='1"
   Fix: parameterized queries (PreparedStatement, HQL with :param bindings).
   Your GSTN: JPA/Hibernate uses parameterized queries by default — protected.

4. Insecure Design:            No rate limiting on OTP → brute force possible.
5. Security Misconfiguration:  Dev debug endpoints exposed in production (/actuator/heapdump).

6. Vulnerable Components:      Old Spring Boot with known CVE.
   Fix: dependency version management, regular security scans.

7. Authentication Failures:    Session fixation, weak tokens.
8. Software Integrity Failures: Malicious library in dependency chain.
9. Logging Failures:           Security events not logged, logs not monitored.
10. SSRF:                       Server makes request to attacker-controlled URL.
```

## K3. Rate-Based Authentication (RBA) ✅

```
RBA = Risk-Based Authentication.
Analyzes: IP, device fingerprint, location, login time, velocity (too many logins too fast).
Assigns risk score. High risk → require additional factor (OTP).

Your GSTN: AuthenticationFwk has RBA as one of 10+ auth strategies.
  Normal login from known device/IP → password only.
  Login from new device → password + OTP.
  Login from foreign IP → password + OTP + admin review.

Adaptive MFA: the level of authentication scales with the computed risk.
```

---

# SECTION L — OBSERVABILITY ❌ (Critical Gap)

## L1. The Three Pillars: Metrics, Logs, Traces

```
Metrics: numbers over time. CPU%, request rate, error rate, P99 latency.
  Tool: Prometheus (scrapes /actuator/prometheus endpoint) + Grafana (dashboards)
  Spring Boot Actuator auto-exposes metrics at /actuator/metrics

Logs: text records of events. Structured JSON preferred over plain text.
  Tool: ELK Stack (Elasticsearch + Logback + Kibana) or Splunk
  KEY: structured logs with correlation ID:
    {"timestamp":"...", "traceId":"abc-123", "caseId":"456", "level":"ERROR", "message":"..."}

Traces: end-to-end request journey across services.
  Tool: Jaeger, Zipkin, Tempo
  Spring Cloud Sleuth / OpenTelemetry auto-injects trace IDs
```

## L2. SRE Metrics — RED and USE ⚠️

```
RED (for services):
  Rate:     requests per second
  Errors:   error rate (errors / total requests)
  Duration: latency distribution (P50, P95, P99)

USE (for resources: CPU, memory, disk):
  Utilization:  % of time resource is busy
  Saturation:   queue depth / wait time
  Errors:       error count

Alerting on P99, not average:
  If 1% of users experience 10s latency but average is 200ms, average hides the problem.
  P99 = 99th percentile = worst case for 99% of users. Alert when P99 > SLA threshold.
```

## L3. Health Checks ⚠️

```
Liveness probe (Kubernetes): is the app alive? If fails → restart container.
  /actuator/health → { "status": "UP" }

Readiness probe (Kubernetes): is the app ready to serve traffic?
  If fails → remove from load balancer (no new traffic). Don't restart.
  Use case: startup (LocalCache loading) — app is alive but not ready.

Spring Boot Actuator:
  /actuator/health — aggregate health (DB connectivity, Redis, Kafka)
  /actuator/info — app version, git commit
  /actuator/metrics/http.server.requests — request count + latency

Your GSTN gap: if LocalCacheFwk @PostConstruct fails to load reference data,
  the app should report readiness=DOWN until data is loaded.
```

---

# SECTION M — STORAGE SYSTEMS ✅⚠️❌

## M1. HBase (Your GSTN: HbaseAccessFwk) ✅

```
HBase = distributed, column-oriented database on HDFS.
Data model: Table → Rows (row key) → Column Families → Columns → Versioned cells.

Row key design is CRITICAL:
  Hot spotting: if row keys are sequential (001, 002, 003...) → all writes go to same region.
  Fix: reverse the key (001 → 100) or prefix with hash.

Read/Write path:
  Write: → MemStore (in-memory) + WAL (disk, for crash recovery)
          → MemStore full → flush to HFile (on HDFS)
  Read: → check MemStore + BlockCache (in-memory) + HFiles (disk)
  
  Bloom Filter: each HFile has a Bloom filter. Quick check: "is this row key in this file?"
    If Bloom says NO → skip entire file. Reduces disk I/O for reads of non-existent rows.

Your GSTN: GSTFunction / GSTPredicate — functional API for HBase queries.
  GSTFunction<RowKey, HBaseRow>: maps row key to result (like a DB function with input validation).
  Composable: chainable predicate conditions on HBase scans.
```

## M2. Redis Data Structures ✅

```
String:      Simple K→V. GET/SET. Used for: session, distributed lock, counter.
Hash:        K → {field: value, ...}. Used for: officer details, case summary.
List:        K → [v1, v2, v3, ...]. LPUSH/RPOP. Used for: task queue, audit log per case.
Set:         K → {v1, v2, ...} (unordered, unique). Used for: set of ARNs assigned to officer.
Sorted Set:  K → {v1:score1, v2:score2}. ZADD/ZRANGE. Used for: leaderboard, priority queue.
Bitmap:      Bitfield operations. Used for: "has taxpayer filed this month?" (bitset by day).

Distributed Lock with Lua Script (atomic):
  SET lock_key request_id NX PX 30000
  -- NX = only if not exists (atomic test-and-set)
  -- PX 30000 = expire in 30 seconds
  
  Unlock (must check ownership, atomic via Lua):
  if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])  -- only delete if you own it
  else return 0 end
```

## M3. Relational vs NoSQL Choice ⚠️

```
Use RDBMS when:
  - ACID transactions required (ledger entries, order issuance)
  - Complex joins needed
  - Schema is well-defined and stable
  - Strong consistency required
  YOUR GSTN: case management, ledger, workflow → Oracle RDBMS

Use Document DB (MongoDB) when:
  - Schema varies per document (different appeal types have different fields)
  - No joins needed (embed related data)
  - Flexible schema evolution

Use Key-Value (Redis, DynamoDB) when:
  - Simple lookups by key
  - Millisecond latency required
  - Scale writes horizontally

Use Column-family (HBase, Cassandra) when:
  - Time-series data (audit logs with billions of rows)
  - Wide rows (one taxpayer with many filing periods as columns)
  - Write-heavy (HBase write path: MemStore → HFile)
  YOUR GSTN: HBase for taxpayer return filing data (billions of entries)

Use Graph DB (Neo4j) when:
  - Relationships between entities are the data (social graph, fraud detection)
  - Multi-hop traversal (find all connections within 3 hops)
```

---

# SECTION N — NETWORKING FUNDAMENTALS ❌

## N1. TCP vs UDP

```
TCP:
  - Connection-oriented (3-way handshake: SYN → SYN-ACK → ACK)
  - Reliable: guaranteed delivery, ordering, error detection
  - Flow control: prevents fast sender overwhelming slow receiver
  - Congestion control: reduces rate when network is congested
  - Use: HTTP, database connections, Kafka, Redis

UDP:
  - No connection. Fire-and-forget.
  - No ordering guarantee. No delivery guarantee.
  - Much lower latency (no handshake, no ack)
  - Use: DNS, video streaming, gaming, monitoring (metrics where loss is acceptable)
```

## N2. HTTP/2 vs HTTP/1.1 ⚠️

```
HTTP/1.1 problems:
  - One request per TCP connection at a time (head-of-line blocking)
  - Multiple connections per host to work around this (6-8 connections in browsers)
  - Headers are text, verbose, repeated on every request

HTTP/2 solutions:
  - Multiplexing: multiple requests on single TCP connection simultaneously
  - Header compression (HPACK)
  - Binary framing (not text)
  - Server push: server proactively sends resources client will need

gRPC uses HTTP/2: enables multiplexed RPC calls, streaming (server → client, bidirectional).
  Your GSTN internal API calls likely use REST (HTTP/1.1).
  gRPC is better for: high-throughput internal service calls, real-time streaming.
```

## N3. DNS Resolution ⚠️

```
Browser → OS cache → recursive resolver (ISP DNS) → root nameserver → TLD (.com) → authoritative NS
TTL determines how long each step caches the result.

For microservices:
  Service discovery (Eureka, Consul) replaces DNS for internal routing.
  But external-facing APIs use DNS + CDN (your GSTN static assets).

DNS-based load balancing: A record returns multiple IPs for same hostname.
  Simple round-robin. No health awareness. TTL = 60s means stale IP for up to 60s after server failure.
```

---

# SECTION O — DESIGN PATTERNS (LLD) ✅

## O1. Patterns You've Used — With Code

### Strategy + Factory (CaseCustomizer) ✅
Already documented in My_Contributions_Deep_Dive.md Section 5.

### Observer Pattern ✅
```java
// Kafka is the Observer pattern at scale:
// Subject (case creation service) publishes event.
// Observers (notification service, audit service, ledger service) subscribe independently.
// No direct coupling between subject and observers.

// In-JVM version: Spring ApplicationEvent
@Component
public class CaseCreatedEventPublisher {
    @Autowired ApplicationEventPublisher publisher;
    public void caseCreated(Case c) {
        publisher.publishEvent(new CaseCreatedEvent(this, c));
    }
}

@Component
public class AuditListener {
    @EventListener
    public void onCaseCreated(CaseCreatedEvent event) { /* audit */ }
}
```

### Template Method ✅
```java
// The case creation flow IS a template method:
public final void createCase(Case c) {       // final: fixed order
    Case prepared = customizer.beforeCreateCase(c);   // variable step
    caseDao.save(prepared);                            // fixed step
    customizer.afterCreateCase(prepared);             // variable step
    notifyWorkflow(prepared);                          // fixed step
}
```

### Decorator Pattern ⚠️
```java
// AOP is a runtime decorator:
// Original method: issueOrder() — pure business logic
// AOP adds: @Transactional, @BoApiAudit, @CircuitBreaker — without modifying the method.
// Stacked decorators, applied at runtime by the proxy.

// In-code example:
interface DocumentService { byte[] getDocument(String id); }

class CachedDocumentService implements DocumentService {
    private final DocumentService delegate;
    private final Cache cache;
    public byte[] getDocument(String id) {
        return cache.getOrLoad(id, () -> delegate.getDocument(id));  // decorates with caching
    }
}
```

### Builder Pattern ✅
```java
// Used in your GSTN VO construction:
CaseTask task = CaseTask.builder()
    .caseId(123).caseTypeCd("APL01").stateCd("27")
    .assignedTo("officer-456").dueDate(LocalDate.now().plusDays(30))
    .build();
// Avoids telescoping constructors. Immutable after build. Readable.
```

### Command Pattern ✅
```java
// Your 12-scenario rule engine IS the Command pattern:
interface SubsequentOrderRule {
    boolean matches(FirstOutcome f, SubsequentOutcome s);  // condition
    void execute(OrderContext ctx);                         // command
}
// Commands are objects. Can be stored, queued, logged, undone.
```

---

# SECTION P — HIGH-LEVEL DESIGN (HLD) ✅⚠️

## P1. The 8-Pillar HLD Framework

For any system design interview, address all 8:

```
1. Requirements Clarification
   Functional: what features?
   Non-functional: scale? latency? availability? consistency?

2. Capacity Estimation
   RPS (requests per second): DAU × requests/user/day ÷ 86400
   Storage: entities/day × size per entity × retention years
   Bandwidth: RPS × avg response size

3. API Design
   Core endpoints (GET/POST/PUT/DELETE)
   Request/response schemas

4. Data Model
   Entities, relationships, indexes
   SQL vs NoSQL choice and justification

5. High-Level Architecture
   Components: API layer, service layer, DB, cache, message queue, CDN
   Data flow diagram

6. Deep Dive on Critical Component
   The hardest part: concurrency, consistency, scale

7. Bottleneck Identification + Solutions
   Single points of failure, hot spots, latency bottlenecks

8. Trade-offs
   Every decision has a trade-off. State yours.
```

## P2. Estimation Cheat Sheet

```
Active users per day (DAU):    write this → derive RPS
Peak RPS = avg RPS × 3 (rule of thumb for peak/avg ratio)
1 million RPS = ~1000 API servers (if each handles 1000 RPS)

Storage:
  1 character = 1 byte
  1 UUID = 36 bytes
  1 int = 4 bytes
  1 long = 8 bytes
  1 case record ≈ 2KB JSON ≈ 500 bytes in DB (compressed)
  
  GSTN: 15.2M taxpayers × 1 appeal each × 2KB ≈ 30GB just for one case type.
  With 20 case types: ~600GB. Spread across 28 shards: ~21GB per shard — manageable.

Latency:
  L1 cache: 1ns
  L2 cache: 4ns
  RAM: 100ns
  SSD random read: 100μs
  HDD random read: 10ms
  Same datacenter network: 0.5ms
  Cross-AZ network: 1-2ms
  Cross-region network: 50-150ms
```

## P3. Design a System Like GSTN — Template Answer

```
"Design a high-scale government tax dispute management platform (15.2 million users, 28 jurisdictions,
~4.8 lakh first-appeal GSTAT backlog cases)"

Requirements:
  - Officers file appeals, view case status, issue orders
  - System handles 1000 concurrent users per state
  - Financial ledger must be consistent (no stale balance)
  - All actions audited

Architecture:
  [Tax Officers] → [CDN for static assets]
                 → [API Gateway (auth, rate limiting)] → [LitigationAPI cluster]
  [LitigationAPI cluster] → [AbstractRoutingDataSource] → [28 Oracle DB shards by stateCd]
                          → [Redis cluster (officer maps, distributed locks)]
                          → [Kafka cluster (audit events, notifications)]
                          → [HBase (filing data, historical records)]
  [Kafka] → [AuditConsumer] → [Audit DB]
          → [NotificationService] → [SMS/Email gateway]

Key design decisions + trade-offs:
  Sharding by stateCd: simple routing, no cross-shard joins, isolation.
    Trade-off: cross-state admin queries require full-scan or reporting replica.
  XA 2PC for order issuance: strict atomicity across 3 DBs.
    Trade-off: coordinator SPOF, lock duration. Alternative: Saga (lower consistency guarantee).
  Two-tier caching: JVM for reference data (0ms), Redis for shared state (1ms).
    Trade-off: JVM cache inconsistency across instances for mutable data.
  Kafka for audit: async, decoupled, replayable.
    Trade-off: dual-write risk (Outbox pattern needed for guaranteed delivery).
```

---

# SECTION Q — SDE-3 BEYOND SDE-2 ❌ (Study List)

## What SDE-3 Needs That SDE-2 Doesn't

```
TOPIC                           SDE-2 LEVEL                 SDE-3 LEVEL
─────────────────────────────────────────────────────────────────────────
Distributed transactions        Know XA 2PC + Saga          Design trade-offs per use case
                                                             Know when NOT to use distributed tx
                                                             
Consensus protocols             Know Raft exists             Explain Raft election + log replication
                                Know ZooKeeper/etcd          Understand split-brain prevention

Database replication            Know primary/replica         Know semi-sync vs async replication
                                                             Know replication lag impact on reads
                                                             Know GTID-based replication (MySQL)

Data modeling at scale          Design for current need      Design for 5-year growth
                                                             Partition key selection for NoSQL
                                                             Hot partition avoidance

Failure mode analysis           Know what can fail           Write failure scenario documents
                                                             Calculate MTTR/MTBF
                                                             Design for N+1 redundancy

Capacity planning               Rough estimates              Excel-level spreadsheet model
                                                             Bottleneck analysis per tier
                                                             Cost optimization (choose cheaper tier)

Code review leadership          Review own code              Set team standards
                                Review peer code             Catch subtle concurrency bugs in reviews
                                                             Reject designs with known failure modes

On-call and production ops      Know deployments exist       Own runbooks
                                                             Write post-mortems
                                                             Define SLOs/SLAs/error budgets

Technical debt management       Identify tech debt           Prioritize tech debt vs features
                                                             Cost/benefit analysis of refactoring

Mentoring                       N/A                          Explain complex concepts simply
                                                             Identify knowledge gaps in team
```

---

# PRIORITY STUDY LIST — What to Read This Week

## If You Have 1 Week:
```
Day 1: Concurrency (Section A) — volatile, synchronized, ThreadLocal, CAS
Day 2: Database (Section B) — isolation levels, explain plan, connection pool
Day 3: Distributed Systems (Section D) — CAP theorem, consistency models, Saga
Day 4: Observability (Section L) — metrics, traces, health checks, Prometheus
Day 5: Networking (Section N) + API Design (Section G) — TCP/HTTP2, idempotency, versioning
Day 6: Mock HLD design — "Design GSTN Litigation System" end-to-end
Day 7: Review all follow-up Q&As, practice speaking answers out loud
```

## If You Have 2 Days:
```
Day 1 (morning):  Concurrency — ThreadLocal, optimistic vs pessimistic, deadlock
Day 1 (afternoon): Isolation levels, N+1, explain plan
Day 2 (morning):  CAP theorem, Saga, circuit breaker, distributed tracing
Day 2 (afternoon): Mock HLD. Practice the 8-pillar framework out loud.
```

---

# CROSS-REFERENCE — Term Glossary (GSTN → Generic)

| GSTN Code | Generic Term | Section |
|---|---|---|
| `DbContextHolder.setDbType()` | ThreadLocal-based request context | A1 |
| `@Version` on entity | Optimistic concurrency control via version field | A2 |
| Redis `SETNX` + TTL | Distributed mutex with lease timeout | A2 |
| `ConcurrentHashMap` in LocalCache | Thread-safe in-process lookup table | A3 |
| XA / Atomikos 2-phase commit | Distributed transaction protocol | D4 |
| `AbstractRoutingDataSource` | Dynamic datasource routing pattern | E2 |
| `stateCd` sharding | Horizontal database partitioning by key | E2 |
| `CacheUtil.getRefDetails()` | In-process cache-aside read | C1 |
| `DistCacheUtil` | Distributed cache client | C1 |
| `KafkaConsumerFwk` manual ack | At-least-once Kafka delivery with manual offset commit | F1 |
| DLQ in KafkaConsumerFwk | Dead Letter Queue for poison-pill message handling | F1 |
| `@BoApiAudit` + `BoApiAuditAspect` | AOP-based cross-cutting concern (audit) | J3 |
| `@PostConstruct` in LocalCacheFwk | Application warm-up / eager initialization | J2 |
| `CaseCustomizerFactory` | Factory Method pattern for runtime type resolution | O1 |
| `CaseCustomizer` interface | Strategy pattern for algorithm variation | O1 |
| `WaiverScheme` + validation | State machine + business rule validation | G |
| `APL_CASE_ASSGN_HIST` | Immutable audit log (append-only history) | B |
| `UNASSIGNED_ARNS_DTLS.batchStatus` | Optimistic job locking (compare-and-swap) | E5 |
| DCR ledger entries | Double-entry bookkeeping / Event Sourcing | P |
| `accessGrpId` / `accessMapId` | RBAC — Role-Based Access Control | K1 |
| AuthenticationFwk 10+ strategies | Multi-factor adaptive authentication | K3 |
| `stateJuriCode` hierarchy | Hierarchical resource partitioning | E2 |
| `GSTFunction` / `GSTPredicate` | Functional API (composable predicate + function) | M1 |

---

*Last Updated: April 2026 — SDE-2/SDE-3 Backend + System Design Complete Skills Map*
*Sections: Concurrency (A), DB (B), Caching (C), Distributed (D), Scalability (E),*
*Kafka (F), API Design (G), Microservices (H), Java (I), Spring (J), Security (K),*
*Observability (L), Storage (M), Networking (N), LLD Patterns (O), HLD (P), SDE-3 gap (Q)*
