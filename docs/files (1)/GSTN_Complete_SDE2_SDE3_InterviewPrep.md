# GSTN Complete SDE-2/SDE-3 Interview Prep

## Mock Round 1: Java + Spring (45 min)

### Q: Explain your most complex Spring Boot service.
Filing Service: 200+ beans, constructor injection throughout, @Transactional with REQUIRES_NEW for audit, custom health indicators for K8s probes, Redis-backed rate limiting per GSTIN, Kafka producer for async validation pipeline. Handles 33K peak QPS.

### Q: Walk me through a production incident you debugged.
Memory leak story: OOM after 3 days → GC logging → heap dump → Eclipse MAT → ConcurrentHashMap session cache with dead cleanup task → replaced with Caffeine → added heap alerts. 22-minute resolution, zero data loss.

### Q: How do you handle database migrations in production?
Flyway for schema versioning. Always backward-compatible migrations (add columns with defaults, never drop in same release). Blue-green deployment: new code handles both old and new schema. Migration runs during deployment. Rollback: new code also handles old schema.

## Mock Round 2: System Design (45 min)

### Design GSTN Filing System
See GSTN_Architecture_Reference.md for full architecture. Key talking points:
1. Traffic spike handling (10x during deadlines)
2. Kafka for async processing (zero data loss)
3. Two-layer caching (Caffeine L1 + Redis L2)
4. Rate limiting (Redis sliding window per GSTIN)
5. Circuit breaker for cascading failure prevention

## Mock Round 3: Behavioral (30 min)

### "Tell me about a time you disagreed with a technical decision."
Kafka migration story. Team lead preferred adding retry logic to existing REST calls. I built data-driven case showing 73% of failures were timeout-related, not transient. Proposed incremental migration (dual-write) to reduce risk. Team lead agreed after seeing the data. Result: cascading failures eliminated.

### "Tell me about your biggest failure."
Early in GSTN, I deployed a config change without testing in staging. It changed the Kafka consumer group ID, causing all consumers to re-read from offset 0. Duplicate processing of 2 days of filings. Fixed within hours, but learned: every config change is a code change. Now in our deployment checklist.

## Code Walkthrough Preparation

### Your DistCacheUtil (Caching Layer)
- Two-tier: check local Caffeine → check Redis → fetch from DB → populate both
- TTL strategy: local (5min), Redis (varies by data type)
- Cache invalidation via Kafka events for tax rule changes

### Your Kafka Consumer with DLQ
- At-least-once delivery with idempotent consumer (event_id check)
- 3 retries with exponential backoff (1s, 5s, 30s)
- DLQ topic for permanent failures
- Monitoring: consumer lag alerts, DLQ message count alerts

### Your XA Transaction (Atomikos JTA)
- Distributed transaction across Appeal + Ledger + Notification DBs
- 2-phase commit coordinated by Atomikos
- Trade-off: correctness over performance
- When to use XA vs Saga: XA for strong consistency needs (financial data)
