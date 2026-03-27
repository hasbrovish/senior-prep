# FAANG / Product-Based / Startup — SDE-2/SDE-3 Interview Questions (5.5 YOE)
# Beyond the 296 — Recently Asked in 2025-2026 Rounds
# Companies: Google, Amazon, Microsoft, Flipkart, Razorpay, PhonePe, Swiggy, Uber, Atlassian, Stripe, Meesho, Cred, Zerodha, Goldman Sachs, Morgan Stanley

---

## ROUND STRUCTURE (Typical SDE-2/SDE-3)

```
Round 1: DSA / Problem Solving (45-60 min) — LeetCode Medium/Hard
Round 2: Low-Level Design (LLD) (45-60 min) — OOP, Design Patterns, SOLID
Round 3: High-Level Design (HLD) (45-60 min) — System Design, Scalability
Round 4: Deep Dive on Past Work + Java/Spring Internals (45-60 min)
Round 5: Hiring Manager / Behavioral (30-45 min)
```

---

## PART A: JAVA DEEP INTERNALS (Asked at Google, Amazon, Flipkart, Goldman Sachs)

---

### AQ1. Explain how `synchronized` works at the JVM level. What is monitor, biased locking, thin lock, fat lock?

**Answer:**

Every Java object has an **object header** containing a **mark word** that stores locking information.

**Lock escalation path:**
```
No Lock → Biased Lock → Thin (Lightweight) Lock → Fat (Heavyweight) Lock
```

1. **Biased Locking** (Java 6+, removed in Java 15):
   - First thread to acquire lock "biases" the object to itself
   - No CAS operation needed for re-entry by same thread
   - If another thread contends → revoke bias → escalate

2. **Thin Lock (Lightweight)**:
   - Uses CAS (Compare-And-Swap) on mark word
   - Thread copies mark word to its **Lock Record** on stack
   - CAS replaces mark word with pointer to Lock Record
   - If CAS fails (contention) → escalate to fat lock

3. **Fat Lock (Heavyweight)**:
   - Uses OS-level **mutex** (via `ObjectMonitor` in JVM)
   - Thread goes into BLOCKED state (context switch — expensive)
   - Has a wait set (for `wait()`) and entry list (for contending threads)

```java
// What the JVM sees internally:
synchronized (this) {  // → monitorenter bytecode
    // critical section
}  // → monitorexit bytecode

// monitorenter:
// 1. Try biased lock (is mark word biased to me?)
// 2. Try CAS thin lock
// 3. Inflate to fat lock, block thread
```

**Interview tip:** Mention that `synchronized` is **reentrant** — same thread can re-enter same lock (counter increments). This avoids self-deadlock.

**GSTN context:** We use `synchronized` sparingly. For high-concurrency caching in `DistCacheUtil`, we prefer `ConcurrentHashMap` and atomic operations. For Kafka consumer config, we use the singleton pattern with `private static` instance initialization (thread-safe by JVM class loading guarantee).

---

### AQ2. What is the Java Memory Model (JMM)? Explain happens-before relationship. Why is `volatile` not enough for compound operations?

**Answer:**

The **JMM** defines how threads interact through memory and what behaviors are allowed. Without JMM rules, compiler/CPU can reorder instructions.

**Happens-before rules:**
1. **Program order**: Each action in a thread happens-before the next action in that thread
2. **Monitor lock**: Unlock happens-before subsequent lock of same monitor
3. **Volatile**: Write to volatile happens-before subsequent read of same volatile
4. **Thread start**: `thread.start()` happens-before any action in the started thread
5. **Thread join**: All actions in a thread happen-before `join()` returns
6. **Transitivity**: If A happens-before B and B happens-before C, then A happens-before C

**Why volatile isn't enough for `count++`:**
```java
volatile int count = 0;

// Thread 1: count++  →  actually 3 steps:
// 1. READ count (= 0)        ←  volatile guarantees visibility
// 2. INCREMENT (0 + 1 = 1)   ←  NOT atomic
// 3. WRITE count (= 1)       ←  volatile guarantees visibility

// Thread 2 can READ between steps 1 and 3 → lost update!

// Solution: Use AtomicInteger
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();  // Single CAS operation — atomic
```

**When to use what:**
| Scenario | Use |
|----------|-----|
| Flag (boolean) shared between threads | `volatile` |
| Counter increment | `AtomicInteger` |
| Complex state update | `synchronized` or `Lock` |
| Read-heavy, write-rare | `ReadWriteLock` |

---

### AQ3. How does `ConcurrentHashMap` work internally in Java 8? What is the CAS + synchronized approach? How does it differ from Java 7's segment locking?

**Answer:**

**Java 7 — Segment locking:**
```
ConcurrentHashMap
├── Segment[0] → Entry[] → lock per segment (ReentrantLock)
├── Segment[1] → Entry[]
├── ...
└── Segment[15] → Entry[]   (default 16 segments = 16 concurrent writers)
```
Problem: Fixed concurrency level, extra memory for segments.

**Java 8 — Node array + CAS + synchronized per bucket:**
```
ConcurrentHashMap
├── Node[0] → null (CAS to insert first node)
├── Node[1] → Node → Node (synchronized on first node for chain operations)
├── Node[2] → TreeBin (Red-Black tree if > 8 nodes)
├── ...
└── Node[n-1]
```

**Operations:**
```java
// PUT operation:
// 1. If bucket empty → CAS (lock-free, no synchronized)
// 2. If bucket has nodes → synchronized(first_node_in_bucket) {
//        insert/update in linked list or tree
//    }
// 3. If chain length > 8 → treeify (like HashMap)

// GET operation: 
// NO LOCKING AT ALL — volatile reads on Node.val and Node.next
// Node class: volatile V val; volatile Node<K,V> next;

// SIZE: Uses LongAdder internally (distributed counters) — O(1) approximate
```

**Why this matters for GSTN:**
In `KafkaConsumerConfig` singleton, multiple consumer threads access shared configuration. `ConcurrentHashMap` allows lock-free reads (GET) while protecting concurrent writes with fine-grained per-bucket locking.

---

### AQ4. What are virtual threads (Project Loom, Java 21)? How do they change server-side Java programming? Would you use them for GSTN?

**Answer:**

**Problem with platform threads:**
- Each Java thread = 1 OS thread (~1MB stack memory)
- 10,000 concurrent requests = 10,000 OS threads = **10GB RAM just for stacks**
- Thread creation/context switching is expensive
- Blocking I/O (DB calls, HTTP calls) wastes thread

**Virtual threads (Java 21):**
```java
// Old way — limited by thread pool size
ExecutorService executor = Executors.newFixedThreadPool(200);  // max 200 concurrent
executor.submit(() -> {
    callDatabase();    // thread blocked, wasted
    callExternalAPI(); // thread blocked, wasted
});

// New way — millions of virtual threads
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
executor.submit(() -> {
    callDatabase();    // virtual thread yields, carrier thread reused
    callExternalAPI(); // virtual thread yields, carrier thread reused
});

// Or directly:
Thread.startVirtualThread(() -> handleRequest(request));
```

**How they work:**
- Virtual threads are scheduled by the JVM on a small pool of **carrier threads** (platform threads)
- When a virtual thread hits a blocking operation (I/O, sleep, lock), the JVM **unmounts** it from the carrier thread
- Carrier thread is free to run another virtual thread
- When I/O completes, virtual thread is **remounted** on any available carrier

**Would I use them for GSTN?**
Absolutely. GSTN services make heavy blocking calls:
- Database calls (MySQL via HikariCP)
- Redis cache calls (DistCacheUtil)
- Inter-service REST calls
- Kafka producer sends

With virtual threads, we could handle 100K+ concurrent filing requests with just 16 carrier threads (one per CPU core) instead of 200+ platform threads.

**Caveat:** Don't use with `synchronized` (pins the carrier thread). Use `ReentrantLock` instead. This is why Spring Boot 3.2+ added virtual thread support with careful `synchronized` → `Lock` migration.

---

### AQ5. Explain GC tuning you've done. How do you choose between G1GC, ZGC, and Shenandoah? What GC flags do you use in production?

**Answer:**

**G1GC (default since Java 9):**
```
Heap divided into ~2048 regions (each 1-32MB)
Regions classified: Eden, Survivor, Old, Humongous

Young GC: Copy live objects from Eden → Survivor (STW, but fast — young gen is small)
Mixed GC: Collect young + some old regions (collects regions with most garbage first — "Garbage First")
Full GC: Fallback — collect everything (try to avoid)
```

**ZGC (Java 15+ production-ready):**
- Pause times < 1ms regardless of heap size (even 16TB)
- Concurrent relocation using colored pointers (metadata in pointer bits)
- Best for: Low-latency services, large heaps

**Production GC flags for GSTN-like service:**
```bash
# G1GC for most services (balanced throughput + latency)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200        # Target max 200ms pause
-XX:G1HeapRegionSize=16m        # Region size for 8GB+ heaps
-XX:InitiatingHeapOccupancyPercent=45  # Start concurrent marking at 45%
-Xms4g -Xmx4g                  # Fixed heap (no resizing overhead)
-XX:+UseStringDeduplication     # Save memory on duplicate strings

# ZGC for latency-critical services (payment, filing)
-XX:+UseZGC
-XX:+ZGenerational              # Generational ZGC (Java 21+)
-Xms8g -Xmx8g

# Debugging flags
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/heapdump.hprof
-Xlog:gc*:file=/var/log/gc.log:time,level,tags
```

**Decision matrix:**
| GC | Use When | GSTN Service |
|-----|---------|------|
| G1GC | General purpose, 4-16GB heap | Return filing, Registration |
| ZGC | Ultra-low latency, large heap | Payment processing, real-time dashboard |
| Shenandoah | Low latency, RedHat JDK | Alternative to ZGC |
| Parallel GC | Max throughput, batch jobs | Batch return processing, reconciliation |

---

### AQ6. What is a memory leak in Java? How do you detect and fix it? Walk through a real debugging scenario.

**Answer:**

**Memory leak in Java:** Objects that are no longer needed but are still referenced (cannot be GCed).

**Common causes:**
1. **Static collections** that keep growing
2. **Unclosed resources** (streams, connections, ResultSet)
3. **Listeners/callbacks** not deregistered
4. **ThreadLocal** not cleaned up (especially in thread pools)
5. **Inner class holding reference** to outer class
6. **Cache without eviction** policy

**Debugging scenario (step by step):**

```bash
# Step 1: Observe symptoms
# - OOM errors in logs
# - Heap usage graph shows sawtooth going UP (GC can't reclaim)
# - gc.log shows Full GC frequency increasing

# Step 2: Take heap dump
jmap -dump:live,format=b,file=heapdump.hprof <PID>
# OR use -XX:+HeapDumpOnOutOfMemoryError (already set in production)

# Step 3: Analyze with Eclipse MAT (Memory Analyzer Tool)
# → Open heapdump.hprof
# → "Leak Suspects" report → shows suspicious objects
# → "Dominator Tree" → shows biggest memory holders
# → "Histogram" → shows object count by class

# Step 4: Identify leak
# Example: Found 500,000 instances of BOUserSession
# Dominator: static HashMap in SessionCache class
# Root cause: Sessions added but never removed on logout/timeout

# Step 5: Fix
// Before (leak):
public class SessionCache {
    private static Map<String, BOUserSession> sessions = new HashMap<>();
    public void addSession(String token, BOUserSession session) {
        sessions.put(token, session);  // NEVER removed!
    }
}

// After (fixed):
public class SessionCache {
    // Use WeakHashMap or explicit cleanup
    private static Map<String, BOUserSession> sessions = new ConcurrentHashMap<>();
    public void addSession(String token, BOUserSession session) {
        sessions.put(token, session);
    }
    public void removeSession(String token) {
        sessions.remove(token);  // Called on logout/timeout
    }
    // OR use Cache with TTL (Guava/Caffeine)
    private static Cache<String, BOUserSession> sessions = 
        Caffeine.newBuilder().expireAfterAccess(30, TimeUnit.MINUTES).build();
}
```

**GSTN context:** Our `DistCacheUtil` uses Redis (external cache) so JVM memory leaks from caching are avoided. But `ThreadLocal` in request context tracking must always be cleaned up in a `finally` block or filter.

---

## PART B: SPRING BOOT DEEP DIVE (Asked at Amazon, Flipkart, Razorpay, PhonePe, Atlassian)

---

### BQ1. How does Spring create a proxy for @Transactional? What's the difference between JDK Dynamic Proxy and CGLIB? When does @Transactional NOT work?

**Answer:**

**Proxy creation flow:**
```
1. Spring scans for @Transactional methods
2. Creates proxy object wrapping the target bean
3. When you @Autowire the service, you get the PROXY, not the real object
4. Proxy intercepts method calls → begins TX → calls real method → commits/rollbacks TX
```

**JDK Dynamic Proxy vs CGLIB:**
| | JDK Dynamic Proxy | CGLIB |
|--|---|---|
| Requires | Interface | No interface needed |
| How | Implements same interface, delegates | Creates subclass, overrides methods |
| Speed | Slightly faster creation | Slightly faster invocation |
| Limitation | Only proxies interface methods | Can't proxy `final` classes/methods |
| Spring default | When interface exists (Spring Boot 2.x) | **Default in Spring Boot 3.x** |

```java
// JDK proxy — works because UserService is an interface
public interface UserService { void save(User u); }

@Service
public class UserServiceImpl implements UserService {
    @Transactional
    public void save(User u) { ... }
}
// Spring creates: Proxy implements UserService → delegates to UserServiceImpl

// CGLIB proxy — no interface
@Service
public class PaymentService {  // No interface
    @Transactional
    public void processPayment(Payment p) { ... }
}
// Spring creates: PaymentService$$EnhancerByCGLIB extends PaymentService
```

**When @Transactional DOES NOT work:**
```java
@Service
public class ReturnService {
    
    @Transactional
    public void fileReturn(ReturnVO vo) { ... }  // TX works ✓
    
    public void processReturn(ReturnVO vo) {
        // PROBLEM: self-invocation bypasses proxy!
        fileReturn(vo);  // ✗ NO TRANSACTION! Calls this.fileReturn() not proxy.fileReturn()
    }
    
    // Fix 1: Inject self
    @Autowired
    private ReturnService self;  // Get the proxy
    public void processReturn(ReturnVO vo) {
        self.fileReturn(vo);  // ✓ Goes through proxy
    }
    
    // Fix 2: Extract to another service
    // Fix 3: Use AspectJ weaving (compile-time, not runtime proxy)
}

// Other cases where @Transactional doesn't work:
// 1. Private methods — proxy can't override private (CGLIB)
// 2. static methods — not intercepted
// 3. Called from constructor — proxy not ready yet
// 4. Exception swallowed in catch block — no rollback triggered
```

**GSTN codebase:** In `WFServiceImpl.java`, we see `@Transactional(propagation = Propagation.REQUIRES_NEW)` — this starts a NEW transaction even if called within an existing one. This is used for audit logging that must persist even if the main transaction rolls back.

---

### BQ2. Explain the entire lifecycle of a Spring Boot HTTP request — from Tomcat receiving the TCP packet to your controller method executing and response going back.

**Answer:**

```
Client sends HTTP request
         │
         ▼
┌─────────────────────────────┐
│ 1. TOMCAT (Embedded Server) │
│    - Accept TCP connection  │
│    - Parse HTTP request     │
│    - Create HttpServletRequest/Response │
│    - Pick thread from pool (default 200)│
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 2. FILTER CHAIN             │
│    - CharacterEncodingFilter│
│    - CorsFilter             │
│    - AuthorizationFilter ←── GSTN custom filter
│    - Spring Security filters│
│    (chain.doFilter() passes │
│     to next filter)         │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 3. DISPATCHER SERVLET       │
│    (Front Controller)       │
│    - Receives ALL requests  │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 4. HANDLER MAPPING          │
│    - URL → Controller method│
│    - Checks @RequestMapping │
│    - Returns HandlerExecutionChain │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 5. INTERCEPTORS (preHandle) │
│    - WebContentInterceptor  │
│    - LocaleInterceptor      │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 6. HANDLER ADAPTER          │
│    - Resolves method args   │
│    - @RequestParam → String │
│    - @RequestBody → Object  │
│      (Jackson deserialization)│
│    - @PathVariable → String │
│    - @Valid → runs validators│
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 7. CONTROLLER METHOD        │
│    @GetMapping("/api/returns")│
│    public Object getReturns()│
│    → calls Service (via proxy)│
│    → calls Repository (JPA) │
│    → returns ResponseEntity │
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 8. MESSAGE CONVERTER        │
│    - Object → JSON          │
│    (MappingJackson2HttpMessageConverter)│
│    - Sets Content-Type header│
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 9. INTERCEPTORS (afterCompletion)│
│ 10. FILTERS (reverse order) │
│ 11. TOMCAT writes response  │
│     to TCP socket           │
└─────────────────────────────┘
```

**GSTN flow specifically:**
```java
// Request: GET /auth/internalapi/newreturns/getanx1aData?gstin=29AAACG1234A1ZD&rtnPrd=072023

// 1. Tomcat receives on port 8080
// 2. AuthorizationFilter.doFilter() → validates auth token from header
// 3. DispatcherServlet routes to Anx1aInternalController
// 4. HandlerAdapter resolves @RequestParam gstin, rtnPrd
// 5. Controller calls Anx1aServiceImpl.getAnx1aRecords()
// 6. Service calls DistCacheUtil (Redis) or DAO (MySQL)
// 7. Response object → Jackson serializes to JSON
// 8. HTTP 200 + JSON body sent back
```

---

### BQ3. How does HikariCP connection pool work? What happens when all connections are exhausted? How do you tune it for 50K concurrent requests?

**Answer:**

**HikariCP internals:**
```
Application Thread                     HikariPool
      │                                    │
      ├── getConnection() ──────────────►  │
      │                                    ├── Check ConcurrentBag
      │                                    │   ├── ThreadLocal list (fastest)
      │                                    │   ├── Shared list (CAS)
      │                                    │   └── Handoff queue (SynchronousQueue)
      │  ◄── Connection returned ──────────┤
      │                                    │
      ├── Use connection (query)           │
      │                                    │
      ├── close() (returns to pool) ──────►│
      │                                    ├── Return to ConcurrentBag
```

**When pool is exhausted:**
```
Thread calls getConnection()
  → Pool full, all connections busy
  → Thread waits on SynchronousQueue for connectionTimeout (default 30s)
  → If timeout expires → throw SQLTransientConnectionException
  → In GSTN → filing request fails → user sees "Service temporarily unavailable"
```

**Tuning for high load:**
```yaml
# application.yml for GSTN services
spring:
  datasource:
    hikari:
      # Pool sizing (critical!)
      maximum-pool-size: 20        # Rule: connections = (CPU cores * 2) + effective_spindle_count
      minimum-idle: 10             # Pre-warmed connections
      
      # Timeouts
      connection-timeout: 10000    # 10s — fail fast, don't hang
      idle-timeout: 300000         # 5 min — return idle connections
      max-lifetime: 600000         # 10 min — recycle before DB timeout (MySQL wait_timeout=28800)
      
      # Leak detection
      leak-detection-threshold: 30000  # 30s — log warning if connection held > 30s
      
      # Validation
      connection-test-query: SELECT 1
```

**Why NOT 500 connections for 50K requests?**
- More connections ≠ faster. Database has limited CPU/IO.
- PostgreSQL formula: `connections = (CPU cores * 2) + effective_spindle_count`
- For 8-core DB server: ~20 connections is optimal
- 50K concurrent requests with 20 connections → each connection serves 2,500 requests via queueing
- If queries average 5ms → 20 connections × 200 queries/sec = 4,000 queries/sec throughput
- For more throughput → use read replicas, caching, or async processing

**GSTN config (from application-test.properties):**
```properties
bo.db.initialSize.R1=5        # initial pool size
bo.db.maxActive.R1=10         # max active connections
```

---

### BQ4. What is Spring Boot's auto-configuration order? How do @AutoConfigureBefore, @AutoConfigureAfter, and @AutoConfigureOrder work?

**Answer:**

Spring Boot auto-configuration loading:
1. Reads `META-INF/spring.factories` → list of all auto-config classes
2. Filters by `@Conditional` annotations (remove non-matching)
3. Sorts by ordering annotations
4. Processes in order

```java
// GSTN's DataSourceAutoConfig runs BEFORE Spring's default
@AutoConfigureBefore(DataSourceAutoConfiguration.class)
@ConditionalOnClass({DataSource.class, LocalContainerEntityManagerFactoryBean.class})
public class DataSourceAutoConfig implements ImportBeanDefinitionRegistrar {
    // Registers dynamic datasources BEFORE Spring tries to auto-configure one
    // This prevents "multiple DataSource bean" conflicts
}

// GSTN also uses EnvironmentPostProcessor — runs even BEFORE auto-config
org.springframework.boot.env.EnvironmentPostProcessor=\
  org.gst.framework.starter.autoconfigure.env.GstEnvironmentPostProcessor
// This modifies Environment (properties) before any bean is created
```

**Order of execution:**
```
1. EnvironmentPostProcessor (GstEnvironmentPostProcessor) — modify properties
2. @AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE) — runs first
3. @AutoConfigureBefore — runs before specified class
4. Default order (alphabetical within same priority)
5. @AutoConfigureAfter — runs after specified class
```

---

### BQ5. You mentioned multi-datasource in GSTN. How do you implement dynamic datasource routing? AbstractRoutingDataSource? How does GSTN route queries to state-specific databases?

**Answer:**

**Architecture:**
```
                    ┌─── Maharashtra DB (MH shard)
Request (GSTIN) ──► RoutingDataSource ──┼─── Karnataka DB (KA shard)
                    │                   ├─── Tamil Nadu DB (TN shard)
                    │  ThreadLocal key  └─── ... (37 shards)
                    │  determines route
```

**Implementation:**
```java
// Step 1: Create Routing DataSource
public class RoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DbContextHolder.getDbType();  // ThreadLocal value
    }
}

// Step 2: ThreadLocal context holder
public class DbContextHolder {
    private static final ThreadLocal<String> contextHolder = new ThreadLocal<>();
    
    public static void setDbType(String dbType) {
        contextHolder.set(dbType);
    }
    
    public static String getDbType() {
        return contextHolder.get();
    }
    
    public static void clearDbType() {
        contextHolder.remove();  // IMPORTANT: prevent memory leak in thread pool
    }
}

// Step 3: Service sets routing before DB call
@Service
public class WLHistoryServiceImpl implements WLHistoryService {
    @Transactional
    public Object searchWLHistoryGSTIN(SearchWLGSTNVO searchVO) {
        String stateCd = findStateCode(searchVO.getGstin());
        setDbRouting(stateCd);  // Sets ThreadLocal → routes to state-specific DB
        
        // This DB call goes to the correct state database
        return welcomeLetterDAO.getGstnDopAddrsHistEntity(gstnRefId);
    }
}

// Step 4: Auto-configuration creates routing datasource
// From DataSourceAutoConfig.java
if ("ROUTING".equalsIgnoreCase(config.getType())) {
    DataSource routingDS = dataSourceFactory.createRoutingDataSource(dbIdentifier);
    // Registers a RoutingDataSource bean with all shard datasources as targets
}
```

**GSTN uses the first 2 digits of GSTIN as state code:**
```
29AAACG1234A1ZD → State code = 29 (Karnataka) → Route to KA database
27AAACM5678B1ZP → State code = 27 (Maharashtra) → Route to MH database
```

---

### BQ6. How do you handle graceful shutdown in Spring Boot? What happens to in-flight requests?

**Answer:**

```java
// application.yml
server:
  shutdown: graceful                    # Enable graceful shutdown (Spring Boot 2.3+)
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s     # Wait up to 30s for in-flight requests

// What happens on SIGTERM:
// 1. Stop accepting NEW requests (return 503)
// 2. Wait for IN-FLIGHT requests to complete (up to 30s)
// 3. Destroy Spring beans (@PreDestroy called)
// 4. Close connection pools, Kafka producers, Redis connections
// 5. JVM shuts down

// Custom shutdown hook for GSTN services:
@Component
public class GracefulShutdown {
    
    @Autowired
    private KafkaProducer kafkaProducer;
    
    @PreDestroy
    public void onShutdown() {
        LOGGER.info("Graceful shutdown initiated");
        kafkaProducer.flush();     // Send any buffered messages
        kafkaProducer.close();     // Close Kafka producer
        // HikariCP auto-closes via Spring bean lifecycle
    }
}
```

**K8s integration:**
```yaml
# K8s sends SIGTERM → pod has terminationGracePeriodSeconds to finish
spec:
  terminationGracePeriodSeconds: 45  # Must be > Spring's timeout-per-shutdown-phase
  containers:
    - name: filing-service
      lifecycle:
        preStop:
          exec:
            command: ["sh", "-c", "sleep 5"]  # Wait for LB to deregister
```

---

## PART C: SYSTEM DESIGN — RECENTLY ASKED (Amazon, Google, Uber, Flipkart, Razorpay)

---

### CQ1. Design a distributed rate limiter that works across multiple service instances (Asked at Razorpay, Stripe, PhonePe)

**Answer:**

**Requirements:**
- Rate limit per API key / per user: 100 requests/minute
- Must work across 10 service instances (not just per-instance)
- Low latency (< 5ms overhead per request)
- Handle burst traffic (GSTN filing deadline)

**Approach: Sliding Window Counter with Redis**

```
┌──────────────────────────────────────────┐
│              Redis Cluster               │
│                                          │
│  Key: rate:{userId}:{minute}             │
│  Value: count (atomic increment)         │
│  TTL: 60 seconds (auto-cleanup)          │
│                                          │
│  For sliding window:                     │
│  Key: rate:{userId}                      │
│  Type: Sorted Set (score = timestamp)    │
└──────────────────────────────────────────┘
         ▲              ▲              ▲
         │              │              │
    Instance 1     Instance 2     Instance 3
```

**Implementation (Token Bucket with Redis):**
```java
@Component
public class DistributedRateLimiter {
    
    @Autowired
    private RedisTemplate<String, String> redis;
    
    // Lua script for atomic check-and-increment
    private static final String LUA_SCRIPT = """
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        
        local current = redis.call('INCR', key)
        if current == 1 then
            redis.call('EXPIRE', key, window)
        end
        
        if current > limit then
            return 0  -- rate limited
        end
        return 1  -- allowed
    """;
    
    public boolean isAllowed(String userId, int limit, int windowSeconds) {
        String key = "rate:" + userId + ":" + (System.currentTimeMillis() / (windowSeconds * 1000));
        Long result = redis.execute(new DefaultRedisScript<>(LUA_SCRIPT, Long.class),
            List.of(key), String.valueOf(limit), String.valueOf(windowSeconds));
        return result != null && result == 1;
    }
}

// Usage in Filter/Interceptor:
@Component
public class RateLimitFilter implements Filter {
    @Autowired
    private DistributedRateLimiter rateLimiter;
    
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        String apiKey = ((HttpServletRequest) req).getHeader("X-API-Key");
        if (!rateLimiter.isAllowed(apiKey, 100, 60)) {  // 100 req/min
            ((HttpServletResponse) res).setStatus(429);  // Too Many Requests
            return;
        }
        chain.doFilter(req, res);
    }
}
```

**Algorithms comparison:**
| Algorithm | Pros | Cons | Best For |
|-----------|------|------|----------|
| Fixed Window | Simple, O(1) | Burst at window edges | Basic rate limiting |
| Sliding Window Log | Accurate | Memory-heavy (store all timestamps) | Small limits |
| Sliding Window Counter | Balanced | Approximate | **GSTN API rate limiting** |
| Token Bucket | Allows bursts | Slightly complex | API gateways |
| Leaky Bucket | Smooth output | No burst allowed | Stream processing |

---

### CQ2. Design an idempotent payment system (Asked at Razorpay, PhonePe, Stripe, Goldman Sachs)

**Answer:**

**Problem:** Network failure after payment processed but before response → client retries → double charge.

**Architecture:**
```
Client                    API Gateway              Payment Service            Bank API
  │                           │                         │                       │
  ├── POST /pay               │                         │                       │
  │   Idempotency-Key: abc123 │                         │                       │
  │   ─────────────────────►  │                         │                       │
  │                           ├── Forward ──────────►   │                       │
  │                           │                         ├── Check Redis         │
  │                           │                         │   Key: idemp:abc123   │
  │                           │                         │   Not found → proceed │
  │                           │                         │                       │
  │                           │                         ├── BEGIN TX            │
  │                           │                         │   INSERT payment      │
  │                           │                         │   INSERT outbox event │
  │                           │                         ├── COMMIT TX           │
  │                           │                         │                       │
  │                           │                         ├── Call bank ─────────►│
  │                           │                         │                       │
  │              ◄── TIMEOUT ──┤                        │  ◄── Success ────────┤
  │   (no response received)  │                         │                       │
  │                           │                         ├── Update status=DONE  │
  │                           │                         ├── Set Redis idemp:abc123 = response
  │                           │                         │                       │
  │── RETRY POST /pay         │                         │                       │
  │   Idempotency-Key: abc123 │                         │                       │
  │   ─────────────────────►  ├── Forward ──────────►   │                       │
  │                           │                         ├── Check Redis         │
  │                           │                         │   Key: idemp:abc123   │
  │                           │                         │   FOUND → return cached response
  │              ◄── 200 OK ──┤  ◄── Cached response ──┤                       │
```

```java
@Service
public class PaymentService {
    
    @Autowired
    private DistCacheUtil distCacheUtil;  // Redis
    
    @Autowired
    private PaymentRepository paymentRepo;
    
    public PaymentResponse processPayment(String idempotencyKey, PaymentRequest req) {
        // Step 1: Check if already processed
        PaymentResponse cached = distCacheUtil.getPaymentResponse(idempotencyKey);
        if (cached != null) {
            return cached;  // Idempotent — return same response
        }
        
        // Step 2: Acquire distributed lock to prevent concurrent duplicates
        boolean locked = distCacheUtil.acquireLock("lock:pay:" + idempotencyKey, 30);
        if (!locked) {
            throw new ConflictException("Payment in progress");
        }
        
        try {
            // Step 3: Double-check after lock
            cached = distCacheUtil.getPaymentResponse(idempotencyKey);
            if (cached != null) return cached;
            
            // Step 4: Process payment
            PaymentEntity payment = createPayment(req);
            paymentRepo.save(payment);
            
            PaymentResponse response = callBankAPI(payment);
            
            // Step 5: Cache response for idempotency (TTL = 24 hours)
            distCacheUtil.setPaymentResponse(idempotencyKey, response, 86400);
            
            return response;
        } finally {
            distCacheUtil.releaseLock("lock:pay:" + idempotencyKey);
        }
    }
}
```

---

### CQ3. Design a notification system that sends 10 million notifications during GSTN filing deadline (Asked at Swiggy, Flipkart, Amazon)

**Answer:**

```
                              ┌─────────────────────┐
                              │   Notification API   │
                              │  (accepts requests)  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   Kafka Topic:       │
                              │   notification-events│
                              │   (50 partitions)    │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │  Email Worker    │  │  SMS Worker      │  │  Push Worker    │
          │  Consumer Group  │  │  Consumer Group   │  │  Consumer Group │
          │  (10 instances)  │  │  (10 instances)   │  │  (5 instances)  │
          └────────┬────────┘  └────────┬─────────┘  └────────┬────────┘
                   ▼                    ▼                      ▼
            SMTP Gateway          SMS Provider            FCM/APNs
            (SES/SendGrid)        (Twilio/MSG91)          (Firebase)

Deduplication: Redis SET — "sent:{userId}:{notifId}" with TTL
Retry: Failed → retry topic (3 retries with exponential backoff) → DLQ
Rate limiting: Per-provider rate limit (SES: 50/sec, SMS: 10/sec)
Priority: P0 (OTP) > P1 (filing deadline) > P2 (marketing)
```

**Key design decisions:**
- **Fan-out:** Single notification event → multiple channels (email + SMS + push)
- **Template engine:** Notification templates in DB, parameterized with user data
- **Scheduling:** For deadline reminders, use Kafka delayed topics or separate scheduler
- **Tracking:** Each notification gets UUID, track status (QUEUED → SENT → DELIVERED → READ)
- **User preferences:** Check DND, channel preference before sending

---

## PART D: LOW-LEVEL DESIGN (LLD) — Asked at Amazon, Microsoft, Atlassian, Flipkart

---

### DQ1. Design a parking lot system (Classic LLD — still asked in 2025-2026)

**Answer:**

```java
// Enums
enum VehicleType { MOTORCYCLE, CAR, TRUCK }
enum SpotType { SMALL, MEDIUM, LARGE }
enum TicketStatus { ACTIVE, PAID }

// Core entities
class Vehicle {
    private String licensePlate;
    private VehicleType type;
}

class ParkingSpot {
    private int spotId;
    private int floor;
    private SpotType type;
    private boolean isAvailable;
    private Vehicle parkedVehicle;
    
    public boolean canFit(Vehicle vehicle) {
        return switch (vehicle.getType()) {
            case MOTORCYCLE -> true;  // fits anywhere
            case CAR -> type != SpotType.SMALL;
            case TRUCK -> type == SpotType.LARGE;
        };
    }
    
    public synchronized boolean park(Vehicle vehicle) {
        if (!isAvailable || !canFit(vehicle)) return false;
        this.parkedVehicle = vehicle;
        this.isAvailable = false;
        return true;
    }
    
    public synchronized Vehicle unpark() {
        Vehicle v = this.parkedVehicle;
        this.parkedVehicle = null;
        this.isAvailable = true;
        return v;
    }
}

class ParkingTicket {
    private String ticketId;
    private Vehicle vehicle;
    private ParkingSpot spot;
    private LocalDateTime entryTime;
    private LocalDateTime exitTime;
    private TicketStatus status;
    private double amount;
}

// Strategy pattern for pricing
interface PricingStrategy {
    double calculate(ParkingTicket ticket);
}

class HourlyPricingStrategy implements PricingStrategy {
    private Map<VehicleType, Double> ratePerHour;
    
    public double calculate(ParkingTicket ticket) {
        long hours = ChronoUnit.HOURS.between(ticket.getEntryTime(), ticket.getExitTime());
        hours = Math.max(1, hours);  // minimum 1 hour
        return hours * ratePerHour.get(ticket.getVehicle().getType());
    }
}

// Main service
class ParkingLot {
    private List<List<ParkingSpot>> floors;  // floor → spots
    private Map<String, ParkingTicket> activeTickets;  // ticketId → ticket
    private PricingStrategy pricingStrategy;
    
    // Strategy: find nearest available spot
    public ParkingTicket parkVehicle(Vehicle vehicle) {
        for (List<ParkingSpot> floor : floors) {
            for (ParkingSpot spot : floor) {
                if (spot.park(vehicle)) {
                    ParkingTicket ticket = new ParkingTicket(vehicle, spot);
                    activeTickets.put(ticket.getTicketId(), ticket);
                    return ticket;
                }
            }
        }
        throw new ParkingFullException("No spots available");
    }
    
    public double unparkVehicle(String ticketId) {
        ParkingTicket ticket = activeTickets.remove(ticketId);
        ticket.setExitTime(LocalDateTime.now());
        ticket.getSpot().unpark();
        return pricingStrategy.calculate(ticket);
    }
}
```

**Design patterns used:** Strategy (pricing), Observer (notify when spot freed), Singleton (ParkingLot instance)

---

### DQ2. Design a Logger/Logging framework (Asked at Uber, Atlassian, Microsoft)

**Answer:**

```java
// Log levels
enum LogLevel { TRACE, DEBUG, INFO, WARN, ERROR, FATAL;
    public boolean isEnabled(LogLevel threshold) {
        return this.ordinal() >= threshold.ordinal();
    }
}

// Sink interface — Strategy pattern
interface LogSink {
    void write(LogMessage message);
}

class ConsoleSink implements LogSink {
    public void write(LogMessage msg) {
        System.out.println(format(msg));
    }
}

class FileSink implements LogSink {
    private BufferedWriter writer;
    private long maxFileSize;
    private int maxFiles;  // rotation
    
    public synchronized void write(LogMessage msg) {
        writer.write(format(msg));
        if (currentFileSize > maxFileSize) {
            rotate();  // file.log → file.log.1, create new file.log
        }
    }
}

class AsyncSink implements LogSink {
    private BlockingQueue<LogMessage> queue;
    private LogSink delegate;
    
    public AsyncSink(LogSink delegate, int queueSize) {
        this.queue = new ArrayBlockingQueue<>(queueSize);
        this.delegate = delegate;
        // Background thread drains queue
        new Thread(() -> {
            while (true) {
                delegate.write(queue.take());
            }
        }).start();
    }
    
    public void write(LogMessage msg) {
        if (!queue.offer(msg)) {
            // Queue full — drop or write synchronously (configurable)
        }
    }
}

// Log message
@Builder
class LogMessage {
    private LogLevel level;
    private String message;
    private String loggerName;
    private long timestamp;
    private String threadName;
    private Map<String, String> mdc;  // MDC context
    private Throwable exception;
}

// Logger
class Logger {
    private String name;
    private LogLevel threshold;
    private List<LogSink> sinks;
    
    public void info(String msg, Object... args) {
        if (LogLevel.INFO.isEnabled(threshold)) {
            LogMessage logMsg = LogMessage.builder()
                .level(LogLevel.INFO)
                .message(String.format(msg, args))
                .loggerName(name)
                .timestamp(System.currentTimeMillis())
                .threadName(Thread.currentThread().getName())
                .mdc(MDC.getCopyOfContextMap())
                .build();
            sinks.forEach(sink -> sink.write(logMsg));
        }
    }
}

// Logger Factory — typical usage
class LoggerFactory {
    private static final Map<String, Logger> loggers = new ConcurrentHashMap<>();
    
    public static Logger getLogger(Class<?> clazz) {
        return loggers.computeIfAbsent(clazz.getName(), 
            name -> new Logger(name, loadConfig(name)));
    }
}

// GSTN uses this exact pattern:
private static final Logger LOGGER = LoggerFactory.getLogger(Anx1aServiceImpl.class);
LOGGER.info("Entering getAnx1aData at {}", System.currentTimeMillis());
```

---

## PART E: CONCURRENCY & MULTITHREADING DEEP DIVE (Amazon, Google, Goldman Sachs, Morgan Stanley)

---

### EQ1. Implement a thread-safe bounded blocking queue (without using java.util.concurrent)

**Answer:**

```java
public class BoundedBlockingQueue<T> {
    private final Object[] items;
    private int head, tail, count;
    private final Object lock = new Object();
    
    public BoundedBlockingQueue(int capacity) {
        items = new Object[capacity];
    }
    
    public void put(T item) throws InterruptedException {
        synchronized (lock) {
            while (count == items.length) {
                lock.wait();  // Queue full — wait for consumer
            }
            items[tail] = item;
            tail = (tail + 1) % items.length;  // circular buffer
            count++;
            lock.notifyAll();  // Wake up waiting consumers
        }
    }
    
    @SuppressWarnings("unchecked")
    public T take() throws InterruptedException {
        synchronized (lock) {
            while (count == 0) {
                lock.wait();  // Queue empty — wait for producer
            }
            T item = (T) items[head];
            items[head] = null;  // Help GC
            head = (head + 1) % items.length;
            count--;
            lock.notifyAll();  // Wake up waiting producers
            return item;
        }
    }
    
    public int size() {
        synchronized (lock) {
            return count;
        }
    }
}
```

**Follow-ups typically asked:**
- Use `ReentrantLock` + `Condition` instead of `synchronized` (separate conditions for notFull and notEmpty)
- Make it work with timeout (timed wait)
- How does `ArrayBlockingQueue` differ? (uses ReentrantLock, fair/unfair option)

---

### EQ2. What is the ABA problem in CAS (Compare-And-Swap)? How does Java solve it?

**Answer:**

**ABA problem:**
```
Thread 1: Read value = A
Thread 1: (preempted)
Thread 2: Change A → B → A  (value is A again, but state changed!)
Thread 1: CAS(expected=A, new=C) → SUCCEEDS (shouldn't!)
```

**Example:** Lock-free stack. Thread 1 reads top=A. Thread 2 pops A, pops B, pushes A back. Thread 1's CAS succeeds, but B is now lost.

**Java solution: `AtomicStampedReference`**
```java
AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 0);

// Read with stamp
int[] stampHolder = new int[1];
String current = ref.get(stampHolder);  // current = "A", stamp = 0

// CAS checks BOTH value AND stamp
ref.compareAndSet("A", "C", 0, 1);  // Only succeeds if value=A AND stamp=0

// If another thread changed A→B→A, stamp would be 2, so CAS fails
```

---

### EQ3. Implement a simple ReadWriteLock. When would you use it over synchronized?

**Answer:**

```java
public class SimpleReadWriteLock {
    private int readers = 0;
    private boolean writerActive = false;
    private int waitingWriters = 0;
    
    public synchronized void lockRead() throws InterruptedException {
        while (writerActive || waitingWriters > 0) {
            wait();  // Writer preference to prevent writer starvation
        }
        readers++;
    }
    
    public synchronized void unlockRead() {
        readers--;
        if (readers == 0) notifyAll();
    }
    
    public synchronized void lockWrite() throws InterruptedException {
        waitingWriters++;
        while (readers > 0 || writerActive) {
            wait();
        }
        waitingWriters--;
        writerActive = true;
    }
    
    public synchronized void unlockWrite() {
        writerActive = false;
        notifyAll();
    }
}
```

**Use over synchronized when:** Read-heavy workloads (90%+ reads). Example: GSTN's reference data (state codes, HSN codes) — updated rarely, read by every request. Multiple readers can proceed concurrently with ReadWriteLock vs one at a time with synchronized.

---

## PART F: RECENTLY TRENDING QUESTIONS (2025-2026 SDE-2/SDE-3 Interviews)

---

### FQ1. Explain observability — metrics, logs, traces. How do you set up monitoring for a microservice?

**Answer:**

**Three Pillars:**
```
1. LOGS — What happened (discrete events)
   SLF4J + Logback → ELK Stack (Elasticsearch + Logstash + Kibana)
   MDC for request correlation: MDC.put("requestId", uuid)

2. METRICS — How much / how fast (aggregated numbers)
   Micrometer → Prometheus → Grafana
   - Counter: request_total (always increasing)
   - Gauge: active_connections (goes up and down)
   - Histogram: request_duration_seconds (distribution)
   - Timer: api_response_time (count + total time)

3. TRACES — The journey of a request across services
   OpenTelemetry → Jaeger/Zipkin
   - Trace = entire request journey
   - Span = one service's contribution
   - TraceId propagated via HTTP header
```

**Spring Boot setup:**
```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health, metrics, prometheus, info
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: gstn-filing-service
      environment: production
```

```java
// Custom business metric
@Service
public class ReturnService {
    private final Counter filingCounter;
    private final Timer filingTimer;
    
    public ReturnService(MeterRegistry registry) {
        this.filingCounter = Counter.builder("gstn.returns.filed")
            .tag("type", "GSTR1")
            .register(registry);
        this.filingTimer = Timer.builder("gstn.returns.filing.duration")
            .register(registry);
    }
    
    public void fileReturn(ReturnVO vo) {
        filingTimer.record(() -> {
            // Business logic
            filingCounter.increment();
        });
    }
}
```

**GSTN Actuator config (from application-prod.yml):**
```yaml
# Swagger disabled in prod, but actuator health exposed
springdoc:
  api-docs:
    enabled: false
  swagger-ui:
    enabled: false
```

---

### FQ2. What is database connection leak? How do you detect and prevent it? (Asked at Amazon, Flipkart)

**Answer:**

**Connection leak:** Application gets a connection from pool but never returns it (missing `close()` or exception before close).

**Symptoms:**
- Pool exhaustion → `ConnectionTimeoutException` after some time
- Active connections keep increasing, never decrease
- Application hangs under load

**Detection with HikariCP:**
```yaml
spring:
  datasource:
    hikari:
      leak-detection-threshold: 30000  # Log WARNING if connection held > 30s
      # HikariCP logs: "Connection leak detection triggered for {connection}"
      # with full stack trace showing WHERE the connection was acquired
```

**Prevention:**
```java
// BAD — connection leaked if exception thrown between get and close
Connection conn = dataSource.getConnection();
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT ...");
// If exception here → conn never closed!
conn.close();

// GOOD — try-with-resources (Java 7+)
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement("SELECT ...");
     ResultSet rs = stmt.executeQuery()) {
    // Process results
}  // Auto-closed even if exception — implements AutoCloseable

// BEST — Use Spring JDBC/JPA
// Spring manages connections automatically via @Transactional
// Connection acquired at TX start, returned at TX end
@Transactional
public List<Return> getReturns(String gstin) {
    return returnRepository.findByGstin(gstin);  // Spring handles everything
}
```

**GSTN context:** Our services use `@Transactional` on service methods, which ensures Spring manages connection lifecycle. Connection pooling via HikariCP with `maxActive=10` prevents runaway connection acquisition.

---

### FQ3. How do you prevent and handle distributed deadlocks across microservices? (Asked at Uber, Amazon)

**Answer:**

**Distributed deadlock scenario:**
```
Service A: Lock resource X, then needs resource Y
Service B: Lock resource Y, then needs resource X
→ Both waiting forever (deadlock!)
```

**Prevention strategies:**

1. **Lock ordering:** Always acquire locks in the same global order
```java
// Always lock by sorted resource ID
public void transferFunds(String fromAccount, String toAccount) {
    String first = fromAccount.compareTo(toAccount) < 0 ? fromAccount : toAccount;
    String second = fromAccount.compareTo(toAccount) < 0 ? toAccount : fromAccount;
    
    redis.lock("account:" + first);   // Always lock smaller ID first
    redis.lock("account:" + second);
    try {
        // Transfer logic
    } finally {
        redis.unlock("account:" + second);
        redis.unlock("account:" + first);
    }
}
```

2. **Lock timeout:** Never wait indefinitely
```java
boolean locked = redis.tryLock("resource:X", 5, TimeUnit.SECONDS);
if (!locked) {
    throw new ResourceBusyException("Could not acquire lock, retry later");
}
```

3. **Saga pattern:** Don't hold locks across services — use compensating transactions
```
Filing Service → Payment Service → Acknowledgment Service
   (if payment fails → compensate: undo filing)
```

4. **Deadlock detection:** Graph-based detection (wait-for graph), detect cycles, abort one participant.

---

### FQ4. What's the difference between optimistic and pessimistic concurrency control? When to use each? (Asked at every company)

**Answer:**

| | Optimistic | Pessimistic |
|--|---|---|
| Assumption | Conflicts are rare | Conflicts are frequent |
| Mechanism | Version check at commit time | Lock at read time |
| JPA annotation | `@Version` | `@Lock(LockModeType.PESSIMISTIC_WRITE)` |
| Blocking | No blocking | Blocks other threads |
| Best for | Read-heavy, low contention | Write-heavy, high contention |
| Failure mode | `OptimisticLockException` → retry | Deadlock possible |

```java
// OPTIMISTIC — GSTN return filing (concurrent unlikely for same return)
@Entity
public class GSTReturn {
    @Id
    private Long id;
    
    @Version  // Hibernate auto-manages this
    private Integer version;
    
    private String gstin;
    private String status;
}

// When two threads update same return:
// Thread 1: reads version=1, updates, saves → version becomes 2 ✓
// Thread 2: reads version=1, updates, saves → version mismatch → OptimisticLockException!
// Thread 2 must retry with fresh data

// PESSIMISTIC — GSTN payment processing (money involved, no retries)
@Repository
public interface PaymentRepository extends JpaRepository<Payment, Long> {
    
    @Lock(LockModeType.PESSIMISTIC_WRITE)  // SELECT ... FOR UPDATE
    @Query("SELECT p FROM Payment p WHERE p.paymentId = :id")
    Payment findByIdForUpdate(@Param("id") Long id);
}

// Thread 1: SELECT FOR UPDATE → row LOCKED in DB
// Thread 2: SELECT FOR UPDATE → BLOCKS until Thread 1 commits/rollbacks
// No lost updates, no retries, but lower throughput
```

**GSTN recommendation:** 
- Filing status update → **Optimistic** (conflict rare, easy retry)
- Payment ledger update → **Pessimistic** (money-critical, must be correct)

---

### FQ5. Explain how Spring Boot handles circular dependencies. Why is it a design smell? (Asked at Atlassian, Microsoft)

**Answer:**

**Circular dependency:** Bean A needs Bean B, Bean B needs Bean A.
```java
@Service
public class OrderService {
    @Autowired
    private PaymentService paymentService;  // OrderService → PaymentService
}

@Service
public class PaymentService {
    @Autowired
    private OrderService orderService;  // PaymentService → OrderService ← CIRCULAR!
}
```

**Spring Boot behavior:**
- **Spring Boot 2.5 and earlier:** Allowed with field injection (resolved via three-level cache: singletonObjects, earlySingletonObjects, singletonFactories)
- **Spring Boot 2.6+:** **Throws error by default!** Must explicitly allow with `spring.main.allow-circular-references=true`
- **Constructor injection:** Always fails (cannot create either bean without the other)

**Three-level cache (how Spring solved it):**
```
1. singletonObjects       — fully initialized beans
2. earlySingletonObjects   — partially initialized (constructor done, not injected)
3. singletonFactories      — factory to create early reference

Steps:
1. Create A (call constructor) → put A-factory in level 3
2. A needs B → create B
3. B needs A → find A-factory in level 3 → get early A reference
4. B fully initialized → move B to level 1
5. A injection completed → move A to level 1
```

**How to fix (proper way):**
```java
// Option 1: Redesign — extract shared logic
@Service
public class OrderPaymentMediator {
    @Autowired private OrderRepository orderRepo;
    @Autowired private PaymentRepository paymentRepo;
    // Both services depend on mediator, not each other
}

// Option 2: Event-driven — decouple via events
@Service
public class OrderService {
    @Autowired private ApplicationEventPublisher publisher;
    
    public void createOrder(OrderVO vo) {
        // Create order
        publisher.publishEvent(new OrderCreatedEvent(order));
    }
}

@Service
public class PaymentService {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        processPayment(event.getOrder());
    }
}

// Option 3: @Lazy (quick fix, not ideal)
@Service
public class OrderService {
    @Autowired
    @Lazy  // Creates proxy, resolves actual bean on first use
    private PaymentService paymentService;
}
```

---

### FQ6. What is API idempotency and how do you implement it in REST APIs? (Every fintech interview)

**Answer:**

```java
// Standard approach: Idempotency-Key header

@RestController
public class FilingController {
    
    @Autowired
    private DistCacheUtil distCacheUtil;
    
    @PostMapping("/api/returns/file")
    public ResponseEntity<FilingResponse> fileReturn(
            @RequestHeader("Idempotency-Key") String idempotencyKey,
            @RequestBody ReturnVO returnVO) {
        
        // 1. Check if this key was already processed
        String cachedResponse = distCacheUtil.get("idemp:" + idempotencyKey);
        if (cachedResponse != null) {
            return ResponseEntity.ok(deserialize(cachedResponse));  // Same response
        }
        
        // 2. Process request
        FilingResponse response = filingService.fileReturn(returnVO);
        
        // 3. Cache response keyed by idempotency key (TTL 24h)
        distCacheUtil.set("idemp:" + idempotencyKey, serialize(response), 86400);
        
        return ResponseEntity.status(201).body(response);
    }
}

// HTTP methods and idempotency:
// GET     — naturally idempotent (read-only)
// PUT     — naturally idempotent (same input → same state)
// DELETE  — naturally idempotent (delete once or many times → result is deleted)
// POST    — NOT idempotent — needs Idempotency-Key
// PATCH   — depends on implementation
```

---

### FQ7. What is back-pressure? How do you implement it in different contexts? (Amazon, Uber)

**Answer:**

**Back-pressure:** When a downstream system is slower than upstream, signal upstream to slow down.

```
Producer (1000 msg/s) → Consumer (100 msg/s) → Consumer overwhelmed without back-pressure!
```

**Implementation by context:**

```java
// 1. Kafka: Consumer controls its own pace (pull model = natural back-pressure)
consumer.poll(Duration.ofMillis(100));
// Consumer only fetches when ready — Kafka retains messages on broker

// 2. Reactive Streams (Spring WebFlux): Subscriber requests N items
Flux.range(1, 1000000)
    .onBackpressureBuffer(1000)     // Buffer up to 1000
    .onBackpressureDrop()           // Drop if buffer full
    .subscribe(item -> process(item));

// 3. Thread pool: Reject new tasks when queue full
ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
executor.setCorePoolSize(5);
executor.setMaxPoolSize(10);
executor.setQueueCapacity(100);
executor.setRejectedExecutionHandler(new CallerRunsPolicy());
// CallerRunsPolicy → caller thread runs the task → naturally slows down producer

// 4. HTTP API: Return 429 Too Many Requests
if (rateLimiter.isOverLimit()) {
    return ResponseEntity.status(429)
        .header("Retry-After", "60")  // Tell client to wait
        .build();
}

// 5. Circuit Breaker: Stop sending requests to failing service
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest req) {
    return restTemplate.postForObject(PAYMENT_URL, req, PaymentResponse.class);
}
```

---

### FQ8. How do you handle database schema migration in a zero-downtime deployment? (Asked at Flipkart, Razorpay, Atlassian)

**Answer:**

**Rule: Schema changes must be backward-compatible during deployment.**

```
Old code (v1)  ──────►  Rolling deployment  ──────►  New code (v2)
    ▲                        ▲                           ▲
    │                   Both versions                    │
    │                   running together                 │
    └──── Must work with ────┘                          │
          old AND new schema                            │
```

**Safe migration strategy (expand-contract):**

```sql
-- Phase 1: EXPAND (add new column, don't remove old)
-- Deploy: Migration V1 runs
ALTER TABLE gst_returns ADD COLUMN filing_status_new VARCHAR(20);
-- Both v1 and v2 code work — v1 ignores new column, v2 writes to both

-- Phase 2: MIGRATE DATA (backfill)
UPDATE gst_returns SET filing_status_new = filing_status WHERE filing_status_new IS NULL;

-- Phase 3: CONTRACT (remove old column — only after ALL instances on v2)
ALTER TABLE gst_returns DROP COLUMN filing_status;
ALTER TABLE gst_returns RENAME COLUMN filing_status_new TO filing_status;
```

**Flyway integration in GSTN:**
```
resources/
├── db/migration/
│   ├── V1__create_return_table.sql
│   ├── V2__add_filing_status.sql         ← Phase 1
│   ├── V3__backfill_filing_status.sql    ← Phase 2
│   └── V4__cleanup_old_column.sql        ← Phase 3 (separate release)
```

**Dangerous operations (avoid during zero-downtime):**
- Renaming columns (old code can't find old name)
- Dropping columns (old code fails)
- Adding NOT NULL without default (old code inserts fail)
- Changing column type (incompatible data)

---

### FQ9. What is the Outbox Pattern and why is it important? How does it solve the dual-write problem? (Every system design round)

**Answer:**

**Dual-write problem:**
```java
// BAD — dual write
public void fileReturn(ReturnVO vo) {
    returnRepository.save(entity);              // Write 1: Database ✓
    kafkaProducer.send("return-filed", event);  // Write 2: Kafka
    // What if Kafka fails? DB has data, Kafka doesn't → INCONSISTENT
    // What if DB fails after Kafka send? Kafka has event, DB doesn't → INCONSISTENT
}
```

**Outbox pattern solution:**
```java
// GOOD — single write to DB (atomic), separate publisher reads outbox
@Transactional
public void fileReturn(ReturnVO vo) {
    // Both writes in SAME transaction → atomic
    returnRepository.save(entity);
    
    OutboxEvent outbox = new OutboxEvent();
    outbox.setAggregateType("Return");
    outbox.setAggregateId(vo.getGstin());
    outbox.setType("RETURN_FILED");
    outbox.setPayload(toJson(vo));
    outboxRepository.save(outbox);
    // COMMIT → both saved or both rolled back
}

// Separate process reads outbox and publishes to Kafka
// Option A: Polling publisher (simple)
@Scheduled(fixedDelay = 500)
public void publishOutboxEvents() {
    List<OutboxEvent> events = outboxRepo.findUnpublished();
    for (OutboxEvent event : events) {
        kafkaProducer.send(event.getType(), event.getPayload());
        event.setPublished(true);
        outboxRepo.save(event);
    }
}

// Option B: CDC (Change Data Capture) — Debezium reads DB binlog
// Debezium → reads MySQL binlog → publishes to Kafka → no polling needed
```

**Why not just use @TransactionalEventListener?**
```java
// This is in-process — if app crashes between DB commit and event publish, event is lost
@TransactionalEventListener(phase = AFTER_COMMIT)
public void onReturnFiled(ReturnFiledEvent event) {
    kafkaProducer.send(...);  // If app crashes here → lost!
}
```

The outbox pattern persists the intent to publish, so even if the app crashes, the event will be published when the app restarts.

---

### FQ10. You have a Spring Boot service with 99th percentile latency of 5 seconds. Walk through your debugging approach. (Asked at every SDE-2+ round)

**Answer:**

**Systematic debugging approach:**

```
Step 1: WHERE is the time spent? (Latency breakdown)
─────────────────────────────────────────────────────
Request → Filter (5ms) → Controller (2ms) → Service (4800ms!) → Response (3ms)
                                                 │
                                    ├── DB Query 1: 2000ms ← SLOW QUERY
                                    ├── External API call: 2500ms ← TIMEOUT
                                    └── Business logic: 300ms ← OK

Tools: Distributed tracing (Jaeger span breakdown)
       Spring Boot Actuator /metrics (http.server.requests.percentile)
       APM tools (New Relic, Datadog)

Step 2: Is it the DATABASE?
─────────────────────────
☐ Check slow query log (MySQL: SET GLOBAL slow_query_log=ON)
☐ EXPLAIN ANALYZE the suspicious query
☐ Check if index is missing or not being used
☐ Check connection pool metrics (HikariCP active/idle/waiting)
☐ Check if N+1 query problem (Hibernate logs: hibernate.show_sql=true)

Step 3: Is it an EXTERNAL SERVICE?
─────────────────────────────────
☐ Check circuit breaker state (is it open?)
☐ Check timeout configuration (default RestTemplate = no timeout!)
☐ Check if downstream service is slow (its metrics)
☐ Add timeout: restTemplate.setConnectTimeout(3000); restTemplate.setReadTimeout(5000);

Step 4: Is it GARBAGE COLLECTION?
───────────────────────────────
☐ Check GC logs: grep "pause" gc.log
☐ If Full GC > 1s → heap tuning needed
☐ Check heap usage trend (Grafana)
☐ Take heap dump if OOM suspected

Step 5: Is it THREAD CONTENTION?
──────────────────────────────
☐ Thread dump: jstack <PID>
☐ Look for BLOCKED threads (deadlock or contention)
☐ Check synchronized blocks holding for too long
☐ Check thread pool exhaustion (Tomcat 200 threads all busy)

Step 6: Is it the NETWORK?
─────────────────────────
☐ Latency between pods (K8s service mesh metrics)
☐ DNS resolution time
☐ Connection reuse (keep-alive vs new connection per request)
```

```java
// Quick win: Add logging to pinpoint bottleneck
@Service
public class ReturnService {
    public ReturnResponse getReturn(String gstin) {
        long start = System.currentTimeMillis();
        
        // DB call
        long dbStart = System.currentTimeMillis();
        ReturnEntity entity = returnRepo.findByGstin(gstin);
        LOGGER.info("DB query took {}ms", System.currentTimeMillis() - dbStart);
        
        // External call
        long apiStart = System.currentTimeMillis();
        ValidationResult result = validationService.validate(entity);
        LOGGER.info("Validation API took {}ms", System.currentTimeMillis() - apiStart);
        
        LOGGER.info("Total service time: {}ms", System.currentTimeMillis() - start);
        return buildResponse(entity, result);
    }
}
```

---

## PART G: BEHAVIORAL QUESTIONS — SDE-2/SDE-3 SPECIFIC (Every Company)

---

### GQ1. Tell me about a time you had to make a critical architectural decision. What trade-offs did you evaluate?

**GSTN-based answer:**

"When we were migrating GSTN services from Spring Framework 4.3 to Spring Boot 2.x, I had to decide the migration strategy. The trade-offs were:

**Option A: Big-bang migration** — Migrate everything at once. Pro: clean break. Con: high risk, everything could break simultaneously during filing season.

**Option B: Strangler Fig pattern** — Migrate service by service. Pro: lower risk, progressive. Con: need to maintain both old and new systems temporarily, inter-service compatibility.

I chose Option B. We created the `gst-spring-boot2-starter` as a shared foundation that standardized auto-configuration for datasources, security, Kafka, and logging. This allowed each team to migrate independently while the starter ensured consistency.

The key trade-off was: we needed to maintain backward compatibility in our shared `Commons/` framework libraries — they had to work with BOTH Spring 4.3 (old services) and Spring Boot 2.x (new services) during the transition period. This meant we couldn't use Spring Boot-specific features in the shared libraries until all consumers migrated."

---

### GQ2. Tell me about a time you improved the performance of a system significantly.

**GSTN-based answer:**

"During the GSTR-1 filing deadline, our return retrieval API was hitting 3-second response times. I profiled the flow:

1. **Root cause:** Each API call was making 12 separate database queries (N+1 problem) — fetching return header, then individual items, then amendments.

2. **Solution:** 
   - Added `JOIN FETCH` to load related data in a single query
   - Implemented Redis caching in `DistCacheUtil` for frequently accessed reference data (HSN codes, state codes)
   - Changed the return data fetching from HBase to a batch read
   
3. **Result:** Response time dropped from 3s to 200ms — 15x improvement. We could handle the filing deadline surge without adding more instances.

The key learning: always profile before optimizing. My initial guess was network latency, but profiling showed it was all database round-trips."

---

### GQ3. How do you handle disagreements in code reviews?

**Answer:**

"In GSTN, a colleague used field injection (`@Autowired`) everywhere while I advocated for constructor injection. Instead of blocking the PR, I:

1. Shared the Spring team's own recommendation (constructor injection for required dependencies)
2. Showed concrete issues: field injection makes unit testing harder — you can't create the object without reflection or Spring context
3. Proposed a compromise: new code uses constructor injection, existing code migrates gradually
4. Created a team ADR (Architecture Decision Record) documenting the decision

The colleague agreed after seeing the testing benefit. Key principle: critique the code, not the person, and always show evidence over opinion."

---

### GQ4. Describe your approach to mentoring junior developers.

**Answer:**

"At GSTN, when a junior developer joined my team, I:

1. **Paired on first task:** We implemented a new Kafka consumer together. I wrote the structure, they filled in the business logic. I explained WHY we use manual offset commits (reliability) vs auto-commit.

2. **Code review as teaching:** Instead of just approving/rejecting, I'd leave comments like 'This works, but consider using @Transactional(propagation = REQUIRES_NEW) here because...' — turning reviews into learning moments.

3. **Gradually increased ownership:** First they did bug fixes → then small features → then they designed a new API endpoint end-to-end while I reviewed.

4. **The mistake I let happen:** Once they put a `@Transactional` annotation on a method that called an external HTTP API. Instead of blocking the review, I asked them to think about what happens if the API takes 30 seconds — the database connection is held for 30 seconds. They realized the problem themselves and remembered it permanently."

---

## PART H: CURVEBALL / TRICKY QUESTIONS (2025-2026 Trending)

---

### HQ1. What happens when you type a URL in the browser and press Enter? (Full stack answer expected for SDE-2+)

**Answer (interview-ready, cover all layers):**

```
1. URL Parsing: Browser parses https://gst.gov.in/returns?gstin=29AAACG1234A
   → Protocol: HTTPS, Host: gst.gov.in, Path: /returns, Query: gstin=...

2. DNS Resolution:
   Browser cache → OS cache → Router cache → ISP DNS → Root DNS → .in TLD → gst.gov.in
   → Returns IP: 103.100.xxx.xxx (multiple IPs for load balancing)

3. TCP Connection:
   Three-way handshake: SYN → SYN-ACK → ACK
   → TCP connection established

4. TLS Handshake (HTTPS):
   ClientHello (cipher suites) → ServerHello (chosen cipher + certificate)
   → Client verifies cert → Key exchange → Symmetric session key established
   → All further data encrypted

5. HTTP Request:
   GET /returns?gstin=29AAACG1234A HTTP/2
   Host: gst.gov.in
   Authorization: Bearer <JWT>

6. Load Balancer:
   AWS ALB/NLB → health check → route to healthy K8s pod
   → Based on: round-robin / least connections / IP hash

7. K8s Ingress → Service → Pod:
   Ingress controller → ClusterIP service → selected Pod

8. Application Processing (Spring Boot):
   Tomcat → Filter chain → DispatcherServlet → Controller → Service → DB/Cache
   (full lifecycle as described in BQ2)

9. Response:
   HTTP/2 200 OK
   Content-Type: application/json
   { "returns": [...] }

10. Browser Rendering:
    Parse JSON → JavaScript framework (Angular) renders UI
    Subsequent AJAX calls for lazy-loaded data
```

---

### HQ2. Is Java pass-by-value or pass-by-reference? Prove it. (Trick question — still asked!)

**Answer:**

"Java is **always pass-by-value**. But the 'value' of an object variable is the **reference (pointer) to the object** — not the object itself."

```java
// Proof 1: Primitive — clearly pass-by-value
void modify(int x) { x = 100; }
int a = 5;
modify(a);
System.out.println(a);  // 5 — unchanged

// Proof 2: Object — the REFERENCE is passed by value
void modify(StringBuilder sb) {
    sb.append(" World");  // Modifies the object (same reference)
}
StringBuilder s = new StringBuilder("Hello");
modify(s);
System.out.println(s);  // "Hello World" — object modified through shared reference

// Proof 3: Reassigning the reference doesn't affect caller
void replace(StringBuilder sb) {
    sb = new StringBuilder("New");  // Reassigns LOCAL copy of reference
}
StringBuilder s = new StringBuilder("Hello");
replace(s);
System.out.println(s);  // "Hello" — still original! Because reference was copied
```

"If Java were pass-by-reference, `replace()` would have changed `s` to point to 'New'. Since it didn't, Java passes the reference BY VALUE."

---

### HQ3. What's the difference between `String`, `StringBuilder`, and `StringBuffer`? What is the String pool? Why is String immutable?

**Answer:**

| | String | StringBuilder | StringBuffer |
|--|--------|---------------|-------------|
| Mutability | **Immutable** | Mutable | Mutable |
| Thread-safe | Yes (immutable) | **No** | Yes (synchronized) |
| Performance | Slow for concatenation | **Fastest** | Slower (sync overhead) |
| Use case | Constants, keys | **Single-threaded string building** | Multi-threaded (rare) |

**String Pool (Interning):**
```java
String s1 = "GSTN";        // Goes to String Pool
String s2 = "GSTN";        // Reuses from String Pool
String s3 = new String("GSTN");  // Goes to Heap (NOT pool)

s1 == s2;     // true (same object from pool)
s1 == s3;     // false (different objects)
s1.equals(s3); // true (same content)

s3.intern();  // Moves s3 to pool (or returns existing pool reference)
```

**Why is String immutable?**
1. **String Pool:** Multiple references share same object — mutation would affect all
2. **Thread safety:** Immutable = inherently thread-safe
3. **Security:** GSTIN strings, passwords, class names — mutation would be a security risk
4. **HashMap key:** hashCode() cached — if String mutated, map lookup would break
5. **Class loading:** Class names are Strings — mutating would break classloading

---

### HQ4. Explain the `equals()` and `hashCode()` contract. What breaks if you violate it?

**Answer:**

**Contract:**
1. If `a.equals(b)` is true → `a.hashCode() == b.hashCode()` MUST be true
2. If `a.hashCode() != b.hashCode()` → `a.equals(b)` MUST be false
3. `hashCode()` being equal does NOT guarantee `equals()` (collisions are allowed)

**What breaks if violated:**
```java
// BAD: Override equals but NOT hashCode
class TaxReturn {
    String gstin;
    String period;
    
    @Override
    public boolean equals(Object o) {
        TaxReturn other = (TaxReturn) o;
        return gstin.equals(other.gstin) && period.equals(other.period);
    }
    // hashCode NOT overridden — uses default (memory address)
}

TaxReturn r1 = new TaxReturn("29AAA...", "072023");
TaxReturn r2 = new TaxReturn("29AAA...", "072023");

r1.equals(r2);  // true ✓

Set<TaxReturn> set = new HashSet<>();
set.add(r1);
set.contains(r2);  // FALSE! ✗
// Because hashCode differs → looks in wrong bucket → doesn't find it

Map<TaxReturn, String> map = new HashMap<>();
map.put(r1, "filed");
map.get(r2);  // NULL! ✗  Same problem

// GSTN uses Lombok @EqualsAndHashCode to auto-generate correct implementations
@EqualsAndHashCode
public class ApplnPK implements Serializable { ... }
```

---

### HQ5. What is the difference between an interface and an abstract class in Java 8+? When to use each?

**Answer:**

| Feature | Interface (Java 8+) | Abstract Class |
|---------|-------|---|
| Multiple inheritance | **Yes** (implements many) | No (extends one) |
| Constructors | No | **Yes** |
| State (instance fields) | No (only static final) | **Yes** |
| Access modifiers | public only (until Java 9) | Any |
| Default methods | **Yes** (Java 8+) | Yes |
| Static methods | **Yes** (Java 8+) | Yes |
| Private methods | **Yes** (Java 9+) | Yes |

**When to use interface:**
- Define a contract (what to do, not how)
- Need multiple inheritance: `class ReturnService implements FilingService, ValidationService`
- Functional interface for lambdas: `@FunctionalInterface`

**When to use abstract class:**
- Share state (fields) among related classes
- Provide partial implementation (Template Method pattern)
- Need constructors for initialization

**GSTN example:**
```java
// Interface — define contract
public interface Anx1aService {
    String getAnx1aRecords(Anx1aParamVO params, String type);
}

// Abstract class — share common workflow behavior
public abstract class BaseReturnProcessor {
    protected DistCacheUtil distCacheUtil;  // Shared state
    
    // Template method
    public final ReturnResponse process(ReturnVO vo) {
        validate(vo);
        ReturnEntity entity = transform(vo);
        save(entity);
        notify(entity);
        return buildResponse(entity);
    }
    
    protected abstract ReturnEntity transform(ReturnVO vo);  // Subclass implements
    protected abstract void validate(ReturnVO vo);
}
```

---

## PART I: SPRING BOOT 3.x / JAVA 21 — LATEST FEATURES (2025-2026 Interviews)

---

### IQ1. What's new in Spring Boot 3.x? What migration challenges exist from 2.x?

**Answer:**

**Key changes in Spring Boot 3.x:**
1. **Java 17 minimum** (Jakarta EE 9+, not Java 8/11)
2. **`javax.*` → `jakarta.*`** namespace migration (biggest breaking change)
3. **Native compilation** with GraalVM (AOT — Ahead of Time compilation)
4. **Observability** built-in (Micrometer Observation API)
5. **HTTP interfaces** (`@HttpExchange` — declarative HTTP clients)
6. **Problem Details** (RFC 7807) for error responses
7. **Virtual thread support** (Java 21)

**Migration challenges for GSTN:**
```java
// 1. Package rename (affects EVERY Java file)
// Before: import javax.persistence.Entity;
// After:  import jakarta.persistence.Entity;

// Before: import javax.servlet.http.HttpServletRequest;
// After:  import jakarta.servlet.http.HttpServletRequest;

// 2. Spring Security — completely rewritten API
// Before:
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) { ... }
}

// After:
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .build();
    }
}

// 3. spring.factories deprecated → META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

---

### IQ2. What are Spring Boot HTTP Interface Clients (Spring 6)?

**Answer:**

```java
// Declarative HTTP client — like Feign but built into Spring
@HttpExchange("/api/v1/returns")
public interface ReturnServiceClient {
    
    @GetExchange("/{gstin}")
    ReturnResponse getReturn(@PathVariable String gstin);
    
    @PostExchange
    ReturnResponse fileReturn(@RequestBody ReturnVO vo);
}

// Configuration
@Configuration
public class ClientConfig {
    @Bean
    ReturnServiceClient returnClient(RestClient.Builder builder) {
        RestClient restClient = builder.baseUrl("http://return-service:8080").build();
        return HttpServiceProxyFactory
            .builderFor(RestClientAdapter.create(restClient))
            .build()
            .createClient(ReturnServiceClient.class);
    }
}

// Usage — clean and testable
@Service
public class FilingService {
    private final ReturnServiceClient returnClient;
    
    public FilingService(ReturnServiceClient returnClient) {
        this.returnClient = returnClient;  // Constructor injection
    }
    
    public ReturnResponse getReturn(String gstin) {
        return returnClient.getReturn(gstin);
    }
}
```

---

### IQ3. What is GraalVM Native Image? Pros and cons for microservices?

**Answer:**

**GraalVM Native Image:** Compiles Java application Ahead-of-Time (AOT) into a standalone native binary.

| | JVM | Native Image |
|--|-----|------|
| Startup time | 3-10 seconds | **~50ms** |
| Memory footprint | 200-500MB | **50-100MB** |
| Peak throughput | **Higher** (JIT optimizes hot paths) | Lower (no runtime optimization) |
| Build time | Fast | **Slow (5-10 min)** |
| Reflection | Full support | **Requires configuration** |
| Dynamic proxies | Full support | **Requires configuration** |

**Best for:** Serverless (Lambda), CLI tools, services with low traffic but need fast cold start

**NOT best for:** High-throughput services (GSTN filing), because JIT's runtime optimization produces faster code after warmup.

```bash
# Build native image with Spring Boot 3
mvn -Pnative spring-boot:build-image
# or
./gradlew nativeCompile
```

---

## QUICK REFERENCE: TOP 20 QUESTIONS FOR EACH COMPANY TYPE

### FAANG (Google, Amazon, Meta, Apple, Netflix):
1. DSA (2 rounds): Trees, Graphs, Dynamic Programming, System Design
2. System Design: Scale, CAP theorem, eventual consistency
3. Java internals: JMM, GC, ConcurrentHashMap internals
4. Behavioral: Leadership principles (Amazon), Googleyness

### Product Companies (Flipkart, Razorpay, PhonePe, Swiggy, Cred):
1. Spring Boot DEEP: Auto-config internals, @Transactional pitfalls, HikariCP tuning
2. Kafka: Exactly-once semantics, consumer lag, partition strategy
3. System Design: Payment system, rate limiter, notification system
4. Database: Sharding, indexing, query optimization

### Startups (Meesho, Zepto, Jupiter, Jar):
1. Full-stack capability: REST API design, DB schema design, deployment
2. Practical problem-solving: "How would you build X in 2 weeks?"
3. Trade-off discussions: Monolith vs microservices, SQL vs NoSQL
4. Ownership mindset: "Tell me about something you built end-to-end"

### Banks/Fintech (Goldman Sachs, Morgan Stanley, JP Morgan):
1. Concurrency: Thread safety, deadlocks, lock-free data structures
2. Low-latency: GC tuning, memory optimization, cache strategies
3. Reliability: Idempotency, exactly-once processing, XA transactions
4. Security: Encryption, JWT, OWASP, audit logging

---

*This file covers ~60 additional questions commonly asked at SDE-2/SDE-3 level (5.5 YOE) across FAANG, product companies, startups, and fintech firms in 2025-2026 interview rounds. Combined with the original 296 questions, this provides ~350+ questions for comprehensive preparation.*
