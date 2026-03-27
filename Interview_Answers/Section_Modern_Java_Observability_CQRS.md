# Modern Java + Observability + CQRS + Event Sourcing + DDD
# 2025–2026 Hiring Trends — SDE-2/SDE-3 Interview Guide
# For: Jayanti Vishnoi | 5.5 YOE GSTN | Java, Spring Boot

---

## PART 1: Java 17-21 Features (Asked in 2025-2026 Rounds)

---

### 1. Records (Java 14+, stable in Java 16)

**What it is:** Immutable data carrier. Replaces boilerplate POJO classes.

```java
// BEFORE (Java 8 style POJO):
public final class Point {
    private final int x;
    private final int y;
    public Point(int x, int y) { this.x = x; this.y = y; }
    public int x() { return x; }
    public int y() { return y; }
    @Override public boolean equals(Object o) { /* 10 lines */ }
    @Override public int hashCode() { /* 5 lines */ }
    @Override public String toString() { /* 3 lines */ }
}

// AFTER (Record):
public record Point(int x, int y) {}
// Compiler generates: constructor, accessors, equals, hashCode, toString
```

**Real-world use — API DTOs:**
```java
// Replace your Spring Boot DTOs with records
public record TaxReturnDto(
    String gstin,
    String period,
    BigDecimal taxLiability,
    LocalDateTime filedAt
) {}

// In controller:
@GetMapping("/returns/{gstin}")
public TaxReturnDto getReturn(@PathVariable String gstin) {
    return new TaxReturnDto(gstin, "2026-03", BigDecimal.TEN, LocalDateTime.now());
}
```

**Limitations:** Cannot extend classes. Cannot have mutable fields. Cannot be used as JPA entities (no no-arg constructor by default).

**Interview Q:** "How would you use Records in your API layer?"
→ "I'd use them for DTOs and value objects — anywhere I need immutable data transfer. Not for JPA entities since Hibernate needs mutable state. At GSTN, our request/response models would benefit from Records — removes ~200 lines of boilerplate."

---

### 2. Sealed Classes (Java 17)

**What it is:** Restrict which classes can extend/implement a type.

```java
// Model payment states — all possible states known at compile time
public sealed interface PaymentResult
    permits PaymentResult.Success, PaymentResult.Failure, PaymentResult.Pending {

    record Success(String transactionId, BigDecimal amount) implements PaymentResult {}
    record Failure(String reason, String errorCode) implements PaymentResult {}
    record Pending(String referenceId) implements PaymentResult {}
}

// Usage with pattern matching (exhaustive — compiler warns if case missing):
PaymentResult result = processPayment(request);
String message = switch (result) {
    case PaymentResult.Success s  -> "Paid ₹" + s.amount() + " (TxnId: " + s.transactionId() + ")";
    case PaymentResult.Failure f  -> "Failed: " + f.reason();
    case PaymentResult.Pending p  -> "Pending: " + p.referenceId();
};
```

**Why better than enums for complex states:** Enum variants can't carry different data. Sealed classes allow each variant to have its own fields.

**GSTN context:** Return filing states (Draft, Submitted, Filed, Rejected) with different data per state is a perfect sealed class use case.

---

### 3. Pattern Matching for instanceof (Java 16)

```java
// BEFORE:
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.toUpperCase());
}

// AFTER:
if (obj instanceof String s) {
    System.out.println(s.toUpperCase()); // s is already cast and available
}

// Combined with sealed classes in switch:
Object shape = getShape();
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t  -> 0.5 * t.base() * t.height();
    default          -> throw new IllegalStateException("Unknown shape");
};
```

---

### 4. Switch Expressions (Java 14)

```java
// Old switch (statement, fall-through bugs):
int day = 3;
String name;
switch (day) {
    case 1: name = "Mon"; break;
    case 2: name = "Tue"; break;
    default: name = "Other";
}

// New switch (expression, arrow syntax, no fall-through):
String name = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3, 4, 5 -> "Midweek";
    default -> "Weekend";
};

// With yield (for multi-line cases):
String result = switch (status) {
    case "FILED" -> {
        logFilingSuccess();
        yield "Return successfully filed";
    }
    default -> "Unknown status";
};
```

---

### 5. Text Blocks (Java 15)

```java
// SQL queries (no more + concatenation):
String query = """
    SELECT g.gstin, r.period, r.status
    FROM gst_returns r
    JOIN gstin_master g ON g.id = r.gstin_id
    WHERE r.status = 'PENDING'
      AND r.due_date < NOW()
    ORDER BY r.due_date
    """;

// JSON in tests:
String expectedJson = """
    {
        "gstin": "29ABCDE1234F1Z5",
        "period": "032026",
        "status": "FILED"
    }
    """;
```

---

### 6. Virtual Threads — Project Loom (Java 21) ⭐ MOST IMPORTANT

**The Problem with Platform Threads:**
```
Traditional thread-per-request model:
- 1 HTTP request → 1 OS thread
- OS thread: ~1MB stack memory
- Server with 8GB → max ~8000 concurrent threads
- Thread is BLOCKED during I/O (DB query, HTTP call, Kafka poll)
- CPU utilization low (threads sleeping while waiting for I/O)
- This is why reactive programming (WebFlux) was invented
```

**Virtual Threads solve this:**
```
Virtual threads:
- Lightweight: ~few KB each
- Managed by JVM, not OS
- When a virtual thread blocks on I/O → JVM parks it (not OS thread!)
- JVM carrier thread (OS thread) picks up another virtual thread
- You can have MILLIONS of virtual threads concurrently
- Code looks synchronous (no callbacks/reactive chains) — simpler!
```

```java
// Creating virtual threads:
Thread vt = Thread.ofVirtual().start(() -> System.out.println("Hello from virtual thread"));

// ExecutorService with virtual threads (Spring Boot 3.2+):
ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
executor.submit(() -> {
    // This thread blocks on DB query → JVM parks it, no OS thread wasted
    User user = userRepository.findById(id);
    return user;
});

// Spring Boot 3.2 — enable with single property:
spring.threads.virtual.enabled=true
// All request-handling threads become virtual threads automatically!
```

**When to use vs not use:**
```
USE Virtual Threads for:   IO-bound work (DB queries, HTTP calls, Kafka, file I/O)
DO NOT USE for:            CPU-bound work (image processing, encryption, computation)
                           → CPU-bound still needs OS threads with proper pool sizing

Your GSTN Kafka consumers:
  - IO-bound: wait for messages, write to DB, call downstream services
  - Virtual threads would allow more concurrent consumers with same heap
  - Switch: spring.threads.virtual.enabled=true in application.properties
```

**Interview Q:** "How would virtual threads change your Kafka consumer design?"
→ "Our consumers are IO-bound — they read messages, write to MySQL, publish to downstream Kafka topics. With virtual threads, we could run many more concurrent consumers without running out of OS threads. The code doesn't change — just enable spring.threads.virtual.enabled=true and Spring Boot handles the rest."

---

### 7. Structured Concurrency (Java 21 Preview)

```java
// Problem: launching multiple concurrent tasks and handling partial failures
// Old way: CompletableFuture chains (complex error handling)

// New way: StructuredTaskScope
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<UserProfile> userFuture   = scope.fork(() -> fetchUserProfile(userId));
    Future<OrderHistory> orderFuture = scope.fork(() -> fetchOrderHistory(userId));

    scope.join();           // wait for all
    scope.throwIfFailed();  // propagate first exception

    var profile = userFuture.resultNow();
    var orders  = orderFuture.resultNow();
    return new UserDashboard(profile, orders);
}
// If fetchUserProfile() fails → fetchOrderHistory() is cancelled automatically
// Clean, readable, correct error propagation
```

---

## PART 2: Spring Boot 3.x Modern Features

---

### Micrometer + Prometheus Integration

Spring Boot 3 auto-configures Micrometer. Prometheus metrics exposed at `/actuator/prometheus`.

```java
// Custom business metrics — add to your service:
@Service
public class ReturnFilingService {
    private final Counter filedCounter;
    private final Timer filingTimer;

    public ReturnFilingService(MeterRegistry registry) {
        this.filedCounter = Counter.builder("gst.returns.filed")
            .tag("type", "GSTR-1")
            .description("Total GST returns filed")
            .register(registry);

        this.filingTimer = Timer.builder("gst.returns.filing.duration")
            .description("Time to process a filing")
            .register(registry);
    }

    public FilingResult fileReturn(ReturnRequest request) {
        return filingTimer.record(() -> {
            FilingResult result = processFilingInternal(request);
            if (result.isSuccess()) filedCounter.increment();
            return result;
        });
    }
}
```

**Grafana dashboard queries:**
```
rate(gst_returns_filed_total[5m])                    → filings per second
histogram_quantile(0.99, gst_returns_filing_duration) → P99 latency
```

---

### Spring Boot 3 Observability (@Observed)

```java
// Auto-creates spans for distributed tracing + metrics
@Service
public class InvoiceService {

    @Observed(name = "invoice.validation",
              contextualName = "validate-invoice")
    public ValidationResult validate(Invoice invoice) {
        // This method is automatically traced + timed
        return doValidation(invoice);
    }
}

// application.properties — enable tracing export to Zipkin/Jaeger:
management.tracing.sampling.probability=1.0
management.zipkin.tracing.endpoint=http://zipkin:9411/api/v2/spans
```

---

### Spring Boot 3 + Virtual Threads

```properties
# application.properties — one line to enable
spring.threads.virtual.enabled=true

# This makes:
# - All Tomcat request threads → virtual threads
# - All @Async tasks → virtual threads
# - All scheduled tasks → virtual threads
```

---

### Spring Security 6 Lambda DSL

```java
// Old style (deprecated in Spring Security 6):
http.authorizeRequests()
    .antMatchers("/public/**").permitAll()
    .anyRequest().authenticated()
    .and().sessionManagement()
    .sessionCreationPolicy(SessionCreationPolicy.STATELESS);

// New style (Security 6 / Spring Boot 3):
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/public/**").permitAll()
            .anyRequest().authenticated()
        )
        .sessionManagement(session -> session
            .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
        )
        .build();
}
```

---

## PART 3: Observability — What Interviewers Now Ask in 2025-2026

### The Three Pillars

```
Metrics  → "What is the system doing?" (numbers over time)
Traces   → "Where did this request go?" (cross-service path)
Logs     → "What happened in detail?" (events with context)

These three together = full observability.
```

---

### Metrics — The RED Method

For every service, track:
- **R**ate — requests per second
- **E**rrors — error rate (%)
- **D**uration — latency (P50, P95, P99)

```java
// For your GSTN services, these are the critical metrics:
// Rate:     gst.filings.per.second
// Errors:   gst.validation.error.rate
// Duration: gst.filing.processing.p99

// USE method (for resources: CPU, DB connections):
// Utilization, Saturation, Errors
// DB connection pool: utilization (% used), saturation (queue depth), errors (timeouts)
```

---

### Distributed Tracing — Correlation IDs

```java
// Structured logging with correlation ID (using MDC — Mapped Diagnostic Context):

@Component
public class CorrelationFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        String correlationId = UUID.randomUUID().toString();
        MDC.put("correlationId", correlationId);
        ((HttpServletResponse) res).setHeader("X-Correlation-Id", correlationId);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();
        }
    }
}

// logback-spring.xml — include correlationId in every log line:
// [%X{correlationId}] %-5level %logger - %msg%n

// Now all logs for one request share the same correlationId
// Can grep logs: grep "abc123-def456" application.log → all logs for that request
```

**OpenTelemetry (vendor-neutral, the future):**
```java
// Spring Boot auto-configures if you add:
// spring-boot-starter-actuator + micrometer-tracing-bridge-otel + opentelemetry-exporter-zipkin

// All HTTP calls, Kafka messages, Redis operations get automatic spans
// Zero code change needed for standard libraries
```

---

### SLIs, SLOs, SLAs — Interview Framework

```
SLI (Service Level Indicator) = the actual metric
  e.g., "P99 latency of /api/file endpoint over last 30 days"

SLO (Service Level Objective) = your internal target
  e.g., "P99 latency < 200ms, 99.9% of the time"

SLA (Service Level Agreement) = contractual commitment to customers
  e.g., "We guarantee 99.9% uptime; penalties if breached"

Error Budget = SLO budget you can "spend" on downtime/slowness
  99.9% SLO → 0.1% error budget → 43.8 minutes downtime per month
  When error budget is exhausted → freeze feature work, focus on reliability
```

**Interview answer to "how would you monitor this system?":**
```
"I'd instrument with the RED method:
1. Rate: request counter via Micrometer, exported to Prometheus
2. Errors: 5xx counter, validation failure counter
3. Duration: histogram for P50/P95/P99

I'd add distributed tracing via OpenTelemetry — all cross-service calls get trace IDs.
For logs, structured JSON with correlationId in every line.

SLO: I'd set P99 < 200ms for the read path, 99.9% availability.
Alert: PagerDuty fires if P99 > 500ms for 5 consecutive minutes or error rate > 1%."
```

---

### "Your API is Slow — Diagnose It"

This is a classic SDE-3 question. Structured answer:

```
Step 1: Metrics — is it slow for all users or some?
  → Check Grafana: is P99 elevated? P50 fine but P99 bad? (tail latency issue)
  → By endpoint? By region? By user cohort?

Step 2: Tracing — where in the request is time spent?
  → Find a slow trace in Jaeger/Zipkin
  → Is it in our service or downstream (DB, Redis, external API)?

Step 3: If DB is slow → EXPLAIN the query
  → Full table scan? Missing index? N+1 queries?
  → Check slow query log: SET long_query_time=1

Step 4: If service is slow → Thread dump
  → jstack <pid> → look for threads in BLOCKED/WAITING state
  → All threads waiting on DB connection pool? → pool exhausted
  → DeadLock? → jstack shows "Found one Java-level deadlock"

Step 5: If GC is suspect → GC logs
  → -Xlog:gc* → look for long GC pauses
  → Is Old Gen full? → memory leak, heap dump analysis

Step 6: Fix + measure → did it improve?
```

---

## PART 4: CQRS + Event Sourcing (Apple Asked This Directly)

---

### CQRS — Command Query Responsibility Segregation

**The core idea:**
```
Traditional: same model for reads and writes
  → One User object: read it, write to it, query complex reports from it

CQRS: separate models for read and write
  Write side (Command):  handles mutations, validates business rules, emits events
  Read side (Query):     optimized read model, possibly denormalized, possibly cached

Why?
  → Read patterns and write patterns are often very different
  → Writes: strong consistency, business logic validation
  → Reads: might need complex aggregations, should be fast, can be eventually consistent
  → Scale independently: if reads >> writes (common), scale read side only
```

**Java CQRS implementation:**

```java
// COMMAND SIDE — write model
public interface Command {}
public record FileReturnCommand(String gstin, String period, ReturnData data) implements Command {}

public class ReturnCommandHandler {
    private final ReturnRepository writeRepo;       // MySQL — source of truth
    private final ApplicationEventPublisher events;

    public void handle(FileReturnCommand cmd) {
        // Validate business rules
        if (!isValidGstin(cmd.gstin())) throw new InvalidGstinException(cmd.gstin());

        // Persist to write store
        Return ret = Return.create(cmd.gstin(), cmd.period(), cmd.data());
        writeRepo.save(ret);

        // Publish domain event
        events.publishEvent(new ReturnFiledEvent(ret.getId(), cmd.gstin(), cmd.period()));
    }
}

// QUERY SIDE — read model (optimized for queries)
public class ReturnQueryService {
    private final ReturnReadRepository readRepo; // Separate read DB or denormalized view

    public ReturnSummaryView getDashboard(String gstin) {
        return readRepo.findSummaryByGstin(gstin); // Pre-computed, fast
    }

    public List<PendingReturn> getPendingReturns() {
        return readRepo.findAllPending(); // Optimized read index
    }
}

// Event handler updates read model:
@EventListener
public void on(ReturnFiledEvent event) {
    // Update denormalized read model
    ReturnReadModel view = new ReturnReadModel(event.gstin(), event.period(), "FILED");
    readRepo.save(view);
}
```

**GSTN context — perfect mapping:**
```
Command side: Filing service (GSTR-1 submission, validation, ARN generation)
Query side:   Dashboard service (taxpayer sees filing status, pending returns, ITC summary)

The filing (write) and dashboard (read) have COMPLETELY different patterns:
- Write: 500/sec peak, strong consistency, business validation
- Read: 10,000/sec, can be slightly stale, complex aggregations

This is exactly why CQRS would benefit GSTN.
```

**Anti-patterns — when NOT to use CQRS:**
```
DON'T use for:
- Simple CRUD apps (user preferences, config management)
- Small teams (CQRS adds operational complexity)
- When read/write patterns are similar
- When strict consistency everywhere is required (adds eventual consistency complexity)

DO use for:
- High read/write ratio difference (> 10:1)
- Complex domain logic on write side
- Need separate scaling of read and write
- Reporting/analytics on same data as transactional data
```

---

### Event Sourcing

**The core idea:**
```
Traditional: store current state
  UPDATE users SET balance = 950 WHERE id = 1   (previous balance gone!)

Event Sourcing: store events that led to state
  Event 1: AccountCreated(id=1, balance=1000)
  Event 2: MoneyDebited(id=1, amount=50, reason="coffee")

  Current state = replay all events
  balance = 1000 - 50 = 950 ✓

  Benefit: full audit trail, can reconstruct any past state, time travel debugging
```

**Java Event Sourcing — Bank Account example:**

```java
// Events (immutable facts)
public sealed interface AccountEvent permits
    AccountCreated, MoneyDeposited, MoneyWithdrawn, AccountClosed {

    record AccountCreated(String accountId, String owner, BigDecimal initialBalance) implements AccountEvent {}
    record MoneyDeposited(String accountId, BigDecimal amount, String reference) implements AccountEvent {}
    record MoneyWithdrawn(String accountId, BigDecimal amount, String reference) implements AccountEvent {}
}

// Aggregate — rebuilds state from events
public class BankAccount {
    private String accountId;
    private BigDecimal balance;
    private String owner;
    private boolean closed;
    private final List<AccountEvent> uncommittedEvents = new ArrayList<>();

    // Reconstitute from event history
    public static BankAccount reconstitute(List<AccountEvent> history) {
        BankAccount account = new BankAccount();
        history.forEach(account::apply);
        return account;
    }

    // Business operation
    public void withdraw(BigDecimal amount, String reference) {
        if (closed) throw new AccountClosedException();
        if (balance.compareTo(amount) < 0) throw new InsufficientFundsException();

        // Don't update state directly — create event
        var event = new AccountEvent.MoneyWithdrawn(accountId, amount, reference);
        apply(event);
        uncommittedEvents.add(event);
    }

    // Apply event (state transition — pure function)
    private void apply(AccountEvent event) {
        switch (event) {
            case AccountEvent.AccountCreated e -> {
                this.accountId = e.accountId();
                this.balance   = e.initialBalance();
                this.owner     = e.owner();
            }
            case AccountEvent.MoneyDeposited e -> this.balance = balance.add(e.amount());
            case AccountEvent.MoneyWithdrawn e -> this.balance = balance.subtract(e.amount());
            case AccountEvent.AccountClosed e  -> this.closed = true;
        }
    }
}

// Event Store (append-only)
public interface EventStore {
    void append(String aggregateId, List<AccountEvent> events, int expectedVersion);
    List<AccountEvent> load(String aggregateId);
    List<AccountEvent> loadFrom(String aggregateId, int fromVersion);
}
```

**Kafka as Event Store:**
```
Kafka is naturally append-only → perfect for event log.
With log compaction: retain latest event per aggregate ID.
Consumer groups replay from beginning to rebuild state → Event Sourcing built-in.

At GSTN: Kafka topics for return filing events are already event sourced!
  - ReturnDraftSaved event
  - ReturnSubmitted event
  - ReturnFiled event
  - ReturnRejected event

This is Event Sourcing without calling it that.
```

**Snapshot optimization:**
```
Problem: aggregate with 10,000 events takes long to reconstitute.
Solution: Periodic snapshot (every 100 events) + replay from snapshot.

EventStore: load snapshot(v900) + events(v900..current) → fast reconstitution
```

**When to choose Event Sourcing:**
```
USE when:
- Audit trail is mandatory (financial, government, healthcare)
- Need time-travel debugging
- Events are domain primitives (DDD fit)
- Complex event-driven workflows

DON'T USE when:
- Simple CRUD data
- Team unfamiliar with event-driven patterns
- Strong consistency required across aggregates
- Schema evolution is complex (events are immutable — changing schema is hard)
```

---

## PART 5: Domain-Driven Design (Stripe + Goldman Ask This)

---

### Core DDD Concepts

**Bounded Context:**
```
A boundary within which a domain model is consistent.
Same term = different meaning in different contexts.

GSTN example:
  Filing Context:    "Return" = document submitted by taxpayer
  Ledger Context:    "Return" = money returned/credited to taxpayer
  Notification Context: "Return" = trigger for sending SMS/email

Each context has its own model. They communicate via domain events or ACL (anti-corruption layer).
```

**Aggregates and Aggregate Root:**
```java
// Aggregate: cluster of domain objects treated as unit
// Aggregate Root: the single entry point — all external access goes through it
// Invariants are enforced at the aggregate root level

public class GstReturn { // Aggregate Root
    private final GstReturnId id;
    private final Gstin gstin;           // Value Object
    private final TaxPeriod period;      // Value Object
    private ReturnStatus status;
    private final List<InvoiceEntry> entries; // Child entities — access only via root
    private int version; // Optimistic locking

    // All business operations go through the root
    public void submit() {
        if (status != ReturnStatus.DRAFT) throw new InvalidStateTransitionException();
        validateEntries();
        this.status = ReturnStatus.SUBMITTED;
        registerEvent(new ReturnSubmittedEvent(id, gstin, period));
    }

    // Never expose mutable collection directly
    public List<InvoiceEntry> getEntries() { return Collections.unmodifiableList(entries); }
}
```

**Entities vs Value Objects:**
```java
// Entity: has identity (ID), mutable over time
public class TaxPayer {
    private TaxPayerId id;      // identity
    private String gstin;
    private Address address;    // can change — still same TaxPayer
}

// Value Object: no identity, defined by its value, immutable
public record Gstin(String value) {
    public Gstin {
        if (!value.matches("[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}"))
            throw new InvalidGstinException(value);
    }
}
// Two Gstins with same value are equal — no ID needed
```

**Domain Events:**
```java
// Something that happened in the domain (past tense)
public record ReturnFiledEvent(
    GstReturnId returnId,
    Gstin gstin,
    TaxPeriod period,
    LocalDateTime filedAt
) implements DomainEvent {}

// Events flow between bounded contexts via Kafka
// Filing Context → Kafka → Ledger Context (update ITC), Notification Context (send SMS)
```

**Repository Pattern:**
```java
// Abstracts persistence — domain doesn't know about DB
public interface GstReturnRepository {
    GstReturn findById(GstReturnId id);
    GstReturn findByGstinAndPeriod(Gstin gstin, TaxPeriod period);
    void save(GstReturn gstReturn);
}

// Implementation (infrastructure layer):
@Repository
public class JpaGstReturnRepository implements GstReturnRepository {
    private final GstReturnJpaRepository jpaRepo; // Spring Data JPA
    private final GstReturnMapper mapper;

    @Override
    public GstReturn findById(GstReturnId id) {
        return jpaRepo.findById(id.value())
            .map(mapper::toDomain)
            .orElseThrow(() -> new ReturnNotFoundException(id));
    }
}
```

---

## PART 6: 20 Interview Questions with Concise Answers

**Q1. What's new in Java 21 that excites you?**
→ "Virtual threads. They let us write simple synchronous code that scales like async. Our Kafka consumers are IO-bound — virtual threads mean we can run more without tuning thread pool sizes. One property to enable in Spring Boot 3.2."

**Q2. How would virtual threads change your Kafka consumer design?**
→ "Currently we have a fixed thread pool (10 threads × partition count). With virtual threads, each message handler can block freely without wasting OS threads. We'd set newVirtualThreadPerTaskExecutor for the Kafka consumer concurrency — same code, better resource usage."

**Q3. Explain CQRS and when you'd use it.**
→ "Separate models for reads and writes. Command side handles mutations with business logic. Query side is optimized for reads, possibly denormalized. Use when read/write patterns differ significantly. At GSTN, filing (write-heavy, strong consistency) vs dashboard (read-heavy, eventual consistency) is a natural CQRS fit."

**Q4. What is Event Sourcing and how does it differ from CQRS?**
→ "Event Sourcing stores events not state — current state is derived by replaying events. Audit trail is built-in. CQRS is about separate read/write models. They often go together but don't require each other. At GSTN, our Kafka return filing events are effectively Event Sourcing."

**Q5. What is a Bounded Context in DDD?**
→ "A boundary within which a domain model is consistent. 'Return' means different things in the Filing context vs Ledger context. Each context has its own model and language. They communicate via domain events or anti-corruption layers."

**Q6. How do you observe a slow API in production?**
→ "Check metrics first (Grafana): is P99 elevated for all endpoints or one? Check traces (Jaeger): where in the request is time spent? If DB: run EXPLAIN on slow queries. If service: thread dump for BLOCKED threads. If GC: check GC logs for long pauses."

**Q7. What are SLOs and why do they matter?**
→ "SLOs are internal reliability targets (e.g., P99 < 200ms, 99.9% uptime). They define the error budget. When budget is exhausted, feature work stops, reliability work starts. Prevents reliability from being an afterthought."

**Q8. What is OpenTelemetry?**
→ "Vendor-neutral observability framework. Standardizes how you instrument code for traces, metrics, and logs. You instrument once, export to any backend (Jaeger, Prometheus, Datadog). Spring Boot 3 auto-configures it."

**Q9. What is a Record in Java and what are its limitations?**
→ "Immutable data carrier. Compiler generates constructor, accessors, equals, hashCode, toString. Great for DTOs and value objects. Limitations: cannot extend classes, cannot have mutable fields, can't use as JPA entity."

**Q10. What are Sealed Classes useful for?**
→ "Restrict the type hierarchy at compile time. Use for modeling domain states where all possible variants are known (payment result, order status). Combined with pattern matching in switch gives exhaustive handling — compiler warns if you miss a case."

**Q11. How does the JVM handle virtual threads?**
→ "Virtual threads are JVM-managed, not OS-managed. When a virtual thread blocks on IO, JVM unmounts it from the carrier OS thread and parks it. The carrier thread picks up another virtual thread. This multiplexing allows millions of virtual threads with far fewer OS threads."

**Q12. When would you NOT use Event Sourcing?**
→ "Simple CRUD where audit isn't needed, when schema evolution would be very complex (events are immutable), when team lacks event-driven experience, when strict cross-aggregate consistency is required."

**Q13. What's the difference between a Domain Event and an Integration Event?**
→ "Domain event: happened within a bounded context, synchronous, part of the domain model. Integration event: crosses bounded context boundary, async via message broker, carries only necessary data for consumers."

**Q14. How does Spring Boot 3 make observability easier?**
→ "Auto-configures Micrometer (metrics), integrates with OpenTelemetry (traces), provides @Observed annotation for automatic method tracing. Expose metrics at /actuator/prometheus, traces to Zipkin/Jaeger — zero boilerplate."

**Q15. What is the Aggregate pattern and why does it matter?**
→ "Cluster of domain objects treated as a unit, with a single root. All external access goes through the root. Enforces consistency boundaries. Important because it tells you transaction boundaries — only one aggregate per transaction."
