# SECTION 1: JAVA CORE — Interview Answers (Q1–Q25)
## With GSTN Codebase References

---

### Q1. How does HashMap work internally? What happens during hash collision? What changed in Java 8?

**Answer:**

HashMap internally uses an **array of Node (bucket array)**. Each Node contains: `hash`, `key`, `value`, `next`.

**How put() works:**
1. Compute `hash(key)` → `hashCode() ^ (hashCode >>> 16)` (spreads higher bits)
2. Calculate bucket index: `(n - 1) & hash` where n = array length
3. If bucket is empty → insert new Node
4. If bucket occupied → **hash collision** → compare keys using `equals()`
   - Same key → overwrite value
   - Different key → chain as linked list

**What changed in Java 8:**
- **Treeification**: When a bucket's linked list exceeds **8 nodes** (and array size ≥ 64), the list converts to a **Red-Black Tree**, reducing worst-case lookup from O(n) to O(log n)
- When tree shrinks below **6 nodes**, it converts back to linked list
- Hash function was simplified (single XOR vs multiple in Java 7)

**GSTN Example:** In our codebase, we use `HashMap` extensively for building response maps. For example, in `DistCacheUtil`, we maintain `Map<String, List<String>> msgMap` for error code lookups — these maps are read-heavy and rarely have collisions since keys are well-distributed error codes.

```java
// From GSTLogicalException.java — error message registry
private static Map<String, List<String>> msgMap;  // HashMap for error code → message mapping
```

**Interview Tip:** Mention that the default initial capacity is 16, load factor is 0.75, and resizing doubles the array and rehashes all entries.

---

### Q2. Difference between HashMap, LinkedHashMap, TreeMap, and ConcurrentHashMap? Which did you use in GSTN and why?

**Answer:**

| Feature | HashMap | LinkedHashMap | TreeMap | ConcurrentHashMap |
|---------|---------|---------------|---------|-------------------|
| Ordering | No order | **Insertion order** | **Sorted (natural/comparator)** | No order |
| Null keys | 1 null key | 1 null key | **No null keys** | **No null keys/values** |
| Thread-safe | No | No | No | **Yes** |
| Time complexity | O(1) avg | O(1) avg | **O(log n)** | O(1) avg |
| Implementation | Array + LinkedList/Tree | Array + Doubly-linked list | **Red-Black Tree** | Segment-based (Java 7) / CAS + synchronized (Java 8) |

**GSTN Usage:**
- **HashMap**: Most common — response building, request parameter mapping. In `Anx1aServiceImpl`, we use HashMap for building JSON response structures.
- **ConcurrentHashMap**: Used in our Kafka configuration. `KafkaConsumerConfig` uses it as a singleton with concurrent access from multiple consumer threads. Also used in `DistCacheUtil` for thread-safe local caching.
- **LinkedHashMap**: Used where we need insertion-order iteration — e.g., maintaining ordered list of GSTR sections for filing sequence.
- **TreeMap**: Used in audit/reporting where sorted display of data (by date, by GSTIN) is required.

```java
// ConcurrentHashMap example — from KafkaConsumerConfig (thread-safe config)
private static KafkaConsumerConfig instance = new KafkaConsumerConfig(); // Singleton with thread-safe maps

// HashMap example — response building in controllers
Map<String, Object> responseMap = new HashMap<>();
responseMap.put("statusCode", "SUCCESS");
responseMap.put("data", result);
```

---

### Q3. How does ConcurrentHashMap achieve thread safety? How is it different from Collections.synchronizedMap()?

**Answer:**

**ConcurrentHashMap (Java 8+):**
- Uses **CAS (Compare-And-Swap)** operations for lock-free reads
- **synchronized block on individual bucket** (node-level locking) for writes
- Multiple threads can **read and write concurrently** on different buckets
- No locking for reads at all — uses `volatile` reads
- Size computation uses `CounterCell` array (distributed counting)

**Java 7 ConcurrentHashMap:** Used **Segment-based locking** (16 segments by default), each segment was essentially a mini-HashMap with its own lock.

**Collections.synchronizedMap():**
- Wraps every method with `synchronized(mutex)` — **one global lock**
- Only **one thread** can access the map at any time (read OR write)
- Iterators are NOT thread-safe — need external synchronization

**Key Differences:**

| Aspect | ConcurrentHashMap | synchronizedMap |
|--------|-------------------|-----------------|
| Lock granularity | Per-bucket / CAS | Entire map |
| Read concurrency | **Lock-free** | Blocked by writes |
| Iterator | **Weakly consistent** | Fail-fast |
| Null keys/values | **Not allowed** | Allowed |
| Performance | **Much better** under contention | Poor under contention |

**GSTN Context:** In GSTN where we handle 100K+ concurrent requests during filing season, we use ConcurrentHashMap in our framework components like `DistCacheUtil` and `KafkaConsumerConfig` — using synchronizedMap would create severe contention bottlenecks.

---

### Q4. ArrayList vs LinkedList — when to use each? Internal resizing of ArrayList?

**Answer:**

**ArrayList:**
- Backed by **dynamic array** (`Object[] elementData`)
- **Fast random access**: O(1) via index
- **Slow insert/delete in middle**: O(n) — shifts elements
- **Memory**: Contiguous, cache-friendly

**LinkedList:**
- **Doubly-linked list** — each node has `prev`, `item`, `next`
- **Slow random access**: O(n) — traverse from head/tail
- **Fast insert/delete at known position**: O(1) if iterator positioned
- **More memory overhead**: Each node = object overhead + 2 pointers + data
- Also implements **Deque** — can be used as stack/queue

**ArrayList Resizing:**
1. Default initial capacity: **10**
2. When full: new capacity = **oldCapacity + (oldCapacity >> 1)** = **1.5x growth**
3. Uses `Arrays.copyOf()` → creates new array and copies elements
4. Best practice: **pre-size** with `new ArrayList<>(expectedSize)` to avoid resizing

**GSTN Usage:** We overwhelmingly use `ArrayList` because:
- Most operations are iteration and random access (building responses, processing lists of GSTINs)
- In our controllers, we receive and return `List<CaseAllocationDetailsVO>` — always ArrayList
- We use `subList()` for chunking large lists (CR27145 pattern in `CaseMgmtController`)

```java
// From CaseMgmtController — chunking pattern with ArrayList
@PostMapping(value = "/auth/api/case/create")
public @ResponseBody Object createCaseApp(
    @RequestBody List<CaseAllocationDetailsVO> caseAllocationDetailsListVO) {
    // Lists are ArrayList — used for iteration and chunking
}
```

---

### Q5. How does HashSet work internally? What's the relationship between equals() and hashCode()?

**Answer:**

**HashSet internally uses a HashMap!**
```java
// JDK source
public class HashSet<E> implements Set<E> {
    private transient HashMap<E, Object> map;
    private static final Object PRESENT = new Object(); // dummy value
    
    public boolean add(E e) {
        return map.put(e, PRESENT) == null; // key = element, value = dummy
    }
}
```

**equals() and hashCode() contract:**
1. If `a.equals(b)` is true → `a.hashCode() == b.hashCode()` MUST be true
2. If `a.hashCode() == b.hashCode()` → `a.equals(b)` MAY or MAY NOT be true (collision)
3. If you override `equals()`, you MUST override `hashCode()`

**Why this matters:**
- HashMap/HashSet first checks `hashCode()` to find the bucket
- Then checks `equals()` to find exact match within the bucket
- If you break the contract: objects that are "equal" may land in different buckets → duplicates in Set, missed lookups in Map

**GSTN Example:** In our entity classes, we use Lombok's `@EqualsAndHashCode` for composite keys:
```java
// From ApplnPK.java — composite key with proper equals/hashCode
@Embeddable
@EqualsAndHashCode  // Lombok generates consistent equals() and hashCode()
public class ApplnPK implements Serializable {
    @ManyToOne
    @JoinColumn(name = "APPLN_DETL_ID")
    private ApplnDraftDetlEntity applnDrftDetl;
    
    @Column(name = "VER_ID")
    private Integer versionId;
}
```

---

### Q6. What is the fail-fast vs fail-safe iterator? Which collections use which?

**Answer:**

**Fail-Fast Iterator:**
- Throws `ConcurrentModificationException` if collection is **structurally modified** during iteration
- Uses internal `modCount` — iterator checks if modCount changed
- **Collections**: ArrayList, HashMap, HashSet, LinkedList, TreeMap
- Happens even in single-threaded context (e.g., modifying list inside for-each loop)

```java
// Fails with ConcurrentModificationException
List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));
for (String s : list) {
    if (s.equals("B")) list.remove(s); // BOOM!
}

// Correct way: use Iterator.remove()
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().equals("B")) it.remove(); // Safe
}
```

**Fail-Safe Iterator:**
- Works on a **clone/snapshot** of the collection — never throws CME
- May not reflect latest modifications
- **Collections**: `ConcurrentHashMap`, `CopyOnWriteArrayList`, `CopyOnWriteArraySet`
- Called **"weakly consistent"** in Java docs

**GSTN Context:** In our multi-threaded Kafka consumer processing, we use ConcurrentHashMap with its weakly-consistent iterators. When multiple consumer threads update shared state, fail-safe iteration ensures no exceptions. For single-threaded response building, we use ArrayList with fail-fast iterators since there's no concurrent modification risk.

---

### Q7. PriorityQueue internals — how does it work? When would you use it in a backend service?

**Answer:**

**Internals:**
- Backed by a **binary min-heap** (array-based)
- `poll()` always returns the **smallest element** (or highest priority)
- `offer()`: O(log n) — sift up
- `poll()`: O(log n) — sift down
- `peek()`: O(1) — just return root
- NOT thread-safe. Use `PriorityBlockingQueue` for multi-threaded scenarios

**Array representation of heap:**
- Parent of index `i`: `(i - 1) / 2`
- Left child: `2 * i + 1`
- Right child: `2 * i + 2`

**Backend use cases:**
1. **Task scheduling by priority** — process high-priority GST returns before low-priority
2. **Top-K queries** — finding top K taxpayers by revenue without sorting entire dataset
3. **Rate limiting** — prioritize requests based on deadline proximity
4. **Dijkstra's algorithm** — shortest path in service routing

**GSTN Example:** During filing season, if we need to prioritize processing of returns, we could use PriorityQueue to process returns filed closer to the deadline first. In our Kafka consumer framework, the scheduled error topic consumption uses similar priority-based processing.

---

### Q8. Thread lifecycle in Java? How do you create threads (Thread class vs Runnable vs Callable)?

**Answer:**

**Thread States (6 states):**
```
NEW → RUNNABLE → (BLOCKED | WAITING | TIMED_WAITING) → TERMINATED
```

1. **NEW**: Thread created, not yet started
2. **RUNNABLE**: `start()` called — eligible to run (includes both ready and running)
3. **BLOCKED**: Waiting to acquire monitor lock (e.g., entering synchronized block)
4. **WAITING**: `wait()`, `join()`, `LockSupport.park()` — indefinite wait
5. **TIMED_WAITING**: `sleep(ms)`, `wait(ms)`, `join(ms)` — bounded wait
6. **TERMINATED**: `run()` completed or exception thrown

**Three ways to create threads:**

| Approach | Returns value? | Throws checked exception? | Usage |
|----------|---------------|--------------------------|-------|
| `extends Thread` | No | No | Simple, but can't extend another class |
| `implements Runnable` | No | No | Preferred — separates task from thread |
| `implements Callable<V>` | **Yes (Future<V>)** | **Yes** | When you need result or exception |

**GSTN Usage:** In our codebase, we primarily use:
- **Runnable with ExecutorService** — Kafka consumer threads in `ConsumerService`
- **@Async** (Spring-managed) — which internally uses a `TaskExecutor` thread pool

```java
// From AsyncServiceImpl — Spring @Async (Runnable under the hood)
@EnableAsync
public class AsyncServiceImpl {
    @Async
    public void addCaptcha(String token, String captchaAnswer) {
        distCacheUtil.addToCaptchaCacheForAudio(token, captchaAnswer);
    }
}

// From AsyncConfig — TaskExecutor (thread pool)
@Bean(name = "taskExecutor")
public ThreadPoolTaskExecutor taskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(5);
    executor.setMaxPoolSize(10);
    executor.setQueueCapacity(100);
    executor.setThreadNamePrefix("AsyncThread-");
    return executor;
}
```

---

### Q9. Difference between synchronized, volatile, and Atomic classes? When to use each?

**Answer:**

| Feature | synchronized | volatile | Atomic (AtomicInteger, etc.) |
|---------|-------------|----------|------------------------------|
| Mechanism | Monitor lock (mutual exclusion) | Memory visibility only | **CAS (Compare-And-Swap)** |
| Atomicity | Yes (compound operations) | **No** (only read/write) | Yes (single variable) |
| Visibility | Yes | Yes | Yes |
| Blocking | **Yes** (contended) | No | **No** (lock-free, spin) |
| Use case | Protecting code blocks | Flags, status variables | Counters, accumulators |

**synchronized:** Use when you need **mutual exclusion** — only one thread can execute the block.
```java
synchronized(this) {
    count++;  // Read + increment + write = atomic
}
```

**volatile:** Use for **single variable** that one thread writes and others read. Prevents CPU caching (reads/writes go to main memory).
```java
private volatile boolean running = true; // Visibility guarantee
```

**Atomic classes:** Use for **lock-free thread-safe operations** on a single variable. Uses hardware CAS instruction.
```java
private AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet(); // Atomic — no lock needed
```

**GSTN Context:** Our `KafkaConsumerConfig` uses the Singleton pattern with a static instance — thread safety is ensured at initialization. Our `DistCacheUtil` methods are synchronized where needed for cache operations. The `@Async` framework uses `ThreadPoolTaskExecutor` which internally uses atomic operations for queue management.

---

### Q10. What is ExecutorService? Types of thread pools? Which did you use for GSTN batch processing?

**Answer:**

**ExecutorService** decouples **task submission** from **thread management**. You submit tasks, the pool manages threads.

**Thread Pool Types:**

| Pool | Factory Method | Threads | Queue | Use Case |
|------|---------------|---------|-------|----------|
| **Fixed** | `newFixedThreadPool(n)` | Fixed n | Unbounded LinkedBlockingQueue | Known workload, bounded concurrency |
| **Cached** | `newCachedThreadPool()` | 0 to Integer.MAX | SynchronousQueue | Short-lived tasks, bursty traffic |
| **Single** | `newSingleThreadExecutor()` | 1 | Unbounded LinkedBlockingQueue | Sequential execution guarantee |
| **Scheduled** | `newScheduledThreadPool(n)` | Fixed core | DelayedWorkQueue | Periodic/delayed tasks |

**GSTN Usage:**

1. **Spring's ThreadPoolTaskExecutor** (wraps Java's ThreadPoolExecutor):
```java
// From AsyncConfig.java in GspAuthActivity
@Bean(name = "taskExecutor")
public ThreadPoolTaskExecutor taskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(5);    // 5 threads always alive
    executor.setMaxPoolSize(10);    // Scale up to 10 under load
    executor.setQueueCapacity(100); // Queue 100 tasks before rejecting
    executor.setThreadNamePrefix("AsyncThread-");
    executor.initialize();
    return executor;
}
```

2. **ScheduledExecutorService** for Kafka error topic consumption:
```java
// From Consumer.java — KafkaConsumerFwk
ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(2);
scheduledExecutorService.scheduleAtFixedRate(/* consume error topic */);
```

3. **Batch processing** uses Spring Batch with `GstBatchJobConfigurer` which configures `JobRepository` and `TaskExecutor` for parallel step execution.

**Key concern:** Always use **bounded queues** in production. Unbounded queues can cause OOM if producers outpace consumers. Our `taskExecutor` uses `queueCapacity(100)` — rejects tasks after 100 queued.

---

### Q11. What is CompletableFuture? How did you use it for parallel API calls in GSTN?

**Answer:**

**CompletableFuture** is Java 8's improvement over `Future` — supports:
- **Asynchronous computation** with callbacks (no blocking `get()`)
- **Chaining**: `thenApply()`, `thenCompose()`, `thenCombine()`
- **Error handling**: `exceptionally()`, `handle()`
- **Combining multiple futures**: `allOf()`, `anyOf()`

**Key methods:**
```java
// Run async, return result
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> callReturnAPI(gstin));

// Chain transformations
future.thenApply(response -> parseResponse(response))
      .thenAccept(parsed -> saveToCache(parsed))
      .exceptionally(ex -> { log.error("Failed", ex); return null; });

// Parallel calls — wait for all
CompletableFuture<String> returns = CompletableFuture.supplyAsync(() -> getReturns(gstin));
CompletableFuture<String> ledger = CompletableFuture.supplyAsync(() -> getLedger(gstin));
CompletableFuture<String> profile = CompletableFuture.supplyAsync(() -> getProfile(gstin));

CompletableFuture.allOf(returns, ledger, profile).join(); // Wait for all 3
```

**GSTN Usage Pattern:** When building a taxpayer dashboard, we need data from multiple services (Returns, Ledger, Registration, Payment). Instead of calling them sequentially (4 × 200ms = 800ms), we call all in parallel:

```java
// Parallel API calls pattern used in GSTN dashboard
CompletableFuture<ReturnSummary> returnsFuture = 
    CompletableFuture.supplyAsync(() -> returnService.getSummary(gstin), taskExecutor);
CompletableFuture<LedgerBalance> ledgerFuture = 
    CompletableFuture.supplyAsync(() -> ledgerService.getBalance(gstin), taskExecutor);

// Wait for all, merge results
CompletableFuture.allOf(returnsFuture, ledgerFuture).join();
DashboardResponse dashboard = new DashboardResponse(returnsFuture.get(), ledgerFuture.get());
```

**Important:** Always pass a custom `Executor` — default uses `ForkJoinPool.commonPool()` which is shared across the JVM and can cause thread starvation.

---

### Q12. What is a deadlock? How do you detect and prevent it? Have you faced one in production?

**Answer:**

**Deadlock** = Two or more threads are **blocked forever**, each waiting for a lock held by the other.

**Four conditions (ALL must be true):**
1. **Mutual Exclusion** — resource can't be shared
2. **Hold and Wait** — thread holds one lock, waits for another
3. **No Preemption** — locks can't be forcibly taken
4. **Circular Wait** — T1 → waits for T2 → waits for T1

**Detection:**
- `jstack <pid>` — thread dump shows "Found one Java-level deadlock"
- JVisualVM / JConsole — "Detect Deadlock" button
- `ThreadMXBean.findDeadlockedThreads()` programmatically
- Thread dump analysis tools (fastThread.io)

**Prevention strategies:**
1. **Lock ordering** — always acquire locks in consistent order (e.g., by ID)
2. **Lock timeout** — `tryLock(timeout)` with `ReentrantLock` instead of `synchronized`
3. **Avoid nested locks** — minimize synchronized scope
4. **Use higher-level concurrency** — `ConcurrentHashMap`, `AtomicReference`, `@Transactional`

**GSTN Production scenario:** In a multi-datasource environment like GSTN, deadlocks typically occur at the **database level**, not Java level. For example, two concurrent return filings updating the same taxpayer's ledger in different order. We handle this with:
- `@Transactional(propagation = Propagation.REQUIRES_NEW)` to isolate transactions
- Consistent update ordering by GSTIN
- Database-level deadlock detection (MySQL auto-detects and rolls back one transaction)
- Retry logic on `DeadlockLoserDataAccessException`

---

### Q13. CountDownLatch vs CyclicBarrier vs Semaphore — differences and use cases?

**Answer:**

| Feature | CountDownLatch | CyclicBarrier | Semaphore |
|---------|---------------|---------------|-----------|
| Purpose | Wait for N events | Wait for N threads to arrive | Limit concurrent access to N |
| Reusable | **No** (one-time) | **Yes** (resets after each barrier) |  **Yes** |
| Who counts down | **Any thread** | **Participating threads** | acquire/release by any thread |
| Action on complete | Waiting threads unblocked | Optional barrier action | Next thread acquires permit |

**CountDownLatch:** "Wait for N things to finish"
```java
CountDownLatch latch = new CountDownLatch(3);
// 3 threads each call latch.countDown() when done
latch.await(); // Main thread waits for count to reach 0
```
**Use case:** Wait for all microservice health checks to complete before starting the app.

**CyclicBarrier:** "N threads wait for each other"
```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> System.out.println("All arrived!"));
// Each thread calls barrier.await() — all wait until 3 reach the barrier
```
**Use case:** Parallel batch processing — all worker threads finish chunk, then proceed to next phase.

**Semaphore:** "Allow only N concurrent access"
```java
Semaphore sem = new Semaphore(5); // 5 permits
sem.acquire(); // Blocks if no permit available
try { accessResource(); } 
finally { sem.release(); }
```
**Use case:** Rate limiting — allow only 5 concurrent connections to a downstream service.

**GSTN Context:** Our connection pool configuration (HikariCP with `maxActive=10`) is conceptually similar to a Semaphore — limiting concurrent DB connections. Our Kafka consumer framework uses similar patterns for thread coordination.

---

### Q14. What is ThreadLocal? When would you use it in a microservices context?

**Answer:**

**ThreadLocal** provides **per-thread isolated variables**. Each thread has its own copy — no synchronization needed.

```java
private static final ThreadLocal<String> requestId = new ThreadLocal<>();

// In filter/interceptor
requestId.set(UUID.randomUUID().toString());

// In any service method (same thread)
String id = requestId.get(); // Gets this thread's value

// MUST clean up to prevent memory leaks (especially with thread pools)
requestId.remove();
```

**Microservices use cases:**
1. **Request context propagation** — store user session, GSTIN, request ID
2. **MDC (Mapped Diagnostic Context)** for logging — internally uses ThreadLocal
3. **Database routing** — store which datasource shard to use for current request
4. **Transaction context** — Spring's TransactionSynchronizationManager uses ThreadLocal

**GSTN Usage — Database Routing:**
In GSTN, we route database queries to different shards based on state code. This uses ThreadLocal:
```java
// Database routing pattern used in GSTN
// Set the DB routing context per request
public void setDbRouting(String stateCd) {
    DbType.setCurrentDb(stateCd);  // ThreadLocal stores current shard
}

// RoutingDataSource reads ThreadLocal to determine which DataSource to use
public class RoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DbType.getCurrentDb(); // Reads from ThreadLocal
    }
}
```

**Warning:** Always call `remove()` in a `finally` block — thread pools reuse threads, stale ThreadLocal values cause **memory leaks** and **data corruption**.

---

### Q15. What is the Fork/Join framework? How does work-stealing algorithm work?

**Answer:**

**Fork/Join Framework** (Java 7) is designed for **divide-and-conquer parallelism**:
- **Fork**: Split task into smaller subtasks
- **Join**: Wait for subtasks to complete, combine results
- Uses `ForkJoinPool` with **work-stealing**

**Work-Stealing Algorithm:**
1. Each thread has its own **deque (double-ended queue)** of tasks
2. Thread pushes/pops from **tail** of its own deque (LIFO — better cache locality)
3. When a thread's deque is empty, it **steals from the head** of another thread's deque (FIFO — steals larger tasks)
4. This ensures **load balancing** without explicit coordination

**Key classes:**
- `RecursiveTask<V>` — returns a result
- `RecursiveAction` — no result (void)
- `ForkJoinPool` — the thread pool

```java
class SumTask extends RecursiveTask<Long> {
    protected Long compute() {
        if (array.length <= THRESHOLD) {
            return sequentialSum(array);
        }
        SumTask left = new SumTask(leftHalf);
        SumTask right = new SumTask(rightHalf);
        left.fork();          // Submit to pool
        Long rightResult = right.compute();  // Compute directly
        Long leftResult = left.join();       // Wait for forked task
        return leftResult + rightResult;
    }
}
```

**GSTN Context:** `CompletableFuture.supplyAsync()` without explicit executor uses `ForkJoinPool.commonPool()`. Our parallel stream operations also use Fork/Join internally. We're careful to NOT use parallel streams for I/O-bound operations (DB/API calls) since the common pool is shared and can cause starvation.

---

### Q16. Explain JVM memory model — Heap (Young Gen, Old Gen, Metaspace) vs Stack?

**Answer:**

```
JVM Memory
├── Heap (shared across threads)
│   ├── Young Generation
│   │   ├── Eden Space (new objects allocated here)
│   │   ├── Survivor S0 (From)
│   │   └── Survivor S1 (To)
│   └── Old Generation (Tenured — long-lived objects)
├── Metaspace (class metadata, method info — native memory, not heap)
├── Stack (per thread)
│   ├── Method frames
│   ├── Local variables
│   └── Operand stack
├── Code Cache (JIT compiled code)
└── Direct Memory (NIO buffers)
```

**Heap:**
- **Eden**: All new objects created here. Minor GC collects Eden.
- **Survivors S0/S1**: Objects surviving Minor GC copy between survivors (aging)
- **Old Gen**: Objects surviving multiple Minor GCs (age threshold, default 15) get promoted
- **Tuning**: `-Xms` (initial heap), `-Xmx` (max heap), `-Xmn` (young gen size)

**Metaspace (replaced PermGen in Java 8):**
- Stores class definitions, method metadata, constant pool
- Uses **native memory** (not limited by -Xmx)
- `-XX:MaxMetaspaceSize` to set limit
- Grows dynamically

**Stack (per thread):**
- Default size: 512KB-1MB (`-Xss` to configure)
- Stores: method call frames, local variables, return addresses
- `StackOverflowError` on deep recursion

**GSTN Context:** For our high-throughput filing services handling 100K+ concurrent requests, we tune:
- `-Xmx4g -Xms4g` (avoid heap resizing)
- `-XX:NewRatio=2` (1/3 young gen, 2/3 old gen)
- `-XX:+UseG1GC` for balanced latency/throughput

---

### Q17. Types of Garbage Collectors — Serial, Parallel, G1GC, ZGC? Which is best for a low-latency tax filing service?

**Answer:**

| GC | Algorithm | Pause | Throughput | Use Case |
|----|-----------|-------|------------|----------|
| **Serial** | Mark-Sweep-Compact | Long STW | Low | Single-thread, small heaps (dev/testing) |
| **Parallel (Throughput)** | Parallel Mark-Sweep-Compact | Medium STW | **Highest** | Batch processing, non-interactive |
| **CMS** (deprecated Java 14) | Concurrent Mark-Sweep | Short STW | Good | Low-latency (legacy) |
| **G1GC** (default Java 9+) | Region-based, incremental | **Predictable** | Good | **Best general-purpose**, heaps 4GB+ |
| **ZGC** (Java 15+) | Colored pointers, load barriers | **< 10ms** | Good | Ultra-low-latency, heaps up to TB |
| **Shenandoah** | Brooks pointers, concurrent compaction | **< 10ms** | Good | Similar to ZGC, Red Hat |

**G1GC (Garbage First) — our choice for GSTN:**
- Divides heap into **equal-sized regions** (1-32MB each)
- Tracks **"garbage-first"** — collects regions with most garbage first
- **Predictable pauses**: `-XX:MaxGCPauseMillis=200` (target, not guarantee)
- Mixed collections: can collect young + some old regions together
- Concurrent marking phase (mostly non-STW)

**For GSTN filing service:** G1GC is the best choice because:
1. Filing deadlines create traffic spikes — need **predictable** response times
2. Heap sizes are 4-8GB — G1GC optimized for this range
3. Mix of short-lived objects (request/response) and long-lived (cached data)
4. ZGC would be ideal for sub-10ms but requires Java 15+; our stack uses Java 8/11

```
# GSTN JVM tuning flags
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:G1HeapRegionSize=16m
-XX:+ParallelRefProcEnabled
```

---

### Q18. What causes OutOfMemoryError? Types and how to troubleshoot?

**Answer:**

**Types of OOM:**

| OOM Type | Cause | Fix |
|----------|-------|-----|
| `Java heap space` | Objects fill up heap | Increase `-Xmx`, fix memory leaks |
| `Metaspace` | Too many classes loaded (classloader leak) | Increase `-XX:MaxMetaspaceSize`, fix hot-deploy leaks |
| `GC overhead limit exceeded` | >98% time in GC, <2% heap freed | Usually a memory leak — fix root cause |
| `Unable to create new native thread` | Too many threads | Reduce thread count, increase OS limits |
| `Direct buffer memory` | NIO direct buffers exhausted | `-XX:MaxDirectMemorySize`, close buffers |

**Troubleshooting steps:**
1. **Heap dump on OOM**: `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/`
2. **Analyze with MAT (Memory Analyzer Tool)** or JVisualVM
3. Look for **Dominator Tree** — which objects hold most memory
4. Check **GC logs**: `-XX:+PrintGCDetails -Xloggc:/path/gc.log`
5. **Common leak patterns:**
   - Unbounded collections (Map growing forever)
   - Static references not cleared
   - ThreadLocal not `remove()`d in thread pools
   - Unclosed resources (streams, connections)
   - Listeners/callbacks not unregistered

**GSTN Production Scenario:** During filing deadline, if a service starts throwing OOM:
1. Take heap dump immediately
2. Check if connection pool is leaking (HikariCP leak detection)
3. Check Redis cache — are we caching too much data locally?
4. In MAT, look for `DistCacheUtil` or large `HashMap` collections
5. Common fix: add TTL to caches, add pagination to queries returning large datasets

---

### Q19. What is JIT compilation? How does the JVM optimize hot code paths?

**Answer:**

**JIT (Just-In-Time) Compilation:** The JVM initially **interprets** bytecode. When it detects a method is called frequently (**hot method**), the JIT compiler **compiles it to native machine code** for much faster execution.

**How it works:**
1. **Interpreter** executes bytecode initially
2. JVM **profiles** code — counts method invocations and loop iterations
3. When threshold reached (default: `-XX:CompileThreshold=10000`), JIT compiles method
4. Future calls execute **native code** instead of bytecode

**Two JIT compilers (Tiered Compilation — default since Java 8):**
- **C1 (Client)**: Fast compilation, basic optimizations — for quick startup
- **C2 (Server)**: Slower compilation, aggressive optimizations — for peak throughput
- **Tiered**: C1 first (quick win), C2 later (max performance)

**JIT Optimizations:**
- **Method inlining** — replace method call with body (biggest optimization)
- **Loop unrolling** — reduce loop overhead
- **Dead code elimination** — remove unreachable code
- **Escape analysis** — allocate objects on stack (no GC needed) if they don't escape method
- **Lock elision** — remove synchronized if lock is never contended
- **Devirtualization** — convert virtual method calls to direct calls

**GSTN Impact:** Our filing APIs handle millions of calls. The JIT compiler heavily optimizes:
- Validation methods (called millions of times with same patterns)
- JSON serialization/deserialization (Jackson methods become native code)
- Database query building methods
- This is why **warmup time matters** — first few thousand requests are slower until JIT kicks in. In production, we use warmup scripts after deployment.

---

### Q20. How does ClassLoader work? Bootstrap → Extension → Application? ClassNotFoundException vs NoClassDefFoundError?

**Answer:**

**ClassLoader Hierarchy (Delegation Model):**
```
Bootstrap ClassLoader (C++ code, loads rt.jar — java.lang.*, java.util.*)
    ↑ delegates to parent first
Extension ClassLoader (jre/lib/ext — javax.*, security)
    ↑ delegates to parent first
Application ClassLoader (classpath — your app classes)
    ↑ delegates to parent first
Custom ClassLoaders (Tomcat's WebAppClassLoader, Spring's LaunchedURLClassLoader)
```

**How it works (Parent Delegation):**
1. Request to load `com.gst.api.ReturnService`
2. Application CL asks Extension CL → asks Bootstrap CL
3. Bootstrap doesn't have it → Extension doesn't have it
4. Application CL loads from classpath
5. **Why?** Prevents malicious `java.lang.String` replacement

**ClassNotFoundException vs NoClassDefFoundError:**

| | ClassNotFoundException | NoClassDefFoundError |
|---|---|---|
| Type | **Checked Exception** | **Error** (unchecked) |
| When | `Class.forName("com.X")` or ClassLoader.loadClass() fails at runtime | Class was present at **compile time** but missing at **runtime** |
| Cause | Class not on classpath | Missing dependency JAR, failed static initializer |
| Fix | Add JAR to classpath | Check deployment packaging, dependency conflicts |

**GSTN Context:** Our multi-module project (30+ modules) frequently encounters classpath issues:
- Each API module (ReturnAPI, LedgerAPI, RegistrationAPI) has its own pom.xml with specific dependency versions
- The `gst-spring-boot2-starter` custom starter must be on classpath for auto-configuration to work
- `NoClassDefFoundError` typically happens when a commons framework JAR version mismatch occurs between modules

---

### Q21. Functional interfaces — Predicate, Function, Consumer, Supplier, BiFunction? Give a real code example from GSTN.

**Answer:**

A **functional interface** has exactly **one abstract method** (can have default/static methods). Annotated with `@FunctionalInterface`.

| Interface | Method | Input → Output | Use Case |
|-----------|--------|---------------|----------|
| `Predicate<T>` | `test(T)` | T → boolean | Filtering, validation |
| `Function<T,R>` | `apply(T)` | T → R | Transformation, mapping |
| `Consumer<T>` | `accept(T)` | T → void | Side effects (logging, saving) |
| `Supplier<T>` | `get()` | () → T | Factory, lazy initialization |
| `BiFunction<T,U,R>` | `apply(T,U)` | (T,U) → R | Two-input transformation |
| `UnaryOperator<T>` | `apply(T)` | T → T | Same type transformation |

**GSTN Code Examples:**

```java
// PREDICATE — Filter valid GSTINs
Predicate<String> isValidGstin = gstin -> gstin != null && gstin.length() == 15;
List<String> validGstins = gstinList.stream()
    .filter(isValidGstin)
    .collect(Collectors.toList());

// FUNCTION — Transform entity to VO
Function<WfTask, TaskVO> entityToVo = task -> {
    TaskVO vo = new TaskVO();
    vo.setTaskId(task.getTaskId());
    vo.setStatus(task.getTaskStatus());
    return vo;
};
List<TaskVO> taskVOs = tasks.stream().map(entityToVo).collect(Collectors.toList());

// CONSUMER — Log and cache each result
Consumer<GSTMaster> cacheAndLog = master -> {
    distCacheUtil.addToEntityDetailsCache(master.getGstin(), master);
    LOGGER.info("Cached: {}", master.getGstin());
};
masters.forEach(cacheAndLog);

// SUPPLIER — Lazy default value
Supplier<ErrorResponse> defaultError = () -> new ErrorResponse("UNKNOWN", "Unexpected error");
```

---

### Q22. Stream API — map, filter, reduce, collect, flatMap? Parallel streams — when are they beneficial and when dangerous?

**Answer:**

**Key Stream Operations:**

```java
// filter — keep elements matching predicate
List<ReturnVO> filedReturns = returns.stream()
    .filter(r -> "FILED".equals(r.getStatus()))
    .collect(Collectors.toList());

// map — transform elements
List<String> gstins = returns.stream()
    .map(ReturnVO::getGstin)
    .collect(Collectors.toList());

// flatMap — flatten nested collections
List<ItemVO> allItems = returns.stream()
    .flatMap(r -> r.getItems().stream())  // List<List<Item>> → List<Item>
    .collect(Collectors.toList());

// reduce — aggregate to single value
BigDecimal totalTax = returns.stream()
    .map(ReturnVO::getTaxAmount)
    .reduce(BigDecimal.ZERO, BigDecimal::add);

// collect — terminal operation with Collectors
Map<String, List<ReturnVO>> byState = returns.stream()
    .collect(Collectors.groupingBy(ReturnVO::getStateCode));
```

**Parallel Streams:**

**Beneficial when:**
- CPU-bound computation (mathematical, parsing)
- Large dataset (> 10,000 elements)
- No shared mutable state
- Splittable source (ArrayList — good, LinkedList — bad)

**Dangerous when:**
- **I/O-bound** operations (DB calls, API calls) — uses ForkJoinPool.commonPool() (limited threads)
- **Shared mutable state** — race conditions
- **Order matters** — parallelism breaks ordering without `forEachOrdered()`
- **Small datasets** — overhead > benefit

**GSTN Warning:** Never use parallel streams for:
```java
// BAD — I/O in parallel stream uses common pool, can starve other operations
returns.parallelStream()
    .forEach(r -> saveToDB(r));  // DB calls in parallel stream = DANGEROUS

// GOOD — Use ExecutorService for I/O parallelism
CompletableFuture.allOf(
    returns.stream()
        .map(r -> CompletableFuture.runAsync(() -> saveToDB(r), customExecutor))
        .toArray(CompletableFuture[]::new)
).join();
```

---

### Q23. Optional — how to use properly? Why is it better than returning null?

**Answer:**

**Optional** is a container that may or may not contain a value. Introduced in Java 8 to avoid `NullPointerException`.

```java
// Creating Optional
Optional<String> opt1 = Optional.of("value");        // NPE if null
Optional<String> opt2 = Optional.ofNullable(value);   // empty if null
Optional<String> opt3 = Optional.empty();              // explicitly empty

// Using Optional (GOOD patterns)
String name = optional.orElse("default");                    // Default value
String name = optional.orElseGet(() -> computeDefault());    // Lazy default
String name = optional.orElseThrow(() -> new NotFoundException("Not found"));

// Chaining
optional.map(String::toUpperCase)
        .filter(s -> s.length() > 5)
        .ifPresent(s -> LOGGER.info("Found: {}", s));
```

**Anti-patterns (DON'T do these):**
```java
// BAD: Checking isPresent() + get() — defeats the purpose
if (optional.isPresent()) { return optional.get(); }

// BAD: Optional as method parameter
public void process(Optional<String> param) {} // Use @Nullable or overloaded methods

// BAD: Optional for fields
private Optional<String> name; // Use null for fields

// BAD: Optional with collections
Optional<List<String>> list; // Return empty list instead
```

**GSTN Example:**
```java
// From GspActiveAuthSessionRepository — Optional return
Optional<GspActiveAuthSession> findByAuthTokenAndUserName(String token, String userName);

// Usage
GspActiveAuthSession session = sessionRepository
    .findByAuthTokenAndUserName(token, userName)
    .orElseThrow(() -> new GSTLogicalException(LOGGER, "AUTH_TOKEN_INVALID"));
```

---

### Q24. Default and static methods in interfaces — why were they added? How do they help backward compatibility?

**Answer:**

**Added in Java 8** to evolve interfaces without breaking existing implementations.

**Default methods:**
```java
public interface ReturnProcessor {
    void process(ReturnVO returnVO);  // Abstract — must implement
    
    default void validate(ReturnVO returnVO) {  // Default — optional override
        if (returnVO.getGstin() == null) throw new ValidationException("GSTIN required");
    }
}
// Existing implementations DON'T need to change when validate() is added
```

**Why added:**
- **Backward compatibility** — Adding `stream()` and `forEach()` to `Collection` interface without breaking all implementations
- **Multiple inheritance of behavior** — Java has no multiple class inheritance but allows multiple interface defaults
- **Reduce boilerplate** — Common implementations once, override when needed

**Static methods:**
```java
public interface Validator {
    boolean validate(String input);
    
    static Validator combine(Validator... validators) {  // Factory method
        return input -> Arrays.stream(validators).allMatch(v -> v.validate(input));
    }
}
```

**Diamond problem resolution:**
```java
interface A { default void greet() { System.out.println("A"); } }
interface B { default void greet() { System.out.println("B"); } }
class C implements A, B {
    @Override
    public void greet() { A.super.greet(); } // MUST override — compiler error otherwise
}
```

**GSTN context:** Our service interfaces (like `WFXAService`, `Anx1aService`) use default methods for common utility operations while keeping core business methods abstract.

---

### Q25. What are Records (Java 14+) and Sealed classes (Java 17)? Have you used them?

**Answer:**

**Records (Java 14+ / 16 stable):**
- **Immutable data carriers** — replace boilerplate POJO/DTO code
- Auto-generates: constructor, getters, `equals()`, `hashCode()`, `toString()`

```java
// Before Records — 50+ lines with Lombok @Data
@Data
@AllArgsConstructor
public class GstinInfo {
    private String gstin;
    private String legalName;
    private String stateCode;
}

// With Records — 1 line!
public record GstinInfo(String gstin, String legalName, String stateCode) {}

// Usage
GstinInfo info = new GstinInfo("29AAACG1234A1ZD", "Infosys", "29");
String gstin = info.gstin(); // getter (no "get" prefix)
```

**Sealed Classes (Java 17):**
- Restrict which classes can extend/implement
- Enables exhaustive pattern matching in `switch`

```java
public sealed interface ReturnType permits GSTR1, GSTR3B, GSTR9 {}
public record GSTR1(String gstin, String period) implements ReturnType {}
public record GSTR3B(String gstin, String period, BigDecimal liability) implements ReturnType {}
public record GSTR9(String gstin, String year) implements ReturnType {}

// Exhaustive switch (compiler checks all subtypes covered)
String getDescription(ReturnType type) {
    return switch (type) {
        case GSTR1 r -> "Outward supplies for " + r.period();
        case GSTR3B r -> "Summary return, liability: " + r.liability();
        case GSTR9 r -> "Annual return for " + r.year();
    }; // No default needed — compiler KNOWS all subtypes
}
```

**GSTN Context:** Our current codebase uses Java 8/11 with Lombok (`@Data`, `@Builder`, `@AllArgsConstructor`) for DTO/VO classes like `HSNResponseDetailsVo`, `UnassignedArnSearchVO`. If we migrate to Java 17+, Records would replace many of these VOs, and Sealed classes would be perfect for our return type hierarchy (GSTR1, GSTR2, GSTR3B, GSTR9, etc.) where we want compile-time guarantees on type handling.
