# Section 01 — Java Core (Q1–Q25)

## Q1: Explain the JVM architecture and memory model.

**Answer:** The JVM has three main subsystems: ClassLoader (loads .class files), Runtime Data Areas (memory), and Execution Engine (JIT compiler + GC).

**Memory areas:**
- **Heap** — shared, stores all objects. Divided into Young Gen (Eden + Survivor) and Old Gen.
- **Stack** — per thread, stores frames (local variables, operand stack, method references).
- **Metaspace** — class metadata (replaced PermGen in Java 8). Grows dynamically.
- **Program Counter** — per thread, tracks current instruction.
- **Native Method Stack** — for JNI calls.

**GSTN context:** At 100K concurrent users, each Tomcat thread's stack defaults to 1MB. With 200 threads, that's 200MB just for stacks. We tuned `-Xss512k` after profiling showed our deepest call chains were ~50 frames deep.

### Follow-up: What's the difference between stack and heap memory?
Stack is thread-private, LIFO, holds primitives and references. Heap is shared, holds objects. Stack allocation is faster (pointer bump) but limited in size. Escape analysis (JIT) can allocate heap objects on the stack if they don't escape the method — we saw this reduce young GC pressure by ~15% on hot paths.

### Follow-up: How does the JIT compiler work?
JVM starts interpreting bytecode. After a method is called ~10,000 times (C2 threshold), JIT compiles it to native code. Optimizations: method inlining, loop unrolling, dead code elimination, escape analysis. You can see this with `-XX:+PrintCompilation`. In GSTN, our GSTIN validation method was the first to get JIT-compiled — called millions of times per hour.

---

## Q2: Explain Java's Garbage Collection mechanisms.

**Answer:** GC automatically reclaims heap memory. Objects with no reachable references are collected.

**GC algorithms:**
- **Serial GC** — single thread, stop-the-world. Only for small heaps (<100MB).
- **Parallel GC** — multiple GC threads, still stop-the-world. Good throughput for batch jobs.
- **G1GC** (default Java 11+) — divides heap into ~2048 equal regions. Does incremental collection targeting regions with most garbage first. Configurable pause target: `-XX:MaxGCPauseMillis=200`.
- **ZGC** — sub-millisecond pauses regardless of heap size. Colored pointers + load barriers. Concurrent compaction.
- **Shenandoah** — similar to ZGC, available in OpenJDK. Concurrent evacuation using Brooks forwarding pointers.

**GC roots:** Static references, active thread stacks, JNI references, synchronized monitors.

**GSTN context:** We use G1GC for API services with `-XX:MaxGCPauseMillis=100`. For overnight batch reconciliation of 300Cr+ invoices, we switch to Parallel GC (throughput > latency). We evaluated ZGC for our real-time filing status service but G1GC was sufficient at our scale.

### Follow-up: How do you diagnose a memory leak?
1. Monitor heap growth over time (Prometheus + Grafana JVM dashboard).
2. Enable GC logging: `-Xlog:gc*:file=gc.log:time,uptime`.
3. Take heap dump: `jmap -dump:live,format=b,file=heap.hprof <pid>`.
4. Analyze with Eclipse MAT: dominator tree → find the object holding unexpectedly large retained size.
5. In GSTN, we found a ConcurrentHashMap-based session cache that never evicted entries because the cleanup scheduled task had silently died. Replaced with Caffeine (bounded, auto-evicting).

### Follow-up: Explain the generational hypothesis.
Most objects die young. Young gen uses copying collection (fast, no fragmentation). Long-lived objects get promoted to old gen. This is why young GC (minor GC) is fast and frequent, while old gen GC (major GC) is slow and rare. At GSTN, ~95% of request-scoped objects die in young gen — they never even get promoted.

---

## Q3: HashMap internals — how does put() work?

**Answer:**
1. Compute hash: `key.hashCode()` → spread bits: `hash ^ (hash >>> 16)` — reduces collisions in lower bits.
2. Find bucket: `(capacity - 1) & hash` (capacity always power of 2).
3. If bucket empty → insert new Node.
4. If bucket has entries → walk linked list/tree, compare hash AND equals().
5. If key exists → replace value. If not → append.
6. If linked list length > 8 AND capacity >= 64 → treeify to red-black tree (O(log n) instead of O(n)).
7. If size > capacity × loadFactor (0.75) → resize (double, rehash all entries).

**GSTN bug story:** Custom GSTIN key class didn't override hashCode() consistently with equals(). Two GSTIN objects with same value went to different buckets. Cache hit rate dropped to ~0%. Root cause found via debugging, fixed by implementing proper hashCode using Objects.hash().

### Follow-up: Why is the treeification threshold 8?
Poisson distribution. With a good hash function and loadFactor 0.75, probability of 8+ items in one bucket is ~0.00000006. Only happens with pathological hashing or hash DoS. The threshold balances tree overhead (more memory, slower for small lists) against degenerate O(n) lookups.

### Follow-up: HashMap vs ConcurrentHashMap vs Hashtable?
- **Hashtable:** Legacy, synchronizes every method on single lock. Complete serialization. Don't use.
- **ConcurrentHashMap:** Java 8+ uses CAS for bucket updates, synchronizes only on individual bins during collision. Read operations are lock-free (volatile reads). We use this for GSTN's GSTIN→taxpayer cache — 95%+ reads.
- **Collections.synchronizedMap():** Wraps any map with synchronized methods. Slightly better than Hashtable (can wrap any Map), but still single-lock.

---

## Q4: Java Concurrency — Thread safety approaches.

**Answer:** Four main approaches:

1. **Immutability** — All fields final, no setters. Zero sync cost. GSTN taxpayer DTOs are immutable.
2. **Synchronized/Locks** — Mutual exclusion. `ReentrantReadWriteLock` for our tax rules config cache (many readers, rare updates).
3. **Lock-free (CAS)** — `AtomicInteger`, `ConcurrentHashMap`, `LongAdder`. GSTN filing counter uses `LongAdder` (better than AtomicLong under high contention — spreads updates across cells).
4. **Thread confinement** — `ThreadLocal` for request context (GSTIN, requestId). Zero sync because data never crosses threads.

### Follow-up: Explain the volatile keyword.
`volatile` guarantees: (1) Visibility — writes immediately flushed to main memory, reads always from main memory, not CPU cache. (2) Prevents instruction reordering around volatile access (memory barrier). Does NOT guarantee atomicity — `volatile int counter; counter++` is still racy (read-modify-write is 3 steps). Use for flags, not counters. We use volatile for our circuit breaker state flag.

### Follow-up: What is a deadlock? How to prevent?
Deadlock: Thread A holds Lock1, waits for Lock2. Thread B holds Lock2, waits for Lock1. Prevention: (1) Lock ordering — always acquire locks in same global order. (2) tryLock with timeout — `lock.tryLock(5, TimeUnit.SECONDS)`. (3) Avoid nested locks when possible. In GSTN batch processing, we use tryLock to prevent deadlocks between filing and validation jobs.

### Follow-up: CompletableFuture vs traditional threading?
CompletableFuture is Java 8's composable async programming. Chain async operations: `supplyAsync().thenApply().thenCombine().exceptionally()`. In GSTN, we use `CompletableFuture.allOf()` to fan out parallel calls to validation service, notification service, and audit service — then combine results. Much cleaner than managing raw threads/ExecutorService + Future.get().

---

## Q5: Explain Java Streams API.

**Answer:** Streams provide declarative data processing pipelines. Lazy evaluation — intermediate ops (map, filter, sorted) build a pipeline, terminal ops (collect, forEach, reduce) trigger execution.

**When to use:** Data transformation, filtering, aggregation where readability matters.
**When NOT to use:** Performance-critical tight loops, complex control flow (break/continue), side effects.

**GSTN example:**
```java
List<FilingDTO> validFilings = rawFilings.stream()
    .filter(f -> f.getStatus() != DRAFT)
    .filter(f -> taxValidator.isValid(f))
    .map(FilingMapper::toDTO)
    .sorted(comparing(FilingDTO::getFilingDate).reversed())
    .collect(toList());
```

For hot-path GSTIN validation (millions of calls), we use plain loops — stream object creation overhead was measurable.

### Follow-up: Parallel streams — when actually faster?
Rarely. Requirements: (1) Large dataset (10K+ elements), (2) CPU-bound operations per element, (3) No shared mutable state, (4) Splittable source (ArrayList good, LinkedList bad). Uses ForkJoinPool.commonPool() — shared across your app. We tested with 50K filing records — only 1.3x speedup because bottleneck was DB lookups, not CPU.

---

## Q6: Explain the String pool and immutability.

**Answer:** Strings are immutable — char/byte array never changes after creation. Benefits: thread safety, hash caching, string pool deduplication.

**String pool:** Literals (`"hello"`) are automatically interned — stored in a shared pool on the heap. `new String("hello")` creates a separate object (not pooled). `String.intern()` explicitly adds to pool.

**StringBuilder vs StringBuffer:** StringBuilder is not thread-safe (fast). StringBuffer is synchronized (slow, rarely needed). String `+` in a loop creates new String each iteration — O(n²). In GSTN's report generator, switching from concat to StringBuilder reduced p99 by 40ms on batch endpoints.

---

## Q7: Explain Java generics and type erasure.

**Answer:** Generics provide compile-time type safety. `List<String>` ensures only Strings go in. But due to **type erasure**, generic type info is removed at runtime — `List<String>` becomes raw `List` in bytecode. This was for backward compatibility with pre-Java 5 code.

**Implications:**
- Can't do `new T()` or `T.class` at runtime — type info erased.
- Can't overload methods differing only in generic type (`void foo(List<String>)` vs `void foo(List<Integer>)` — same erasure).
- `instanceof` can't check generic type.
- Wildcards: `? extends T` (upper bound, read-only), `? super T` (lower bound, write-only) — PECS: Producer Extends, Consumer Super.

---

## Q8: Explain the Java Memory Model (JMM) and happens-before.

**Answer:** JMM defines how threads communicate through memory. Without proper synchronization, one thread's writes may not be visible to another (CPU caching, instruction reordering).

**Happens-before rules:**
1. Program order within a thread
2. Monitor lock: unlock happens-before subsequent lock of same monitor
3. Volatile write happens-before subsequent volatile read of same variable
4. Thread start: `thread.start()` happens-before any action in that thread
5. Thread join: all actions in thread happen-before `join()` returns
6. Transitive: if A happens-before B, and B happens-before C, then A happens-before C

Without these guarantees, compiler and CPU can reorder instructions. Classic example: double-checked locking was broken before Java 5 because JIT could reorder object initialization. The `volatile` keyword on the singleton field fixes it by inserting memory barriers.

---

## Q9: Exception handling best practices.

**Answer:**
- **Checked exceptions:** Business errors that caller must handle (`IOException`, `SQLException`). Use for recoverable conditions.
- **Unchecked exceptions (RuntimeException):** Programming errors (`NullPointerException`, `IllegalArgumentException`). Don't force callers to handle.
- **Error:** JVM-level (OutOfMemoryError, StackOverflowError). Don't catch these.

**Best practices at GSTN:**
1. Custom exception hierarchy: `GSTNException` → `FilingValidationException`, `AuthenticationException`, etc.
2. Never catch `Exception` broadly — catch specific types.
3. Always log the original exception: `catch (SQLException e) { throw new DataAccessException("Filing query failed", e); }` — don't lose the stack trace.
4. Use try-with-resources for AutoCloseable (DB connections, streams).
5. Global exception handler in Spring (`@ControllerAdvice`) maps exceptions to proper HTTP responses.

---

## Q10: Explain the equals() and hashCode() contract.

**Answer:**
1. If `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` MUST be true.
2. If `a.hashCode() == b.hashCode()`, `a.equals(b)` may or may not be true (hash collisions allowed).
3. `equals()` must be reflexive, symmetric, transitive, consistent, and `a.equals(null)` returns false.

**Breaking the contract:** If you override equals() but not hashCode(), HashMap breaks — equal objects can end up in different buckets (different hashCodes → different bucket indices).

**GSTN bug:** Custom GSTIN key class overrode equals() (comparing gstin string) but inherited Object.hashCode() (identity-based). Two GSTIN objects with same value had different hashCodes → cache misses. Fixed with `Objects.hash(gstinNumber)`.

**Best practice:** Use `@Override`, use `Objects.equals()` and `Objects.hash()`, consider records (Java 16+) which auto-generate both.

---

## Q11: Explain functional interfaces and lambda expressions.

**Answer:** A functional interface has exactly one abstract method. Lambda provides concise syntax for implementing it.

Core functional interfaces in `java.util.function`:
- `Predicate<T>`: T → boolean (for filtering)
- `Function<T,R>`: T → R (for mapping)
- `Consumer<T>`: T → void (for side effects)
- `Supplier<T>`: () → T (for lazy creation)
- `BiFunction<T,U,R>`: (T,U) → R

**Method references:** `String::toUpperCase` is shorthand for `s -> s.toUpperCase()`.

**GSTN usage:** We use `Predicate` chains for composable validation rules:
```java
Predicate<Filing> isActive = f -> f.getStatus() == ACTIVE;
Predicate<Filing> isCurrentPeriod = f -> f.getPeriod().equals(currentPeriod);
List<Filing> result = filings.stream()
    .filter(isActive.and(isCurrentPeriod))
    .collect(toList());
```

---

## Q12–Q25: Additional Core Topics (Summary)

### Q12: What are Records (Java 16+)?
Immutable data carriers. Auto-generates constructor, getters, equals(), hashCode(), toString(). `record GSTINKey(String gstin, String period) {}` — replaces boilerplate DTOs.

### Q13: Sealed classes (Java 17)?
Restrict which classes can extend. `sealed class FilingStatus permits Draft, Submitted, Validated, Rejected {}` — compiler knows all subtypes. Enables exhaustive pattern matching in switch.

### Q14: Explain the Optional class.
Container for possibly-null values. Prevents NPE through explicit handling: `optional.map().orElse()`. Never use Optional for fields or method params — only return types. We use Optional for DB lookups: `findByGstin()` returns `Optional<Taxpayer>`.

### Q15: What is the Fork/Join framework?
Work-stealing thread pool for recursive divide-and-conquer. `RecursiveTask<V>` (returns result) or `RecursiveAction` (void). Each task forks subtasks; idle threads steal work from busy threads. CompletableFuture's async methods use ForkJoinPool.commonPool() by default.

### Q16: Explain Java modules (JPMS, Java 9+).
Module system: `module-info.java` declares what a module exports and requires. Stronger encapsulation than packages — internal classes truly hidden. `module gstn.filing { exports com.gstn.filing.api; requires spring.boot; }`. We haven't adopted modules at GSTN due to library compatibility issues, but understand the concept.

### Q17: What are virtual threads (Java 21)?
Lightweight threads managed by JVM, not OS. `Thread.ofVirtual().start(() -> {...})`. Can run millions simultaneously. Perfect for I/O-bound workloads (DB calls, HTTP calls). Traditional platform threads are expensive (~1MB stack each). Virtual threads share carrier threads. GSTN could benefit — we currently use thread pools sized at ~200 for Tomcat; with virtual threads, each request gets its own cheap thread.

### Q18: Explain the Executor framework.
`ExecutorService` manages thread pools. Types: FixedThreadPool (bounded), CachedThreadPool (unbounded, short-lived tasks), ScheduledThreadPool (delayed/periodic), WorkStealingPool (fork-join). Always use `Executors` or `ThreadPoolExecutor` with explicit queue and rejection policy. GSTN uses fixed pools for API (200 threads) and scheduled pools for batch jobs (cleanup, reconciliation).

### Q19: Explain Java I/O vs NIO.
**I/O (java.io):** Stream-based, blocking. Read/write one byte/char at a time. Simple but doesn't scale.
**NIO (java.nio):** Buffer-based, non-blocking channels, selectors for multiplexing. One thread can handle many connections. Netty/Spring WebFlux built on NIO. GSTN's API gateway uses Netty under the hood.

### Q20: What is reflection and when to use it?
Inspecting/modifying class structure at runtime. `Class.forName()`, `method.invoke()`. Used by Spring (DI, AOP proxy), Hibernate (field mapping), serialization libraries. Performance cost: bypasses compile-time checks, slower than direct calls. Don't use in hot paths.

### Q21: Explain annotations and how to create custom ones.
Metadata on code elements. `@Retention(RUNTIME)` for reflection access, `@Target(METHOD)` for where it applies. GSTN custom annotations: `@AuditLog` (AOP-based audit trail), `@RateLimited(qps=100)` (method-level rate limiting via aspect).

### Q22: What is serialization?
Converting object to byte stream and back. `Serializable` interface, `serialVersionUID` for version control. Security risk: deserialization can execute arbitrary code. Prefer JSON (Jackson) over Java serialization. GSTN uses Jackson for all API serialization.

### Q23: Explain the ClassLoader hierarchy.
Bootstrap (core Java) → Platform/Extension → Application (classpath). Parent delegation: child asks parent first. Custom classloaders for hot-reloading, plugin systems. Spring Boot uses a custom classloader for nested JARs.

### Q24: Explain Java's type system — primitives vs wrappers.
8 primitives (int, long, double, etc.) live on stack. Wrappers (Integer, Long, Double) are objects on heap. Autoboxing converts between them. Performance trap: `Integer` in a tight loop creates garbage. Use `int[]` not `Integer[]` in DSA problems. Integer cache: -128 to 127 are cached — `Integer.valueOf(127) == Integer.valueOf(127)` is true.

### Q25: Explain the Collections framework hierarchy.
`Collection` → `List` (ordered: ArrayList, LinkedList), `Set` (unique: HashSet, TreeSet, LinkedHashSet), `Queue` (FIFO: PriorityQueue, ArrayDeque). `Map` (separate hierarchy: HashMap, TreeMap, LinkedHashMap, ConcurrentHashMap). Choose based on: ordering needs, uniqueness, thread safety, performance characteristics. GSTN default: ArrayList for lists, HashMap for maps, ConcurrentHashMap for shared state.
