# SECTIONS 9-11: DESIGN PATTERNS, DOCKER/K8S, CI/CD — Interview Answers (Q166–Q205)
## With GSTN Codebase References

---

# SECTION 9: DESIGN PATTERNS (Q166–Q180)

### Q166. Singleton — thread-safe implementations?

**Answer:**

**GSTN uses Singleton** in KafkaConsumerConfig:
```java
// From KafkaConsumerConfig.java — Eager initialization (simplest thread-safe)
public class KafkaConsumerConfig {
    private static KafkaConsumerConfig instance = new KafkaConsumerConfig(); // Created at class loading
    
    private KafkaConsumerConfig() {} // Private constructor
    
    public static KafkaConsumerConfig getInstance() {
        return instance;
    }
}
```

**Thread-safe implementations:**

```java
// 1. ENUM (recommended by Joshua Bloch) — simplest, serialization-safe
public enum KafkaConfig {
    INSTANCE;
    private Properties props = new Properties();
    public KafkaConsumer<Long, String> getNewConsumer() { return new KafkaConsumer<>(props); }
}

// 2. Bill Pugh (static inner class) — lazy + thread-safe
public class Singleton {
    private Singleton() {}
    private static class Holder {
        private static final Singleton INSTANCE = new Singleton(); // Loaded lazily
    }
    public static Singleton getInstance() { return Holder.INSTANCE; }
}

// 3. Double-checked locking (Java 5+ with volatile)
public class Singleton {
    private static volatile Singleton instance;
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**In Spring:** All `@Service`, `@Component` beans are singletons by default — Spring manages lifecycle.

---

### Q167. Factory Method vs Abstract Factory?

**Answer:**

**Factory Method:** Single method to create objects based on type.
```java
// GSTN: Create different validators based on return type
public class ValidatorFactory {
    public static Validator createValidator(String returnType) {
        switch (returnType) {
            case "GSTR1": return new GSTR1Validator();
            case "GSTR3B": return new GSTR3BValidator();
            case "GSTR9": return new GSTR9AnnualValidator();
            default: throw new IllegalArgumentException("Unknown return type");
        }
    }
}
```

**Abstract Factory:** Factory of factories — creates families of related objects.
```java
// GSTN: Different processing pipelines per environment
interface GSTProcessingFactory {
    Validator createValidator();
    Processor createProcessor();
    Notifier createNotifier();
}

class ProductionFactory implements GSTProcessingFactory {
    public Validator createValidator() { return new StrictValidator(); }
    public Processor createProcessor() { return new KafkaProcessor(); }
    public Notifier createNotifier() { return new SMSNotifier(); }
}

class TestFactory implements GSTProcessingFactory {
    public Validator createValidator() { return new MockValidator(); }
    public Processor createProcessor() { return new InMemoryProcessor(); }
    public Notifier createNotifier() { return new LogNotifier(); }
}
```

---

### Q168. Builder pattern — Lombok's @Builder?

**Answer:**

```java
// GSTN uses Lombok @Builder extensively
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class HSNResponseDetailsVo {
    private String url;
    private String message;
    private String errorCode;
    private List<HSNDetailsVo> data;
}

// Usage — fluent API
HSNResponseDetailsVo response = HSNResponseDetailsVo.builder()
    .url("/api/hsn/search")
    .message("Success")
    .errorCode("0")
    .data(hsnDetailsList)
    .build();
```

**When Builder is useful:**
- Many constructor parameters (> 4)
- Optional parameters (avoid telescoping constructors)
- Immutable objects
- Complex object construction with validation

---

### Q169. Strategy pattern — GSTN validation strategies?

**Answer:**

```java
// Strategy interface
public interface ReturnValidationStrategy {
    ValidationResult validate(ReturnVO returnVO);
}

// Concrete strategies for different return types
public class GSTR1ValidationStrategy implements ReturnValidationStrategy {
    public ValidationResult validate(ReturnVO vo) {
        // Validate outward supplies, HSN codes, invoice details
    }
}

public class GSTR3BValidationStrategy implements ReturnValidationStrategy {
    public ValidationResult validate(ReturnVO vo) {
        // Validate summary figures, ITC claims, tax liability
    }
}

// Context — selects strategy at runtime
@Service
public class ReturnProcessor {
    private final Map<String, ReturnValidationStrategy> strategies;
    
    public ReturnProcessor(List<ReturnValidationStrategy> strategyList) {
        this.strategies = strategyList.stream()
            .collect(Collectors.toMap(s -> s.getType(), Function.identity()));
    }
    
    public void process(ReturnVO returnVO) {
        ReturnValidationStrategy strategy = strategies.get(returnVO.getType());
        ValidationResult result = strategy.validate(returnVO);
    }
}
```

**GSTN's AOP-based validation is similar to Strategy:**
```java
@Aspect
public class G2BApiValidator {
    @Before("execution(* org.gst.masters.api.controller.G2BController.*(..))")
    public void validateRequest() { /* validate based on request type */ }
}
```

---

### Q170. Observer pattern — event-driven and Kafka?

**Answer:**

Kafka is the **Observer pattern at massive scale**:
- **Subject (Producer)**: Filing service produces "RETURN_FILED" events
- **Observers (Consumers)**: Multiple services subscribe and react independently
  - Notification service → sends SMS/email
  - Ledger service → updates ledger balance
  - Dashboard service → updates statistics
  - Audit service → records audit trail

```java
// Spring Events — Observer within one application
@Component
public class ReturnFiledEventPublisher {
    @Autowired private ApplicationEventPublisher publisher;
    
    public void publishFiledEvent(ReturnVO vo) {
        publisher.publishEvent(new ReturnFiledEvent(this, vo));
    }
}

@Component
public class AuditListener {
    @EventListener
    public void onReturnFiled(ReturnFiledEvent event) {
        auditService.recordAudit(event.getReturnVO());
    }
}
```

---

### Q171. Template Method pattern in Spring?

**Answer:**

**Template Method** defines the skeleton of an algorithm, with subclasses overriding specific steps.

Spring uses this extensively:
- `JdbcTemplate` — handles connection management, you provide SQL
- `RestTemplate` — handles HTTP plumbing, you provide URL and type
- `AbstractRoutingDataSource` — you override `determineCurrentLookupKey()`

**GSTN Example — RoutingDataSource:**
```java
// Spring's template method — you only override the "variable" step
public class GSTNRoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DbType.getCurrentDb(); // GSTN overrides this one method
    }
    // AbstractRoutingDataSource.getConnection() uses this key to pick DataSource
}
```

---

### Q172. Proxy pattern — Spring AOP?

**Answer:**

Spring creates **proxies** around beans to add cross-cutting behavior (transactions, logging, security).

**Two proxy types:**
| | JDK Dynamic Proxy | CGLIB Proxy |
|--|---|---|
| Requires | Interface | No interface needed |
| Method | `java.lang.reflect.Proxy` | Generates subclass at runtime |
| Performance | Slightly slower | Slightly faster |
| Spring default | If bean implements interface | If bean has no interface |

```java
// When @Transactional is added, Spring creates proxy:
// Client → Proxy (begin TX) → Actual Bean Method → Proxy (commit/rollback)

@Service  // Spring creates CGLIB proxy (no interface)
public class ReturnService {
    @Transactional  // Proxy intercepts this method
    public void fileReturn(ReturnVO vo) { ... }
}
```

**GSTN AOP Logging uses JDK proxies:**
```java
@Aspect
public class LoggingAspect {
    @Before("execution(* org.gst..*(..))")
    public void logMethodEntry(JoinPoint joinPoint) {
        LOGGER.info("Entering: {}", joinPoint.getSignature().getName());
    }
}
```

---

### Q173–Q178. Decorator, Chain of Responsibility, Repository, Circuit Breaker, Adapter, Facade

**Q173. Decorator:** Wraps object to add behavior. Java I/O: `new BufferedReader(new InputStreamReader(new FileInputStream("file")))`. Each layer adds capability.

**Q174. Chain of Responsibility — Spring Security Filter Chain:**
```
Request → Filter1 (CORS) → Filter2 (Auth) → Filter3 (CSRF) → Controller
// Each filter decides to process and pass along OR reject
// GSTN's AuthorizationFilter is part of this chain
```

**Q175. Repository vs DAO:**
- **DAO**: Encapsulates database access, returns entities. More tightly coupled to persistence.
- **Repository**: Domain-driven, higher abstraction. Returns domain aggregates.
- `JpaRepository` in Spring Data is actually a Repository pattern.

**Q176. Circuit Breaker states:** CLOSED → (failures exceed threshold) → OPEN → (wait duration) → HALF-OPEN → (test calls) → CLOSED/OPEN

**Q177. Adapter:** Convert one interface to another. GSTN example: Converting legacy XML-based return data to new JSON-based format.

**Q178. Facade:** Simplified interface to complex subsystem. GSTN's `DistCacheUtil` is a Facade — provides simple methods (`getGstMstrDetails()`, `addToEntityDetailsCache()`) hiding complex Redis operations.

---

### Q179. SOLID principles?

**Answer:**

| Principle | Definition | GSTN Example |
|-----------|-----------|-------------|
| **S**ingle Responsibility | One class = one reason to change | `AuthorizationFilter` only handles auth, not business logic |
| **O**pen/Closed | Open for extension, closed for modification | Strategy pattern for validators — add new validator class, don't modify existing |
| **L**iskov Substitution | Subtypes replaceable for parent types | `GSTLogicalException extends Exception` — anywhere Exception is caught, GSTLogicalException works |
| **I**nterface Segregation | Many specific interfaces > one fat interface | `WFXAService`, `Anx1aService` — each service has its own interface |
| **D**ependency Inversion | Depend on abstractions, not concretions | Service depends on `JpaRepository` interface, not specific implementation |

---

### Q180. DRY, KISS, YAGNI?

**Answer:**

- **DRY (Don't Repeat Yourself):** GSTN's `Commons/` frameworks eliminate duplication — `GstExceptionFwk`, `DistCacheFwk`, `AuthenticationFwk` are shared across ALL services.
- **KISS (Keep It Simple, Stupid):** Field injection with `@Autowired` is simpler than complex factory patterns — works for GSTN's scale.
- **YAGNI (You Ain't Gonna Need It):** Don't build features until needed. Don't implement CQRS if simple queries work. Don't add WebFlux if MVC handles your load.

---

# SECTION 10: DOCKER & KUBERNETES (Q181–Q195)

### Q181. Docker — Container vs VM?

**Answer:**

| | Container | Virtual Machine |
|--|---|---|
| Isolation | **Process-level** (shared kernel) | **Hardware-level** (own kernel) |
| Size | **MB** (just app + deps) | **GB** (full OS) |
| Startup | **Seconds** | Minutes |
| Performance | **Near-native** | Overhead from hypervisor |
| Density | **100s per host** | Tens per host |
| Security | Shared kernel risk | Stronger isolation |

**Why containers for microservices:** Each GSTN service (ReturnAPI, LedgerAPI, etc.) packaged as a container. Lightweight, fast startup, consistent across environments (dev → prod).

---

### Q182. Dockerfile for Spring Boot?

**Answer:**

```dockerfile
# Multi-stage build — smaller final image
# Stage 1: Build
FROM maven:3.8-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:resolve  # Cache dependencies layer
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
RUN addgroup -S app && adduser -S app -G app  # Non-root user (security)
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
USER app  # Run as non-root
EXPOSE 8080
ENTRYPOINT ["java", "-XX:+UseG1GC", "-XX:MaxRAMPercentage=75", "-jar", "app.jar"]
```

**Why multi-stage:** Build stage has JDK + Maven (800MB+). Runtime only needs JRE (200MB). Final image is 4x smaller.

---

### Q183. Docker image layers?

**Answer:**

Each Dockerfile instruction creates a **layer**. Layers are cached — unchanged layers aren't rebuilt.

```dockerfile
FROM eclipse-temurin:17-jre-alpine    # Layer 1: Base image (cached)
COPY pom.xml .                         # Layer 2: POM (cache if unchanged)
RUN mvn dependency:resolve             # Layer 3: Dependencies (cached if POM unchanged)
COPY src ./src                         # Layer 4: Source code (changes frequently)
RUN mvn package                        # Layer 5: Build (rebuilds when src changes)
```

**Minimize image size:**
1. Use **Alpine** base images (5MB vs 200MB)
2. Multi-stage builds — discard build tools
3. **Order layers by change frequency** — put rarely changing layers first
4. Use `.dockerignore` to exclude unnecessary files
5. Combine RUN commands to reduce layers

---

### Q184. Docker security — non-root user?

**Answer:**

By default, containers run as **root** — if container is compromised, attacker has root access to host kernel.

```dockerfile
# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set ownership
COPY --chown=appuser:appgroup --from=builder /app/target/*.jar app.jar

# Switch to non-root user
USER appuser

# Now container process runs as "appuser" — limited privileges
```

**Additional security:**
- Read-only filesystem: `docker run --read-only`
- Drop capabilities: `--cap-drop ALL --cap-add NET_BIND_SERVICE`
- No new privileges: `--security-opt=no-new-privileges`
- Scan images for vulnerabilities: Trivy, Snyk

---

### Q185-Q186. Docker Compose and Networking

**Docker Compose for local development:**
```yaml
version: '3.8'
services:
  gstn-return-api:
    build: ./Core-API/ReturnAPI
    ports: ["8080:8080"]
    environment:
      - SPRING_PROFILES_ACTIVE=local
      - DB_HOST=mysql
      - REDIS_HOST=redis
      - KAFKA_BROKERS=kafka:9092
    depends_on: [mysql, redis, kafka]

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: gstn
    ports: ["3306:3306"]
    volumes: ["mysql-data:/var/lib/mysql"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  kafka:
    image: confluentinc/cp-kafka:latest
    ports: ["9092:9092"]

volumes:
  mysql-data:
```

**Networking:** Bridge (default — containers on same bridge talk via container name), Host (share host network), Overlay (multi-host — Docker Swarm/K8s).

---

### Q187. Kubernetes architecture?

**Answer:**

```
Control Plane (Master):
├── API Server        — REST API, entry point for all operations
├── etcd              — Distributed key-value store (cluster state)
├── Scheduler         — Assigns pods to nodes based on resources
└── Controller Manager — Ensures desired state = actual state
    ├── Deployment Controller
    ├── ReplicaSet Controller
    └── Service Controller

Worker Nodes:
├── kubelet           — Manages pods on the node
├── kube-proxy        — Network proxy, service routing
└── Container Runtime — Docker/containerd, runs containers
```

---

### Q188. K8s Objects?

**Answer:**

| Object | Purpose | GSTN Example |
|--------|---------|--------------|
| **Pod** | Smallest unit, one or more containers | Single ReturnAPI instance |
| **Deployment** | Manages ReplicaSet, rolling updates | `return-api-deployment` with 5 replicas |
| **Service** | Stable network endpoint | `return-api-svc` load-balances across pods |
| **ConfigMap** | Non-sensitive config | `gst.kafka.bootstrap-servers`, `gst.cache.ttl` |
| **Secret** | Sensitive config (base64) | DB passwords, JWT secrets |
| **Ingress** | External HTTP routing | Route `api.gst.gov.in/returns/*` → return-api-svc |
| **PVC** | Persistent storage | MySQL data volumes |
| **HPA** | Auto-scaling | Scale pods 3→20 during filing deadline |

---

### Q189. Deployment strategies?

**Answer:**

**Rolling Update (default):**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # Max 25% extra pods during update
      maxUnavailable: 25%   # Max 25% pods down during update
```
Gradually replaces old pods with new ones. Zero downtime. GSTN uses this for regular deployments.

**Recreate:**
```yaml
spec:
  strategy:
    type: Recreate  # Kill all old pods, then create new
```
Brief downtime. Used when old and new versions can't coexist (schema change).

---

### Q190. Blue-green vs Canary?

**Answer:**

**Blue-Green:**
```
Blue (current) → receiving all traffic
Green (new)    → deployed, tested, ready
Switch: Route ALL traffic to Green instantly
Rollback: Route back to Blue
```

**Canary:**
```
Stable (v1) → 95% traffic
Canary (v2) → 5% traffic → monitor metrics
If healthy → gradually increase: 10%, 25%, 50%, 100%
If unhealthy → route 100% back to v1
```

**GSTN:** Canary is preferred for filing services — test with small traffic first, especially during critical periods.

---

### Q191. Horizontal Pod Autoscaler (HPA)?

**Answer:**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: return-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: return-api
  minReplicas: 3
  maxReplicas: 50  # Scale up to 50 during deadline
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale when CPU > 70%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**GSTN filing deadline:** Normal: 3 pods. Deadline day: HPA scales to 50 pods based on CPU utilization. Custom metrics: Kafka consumer lag can also trigger scaling.

---

### Q192. Liveness vs Readiness probes?

**Answer:**

| | Liveness Probe | Readiness Probe |
|--|---|---|
| Purpose | Is the pod **alive**? | Is the pod **ready to serve**? |
| Failure | K8s **restarts** the pod | K8s **removes from service** (no traffic) |
| Use case | Detect deadlocks, hung processes | Warmup, dependency checks |
| Endpoint | `/actuator/health/liveness` | `/actuator/health/readiness` |

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3  # 3 failures → restart

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 3  # 3 failures → remove from service
```

**GSTN:** Readiness probe checks DB connection, Redis cache, Kafka broker connectivity. If any dependency is down, pod is removed from service → prevents errors from reaching users.

---

### Q193-Q195. ConfigMaps/Secrets, Service Types, Helm

**Q193. ConfigMaps & Secrets:**
```yaml
# ConfigMap — non-sensitive
apiVersion: v1
kind: ConfigMap
metadata: {name: gstn-config}
data:
  spring.profiles.active: prod
  gst.kafka.bootstrap-servers: kafka:9092

# Secret — sensitive (base64 encoded)
apiVersion: v1
kind: Secret
metadata: {name: gstn-secrets}
data:
  db-password: cGFzc3dvcmQxMjM=  # base64
```

Mounted as env vars or volume files.

**Q194. Service Types:**
| Type | Scope | Use Case |
|------|-------|----------|
| **ClusterIP** | Internal only | Service-to-service (default) |
| **NodePort** | External via node port | Development/testing |
| **LoadBalancer** | Cloud LB (ELB/NLB) | Production external access |
| **ExternalName** | DNS alias | External service reference |

**Q195. Helm Charts:** Package K8s manifests into reusable, parameterized templates. `values.yaml` configures per environment. `helm install gstn-return-api ./charts/return-api -f prod-values.yaml`

---

# SECTION 11: CI/CD (Q196–Q205)

### Q196. CI/CD pipeline?

**Answer:**

```
Code Commit (Git)
    ↓
Build (Maven: mvn clean package)
    ↓
Unit Tests (TestNG — GSTN uses TestNG 6.8.7)
    ↓
Code Quality (SonarQube — coverage, bugs, security)
    ↓
Docker Build (multi-stage Dockerfile)
    ↓
Push to Registry (Nexus/Docker Registry)
    ↓
Deploy to Dev/QA (K8s rolling update)
    ↓
Integration Tests (against real APIs/DB)
    ↓
Deploy to Staging
    ↓
Performance Tests
    ↓
Deploy to Production (Canary → Full rollout)
```

---

### Q197–Q205. Jenkins, SonarQube, Secrets, IaC, Flyway, GitFlow, Rollback, Artifacts, Testing

**Q197. Jenkins:** GSTN likely uses Jenkins for CI/CD. Pipeline defined in `Jenkinsfile`. Stages: Build → Test → SonarQube → Docker → Deploy.

**Q198. SonarQube:** Enforces quality gates — minimum 80% code coverage, 0 critical bugs, 0 vulnerabilities. Blocks deployment if gates fail.

**Q199. Secrets Management:** K8s Secrets for runtime. HashiCorp Vault for centralized secret management. Never commit secrets to Git.

**Q200. Infrastructure as Code:** Terraform for provisioning AWS resources (EC2, RDS, EKS). Versioned in Git, reviewed like code.

**Q201. DB Migrations in CI/CD:** Flyway runs as part of application startup (`spring.flyway.enabled=true`). Migration scripts versioned in Git alongside code.

**Q202. GitFlow:**
```
main    → production code
develop → integration branch
feature/* → feature development
release/* → release preparation
hotfix/*  → production bugfixes
```

**Q203. Rollbacks:** K8s: `kubectl rollout undo deployment/return-api`. Automated: if health check fails after deploy → auto rollback. Feature flags: disable new feature without redeployment.

**Q204. Artifact Versioning:** Semantic versioning (MAJOR.MINOR.PATCH). Stored in Nexus/Artifactory. Maven version in pom.xml. Docker tags: `return-api:2.5.1`.

**Q205. Test Types:**
- **Smoke test**: Basic functionality check after deployment (can API respond?)
- **Regression test**: Full test suite ensuring existing features work
- **Integration test**: Tests with real DB/Kafka/Redis (TestContainers)
