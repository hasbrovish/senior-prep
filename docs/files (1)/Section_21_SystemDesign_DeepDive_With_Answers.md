# Section 21 — System Design Deep Dive with Full Answers

## Design 1: Tax Filing System (GSTN — Your Strongest Asset)

### Requirements
- 14M taxpayers, 100K concurrent during deadline spikes (10x normal)
- Monthly/quarterly filing: form → validation → digital signature → acknowledgment
- Strong consistency for tax data, audit trail for compliance
- p99 latency < 500ms for submission, < 200ms for status check

### Estimation
- Peak QPS: 100K concurrent × 1 req/3s = ~33K QPS
- Storage: 14M × 12 filings × 50KB = ~8.4 TB/year
- Read:Write: Filing season 1:1, off-season 10:1

### Architecture
```
[Web/Mobile] → [CDN + WAF] → [API Gateway (rate limiting, auth)]
  → [Filing Service] → [Kafka] → [Validation Service]
                                → [Notification Service]
                                → [Audit Service]

[Filing Service] → [MySQL primary + 2 read replicas] + [Redis Cluster (cache)]
[HBase cluster] → 300Cr+ invoice matching
[ELK] ← all services (structured JSON logs with traceId)
[Prometheus/Grafana] ← metrics from all services
```

### Deep Dive: Traffic Spike Handling
1. **Rate limiting** — Redis token bucket per GSTIN. Prevents abuse, protects downstream.
2. **Async processing** — Filing → Kafka immediately. User gets acknowledgment. Validation async.
3. **K8s HPA** — Scales filing pods 10→50 on CPU + custom Kafka lag metrics.
4. **Cache warming** — Tax rules + GSTIN master data pre-loaded before deadline.
5. **Read replicas** — Status checks routed to replicas.
6. **Circuit breaker** — If validation overwhelmed, filings queue in Kafka. Zero data loss.

### Key Tradeoff: Sync vs Async Filing
Async (Kafka) for resilience. Tradeoff: user doesn't see validation errors immediately. Mitigation: client-side pre-validation catches 80% of errors.

---

## Design 2: Rate Limiter

### Algorithms
- **Token Bucket:** Smooth, allows bursts. Refill rate + bucket size. Best for API rate limiting.
- **Sliding Window Counter:** Weighted average of current + previous window. Good accuracy, low memory.
- **Fixed Window:** Simple but allows 2x burst at window edges.

### GSTN Implementation: Redis Sliding Window
```
MULTI
  INCR rate_limit:{gstin}:{current_window}
  EXPIRE rate_limit:{gstin}:{current_window} 60
  GET rate_limit:{gstin}:{previous_window}
EXEC
weighted_count = prev_count × overlap_ratio + current_count
```
Redis failure fallback: local Guava RateLimiter. Not distributed but better than nothing.

---

## Design 3: URL Shortener
- Short code: Base62 of Snowflake ID (non-sequential, distributed, no collisions)
- Write: MySQL. Read: Redis cache (Zipfian — 90% traffic to 10% URLs)
- 301 (browser caches, fewer hits) vs 302 (every click tracked)

---

## Design 4: Chat/Messaging System
- WebSocket for real-time delivery
- Kafka for message persistence and offline delivery
- Redis pub/sub for presence (online/offline)
- Fan-out on write (small groups) vs fan-out on read (large channels)
- Delivered/Read receipts via separate Kafka topic

---

## Design 5: Notification System (Built This at GSTN)
- Multi-channel: SMS, Email, Push, In-app
- Priority Kafka topics: critical (OTP, filing ack), standard (reminders), bulk (promotional)
- Template engine with multilingual support (Hindi, English, regional)
- Idempotency: dedup_key = {user_id}:{event_type}:{event_id} checked in Redis
- DLQ after 3 retries with exponential backoff
- Backpressure: Kafka consumer pause when SMS gateway is slow

---

## Design 6: Distributed Cache
- L1: Caffeine (per-pod, 10K entries, 5min TTL)
- L2: Redis Cluster (6 nodes, shared across pods)
- Cache-aside pattern (default), write-through for critical paths
- Invalidation: TTL for most data, Kafka events for tax rule changes
- Thundering herd: SETNX distributed lock + stale-while-revalidate

---

## Design 7: Search System (Elasticsearch)
- Inverted index: term → list of document IDs
- Tokenizer + analyzer pipeline for text processing
- GSTN: Full-text search on filing descriptions, taxpayer names
- Sharding by GSTIN hash, replication factor 2
- Near real-time: index refresh every 1s (configurable)

---

## Design 8: Payment System (For Stripe-type interviews)
- Idempotency keys: client generates unique key per payment attempt
- State machine: PENDING → PROCESSING → SUCCEEDED/FAILED
- Distributed transactions: Saga pattern (not XA — too slow for payments)
- PCI compliance: tokenize card data, separate secure vault, never log PAN
- Reconciliation: Daily batch matching between internal ledger and payment processor
- Webhook delivery: at-least-once with exponential retry + signature verification

---

## Numbers Every SDE Should Know

| Operation | Latency |
|-----------|---------|
| L1 cache | 0.5 ns |
| L2 cache | 7 ns |
| RAM | 100 ns |
| SSD random read | 150 μs |
| Redis GET | 0.1-0.5 ms |
| MySQL simple query | 1-10 ms |
| Kafka produce (acks=1) | 2-5 ms |
| Same datacenter RTT | 500 μs |
| Cross-continent RTT | 150 ms |

---

## System Design Framework (SDE-3 Level)
1. **Requirements** (3-5 min): Functional + non-functional + constraints
2. **Estimation** (3 min): QPS, storage, bandwidth
3. **High-level design** (10 min): Components, data flow, API, schema
4. **Deep dive** (15-20 min): Pick 2-3 components, tradeoffs, failure modes
5. **Wrap-up** (3 min): Bottlenecks, monitoring, future evolution
