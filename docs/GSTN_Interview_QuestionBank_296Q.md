# Interview Question Bank — Jayanti Vishnoi (Specialist Programmer L2, 5.5 Years)
# Context: GSTN (Goods & Services Tax Network) — Large-scale government tax platform
# Stack: Java, Spring Boot, Hibernate, Golang, Angular, Kafka, Redis, MySQL, MongoDB, Docker, K8s, AWS
# Purpose: Feed this file + your GSTN codebase to Copilot for contextual answers

---

## SECTION 1: JAVA CORE (25 Questions)

### 1.1 Collections & Data Structures
Q1. How does HashMap work internally? What happens during hash collision? What changed in Java 8?
Q2. Difference between HashMap, LinkedHashMap, TreeMap, and ConcurrentHashMap? Which did you use in GSTN and why?
Q3. How does ConcurrentHashMap achieve thread safety? How is it different from Collections.synchronizedMap()?
Q4. ArrayList vs LinkedList — when to use each? Internal resizing of ArrayList?
Q5. How does HashSet work internally? What's the relationship between equals() and hashCode()?
Q6. What is the fail-fast vs fail-safe iterator? Which collections use which?
Q7. PriorityQueue internals — how does it work? When would you use it in a backend service?

### 1.2 Multithreading & Concurrency
Q8. Thread lifecycle in Java? How do you create threads (Thread class vs Runnable vs Callable)?
Q9. Difference between synchronized, volatile, and Atomic classes? When to use each?
Q10. What is ExecutorService? Types of thread pools (Fixed, Cached, Scheduled, SingleThread)? Which did you use for GSTN batch processing?
Q11. What is CompletableFuture? How did you use it for parallel API calls in GSTN?
Q12. What is a deadlock? How do you detect and prevent it? Have you faced one in production?
Q13. CountDownLatch vs CyclicBarrier vs Semaphore — differences and use cases?
Q14. What is ThreadLocal? When would you use it in a microservices context (e.g., storing request context)?
Q15. What is the Fork/Join framework? How does work-stealing algorithm work?

### 1.3 JVM Internals
Q16. Explain JVM memory model — Heap (Young Gen, Old Gen, Metaspace) vs Stack?
Q17. Types of Garbage Collectors — Serial, Parallel, G1GC, ZGC? Which is best for a low-latency tax filing service?
Q18. What causes OutOfMemoryError? Types (Heap space, Metaspace, GC overhead limit)? How do you troubleshoot?
Q19. What is JIT compilation? How does the JVM optimize hot code paths?
Q20. How does ClassLoader work? Bootstrap → Extension → Application? ClassNotFoundException vs NoClassDefFoundError?

### 1.4 Java 8+ Features
Q21. Functional interfaces — Predicate, Function, Consumer, Supplier, BiFunction? Give a real code example from GSTN.
Q22. Stream API — map, filter, reduce, collect, flatMap? Parallel streams — when are they beneficial and when dangerous?
Q23. Optional — how to use properly? Why is it better than returning null?
Q24. Default and static methods in interfaces — why were they added? How do they help backward compatibility?
Q25. What are Records (Java 14+) and Sealed classes (Java 17)? Have you used them?

---

## SECTION 2: SPRING BOOT (35 Questions — Highest Weightage)

### 2.1 Core Concepts
Q26. How does Spring Boot auto-configuration work? What role do @Conditional annotations play?
Q27. What is the difference between @Component, @Service, @Repository, and @Controller? Are they functionally different?
Q28. Explain Dependency Injection — Constructor injection vs Field injection vs Setter injection? Why is constructor injection recommended?
Q29. What is the Spring Bean lifecycle? @PostConstruct → InitializingBean → Custom init → @PreDestroy → DisposableBean?
Q30. Bean scopes — Singleton, Prototype, Request, Session? What's the default? When would you use Prototype in GSTN?
Q31. What is circular dependency? How does Spring handle it? How do you resolve it (using @Lazy, setter injection, or redesign)?
Q32. What is @Qualifier and when do you need it? How does it help when multiple beans of the same type exist?
Q33. Difference between @Bean and @Component? When to use which?
Q34. What is Spring ApplicationContext vs BeanFactory? Which is preferred and why?

### 2.2 Configuration & Properties
Q35. How do you fetch a property from application.properties/yml? @Value("${property.name}") — how to set default values?
Q36. @Value vs @ConfigurationProperties — when to use each? How does type-safe configuration binding work?
Q37. How do you manage multiple environments (dev, QA, staging, prod)? Spring Profiles — @Profile, application-{profile}.yml, activation methods?
Q38. How do you externalize configuration in production? Environment variables, ConfigServer, Vault for secrets?
Q39. What is @PropertySource? How do you load custom property files?

### 2.3 REST APIs
Q40. @GetMapping, @PostMapping, @PutMapping, @PatchMapping, @DeleteMapping — when to use each? PUT vs PATCH?
Q41. @PathVariable vs @RequestParam vs @RequestBody — differences with examples?
Q42. How do you implement pagination and sorting in REST APIs? Spring Data's Pageable?
Q43. How do you version REST APIs? URI versioning (/v1/returns) vs Header versioning vs Query param?
Q44. What is content negotiation? How does Spring handle JSON vs XML responses?
Q45. How do you validate request bodies? @Valid, @NotNull, @Size, @Pattern, custom validators?
Q46. What HTTP status codes do you use? 200, 201, 204, 400, 401, 403, 404, 409, 500 — when to use each?
Q47. How do you implement HATEOAS in Spring Boot? Have you used it?
Q48. How do you handle file upload/download in REST APIs? MultipartFile?

### 2.4 Exception Handling
Q49. What is @ControllerAdvice + @ExceptionHandler? How did you implement global exception handling in GSTN?
Q50. How do you create a custom exception hierarchy? BusinessException vs TechnicalException?
Q51. How do you return a standardized error response? (timestamp, status, message, path, errorCode)?
Q52. Checked vs Unchecked exceptions in Spring — when to throw which? ResponseStatusException?

### 2.5 Logging & Monitoring
Q53. SLF4J + Logback — how do you configure? Different log levels (TRACE, DEBUG, INFO, WARN, ERROR)?
Q54. What is MDC (Mapped Diagnostic Context)? How do you use it to trace requests across microservices?
Q55. How do you configure different log levels per environment (DEBUG in dev, WARN in prod)?
Q56. Spring Boot Actuator — what endpoints do you expose? /health, /metrics, /info, /env? How do you secure them?
Q57. How do you create custom health indicators? Example: checking if GSTN's downstream payment gateway is healthy?
Q58. How do you integrate with monitoring tools? Prometheus + Grafana? Micrometer metrics?

### 2.6 Transactions
Q59. @Transactional — how does it work internally (AOP proxy)? What happens if you call a @Transactional method from within the same class?
Q60. Transaction propagation types — REQUIRED, REQUIRES_NEW, NESTED, SUPPORTS, NOT_SUPPORTED, MANDATORY, NEVER? Give GSTN examples.
Q61. Transaction isolation levels — READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE? Which for GSTN payment processing?
Q62. What is a read-only transaction? @Transactional(readOnly = true) — what optimization does it provide?
Q63. How do you handle distributed transactions across microservices? XA transactions — you've worked with these. Two-phase commit and its limitations?

### 2.7 Security
Q64. How does Spring Security work? Security filter chain? Authentication vs Authorization?
Q65. JWT-based authentication flow — how do you implement it in Spring Boot?
Q66. How do you implement role-based access control (RBAC)? @PreAuthorize, @Secured?
Q67. CSRF protection — what is it? When to enable/disable?
Q68. How do you handle CORS in Spring Boot? @CrossOrigin vs global config?
Q69. OAuth2 — have you integrated with any OAuth2 provider? Client credentials flow vs Authorization code flow?

### 2.8 Advanced Spring Boot
Q70. What are Filters, Interceptors, and AOP? Differences and when to use each?
Q71. How do you implement rate limiting in Spring Boot? Bucket4j? Redis-based token bucket? Custom filter?
Q72. @Async — how to use it? How do you configure the TaskExecutor? Error handling in async methods?
Q73. @Scheduled — cron expressions, fixedRate vs fixedDelay? How do you prevent overlapping executions in a clustered environment?
Q74. What is Spring WebFlux? Reactive programming? When would you choose it over Spring MVC?
Q75. How do you write integration tests in Spring Boot? @SpringBootTest, MockMvc, @DataJpaTest, TestContainers?

---

## SECTION 3: HIBERNATE / JPA (15 Questions)

Q76. What is the difference between JPA, Hibernate, and Spring Data JPA?
Q77. Entity states — Transient, Persistent, Detached, Removed? How does the persistence context work?
Q78. @OneToMany, @ManyToOne, @ManyToMany, @OneToOne — how do you map relationships? Fetch types (LAZY vs EAGER)?
Q79. What is the N+1 query problem? How do you solve it? JOIN FETCH, @EntityGraph, @BatchSize?
Q80. First-level cache (Session) vs Second-level cache (SessionFactory)? How do you configure second-level cache with Redis/EhCache?
Q81. HQL vs JPQL vs Native SQL vs Criteria API — when to use each?
Q82. Optimistic locking (@Version) vs Pessimistic locking (@Lock)? When to use each in GSTN?
Q83. Database migration — Flyway vs Liquibase? How do you manage schema changes across environments?
Q84. How do you handle bulk inserts efficiently? batch_size, StatelessSession?
Q85. What is the Dirty Checking mechanism in Hibernate?
Q86. Projection queries — how do you fetch only specific columns instead of full entity?
Q87. What is @Embeddable and @Embedded? When to use composite keys (@EmbeddedId)?
Q88. Spring Data JPA — derived query methods, @Query, @Modifying? How do you write custom repository implementations?
Q89. How do you audit entities? @CreatedDate, @LastModifiedDate, @CreatedBy?
Q90. What is the difference between save(), saveAndFlush(), persist()? When does INSERT actually fire?

---

## SECTION 4: MICROSERVICES ARCHITECTURE (20 Questions)

Q91. How did you decompose GSTN into microservices? By domain (returns, registration, payments, e-way bills)?
Q92. Monolith vs Microservices — trade-offs? When would you NOT choose microservices?
Q93. Synchronous (REST/gRPC) vs Asynchronous (Kafka/RabbitMQ) communication — when to use each in GSTN?
Q94. What is an API Gateway? Responsibilities (routing, auth, rate limiting, load balancing)? Have you used Spring Cloud Gateway or Zuul?
Q95. Service Discovery — Eureka, Consul, or K8s DNS? How do GSTN services find each other?
Q96. Circuit Breaker pattern — Resilience4j? States (Closed, Open, Half-Open)? Fallback strategies? How did you prevent cascading failures?
Q97. Saga Pattern — Choreography vs Orchestration? How do you handle distributed transactions? GSTN example: filing → validation → payment → acknowledgment?
Q98. What is eventual consistency? Where do you accept it in GSTN vs where must you have strong consistency?
Q99. Bulkhead pattern — thread pool isolation? How do you prevent one slow service from bringing everything down?
Q100. Retry pattern — exponential backoff with jitter? How do you implement it with Resilience4j?
Q101. What is the Strangler Fig pattern? How would you migrate a monolith to microservices?
Q102. How do you handle API versioning across microservices?
Q103. What is an anti-corruption layer? When do you use it?
Q104. CQRS (Command Query Responsibility Segregation) — what is it? When would you use it for GSTN's read-heavy dashboards?
Q105. What is Event Sourcing? How is it different from traditional CRUD? Pros and cons?
Q106. How do you handle data consistency across microservices? Outbox pattern?
Q107. What is Service Mesh? Istio/Linkerd? When is it needed?
Q108. How do you test microservices? Contract testing (Pact)? Integration testing with TestContainers?
Q109. How do you manage shared libraries across microservices without tight coupling?
Q110. Distributed tracing — Zipkin/Jaeger/OpenTelemetry? How do you trace a request across 5+ GSTN microservices?

---

## SECTION 5: KAFKA (15 Questions)

Q111. Kafka architecture — Brokers, Topics, Partitions, Replicas, ISR (In-Sync Replicas)?
Q112. How does Kafka guarantee ordering? (Only within a partition.) How do you ensure all events for a GSTIN go to the same partition?
Q113. Producer configurations — acks=0 vs acks=1 vs acks=all? Which for GSTN filing events?
Q114. What is the role of the partition key? How do you choose it for GSTN?
Q115. Consumer Groups — how do they work? What triggers rebalancing? How to minimize rebalancing impact?
Q116. Offset management — auto commit vs manual commit? When to use each?
Q117. Exactly-once semantics — idempotent producers + transactional consumers? How complex is this in practice?
Q118. Dead Letter Queue (DLQ) — how do you handle poison messages? Retry strategy before DLQ?
Q119. Consumer lag — how do you monitor it? What actions do you take when lag increases during GSTN filing season?
Q120. Kafka vs RabbitMQ vs SQS — when to use each?
Q121. Kafka Streams vs Apache Flink — when to use each for stream processing?
Q122. How do you handle schema evolution? Avro + Schema Registry?
Q123. Kafka retention policies — time-based vs size-based? Compacted topics?
Q124. How do you handle back-pressure when consumers can't keep up with producers?
Q125. Kafka Connect — what is it? Source connectors vs Sink connectors?

---

## SECTION 6: REDIS (10 Questions)

Q126. Redis data structures — String, Hash, List, Set, Sorted Set? Which for session management? Rate limiting? Caching?
Q127. Redis eviction policies — LRU, LFU, allkeys-lru, volatile-ttl? Which for GSTN session cache?
Q128. Cache-aside vs Write-through vs Write-behind — which pattern for GSTN? Why?
Q129. Cache invalidation strategies — TTL, event-driven, versioned keys? How do you handle cache invalidation when taxpayer data updates?
Q130. Redis Cluster vs Sentinel — how do you ensure high availability?
Q131. Distributed locking with Redis — Redisson/RedLock? Scenario: preventing duplicate GST return processing?
Q132. Redis Pub/Sub vs Kafka — when to use each?
Q133. Redis persistence — RDB snapshots vs AOF (Append Only File)? Which for GSTN?
Q134. How do you handle cache stampede / thundering herd problem?
Q135. Redis pipelining and Lua scripting — when to use them for performance?

---

## SECTION 7: DATABASE & SQL (15 Questions)

Q136. Indexing — B-tree vs Hash indexes? Composite indexes? Covering indexes? How do you optimize queries on a table with 100M+ GST return records?
Q137. EXPLAIN/ANALYZE — how do you read a query execution plan? Full table scan vs Index scan vs Index-only scan?
Q138. ACID properties — explain with a GSTN transaction example?
Q139. Normalization (1NF, 2NF, 3NF, BCNF) vs Denormalization — when did you denormalize for performance?
Q140. Connection pooling — HikariCP? Max pool size, idle timeout, connection timeout configs? How many connections for 100K concurrent requests?
Q141. Read replicas — master-slave replication? How do you route read queries to replicas and writes to master?
Q142. Sharding strategies — range-based vs hash-based? How would you shard GSTN data by state/GSTIN?
Q143. Partitioning — table partitioning by date/range? How does it help GSTN's monthly return data?
Q144. Stored procedures vs application-level logic — pros/cons?
Q145. Database locking — row-level vs table-level? Shared locks vs Exclusive locks? Deadlocks in MySQL?
Q146. Slow query optimization — common causes and fixes?
Q147. MySQL vs PostgreSQL — key differences? Why did GSTN choose MySQL?
Q148. SQL joins — INNER, LEFT, RIGHT, FULL OUTER, CROSS? Self-join? Performance implications?
Q149. Subqueries vs JOINs — when is each more performant?
Q150. What is a materialized view? When would you use it for GSTN reporting?

---

## SECTION 8: DISTRIBUTED SYSTEMS CONCEPTS (15 Questions)

Q151. CAP Theorem — Consistency, Availability, Partition Tolerance? Which does GSTN prioritize? Why?
Q152. Consistent Hashing — what is it? How is it used in distributed caching and load balancing?
Q153. Leader Election — how do distributed systems choose a leader? Zookeeper, etcd?
Q154. Consensus algorithms — Raft, Paxos? Why are they important?
Q155. Idempotency — how do you ensure re-processing a message doesn't file a return twice? Idempotency keys?
Q156. Rate Limiting algorithms — Token Bucket, Leaky Bucket, Fixed Window, Sliding Window? Which for GSTN API rate limiting?
Q157. Load Balancing algorithms — Round Robin, Least Connections, Weighted, IP Hash, Consistent Hashing?
Q158. What is back-pressure? How do you implement it in a distributed system?
Q159. Distributed caching — challenges with consistency, invalidation, partitioning?
Q160. What is a distributed lock? How is it different from a database lock? Drawbacks?
Q161. What is a Bloom Filter? Where would you use it? (e.g., checking if a GSTIN exists before expensive lookup)
Q162. Write-Ahead Log (WAL) — what is it? How do databases and Kafka use it?
Q163. Gossip Protocol — how do distributed systems share state?
Q164. Split Brain problem — what is it? How do you prevent it?
Q165. What is clock skew in distributed systems? How do you handle it? Vector clocks, NTP?

---

## SECTION 9: DESIGN PATTERNS (15 Questions)

Q166. Singleton — how to implement thread-safe? Bill Pugh, Double-checked locking, Enum?
Q167. Factory Method vs Abstract Factory — when to use each?
Q168. Builder pattern — how does it relate to Lombok's @Builder? When is it useful?
Q169. Strategy pattern — how did you use it in GSTN? (e.g., different validation strategies for different return types)
Q170. Observer pattern — how does it relate to event-driven architecture and Kafka?
Q171. Template Method pattern — have you used it in Spring?
Q172. Proxy pattern — how does Spring AOP use it? JDK Dynamic Proxy vs CGLIB?
Q173. Decorator pattern — how does it work? InputStream chain in Java I/O?
Q174. Chain of Responsibility — how does Spring Security filter chain implement it?
Q175. Repository pattern — how is it different from DAO?
Q176. Circuit Breaker as a pattern — states and transitions?
Q177. Adapter pattern — when to use it? Converting legacy GSTN data formats?
Q178. Facade pattern — how do you simplify complex subsystem interactions?
Q179. SOLID principles — explain each with a code example?
Q180. DRY, KISS, YAGNI — how do you apply these in daily coding?

---

## SECTION 10: DOCKER & KUBERNETES (15 Questions)

Q181. What is Docker? Container vs VM? Why containers for microservices?
Q182. Dockerfile — write a Dockerfile for a Spring Boot app? Multi-stage builds? Why multi-stage?
Q183. Docker image layers — how do they work? How do you minimize image size?
Q184. Docker security — running as non-root user? How did you handle the root user issue?
Q185. Docker Compose — how do you define multi-container apps? Have you used it for local development with MySQL + Redis + Kafka?
Q186. Docker networking — bridge, host, overlay? How do containers communicate?
Q187. Kubernetes architecture — Master (API server, etcd, scheduler, controller manager) vs Worker (kubelet, kube-proxy)?
Q188. K8s objects — Pod, Deployment, Service, ConfigMap, Secret, Ingress, PersistentVolumeClaim?
Q189. K8s Deployment strategies — Rolling Update vs Recreate? maxSurge, maxUnavailable?
Q190. Blue-green vs Canary deployment — how to implement in K8s?
Q191. Horizontal Pod Autoscaler (HPA) — what metrics trigger scaling? How do you handle GSTN filing deadline traffic spikes?
Q192. Liveness vs Readiness probes — what endpoint? What happens if readiness probe fails vs liveness probe fails?
Q193. K8s ConfigMaps and Secrets — how do you manage configuration? How do you mount them?
Q194. K8s Service types — ClusterIP, NodePort, LoadBalancer, ExternalName?
Q195. Helm charts — what are they? How do you template K8s manifests?

---

## SECTION 11: CI/CD (10 Questions)

Q196. Describe your CI/CD pipeline? Code commit → build → unit tests → code quality → integration tests → deploy?
Q197. Jenkins vs GitLab CI vs GitHub Actions — which have you used? Pipeline configuration?
Q198. What is SonarQube? How do you enforce code quality gates (coverage, bugs, vulnerabilities)?
Q199. How do you manage secrets in CI/CD pipelines? Vault, AWS Secrets Manager?
Q200. What is Infrastructure as Code? Terraform/CloudFormation experience?
Q201. How do you handle database migrations in CI/CD? Flyway/Liquibase integration?
Q202. What is GitFlow? Feature branches, develop, release, hotfix branches?
Q203. How do you handle rollbacks? Automated rollback on health check failure?
Q204. What is artifact versioning? Nexus/Artifactory? Semantic versioning?
Q205. What is a smoke test vs regression test vs integration test in a pipeline?

---

## SECTION 12: CLOUD / AWS (15 Questions)

Q206. AWS services you've used — EC2, S3, RDS, SQS, SNS, Lambda, ECS/EKS, CloudWatch, IAM? Map each to GSTN usage.
Q207. EC2 instance types — compute optimized, memory optimized, general purpose? How do you choose for GSTN services?
Q208. S3 — storage classes (Standard, IA, Glacier)? Lifecycle policies? Presigned URLs? How do you store GST return documents?
Q209. SQS vs SNS vs Kafka — when to use each? SQS FIFO vs Standard?
Q210. AWS Lambda — cold starts, concurrency limits, timeout limits? When is serverless appropriate?
Q211. ECS vs EKS — when to use each? Fargate vs EC2 launch type?
Q212. CloudWatch — metrics, alarms, log groups? How do you set up alerting for GSTN service failures?
Q213. IAM — roles, policies, least privilege principle? How do you manage service-to-service authentication?
Q214. VPC — subnets (public vs private), security groups, NACLs, NAT gateway? How is GSTN's network architecture designed?
Q215. RDS — Multi-AZ, Read Replicas, automated backups? Which DB engine for GSTN?
Q216. Auto Scaling Groups — launch templates, scaling policies, target tracking?
Q217. ElastiCache (Redis/Memcached) — how do you manage caching in AWS?
Q218. AWS Bedrock — you've done POC work. How do you integrate LLM capabilities?
Q219. Cost optimization — Reserved Instances, Spot Instances, right-sizing? How do you reduce AWS costs?
Q220. AWS Well-Architected Framework — five pillars? Which is most important for GSTN?

---

## SECTION 13: NETWORKING & SECURITY (10 Questions)

Q221. HTTP/1.1 vs HTTP/2 vs HTTP/3 — key differences? Multiplexing, header compression?
Q222. HTTPS — TLS handshake flow? How does GSTN ensure data in transit is encrypted?
Q223. TCP vs UDP — when to use each? TCP three-way handshake?
Q224. DNS resolution — how does a request reach your GSTN service? DNS → Load Balancer → Service?
Q225. REST vs gRPC vs GraphQL — when to use each for inter-service communication?
Q226. OAuth2 and OpenID Connect — grant types? Which for GSTN?
Q227. OWASP Top 10 — SQL Injection, XSS, CSRF, Broken Authentication? How do you prevent each?
Q228. API security — rate limiting, API keys, JWT, mTLS? How do you secure GSTN APIs?
Q229. Encryption — symmetric vs asymmetric? AES vs RSA? Encryption at rest vs in transit?
Q230. Load balancing — L4 vs L7? Round Robin vs Least Connections? How is GSTN traffic distributed?

---

## SECTION 14: SYSTEM DESIGN (10 Scenarios)

Q231. Design a Tax Filing System (basically GSTN) — API gateway, services, database, caching, messaging, scalability?
Q232. Design a Rate Limiter — Token Bucket vs Sliding Window? Redis-based distributed rate limiter?
Q233. Design a Notification System — email, SMS, push for filing deadlines? Queue-based, retry, deduplication?
Q234. Design a URL Shortener — hashing, database design, caching, redirection?
Q235. Design a Distributed Cache — consistent hashing, eviction, replication?
Q236. Design a File Storage Service — like S3? Metadata DB, block storage, replication?
Q237. Design a Payment Processing System — idempotency, retry, reconciliation?
Q238. Design a Logging/Monitoring System — log aggregation, alerting, dashboards?
Q239. Design an Authentication/Authorization System — JWT, OAuth2, RBAC, session management?
Q240. Design a search system — inverted index, relevance scoring, ElasticSearch?

---

## SECTION 15: GOLANG (Since it's on your resume — 8 Questions)

Q241. Why Go over Java for certain services? When did you choose Go for Infosys MarketPlace?
Q242. Goroutines vs Java Threads — how is Go's concurrency model different?
Q243. Channels in Go — buffered vs unbuffered? How do you use them for communication?
Q244. Go interfaces — how are they different from Java interfaces? Duck typing?
Q245. Error handling in Go — no exceptions? How do you handle errors?
Q246. Go's garbage collector — how is it different from JVM's GC?
Q247. How did you use MongoDB + GraphQL with Go for Infosys MarketPlace?
Q248. Go's standard library — net/http, encoding/json? How did you build REST APIs in Go?

---

## SECTION 16: TESTING (8 Questions)

Q249. Unit testing vs Integration testing vs E2E testing — what's your testing strategy?
Q250. JUnit 5 — @Test, @BeforeEach, @AfterEach, @ParameterizedTest? Assertions?
Q251. Mockito — @Mock, @InjectMocks, @Spy? when(), verify(), ArgumentCaptor?
Q252. How do you achieve 90%+ code coverage? Is coverage a good metric?
Q253. TestContainers — how do you test with real databases/Redis/Kafka in integration tests?
Q254. MockMvc — how do you test REST controllers without starting the full server?
Q255. TDD vs BDD — have you practiced either? Pros and cons?
Q256. How do you test Kafka consumers and producers?

---

## SECTION 17: BEHAVIORAL / SITUATIONAL (10 Questions)

Q257. Tell me about yourself — your journey, experience, and what excites you?
Q258. Tell me about a production incident you handled at GSTN? How did you debug, fix, and prevent recurrence?
Q259. Describe a technically challenging problem you solved? What made it hard? What was your approach?
Q260. How do you handle tight deadlines? Give a GSTN filing season example.
Q261. Tell me about a disagreement with a team member on a technical approach? How did you resolve it?
Q262. How do you mentor junior developers? Give a specific example.
Q263. What's your biggest technical mistake and what did you learn from it?
Q264. How do you stay updated with technology? Learning approach?
Q265. Why do you want to switch/grow from your current role?
Q266. Where do you see yourself in 3-5 years?

---

## SECTION 18: QUICK-FIRE / RAPID ROUND (20 Short Answer Questions)

Q267. What is Spring Boot starter? How does it simplify dependency management?
Q268. What is the difference between @RestController and @Controller?
Q269. What is @ResponseBody?
Q270. What is Spring Boot DevTools? Hot reload?
Q271. What is Actuator's /health endpoint? How do you customize it?
Q272. What is @Conditional annotations? @ConditionalOnProperty, @ConditionalOnClass?
Q273. What is the embedded server in Spring Boot? Tomcat vs Jetty vs Undertow?
Q274. What is @EnableAutoConfiguration?
Q275. What is application.yml vs application.properties?
Q276. What is CommandLineRunner and ApplicationRunner?
Q277. What is @RequestMapping?
Q278. What is ResponseEntity? When to use it?
Q279. What is @Transient in JPA?
Q280. What is @Lazy annotation?
Q281. What is Spring AOP? @Aspect, @Before, @After, @Around?
Q282. What is connection pool exhaustion? How do you diagnose and fix it?
Q283. What is a DTO (Data Transfer Object)? Why not expose entities directly?
Q284. What is MapStruct? How do you map DTOs to entities?
Q285. What is Swagger/OpenAPI? How do you document REST APIs?
Q286. What is WebSocket? When would you use it instead of REST?

---

## SECTION 19: SCENARIO-BASED PROBLEM SOLVING (10 Questions)

Q287. GSTN's filing service is getting 10x traffic during deadline. Redis cache is returning stale data. How do you handle this?
Q288. A Kafka consumer is processing duplicate messages. How do you debug and fix?
Q289. Your Spring Boot service has a memory leak in production. How do you diagnose? (Heap dump, JVisualVM, MAT)
Q290. A database query that was running fine is suddenly slow. What do you check first? (Execution plan, index changes, data volume, locks)
Q291. Your microservice is timing out when calling another service. How do you handle gracefully? (Circuit breaker, timeout config, fallback)
Q292. You need to deploy a critical fix to production without downtime. How? (Blue-green, rolling deployment, feature flags)
Q293. A junior developer's code review shows they're using @Transactional on a method that calls an external API. What do you tell them? (Long transaction, connection holding, compensating transaction)
Q294. Your REST API needs to support both JSON and XML responses. How do you implement content negotiation?
Q295. You discover that your service is leaking database connections. How do you diagnose and fix? (HikariCP metrics, connection timeout, leak detection threshold)
Q296. Two microservices need to update their databases atomically. How do you solve this without XA transactions? (Saga, Outbox pattern)

---

## HOW TO USE THIS WITH COPILOT

### Instructions for Copilot:
1. Open this file alongside your GSTN codebase
2. For each question, ask Copilot: "Answer Q[number] with specific examples from this codebase"
3. Copilot will reference your actual code, class names, configurations, and patterns
4. Focus on Sections 2 (Spring Boot), 4 (Microservices), 5 (Kafka), and 7 (Database) — highest interview weightage

### Priority Order (15-hour prep plan):
- **Hours 1-4**: Section 2 (Spring Boot) — 35 questions, most commonly asked
- **Hours 4-6**: Section 1 (Java Core) — 25 questions, fundamentals
- **Hours 6-8**: Section 3 (Hibernate) + Section 7 (Database) — 30 questions combined
- **Hours 8-10**: Section 4 (Microservices) + Section 5 (Kafka) + Section 6 (Redis) — 45 questions
- **Hours 10-12**: Section 8 (Distributed Systems) + Section 14 (System Design) — 25 questions
- **Hours 12-14**: Section 10 (Docker/K8s) + Section 11 (CI/CD) + Section 12 (AWS) — 40 questions
- **Hours 14-15**: Section 17 (Behavioral) + Section 19 (Scenarios) — rapid verbal practice

### Remember:
- Don't just know the answer — practice SAYING it in 60-90 seconds
- Always tie answers back to GSTN (scale, users, architecture)
- Your weak areas from last interview: SLF4J/Logback config, Spring Profiles, @Value annotation — nail these first!
