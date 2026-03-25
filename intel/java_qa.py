"""
Java / Spring / Concurrency / JVM / Golang Interview Q&A Tracker.

Extracted from JAVA_SPRING_GOLANG_INTERVIEW_GUIDE.md (300+ questions).
Curated to ~160 P0 "must-know" questions for SDE-2 level.

Tracks which topics/questions you have studied via progress.json.

Usage:
  prep java                    → today's recommended topic + weak areas
  prep java list               → all topics with readiness %
  prep java <topic>            → show P0 questions for a topic
  prep java done <topic>       → mark topic as studied today
  prep java reset <topic>      → reset a topic (re-study)
"""

import json
from pathlib import Path
from datetime import date

BASE      = Path(__file__).parent.parent
PROG_FILE = BASE / "logs" / "progress.json"

# ── Question Bank ─────────────────────────────────────────────────────────────
# Each question: (id, question, priority, company_tag, hint)
# Priority: P0 = must know (90%+ interviews), P1 = important, P2 = differentiator
# Hint: 1-line answer anchor to aid recall

JAVA_QA = {

  # ══════════════════════════════════════════════════════════════════════════
  "oop": {
    "label": "OOP Fundamentals",
    "tag": "java",
    "questions": [
      ("J1",  "What are the 4 pillars of OOP? Give examples.",                         "P0", "all",          "Encapsulation, Inheritance, Polymorphism, Abstraction"),
      ("J2",  "Difference between Abstraction and Encapsulation?",                     "P0", "all",          "Abstraction = hide complexity (interface); Encapsulation = hide data (private fields)"),
      ("J3",  "Runtime vs Compile-time polymorphism?",                                 "P0", "all",          "Runtime = method overriding (dynamic dispatch); Compile-time = method overloading"),
      ("J4",  "Can we override static methods?",                                       "P0", "all",          "No — static methods are hidden, not overridden (method hiding)"),
      ("J5",  "Composition vs inheritance — when to use which?",                       "P0", "all",          "Prefer composition ('has-a') over inheritance ('is-a') for flexibility"),
      ("J6",  "How does Java achieve multiple inheritance?",                            "P0", "all",          "Via interfaces (multiple interface implementation)"),
      ("J7",  "What is Liskov Substitution Principle?",                                "P1", "google",       "Subclass must be substitutable for superclass without breaking behaviour"),
      ("J8",  "What is covariant return type?",                                        "P1", "all",          "Overriding method can return subtype of parent return type (Java 5+)"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "strings": {
    "label": "Strings & Immutability",
    "tag": "java",
    "questions": [
      ("J9",  "Why is String immutable in Java?",                                      "P0", "all",          "Security, thread-safety, caching hashCode, String pool reuse"),
      ("J10", "String vs StringBuilder vs StringBuffer?",                               "P0", "all",          "String=immutable; SB=mutable+not threadsafe; StringBuffer=mutable+threadsafe"),
      ("J11", "What is String Pool? Where is it stored?",                               "P0", "all",          "Heap (metaspace in Java 8+); literals go to pool, new String() bypasses it"),
      ("J12", "How many objects: String s = new String('abc')?",                        "P0", "all",          "2 if 'abc' not in pool (pool + heap), 1 if already in pool"),
      ("J13", "Why is String a popular HashMap key?",                                   "P1", "all",          "Immutable → stable hashCode; cached hashCode → fast lookups"),
      ("J14", "What is string interning? When to use?",                                 "P1", "all",          "Forces string into pool via intern(); reduces memory for many repeated strings"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "exceptions": {
    "label": "Exception Handling",
    "tag": "java",
    "questions": [
      ("J15", "Checked vs Unchecked exceptions?",                                       "P0", "all",          "Checked=must handle (IOException); Unchecked=RuntimeException subclasses"),
      ("J16", "throw vs throws?",                                                       "P0", "all",          "throw=actually throw an instance; throws=declare method can throw"),
      ("J17", "Can we have try without catch?",                                         "P1", "all",          "Yes with finally or try-with-resources"),
      ("J18", "What happens if exception occurs in finally block?",                     "P0", "all",          "Suppresses the original exception; finally exception propagates instead"),
      ("J19", "Try-with-resources — how does it work?",                                 "P0", "all",          "Auto-calls close() on AutoCloseable; suppressed exceptions preserved"),
      ("J20", "Custom checked vs unchecked exception — when to use?",                   "P0", "amazon",       "Checked for recoverable (caller should handle); unchecked for programming errors"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "java8": {
    "label": "Java 8+ Features",
    "tag": "java",
    "questions": [
      ("J21", "What is a functional interface?",                                         "P0", "all",          "Interface with exactly 1 abstract method; @FunctionalInterface annotation"),
      ("J22", "Explain lambda expressions — syntax and use.",                            "P0", "all",          "(params) -> body; replaces anonymous class for functional interfaces"),
      ("J23", "Method reference — types?",                                               "P0", "all",          "Static, Instance (specific/arbitrary), Constructor :: operator"),
      ("J24", "Predicate vs Function vs Consumer vs Supplier?",                          "P0", "all",          "Predicate=T→bool; Function=T→R; Consumer=T→void; Supplier=()→T"),
      ("J25", "What is Optional? Why use it? Anti-patterns?",                            "P0", "all",          "Avoid null returns; don't use as field/param; use map/flatMap/orElse"),
      ("J26", "Default method in interface — why added?",                                "P0", "all",          "Add methods to interfaces without breaking existing implementations (Java 8)"),
      ("J27", "What if two interfaces have same default method?",                        "P1", "all",          "Compile error; implementing class must override to resolve"),
      ("J28", "Stream API — explain intermediate vs terminal ops.",                      "P0", "all",          "Intermediate=lazy (filter/map); Terminal=eager, triggers pipeline (collect/forEach)"),
      ("J29", "map() vs flatMap() in streams?",                                          "P0", "all",          "map=1:1 transform; flatMap=1:N then flatten (for nested streams/Optional)"),
      ("J30", "What is lazy evaluation in streams?",                                     "P1", "all",          "Intermediate ops not executed until terminal op called; enables short-circuit"),
      ("J31", "Parallel streams — when to use vs avoid?",                                "P0", "all",          "Use for CPU-bound, large datasets, no side effects; avoid for small/IO-bound"),
      ("J32", "Records in Java 14+ — when to use?",                                     "P1", "all",          "Immutable data carriers; auto-generates equals/hashCode/toString/getters"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "collections": {
    "label": "Java Collections",
    "tag": "java",
    "questions": [
      ("J33", "ArrayList vs LinkedList — internals + when to use?",                      "P0", "all",          "ArrayList=resizable array (fast random access); LL=doubly linked (fast insert/delete)"),
      ("J34", "How does ArrayList grow?",                                                "P0", "all",          "Grows to 1.5× capacity; copies array; default capacity 10"),
      ("J35", "fail-fast vs fail-safe iterator?",                                        "P0", "all",          "fail-fast throws ConcurrentModificationException on structural change; fail-safe copies"),
      ("J36", "CopyOnWriteArrayList — when to use?",                                     "P1", "all",          "Read-heavy concurrent access; writes are expensive (full copy); no CME"),
      ("J37", "EXPLAIN HashMap internals completely.",                                    "P0", "all",          "Array of buckets; hashCode()→index; linked list/tree for collisions; threshold 0.75"),
      ("J38", "What is hashing? How hashCode() works in HashMap?",                       "P0", "all",          "hashCode() → (h=key.hashCode())^(h>>>16); spreads high bits to low"),
      ("J39", "What happens when two keys have same hashCode?",                          "P0", "all",          "Collision → same bucket → linked list; check equals() for exact key match"),
      ("J40", "Why bucket converts to tree at threshold 8?",                             "P1", "all",          "O(n) list search → O(log n) tree; reverts to list below 6"),
      ("J41", "What is load factor? Default? What happens at resize?",                   "P0", "all",          "0.75 default; at 0.75 * capacity → resize to 2×; rehash all entries"),
      ("J42", "HashMap vs Hashtable vs ConcurrentHashMap?",                              "P0", "all",          "HashMap=not threadsafe; Hashtable=fully sync (slow); CHM=segment/node locking"),
      ("J43", "ConcurrentHashMap internals — how thread-safe without full lock?",        "P0", "goldman",      "Java 8: node-level CAS + synchronized on first insert; reads no lock"),
      ("J44", "LinkedHashMap — how does it maintain insertion order?",                   "P1", "all",          "Doubly-linked list threaded through HashMap nodes; accessOrder=true for LRU"),
      ("J45", "HashSet internals — how does it work?",                                   "P0", "all",          "Backed by HashMap; element is key, PRESENT dummy is value"),
      ("J46", "How to implement equals() and hashCode() correctly?",                     "P0", "all",          "Same fields in both; if equals()→true then hashCode() must be same"),
      ("J47", "BlockingQueue types — when to use which?",                                "P0", "all",          "ArrayBQ=bounded; LinkedBQ=optionally bounded; PriorityBQ=ordered; use in producers/consumers"),
      ("J48", "PriorityQueue internals — min-heap?",                                     "P1", "all",          "Binary min-heap backed by array; poll()=O(log n); peek()=O(1)"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "concurrency": {
    "label": "Java Concurrency",
    "tag": "java",
    "questions": [
      ("J49", "Thread vs Runnable vs Callable?",                                         "P0", "all",          "Thread=class; Runnable=no return/exception; Callable=returns Future+throws"),
      ("J50", "Thread lifecycle and states?",                                            "P0", "all",          "NEW→RUNNABLE→BLOCKED/WAITING/TIMED_WAITING→TERMINATED"),
      ("J51", "How to stop a thread safely?",                                            "P0", "all",          "Use interrupt() flag; check Thread.interrupted() or InterruptedException"),
      ("J52", "synchronized keyword — method vs block level?",                           "P0", "all",          "Method=lock on 'this' (or Class for static); block=explicit object lock"),
      ("J53", "volatile keyword — what does it guarantee?",                              "P0", "goldman",      "Visibility: all threads see latest write; does NOT guarantee atomicity"),
      ("J54", "volatile vs synchronized?",                                               "P0", "all",          "volatile=visibility only; synchronized=visibility+atomicity+mutual exclusion"),
      ("J55", "Why volatile doesn't guarantee atomicity?",                               "P0", "goldman",      "i++ = read+increment+write (3 ops); another thread can interleave"),
      ("J56", "What is deadlock? How to detect and prevent?",                            "P0", "all",          "Circular wait on locks; prevent=consistent lock order/tryLock/timeout"),
      ("J57", "What is livelock?",                                                       "P1", "all",          "Threads keep responding to each other without progress; e.g. politeness loop"),
      ("J58", "What is race condition? How to avoid?",                                   "P0", "all",          "Two threads access shared data non-atomically; fix=synchronize/atomic/volatile"),
      ("J59", "What is memory visibility problem?",                                      "P0", "goldman",      "Thread caches var in CPU register/L1; other thread sees stale value; fix=volatile/sync"),
      ("J60", "What is happens-before relationship?",                                    "P1", "goldman",      "JMM guarantee: action A happens-before B means B sees A's writes"),
      ("J61", "ReentrantLock vs synchronized?",                                          "P0", "all",          "ReentrantLock=explicit lock/unlock, tryLock, fairness, multiple conditions"),
      ("J62", "ReadWriteLock — when to use?",                                            "P0", "all",          "Many readers, few writers; multiple concurrent reads, exclusive write"),
      ("J63", "ExecutorService — why use over raw threads?",                             "P0", "all",          "Thread pooling, task queuing, lifecycle management, Future support"),
      ("J64", "ThreadPoolExecutor parameters — explain each.",                           "P0", "all",          "corePoolSize, maxPoolSize, keepAlive, timeUnit, workQueue, handler"),
      ("J65", "FixedThreadPool vs CachedThreadPool vs ScheduledThreadPool?",             "P0", "all",          "Fixed=bounded; Cached=unbounded short-lived; Scheduled=delayed/periodic"),
      ("J66", "How to size a thread pool? CPU-bound vs IO-bound?",                      "P0", "all",          "CPU: N+1 threads; IO: N * (1 + wait/compute ratio)"),
      ("J67", "ForkJoinPool — work-stealing algorithm?",                                 "P1", "all",          "Each thread has deque; steals from tail of other thread's queue"),
      ("J68", "Future vs CompletableFuture?",                                            "P0", "all",          "Future=blocking get(); CF=async chaining (thenApply/thenCompose/allOf)"),
      ("J69", "CompletableFuture: thenApply vs thenCompose vs thenCombine?",             "P0", "all",          "thenApply=transform; thenCompose=flatMap (returns CF); thenCombine=zip two CFs"),
      ("J70", "How to handle exceptions in CompletableFuture?",                         "P0", "all",          "exceptionally()=fallback; handle()=process both result+exception"),
      ("J71", "AtomicInteger — how does it work? What is CAS?",                         "P0", "all",          "Compare-And-Swap: if current==expected then set new; hardware instruction, lock-free"),
      ("J72", "CountDownLatch vs CyclicBarrier?",                                       "P0", "all",          "CDL=one-time, count down to 0 then release; CB=reusable, await until all arrive"),
      ("J73", "Semaphore — use case?",                                                   "P0", "all",          "Control concurrent access to resource pool (e.g. 10 DB connections max)"),
      ("J74", "Virtual Threads (Java 21 Project Loom)?",                                 "P1", "all",          "Lightweight threads on carrier threads; ideal for IO-bound; don't use ThreadLocals heavily"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "jvm": {
    "label": "JVM & Memory Model",
    "tag": "java",
    "questions": [
      ("J75", "JVM memory areas — Heap, Stack, Metaspace?",                             "P0", "all",          "Heap=objects; Stack=frames/local vars (per thread); Metaspace=class metadata"),
      ("J76", "Stack vs Heap memory?",                                                  "P0", "all",          "Stack=LIFO, fast, per-thread, primitives+refs; Heap=shared, GC-managed, objects"),
      ("J77", "GC algorithms — Serial, Parallel, G1, ZGC?",                             "P1", "all",          "G1=default Java 11+ (region-based); ZGC=<10ms pause; G1 for most apps"),
      ("J78", "Young generation vs Old generation?",                                    "P1", "all",          "Young=Eden+S0+S1 (minor GC); Old=long-lived objects (major GC); promotion after N cycles"),
      ("J79", "What is Stop-the-World pause?",                                          "P1", "all",          "GC pauses all app threads; ZGC/Shenandoah minimize this"),
      ("J80", "What is memory leak in Java? How to detect?",                            "P0", "all",          "Objects held in memory unintentionally (static maps, listeners); use VisualVM/heap dump"),
      ("J81", "What causes OutOfMemoryError? Types?",                                   "P0", "all",          "Java heap space, GC overhead limit, Metaspace, unable to create thread"),
      ("J82", "What is thread dump? How to analyze?",                                   "P1", "all",          "Snapshot of all thread states; look for BLOCKED threads with same lock address"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "spring_core": {
    "label": "Spring Core & IoC",
    "tag": "spring",
    "questions": [
      ("S1",  "What is Dependency Injection? Types?",                                   "P0", "all",          "Constructor, Setter, Field injection; inversion of control principle"),
      ("S2",  "Constructor vs Setter injection — when to use?",                         "P0", "all",          "Constructor=mandatory deps (immutable); Setter=optional deps"),
      ("S3",  "Spring Bean Lifecycle — complete flow?",                                 "P0", "all",          "Instantiate→DI→@PostConstruct→ready→@PreDestroy→destroy"),
      ("S4",  "Bean Scopes — singleton, prototype, request, session?",                  "P0", "all",          "Singleton=1 per context; prototype=new on each request; request/session=web scopes"),
      ("S5",  "What happens if prototype bean injected into singleton?",                 "P0", "all",          "Singleton uses same prototype instance; fix=ApplicationContext.getBean() or @Lookup"),
      ("S6",  "@Component vs @Service vs @Repository vs @Controller?",                  "P0", "all",          "All are @Component specializations; @Repository=exception translation"),
      ("S7",  "How does @Autowired work internally?",                                   "P0", "all",          "AutowiredAnnotationBeanPostProcessor; byType first, byName if ambiguous"),
      ("S8",  "@Qualifier vs @Primary?",                                                "P0", "all",          "@Primary=default bean; @Qualifier=explicit name selection"),
      ("S9",  "Circular dependency — how does Spring handle?",                          "P0", "all",          "Setter/field injection uses 3-level cache; constructor injection = startup failure"),
      ("S10", "BeanFactory vs ApplicationContext?",                                     "P1", "all",          "BF=lazy init basic; AC=eager init, events, i18n, AOP; always use AC"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "spring_boot": {
    "label": "Spring Boot",
    "tag": "spring",
    "questions": [
      ("S11", "How does Spring Boot auto-configuration work?",                           "P0", "all",          "@EnableAutoConfiguration reads spring.factories; @Conditional annotations filter"),
      ("S12", "@SpringBootApplication — what annotations does it include?",              "P0", "all",          "@Configuration + @EnableAutoConfiguration + @ComponentScan"),
      ("S13", "Spring profiles — how to use?",                                          "P0", "all",          "@Profile('dev'); application-{profile}.yml; spring.profiles.active"),
      ("S14", "@ConfigurationProperties vs @Value?",                                    "P0", "all",          "@CP=type-safe binding of prefix; @Value=single property with SpEL"),
      ("S15", "Spring Boot Actuator — key endpoints?",                                  "P0", "all",          "/health, /metrics, /env, /loggers, /threaddump, /heapdump"),
      ("S16", "How to disable specific auto-configuration?",                            "P1", "all",          "@SpringBootApplication(exclude=DataSourceAutoConfiguration.class)"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "spring_jpa": {
    "label": "Spring Data JPA & Transactions",
    "tag": "spring",
    "questions": [
      ("S17", "@Transactional — how does it work internally?",                           "P0", "all",          "AOP proxy intercepts; starts TX before method, commits/rollback after"),
      ("S18", "@Transactional propagation levels?",                                     "P0", "all",          "REQUIRED(default), REQUIRES_NEW, SUPPORTS, NOT_SUPPORTED, MANDATORY, NEVER, NESTED"),
      ("S19", "@Transactional isolation levels?",                                        "P0", "cars24",       "DEFAULT/READ_UNCOMMITTED/READ_COMMITTED/REPEATABLE_READ/SERIALIZABLE"),
      ("S20", "dirty read, phantom read, non-repeatable read?",                          "P0", "all",          "Dirty=uncommitted; NRR=same row different value; Phantom=new rows appear"),
      ("S21", "@Transactional self-invocation problem?",                                 "P0", "all",          "Internal call bypasses proxy; fix=inject self or use AopContext.currentProxy()"),
      ("S22", "N+1 problem — what is it and how to solve?",                              "P0", "all",          "1 query for parents + N for each child; fix=JOIN FETCH / @EntityGraph / batch size"),
      ("S23", "Lazy vs Eager loading?",                                                  "P0", "all",          "Lazy=load on access; Eager=load with parent; default: @OneToMany=LAZY, @ManyToOne=EAGER"),
      ("S24", "LazyInitializationException — how to solve?",                             "P0", "all",          "Session closed before accessing lazy collection; fix=open-in-view/JOIN FETCH/DTO"),
      ("S25", "Optimistic vs Pessimistic locking?",                                     "P0", "all",          "Optimistic=@Version check at commit; Pessimistic=SELECT FOR UPDATE (DB-level lock)"),
      ("S26", "Pagination and Sorting in Spring Data?",                                  "P0", "all",          "Pageable param; findAll(PageRequest.of(0, 10, Sort.by('name')))"),
      ("S27", "JPA vs Hibernate vs Spring Data JPA?",                                   "P0", "all",          "JPA=spec; Hibernate=implementation; SDJPA=abstraction layer with repositories"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "microservices": {
    "label": "Microservices & Spring Cloud",
    "tag": "spring",
    "questions": [
      ("S28", "Microservices — advantages and disadvantages?",                           "P0", "all",          "Pros: scale, deploy, tech choice; Cons: network latency, distributed tracing, data consistency"),
      ("S29", "Circuit Breaker pattern — states?",                                      "P0", "all",          "CLOSED (normal) → OPEN (failing, fail-fast) → HALF_OPEN (probe); Resilience4j"),
      ("S30", "Saga pattern for distributed transactions?",                              "P0", "amazon",       "Choreography (events) vs Orchestration (saga orchestrator); compensating transactions"),
      ("S31", "Event-driven architecture with Kafka?",                                   "P0", "all",          "Producer→topic→consumer group; decoupled, async, replay; exactly-once semantics"),
      ("S32", "Service Discovery — Eureka?",                                             "P1", "all",          "Client-side: fetch registry, pick instance; Eureka server + @EnableEurekaClient"),
      ("S33", "API Gateway pattern?",                                                    "P0", "all",          "Single entry point; auth/rate-limit/routing/logging; Spring Cloud Gateway"),
      ("S34", "Bulkhead pattern?",                                                       "P1", "all",          "Isolate failures; separate thread pools per service; prevents cascade failure"),
      ("S35", "Distributed tracing — how?",                                              "P1", "all",          "TraceId+SpanId propagated in headers; Zipkin/Jaeger aggregates; Sleuth auto-instruments"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "databases": {
    "label": "Databases & SQL",
    "tag": "backend",
    "questions": [
      ("D1",  "ACID properties?",                                                        "P0", "all",          "Atomicity, Consistency, Isolation, Durability"),
      ("D2",  "CAP theorem?",                                                            "P0", "all",          "Can have only 2 of 3: CP=strong consistency (HBase/Zookeeper); AP=availability (Cassandra/DynamoDB)"),
      ("D3",  "SQL joins — INNER, LEFT, RIGHT, FULL?",                                  "P0", "all",          "INNER=matching rows; LEFT=all left+matching right; FULL=all rows both sides"),
      ("D4",  "Database indexing — types?",                                             "P0", "all",          "B-tree (range), Hash (equality), Composite, Covering, Partial, Full-text"),
      ("D5",  "B-Tree vs B+ Tree index?",                                               "P1", "all",          "B+=all data in leaves, linked list for range scans; B=data at any node"),
      ("D6",  "When NOT to use index?",                                                  "P1", "all",          "Low cardinality, write-heavy tables, small tables, frequent full scans"),
      ("D7",  "What is query execution plan? EXPLAIN?",                                  "P0", "all",          "Shows optimizer's plan; look for seq scan, index scan, hash join, nested loop"),
      ("D8",  "Database normalization — 1NF/2NF/3NF?",                                  "P0", "all",          "1NF=atomic; 2NF=no partial dependency; 3NF=no transitive dependency"),
      ("D9",  "Database sharding — horizontal vs vertical?",                             "P0", "all",          "Horizontal=split rows (by user_id); Vertical=split columns (feature split)"),
      ("D10", "Master-Slave replication?",                                               "P0", "all",          "Master=writes; Slave=reads; async or sync replication; replication lag"),
      ("D11", "Connection pooling — HikariCP?",                                         "P0", "all",          "Pool of pre-created connections; Hikari=fastest; set pool size=N+1 for CPU-bound"),
      ("D12", "When to use SQL vs NoSQL?",                                               "P0", "all",          "SQL=ACID, complex joins, known schema; NoSQL=scale, flexible schema, high write throughput"),
      ("D13", "Redis — use cases + data structures?",                                    "P0", "all",          "Cache, session, rate-limit, pub/sub, leaderboard; String/Hash/List/Set/ZSet/HLL"),
      ("D14", "Redis vs Memcached?",                                                     "P1", "all",          "Redis=persistence+rich data types+cluster; Memcached=simpler, multi-threaded"),
      ("D15", "Cassandra — when to use?",                                                "P1", "all",          "Time-series, IoT, write-heavy; AP system; wide-column; partition+clustering keys"),
      ("D16", "Elasticsearch — use cases?",                                              "P1", "all",          "Full-text search, log analytics (ELK); inverted index; NOT for primary storage"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "golang": {
    "label": "Golang",
    "tag": "golang",
    "questions": [
      ("G1",  "What are goroutines? How different from threads?",                        "P0", "all",          "Lightweight (2KB stack); managed by Go scheduler (M:N threading); cheap to spawn 1M+"),
      ("G2",  "What are channels? Buffered vs unbuffered?",                             "P0", "all",          "Type-safe pipe between goroutines; unbuffered=sync; buffered=async up to capacity"),
      ("G3",  "What is select statement in Go?",                                        "P0", "all",          "Like switch for channels; picks whichever channel is ready; default=non-blocking"),
      ("G4",  "What is defer in Go?",                                                   "P0", "all",          "Deferred to function return (LIFO); use for cleanup (defer file.Close())"),
      ("G5",  "What is context.Context? When to use?",                                  "P0", "all",          "Cancellation+deadline+values across goroutines; pass as first param; cancel on done"),
      ("G6",  "How does Go handle errors?",                                             "P0", "all",          "Multiple returns (val, error); check err != nil; errors.Is/As for wrapping"),
      ("G7",  "What is interface{} / any in Go?",                                       "P1", "all",          "Empty interface; holds any value; type assertion/switch for type checking"),
      ("G8",  "Goroutine leak — what is it? How to prevent?",                           "P0", "all",          "Goroutine blocks forever; use context cancellation, WaitGroup, channel close"),
      ("G9",  "What is sync.WaitGroup?",                                                "P0", "all",          "Wait for N goroutines to finish; Add(n)/Done()/Wait()"),
      ("G10", "sync.Mutex vs sync.RWMutex?",                                            "P0", "all",          "Mutex=exclusive; RWMutex=multiple readers OR one writer"),
      ("G11", "What is Go's garbage collector?",                                        "P1", "all",          "Tricolor concurrent mark-and-sweep; low latency; GOGC controls aggressiveness"),
      ("G12", "What is a goroutine scheduler (GMP model)?",                             "P1", "google",       "G=goroutine, M=OS thread, P=logical processor; work-stealing scheduler"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "design_patterns": {
    "label": "Design Patterns (SOLID + GoF)",
    "tag": "lld",
    "questions": [
      ("DP1", "SOLID principles — explain each briefly.",                                "P0", "all",          "SRP, OCP, LSP, ISP, DIP — one change per class, extend not modify, substitutable, specific interfaces, depend on abstractions"),
      ("DP2", "Singleton pattern — how to make thread-safe in Java?",                   "P0", "all",          "Double-checked locking with volatile, or enum singleton (best), or static holder"),
      ("DP3", "Factory vs Abstract Factory vs Builder?",                                "P0", "all",          "Factory=one product; AF=family of products; Builder=step-by-step complex object"),
      ("DP4", "Strategy pattern — explain with example.",                               "P0", "all",          "Define family of algos, encapsulate each, make interchangeable; e.g. PaymentStrategy"),
      ("DP5", "Observer pattern — explain with example.",                               "P0", "all",          "Subject notifies all observers on state change; EventBus, Listeners"),
      ("DP6", "Decorator pattern — when to use?",                                       "P1", "all",          "Add behavior without subclassing; wrap objects; e.g. Java IO streams"),
      ("DP7", "Proxy pattern — types?",                                                  "P1", "all",          "Virtual(lazy init), Protection(auth), Remote(RPC), Smart reference; Spring AOP uses proxy"),
      ("DP8", "Command pattern — use case?",                                             "P1", "all",          "Encapsulate request as object; undo/redo, queuing; e.g. HTTP request, job queue"),
      ("DP9", "Template Method pattern?",                                                "P1", "all",          "Define skeleton in base class, subclass fills steps; e.g. JdbcTemplate"),
      ("DP10","Composite pattern — use case?",                                           "P1", "all",          "Tree structure where leaf and composite treated uniformly; e.g. File System, Menu"),
    ]
  },

  # ══════════════════════════════════════════════════════════════════════════
  "kafka": {
    "label": "Kafka & Messaging",
    "tag": "backend",
    "questions": [
      ("K1",  "Kafka architecture — topics, partitions, brokers, consumer groups?",     "P0", "all",          "Topic→partitions (ordered log); broker=server; CG=parallel consumers (1 per partition)"),
      ("K2",  "What is consumer group? Partition assignment?",                          "P0", "all",          "Group of consumers sharing topic; each partition → 1 consumer; rebalance on join/leave"),
      ("K3",  "What is offset? How is it committed?",                                   "P0", "all",          "Position in partition log; auto-commit or manual (commitSync/commitAsync)"),
      ("K4",  "Exactly-once semantics in Kafka?",                                       "P0", "amazon",       "Producer idempotency + transactions (begin/commit) + idempotent consumer logic"),
      ("K5",  "Kafka vs RabbitMQ?",                                                     "P0", "all",          "Kafka=log-based, replay, high throughput; RMQ=traditional queue, flexible routing"),
      ("K6",  "What is a Dead Letter Queue (DLQ)?",                                     "P0", "all",          "Topic for failed messages; prevents consumer blocking; process separately"),
      ("K7",  "How to handle poison pill messages?",                                    "P1", "all",          "Catch exception, send to DLQ, commit offset; or retry N times first"),
      ("K8",  "Kafka partitioning strategy?",                                           "P1", "all",          "Default=hash(key)%partitions; null key=round-robin; custom partitioner possible"),
    ]
  },
}

# ── Ordered topic list for daily rotation ────────────────────────────────────
TOPIC_ORDER = [
    "oop", "strings", "exceptions", "java8",
    "collections", "concurrency", "jvm",
    "spring_core", "spring_boot", "spring_jpa", "microservices",
    "databases", "kafka", "design_patterns", "golang",
]

TOPIC_WEEK_MAP = {
    # Week when this topic should be studied (aligns with 26-week plan)
    "oop":            1,
    "strings":        1,
    "exceptions":     1,
    "java8":          2,
    "collections":    2,
    "concurrency":    3,
    "jvm":            3,
    "spring_core":    4,
    "spring_boot":    4,
    "spring_jpa":     5,
    "microservices":  5,
    "databases":      6,
    "kafka":          6,
    "design_patterns": 4,
    "golang":         7,
}


# ── Progress tracking ─────────────────────────────────────────────────────────

def _load_progress() -> dict:
    try:
        return json.loads(PROG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save_progress(prog: dict):
    PROG_FILE.parent.mkdir(exist_ok=True)
    PROG_FILE.write_text(json.dumps(prog, indent=2, default=str), encoding="utf-8")

def _java_state() -> dict:
    return _load_progress().get("java_qa", {"studied": {}, "scores": {}})

def _save_java_state(state: dict):
    prog = _load_progress()
    prog["java_qa"] = state
    _save_progress(prog)


# ── Core API ──────────────────────────────────────────────────────────────────

def get_topics() -> list:
    """Return all topics with studied status."""
    state  = _java_state()
    result = []
    for tid in TOPIC_ORDER:
        t       = JAVA_QA[tid]
        studied = state["studied"].get(tid, [])
        p0_qs   = [q for q in t["questions"] if q[2] == "P0"]
        p0_done = len([q for q in p0_qs if q[0] in studied])
        result.append({
            "id":       tid,
            "label":    t["label"],
            "tag":      t["tag"],
            "total":    len(t["questions"]),
            "p0_total": len(p0_qs),
            "p0_done":  p0_done,
            "pct":      round(p0_done / max(len(p0_qs), 1) * 100),
            "week":     TOPIC_WEEK_MAP.get(tid, 99),
        })
    return result


def get_questions(topic_id: str, priority: str = "P0") -> list:
    """Return questions for a topic filtered by priority."""
    t = JAVA_QA.get(topic_id)
    if not t:
        return []
    state   = _java_state()
    studied = set(state["studied"].get(topic_id, []))
    qs      = [q for q in t["questions"] if not priority or q[2] == priority]
    return [{"id": q[0], "q": q[1], "priority": q[2], "company": q[3], "hint": q[4],
             "studied": q[0] in studied} for q in qs]


def mark_topic_studied(topic_id: str) -> int:
    """Mark all P0 questions in a topic as studied. Returns count marked."""
    state = _java_state()
    t     = JAVA_QA.get(topic_id)
    if not t:
        return 0
    p0_ids = [q[0] for q in t["questions"] if q[2] == "P0"]
    studied = state["studied"].get(topic_id, [])
    new_ids = [qid for qid in p0_ids if qid not in studied]
    state["studied"][topic_id] = studied + new_ids
    state["studied"][topic_id + "_date"] = str(date.today())
    _save_java_state(state)
    return len(new_ids)


def mark_question_studied(topic_id: str, question_id: str) -> bool:
    """Mark a single question as studied."""
    state   = _java_state()
    studied = state["studied"].get(topic_id, [])
    if question_id not in studied:
        state["studied"][topic_id] = studied + [question_id]
        _save_java_state(state)
        return True
    return False


def reset_topic(topic_id: str):
    """Reset studied status for a topic."""
    state = _java_state()
    state["studied"].pop(topic_id, None)
    state["studied"].pop(topic_id + "_date", None)
    _save_java_state(state)


def get_today_topic(current_week: int = 1) -> dict:
    """Return the weakest P0 topic for the current week or earlier."""
    topics = [t for t in get_topics() if t["week"] <= max(current_week, 3)]
    if not topics:
        topics = get_topics()
    # Sort by pct (ascending), then by week
    topics.sort(key=lambda x: (x["pct"], x["week"]))
    return topics[0] if topics else {}


def get_progress() -> dict:
    """Return overall Java Q&A progress."""
    topics      = get_topics()
    total_p0    = sum(t["p0_total"] for t in topics)
    done_p0     = sum(t["p0_done"] for t in topics)
    by_tag: dict = {}
    for t in topics:
        tag = t["tag"]
        if tag not in by_tag:
            by_tag[tag] = {"total_p0": 0, "done_p0": 0}
        by_tag[tag]["total_p0"] += t["p0_total"]
        by_tag[tag]["done_p0"]  += t["p0_done"]
    return {
        "total_p0": total_p0,
        "done_p0":  done_p0,
        "pct":      round(done_p0 / max(total_p0, 1) * 100),
        "by_tag":   by_tag,
    }


# ── Terminal display ──────────────────────────────────────────────────────────

def print_java_today(current_week: int = 1):
    """Print today's recommended Java topic."""
    today  = get_today_topic(current_week)
    prog   = get_progress()

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  JAVA / SPRING Q&A TRACKER                              ║
  ╚══════════════════════════════════════════════════════════╝

  P0 Coverage: {prog['done_p0']}/{prog['total_p0']} questions ready ({prog['pct']}%)
""")

    tag_icons = {"java": "☕", "spring": "🌿", "backend": "🗄", "lld": "◆", "golang": "🐹"}
    for tag, v in prog["by_tag"].items():
        pct = round(v["done_p0"] / max(v["total_p0"], 1) * 100)
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"  {tag_icons.get(tag,'·')} {tag:<12} [{bar}] {pct:>3}%  {v['done_p0']}/{v['total_p0']} P0")

    if today:
        print(f"\n  ▶ STUDY TODAY: {today['label']}  ({today['pct']}% P0 done)")
        print(f"     prep java {today['id']}")
    print()


def print_java_topic(topic_id: str, show_hints: bool = False):
    """Print all P0 questions for a topic."""
    t = JAVA_QA.get(topic_id)
    if not t:
        # Try fuzzy match
        for tid, tv in JAVA_QA.items():
            if topic_id.lower() in tv["label"].lower() or topic_id.lower() in tid:
                topic_id = tid
                t = tv
                break
    if not t:
        print(f"\n  ❌ Topic '{topic_id}' not found. Run: prep java list\n")
        return

    questions = get_questions(topic_id, priority="P0")
    p1_qs     = get_questions(topic_id, priority="P1")
    done_count = sum(1 for q in questions if q["studied"])

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  {t['label']:<52}  ║
  ╚══════════════════════════════════════════════════════════╝

  P0 questions: {done_count}/{len(questions)} studied
""")

    for q in questions:
        status = "✅" if q["studied"] else "○"
        company = f" [{q['company']}]" if q["company"] not in ("all", "") else ""
        print(f"  {status} {q['id']:<4} {q['q']}{company}")
        if show_hints:
            print(f"       💡 {q['hint']}")

    if p1_qs:
        print(f"\n  P1 (Important — study after P0):")
        for q in p1_qs:
            status = "✅" if q["studied"] else "○"
            print(f"  {status} {q['id']:<4} {q['q']}")

    print(f"\n  Mark done: prep java done {topic_id}")
    if not show_hints:
        print(f"  With hints: prep java {topic_id} --hints")
    print()


def print_java_list():
    """Print all topics with readiness."""
    topics = get_topics()
    print(f"\n  JAVA Q&A — ALL TOPICS\n  {'─'*60}")
    for t in topics:
        pct    = t["pct"]
        bar    = "█" * (pct // 5) + "░" * (20 - pct // 5)
        status = "✅" if pct == 100 else ("🟡" if pct > 50 else "🔴")
        print(f"  {status} Week{t['week']:>2}  {t['label']:<38} {t['p0_done']:>2}/{t['p0_total']:<2} [{bar}] {pct}%")
        print(f"         prep java {t['id']}")
    print()
