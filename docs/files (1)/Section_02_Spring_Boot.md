# Section 02 — Spring Boot (Q26–Q60)

## Q26: How does Spring's IoC container and DI work under the hood?

**Answer:** Spring IoC manages bean lifecycle. At startup:
1. **Bean Definition Loading** — Scans @Component/@Service/@Repository/@Controller. Each becomes a BeanDefinition in BeanDefinitionRegistry.
2. **Dependency Resolution** — Resolves via constructor injection (preferred), setter, or field injection. Builds dependency graph, detects circular dependencies.
3. **Bean Creation** — Instantiates in dependency order. Applies BeanPostProcessors (how @Transactional, @Cacheable, AOP proxies work).

GSTN has ~200 beans. We mandate constructor injection: explicit dependencies, supports final fields (immutability), trivial to unit test (pass mocks in constructor).

### Follow-up: How does Spring handle circular dependencies?
Constructor injection: fails fast with `BeanCurrentlyInCreationException` — good, reveals design problems. Setter/field injection: three-level cache (singletonObjects → earlySingletonObjects → singletonFactories) injects partially initialized beans. Fragile if @PostConstruct depends on the other bean. Best: refactor to break the cycle.

---

## Q27: Explain @Transactional — how it works internally.

**Answer:** @Transactional creates a proxy around your bean. When a transactional method is called:
1. Proxy intercepts the call
2. Opens a DB transaction (via PlatformTransactionManager)
3. Calls your actual method
4. On success: commits. On RuntimeException: rolls back. On checked exception: commits (unless rollbackFor specified).

**Critical gotcha:** Self-invocation bypasses proxy. If method A() calls B() in the same class, and only B() has @Transactional, the transaction won't be created — the call goes through `this`, not the proxy.

**Propagation levels we use at GSTN:**
- `REQUIRED` (default): Join existing transaction or create new. Used for most service methods.
- `REQUIRES_NEW`: Suspend current, create new. GSTN's audit log always uses REQUIRES_NEW — audit must persist even if the main filing transaction rolls back.
- `MANDATORY`: Must run in existing transaction. Used for repository methods that should never be called outside a transaction.

**GSTN XA transactions:** Our ledger update touches Appeal DB + Ledger DB + Notification DB. We use Atomikos JTA for distributed XA transactions across these datasources. @Transactional with JtaTransactionManager coordinates 2-phase commit.

### Follow-up: What's the difference between @Transactional on class vs method?
Class-level applies to all public methods. Method-level overrides class-level. We put `@Transactional(readOnly = true)` on the class for read-heavy services, then override with `@Transactional` on mutation methods — this hints the DB to optimize read paths.

---

## Q28: Explain Spring Profiles and activation methods.

**Answer:** Profiles conditionally register beans and load config per environment.

**Activation methods (ALL of them):**
1. `spring.profiles.active=dev` in application.properties
2. Environment variable: `SPRING_PROFILES_ACTIVE=prod`
3. Command line: `--spring.profiles.active=staging`
4. Programmatic: `SpringApplication.setAdditionalProfiles("dev")`
5. `@ActiveProfiles("test")` in JUnit
6. In Kubernetes: env var in deployment YAML
7. `spring.profiles.default=dev` for fallback when no profile set

**Priority:** Command line > env variable > properties file.

**Profile-specific config:** `application-{profile}.yml` loaded when that profile is active. `application.yml` always loaded as base.

**Conditional beans:**
```java
@Configuration
@Profile("prod")
public class ProdCacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new RedisCacheManager(...);
    }
}

@Configuration
@Profile("dev")
public class DevCacheConfig {
    @Bean
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager();
    }
}
```

**GSTN profiles:** `dev`, `staging`, `uat`, `prod`. Each varies: DB URLs, Kafka clusters, Redis configs, rate limits, log levels.

### Follow-up: Can multiple profiles be active?
Yes. `spring.profiles.active=prod,filing-season` activates both. Properties merged; last profile wins on conflicts. We use `prod` + `filing-season` for increased thread pools during deadline periods.

---

## Q29: Explain @Value annotation and its gotchas.

**Answer:** @Value injects property values into bean fields.

```java
@Value("${gstn.filing.max-retry:3}")      // with default
private int maxRetry;

@Value("${gstn.cache.ttl-seconds}")        // required (fails if missing)
private long cacheTtlSeconds;

@Value("#{${gstn.rate-limits}}")           // SpEL expression
private Map<String, Integer> rateLimits;
```

**Gotchas:**
1. **Doesn't work on static fields** — DI is instance-level.
2. **Constructor injection:** Put @Value on constructor parameter, not field, when using constructor injection.
3. **Missing property without default** → `BeanCreationException` at startup. Always provide defaults for non-critical config.
4. **No runtime refresh** — value fixed after injection. For dynamic config, use @ConfigurationProperties + @RefreshScope.
5. **Type conversion:** Handles int, boolean, String automatically. Complex types need SpEL or custom converters.

**@Value vs @ConfigurationProperties:** @Value for 1-3 simple values. @ConfigurationProperties for 3+ related properties — binds entire prefix to a POJO, type-safe, validates with @Validated, IDE autocomplete. GSTN Kafka config uses `@ConfigurationProperties(prefix = "gstn.kafka")`.

---

## Q30: SLF4J + Logback configuration in Spring Boot.

**Answer:**
- **SLF4J** = API/facade. Code uses `LoggerFactory.getLogger(MyClass.class)`.
- **Logback** = Implementation. Spring Boot's default binding.

**Config file resolution:**
1. `logback-test.xml` (classpath, test scope)
2. `logback.xml`
3. `logback-spring.xml` ← **preferred** (supports `<springProfile>`, `<springProperty>`)

**Why logback-spring.xml?** Processed by Spring Boot (not raw Logback). Enables profile-conditional logging, property references from application.yml. Regular logback.xml loads before Spring context.

```xml
<configuration>
  <springProperty scope="context" name="APP_NAME" source="spring.application.name"/>
  
  <springProfile name="dev">
    <root level="DEBUG"><appender-ref ref="CONSOLE"/></root>
  </springProfile>
  
  <springProfile name="prod">
    <root level="WARN"><appender-ref ref="JSON_FILE"/></root>
    <logger name="com.gstn" level="INFO"/>
  </springProfile>
</configuration>
```

**GSTN logging architecture:**
- Dev: Console, DEBUG level, human-readable pattern.
- Prod: Rolling JSON files (LogstashEncoder) → ELK stack. WARN root, INFO for com.gstn.
- MDC: `traceId`, `gstin`, `requestId` in every log line via servlet filter.
- Async appender: 256 queue, discards DEBUG/TRACE at 80% capacity.

### Follow-up: How do you handle structured logging in microservices?
Every log line needs cross-service traceability. MDC (Mapped Diagnostic Context) is thread-local key-value store. Servlet filter sets `traceId` (from Spring Sleuth/Micrometer Tracing), `gstin`, `requestId`. Inter-service calls propagate traceId via HTTP headers. In Kibana, filter by traceId to see the full request journey across filing → validation → notification services.

---

## Q31: Spring Boot Actuator and monitoring.

**Answer:** Actuator exposes operational endpoints:
- `/actuator/health` — DB, Redis, Kafka connectivity. K8s liveness/readiness probes.
- `/actuator/metrics` — Micrometer → Prometheus. We track: request latency (p50/p95/p99), JVM heap, GC pauses, Kafka consumer lag, Redis hit ratio.
- `/actuator/info` — Git commit, build timestamp.

**Custom health indicator:**
```java
@Component
public class KafkaHealthIndicator implements HealthIndicator {
    public Health health() {
        try {
            adminClient.listTopics().names().get(5, SECONDS);
            return Health.up().withDetail("broker", bootstrapServers).build();
        } catch (Exception e) {
            return Health.down().withException(e).build();
        }
    }
}
```

**K8s integration:** Liveness (`/health/liveness`) — fail = pod restart. Readiness (`/health/readiness`) — fail = remove from load balancer. GSTN incident: Redis connection leak failed readiness, gracefully removed pod from LB — zero user impact while we investigated.

---

## Q32: Spring Security filter chain.

**Answer:** Chain of ~15 servlet filters. Key ones in order:
1. SecurityContextPersistenceFilter — loads auth from session
2. CsrfFilter — validates CSRF tokens
3. UsernamePasswordAuthenticationFilter — login forms
4. BearerTokenAuthenticationFilter — JWT/OAuth2
5. ExceptionTranslationFilter — auth exceptions → HTTP responses
6. FilterSecurityInterceptor — final access decision

**GSTN:** JWT-based stateless auth. Custom filter extracts GSTIN, role, permissions from JWT. Role-based access: ADMIN manages filings, TAXPAYER accesses only their own data. Rate limiting filter throttles per-GSTIN via Redis. Chose stateless JWT over sessions because GSTN runs across multiple K8s pods — session replication would be complex at our scale.

---

## Q33: Explain AOP (Aspect-Oriented Programming) in Spring.

**Answer:** AOP separates cross-cutting concerns (logging, security, transactions) from business logic.

**Concepts:**
- **Aspect:** The cross-cutting module (@Aspect class)
- **Pointcut:** WHERE to apply (expression matching methods)
- **Advice:** WHAT to do and WHEN (before, after, around)
- **Join Point:** The actual method being intercepted

**GSTN custom aspects:**
```java
@Aspect
@Component
public class AuditAspect {
    @Around("@annotation(AuditLog)")
    public Object audit(ProceedingJoinPoint joinPoint) throws Throwable {
        String method = joinPoint.getSignature().getName();
        String gstin = MDC.get("gstin");
        auditService.logEntry(gstin, method);
        try {
            Object result = joinPoint.proceed();
            auditService.logSuccess(gstin, method);
            return result;
        } catch (Exception e) {
            auditService.logFailure(gstin, method, e);
            throw e;
        }
    }
}
```

Used for: audit logging, performance monitoring, rate limiting, input sanitization. @Transactional itself is implemented via AOP proxy.

---

## Q34: Explain Spring Boot auto-configuration.

**Answer:** Spring Boot examines classpath and auto-configures beans. If `spring-boot-starter-data-jpa` is on classpath → auto-configures DataSource, EntityManagerFactory, TransactionManager.

**How it works:** `@EnableAutoConfiguration` triggers scanning of `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`. Each config class has `@ConditionalOnClass`, `@ConditionalOnMissingBean` — only activates if dependency exists AND you haven't defined your own bean.

**Customization:** Define your own @Bean to override auto-configured one. Or exclude: `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)`.

---

## Q35–Q60: Additional Spring Topics (Key Answers)

### Q35: @Bean vs @Component?
@Component: class-level, detected by component scan. @Bean: method-level in @Configuration class, returns the bean. Use @Bean when you need to configure a third-party class you can't annotate, or need complex initialization logic.

### Q36: Bean scopes?
- **Singleton** (default): one instance per container. GSTN services.
- **Prototype**: new instance per injection. Rare — use for stateful objects.
- **Request/Session**: web-scoped. Request-scoped for per-request caching.

### Q37: @RestController vs @Controller?
@RestController = @Controller + @ResponseBody on every method. Returns data (JSON) directly. @Controller returns view names (Thymeleaf/JSP). GSTN is pure REST API → all @RestController.

### Q38: Exception handling in Spring?
`@ControllerAdvice` + `@ExceptionHandler`. Global handler maps exceptions to HTTP responses. GSTN hierarchy: `FilingValidationException → 400`, `AuthException → 401`, `RateLimitException → 429`, `InternalException → 500`. Always return structured error JSON with error code, message, traceId.

### Q39: Spring Data JPA repositories?
Interface extending `JpaRepository<Entity, ID>`. Spring auto-implements CRUD methods. Query derivation from method name: `findByGstinAndStatus(String gstin, Status status)`. Custom queries: `@Query("SELECT f FROM Filing f WHERE f.period = :period AND f.status IN :statuses")`.

### Q40: How does @Cacheable work?
AOP-based. First call: executes method, caches result. Subsequent calls with same key: returns cached value, skips method. `@CacheEvict` removes entries. GSTN uses `@Cacheable(value="taxpayer", key="#gstin")` with Redis backend. TTL configured per cache via CacheManager.

### Q41: Property resolution order in Spring Boot?
17 levels, highest to lowest priority:
1. Command line args
2. System properties
3. Environment variables (SPRING_APPLICATION_JSON)
4. application-{profile}.properties
5. application.properties
6. @PropertySource
7. Default properties

GSTN: defaults in application.yml, overrides in application-{profile}.yml, secrets via K8s env vars.

### Q42: Explain Spring WebFlux.
Reactive, non-blocking web framework. Uses Project Reactor (Mono/Flux). Event loop model (Netty) — few threads handle many connections. Best for I/O-bound services with many concurrent connections. GSTN evaluated for filing status SSE (Server-Sent Events) but stuck with MVC — team expertise, ecosystem maturity, debugging complexity.

### Q43: How do you write integration tests in Spring Boot?
`@SpringBootTest` loads full context. `@DataJpaTest` for repository tests (auto-configures H2). `@WebMvcTest` for controller tests (MockMvc). TestContainers for real DB/Kafka/Redis in tests. GSTN uses TestContainers for integration tests against MySQL + Redis — catches issues that H2 misses.
