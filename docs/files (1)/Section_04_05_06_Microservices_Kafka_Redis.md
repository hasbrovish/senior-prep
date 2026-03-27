# Section 04/05/06 — Microservices, Kafka, Redis (Q91–Q135)

## Q91: Explain microservices architecture patterns.

**Answer:** Microservices decompose a system into independently deployable services, each owning its data.

**Patterns we use at GSTN:**
- **API Gateway:** Single entry point. Rate limiting, auth, routing. Our gateway handles 100K concurrent, routes to filing/validation/notification services.
- **Service Discovery:** Kubernetes DNS-based. Each service registered automatically.
- **Circuit Breaker:** Resilience4j. If validation service errors exceed 50% in 30s window → open circuit → return cached/default response → half-open after 60s → test with single request.
- **Saga Pattern:** Long-running transactions across services. Filing saga: submit → validate → sign → acknowledge. Compensating transactions on failure (e.g., rollback filing status if signature fails).
- **CQRS:** Separate read/write models. Filing writes go to MySQL, read-optimized views in Redis/Elasticsearch.
- **Event Sourcing:** Audit log stores every state change as immutable event. Can reconstruct any filing's state at any point in time. 7-year retention (tax compliance).

### Follow-up: How do you handle distributed transactions without XA?
Saga pattern with Kafka. Each step publishes success/failure event. Next step listens and proceeds or compensates. Example: FilingSubmitted → ValidationService validates → FilingValidated/FilingRejected → NotificationService sends confirmation. If validation fails, compensating action reverts filing status. Eventual consistency, not strong consistency — acceptable for our use case.

---

## Q100: Explain Apache Kafka architecture.

**Answer:**
- **Broker:** Kafka server. GSTN runs 5-broker cluster.
- **Topic:** Named stream of records. We have: `filing-events`, `notification-triggers`, `audit-log`.
- **Partition:** Ordered, immutable sequence within a topic. Parallelism unit. We partition `filing-events` by GSTIN hash → guarantees per-taxpayer ordering.
- **Consumer Group:** Set of consumers sharing topic partitions. Each partition consumed by exactly one consumer in the group. Adding consumers = horizontal scaling (up to partition count).
- **Offset:** Position in partition. Consumer commits offset after processing. If consumer dies, new consumer resumes from last committed offset.
- **Replication:** Each partition replicated to N brokers (replication factor). One leader handles reads/writes; followers replicate. Leader dies → follower promoted. GSTN uses replication factor 3.

### Follow-up: Explain exactly-once semantics in Kafka.
Three levels:
1. **At-most-once:** Commit offset before processing. If consumer crashes mid-processing, message lost.
2. **At-least-once:** Process then commit. If crash after processing but before commit, message reprocessed. GSTN default — combined with idempotent consumers.
3. **Exactly-once:** Kafka transactions. Producer: `enable.idempotence=true` + `transactional.id`. Consumer: read-process-write in same transaction. Complex, performance overhead.

We use at-least-once + idempotent consumers (check event_id in processed_events table before processing). Simpler, nearly equivalent to exactly-once.

### Follow-up: How do you handle consumer lag?
Monitor via Kafka consumer lag metric (current offset vs log-end offset). Alert if lag exceeds threshold (e.g., >10K messages for filing-events). Remediation: scale consumer instances (K8s HPA triggered by custom Kafka lag metric), increase partition count for long-term, check for slow consumers (DB bottleneck, expensive processing).

---

## Q105: Explain DLQ (Dead Letter Queue) pattern.

**Answer:** Messages that fail processing after N retries are moved to a DLQ topic instead of blocking the consumer.

**GSTN implementation:**
```
filing-events (main topic)
  → Consumer processes
  → Failure? Retry 3 times with exponential backoff (1s, 5s, 30s)
  → Still fails? Publish to filing-events-dlq
  → DLQ consumer: logs, alerts SRE, stores in investigation dashboard
  → Manual investigation → fix → replay from DLQ
```

**Key design:** DLQ messages include original headers + error details (exception class, message, stack trace, retry count). Our investigation dashboard shows DLQ messages grouped by error type — most common pattern was serialization errors from schema evolution.

---

## Q110: Redis data structures and use cases.

**Answer:**
- **String:** Simple key-value. Session tokens, feature flags. `SET session:gstin123 "{...}" EX 1800`.
- **Hash:** Object with fields. Taxpayer profile cache. `HSET taxpayer:gstin123 name "Jayanti" status "Active"`.
- **List:** Ordered collection. Recent filing activity feed.
- **Set:** Unique values. Tracking unique GSTINs that filed today.
- **Sorted Set:** Set with scores. Leaderboard of most active filers. Rate limiting sliding window.
- **HyperLogLog:** Approximate cardinality. Counting unique daily visitors (~0.81% error, 12KB memory regardless of cardinality).

**GSTN Redis architecture:**
- 6-node cluster (3 masters, 3 replicas)
- Primary uses: session cache (15min TTL), filing status cache (5min TTL), rate limiting (sliding window per GSTIN), distributed locks (Redisson)
- Cache-aside pattern: read from Redis → miss → read MySQL → populate Redis
- Failure mode: Redis down → fall back to MySQL directly. Slower but functional.

### Follow-up: Redis persistence — RDB vs AOF?
- **RDB:** Point-in-time snapshots. Fast recovery, but lose data between snapshots. Good for cache (data loss = acceptable).
- **AOF:** Append every write command. Near-zero data loss (fsync every second). Slower recovery (replay entire log).
- **Hybrid (Redis 4+):** RDB snapshot + AOF since last snapshot. Best of both.
GSTN: AOF with fsync every second for rate limiting data. RDB for cache (loss is acceptable — cache warms up from MySQL).

### Follow-up: How do you prevent cache stampede?
When a popular key expires, 100 threads simultaneously hit the DB. Solutions:
1. **Mutex/lock:** First thread acquires distributed lock (SETNX), fetches from DB, populates cache. Others wait.
2. **Stale-while-revalidate:** Return stale value while one thread refreshes. We use this at GSTN.
3. **Pre-refresh:** Background thread refreshes cache before TTL expires.
4. **Randomized TTL:** Jitter prevents synchronized expiration.

---

## Q120: Explain the CAP theorem and how it applies to your systems.

**Answer:** A distributed system can guarantee at most 2 of 3: Consistency, Availability, Partition tolerance. Since network partitions are inevitable, the real choice is CP vs AP.

- **CP (Consistency + Partition tolerance):** During partition, refuse requests rather than return stale data. ZooKeeper, HBase. GSTN's ledger is CP — wrong tax data is worse than temporary unavailability.
- **AP (Availability + Partition tolerance):** During partition, return possibly stale data. Cassandra, DynamoDB. GSTN's filing status cache is AP — showing status from 5 minutes ago is acceptable.

**In practice:** We use different consistency levels for different data:
- Filing amounts, tax calculations: Strong consistency (MySQL with synchronous replication)
- Filing status display: Eventual consistency (Redis cache, 5min TTL)
- Notification delivery: At-least-once (Kafka with retry)
- Audit trail: Append-only, eventually consistent (Kafka → MySQL batch insert)
