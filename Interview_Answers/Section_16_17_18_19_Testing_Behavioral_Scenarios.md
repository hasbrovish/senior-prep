# SECTIONS 16-19: TESTING, BEHAVIORAL, QUICK-FIRE, SCENARIOS — Interview Answers (Q249–Q296)
## With GSTN Codebase References

---

# SECTION 16: TESTING (Q249–Q256)

### Q249. Unit vs Integration vs E2E Testing?

**Answer:**

| Level | Scope | Speed | GSTN Example |
|-------|-------|-------|-------------|
| **Unit** | Single class/method in isolation | Fast (ms) | Test `Anx1aServiceImpl.processReturn()` with mocked repository |
| **Integration** | Multiple components together | Medium (sec) | Test Controller → Service → Repository with embedded DB |
| **E2E** | Full system including external dependencies | Slow (min) | Complete filing flow: taxpayer login → save GSTR1 → validate → submit |

**Testing Pyramid:** Many unit tests (70%), fewer integration (20%), fewest E2E (10%).

GSTN uses **TestNG 6.8.7** (not JUnit) — configured via `testng.xml` files in each module.

```xml
<!-- From BOLitigationWeb/testng.xml -->
<suite name="Suite">
    <test name="Test">
        <classes>
            <class name="com.gstn.litigation.test.SomeTest"/>
        </classes>
    </test>
</suite>
```

---

### Q250. Mocking — Mockito patterns?

**Answer:**

```java
// Mock dependencies
@Mock
private GspAuthToknLogRepository tokenRepo;

@InjectMocks
private AuthServiceImpl authService;

@BeforeMethod
public void setup() {
    MockitoAnnotations.initMocks(this);
}

@Test
public void testTokenValidation() {
    // Given
    when(tokenRepo.findByToken("abc123")).thenReturn(mockTokenEntity);
    
    // When
    boolean valid = authService.validateToken("abc123");
    
    // Then
    assertTrue(valid);
    verify(tokenRepo, times(1)).findByToken("abc123");
}
```

**Key annotations:**
- `@Mock` — Create mock instance
- `@Spy` — Partial mock (real methods unless stubbed)
- `@InjectMocks` — Auto-inject mocks into target class
- `@Captor` — Capture arguments for verification

---

### Q251. TDD — Test-Driven Development?

**Answer:**

**Red → Green → Refactor cycle:**
1. **Red** — Write a failing test for the desired behavior
2. **Green** — Write minimal code to make the test pass
3. **Refactor** — Clean up code while keeping tests green

```java
// Step 1: RED — test first
@Test
public void shouldRejectInvalidGSTIN() {
    ValidationResult result = validator.validateGSTIN("INVALID");
    assertFalse(result.isValid());
    assertEquals("GSTIN format invalid", result.getError());
}

// Step 2: GREEN — implement
public ValidationResult validateGSTIN(String gstin) {
    if (!gstin.matches("\\d{2}[A-Z]{5}\\d{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}")) {
        return ValidationResult.error("GSTIN format invalid");
    }
    return ValidationResult.valid();
}

// Step 3: REFACTOR — extract regex constant, improve naming
```

---

### Q252. TestNG vs JUnit?

**Answer:**

| Feature | TestNG (GSTN uses this) | JUnit 5 |
|---------|------------------------|---------|
| Annotations | `@Test`, `@BeforeMethod`, `@AfterMethod` | `@Test`, `@BeforeEach`, `@AfterEach` |
| XML config | `testng.xml` for suite/group definitions | `@Suite`, extensions |
| Parameterized | `@DataProvider` | `@ParameterizedTest` |
| Parallel | Built-in parallel execution | Extension model |
| Groups | `@Test(groups = {"smoke", "regression"})` | `@Tag("smoke")` |
| Dependency | `@Test(dependsOnMethods = {"login"})` | `@Order(1)` |

**Why GSTN uses TestNG:** Started before JUnit 5 existed. TestNG had better parameterized testing and group execution. Migration cost not justified.

---

### Q253. Code Coverage — What's meaningful?

**Answer:**

- **Line coverage:** Which lines were executed (most basic)
- **Branch coverage:** Were all if/else paths tested? (more useful)
- **Mutation testing:** Do tests fail when code is changed? (most rigorous)

**Targets:**
- 80%+ line coverage for business logic (validators, services)
- 100% coverage for security-critical code (authentication, authorization)
- Less emphasis on coverage for controllers (integration tests cover those)

**Tools:** JaCoCo (Java Code Coverage) integrated with Maven/SonarQube.

---

### Q254. Testing Microservices?

**Answer:**

1. **Contract Testing:** Consumer-driven contracts (Pact, Spring Cloud Contract)
   - ReturnAPI defines contract: "I call RegistrationAPI with GSTIN, expect taxpayer name back"
   - Provider verifies it satisfies the contract

2. **Component Testing:** Test one microservice with stubbed dependencies

3. **Integration Testing:** Test real HTTP calls between 2 services using TestContainers

4. **Chaos Testing:** Kill random pods during filing and verify system degrades gracefully

---

### Q255-Q256. Load Testing, Test Data Management

**Q255. Load Testing:**
- **JMeter/Gatling** for API load testing
- Simulate filing deadline: 200K concurrent users submitting GSTR1
- Measure: p95 response time < 2s, error rate < 0.1%
- Types: Load test → Stress test → Spike test → Soak test

**Q256. Test Data Management:**
- Anonymized production data for performance testing
- Builders for unit test data: `TestDataBuilder.aReturn().withGSTIN("29...").build()`
- Separate test databases per developer/pipeline
- Cleanup: `@AfterMethod` or transactional rollback

---

# SECTION 17: BEHAVIORAL (Q257–Q266)

### Q257. Tell me about yourself?

**Answer:**

"I'm Jayanti Vishnoi, a Specialist Programmer L2 at Infosys with 5.5 years of experience. I've worked on two major projects:

**1. GSTN (Goods & Services Tax Network) — 4.5 years:**
I work on India's GST platform serving 14M+ taxpayers. I develop and maintain microservices using Spring Boot, Hibernate, Kafka, Redis, and MySQL. I've contributed to multiple modules — Return Filing, Back-Office Services, Litigation, Registration, and user management. My work spans the full stack from REST API development to database optimization and distributed caching.

**2. Infosys MarketPlace — 1 year:**
Built a marketplace application using Go, MongoDB, and GraphQL. This gave me experience with polyglot programming and NoSQL databases.

I'm particularly strong in backend architecture, performance optimization, and building scalable systems that handle high traffic during filing deadlines."

---

### Q258. Most challenging technical problem?

**Answer:**

"During a GSTR1 filing deadline, we observed response times spiking from 200ms to 15 seconds. The system was handling 200K+ concurrent users.

**Root cause analysis:**
1. Thread dumps showed threads blocked on database connections
2. HikariCP pool was exhausted (max 50 connections, all active)
3. Slow queries identified — full table scans on the `invoice` table

**Solution:**
1. **Immediate:** Added database index on `(gstin, return_period)` — query time dropped from 8s to 50ms
2. **Short-term:** Increased HikariCP pool to 100 connections with proper timeout configuration
3. **Long-term:** Implemented Redis caching for frequently accessed taxpayer data using `DistCacheUtil` — cache hit rate reached 85%

**Result:** Response times dropped to 150ms. System handled the filing deadline with zero downtime."

---

### Q259. Conflict with a team member?

**Answer:**

"A fellow developer wanted to use a stored procedure for complex return computation, arguing it would be faster. I advocated for implementing it in the Java service layer because:

1. Stored procedures are hard to unit test
2. They bypass our Spring transaction management
3. They're harder to version control and deploy
4. We couldn't leverage our existing caching layer

**Approach:** I prepared benchmarks comparing both approaches with realistic data volumes. The Java implementation with Redis caching actually outperformed the stored procedure by 3x because the cache hit rate was 90%.

**Outcome:** We went with the Java approach. The developer appreciated the data-driven decision. We established a team guideline: keep business logic in the application layer, use stored procedures only for complex data migrations."

---

### Q260-Q266. Leadership, Deadline, Learning, Failure, Architecture, Impact, Growth

**Q260. Taking initiative:**
"I noticed our deployment process was manual and error-prone — 2 hours per service. I proposed and implemented Jenkins CI/CD pipelines with automated testing. Deployment time reduced to 15 minutes. This was adopted across all services."

**Q261. Handling tight deadlines:**
"During the annual return filing (GSTR-9) launch, we had 3 weeks to implement and test major validation changes. I broke the work into daily milestones, coordinated parallel work across 4 developers, and ran daily testing sessions. We delivered 2 days early."

**Q262. Learning a new technology:**
"When GSTN migrated from Spring 4 to Spring Boot 2, I spent weekends learning the auto-configuration mechanism. I created the `gst-spring-boot2-starter` custom starter with spring.factories, helping the team migrate 20+ services. I documented the migration guide and conducted knowledge-sharing sessions."

**Q263. A mistake and what you learned:**
"I once deployed a Redis caching change to production that didn't include proper TTL settings. The cache grew unbounded and eventually caused OOM. Lesson: Always set TTL on cached data. I added a code review checklist item for cache TTL and created a utility method `setWithTTL()` that enforces TTL as a required parameter."

**Q264. Architecture decision:**
"I drove the decision to implement state-based database routing using `RoutingDataSource`. Instead of one massive database, we route queries based on GSTIN prefix (state code). This improved query performance by 5x and enabled horizontal scaling per state."

**Q265. Biggest impact:**
"Implementing the distributed caching layer with `DistCacheUtil`. It had the single biggest impact on system performance — reduced database load by 60%, improved average response time by 3x, and saved significant infrastructure cost by requiring fewer database read replicas."

**Q266. Where do you see yourself in 3-5 years:**
"I want to grow into a **Technical Architect** role. I'm actively building depth in distributed systems, cloud architecture, and system design. At GSTN, I've already started architecting solutions end-to-end. I'm looking for a role where I can own the technical direction of critical services while mentoring junior developers."

---

# SECTION 18: QUICK-FIRE / CONCEPTUAL (Q267–Q286)

### Q267. Explain polymorphism?
**Runtime polymorphism:** Method overriding — subclass provides specific implementation of parent class method. `List<Animal> animals` can contain Dog, Cat — calling `animal.speak()` invokes the correct implementation. **Compile-time:** Method overloading — same method name, different parameters.

### Q268. Abstract class vs Interface?
| | Abstract Class | Interface |
|--|---|---|
| Methods | Can have concrete methods | All abstract (before Java 8), default methods (Java 8+) |
| State | Can have instance fields | Only constants |
| Multiple | Single inheritance | Multiple implementation |
| Constructor | Yes | No |
| Use | "IS-A" + shared code | "CAN-DO" capability |

### Q269. SOLID Principles?
- **S:** Single Responsibility — `ReturnService` handles returns only, not payments
- **O:** Open/Closed — Extend via new validators, don't modify existing ones
- **L:** Liskov Substitution — Any `Validator` subtype works where `Validator` is expected
- **I:** Interface Segregation — `Readable`, `Writable` instead of one fat `CRUD` interface
- **D:** Dependency Inversion — Service depends on `Repository` interface, not `JdbcRepository` impl

### Q270. What is dependency injection?
Instead of a class creating its own dependencies (`new JdbcUserRepo()`), the framework **injects** them. Spring does this via `@Autowired` / constructor injection. Benefits: testability (inject mocks), loose coupling, configurability.

### Q271. REST constraints?
Client-Server, Stateless, Cacheable, Uniform Interface, Layered System, Code on Demand (optional).

### Q272. CAP theorem?
In a network partition (P), you must choose **Consistency** (C) or **Availability** (A). GSTN: CP for payment ledger (consistency critical), AP for dashboard reads (eventual consistency OK).

### Q273. ACID vs BASE?
| ACID | BASE |
|------|------|
| Atomicity, Consistency, Isolation, Durability | Basically Available, Soft state, Eventually consistent |
| Relational DB (MySQL) | NoSQL (MongoDB, Redis) |
| Strong consistency | High availability |

### Q274. Microservices vs Monolith?
Monolith: Single deployable unit, simple. Microservices: Independent services, complex but scalable. GSTN evolved from monolith → ~20 microservices.

### Q275. Circuit Breaker?
Prevents cascading failures. States: **Closed** (flowing) → **Open** (blocked, return fallback) → **Half-Open** (test a few requests). Implemented via Resilience4j/Hystrix.

### Q276. Event Sourcing?
Store **events** instead of current state. Replay to reconstruct state. Kafka topics as event log. Benefit: full audit trail, temporal queries. GSTN Kafka events for return filing status changes.

### Q277. CQRS?
Command Query Responsibility Segregation — separate read and write models. Writes to MySQL, reads from Redis/Solr. GSTN's dashboard reads from cache while filing writes to DB.

### Q278. Idempotency?
Same request executed multiple times produces same result. How: unique request ID, check before processing. Critical for payments — prevent double debit.

### Q279. 12-Factor App principles?
1. Codebase (git), 2. Dependencies (pom.xml), 3. Config (externalized), 4. Backing services (treat as resources), 5. Build/release/run, 6. Stateless processes, 7. Port binding, 8. Concurrency, 9. Disposability, 10. Dev/prod parity, 11. Logs (streams), 12. Admin processes.

### Q280. Blue-Green Deployment?
Two identical environments. Deploy to Green (inactive). Test. Switch traffic. If issues, switch back to Blue. Zero-downtime deployment.

### Q281. Canary Deployment?
Route 5% traffic to new version. Monitor errors/latency. If OK, gradually increase to 100%. If problems, route all traffic back to old version.

### Q282. Feature Flags?
Toggle features without deployment. `if (featureFlags.isEnabled("new-gstr1-validation"))`. Enable for specific states first, then nationally.

### Q283. Strangler Pattern?
Migrate monolith to microservices incrementally. Route specific endpoints to new service while rest stays in monolith. Eventually, monolith is fully replaced.

### Q284. Saga Pattern?
Distributed transaction across microservices. Choreography: events trigger next step. Orchestration: central coordinator manages steps. Compensating transactions on failure.

### Q285. Bulkhead Pattern?
Isolate failures. Separate thread pools per dependency. If PaymentService is slow, it uses its own thread pool — doesn't affect ReturnService thread pool.

### Q286. Sidecar Pattern?
Attach a helper container alongside main container. Handles cross-cutting: logging, monitoring, proxy (Envoy/Istio). Main container focuses on business logic.

---

# SECTION 19: SCENARIO-BASED (Q287–Q296)

### Q287. Production memory leak — how do you debug?

**Answer:**

```
Step 1: DETECT
  - Monitor: GC time increasing, heap usage growing, OOM errors
  - Alert: CloudWatch/Prometheus alert on JVM heap > 85%

Step 2: CAPTURE
  - jmap -dump:live,format=b,file=heap.hprof <PID>
  - Or: -XX:+HeapDumpOnOutOfMemoryError (preconfigured)
  
Step 3: ANALYZE
  - Load heap dump in Eclipse MAT (Memory Analyzer Tool)
  - Check "Leak Suspects" report
  - Look for: retained heap, dominator tree

Step 4: COMMON CAUSES
  - Unclosed streams/connections (DB, HTTP)
  - Growing collections (unbounded cache without TTL)
  - Static collections holding references
  - ThreadLocal not cleaned up
  - Listeners/callbacks not deregistered

Step 5: FIX (GSTN example)
  - Found: DistCacheUtil local map growing without eviction
  - Fix: Added TTL + max-size eviction policy
  - Verify: Monitor heap after deployment
```

---

### Q288. API response time degraded from 200ms to 5 seconds?

**Answer:**

```
1. NARROW THE SCOPE
   - Is it one API or all APIs? → Check if common dependency (DB, Redis)
   - Is it one pod or all pods? → If one, likely pod-level issue
   - When did it start? → Correlate with recent deployment

2. CHECK EACH LAYER (top to bottom)
   - Network: Any DNS issues, timeouts?
   - Load Balancer: Uneven distribution?
   - Application: Thread dumps — where are threads blocked?
   - Database: Slow query log (queries > 1s)
   - Cache: Redis latency, connection count
   - External services: Any dependency degraded?

3. GSTN-SPECIFIC ACTIONS
   - Check HikariCP pool: GET /actuator/hikaricp → active/idle/waiting
   - Check Redis: redis-cli info → connected_clients, used_memory
   - Check Kafka consumer lag: if events backing up
   - Check GC: -Xloggc → is GC pausing the application?

4. TYPICAL RESOLUTION
   - Missing index: EXPLAIN query → add index
   - Connection pool exhausted: adjust pool size + timeout
   - N+1 query: add @BatchSize or JOIN FETCH
   - Cache miss storm: warm cache before peak
```

---

### Q289. Database connection pool exhaustion?

**Answer:**

```java
// Symptoms: "HikariPool-1 - Connection is not available, request timed out"

// Diagnosis:
// 1. Check active connections
SELECT * FROM information_schema.processlist WHERE db = 'gstn_db';

// 2. Check pool metrics via actuator
// HikariCP metrics: active=50, idle=0, pending=200, total=50

// Root Causes:
// a) Long-running queries holding connections
// b) Missing @Transactional causing connection not returned
// c) Pool too small for traffic

// Fix:
spring:
  datasource:
    hikari:
      maximum-pool-size: 100      # Was 50
      connection-timeout: 5000     # Fail fast instead of waiting forever
      max-lifetime: 1800000        # 30 minutes
      leak-detection-threshold: 30000  # Log warning if connection held > 30s
```

---

### Q290. Kafka consumer lag increasing?

**Answer:**

```
1. CHECK LAG
   kafka-consumer-groups.sh --describe --group return-filing-group
   → Shows: CURRENT-OFFSET, LOG-END-OFFSET, LAG

2. ROOT CAUSES
   a) Slow processing (DB calls in consumer loop)
   b) Too few partitions/consumers
   c) Large message size
   d) Consumer rebalancing storm

3. FIXES
   a) Batch processing: poll 500 messages, batch-insert into DB
   b) Increase partitions + consumer instances (1:1 mapping)
   c) Compress messages (snappy/lz4)
   d) increase max.poll.interval.ms to prevent unnecessary rebalance
   e) Move heavy processing to async: consume → put in local queue → process in separate thread pool
```

---

### Q291. Redis cache inconsistency with database?

**Answer:**

```
Problem: User updates profile in DB, but cache still has old data.

Strategies:
1. CACHE-ASIDE (GSTN uses this):
   Write: Update DB → Delete cache key (don't update cache)
   Read: Check cache → miss → query DB → write to cache

   Why delete not update? Prevents race condition where stale data overwrites.

2. Write-Through: Write DB + cache atomically. Consistent but slower.

3. TTL as safety net: Even if invalidation fails, data expires in X minutes.

4. Event-driven invalidation:
   DB change → Kafka event → Cache invalidation consumer
   
GSTN implementation: DistCacheUtil.remove(key) after DB update + TTL of 15 minutes.
```

---

### Q292-Q296. Deployment Failure, Concurrent Filing, Cross-team Integration, Security Breach, Scale 10x

**Q292. Deployment caused production issues?**
1. Detect: Monitoring alerts (5xx spike, error rate > 1%)
2. **Immediate rollback:** Switch ALB to previous version (Blue-Green)
3. Investigate in staging: Reproduce with production traffic sample
4. Fix, add regression test, deploy to staging first
5. Post-mortem: Document root cause, add to checklist

**Q293. Two taxpayers filing simultaneously for same GSTIN?**
```
Problem: Race condition — both read "no return filed", both submit.
Solution:
1. Distributed lock: Redis SETNX on key "filing:{gstin}:{period}"
2. Lock TTL: 5 minutes (auto-expire on crash)
3. Optimistic locking: @Version field on return entity
4. DB unique constraint: (gstin, return_period, return_type)
```

**Q294. Cross-team Integration challenges?**
- API contract first: Define OpenAPI spec before implementation
- Consumer-driven contracts: Each team writes tests against expected API
- Integration environment: Shared staging for cross-service testing
- Regular sync meetings + Slack channel for integration issues

**Q295. Security breach response?**
```
1. CONTAIN: Isolate affected service, revoke compromised credentials
2. ASSESS: Determine scope — what data was accessed?
3. BLOCK: Block attacker IPs, rotate API keys
4. NOTIFY: Inform security team, management, affected users (per compliance)
5. FIX: Patch vulnerability, add WAF rules
6. POST-MORTEM: Root cause analysis, strengthen security controls
7. AUDIT: Review access logs, check for lateral movement
```

**Q296. Scale system to handle 10x traffic?**
```
Current: 200K concurrent users
Target: 2M concurrent users

Horizontal scaling:
  - Auto-scale pods from 50 → 500 (HPA based on CPU/custom metrics)
  - Scale DB read replicas from 2 → 10
  - Scale Redis cluster from 6 → 30 nodes

Vertical optimization:
  - Add database indexes for hot queries
  - Increase cache TTL to reduce DB hits
  - Connection pool tuning (maxPool per service)
  - Async processing: move non-critical operations to Kafka

Architecture changes:
  - CDN for static assets (offload 40% of requests)
  - Rate limiting per GSTIN (prevent abuse)
  - Read/write separation (CQRS)
  - Database sharding by state (already implemented)
  - Pre-compute dashboard data (materialized views)
  - Queue-based load leveling for burst traffic
```

---

## END OF ALL 296 QUESTIONS

**Files created:**
1. `Section_01_Java_Core.md` — Q1-Q25
2. `Section_02_Spring_Boot.md` — Q26-Q75
3. `Section_03_Hibernate_JPA.md` — Q76-Q90
4. `Section_04_05_06_Microservices_Kafka_Redis.md` — Q91-Q135
5. `Section_07_08_Database_DistributedSystems.md` — Q136-Q165
6. `Section_09_10_11_Patterns_Docker_CICD.md` — Q166-Q205
7. `Section_12_13_14_15_Cloud_Network_Design_Go.md` — Q206-Q248
8. `Section_16_17_18_19_Testing_Behavioral_Scenarios.md` — Q249-Q296
