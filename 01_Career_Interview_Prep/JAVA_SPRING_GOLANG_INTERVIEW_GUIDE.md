# JAVA / SPRING BOOT / GOLANG BACKEND INTERVIEW GUIDE
## Complete Question Bank for SDE-2 Level (2025-2026)

---

## DOCUMENT PURPOSE

This document contains:
1. **300+ Interview Questions** - Organized by topic and difficulty
2. **Company-wise Patterns** - What service vs product companies ask
3. **Recent Trends (2024-2025)** - Actual questions from interviews
4. **Resources & References** - Where to study each topic
5. **Answer Depth Expectations** - What "good" looks like at SDE-2 level

---

## HOW TO USE THIS DOCUMENT

```
Priority Legend:
🔴 P0 - MUST KNOW (Asked in 90%+ interviews)
🟡 P1 - IMPORTANT (Asked in 50-70% interviews)
🟢 P2 - GOOD TO HAVE (Differentiator, asked in 20-30%)

Difficulty:
⭐ Basic - Expected from all candidates
⭐⭐ Intermediate - Expected from 3+ years experience
⭐⭐⭐ Advanced - Expected from 5+ years / SDE-2 level
```

---

# PART 1: CORE JAVA

## Section 1.1: Java Fundamentals

### Object-Oriented Programming 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 1 | What are the four pillars of OOP? Explain with examples. | ⭐ | 🔴 |
| 2 | Difference between Abstraction and Encapsulation? | ⭐ | 🔴 |
| 3 | What is polymorphism? Runtime vs Compile-time? | ⭐ | 🔴 |
| 4 | Can we override static methods? Why or why not? | ⭐⭐ | 🔴 |
| 5 | What is method hiding vs method overriding? | ⭐⭐ | 🟡 |
| 6 | Explain the diamond problem. How does Java solve it? | ⭐⭐ | 🟡 |
| 7 | What is covariant return type? | ⭐⭐ | 🟡 |
| 8 | Difference between composition and inheritance? When to use which? | ⭐⭐ | 🔴 |
| 9 | What is the Liskov Substitution Principle? | ⭐⭐⭐ | 🟡 |
| 10 | How does Java achieve multiple inheritance? | ⭐⭐ | 🔴 |

### String Handling 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 11 | Why is String immutable in Java? | ⭐ | 🔴 |
| 12 | Difference between String, StringBuilder, StringBuffer? | ⭐ | 🔴 |
| 13 | What is String Pool? Where is it stored? | ⭐⭐ | 🔴 |
| 14 | How many objects created: `String s = new String("abc")`? | ⭐⭐ | 🔴 |
| 15 | Why is String a popular HashMap key? | ⭐⭐ | 🟡 |
| 16 | What is string interning? | ⭐⭐ | 🟡 |
| 17 | How does `String.intern()` work? | ⭐⭐⭐ | 🟢 |

### Exception Handling 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 18 | Difference between Checked and Unchecked exceptions? | ⭐ | 🔴 |
| 19 | Difference between `throw` and `throws`? | ⭐ | 🔴 |
| 20 | What is exception chaining? | ⭐⭐ | 🟡 |
| 21 | Can we have try without catch? | ⭐⭐ | 🟡 |
| 22 | What happens if exception in finally block? | ⭐⭐ | 🔴 |
| 23 | Try-with-resources - how does it work? | ⭐⭐ | 🔴 |
| 24 | Can we catch multiple exceptions in single catch? | ⭐⭐ | 🟡 |
| 25 | Create custom exception - checked vs unchecked? | ⭐⭐ | 🔴 |
| 26 | What is suppressed exception in try-with-resources? | ⭐⭐⭐ | 🟢 |

### Java 8+ Features 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 27 | What is a functional interface? Examples? | ⭐ | 🔴 |
| 28 | Explain lambda expressions with syntax | ⭐ | 🔴 |
| 29 | What is method reference? Types? | ⭐⭐ | 🔴 |
| 30 | Difference between Predicate, Function, Consumer, Supplier? | ⭐⭐ | 🔴 |
| 31 | What is Optional? Why use it? | ⭐⭐ | 🔴 |
| 32 | Optional best practices and anti-patterns? | ⭐⭐⭐ | 🟡 |
| 33 | What is default method in interface? Why added? | ⭐⭐ | 🔴 |
| 34 | What if two interfaces have same default method? | ⭐⭐ | 🟡 |
| 35 | Explain Stream API with examples | ⭐⭐ | 🔴 |
| 36 | Difference between map() and flatMap()? | ⭐⭐ | 🔴 |
| 37 | Intermediate vs Terminal operations? | ⭐⭐ | 🔴 |
| 38 | What is lazy evaluation in streams? | ⭐⭐ | 🟡 |
| 39 | Parallel streams - when to use, when to avoid? | ⭐⭐⭐ | 🔴 |
| 40 | What are Records in Java 14+? | ⭐⭐ | 🟡 |
| 41 | What are Sealed Classes? | ⭐⭐⭐ | 🟢 |
| 42 | Pattern matching for instanceof? | ⭐⭐ | 🟡 |

---

## Section 1.2: Java Collections 🔴

### List Interface

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 43 | ArrayList vs LinkedList - internal implementation? | ⭐⭐ | 🔴 |
| 44 | When to use ArrayList vs LinkedList? | ⭐⭐ | 🔴 |
| 45 | How does ArrayList grow? | ⭐⭐ | 🔴 |
| 46 | What is CopyOnWriteArrayList? When to use? | ⭐⭐⭐ | 🟡 |
| 47 | How to make ArrayList thread-safe? | ⭐⭐ | 🔴 |
| 48 | What is fail-fast vs fail-safe iterator? | ⭐⭐ | 🔴 |
| 49 | How does ConcurrentModificationException occur? | ⭐⭐ | 🔴 |

### Map Interface 🔴 (MOST ASKED)

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 50 | **Explain HashMap internals completely** | ⭐⭐⭐ | 🔴🔴🔴 |
| 51 | What is hashing? How hashCode() works? | ⭐⭐ | 🔴 |
| 52 | What happens when two keys have same hashCode? | ⭐⭐ | 🔴 |
| 53 | Why bucket converts to tree at threshold 8? | ⭐⭐⭐ | 🟡 |
| 54 | What is load factor? Default value? | ⭐⭐ | 🔴 |
| 55 | What happens during HashMap resize? | ⭐⭐⭐ | 🔴 |
| 56 | Why HashMap is not thread-safe? | ⭐⭐ | 🔴 |
| 57 | What happens if two threads put in HashMap simultaneously? | ⭐⭐⭐ | 🔴 |
| 58 | HashMap vs Hashtable vs ConcurrentHashMap? | ⭐⭐ | 🔴 |
| 59 | **ConcurrentHashMap internals** - segment locking vs node locking? | ⭐⭐⭐ | 🔴🔴 |
| 60 | How does ConcurrentHashMap achieve thread-safety without locking entire map? | ⭐⭐⭐ | 🔴 |
| 61 | LinkedHashMap - how does it maintain order? | ⭐⭐ | 🟡 |
| 62 | TreeMap internals - Red-Black tree? | ⭐⭐⭐ | 🟡 |
| 63 | WeakHashMap - use cases? | ⭐⭐⭐ | 🟢 |
| 64 | IdentityHashMap - when to use? | ⭐⭐⭐ | 🟢 |

### Set Interface

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 65 | HashSet internals - how does it work? | ⭐⭐ | 🔴 |
| 66 | LinkedHashSet vs HashSet vs TreeSet? | ⭐⭐ | 🔴 |
| 67 | How to implement equals() and hashCode() correctly? | ⭐⭐ | 🔴 |
| 68 | What if we don't override hashCode() when overriding equals()? | ⭐⭐ | 🔴 |
| 69 | ConcurrentSkipListSet - use case? | ⭐⭐⭐ | 🟢 |

### Queue Interface

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 70 | PriorityQueue internals - heap implementation? | ⭐⭐ | 🟡 |
| 71 | ArrayDeque vs LinkedList as Deque? | ⭐⭐ | 🟡 |
| 72 | BlockingQueue types - when to use which? | ⭐⭐⭐ | 🔴 |
| 73 | Difference between offer(), add(), put() in BlockingQueue? | ⭐⭐ | 🟡 |
| 74 | ArrayBlockingQueue vs LinkedBlockingQueue? | ⭐⭐⭐ | 🟡 |

---

## Section 1.3: Java Concurrency 🔴🔴 (GOLDMAN SACHS FOCUS)

### Thread Basics

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 75 | Thread vs Runnable vs Callable? | ⭐ | 🔴 |
| 76 | Thread lifecycle and states? | ⭐⭐ | 🔴 |
| 77 | What is daemon thread? | ⭐⭐ | 🟡 |
| 78 | What is thread priority? Does it guarantee execution order? | ⭐⭐ | 🟡 |
| 79 | How to stop a thread safely? | ⭐⭐ | 🔴 |
| 80 | What is thread starvation? | ⭐⭐ | 🟡 |

### Synchronization 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 81 | What is synchronized keyword? Method vs block level? | ⭐⭐ | 🔴 |
| 82 | What is monitor/intrinsic lock? | ⭐⭐ | 🔴 |
| 83 | **volatile keyword - what does it guarantee?** | ⭐⭐⭐ | 🔴🔴 |
| 84 | volatile vs synchronized? | ⭐⭐⭐ | 🔴 |
| 85 | Why volatile doesn't guarantee atomicity? | ⭐⭐⭐ | 🔴 |
| 86 | What is happens-before relationship? | ⭐⭐⭐ | 🟡 |
| 87 | What is memory visibility problem? | ⭐⭐⭐ | 🔴 |
| 88 | **What is deadlock? How to detect and prevent?** | ⭐⭐⭐ | 🔴🔴 |
| 89 | What is livelock? | ⭐⭐⭐ | 🟡 |
| 90 | What is race condition? How to avoid? | ⭐⭐ | 🔴 |

### Locks 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 91 | ReentrantLock vs synchronized? | ⭐⭐⭐ | 🔴 |
| 92 | What is lock fairness? | ⭐⭐⭐ | 🟡 |
| 93 | ReadWriteLock - when to use? | ⭐⭐⭐ | 🔴 |
| 94 | StampedLock - optimistic reading? | ⭐⭐⭐ | 🟢 |
| 95 | What is tryLock()? | ⭐⭐ | 🔴 |
| 96 | Condition interface - await() and signal()? | ⭐⭐⭐ | 🟡 |

### Executor Framework 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 97 | What is ExecutorService? Why use it? | ⭐⭐ | 🔴 |
| 98 | **ThreadPoolExecutor parameters - explain each** | ⭐⭐⭐ | 🔴🔴 |
| 99 | FixedThreadPool vs CachedThreadPool vs ScheduledThreadPool? | ⭐⭐⭐ | 🔴 |
| 100 | How to size a thread pool? CPU-bound vs IO-bound? | ⭐⭐⭐ | 🔴 |
| 101 | What is ForkJoinPool? Work-stealing algorithm? | ⭐⭐⭐ | 🟡 |
| 102 | Future vs CompletableFuture? | ⭐⭐⭐ | 🔴 |
| 103 | How to handle exceptions in ExecutorService? | ⭐⭐⭐ | 🟡 |
| 104 | shutdown() vs shutdownNow()? | ⭐⭐ | 🔴 |

### CompletableFuture 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 105 | What is CompletableFuture? Why added in Java 8? | ⭐⭐ | 🔴 |
| 106 | supplyAsync() vs runAsync()? | ⭐⭐ | 🔴 |
| 107 | thenApply() vs thenCompose() vs thenCombine()? | ⭐⭐⭐ | 🔴 |
| 108 | How to handle exceptions - exceptionally() vs handle()? | ⭐⭐⭐ | 🔴 |
| 109 | allOf() vs anyOf()? | ⭐⭐⭐ | 🟡 |
| 110 | What thread pool does CompletableFuture use by default? | ⭐⭐⭐ | 🟡 |
| 111 | How to timeout a CompletableFuture? | ⭐⭐⭐ | 🟡 |

### Atomic Classes & Concurrent Utilities

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 112 | AtomicInteger - how does it work? CAS? | ⭐⭐⭐ | 🔴 |
| 113 | What is Compare-And-Swap (CAS)? | ⭐⭐⭐ | 🔴 |
| 114 | AtomicReference - use case? | ⭐⭐⭐ | 🟡 |
| 115 | CountDownLatch - use case and example? | ⭐⭐⭐ | 🔴 |
| 116 | CyclicBarrier vs CountDownLatch? | ⭐⭐⭐ | 🔴 |
| 117 | Semaphore - how to use for rate limiting? | ⭐⭐⭐ | 🔴 |
| 118 | Phaser - use case? | ⭐⭐⭐ | 🟢 |
| 119 | Exchanger - use case? | ⭐⭐⭐ | 🟢 |

### Virtual Threads (Java 21) 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 120 | What are Virtual Threads (Project Loom)? | ⭐⭐⭐ | 🟡 |
| 121 | Virtual Threads vs Platform Threads? | ⭐⭐⭐ | 🟡 |
| 122 | When to use Virtual Threads? | ⭐⭐⭐ | 🟡 |
| 123 | Limitations of Virtual Threads? | ⭐⭐⭐ | 🟢 |

---

## Section 1.4: Java Memory Model & JVM 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 124 | JVM memory areas - Heap, Stack, Metaspace? | ⭐⭐ | 🔴 |
| 125 | Stack vs Heap memory? | ⭐⭐ | 🔴 |
| 126 | What is Metaspace? How different from PermGen? | ⭐⭐⭐ | 🟡 |
| 127 | What is garbage collection? | ⭐⭐ | 🔴 |
| 128 | GC algorithms - Serial, Parallel, CMS, G1, ZGC? | ⭐⭐⭐ | 🟡 |
| 129 | Young generation vs Old generation? | ⭐⭐ | 🟡 |
| 130 | What is Stop-the-World pause? | ⭐⭐⭐ | 🟡 |
| 131 | How to tune GC? | ⭐⭐⭐ | 🟢 |
| 132 | What is memory leak in Java? How to detect? | ⭐⭐⭐ | 🔴 |
| 133 | What causes OutOfMemoryError? Types? | ⭐⭐⭐ | 🔴 |
| 134 | What is thread dump? How to analyze? | ⭐⭐⭐ | 🟡 |
| 135 | What is heap dump? Tools to analyze? | ⭐⭐⭐ | 🟡 |

---

# PART 2: SPRING BOOT

## Section 2.1: Spring Core 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 136 | What is Dependency Injection? Types? | ⭐ | 🔴 |
| 137 | Constructor vs Setter injection - when to use? | ⭐⭐ | 🔴 |
| 138 | What is IoC Container? | ⭐⭐ | 🔴 |
| 139 | BeanFactory vs ApplicationContext? | ⭐⭐ | 🟡 |
| 140 | **Spring Bean Lifecycle - complete flow** | ⭐⭐⭐ | 🔴 |
| 141 | @PostConstruct and @PreDestroy? | ⭐⭐ | 🔴 |
| 142 | Bean Scopes - singleton, prototype, request, session? | ⭐⭐ | 🔴 |
| 143 | What happens if prototype bean injected into singleton? | ⭐⭐⭐ | 🔴 |
| 144 | @Component vs @Service vs @Repository vs @Controller? | ⭐⭐ | 🔴 |
| 145 | What is @Autowired? How does it work internally? | ⭐⭐ | 🔴 |
| 146 | @Qualifier vs @Primary? | ⭐⭐ | 🔴 |
| 147 | Circular dependency - how does Spring handle? | ⭐⭐⭐ | 🔴 |

## Section 2.2: Spring Boot Specifics 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 148 | What is Spring Boot? How different from Spring? | ⭐ | 🔴 |
| 149 | What is @SpringBootApplication? | ⭐⭐ | 🔴 |
| 150 | **How does auto-configuration work?** | ⭐⭐⭐ | 🔴 |
| 151 | What is spring.factories file? | ⭐⭐⭐ | 🟡 |
| 152 | @Conditional annotations - types and use? | ⭐⭐⭐ | 🟡 |
| 153 | How to disable specific auto-configuration? | ⭐⭐ | 🟡 |
| 154 | application.properties vs application.yml? | ⭐ | 🔴 |
| 155 | Spring profiles - how to use? | ⭐⭐ | 🔴 |
| 156 | @ConfigurationProperties vs @Value? | ⭐⭐ | 🔴 |
| 157 | What is Spring Boot Actuator? Endpoints? | ⭐⭐ | 🔴 |
| 158 | How to create custom Actuator endpoint? | ⭐⭐⭐ | 🟡 |
| 159 | Spring Boot starters - purpose? | ⭐⭐ | 🔴 |
| 160 | How to create custom starter? | ⭐⭐⭐ | 🟢 |

## Section 2.3: Spring MVC & REST 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 161 | Spring MVC request flow? | ⭐⭐ | 🔴 |
| 162 | DispatcherServlet role? | ⭐⭐ | 🔴 |
| 163 | @Controller vs @RestController? | ⭐ | 🔴 |
| 164 | @RequestMapping vs @GetMapping, @PostMapping? | ⭐ | 🔴 |
| 165 | @PathVariable vs @RequestParam vs @RequestBody? | ⭐⭐ | 🔴 |
| 166 | How to handle exceptions globally? @ControllerAdvice? | ⭐⭐ | 🔴 |
| 167 | @ResponseStatus annotation? | ⭐⭐ | 🟡 |
| 168 | How to validate request body? @Valid? | ⭐⭐ | 🔴 |
| 169 | Custom validator creation? | ⭐⭐ | 🟡 |
| 170 | Content negotiation - how does it work? | ⭐⭐ | 🟡 |
| 171 | CORS handling in Spring? | ⭐⭐ | 🔴 |
| 172 | How to handle file upload? | ⭐⭐ | 🟡 |

## Section 2.4: Spring Data JPA 🔴 (CARS24 ASKED)

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 173 | What is JPA? Hibernate vs JPA? | ⭐⭐ | 🔴 |
| 174 | What is Spring Data JPA? Benefits? | ⭐⭐ | 🔴 |
| 175 | JpaRepository vs CrudRepository vs Repository? | ⭐⭐ | 🔴 |
| 176 | How does query method naming work? | ⭐⭐ | 🔴 |
| 177 | @Query annotation - JPQL vs Native? | ⭐⭐ | 🔴 |
| 178 | **@Transactional - how does it work internally?** | ⭐⭐⭐ | 🔴🔴 |
| 179 | @Transactional propagation levels? | ⭐⭐⭐ | 🔴 |
| 180 | **@Transactional isolation levels?** (CARS24 asked) | ⭐⭐⭐ | 🔴🔴 |
| 181 | What is dirty read, phantom read, non-repeatable read? | ⭐⭐⭐ | 🔴 |
| 182 | @Transactional self-invocation problem? | ⭐⭐⭐ | 🔴 |
| 183 | **N+1 problem - what is it and how to solve?** | ⭐⭐⭐ | 🔴🔴 |
| 184 | Lazy vs Eager loading? | ⭐⭐ | 🔴 |
| 185 | LazyInitializationException - how to solve? | ⭐⭐⭐ | 🔴 |
| 186 | @EntityGraph - use case? | ⭐⭐⭐ | 🟡 |
| 187 | Optimistic vs Pessimistic locking? | ⭐⭐⭐ | 🔴 |
| 188 | @Version annotation - optimistic locking? | ⭐⭐⭐ | 🟡 |
| 189 | JPA Auditing - @CreatedDate, @LastModifiedDate? | ⭐⭐ | 🟡 |
| 190 | Pagination and Sorting in Spring Data? | ⭐⭐ | 🔴 |

## Section 2.5: Spring Security 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 191 | Spring Security filter chain? | ⭐⭐⭐ | 🟡 |
| 192 | Authentication vs Authorization? | ⭐ | 🔴 |
| 193 | How does Spring Security work? | ⭐⭐ | 🔴 |
| 194 | UserDetailsService interface? | ⭐⭐ | 🔴 |
| 195 | JWT authentication flow? | ⭐⭐⭐ | 🔴 |
| 196 | OAuth2 basics - when to use? | ⭐⭐⭐ | 🟡 |
| 197 | @PreAuthorize vs @Secured? | ⭐⭐ | 🟡 |
| 198 | CSRF protection - how does it work? | ⭐⭐ | 🟡 |
| 199 | How to disable CSRF for APIs? | ⭐⭐ | 🟡 |
| 200 | Method-level security? | ⭐⭐ | 🟡 |

## Section 2.6: Microservices with Spring 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 201 | What are microservices? Advantages/Disadvantages? | ⭐⭐ | 🔴 |
| 202 | Service Discovery - Eureka? | ⭐⭐⭐ | 🟡 |
| 203 | API Gateway pattern? Spring Cloud Gateway? | ⭐⭐⭐ | 🟡 |
| 204 | Circuit Breaker pattern? Resilience4j? | ⭐⭐⭐ | 🔴 |
| 205 | How does Circuit Breaker work? States? | ⭐⭐⭐ | 🔴 |
| 206 | Bulkhead pattern? | ⭐⭐⭐ | 🟡 |
| 207 | Retry pattern? | ⭐⭐⭐ | 🟡 |
| 208 | Distributed tracing - Spring Cloud Sleuth? | ⭐⭐⭐ | 🟡 |
| 209 | Config Server - centralized configuration? | ⭐⭐⭐ | 🟡 |
| 210 | Saga pattern for distributed transactions? | ⭐⭐⭐ | 🔴 |
| 211 | Event-driven architecture with Kafka? | ⭐⭐⭐ | 🔴 |

---

# PART 3: DATABASE & ORM

## Section 3.1: SQL & Database Concepts 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 212 | ACID properties? | ⭐⭐ | 🔴 |
| 213 | CAP theorem? | ⭐⭐⭐ | 🔴 |
| 214 | SQL joins - INNER, LEFT, RIGHT, FULL, CROSS? | ⭐⭐ | 🔴 |
| 215 | What is database indexing? Types? | ⭐⭐ | 🔴 |
| 216 | B-Tree vs B+ Tree index? | ⭐⭐⭐ | 🟡 |
| 217 | When NOT to use index? | ⭐⭐⭐ | 🟡 |
| 218 | What is query execution plan? EXPLAIN? | ⭐⭐⭐ | 🔴 |
| 219 | Database normalization - 1NF, 2NF, 3NF, BCNF? | ⭐⭐ | 🔴 |
| 220 | When to denormalize? | ⭐⭐⭐ | 🟡 |
| 221 | What is database sharding? | ⭐⭐⭐ | 🔴 |
| 222 | Horizontal vs Vertical scaling? | ⭐⭐ | 🔴 |
| 223 | Master-Slave replication? | ⭐⭐⭐ | 🔴 |
| 224 | Connection pooling - HikariCP? | ⭐⭐⭐ | 🔴 |

## Section 3.2: SQL vs NoSQL 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 225 | When to use SQL vs NoSQL? | ⭐⭐ | 🔴 |
| 226 | MongoDB vs PostgreSQL - use cases? | ⭐⭐⭐ | 🔴 |
| 227 | Redis - use cases? Data structures? | ⭐⭐⭐ | 🔴 |
| 228 | Redis vs Memcached? | ⭐⭐⭐ | 🟡 |
| 229 | Cassandra - when to use? | ⭐⭐⭐ | 🟢 |
| 230 | Elasticsearch - use cases? | ⭐⭐⭐ | 🟡 |

---

# PART 4: GOLANG

## Section 4.1: Go Basics 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 231 | Why Go? What problems does it solve? | ⭐ | 🔴 |
| 232 | Go vs Java - key differences? | ⭐⭐ | 🔴 |
| 233 | What is a package in Go? | ⭐ | 🔴 |
| 234 | Exported vs unexported identifiers? | ⭐ | 🔴 |
| 235 | Arrays vs Slices? | ⭐⭐ | 🔴 |
| 236 | How does slice grow internally? | ⭐⭐ | 🔴 |
| 237 | Maps in Go - how they work? | ⭐⭐ | 🔴 |
| 238 | Are maps thread-safe? How to make thread-safe? | ⭐⭐⭐ | 🔴 |
| 239 | Structs in Go - embedding? | ⭐⭐ | 🔴 |
| 240 | Interfaces in Go - implicit implementation? | ⭐⭐ | 🔴 |
| 241 | Empty interface - interface{}? | ⭐⭐ | 🔴 |
| 242 | Type assertion and type switch? | ⭐⭐ | 🔴 |
| 243 | Pointers in Go - when to use? | ⭐⭐ | 🔴 |
| 244 | Value receiver vs Pointer receiver? | ⭐⭐ | 🔴 |
| 245 | defer statement - execution order? | ⭐⭐ | 🔴 |
| 246 | panic and recover? | ⭐⭐ | 🔴 |
| 247 | Error handling in Go - best practices? | ⭐⭐ | 🔴 |
| 248 | init() function - execution order? | ⭐⭐ | 🟡 |
| 249 | new() vs make()? | ⭐⭐ | 🔴 |

## Section 4.2: Go Concurrency 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 250 | **What is a goroutine? How different from thread?** | ⭐⭐ | 🔴🔴 |
| 251 | How does Go scheduler work? G, M, P model? | ⭐⭐⭐ | 🔴 |
| 252 | How to start a goroutine? | ⭐ | 🔴 |
| 253 | **Channels - what are they? Types?** | ⭐⭐ | 🔴🔴 |
| 254 | Buffered vs Unbuffered channels? | ⭐⭐ | 🔴 |
| 255 | When does channel send/receive block? | ⭐⭐⭐ | 🔴 |
| 256 | How to close a channel? | ⭐⭐ | 🔴 |
| 257 | What happens if you send on closed channel? | ⭐⭐ | 🔴 |
| 258 | select statement - how does it work? | ⭐⭐⭐ | 🔴 |
| 259 | Default case in select? | ⭐⭐ | 🟡 |
| 260 | **Deadlock in Go - how does it occur?** | ⭐⭐⭐ | 🔴 |
| 261 | sync.WaitGroup - how to use? | ⭐⭐ | 🔴 |
| 262 | sync.Mutex vs sync.RWMutex? | ⭐⭐⭐ | 🔴 |
| 263 | When to use channels vs mutex? | ⭐⭐⭐ | 🔴 |
| 264 | sync.Once - use case? | ⭐⭐ | 🟡 |
| 265 | sync.Pool - use case? | ⭐⭐⭐ | 🟡 |
| 266 | context package - cancellation, timeouts? | ⭐⭐⭐ | 🔴 |
| 267 | context.WithCancel vs WithTimeout vs WithDeadline? | ⭐⭐⭐ | 🔴 |
| 268 | Goroutine leak - how to prevent? | ⭐⭐⭐ | 🔴 |

## Section 4.3: Go Patterns 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 269 | Worker pool pattern? | ⭐⭐⭐ | 🔴 |
| 270 | Fan-in, Fan-out pattern? | ⭐⭐⭐ | 🔴 |
| 271 | Pipeline pattern? | ⭐⭐⭐ | 🟡 |
| 272 | Generator pattern? | ⭐⭐⭐ | 🟡 |
| 273 | Rate limiting with Go? | ⭐⭐⭐ | 🔴 |
| 274 | Graceful shutdown in Go? | ⭐⭐⭐ | 🔴 |

## Section 4.4: Go Memory & Performance 🟡

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 275 | How does Go garbage collector work? | ⭐⭐⭐ | 🟡 |
| 276 | Stack vs Heap allocation in Go? | ⭐⭐⭐ | 🟡 |
| 277 | Escape analysis? | ⭐⭐⭐ | 🟢 |
| 278 | How to profile Go application? pprof? | ⭐⭐⭐ | 🟡 |
| 279 | GOMAXPROCS - what does it do? | ⭐⭐ | 🔴 |
| 280 | Race detector - how to use? | ⭐⭐ | 🔴 |

---

# PART 5: SYSTEM DESIGN CONCEPTS

## Section 5.1: Design Patterns 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 281 | **Singleton pattern - thread-safe implementation?** (Goldman asked) | ⭐⭐⭐ | 🔴🔴 |
| 282 | Factory pattern vs Abstract Factory? | ⭐⭐ | 🔴 |
| 283 | Builder pattern - when to use? | ⭐⭐ | 🔴 |
| 284 | Strategy pattern - example? | ⭐⭐ | 🔴 |
| 285 | Observer pattern - example? | ⭐⭐ | 🔴 |
| 286 | Decorator pattern - example? | ⭐⭐ | 🟡 |
| 287 | Adapter pattern - example? | ⭐⭐ | 🟡 |
| 288 | Proxy pattern - types? | ⭐⭐ | 🟡 |
| 289 | Template method pattern? | ⭐⭐ | 🟡 |
| 290 | Dependency Injection pattern? | ⭐⭐ | 🔴 |

## Section 5.2: Backend Concepts 🔴

| # | Question | Difficulty | Priority |
|---|----------|------------|----------|
| 291 | REST vs GraphQL vs gRPC? | ⭐⭐⭐ | 🔴 |
| 292 | REST best practices? | ⭐⭐ | 🔴 |
| 293 | API versioning strategies? | ⭐⭐ | 🔴 |
| 294 | Idempotency - what and why? | ⭐⭐⭐ | 🔴 |
| 295 | Rate limiting algorithms - Token Bucket, Leaky Bucket? | ⭐⭐⭐ | 🔴 |
| 296 | Caching strategies - Cache-aside, Write-through? | ⭐⭐⭐ | 🔴 |
| 297 | Cache invalidation strategies? | ⭐⭐⭐ | 🔴 |
| 298 | Message queues - Kafka vs RabbitMQ? | ⭐⭐⭐ | 🔴 |
| 299 | Event sourcing vs CRUD? | ⭐⭐⭐ | 🟡 |
| 300 | CQRS pattern? | ⭐⭐⭐ | 🟡 |

---

# PART 6: COMPANY-WISE QUESTION PATTERNS

## Service Companies (TCS, Infosys, Wipro)

Focus: Core Java basics, Collections, SQL, Spring basics

```
Most Asked:
1. OOP concepts with examples
2. String immutability
3. ArrayList vs LinkedList
4. HashMap basics (not internals)
5. Exception handling
6. Spring basics - DI, IoC
7. SQL joins
8. Basic CRUD operations
```

## Product Companies (Flipkart, Swiggy, Zomato)

Focus: Java internals, Concurrency, System Design

```
Most Asked:
1. HashMap internals - COMPLETE
2. ConcurrentHashMap internals
3. Thread pool sizing
4. @Transactional internals
5. N+1 problem
6. Circuit breaker pattern
7. Kafka basics
8. Caching strategies
```

## FAANG / Top Tier (Google, Amazon, Uber)

Focus: Advanced concurrency, Trade-offs, System Design depth

```
Most Asked:
1. CompletableFuture chains
2. Deadlock detection and prevention
3. Java Memory Model
4. Custom thread pool implementation
5. Distributed transactions
6. CAP theorem implications
7. Rate limiting implementation
8. Trade-off discussions
```

## Finance (Goldman Sachs, Morgan Stanley)

Focus: Concurrency, Low-latency, Memory management

```
Most Asked (Goldman Oct 2025):
1. Thread-safe Singleton - ALL implementations
2. volatile vs synchronized - DEEP
3. ThreadPoolExecutor parameters - EACH ONE
4. Deadlock scenarios and prevention
5. ConcurrentHashMap vs synchronized HashMap
6. Java Memory Model - happens-before
7. GC tuning basics
8. Lock-free programming concepts
```

---

# PART 7: INTERVIEW ANSWER TEMPLATES

## Template 1: HashMap Internals (The Gold Standard)

```
QUESTION: "Explain HashMap internals"

COMPLETE ANSWER (What interviewers want):

"HashMap uses an array of Node<K,V> as buckets. Here's how it works:

1. STORAGE STRUCTURE:
   - Array of buckets (Node<K,V>[])
   - Each Node has: hash, key, value, next
   - Default initial capacity: 16
   - Maximum capacity: 2^30

2. PUT OPERATION:
   - Calculate hash: hash = key.hashCode() ^ (h >>> 16)
   - Find bucket index: (n-1) & hash
   - If bucket empty, insert directly
   - If occupied, check for collision

3. COLLISION HANDLING:
   - Java 7: Linked list only
   - Java 8+: Linked list → Red-Black tree at threshold 8
   - Why 8? Poisson distribution - probability of 8 collisions is 0.00000006
   - Tree converts back to list at threshold 6

4. RESIZE (REHASHING):
   - Triggered when size > capacity * loadFactor
   - Default loadFactor: 0.75
   - New capacity = 2 * old capacity
   - All entries rehashed to new positions

5. THREAD SAFETY:
   - NOT thread-safe
   - Concurrent modification can cause infinite loop (Java 7)
   - Use ConcurrentHashMap for thread-safety

Time Complexity:
- Average: O(1) for get/put
- Worst case (all collisions): O(n) for list, O(log n) for tree"
```

## Template 2: @Transactional Internals

```
QUESTION: "How does @Transactional work?"

COMPLETE ANSWER:

"@Transactional works through AOP proxy mechanism:

1. PROXY CREATION:
   - Spring creates proxy around the bean
   - Either JDK dynamic proxy (interface) or CGLIB (class)
   - Proxy intercepts method calls

2. TRANSACTION FLOW:
   Before method:
   - Get connection from DataSource
   - Set autoCommit = false
   - Begin transaction

   After method (success):
   - Commit transaction
   - Return connection to pool

   On exception:
   - Rollback transaction
   - By default, only for RuntimeException

3. KEY ATTRIBUTES:
   - propagation: REQUIRED (default), REQUIRES_NEW, etc.
   - isolation: READ_COMMITTED (default)
   - rollbackFor: Exception classes to rollback
   - timeout: Transaction timeout

4. SELF-INVOCATION PROBLEM:
   - If method A calls method B in same class
   - B's @Transactional is IGNORED
   - Because call doesn't go through proxy
   - Solution: Inject self, or use AopContext

5. ISOLATION LEVELS:
   - READ_UNCOMMITTED: Dirty reads possible
   - READ_COMMITTED: No dirty reads
   - REPEATABLE_READ: No non-repeatable reads
   - SERIALIZABLE: No phantom reads"
```

## Template 3: Thread-Safe Singleton (Goldman Sachs)

```
QUESTION: "Implement thread-safe Singleton"

ANSWER - 4 APPROACHES:

1. SYNCHRONIZED METHOD (Simple, slow):
public class Singleton {
    private static Singleton instance;
    
    private Singleton() {}
    
    public static synchronized Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
// Problem: Synchronization overhead on EVERY call

2. DOUBLE-CHECKED LOCKING (Efficient):
public class Singleton {
    private static volatile Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {                 // First check (no lock)
            synchronized (Singleton.class) {
                if (instance == null) {         // Second check (with lock)
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
// Why volatile? Prevents instruction reordering
// Without volatile: Thread B might see partially constructed object

3. BILL PUGH (Recommended):
public class Singleton {
    private Singleton() {}
    
    private static class Holder {
        static final Singleton INSTANCE = new Singleton();
    }
    
    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}
// Uses class loading mechanism - lazy AND thread-safe

4. ENUM (Most robust):
public enum Singleton {
    INSTANCE;
    
    public void doSomething() { }
}
// Handles serialization, reflection attacks automatically
```

---

# PART 8: RESOURCES & REFERENCES

## Books

| Book | Topics | Priority |
|------|--------|----------|
| Effective Java (Joshua Bloch) | Best practices, Design | 🔴 |
| Java Concurrency in Practice | Concurrency, Threading | 🔴 |
| Designing Data-Intensive Applications | System Design, Databases | 🔴 |
| Spring in Action | Spring Framework | 🟡 |
| The Go Programming Language | Go fundamentals | 🟡 |

## Online Resources

| Resource | URL | Topics |
|----------|-----|--------|
| Baeldung | baeldung.com | Java, Spring |
| Java Brains (YouTube) | youtube.com/javabrains | Spring Boot |
| InterviewBit | interviewbit.com | All topics |
| GeeksforGeeks | geeksforgeeks.org | DSA, Java |
| Go by Example | gobyexample.com | Go |
| Go Blog | blog.golang.org | Go patterns |
| Effective Go | golang.org/doc/effective_go | Go best practices |
| Java Revisited | javarevisited.blogspot.com | Java, Concurrency |

## YouTube Channels

| Channel | Topics |
|---------|--------|
| Concept && Coding (Shrayansh) | LLD, HLD, Java |
| Java Brains | Spring, Microservices |
| Defog Tech | Java internals |
| Tech Dummies | Spring Boot |
| GopherCon | Go advanced |

## Practice Platforms

| Platform | Use |
|----------|-----|
| LeetCode | DSA |
| InterviewBit | Java + DSA |
| HackerRank | Java certification |
| Exercism | Go practice |

---

# PART 9: 30-DAY STUDY PLAN

## Week 1: Java Core + Collections

| Day | Topics | Questions |
|-----|--------|-----------|
| 1-2 | OOP, String, Exception | #1-26 |
| 3-4 | Collections - List, Set | #43-69 |
| 5-7 | HashMap, ConcurrentHashMap | #50-64 (DEEP) |

## Week 2: Concurrency

| Day | Topics | Questions |
|-----|--------|-----------|
| 8-9 | Threads, Synchronization | #75-90 |
| 10-11 | Locks, ExecutorService | #91-104 |
| 12-14 | CompletableFuture, Atomic | #105-123 |

## Week 3: Spring Boot

| Day | Topics | Questions |
|-----|--------|-----------|
| 15-16 | Spring Core, DI | #136-147 |
| 17-18 | Spring Boot, Auto-config | #148-160 |
| 19-21 | JPA, Transactions | #173-190 (DEEP) |

## Week 4: Golang + Integration

| Day | Topics | Questions |
|-----|--------|-----------|
| 22-24 | Go basics, Concurrency | #231-268 |
| 25-26 | Design Patterns | #281-290 |
| 27-28 | Backend Concepts | #291-300 |
| 29-30 | Revision + Mock | All P0 questions |

---

## FINAL CHECKLIST

Before any interview, verify you can answer:

```
JAVA CORE:
□ HashMap internals - COMPLETE (bucket, collision, resize, tree)
□ ConcurrentHashMap - segment vs node locking
□ equals() and hashCode() contract
□ String immutability reasons

CONCURRENCY:
□ volatile - visibility, NOT atomicity
□ synchronized vs ReentrantLock
□ ThreadPoolExecutor - ALL parameters
□ CompletableFuture - thenApply vs thenCompose
□ Deadlock - detect, prevent, example

SPRING:
□ @Transactional - proxy, self-invocation, isolation
□ Bean lifecycle - complete flow
□ N+1 problem - identify and solve
□ Auto-configuration mechanism

GOLANG:
□ Goroutine vs Thread
□ Channel blocking behavior
□ context package usage
□ select statement

DESIGN:
□ Singleton - ALL 4 implementations
□ Rate limiting algorithms
□ Caching strategies
```

---

*This document should be your primary reference. Master the 🔴 P0 questions first, then move to 🟡 P1.*

*Good luck with your interviews!*
