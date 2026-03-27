# SECTIONS 4-6: MICROSERVICES, KAFKA, REDIS — Interview Answers (Q91–Q135)
## With GSTN Codebase References

---

# SECTION 4: MICROSERVICES ARCHITECTURE (Q91–Q110)

### Q91. How did you decompose GSTN into microservices?

**Answer:**

GSTN is decomposed by **business domain (bounded context)**, following Domain-Driven Design principles:

```
GSTN Microservice Architecture:
├── Core-API/
│   ├── RegistrationAPI      — Taxpayer registration, amendment, cancellation
│   ├── ReturnAPI             — GSTR1, GSTR3B filing and processing
│   ├── Return2API            — GSTR2 (inward supplies)
│   ├── Anx1API / Anx2API     — New Return annexures
│   ├── LedgerAPI             — Cash/ITC/Liability ledgers
│   ├── PaymentAPI / PmtAPI   — GST payment processing
│   ├── RefundAPI             — Refund claims and processing
│   ├── LitigationAPI         — Legal proceedings
│   ├── EinvoiceAPI           — E-Invoice generation
│   ├── ServicesAPI           — Common taxpayer services
│   ├── UserMastersAPI        — User management
│   ├── AuditAPI              — Audit trail
│   ├── CommunicationAPI      — Notifications (email/SMS)
│   ├── DashboardAPI          — Analytics and reporting
│   ├── MobileAPI             — Mobile app backend
│   ├── IMSAPI               — Invoice Management System
│   └── WelcomeLetterMS       — Welcome letter generation
├── BO-Web/ (Back Office)
│   ├── BOServicesWeb         — BO common services
│   ├── BOAuditWeb            — Audit operations
│   ├── BOLitigationWeb       — Litigation management
│   ├── BOMISWeb              — Management Information System
│   └── BOReturnsWeb          — Return processing
├── Commons/ (Shared Frameworks)
│   ├── AuthenticationFwk     — Authentication framework
│   ├── KafkaConsumerFwk      — Kafka consumer framework
│   ├── DistCacheFwk          — Distributed caching (Redis)
│   ├── WorkFlowFwk           — Workflow engine
│   ├── GstExceptionFwk       — Exception handling
│   └── gst-spring-boot2-starter — Custom Spring Boot starter
└── Common-Web/
    └── CommonServicesWeb     — Shared web services
```

**Each service has:**
- Its own database schema (or shared with routing)
- Its own pom.xml with specific dependencies
- Independent deployment
- Communication via REST (sync) or Kafka (async)

---

### Q92. Monolith vs Microservices — trade-offs?

**Answer:**

| Aspect | Monolith | Microservices |
|--------|----------|---------------|
| Deployment | Single unit | Independent per service |
| Complexity | Simple start, complex growth | Complex start, manageable growth |
| Team scaling | Merge conflicts, bottlenecks | Independent teams per service |
| Data management | Shared DB, ACID easy | Distributed data, eventual consistency |
| Debugging | Stack trace, easy | Distributed tracing needed |
| Latency | In-process calls | Network calls (latency) |
| Technology | Single stack | Polyglot possible |

**When NOT to use microservices:**
- Small team (< 5 developers)
- Simple domain with low complexity
- Startup with unclear domain boundaries
- When you can't afford operational overhead (K8s, monitoring, tracing)

**GSTN Choice:** GSTN handles 1B+ invoices/month, 14M+ taxpayers, filing deadline spikes. Microservices allow:
- **Independent scaling**: ReturnAPI scales 10x during deadlines while RegistrationAPI stays at 2x
- **Independent deployment**: Critical fix to PaymentAPI doesn't require redeploying everything
- **Team autonomy**: 40+ developers across teams, each owning their services

---

### Q93. Synchronous vs Asynchronous communication?

**Answer:**

| | Synchronous (REST) | Asynchronous (Kafka) |
|--|------|------|
| Pattern | Request-Response | Fire-and-Forget / Event-Driven |
| Coupling | **Temporal** — both must be running | **Decoupled** — producer doesn't wait |
| Latency | Immediate response | Eventual processing |
| Failure | Cascading failures possible | Buffered — consumer retries |
| Use when | Need immediate response | Can tolerate delay |

**GSTN Examples:**

**Synchronous (REST):**
- Filing return → real-time validation → immediate response (valid/invalid)
- Taxpayer login → authentication check → immediate token
- Dashboard data → aggregate from multiple services → immediate display

**Asynchronous (Kafka):**
- Return filed → Send notification (email/SMS) → doesn't need immediate
- Return filed → Update ledger → can be eventually consistent
- E-invoice generated → propagate to return system → async processing

```java
// Async — Kafka producer in GSTN
@Autowired
private CommonKafkaProducerUtil commonKafkaProducerUtil;

public void sendMessage(String topic, String kafkaMsg, String key) {
    commonKafkaProducerUtil.syncProducedWKey(topic, kafkaMsg, key);
}
```

---

### Q94. What is an API Gateway?

**Answer:**

API Gateway is a **single entry point** for all client requests. It handles cross-cutting concerns:

| Responsibility | How |
|---------------|-----|
| **Routing** | Route `/v1/returns/*` → ReturnAPI, `/v1/registration/*` → RegistrationAPI |
| **Authentication** | Validate JWT before forwarding |
| **Rate limiting** | Throttle requests per client |
| **Load balancing** | Distribute across service instances |
| **SSL termination** | Handle HTTPS, forward HTTP internally |
| **Request/Response transformation** | Add headers, modify payloads |
| **Circuit breaking** | Protect against cascading failures |

**GSTN Architecture:**
```
Internet → CDN → API Gateway → Internal Services
                    │
                    ├── /v1.0/taxpayerapi/anx1a/* → Anx1API
                    ├── /auth/api/case/*          → BOAuditWeb
                    ├── /auth/api/returns/*        → ReturnAPI
                    └── /auth/api/ledger/*         → LedgerAPI
```

---

### Q95. Service Discovery?

**Answer:**

**Kubernetes DNS** — GSTN uses K8s-based service discovery:
- Each K8s Service gets a DNS name: `return-api.gstn-namespace.svc.cluster.local`
- No need for Eureka/Consul — K8s provides built-in discovery
- kube-proxy handles load balancing across pod replicas

**Spring Cloud alternatives:**
- **Eureka** — Netflix OSS, Java-native, heartbeat-based
- **Consul** — HashiCorp, multi-DC, health checking
- **K8s DNS** — simplest in K8s environment (GSTN's approach)

---

### Q96. Circuit Breaker pattern — Resilience4j?

**Answer:**

**Three states:**
```
CLOSED (normal) 
    → failure rate > threshold (50%) 
    → OPEN (reject all requests, return fallback)
    → after wait duration (60s)
    → HALF-OPEN (allow N trial requests)
    → if trial succeeds → CLOSED
    → if trial fails → OPEN
```

```java
// Resilience4j Circuit Breaker
@CircuitBreaker(name = "paymentGateway", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentGatewayClient.pay(request); // External call
}

public PaymentResponse paymentFallback(PaymentRequest request, Exception e) {
    LOGGER.warn("Payment gateway unavailable, queuing for retry", e);
    kafkaProducer.send("payment-retry-topic", request);
    return PaymentResponse.queued("Payment queued for processing");
}
```

**GSTN scenario:** During filing deadline, if the payment gateway becomes slow:
1. Circuit opens → stops calling failing gateway
2. Returns fallback response → "Payment processing delayed, will be retried"
3. Queues request to Kafka for retry
4. After gateway recovers → circuit half-opens → tests → closes

---

### Q97. Saga Pattern — Choreography vs Orchestration?

**Answer:**

**GSTN Filing Saga Example:**

```
Filing → Validation → Payment → Ledger Update → Acknowledgment
```

**Choreography (event-driven):**
```
Filing Service publishes "RETURN_FILED" event
    → Validation Service consumes, validates, publishes "VALIDATED"
        → Payment Service consumes, processes payment, publishes "PAID"
            → Ledger Service consumes, updates ledger, publishes "LEDGER_UPDATED"
                → Acknowledgment Service sends confirmation
                
Compensating: If Payment fails → publishes "PAYMENT_FAILED"
    → Validation Service rolls back validation status
    → Filing Service marks return as "FAILED"
```

**Orchestration (central coordinator):**
```java
public class FilingSagaOrchestrator {
    public void executeFilingSaga(ReturnVO returnVO) {
        try {
            validationService.validate(returnVO);     // Step 1
            paymentService.processPayment(returnVO);  // Step 2
            ledgerService.updateLedger(returnVO);      // Step 3
            ackService.sendAcknowledgment(returnVO);   // Step 4
        } catch (PaymentException e) {
            // Compensate: undo validation
            validationService.undoValidation(returnVO);
        }
    }
}
```

| | Choreography | Orchestration |
|--|---|---|
| Coordination | Events between services | Central orchestrator |
| Coupling | Loose — services don't know each other | Tighter — orchestrator knows all steps |
| Complexity | Harder to track flow | Easier to understand and debug |
| Single point of failure | No | Yes (orchestrator) |

---

### Q98. Eventual consistency?

**Answer:**

**Strong consistency required (GSTN):**
- Payment processing → immediate balance deduction
- Ledger balance → must be accurate for next operation
- Filing status → must be consistent for duplicate check

**Eventual consistency acceptable (GSTN):**
- Notification after filing → email can be delayed by minutes
- Dashboard/MIS reports → can show slightly stale data
- Search indexes → can take seconds to update
- Cross-service data propagation → ledger reflects filing after Kafka processing

**Pattern:** Use strong consistency within a service (ACID transactions). Accept eventual consistency between services (Kafka events).

---

### Q99. Bulkhead pattern?

**Answer:**

**Isolate resources** so one slow service doesn't exhaust all resources:

```java
// Thread pool bulkhead — separate thread pools per service call
@Bulkhead(name = "paymentService", type = Bulkhead.Type.THREADPOOL,
          fallbackMethod = "paymentFallback")
public PaymentResponse pay(PaymentRequest req) { ... }

// Configuration
resilience4j.bulkhead.instances.paymentService:
  maxConcurrentCalls: 25        # Max 25 concurrent calls
  maxWaitDuration: 500ms        # Wait 500ms before rejecting

resilience4j.thread-pool-bulkhead.instances.paymentService:
  maxThreadPoolSize: 10
  coreThreadPoolSize: 5
  queueCapacity: 20
```

**GSTN:** Without bulkhead, if Payment Gateway slows down, all 200 Tomcat threads could be waiting for payment → entire service unresponsive. With bulkhead, only 25 threads are allocated to payment calls → remaining 175 threads serve other requests.

---

### Q100. Retry pattern with exponential backoff?

**Answer:**

```java
@Retry(name = "paymentRetry", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentGateway.pay(request);
}

// Configuration
resilience4j.retry.instances.paymentRetry:
  maxAttempts: 3
  waitDuration: 1s
  enableExponentialBackoff: true
  exponentialBackoffMultiplier: 2  # 1s, 2s, 4s
  randomizedWaitFactor: 0.5       # Jitter: adds 0-50% random delay
  retryExceptions:
    - java.net.ConnectException
    - java.net.SocketTimeoutException
  ignoreExceptions:
    - org.gst.excep.GSTLogicalException  # Don't retry business errors
```

**Why jitter?** Without it, if 1000 requests fail simultaneously, they ALL retry at the same time → thundering herd → service overwhelmed again. Jitter spreads retries over time.

---

### Q101–Q105. Strangler Fig, API Versioning, Anti-corruption Layer, CQRS, Event Sourcing

**Q101. Strangler Fig Pattern:**
Gradually replace monolith by routing requests to new microservices one endpoint at a time. Use API gateway to route: old endpoints → monolith, migrated endpoints → new service. Eventually, monolith is "strangled" and can be decommissioned.

**Q102. API Versioning across microservices:**
GSTN uses URI versioning: `/v1.0/taxpayerapi/anx1a/getrecords`. Each service manages its own version independently. API Gateway routes to correct version.

**Q103. Anti-corruption Layer:**
A translation layer between your service and a legacy/external system. Prevents legacy data models from "corrupting" your clean domain model.
```java
// Adapter to convert legacy GSTN data format to new model
public class LegacyGstReturnAdapter {
    public NewReturnModel convert(LegacyReturnFormat legacy) {
        NewReturnModel model = new NewReturnModel();
        model.setGstin(legacy.getTIN());  // TIN → GSTIN
        model.setPeriod(convertPeriod(legacy.getRetPrd()));
        return model;
    }
}
```

**Q104. CQRS:**
Separate read and write models. GSTN use case: Write model stores raw return data in MySQL. Read model stores pre-aggregated data in separate read-optimized tables or Solr (GSTN uses SolrDIHFwk for search). Dashboard queries read from optimized read models.

**Q105. Event Sourcing:**
Store every state change as an immutable event instead of current state. Pros: complete audit trail, replay capability. Cons: complex queries, eventual consistency. GSTN stores audit events in `ALERT_DETL` tables and publishes to Kafka for event-driven processing.

---

### Q106. Outbox pattern?

**Answer:**

```
Service → Write to DB (business data + outbox table) → atomically (single TX)
Outbox Poller → reads outbox table → publishes to Kafka → marks as published
```

```java
@Transactional
public void fileReturn(ReturnVO returnVO) {
    // Step 1: Save return
    returnRepository.save(returnEntity);
    
    // Step 2: Write to outbox table (same transaction!)
    OutboxEvent event = new OutboxEvent();
    event.setAggregateId(returnVO.getGstin());
    event.setType("RETURN_FILED");
    event.setPayload(toJson(returnVO));
    event.setStatus("PENDING");
    outboxRepository.save(event);
    // Both are committed atomically — no data loss
}

// Separate scheduled job polls outbox and publishes to Kafka
@Scheduled(fixedDelay = 1000)
public void publishOutboxEvents() {
    List<OutboxEvent> pending = outboxRepository.findByStatus("PENDING");
    for (OutboxEvent event : pending) {
        kafkaProducer.send(event.getType(), event.getPayload());
        event.setStatus("PUBLISHED");
        outboxRepository.save(event);
    }
}
```

**Why?** Avoids dual-write problem — writing to DB and Kafka separately can leave them inconsistent if one fails.

---

### Q107–Q110. Service Mesh, Testing, Shared Libraries, Distributed Tracing

**Q107. Service Mesh (Istio):**
A dedicated infrastructure layer for service-to-service communication. Handles mTLS, traffic management, observability without code changes. Each pod gets a sidecar proxy (Envoy). Needed for: zero-trust networking, canary deployments, traffic shifting.

**Q108. Testing microservices:**
- **Contract Testing (Pact)**: Consumer defines expected API → provider verifies
- **Integration Testing (TestContainers)**: Real MySQL/Redis/Kafka in Docker containers
- **GSTN uses TestNG** for unit and integration tests (testng.xml in each module)

**Q109. Shared libraries (GSTN approach):**
```
Commons/ — shared frameworks
├── GstExceptionFwk    — Common exception classes
├── DistCacheFwk       — Redis caching utility
├── KafkaConsumerFwk   — Kafka consumer framework
├── AuthenticationFwk  — Auth utilities
├── WorkFlowFwk        — Workflow engine
├── gst-spring-boot2-starter — Auto-configuration
└── CommonUtilFwk      — General utilities
```
Each is a Maven artifact with its own version. Services depend on specific versions via pom.xml. Breaking changes require version bump and coordinated migration.

**Q110. Distributed Tracing:**
Pass correlation ID across services via HTTP header. Use MDC for logging:
```java
MDC.put("requestId", request.getHeader("X-Request-ID"));
// All logs in this thread include requestId
// Forward same requestId to downstream calls
```
Tools: Zipkin, Jaeger, OpenTelemetry for end-to-end trace visualization.

---

# SECTION 5: KAFKA (Q111–Q125)

### Q111. Kafka architecture?

**Answer:**

```
Producer → [Topic: return-filed-events]
              ├── Partition 0 → Broker 1 (Leader), Broker 2 (Replica)
              ├── Partition 1 → Broker 2 (Leader), Broker 3 (Replica)
              └── Partition 2 → Broker 3 (Leader), Broker 1 (Replica)
                                    ↓
           Consumer Group: filing-processor-group
              ├── Consumer 1 ← Partition 0
              ├── Consumer 2 ← Partition 1
              └── Consumer 3 ← Partition 2
```

**Key concepts:**
- **Broker**: Kafka server that stores and serves data
- **Topic**: Named category/feed (e.g., `return-filed-events`)
- **Partition**: Ordered, immutable sequence of messages. Parallelism unit.
- **Replica**: Copy of partition for fault tolerance
- **ISR (In-Sync Replicas)**: Replicas that are fully caught up with leader

**GSTN Kafka config:**
```java
// From KafkaClientProperties — Spring Boot properties
@Data
@ConfigurationProperties(prefix = "gst.kafka")
public class KafkaClientProperties {
    private String bootstrapServers;   // Broker addresses
    private String clientId;           // Client identifier
    private Producer producer = new Producer();
    private Consumer consumer = new Consumer();
}
```

---

### Q112. How does Kafka guarantee ordering?

**Answer:**

Kafka guarantees ordering **only within a single partition**. Messages across partitions have no ordering guarantee.

**GSTN approach — partition by GSTIN:**
```java
// Use GSTIN as partition key
// All events for same GSTIN go to same partition → ordered processing
commonKafkaProducerUtil.syncProducedWKey(topic, kafkaMsg, gstin);  // gstin is the key

// Partitioning: hash(gstin) % numPartitions = partition number
// 29AAACG1234A1ZD → hash → partition 2
// All subsequent events for this GSTIN → partition 2 → processed in order
```

**Why this matters:** A return filing event MUST be processed before its amendment event. Using GSTIN as key guarantees this order.

---

### Q113. Producer acks configuration?

**Answer:**

| acks | Durability | Latency | When to use |
|------|-----------|---------|-------------|
| `0` | None — fire and forget | Fastest | Metrics, logs (loss acceptable) |
| `1` | Leader acknowledged | Medium | Most use cases |
| `all` (-1) | All ISR acknowledged | Slowest | **GSTN filing events** (no data loss) |

```java
// GSTN Kafka Producer config
@Data
public static class Producer {
    private String acks;            // "all" for filing events
    private String compressionType; // "snappy" for performance
    private Integer batchSize;      // 16384 bytes
    private Integer retries;        // 3 retries on failure
}
```

**For GSTN filing events:** `acks=all` because losing a return filing event is unacceptable. For metrics/logging events: `acks=1` is sufficient.

---

### Q114. Partition key selection?

**Answer:**

**GSTN:** Use **GSTIN** as partition key because:
1. All events for one taxpayer go to same partition → ordered processing
2. Even distribution — 14M+ GSTINs distribute well across partitions
3. Consumer can aggregate all events for a GSTIN without cross-partition coordination

```java
// From KafkaServiceImpl
public void sendMessage(String topic, String kafkaMsg, String key) {
    commonKafkaProducerUtil.syncProducedWKey(topic, kafkaMsg, key);
    // key = gstin → determines partition
}
```

**Bad partition keys:**
- State code (only 37 values → uneven distribution)
- Timestamp (sequential → all go to one partition)
- Random UUID (no ordering guarantee for same entity)

---

### Q115. Consumer Groups and rebalancing?

**Answer:**

**Consumer Group:** Multiple consumers sharing the workload of a topic. Each partition is consumed by exactly ONE consumer in the group.

```
Topic: return-events (6 partitions)
Consumer Group: filing-processor

Consumer 1 → P0, P1    (2 partitions each if 3 consumers)
Consumer 2 → P2, P3
Consumer 3 → P4, P5
```

**Rebalancing triggers:**
- Consumer joins or leaves group
- Consumer heartbeat timeout (crashes)
- Topic partition count changes
- Consumer takes too long to process (exceeds `max.poll.interval.ms`)

**Minimize rebalancing impact:**
1. **Static membership** (`group.instance.id`) — consumer restarts don't trigger rebalance
2. **Incremental cooperative rebalancing** — only revoke affected partitions
3. **Tune timeouts**: `session.timeout.ms`, `heartbeat.interval.ms`, `max.poll.interval.ms`

**GSTN KafkaConsumerFwk:**
```java
// From KafkaConsumerConfig — singleton pattern for config
public class KafkaConsumerConfig {
    private static KafkaConsumerConfig instance = new KafkaConsumerConfig();
    private Properties props = new Properties();
    private List<String> topicList = null;
    
    public KafkaConsumer<Long, String> getNewConsumer() {
        return new KafkaConsumer<Long, String>(props);
    }
}
```

---

### Q116. Offset management?

**Answer:**

| | Auto Commit | Manual Commit |
|--|---|---|
| Config | `enable.auto.commit=true` | `enable.auto.commit=false` |
| When | Every `auto.commit.interval.ms` | After processing |
| Risk | Data loss (committed before processed) | Duplicate processing (crash before commit) |
| Use case | Tolerant of loss | **GSTN — must process everything** |

```java
// Manual commit (at-least-once)
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        processRecord(record);  // Process first
    }
    consumer.commitSync();  // Then commit — ensures at-least-once
}
```

---

### Q117. Exactly-once semantics?

**Answer:**

**Exactly-once = Idempotent producer + Transactional consumer**

```java
// Producer — idempotent (no duplicates)
props.put("enable.idempotence", true);
props.put("acks", "all");
props.put("retries", Integer.MAX_VALUE);

// Producer — transactional (atomic writes across partitions/topics)
props.put("transactional.id", "filing-producer-1");
producer.initTransactions();
producer.beginTransaction();
producer.send(record1);
producer.send(record2);
producer.commitTransaction(); // Both or neither

// Consumer — read committed + manual offset
props.put("isolation.level", "read_committed"); // Only read committed messages
```

**In practice:** Exactly-once across systems is very hard. GSTN uses **at-least-once + idempotency** — process messages at least once, but design handlers to be idempotent (processing same message twice has no side effect).

---

### Q118. Dead Letter Queue (DLQ)?

**Answer:**

```java
// GSTN Kafka Consumer with error topic handling
// From Consumer.java in KafkaConsumerFwk
public void scheduleErrorTopicConsumptionAt(int startHr, int startMin, int startSec, 
                                             long stopInSecs) {
    ScheduledExecutorService scheduledExecutorService = Executors.newScheduledThreadPool(2);
    scheduledExecutorService.scheduleAtFixedRate(/* consume error topic */);
}
```

**DLQ pattern:**
```
Main Topic → Consumer tries processing
    ↓ Failure (parse error, validation)
Retry Topic → Retry 3 times with backoff
    ↓ Still failing
DLQ Topic → Stores permanently for manual investigation
```

```java
public void processMessage(ConsumerRecord<String, String> record) {
    try {
        businessLogic(record.value());
    } catch (TransientException e) {
        // Retryable — publish to retry topic
        kafkaProducer.send("FILING_RETRY_TOPIC", record.value());
    } catch (PoisonMessageException e) {
        // Non-retryable — publish to DLQ
        kafkaProducer.send("FILING_DLQ_TOPIC", record.value());
        LOGGER.error("Poison message sent to DLQ: {}", record.key());
    }
}
```

---

### Q119–Q125. Consumer Lag, Kafka vs RabbitMQ, Streams, Schema Registry, Retention, Back-pressure, Connect

**Q119. Consumer lag monitoring:**
- Monitor with: `kafka-consumer-groups.sh --describe`, Burrow, Grafana dashboards
- During GSTN filing season: if lag increases → scale consumers (add more instances to consumer group) or increase partitions
- Alert thresholds: Warning at 10K lag, Critical at 100K lag

**Q120. Kafka vs RabbitMQ vs SQS:**

| | Kafka | RabbitMQ | SQS |
|--|---|---|---|
| Model | Log-based (pull) | Message queue (push) | Managed queue |
| Throughput | **Millions/sec** | Thousands/sec | Thousands/sec |
| Replay | **Yes** (retention-based) | No (consumed = gone) | No |
| Ordering | Per-partition | Per-queue | FIFO queues |
| Best for | Event streaming, GSTN | Task distribution, RPC | AWS-native, simple queues |

**Q121. Kafka Streams vs Flink:**
- Kafka Streams: Library (no separate cluster), simple stateful processing
- Flink: Standalone cluster, complex event processing, windowing, exactly-once

**Q122. Schema evolution (Avro + Schema Registry):**
- Schema Registry stores Avro schemas centrally
- Backward/Forward compatibility checks prevent breaking changes
- GSTN could use for evolving return filing event schemas

**Q123. Retention policies:**
- Time-based: `retention.ms=604800000` (7 days)
- Size-based: `retention.bytes=1073741824` (1GB per partition)
- Compacted: Keep only latest value per key (good for state stores)

**Q124. Back-pressure handling:**
- Increase consumers (scale horizontally)
- Increase partitions (more parallelism)
- `max.poll.records` — limit records per poll
- Pause/resume partitions based on processing capacity

**Q125. Kafka Connect:**
- Source connectors: DB → Kafka (CDC with Debezium)
- Sink connectors: Kafka → DB/Elasticsearch/S3
- GSTN uses SolrDIHFwk for similar data ingestion patterns

---

# SECTION 6: REDIS (Q126–Q135)

### Q126. Redis data structures?

**Answer:**

| Data Structure | Use Case in GSTN |
|----------------|-----------------|
| **String** | Session tokens, simple key-value cache (`authToken → userId`) |
| **Hash** | Store taxpayer session data (`session:12345 → {gstin, role, loginTime}`) |
| **List** | Recent activity log, message queue |
| **Set** | Unique GSTIN tracking, deduplication |
| **Sorted Set** | Rate limiting (scored by timestamp), leaderboards |
| **HyperLogLog** | Count unique visitors/GSTINs (approximate) |

**GSTN DistCacheUtil methods:**
```java
// String operations — simple caching
public GSTMaster getGstMstrDetails(String uid)
public void addToEntityDetailsCache(String userName, List<EntityDetails> entityList)

// Session management
public EntityDetails getEntityDetails(String userName)
public void addToCaptchaCacheForAudio(String token, String captchaAnswer)
public void removeCaptchaForAudio(String token)

// Risk assessment caching
public void addToRiskAssesmentCache(String key, RiskAssessment value)
public RiskAssessment getRiskAssesmentCacheValue(String key)
public void removeFromRiskAssesmentCache(String key)

// OTP caching
public String getOtpCacheValue(String username)
public void removeFromOtpCache(String username)
```

---

### Q127. Redis eviction policies?

**Answer:**

| Policy | Evicts From | Algorithm | Use Case |
|--------|------------|-----------|----------|
| `noeviction` | Nothing | Return error | When data loss is unacceptable |
| `allkeys-lru` | All keys | **LRU** | General-purpose cache |
| `volatile-lru` | Keys with TTL | LRU | Mixed: cache + persistent data |
| `allkeys-lfu` | All keys | **LFU** | Frequency-based (hot data stays) |
| `volatile-ttl` | Keys with TTL | Shortest TTL first | Time-sensitive data |

**For GSTN session cache:** `volatile-lru` — sessions have TTL, evict least recently used when memory is full. Reference data (state codes, HSN codes) doesn't have TTL and is preserved.

---

### Q128. Cache-aside vs Write-through vs Write-behind?

**Answer:**

**Cache-Aside (Lazy Loading) — GSTN's pattern:**
```java
// GSTN's DistCacheUtil implements cache-aside
public GSTMaster getGstMstrDetails(String uid) {
    // 1. Check cache first
    GSTMaster cached = cache.get("gstm:" + uid);
    if (cached != null) return cached;
    
    // 2. Cache miss → query database
    GSTMaster fromDb = repository.findByUid(uid);
    
    // 3. Put in cache for next time
    cache.put("gstm:" + uid, fromDb, TTL_SECONDS);
    return fromDb;
}
```

| Pattern | Write | Read | Consistency | GSTN? |
|---------|-------|------|-------------|-------|
| **Cache-Aside** | Write to DB, invalidate cache | Check cache → miss → read DB → cache | Eventual | **Yes** |
| Write-Through | Write to cache AND DB simultaneously | Read from cache | Strong | No |
| Write-Behind | Write to cache → async write to DB | Read from cache | Eventual | No |

**Why Cache-Aside for GSTN:** Simple, tolerant of cache failures (fallback to DB), no cache dependency for writes.

---

### Q129. Cache invalidation strategies?

**Answer:**

1. **TTL (Time-To-Live)**: Auto-expire after fixed time — simplest, used for sessions
2. **Event-driven**: When data changes, publish event → invalidate cache
3. **Versioned keys**: `gstm:v2:29AAACG1234A1ZD` — increment version on update

```java
// GSTN pattern — TTL-based with explicit invalidation
// Set with TTL
distCacheUtil.addToEntityDetailsCache(userName, entityList); // Has TTL

// Explicit removal when data changes
distCacheUtil.removeFromRiskAssesmentCache(key);
distCacheUtil.removeFromOtpCache(username);
distCacheUtil.removeCaptchaForAudio(token);
```

**When taxpayer data updates:**
1. Save to DB → publish "TAXPAYER_UPDATED" to Kafka
2. Cache invalidation consumer → removes cached entry from Redis
3. Next read → cache miss → fresh data from DB → re-cached

---

### Q130. Redis Cluster vs Sentinel?

**Answer:**

| | Redis Sentinel | Redis Cluster |
|--|---|---|
| Purpose | **High availability** (failover) | **Horizontal scaling** (sharding + HA) |
| Data distribution | All data on ONE master | Data **sharded** across masters |
| Scaling | Vertical only | Horizontal (add nodes) |
| Failover | Monitor → detect failure → promote replica | Built-in (gossip protocol) |
| Storage | Limited by single node RAM | RAM of ALL nodes combined |

**GSTN:** For large-scale distributed caching with 14M+ taxpayers, Redis Cluster provides both sharding and high availability.

---

### Q131. Distributed locking with Redis (Redisson/RedLock)?

**Answer:**

**Scenario:** Prevent duplicate GST return processing when same return arrives from multiple queues.

```java
// Using Redisson distributed lock
RLock lock = redissonClient.getLock("return-lock:" + gstin + ":" + period);
try {
    if (lock.tryLock(10, 60, TimeUnit.SECONDS)) { // Wait 10s, lock for 60s
        try {
            // Check if already processed
            if (!isAlreadyProcessed(gstin, period)) {
                processReturn(gstin, period);
            }
        } finally {
            lock.unlock();
        }
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

**RedLock (multi-node):** Acquire lock on majority of Redis instances (N/2 + 1) → even if one Redis node fails, lock is still valid. Required for true distributed locking.

---

### Q132–Q135. Pub/Sub vs Kafka, Persistence, Cache Stampede, Pipelining

**Q132. Redis Pub/Sub vs Kafka:**
- Redis Pub/Sub: Fire-and-forget, no persistence, no replay, simple → notifications
- Kafka: Durable, replayable, consumer groups → event processing. GSTN uses Kafka for critical events.

**Q133. Redis persistence:**
- **RDB**: Point-in-time snapshots → fast recovery but data loss between snapshots
- **AOF**: Log every write → slower but minimal data loss
- **GSTN**: RDB + AOF combined for balance

**Q134. Cache stampede:**
When cache key expires → many concurrent requests all hit DB simultaneously.
Solutions: 
- **Locking**: First request fetches, others wait
- **Early expiry**: Refresh before TTL expires
- **Probabilistic early expiry**: Random chance to refresh before expiry

**Q135. Redis pipelining:**
Send multiple commands without waiting for individual responses → reduces network round trips. Lua scripting for atomic multi-step operations (e.g., check-and-set for rate limiting).


---

<!-- Auto-generated: 2026-03-27 12:06 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:07 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:09 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:18 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:22 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:28 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 12:42 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 13:07 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 13:10 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 19:27 | Source: generate_kafka_2026-03-27 -->

Q&A generated


---

<!-- Auto-generated: 2026-03-27 19:45 | Source: generate_kafka_2026-03-27 -->

Q&A generated
