# SECTION 2: SPRING BOOT — Interview Answers (Q26–Q75)
## With GSTN Codebase References — HIGHEST WEIGHTAGE

---

## 2.1 Core Concepts

### Q26. How does Spring Boot auto-configuration work? What role do @Conditional annotations play?

**Answer:**

Spring Boot auto-configuration automatically configures beans based on **what's on the classpath** and **what properties are set**.

**How it works internally:**

1. `@SpringBootApplication` includes `@EnableAutoConfiguration`
2. Spring reads `META-INF/spring.factories` file → lists all auto-configuration classes
3. Each auto-config class uses `@Conditional` annotations to decide if it should activate
4. Beans are registered only when conditions are met

**GSTN's custom spring.factories:**
```properties
# From gst-spring-boot2-starter/src/main/resources/META-INF/spring.factories
org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
  org.gst.framework.starter.autoconfigure.cache.CacheFrameworkAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.cache.CacheAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.datasource.CoreStaticMasterDataSourceAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.datasource.DataSourceAutoConfig,\
  org.gst.framework.starter.autoconfigure.log.LogAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.security.FoSecurityAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.security.BoSecurityAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.kafka.KafkaClientAutoConfiguration,\
  org.gst.framework.starter.autoconfigure.util.GstUtilsAutoConfiguration

org.springframework.boot.env.EnvironmentPostProcessor=\
  org.gst.framework.starter.autoconfigure.env.GstEnvironmentPostProcessor
```

**@Conditional annotations used in GSTN:**

```java
// From DataSourceAutoConfig.java — only activate if DataSource and JPA are on classpath
@ConditionalOnClass({DataSource.class, LocalContainerEntityManagerFactoryBean.class})

// From BoSecurityAutoConfiguration.java — only if property is set
@ConditionalOnProperty(prefix = "gst.security.bo", name = "enabled", 
                       havingValue = "true", matchIfMissing = false)

// From LogAutoConfiguration.java — only if AspectJ is available
@ConditionalOnClass({ Aspect.class })
@ConditionalOnProperty(prefix = "gst.logging", name = "enabled", 
                       havingValue = "true", matchIfMissing = true)

// From SessionRedisConfig.java — only if Redis session caching is enabled
@ConditionalOnProperty(prefix = "gst.cache.redis.session", name = "enabled", 
                       havingValue = "true", matchIfMissing = false)
```

**Key @Conditional annotations:**
| Annotation | Condition |
|------------|-----------|
| `@ConditionalOnClass` | Class exists on classpath |
| `@ConditionalOnMissingClass` | Class NOT on classpath |
| `@ConditionalOnBean` | Bean already exists in context |
| `@ConditionalOnMissingBean` | Bean NOT in context (prevents duplicate) |
| `@ConditionalOnProperty` | Property has specific value |
| `@ConditionalOnWebApplication` | It's a web application |

**Interview Key Point:** "In GSTN, we built a custom Spring Boot starter (`gst-spring-boot2-starter`) that auto-configures datasources, security, Kafka, caching, and logging. Each feature is conditionally enabled via properties like `gst.security.bo.enabled=true`. This allows each microservice to pick only what it needs."

---

### Q27. What is the difference between @Component, @Service, @Repository, and @Controller? Are they functionally different?

**Answer:**

All four are **stereotype annotations** that mark a class as a Spring-managed bean. They are all **specializations of @Component**.

| Annotation | Layer | Special Behavior |
|------------|-------|-----------------|
| `@Component` | Generic | Base annotation — no special behavior |
| `@Service` | **Business Logic** | Semantic only — indicates service layer. Enables `@Transactional` |
| `@Repository` | **Data Access** | **Exception translation**: Converts JDBC/JPA exceptions to Spring's `DataAccessException` hierarchy |
| `@Controller` | **Web/Presentation** | Enables `@RequestMapping`. Returns view names (JSP, Thymeleaf) |
| `@RestController` | **Web/REST** | = `@Controller` + `@ResponseBody`. Returns JSON/XML directly |

**Functionally different?** Only `@Repository` has real extra behavior (exception translation). `@Service` and `@Controller` are primarily **semantic** — but following the convention enables AOP pointcuts and better architecture.

**GSTN Usage:**
```java
// SERVICE layer — business logic with transaction management
@Service
public class Anx1aServiceImpl implements Anx1aService {
    @Transactional(value = "transactionManagerAnx1aBatch", 
                  propagation = Propagation.REQUIRED, rollbackFor = Exception.class)
    public String getAnx1aRecords(Anx1aParamVO params, String type) { ... }
}

// REPOSITORY layer — data access with exception translation
@Repository
public interface GspAuthToknLogRepository extends JpaRepository<GspAuthTokenLog, Long> {
    @Modifying
    @Query("UPDATE GspAuthTokenLog e SET e.authStatus = 'X' ...")
    void markAuthTokenExpired(@Param("username") String username, ...);
}

// CONTROLLER layer — REST endpoints
@RestController
public class Anx1aInternalController {
    @GetMapping(value = "/auth/internalapi/newreturns/getanx1aData")
    public @ResponseBody String getAnx1aData(@RequestParam String gstin) { ... }
}

// Note: Some GSTN controllers use @Controller + @ResponseBody instead of @RestController
@Controller
public class CaseMgmtController {
    @PostMapping(value = "/auth/api/case/create")
    public @ResponseBody Object createCaseApp(...) { ... }
}
```

---

### Q28. Explain Dependency Injection — Constructor injection vs Field injection vs Setter injection? Why is constructor injection recommended?

**Answer:**

**Dependency Injection (DI):** Instead of an object creating its dependencies, the **container injects them** from the outside. This enables loose coupling, testability, and flexibility.

**Three types:**

```java
// 1. FIELD INJECTION (used extensively in GSTN codebase)
@Service
public class Anx1aServiceImpl {
    @Autowired
    OfflineAsynchFileGenDAO asyncDAO;
    
    @Autowired
    DistCacheUtil distCacheUtil;
    
    @Autowired
    Anx1aKafkaService anx1aKafkaService;
}

// 2. CONSTRUCTOR INJECTION (recommended)
@Service
public class Anx1aServiceImpl {
    private final OfflineAsynchFileGenDAO asyncDAO;
    private final DistCacheUtil distCacheUtil;
    
    // @Autowired is optional when only one constructor (Spring 4.3+)
    public Anx1aServiceImpl(OfflineAsynchFileGenDAO asyncDAO, DistCacheUtil distCacheUtil) {
        this.asyncDAO = asyncDAO;
        this.distCacheUtil = distCacheUtil;
    }
}

// 3. SETTER INJECTION
@Service
public class Anx1aServiceImpl {
    private DistCacheUtil distCacheUtil;
    
    @Autowired
    public void setDistCacheUtil(DistCacheUtil distCacheUtil) {
        this.distCacheUtil = distCacheUtil;
    }
}
```

**Why Constructor Injection is recommended:**

| Aspect | Constructor | Field | Setter |
|--------|-------------|-------|--------|
| **Immutability** | `final` fields possible | No | No |
| **Required dependencies** | Enforced at compile time | NPE at runtime | NPE at runtime |
| **Testability** | Easy — just pass mock in constructor | Needs reflection or Spring | Needs Spring or manual set |
| **Circular dependency** | **Fails fast** at startup | Hides circular dependency | Hides it |
| **Code readability** | Clear what dependencies exist | Hidden in fields | Scattered setters |

**GSTN Current State:** Our codebase predominantly uses **field injection** (`@Autowired` on fields). This is legacy and works but is harder to unit test. For new code and during refactoring, we should move to constructor injection. With Lombok, this is easy:

```java
@Service
@RequiredArgsConstructor  // Lombok generates constructor for final fields
public class Anx1aServiceImpl {
    private final OfflineAsynchFileGenDAO asyncDAO;
    private final DistCacheUtil distCacheUtil;
    private final Anx1aKafkaService anx1aKafkaService;
}
```

---

### Q29. What is the Spring Bean lifecycle?

**Answer:**

```
1. Bean Definition Loading (parse @Component, @Bean, XML)
     ↓
2. Bean Instantiation (constructor called)
     ↓
3. Dependency Injection (populate @Autowired fields)
     ↓
4. BeanNameAware.setBeanName() — if implemented
     ↓
5. BeanFactoryAware.setBeanFactory() — if implemented
     ↓
6. ApplicationContextAware.setApplicationContext() — if implemented
     ↓
7. BeanPostProcessor.postProcessBeforeInitialization()
     ↓
8. @PostConstruct method — JSR-250
     ↓
9. InitializingBean.afterPropertiesSet() — if implemented
     ↓
10. Custom init-method (specified in @Bean(initMethod="..."))
     ↓
11. BeanPostProcessor.postProcessAfterInitialization()
     ↓
--- BEAN IS READY TO USE ---
     ↓
--- APPLICATION SHUTDOWN ---
     ↓
12. @PreDestroy method — JSR-250
     ↓
13. DisposableBean.destroy() — if implemented
     ↓
14. Custom destroy-method (specified in @Bean(destroyMethod="..."))
```

**Most commonly used in GSTN:**
- `@PostConstruct` — Initialize caches, load properties
- `@PreDestroy` — Close connections, flush caches
- `BeanPostProcessor` — Custom Spring Boot auto-configuration, AOP proxying

**GSTN Example:**
```java
// DataSourceAutoConfig uses ImportBeanDefinitionRegistrar (registration phase)
// to dynamically register DataSource beans based on properties
@Configuration
public class DataSourceAutoConfig implements ImportBeanDefinitionRegistrar, EnvironmentAware {
    @Override
    public void registerBeanDefinitions(AnnotationMetadata metadata, BeanDefinitionRegistry registry) {
        // Registers DataSource, EntityManagerFactory, TransactionManager beans dynamically
    }
}
```

---

### Q30. Bean scopes — Singleton, Prototype, Request, Session? Default? When to use Prototype in GSTN?

**Answer:**

| Scope | Instances | Lifecycle | Use Case |
|-------|-----------|-----------|----------|
| **singleton** (DEFAULT) | 1 per Spring context | Context lifetime | Services, repositories, config |
| **prototype** | New instance per injection | Caller manages | Stateful beans, per-request objects |
| **request** | 1 per HTTP request | Request lifetime | Request-specific data |
| **session** | 1 per HTTP session | Session lifetime | User session data |
| **application** | 1 per ServletContext | App lifetime | Servlet context attributes |
| **websocket** | 1 per WebSocket session | WS lifetime | WebSocket-specific data |

**Default is Singleton** — one shared instance. All `@Service`, `@Repository`, `@Controller` beans are singletons.

**When to use Prototype in GSTN:**
```java
// APIHeaderVO is request-scoped — different for each API call
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class APIHeaderVO {
    private String gstin;
    private String authToken;
    private boolean exception;
    // Each request gets its own instance
}
```

**Why Prototype-in-Singleton is tricky:**
```java
@Service  // Singleton
public class MyService {
    @Autowired
    private PrototypeBean proto;  // Injected ONCE at singleton creation
    // proto is effectively singleton! 
    
    // SOLUTION: Use Provider or ObjectFactory
    @Autowired
    private ObjectProvider<PrototypeBean> protoProvider;
    
    public void doWork() {
        PrototypeBean freshInstance = protoProvider.getObject(); // New instance each time
    }
}
```

---

### Q31. What is circular dependency? How does Spring handle it? How do you resolve it?

**Answer:**

**Circular Dependency:** A depends on B, and B depends on A. During construction, both need the other to exist first → impossible.

```java
@Service
public class ServiceA {
    @Autowired private ServiceB serviceB;  // Needs B
}

@Service  
public class ServiceB {
    @Autowired private ServiceA serviceA;  // Needs A → Circular!
}
```

**How Spring handles it:**
- **Field/Setter injection**: Spring creates partial beans (without dependencies), stores them in the "early reference" cache, then injects dependencies. This **resolves** circular dependency but hides a design problem.
- **Constructor injection**: **Fails immediately** with `BeanCurrentlyInCreationException`. This is actually BETTER because it forces you to fix the design.

**Spring's 3-level cache for resolving field injection circulars:**
1. `singletonObjects` — fully initialized beans
2. `earlySingletonObjects` — partially initialized (dependencies not yet injected)
3. `singletonFactories` — factory methods to create early references

**Resolution strategies:**

1. **@Lazy** — Defer one dependency:
```java
@Service
public class ServiceA {
    @Autowired @Lazy private ServiceB serviceB;  // Proxy created, actual bean loaded later
}
```

2. **Redesign (BEST)** — Extract common logic:
```java
@Service
public class CommonService { /* shared logic */ }

@Service
public class ServiceA {
    @Autowired private CommonService common;
}

@Service
public class ServiceB {
    @Autowired private CommonService common;
}
```

3. **Use events** — Decouple with `ApplicationEventPublisher`

**GSTN Context:** In our large codebase with 30+ modules, circular dependencies can occur between `AuthenticationUtil` and `DistCacheUtil`. We resolve them using `@Lazy` or by redesigning the dependency flow to be unidirectional.

---

### Q32. What is @Qualifier and when do you need it?

**Answer:**

`@Qualifier` specifies **which bean to inject** when multiple beans of the same type exist.

```java
// Two DataSource beans in GSTN
@Bean(name = "txDataSource")
public DataSource txDataSource() { ... }

@Bean(name = "masterDataSource")
public DataSource masterDataSource() { ... }

// Without @Qualifier → NoUniqueBeanDefinitionException
@Service
public class MyService {
    @Autowired
    @Qualifier("txDataSource")  // Specifies which DataSource
    private DataSource dataSource;
}
```

**GSTN Multi-DataSource Example:**
```java
// From JpaTxRepositoryConfig.java — different transaction managers for different databases
@EnableJpaRepositories(
    basePackages = "org.gst.common.repository.tx",
    entityManagerFactoryRef = "txEntityManagerFactory",      // Qualifier by reference
    transactionManagerRef = "txTransactionManager"           // Qualifier by reference
)

// In service layer — specifying which transaction manager
@Transactional(value = "transactionManagerAnx1aBatch")   // Acts like @Qualifier
@Transactional(value = "transactionManagerReturns")
@Transactional(value = "transactionManagerItcLedger")
```

**Alternative to @Qualifier:**
```java
// @Primary — mark one bean as default
@Bean @Primary
public DataSource primaryDataSource() { ... }

// Named beans with @Service("name")
@Service("masterService")
public class UserMasterServiceImpl implements UserMasterService { ... }
```

---

### Q33. Difference between @Bean and @Component? When to use which?

**Answer:**

| Aspect | @Component | @Bean |
|--------|-----------|-------|
| Declared on | **Class** | **Method** (inside @Configuration) |
| Detection | **Classpath scanning** (@ComponentScan) | **Explicit method** in config class |
| Control | Spring controls instantiation | **You control** instantiation logic |
| Third-party classes | Can't annotate (not your code) | **Can wrap** any class |
| Conditional | Limited | Full control (if/else in method) |

**When to use @Bean:**
1. Third-party library classes you can't annotate
2. Complex instantiation logic
3. Need multiple instances of same class with different config

**GSTN Examples:**
```java
// @Bean — for configuring thread pool (complex setup)
@Configuration
@EnableAsync
public class AsyncConfig {
    @Bean(name = "taskExecutor")
    public ThreadPoolTaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("AsyncThread-");
        executor.initialize();
        return executor;
    }
}

// @Component — for your own class (simple, auto-detected)
@Component
public class APIHeaderVO { ... }

// @Bean — for DataSource (third-party HikariDataSource)
@Bean
public DataSource createDataSource(String dbIdentifier, String shard) {
    HikariDataSource ds = new HikariDataSource();
    ds.setJdbcUrl(url);
    ds.setUsername(username);
    ds.setMaximumPoolSize(10);
    return ds;
}
```

---

### Q34. What is Spring ApplicationContext vs BeanFactory?

**Answer:**

`BeanFactory` is the basic container. `ApplicationContext` extends it with enterprise features.

| Feature | BeanFactory | ApplicationContext |
|---------|------------|-------------------|
| Bean creation | **Lazy** (on first request) | **Eager** (at startup) |
| Event publishing | No | Yes (ApplicationEvent) |
| AOP support | Basic | Full |
| Message i18n | No | Yes (MessageSource) |
| Environment abstraction | No | Yes (profiles, properties) |
| Annotation support | Limited | Full (@Autowired, @Value, etc.) |

**ApplicationContext is always preferred** in production. It catches configuration errors at startup rather than at runtime. Spring Boot exclusively uses `ApplicationContext` implementations:
- `AnnotationConfigApplicationContext` — standalone
- `AnnotationConfigServletWebServerApplicationContext` — web app

**GSTN:** We use `ApplicationContext` through Spring Boot. The `GstEnvironmentPostProcessor` customizes the environment before the context fully refreshes.

---

## 2.2 Configuration & Properties

### Q35. How do you fetch a property from application.properties/yml? @Value — how to set default values?

**Answer:**

```java
// Basic @Value injection
@Value("${server.port}")
private int serverPort;

// With DEFAULT value (if property missing)
@Value("${gst.cache.ttl:3600}")  // default 3600 if not set
private int cacheTtl;

// SpEL (Spring Expression Language)
@Value("#{${gst.max.retry:3} * 2}")  // Expression: 3 * 2 = 6
private int maxAttempts;

// Inject list
@Value("${gst.allowed.states:KA,MH,TN}")
private List<String> allowedStates;

// From environment variable
@Value("${DB_PASSWORD:defaultPass}")
private String dbPassword;
```

**GSTN Usage:**
```java
// From services — GSTPropertyReader pattern
@Autowired
GSTPropertyReader gstProperty;

// Properties are read from externalized configuration
String maxRetry = gstProperty.getProperty("gst.filing.max.retry");
```

**application-test.properties in GSTN:**
```properties
# From NgtpRegApi test properties
hibernate.show_sql=true
db.driverClassName=org.h2.Driver
bo.db.url.R1=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1
bo.db.username.R1=su
bo.db.initialSize.R1=5
bo.db.maxActive.R1=10
```

**Common mistakes:**
- `@Value` won't work in static fields
- `@Value` won't work if bean not managed by Spring
- Property must exist or have default — otherwise `BeanCreationException`

---

### Q36. @Value vs @ConfigurationProperties — when to use each?

**Answer:**

| Feature | @Value | @ConfigurationProperties |
|---------|--------|-------------------------|
| Binding | Single property | **Entire group** of properties |
| Type safety | String-based | **Type-safe binding** |
| Validation | No built-in | Supports `@Validated`, `@NotNull` |
| Relaxed binding | No | Yes (`kebab-case`, `camelCase`, `UPPER_CASE`) |
| IDE support | Limited | **Auto-complete**, metadata |
| Use case | Simple, few properties | **Complex configuration objects** |

**@ConfigurationProperties — GSTN Example:**
```java
// From KafkaClientProperties.java in gst-spring-boot2-starter
@Data
@ConfigurationProperties(prefix = "gst.kafka")
public class KafkaClientProperties {
    private String bootstrapServers;
    private String clientId;
    private Producer producer = new Producer();
    private Consumer consumer = new Consumer();
    
    @Data
    public static class Producer {
        private boolean enabled = false;
        private String acks;
        private String compressionType;
        private Integer batchSize;
        private Integer retries;
    }
    
    @Data
    public static class Consumer {
        private boolean enabled = false;
        private String groupId;
        // ... more nested properties
    }
}
```

**Corresponding application.yml:**
```yaml
gst:
  kafka:
    bootstrap-servers: kafka-broker1:9092,kafka-broker2:9092
    client-id: gstn-filing-service
    producer:
      enabled: true
      acks: all
      compression-type: snappy
      batch-size: 16384
    consumer:
      enabled: true
      group-id: filing-consumer-group
```

**Rule of thumb:** Use `@Value` for 1-3 simple properties. Use `@ConfigurationProperties` for structured configuration groups.

---

### Q37. How do you manage multiple environments? Spring Profiles?

**Answer:**

**Spring Profiles** allow environment-specific configuration.

**GSTN environment files:**
```
application.yml              # Common/default properties
application-local.yml         # Local development
application-test.yml          # Test environment (H2 in-memory DB)
application-prod.yml          # Production (security hardened)
```

**GSTN's profile files:**
```yaml
# application-prod.yml (from GspAuthActivity)
springdoc:
  api-docs:
    enabled: false      # Disable Swagger in production
  swagger-ui:
    enabled: false      # Security: no API docs exposed

# application-local.yml — local development with debugging
spring:
  jpa:
    show-sql: true
```

**Activation methods:**
```bash
# 1. Command line argument
java -jar app.jar --spring.profiles.active=prod

# 2. Environment variable
export SPRING_PROFILES_ACTIVE=prod

# 3. application.properties
spring.profiles.active=prod

# 4. In code (not recommended)
SpringApplication app = new SpringApplication(MyApp.class);
app.setAdditionalProfiles("prod");
```

**@Profile annotation:**
```java
@Configuration
@Profile("prod")
public class ProdSecurityConfig { ... }  // Only loads in prod

@Configuration
@Profile("!prod")  // NOT prod
public class DevSecurityConfig { ... }   // Loads in dev, qa, staging
```

**GSTN pattern:** We activate profiles per deployment environment. Each Kubernetes deployment passes `SPRING_PROFILES_ACTIVE` as environment variable.

---

### Q38. How do you externalize configuration in production?

**Answer:**

**Priority order (highest wins):**
1. Command-line arguments (`--server.port=8080`)
2. JVM system properties (`-Dserver.port=8080`)
3. Environment variables (`SERVER_PORT=8080`)
4. External `application-{profile}.yml` (outside JAR)
5. Internal `application-{profile}.yml` (inside JAR)
6. `application.yml` (default)

**GSTN Production approach:**

1. **Properties files on server** — `GSTPropertyReader` loads from external paths
2. **Environment variables** — Kubernetes ConfigMaps/Secrets mounted as env vars
3. **Spring Boot's EnvironmentPostProcessor** — GSTN's `GstEnvironmentPostProcessor` customizes property sources before context loads
4. **Secrets** — Database passwords, API keys via Kubernetes Secrets (mounted as files or env vars)

```java
// GSTN's custom EnvironmentPostProcessor
// From gst-spring-boot2-starter spring.factories
org.springframework.boot.env.EnvironmentPostProcessor=\
  org.gst.framework.starter.autoconfigure.env.GstEnvironmentPostProcessor
```

**Never commit secrets to code.** Use: Vault, K8s Secrets, or AWS Secrets Manager.

---

### Q39. What is @PropertySource? How do you load custom property files?

**Answer:**

```java
@Configuration
@PropertySource("classpath:kafka-config.properties")       // From classpath
@PropertySource("file:/opt/config/gst-custom.properties")  // From filesystem
@PropertySource(value = "classpath:optional.properties", ignoreResourceNotFound = true)
public class CustomConfig {
    
    @Value("${custom.property}")
    private String customProp;
}
```

**GSTN uses `GSTPropertyReader`** — a custom utility that loads properties from configurable file paths. This predates Spring Boot's `@ConfigurationProperties` and provides backward compatibility with our older Spring Framework 4.x modules.

---

## 2.3 REST APIs

### Q40. @GetMapping, @PostMapping, @PutMapping, @PatchMapping, @DeleteMapping — when to use each?

**Answer:**

| Method | Annotation | Idempotent? | Request Body? | Use Case |
|--------|-----------|-------------|---------------|----------|
| **GET** | `@GetMapping` | Yes | No | Fetch data |
| **POST** | `@PostMapping` | **No** | Yes | Create resource |
| **PUT** | `@PutMapping` | Yes | Yes | **Full update** (replace entire resource) |
| **PATCH** | `@PatchMapping` | Yes | Yes | **Partial update** (update specific fields) |
| **DELETE** | `@DeleteMapping` | Yes | Usually no | Delete resource |

**PUT vs PATCH:**
- **PUT**: Send the COMPLETE resource → server replaces it entirely
- **PATCH**: Send only CHANGED fields → server merges them

**GSTN controller examples:**
```java
// GET — Retrieve ANX1A data
@GetMapping(value = "/auth/internalapi/newreturns/getanx1aData",
            produces = MediaType.APPLICATION_JSON_VALUE)
public @ResponseBody String getAnx1aData(
    @RequestParam(name = "gstin") String gstin,
    @RequestParam(name = "rtn_prd") String returnPrd) { ... }

// POST — Create case application
@PostMapping(value = "/auth/api/case/create",
             produces = MediaType.APPLICATION_JSON_VALUE)
public @ResponseBody Object createCaseApp(
    @RequestBody List<CaseAllocationDetailsVO> caseDetailsList) { ... }

// PUT — Save/update ANX1A data (full replacement)
@RequestMapping(value = "/v1.0/taxpayerapi/anx1a/saveanx1a",
               method = RequestMethod.PUT,
               consumes = MediaType.APPLICATION_JSON_VALUE)
public String saveAnx1a(@RequestBody String request) { ... }
```

---

### Q41. @PathVariable vs @RequestParam vs @RequestBody — differences with examples?

**Answer:**

| Annotation | Source | Mandatory? | Example URL |
|------------|--------|-----------|-------------|
| `@PathVariable` | **URL path** segment | Yes (default) | `/api/returns/{gstin}` |
| `@RequestParam` | **Query string** parameter | Yes (default), configurable | `/api/returns?gstin=29XXX&period=042024` |
| `@RequestBody` | **HTTP body** (JSON/XML) | Yes (default) | POST body |

**GSTN codebase examples:**

```java
// @PathVariable — extract from URL path
@PostMapping("/auth/api/un/save/{unRegRefId}")
public @ResponseBody Object saveUNBodyAuthorisedDtls(
    @PathVariable("unRegRefId") String unRegRefId,
    @RequestBody UnBodyVO unBodyVO) { ... }

@GetMapping("/auth/api/temp/{tempRegRefId}")
public @ResponseBody Object getTmpRegDtls(
    @PathVariable("tempRegRefId") String tempRegRefId) { ... }

// @RequestParam — query parameters with optional support
@GetMapping("/auth/internalapi/newreturns/getanx1aData")
public @ResponseBody String getAnx1aData(
    @RequestParam(name = "gstin") String gstin,                    // Required
    @RequestParam(name = "sec_name", required = false) String sec, // Optional
    @RequestParam(name = "rtn_prd") String returnPrd,             // Required  
    @RequestParam(name = "from_date", required = false) String fromDate,
    @RequestParam(name = "to_date", required = false) String toDate) { ... }

// @RequestBody — JSON body for POST/PUT
@PostMapping("/auth/api/case/assignCase")
public @ResponseBody Object assignCaseApp(
    @RequestBody CaseAssignDetailsVO caseAssignDetailsVO) { ... }
```

---

### Q42. How do you implement pagination and sorting in REST APIs? Spring Data's Pageable?

**Answer:**

```java
// Repository — accepts Pageable
public interface ReturnRepository extends JpaRepository<ReturnEntity, Long> {
    Page<ReturnEntity> findByGstin(String gstin, Pageable pageable);
    
    @Query("SELECT r FROM ReturnEntity r WHERE r.period = :period")
    Page<ReturnEntity> findByPeriod(@Param("period") String period, Pageable pageable);
}

// Controller — receives pagination params
@GetMapping("/api/returns")
public Page<ReturnVO> getReturns(
    @RequestParam String gstin,
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size,
    @RequestParam(defaultValue = "filingDate") String sortBy,
    @RequestParam(defaultValue = "desc") String direction) {
    
    Sort sort = Sort.by(Sort.Direction.fromString(direction), sortBy);
    Pageable pageable = PageRequest.of(page, size, sort);
    return returnRepository.findByGstin(gstin, pageable);
}
```

**Response structure (Page<T>):**
```json
{
  "content": [...],
  "totalElements": 1250,
  "totalPages": 63,
  "size": 20,
  "number": 0,
  "first": true,
  "last": false
}
```

**GSTN Context:** For large datasets (millions of returns), pagination is critical. Our search APIs like WL History Search use pagination:
```java
@PostMapping("/wlHistorySearch")
public @ResponseBody Object searchWLHistory(@RequestBody SearchWLRequest request) {
    // SearchWLRequest contains page number and size
    // Service returns paginated results
}
```

---

### Q43. How do you version REST APIs?

**Answer:**

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URI versioning** | `/v1.0/taxpayerapi/anx1a/getrecords` | Simple, visible, cacheable | URL pollution |
| Header versioning | `Accept: application/vnd.gstn.v2+json` | Clean URLs | Hidden, not cacheable |
| Query param | `/api/returns?version=2` | Simple | Ugly, not RESTful |

**GSTN uses URI versioning:**
```java
// API version in URL path — standard GSTN pattern
@RequestMapping(value = "/v1.0/taxpayerapi/anx1a/getrecords",
               method = RequestMethod.GET,
               produces = MediaType.APPLICATION_JSON_VALUE)
public String getAnx1aData(HttpServletRequest request) { ... }

@RequestMapping(value = "/v1.0/taxpayerapi/anx1a/saveanx1a",
               method = RequestMethod.PUT)
public String saveAnx1a(@RequestBody String request) { ... }
```

URI versioning is the most common and practical approach — easy to route in API gateway, cacheable by CDN, and visible in logs.

---

### Q44. What is content negotiation?

**Answer:**

Content negotiation allows the **same endpoint to return different formats** (JSON, XML) based on the client's preference.

**How Spring handles it:**
1. **Accept header**: Client sends `Accept: application/json` or `Accept: application/xml`
2. **URL suffix**: `/api/returns.json` vs `/api/returns.xml` (deprecated)
3. **Query parameter**: `/api/returns?format=xml`

```java
// Spring auto-negotiates based on Accept header when Jackson + JAXB are on classpath
@GetMapping(value = "/api/returns", 
            produces = {MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE})
public ReturnVO getReturn(@RequestParam String gstin) {
    return returnService.getReturn(gstin);
}
```

**GSTN:** Our APIs exclusively use `produces = MediaType.APPLICATION_JSON_VALUE` — JSON is the standard for all GSTN APIs.

---

### Q45. How do you validate request bodies?

**Answer:**

```java
// VO/DTO with validation annotations
public class ReturnFilingRequest {
    @NotNull(message = "GSTIN is required")
    @Size(min = 15, max = 15, message = "GSTIN must be 15 characters")
    @Pattern(regexp = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$",
             message = "Invalid GSTIN format")
    private String gstin;
    
    @NotNull(message = "Return period is required")
    @Pattern(regexp = "^(0[1-9]|1[0-2])\\d{4}$", message = "Period must be MMYYYY")
    private String returnPeriod;
    
    @NotNull @Min(0) @Max(999999999)
    private BigDecimal taxableAmount;
}

// Controller — trigger validation with @Valid
@PostMapping("/api/returns/file")
public ResponseEntity<?> fileReturn(@Valid @RequestBody ReturnFilingRequest request) {
    // Only reaches here if validation passes
    return ResponseEntity.ok(returnService.file(request));
}
```

**GSTN validation patterns:**
```java
// Manual validation in controller (GSTN's current approach)
if (gstin == null || gstin.trim().isEmpty()) {
    return respGenerator.generateErrorResponse(
        Anx1aErrorCode.HBASE01_Code, Anx1aErrorCode.HBASE01_MSG);
}

// AOP-based validation (from UserMastersAPI)
@Aspect
public class G2BApiValidator {
    @Before("execution(* org.gst.masters.api.controller.G2BController.*(..))")
    public void validateRequest() { 
        // Validate API headers, auth tokens before controller method executes
    }
}
```

**Custom Validator:**
```java
@Constraint(validatedBy = GstinValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidGstin {
    String message() default "Invalid GSTIN";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class GstinValidator implements ConstraintValidator<ValidGstin, String> {
    @Override
    public boolean isValid(String gstin, ConstraintValidatorContext ctx) {
        return gstin != null && gstin.matches("^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}...");
    }
}
```

---

### Q46. What HTTP status codes do you use?

**Answer:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| **200** OK | Successful GET/PUT/PATCH | Return filing retrieved/updated |
| **201** Created | Successful POST | New return filed, new registration created |
| **204** No Content | Successful DELETE | Resource deleted, nothing to return |
| **400** Bad Request | Validation failure | Invalid GSTIN format, missing fields |
| **401** Unauthorized | Authentication failed | Invalid/expired JWT token |
| **403** Forbidden | Authorized but not allowed | Taxpayer trying to access another's data |
| **404** Not Found | Resource doesn't exist | GSTIN not registered |
| **409** Conflict | Resource state conflict | Return already filed for this period |
| **429** Too Many Requests | Rate limit exceeded | Filing season API throttling |
| **500** Internal Server Error | Server-side failure | Unexpected exception |
| **502** Bad Gateway | Upstream failure | Payment gateway down |
| **503** Service Unavailable | Service maintenance | Planned downtime |

---

### Q47. How do you implement HATEOAS? Have you used it?

**Answer:**

HATEOAS (Hypermedia As The Engine Of Application State) adds **links** to responses telling clients what actions are available next.

```java
// With Spring HATEOAS
@GetMapping("/api/returns/{id}")
public EntityModel<ReturnVO> getReturn(@PathVariable Long id) {
    ReturnVO returnVO = returnService.get(id);
    return EntityModel.of(returnVO,
        linkTo(methodOn(ReturnController.class).getReturn(id)).withSelfRel(),
        linkTo(methodOn(ReturnController.class).fileReturn(id)).withRel("file"),
        linkTo(methodOn(ReturnController.class).getAll()).withRel("all-returns"));
}
```

**GSTN:** We don't currently use HATEOAS. Our APIs are straightforward JSON responses. HATEOAS adds complexity that isn't needed for our internal service-to-service communication — it's more valuable for public APIs with diverse client applications.

---

### Q48. How do you handle file upload/download in REST APIs?

**Answer:**

```java
// FILE UPLOAD
@PostMapping("/api/returns/upload")
public ResponseEntity<String> uploadReturn(
    @RequestParam("file") MultipartFile file,
    @RequestParam("gstin") String gstin) {
    
    if (file.isEmpty()) throw new BadRequestException("File is empty");
    if (file.getSize() > 10_000_000) throw new BadRequestException("File too large");
    
    // Validate content type
    String contentType = file.getContentType();
    if (!"application/json".equals(contentType)) {
        throw new BadRequestException("Only JSON files accepted");
    }
    
    byte[] bytes = file.getBytes();
    // Process file...
    return ResponseEntity.ok("Uploaded successfully");
}

// FILE DOWNLOAD
@GetMapping("/api/returns/download/{id}")
public ResponseEntity<Resource> downloadReturn(@PathVariable Long id) {
    byte[] data = returnService.getReturnFile(id);
    ByteArrayResource resource = new ByteArrayResource(data);
    
    return ResponseEntity.ok()
        .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=return.json")
        .contentType(MediaType.APPLICATION_JSON)
        .contentLength(data.length)
        .body(resource);
}
```

**GSTN:** Our offline file generation (`OfflineAsynchFileGenDAO`) generates return files asynchronously and stores them. Taxpayers download generated returns via signed URLs.

---

## 2.4 Exception Handling

### Q49. What is @ControllerAdvice + @ExceptionHandler? How did you implement global exception handling in GSTN?

**Answer:**

`@ControllerAdvice` is a **global exception handler** — catches exceptions from ALL controllers in one place.

```java
@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(GSTLogicalException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(GSTLogicalException ex) {
        ErrorResponse error = new ErrorResponse();
        error.setErrorCode(ex.getErrorCode());
        error.setMessage(ex.getMessage());
        error.setTimestamp(System.currentTimeMillis());
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(GSTRuntimeException.class)
    public ResponseEntity<ErrorResponse> handleRuntimeException(GSTRuntimeException ex) {
        ErrorResponse error = new ErrorResponse();
        error.setErrorCode(ex.getErrorCode());
        error.setMessage("Internal server error");
        return ResponseEntity.status(500).body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
        LOGGER.error("Unexpected error", ex);
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "Unexpected error"));
    }
}
```

**GSTN Exception Hierarchy:**
```java
// Checked — business logic errors (expected failures)
public class GSTLogicalException extends Exception {
    private String errorCode;
    private String message;
    private int httpStatusCode;
    private static Map<String, List<String>> msgMap; // Error registry
}

// Unchecked — system errors (unexpected failures)
public class GSTRuntimeException extends RuntimeException {
    private String errorCode;
    private String message;
    private int httpStatusCode;
    private static Map<String, List<String>> runtimeExpMap;
}

// Domain-specific exceptions
public class ValidationFwkException extends Exception {}
public class ReplayCountExceededException extends Exception {}
public class ReturnSystemException extends RuntimeException {}
public class HBaseFwkIllegalArgumentException extends Exception {}
```

---

### Q50. How do you create a custom exception hierarchy?

**Answer:**

```
Exception (Checked)
├── GSTLogicalException (Business logic errors)
│   ├── ValidationFwkException (Input validation failures)
│   ├── ReplayCountExceededException (Duplicate filing attempt)
│   ├── HBaseFwkIllegalArgumentException (HBase query errors)
│   └── ZdlException (ZDL processing errors)
│
RuntimeException (Unchecked)
├── GSTRuntimeException (System errors)
│   ├── GstUncheckedException (Generic runtime errors)
│   └── ReturnSystemException (Return processing system failures)
│   └── SpoutException (Kafka spout errors)
```

**Best Practice:** Checked exceptions for recoverable conditions (validation, not found), Unchecked for programming errors and system failures.

---

### Q51. How do you return a standardized error response?

**Answer:**

```java
// Standard error response VO
public class ErrorResponse {
    private String errorCode;     // "GSTIN_INVALID", "AUTH_EXPIRED"
    private String message;       // Human-readable message
    private long timestamp;       // When error occurred
    private String path;          // Request path
    private int status;           // HTTP status code
    private List<FieldError> fieldErrors;  // Validation errors
}

// GSTN's response pattern
// From ResponseUtil — standardized error generation
public class ResponseUtil {
    public String generateErrorResponse(String errorCode, String errorMessage) {
        ErrorResponse response = new ErrorResponse();
        response.setStatusCode(errorCode);
        response.setStatusMessage(errorMessage);
        response.setTimestamp(System.currentTimeMillis());
        return gson.toJson(response);
    }
}

// Usage in controller
if (gstin == null || gstin.trim().isEmpty()) {
    return respGenerator.generateErrorResponse(
        Anx1aErrorCode.HBASE01_Code, Anx1aErrorCode.HBASE01_MSG);
}
```

---

### Q52. Checked vs Unchecked exceptions in Spring?

**Answer:**

| Aspect | Checked (extends Exception) | Unchecked (extends RuntimeException) |
|--------|----|---|
| Compiler | Forces try-catch or throws | No compile-time enforcement |
| @Transactional rollback | **Does NOT rollback** by default | **Rollbacks** by default |
| Use case | Expected, recoverable errors | Programming errors, system failures |
| GSTN example | `GSTLogicalException` | `GSTRuntimeException` |

**Critical Spring gotcha:**
```java
@Transactional
public void fileReturn(ReturnVO returnVO) throws GSTLogicalException {
    repository.save(returnVO);
    if (invalid) throw new GSTLogicalException("INVALID"); 
    // Transaction will NOT rollback! GSTLogicalException is checked.
}

// Fix — explicitly specify rollbackFor
@Transactional(rollbackFor = Exception.class)  // Rollback on ALL exceptions
public void fileReturn(ReturnVO returnVO) throws GSTLogicalException { ... }
```

This is exactly what GSTN does:
```java
@Transactional(value = "transactionManagerAnx1aBatch", 
              propagation = Propagation.REQUIRED, 
              rollbackFor = Exception.class)  // Always rollback!
```

---

## 2.5 Logging & Monitoring

### Q53. SLF4J + Logback configuration?

**Answer:**

**SLF4J** = API (facade). **Logback** = Implementation. This separation lets you switch implementations without code changes.

```java
// In GSTN service classes
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Anx1aServiceImpl {
    private static final Logger LOGGER = LoggerFactory.getLogger(Anx1aServiceImpl.class);
    
    public void process() {
        LOGGER.info("Entering searchWLHistoryGSTIN : {} at {}", searchVO, System.currentTimeMillis());
        LOGGER.debug("Processing GSTIN: {}", gstin);  // Parameterized logging (no string concat)
        LOGGER.error("Error in searchWLHistoryGSTIN", exception);
    }
}
```

**Log Levels:** TRACE < DEBUG < INFO < WARN < ERROR

**logback.xml configuration:**
```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>/var/log/gstn/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>/var/log/gstn/application.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

**GSTN uses Logback 1.1.7** as seen in pom.xml dependencies.

---

### Q54. What is MDC (Mapped Diagnostic Context)?

**Answer:**

MDC uses **ThreadLocal** to store key-value pairs that are automatically included in every log statement within that thread.

```java
// In Filter/Interceptor — set at request start
public class MdcFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        try {
            MDC.put("requestId", UUID.randomUUID().toString());
            MDC.put("gstin", request.getHeader("gstin"));
            MDC.put("userId", extractUserId(request));
            chain.doFilter(req, res);
        } finally {
            MDC.clear();  // MUST clear to prevent memory leak
        }
    }
}

// logback.xml — include MDC values in log pattern
// %X{requestId} extracts from MDC
<pattern>%d [%thread] [requestId=%X{requestId}] [gstin=%X{gstin}] %-5level %logger - %msg%n</pattern>

// Output: 2026-03-18 10:30:00 [http-nio-8080-1] [requestId=abc-123] [gstin=29AAACG1234A1ZD] INFO ReturnService - Filing return
```

**Cross-service tracing:** Pass requestId in HTTP header → downstream services put it in MDC → all logs across services have same requestId for end-to-end tracing.

---

### Q55. Different log levels per environment?

**Answer:**

```yaml
# application-dev.yml
logging:
  level:
    root: INFO
    org.gst: DEBUG           # Debug our code
    org.hibernate.SQL: DEBUG  # See SQL queries
    org.springframework: INFO

# application-prod.yml  
logging:
  level:
    root: WARN
    org.gst: INFO            # Only INFO in prod
    org.hibernate.SQL: WARN  # No SQL logging in prod
    org.springframework: WARN
```

**GSTN:** In test properties, `hibernate.show_sql=true` enables SQL logging. In prod, this is disabled for performance and security.

---

### Q56. Spring Boot Actuator endpoints?

**Answer:**

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus  # Expose specific endpoints
  endpoint:
    health:
      show-details: when-authorized  # Only show details to authenticated users
```

**Key endpoints:**
| Endpoint | Purpose |
|----------|---------|
| `/actuator/health` | Application health status |
| `/actuator/metrics` | JVM, HTTP, DB metrics |
| `/actuator/info` | App info (version, build) |
| `/actuator/env` | Environment properties |
| `/actuator/loggers` | View/change log levels at runtime |
| `/actuator/prometheus` | Prometheus-format metrics |

**Security:** Always restrict actuator endpoints in production. GSTN disables Swagger in prod (`springdoc.api-docs.enabled=false`), and actuator endpoints should be similarly restricted.

---

### Q57. Custom health indicators?

**Answer:**

```java
@Component
public class PaymentGatewayHealthIndicator implements HealthIndicator {
    
    @Autowired
    private PaymentGatewayClient client;
    
    @Override
    public Health health() {
        try {
            boolean reachable = client.ping();
            if (reachable) {
                return Health.up()
                    .withDetail("service", "Payment Gateway")
                    .withDetail("latency", client.getLatency() + "ms")
                    .build();
            }
            return Health.down()
                .withDetail("error", "Payment Gateway unreachable")
                .build();
        } catch (Exception e) {
            return Health.down(e).build();
        }
    }
}

// Kubernetes readiness probe calls /actuator/health
// If DOWN → pod removed from service → no traffic received
```

---

### Q58. Prometheus + Grafana integration?

**Answer:**

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```java
// Custom metrics
@Service
public class ReturnService {
    private final Counter filingCounter;
    private final Timer filingTimer;
    
    public ReturnService(MeterRegistry registry) {
        this.filingCounter = Counter.builder("gstn.returns.filed")
            .tag("type", "GSTR1")
            .register(registry);
        this.filingTimer = Timer.builder("gstn.returns.processing.time")
            .register(registry);
    }
    
    public void fileReturn(ReturnVO returnVO) {
        filingTimer.record(() -> {
            // Processing logic
            filingCounter.increment();
        });
    }
}
```

Prometheus scrapes `/actuator/prometheus` → Grafana dashboards visualize metrics.

---

## 2.6 Transactions

### Q59. @Transactional — how does it work internally? Same-class method call?

**Answer:**

**Internally:** Spring creates a **proxy** (JDK dynamic proxy or CGLIB) around the bean. The proxy intercepts method calls and manages transactions.

```
Client → Proxy → begin transaction → Actual Method → commit/rollback → return
```

**Same-class method call problem:**
```java
@Service
public class ReturnService {
    
    @Transactional
    public void processReturn(ReturnVO vo) {
        // This calls saveReturn directly — BYPASSES PROXY!
        saveReturn(vo);  // @Transactional on saveReturn is IGNORED
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveReturn(ReturnVO vo) {
        // This method's @Transactional won't work when called from processReturn
        // because Spring AOP uses proxy-based interception
    }
}
```

**Solutions:**
1. **Extract to another class** (most common)
2. **Self-injection**: `@Autowired private ReturnService self;` then `self.saveReturn(vo);`
3. **Use `AopContext.currentProxy()`** (not recommended)

---

### Q60. Transaction propagation types?

**Answer:**

| Propagation | Behavior | GSTN Use Case |
|-------------|----------|---------------|
| **REQUIRED** (default) | Use existing TX; create new if none | Normal service methods |
| **REQUIRES_NEW** | **Suspend** current TX; create new | Audit logging (must save even if main TX fails) |
| **NESTED** | Savepoint within current TX | Partial rollback within a step |
| **SUPPORTS** | Use TX if exists; else run without | Read-only queries |
| **NOT_SUPPORTED** | Suspend current TX; run without | External API calls |
| **MANDATORY** | Must have existing TX; else exception | Methods that must be part of larger TX |
| **NEVER** | Must NOT have TX; else exception | Non-transactional operations |

**GSTN Examples:**
```java
// REQUIRED — default, most service methods
@Transactional(value = "transactionManagerAnx1aBatch", 
              propagation = Propagation.REQUIRED, 
              rollbackFor = Exception.class)
public String getAnx1aRecords(Anx1aParamVO params) { ... }

// REQUIRES_NEW — Ledger operations need independent transactions
@Transactional(value = "transactionManagerItcLedger", 
              propagation = Propagation.REQUIRES_NEW, 
              rollbackFor = Exception.class)
public void updateLedgerBalance(LedgerVO ledger) { ... }

// REQUIRES_NEW — Workflow operations independent of parent
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void createAuditEntry(AuditVO audit) { ... }
// Even if parent TX rolls back, audit entry is saved
```

---

### Q61. Transaction isolation levels?

**Answer:**

| Isolation | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|-----------|-----------|-------------------|-------------|-------------|
| READ_UNCOMMITTED | Yes | Yes | Yes | Fastest |
| **READ_COMMITTED** | No | Yes | Yes | **MySQL default** |
| REPEATABLE_READ | No | No | Yes | Good |
| SERIALIZABLE | No | No | No | Slowest |

**For GSTN payment processing:** Use **REPEATABLE_READ** or **SERIALIZABLE** to prevent:
- Two concurrent requests deducting from the same ledger balance
- Credit and debit race conditions

```java
@Transactional(isolation = Isolation.REPEATABLE_READ)
public void processPayment(PaymentVO payment) {
    BigDecimal balance = ledgerRepository.getBalance(payment.getGstin());
    if (balance.compareTo(payment.getAmount()) >= 0) {
        ledgerRepository.debit(payment.getGstin(), payment.getAmount());
    }
}
```

---

### Q62. What is a read-only transaction?

**Answer:**

```java
@Transactional(readOnly = true)
public List<ReturnVO> getReturnsByGstin(String gstin) {
    return returnRepository.findByGstin(gstin);
}
```

**Optimizations:**
1. **Hibernate skips dirty checking** — doesn't track entity changes → less memory, faster
2. **No flush at end** — read-only transactions don't flush persistence context
3. **JDBC driver optimization** — some drivers optimize for read-only connections
4. **Routing to read replica** — application can route read-only TX to slave database

**GSTN Context:** Our read-heavy dashboard queries and search APIs should use `readOnly = true`. With our RoutingDataSource, we could route read-only transactions to read replicas.

---

### Q63. How do you handle distributed transactions? XA transactions?

**Answer:**

**XA (eXtended Architecture)** provides **two-phase commit** across multiple databases/resources.

**Two-Phase Commit:**
1. **Prepare phase**: Transaction Manager asks all resources "Can you commit?" → each votes YES/NO
2. **Commit phase**: If all YES → TM sends COMMIT to all. If any NO → TM sends ROLLBACK to all.

**GSTN WFXAServiceImpl:**
```java
// From WorkFlowFwk — XA transaction across multiple databases
public class WFXAServiceImpl implements WFXAService {
    // Manages transactions across workflow DB + business DB
    // Both must commit or both rollback
}
```

**XA Limitations:**
- **Performance**: Holds locks across prepare phase → slow
- **Availability**: If TM crashes between prepare and commit → blocking
- **Not suitable for microservices**: Tight coupling between services

**Alternatives for microservices (GSTN):**
1. **Saga Pattern**: Chain of local transactions with compensating actions
2. **Outbox Pattern**: Write event to outbox table → publish to Kafka → other services consume
3. **Eventual consistency**: Accept temporary inconsistency, reconcile later

---

## 2.7 Security

### Q64. How does Spring Security work?

**Answer:**

**Security Filter Chain** — a chain of servlet filters that intercept every request:

```
Request → DelegatingFilterProxy → FilterChainProxy → Security Filters → Controller
```

**Key filters (in order):**
1. `SecurityContextPersistenceFilter` — Load SecurityContext from session
2. `UsernamePasswordAuthenticationFilter` — Process login
3. `BasicAuthenticationFilter` — HTTP Basic auth
4. `ExceptionTranslationFilter` — Convert security exceptions
5. `FilterSecurityInterceptor` — Authorization check (is user allowed?)

**GSTN Security Configuration:**
```java
// From gst-spring-boot2-starter — conditional security configs
@ConditionalOnClass({HttpSecurity.class})
@ConditionalOnProperty(prefix = "gst.security.fo", name = "enabled", havingValue = "true")
public class FoSecurityAutoConfiguration { ... }  // Front-office security

@ConditionalOnProperty(prefix = "gst.security.bo", name = "enabled", havingValue = "true")
public class BoSecurityAutoConfiguration { ... }  // Back-office security

@ConditionalOnProperty(prefix = "gst.security.gsp", name = "enabled", havingValue = "true")
public class GspSecurityAutoConfiguration { ... } // GSP (third-party) security
```

**GSTN's AuthorizationFilter:**
```java
// Custom filter — implements javax.servlet.Filter
public class AuthorizationFilter implements Filter {
    @Autowired
    private AuthenticationUtil authenticateUtil;
    
    @Autowired
    private AuthorizationUtil authorizationUtil;
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) {
        // 1. Extract auth token from request
        // 2. Validate token via AuthenticationUtil
        // 3. Check authorization via AuthorizationUtil
        // 4. If valid → chain.doFilter() (continue)
        // 5. If invalid → return 401/403
    }
}
```

---

### Q65. JWT-based authentication flow?

**Answer:**

```
1. Login: Client → POST /auth/login (username + password)
2. Server validates credentials → generates JWT → returns token
3. Client stores JWT (localStorage/cookie)
4. Subsequent requests: Client → sends JWT in Authorization header
5. Server validates JWT signature → extracts claims → processes request

JWT Structure: HEADER.PAYLOAD.SIGNATURE
  Header:  {"alg": "HS256", "typ": "JWT"}
  Payload: {"sub": "user123", "gstin": "29AAACG1234A1ZD", "role": "TAXPAYER", "exp": 1679000000}
  Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)
```

**GSTN Token Management:**
```java
// Token stored in database and cache
@Repository
public interface GspAuthToknLogRepository extends JpaRepository<GspAuthTokenLog, Long> {
    
    @Modifying
    @Query("UPDATE GspAuthTokenLog e SET e.authStatus = 'X' " +
           "WHERE e.userName = :username AND e.clientId = :clientId AND e.authToken = :authToken")
    void markAuthTokenExpired(@Param("username") String username,
                             @Param("clientId") String clientId,
                             @Param("authToken") String authToken);
}

// Session management via distributed cache
@Async
public void keepAliveSession(String authToken) {
    authenticationUtil.keepAliveSession(authToken);  // Extend session TTL in Redis
}
```

---

### Q66. Role-based access control (RBAC)?

**Answer:**

```java
// Spring Security annotations
@PreAuthorize("hasRole('TAX_OFFICER')")
@PostMapping("/auth/api/case/create")
public Object createCase(@RequestBody CaseVO caseVO) { ... }

@PreAuthorize("hasAnyRole('ADMIN', 'SUPER_ADMIN')")
@DeleteMapping("/api/returns/{id}")
public void deleteReturn(@PathVariable Long id) { ... }

@PreAuthorize("hasRole('TAXPAYER') and #gstin == authentication.principal.gstin")
@GetMapping("/api/returns/{gstin}")
public Object getReturns(@PathVariable String gstin) { ... }
```

**GSTN RBAC pattern:**
```java
// BOUserSession contains role information
BOUserSession boUserSession = authenticationUtil.getBOUserSession(request);
if (null != boUserSession) {
    // Check role-based permissions
    caseAllocationDetailsVOList = caseMgmtService.createCaseApp(
        caseAllocationDetailsListVO, boUserSession);
}

// Role-access mapping entity
@Getter @Setter @AllArgsConstructor
public class RoleAccessMapEntity {
    // Maps roles to allowed operations
}
```

---

### Q67–Q69. CSRF, CORS, OAuth2?

**CSRF Protection:**
- Protects against cross-site request forgery
- Enabled by default for browser-based apps
- **Disabled for REST APIs** (stateless, JWT-based — no cookies)
```java
http.csrf().disable();  // Disable for stateless REST API
```

**CORS Configuration:**
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("https://gst.gov.in", "https://services.gst.gov.in")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowedHeaders("*")
            .allowCredentials(true)
            .maxAge(3600);
    }
}
```

**OAuth2:** GSTN uses token-based authentication. GSP (GST Suvidha Provider) integration uses OAuth2 client credentials flow for machine-to-machine authentication, as seen in `GspSecurityAutoConfiguration`.

---

## 2.8 Advanced Spring Boot

### Q70. Filters, Interceptors, and AOP — differences?

**Answer:**

| Aspect | Filter | Interceptor | AOP |
|--------|--------|-------------|-----|
| Level | **Servlet** (before Spring) | **Spring MVC** | **Any Spring bean** |
| Interface | `javax.servlet.Filter` | `HandlerInterceptor` | `@Aspect` |
| Access to | Request/Response only | Handler method info | Method args, return value |
| Use case | Auth, logging, CORS | Timing, logging, auth | Cross-cutting concerns |
| Order | Executes FIRST | After Filter, before handler | Around method execution |

**GSTN examples of all three:**

```java
// FILTER — AuthorizationFilter (servlet level)
public class AuthorizationFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        // Auth check BEFORE Spring MVC processing
        chain.doFilter(req, res);
    }
}

// INTERCEPTOR — WebContentInterceptor (Spring MVC level)
// From servlet-context.xml
<mvc:interceptors>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <bean class="org.springframework.web.servlet.mvc.WebContentInterceptor">
            <property name="cacheSeconds" value="0"/>
        </bean>
    </mvc:interceptor>
</mvc:interceptors>

// AOP — LoggingAspect (method level)
@Aspect
public class LoggingAspect {
    @Before("execution(* org.gst..*(..))")
    public void logMethodEntry(JoinPoint joinPoint) {
        LOGGER.info("Entering: {}", joinPoint.getSignature().getName());
    }
    
    @AfterReturning(value = "execution(* org.gst..*(..))", returning = "result")
    public void logAfterSuccess(JoinPoint joinPoint, Object result) {
        LOGGER.info("Exiting: {}", joinPoint.getSignature().getName());
    }
    
    @AfterThrowing(value = "execution(* org.gst..*(..))", throwing = "ex")
    public void logException(JoinPoint joinPoint, Throwable ex) {
        LOGGER.error("Exception in: {}", joinPoint.getSignature().getName(), ex);
    }
}
```

---

### Q71. Rate limiting in Spring Boot?

**Answer:**

```java
// Using Bucket4j (Token Bucket algorithm)
@Component
public class RateLimitFilter implements Filter {
    
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();
    
    private Bucket createBucket() {
        return Bucket4j.builder()
            .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
            .build();
    }
    
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) {
        String clientId = extractClientId(req);
        Bucket bucket = buckets.computeIfAbsent(clientId, k -> createBucket());
        
        if (bucket.tryConsume(1)) {
            chain.doFilter(req, res);
        } else {
            HttpServletResponse response = (HttpServletResponse) res;
            response.setStatus(429); // Too Many Requests
            response.getWriter().write("Rate limit exceeded");
        }
    }
}
```

**For GSTN distributed rate limiting:** Use Redis-based token bucket so rate limits are shared across all instances.

---

### Q72. @Async — how to use it? Error handling?

**Answer:**

**GSTN @Async usage:**
```java
// From AsyncServiceImpl
@EnableAsync
public class AsyncServiceImpl {
    
    @Async
    public void addCaptcha(String token, String captchaAnswer) {
        LOGGER.info("Entering async addCaptcha at {}", System.currentTimeMillis());
        try {
            distCacheUtil.addToCaptchaCacheForAudio(token, captchaAnswer);
        } catch (Exception e) {
            LOGGER.error("Exception in async adding captcha to cache {}", e);
        } finally {
            LOGGER.info("Exiting async addCaptcha at {}", System.currentTimeMillis());
        }
    }
    
    @Async
    public void removeCaptcha(String token) {
        LOGGER.info("Entering async removeCaptcha at {}", System.currentTimeMillis());
        try {
            distCacheUtil.removeCaptchaForAudio(token);
        } catch (Exception e) {
            LOGGER.error("Exception in async removing captcha to cache {}", e);
        }
    }
    
    @Async
    public void keepAliveSession(String authToken) {
        try {
            authenticationUtil.keepAliveSession(authToken);
        } catch (Exception e) {
            LOGGER.error("Exception in async keepAliveSession {}", e);
        }
    }
}
```

**Error handling:** @Async void methods → exceptions are lost unless you:
1. Handle inside the method (GSTN's approach — try-catch)
2. Configure `AsyncUncaughtExceptionHandler`
3. Return `CompletableFuture<T>` — caller can handle errors

**TaskExecutor configuration:**
```java
// From AsyncConfig.java
@Bean(name = "taskExecutor")
public ThreadPoolTaskExecutor taskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(5);
    executor.setMaxPoolSize(10);
    executor.setQueueCapacity(100);
    executor.setThreadNamePrefix("AsyncThread-");
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    executor.initialize();
    return executor;
}
```

---

### Q73. @Scheduled — cron expressions, fixedRate vs fixedDelay?

**Answer:**

```java
// fixedRate — runs every 5 seconds regardless of previous execution time
@Scheduled(fixedRate = 5000)

// fixedDelay — waits 5 seconds AFTER previous execution completes
@Scheduled(fixedDelay = 5000)

// Cron expressions — "sec min hour dayOfMonth month dayOfWeek"
@Scheduled(cron = "0 0 2 * * ?")    // Every day at 2:00 AM
@Scheduled(cron = "0 */15 * * * ?") // Every 15 minutes
@Scheduled(cron = "0 0 0 1 * ?")    // First day of every month at midnight
```

**Preventing overlap in clustered environment:**
- Use **ShedLock** — distributed lock in Redis/DB
- Use **Quartz Scheduler** with DB-backed job store
- GSTN uses `JobLockAutoConfiguration` for batch job locking:
```java
// From gst-spring-boot2-starter
@ConditionalOnProperty(name = "gst.batch.job.lock.cluster.enabled", havingValue = "true")
// Ensures only one instance runs the scheduled job across the cluster
```

---

### Q74. What is Spring WebFlux? Reactive programming?

**Answer:**

**Spring WebFlux** = non-blocking, reactive web framework. Uses **Reactor** (Mono/Flux) instead of blocking servlet model.

| Spring MVC | Spring WebFlux |
|-----------|----------------|
| Thread-per-request | Event loop (Netty) |
| Blocking I/O | Non-blocking I/O |
| Servlet API | Reactive Streams |
| 200 threads = 200 concurrent requests | 4 threads = 10K+ concurrent requests |
| Better for CPU-bound | Better for I/O-bound (many slow calls) |

**When to choose WebFlux:**
- High concurrency with slow downstream services
- Streaming data (SSE, WebSocket)
- Microgateway/proxy services

**When NOT to choose (stay with MVC):**
- Blocking database drivers (JDBC) — unless using R2DBC
- Team not familiar with reactive paradigm
- Simple CRUD applications
- GSTN currently uses Spring MVC — the blocking model works well with our architecture

---

### Q75. Integration tests in Spring Boot?

**Answer:**

```java
// Full application context test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ReturnApiIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void testFileReturn() {
        ReturnVO returnVO = new ReturnVO("29AAACG1234A1ZD", "042024");
        ResponseEntity<String> response = restTemplate.postForEntity(
            "/api/returns/file", returnVO, String.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }
}

// Controller-only test (no full context)
@WebMvcTest(Anx1aInternalController.class)
class Anx1aControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private Anx1aService anx1aService;
    
    @Test
    void testGetAnx1aData() throws Exception {
        when(anx1aService.getAnx1aRecords(any(), any())).thenReturn("{}");
        
        mockMvc.perform(get("/auth/internalapi/newreturns/getanx1aData")
                .param("gstin", "29AAACG1234A1ZD")
                .param("rtn_prd", "042024"))
            .andExpect(status().isOk())
            .andExpect(content().json("{}"));
    }
}

// Repository test
@DataJpaTest
class ReturnRepositoryTest {
    @Autowired
    private TestEntityManager em;
    @Autowired
    private ReturnRepository repo;
}
```

**GSTN testing:** Uses TestNG 6.8.7 (not JUnit) as seen in pom.xml files and testng.xml configurations across modules.
