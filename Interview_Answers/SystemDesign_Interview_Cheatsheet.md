# System Design Interview — Master Cheatsheet
# Sources: Ashish PS (algomaster.io) + Hello Interview + Google Doc Template + Real Interview Data
# Jayanti Vishnoi | Used for: Apple, Oracle, Amazon, DoorDash prep

---

## THE 45-MINUTE INTERVIEW MAP

```
Phase 1 — Requirements       [5 min]
Phase 2 — Core Entities      [2 min]
Phase 3 — API Design         [5 min]
Phase 4 — Capacity Est.      [3 min]  ← skip if interviewer says so
Phase 5 — High-Level Design  [10-15 min]
Phase 6 — Deep Dives         [10 min]
Phase 7 — Verify & Wrap      [5 min]
```

**#1 Mistake**: Jumping to architecture before clarifying requirements.
**#1 Win**: Grounding your design in real math (RPS, storage, latency).

---

## PHASE 1 — REQUIREMENTS (5 min)

### Functional Requirements
Ask EXACTLY 3 things (not 10 — show discipline):
- "What are the 3 core things users should be able to do?"
- "Who are the users — consumers, businesses, internal services?"
- "Any external integrations or third-party dependencies?"

**Write on whiteboard/doc:** "Users should be able to..."
1. [Primary action]
2. [Secondary action]
3. [Read/view action]

### Non-Functional Requirements
Pick 3–5 that actually matter for this system:
- **Availability**: "Does this need 99.9% or 99.99%? Can we tolerate brief downtime?"
- **Consistency**: "Is eventual consistency OK, or must reads always reflect latest write?"
- **Latency**: "What's the acceptable p99 latency?" → Always quantify: "<200ms for search"
- **Scale**: "How many users? What's peak QPS?"
- **Durability**: "Can we lose any data, or must everything be persisted?"

### Real Examples from Your Interviews
| Problem | FR | NFR |
|---------|-----|-----|
| Apple Music | Stream songs, create playlists, search | Low latency streaming, 99.99% availability |
| URL Shortener | Shorten URL, redirect, analytics | <10ms redirect, 100:1 read/write ratio |
| Distributed Cache | Get/Set key-value, TTL, eviction | Sub-ms latency, consistency across nodes |
| Portfolio Platform | View broker accounts, see positions | Near real-time data, strong consistency for trades |
| Event Tracking System | Submit events, define processing logic, SLA monitoring | High throughput, reliable delivery, SLA guarantees |

---

## PHASE 2 — CORE ENTITIES (2 min)

List 4–6 primary objects. This builds shared vocabulary.

**Template:** "The core entities in my system are: [User], [X], [Y], [Z]"

Examples:
- URL Shortener: `User`, `URL`, `Click` (analytics)
- Apple Music: `User`, `Song`, `Album`, `Playlist`, `Stream`
- Distributed Cache: `CacheNode`, `KeyValueEntry`, `ConsistentHashRing`
- Event Tracking: `Service`, `Event`, `ProcessingRule`, `SLADefinition`, `Alert`

---

## PHASE 3 — API DESIGN (5 min)

Default to REST. Use plural resource names. User from auth token, never request body.

**Template per endpoint:**
```
POST   /resource          → Create
GET    /resource/{id}     → Read one
GET    /resources?params  → List/search
PUT    /resource/{id}     → Update
DELETE /resource/{id}     → Delete
```

**For streaming/real-time**: Mention WebSocket or SSE here.
**For inter-service**: Mention gRPC or async Kafka event.

---

## PHASE 4 — CAPACITY ESTIMATION (3 min)

Only calculate when it drives a design decision (e.g., "do I need sharding?").

### The Numbers You Must Memorize

```
TIME
1 day  = 86,400 sec ≈ 100K sec
1 year = 31.5M sec ≈ 30M sec

STORAGE
1 char  = 1 byte
1 int   = 4 bytes
1 long  = 8 bytes
1 UUID  = 16 bytes
1 image = 200KB–5MB
1 video (1080p, 1 hr) = ~2GB

LATENCY (L1 Cache → Disk)
L1 cache:       0.5 ns
RAM:            100 ns
SSD:            100 µs
HDD:            10 ms
Network (same datacenter): 0.5 ms
Network (cross-region):    150 ms
```

### The 3-Step Estimation Formula
```
1. Users → DAU
   Example: 100M users, 10% DAU = 10M DAU

2. DAU → QPS
   Example: 10M DAU × 5 actions/day ÷ 100K sec = 500 QPS
   Peak = 500 × 3 = 1,500 QPS (use 3x for peak)

3. QPS → Storage/Bandwidth
   Example: 500 writes/sec × 1KB/write = 500KB/sec write throughput
   Per day: 500KB × 86,400 = ~43GB/day
   Per year: 43GB × 365 = ~15TB/year
```

### Real Estimates from Your Interviews

**Apple Music Streaming (Bitrate Discussion)**
```
Songs: 10M songs × 5MB avg = 50TB storage for audio
Streams: 10M DAU × 2 streams/day × 3 min × 128kbps = ~5GB/s bandwidth
CDN is mandatory — you cannot serve 5GB/s from one datacenter
```

**Distributed Cache (Oracle Interview)**
```
10M keys × 1KB avg value = 10GB data
Single Redis node handles ~100K ops/sec → need cluster for 500K QPS
Consistent hashing to distribute across N nodes
```

**URL Shortener**
```
100:1 read/write ratio
1M writes/day = ~12 writes/sec
100M reads/day = ~1,200 reads/sec
URL entry: ~500 bytes × 1M/day × 365 days × 5 years = ~1TB
```

---

## PHASE 5 — HIGH-LEVEL DESIGN (10–15 min)

Build incrementally through your API endpoints. One endpoint → one flow.

### Standard Component Toolkit

```
CLIENT
  ↓
CDN (for static assets, video/audio chunks)
  ↓
API GATEWAY (auth, rate limiting, routing)
  ↓
LOAD BALANCER
  ↓
APPLICATION SERVERS (stateless, horizontally scalable)
  ↓
CACHE (Redis) ← check here before DB
  ↓
DATABASE (SQL or NoSQL — justify your choice)
  ↓
MESSAGE QUEUE (Kafka) ← for async, heavy workloads
  ↓
BACKGROUND WORKERS
```

### SQL vs NoSQL Decision Tree
```
Use SQL (PostgreSQL/MySQL) when:
  - ACID transactions needed (payments, ledger, orders)
  - Complex joins and relationships
  - Data is structured and schema is stable
  - Examples: user accounts, financial transactions, order management

Use NoSQL when:
  - Massive scale, flexible schema
  - Key-value lookups (Redis, DynamoDB)
  - Time-series data (Cassandra)
  - Document storage (MongoDB for catalogs, configs)
  - Full-text search (Elasticsearch)
```

### Caching Strategy — When to Use What
```
Cache-aside (Lazy loading):
  → App checks cache → miss → load from DB → populate cache
  → Best for: read-heavy, data can be slightly stale
  → Your GSTN DistCacheUtil uses this

Write-through:
  → Write to cache AND DB simultaneously
  → Best for: financial data, where stale reads are unacceptable
  → Latency: slightly higher writes, but consistent reads

Write-behind (Write-back):
  → Write to cache only → async flush to DB
  → Best for: high-write workloads where DB can be slightly behind
  → Risk: data loss if cache fails before flush

Read-through:
  → Cache sits in front of DB, handles its own population
  → Best for: managed cache services (ElastiCache)

Refresh-ahead:
  → Proactively refresh cache before TTL expires
  → Best for: predictable access patterns
```

---

## PHASE 6 — DEEP DIVES (10 min)

Senior candidates proactively lead these. Junior candidates respond to probes.

### Distributed Caching Deep Dive (Oracle asked this)
```
Consistent Hashing:
  - Hash both nodes and keys to same ring (0 to 2^32)
  - Key goes to first node clockwise
  - Adding/removing node: only K/N keys remapped (K=keys, N=nodes)
  - Virtual nodes: each physical node = 100-200 virtual positions on ring
  - Prevents hotspots from uneven key distribution

Replication (Quorum):
  - N = total replicas (typically 3)
  - W = write quorum (2) — must confirm before success
  - R = read quorum (2) — must agree before returning
  - W + R > N → strong consistency (reads always see latest write)
  - W=1, R=1 → eventual consistency, better availability

Bloom Filter:
  - Probabilistic data structure — "definitely not in cache" or "probably in cache"
  - Used to avoid DB lookups for keys that definitely don't exist
  - False positives possible, false negatives impossible
  - Use case: prevent cache penetration attacks

Eviction Policies:
  - LRU (Least Recently Used): evict the least recently accessed
  - LFU (Least Frequently Used): evict the least accessed over time
  - TTL-based: expire after fixed time regardless of access
  - Your GSTN work: EhCache uses LRU + TTL combination
```

### Database Scaling Deep Dive
```
Read Replicas:
  - Master handles writes, replicas handle reads
  - Replica lag is the key trade-off (eventual consistency)
  - CQRS naturally maps here: command → master, query → replica
  - Your GSTN GSTR-2A optimization used this pattern

Sharding (Horizontal Partitioning):
  - Split data across multiple DB instances by shard key
  - Range-based: shard by date range, user ID range
  - Hash-based: hash(user_id) % N → uniform distribution
  - Directory-based: lookup service maps key to shard
  - Trade-off: cross-shard queries become complex (avoid joins across shards)

Vertical Partitioning:
  - Split table by columns (hot columns in fast storage)
  - Example: user profile vs user activity — different access patterns
```

### Message Queue Deep Dive (Kafka — your strength)
```
When to use Kafka vs direct API call:
  - Use Kafka: async processing, spiky traffic, multiple consumers, audit trail
  - Use direct: synchronous, user waits for result, simple flow

Kafka guarantees:
  - At-least-once: acks=all + manual offset commit (your DLQ framework)
  - Exactly-once: transactional producer + idempotent consumer
  - At-most-once: acks=0 (fire and forget — never for financial data)

Partition strategy:
  - Key-based: same key always same partition → ordering guarantee
  - Round-robin: even distribution, no ordering
  - Your GSTN learning: large taxpayer GSTN-ID based partitioning
```

---

## PHASE 7 — VERIFY & WRAP (5 min)

Go back to your non-functional requirements and verify:
```
"Let me verify we meet our requirements:
- Availability: We have load balancer + DB replication → can survive single node failure
- Latency: Cache layer gives us sub-10ms for reads, CDN for static assets
- Scale: Stateless app servers + consistent hash cache scales horizontally
- Consistency: [explain your choice based on system requirements]"
```

---

## SYSTEM DESIGN PROBLEM BANK (From Your Real Interviews)

### 1. Apple Music Streaming App
**Key insight**: Bitrate discussion means they want you to talk about adaptive streaming.
```
- Audio stored in S3/blob storage, chunked in 30s segments
- CDN distributes chunks globally (latency is critical for audio)
- Adaptive bitrate: 128kbps (mobile), 256kbps (wifi), 320kbps (premium)
- Metadata (song, artist, album) in PostgreSQL
- User playlists + listen history in Cassandra (write-heavy, time-series)
- Search: Elasticsearch for song/artist/album search
- Real-time: WebSocket or SSE for "now playing" sync across devices
```

### 2. URL Shortener
```
- Generate short code: Base62 encoding of auto-increment ID (7 chars = 62^7 = 3.5 trillion URLs)
- DB: Store {short_code → original_url, created_at, user_id, expiry}
- Cache (Redis): short_code → url (100:1 read/write ratio → cache everything)
- Redirect: 301 (permanent, browser caches) vs 302 (temporary, every request hits your servers)
- Analytics: Async Kafka event on every click → Flink/Spark aggregate
```

### 3. Distributed Key-Value Cache (Oracle)
```
Consistent hashing ring for sharding across nodes
Replication factor = 3, Quorum W=2, R=2
Bloom filter at each node to avoid DB fallback for missing keys
Eviction: LRU + TTL
Failure detection: Gossip protocol between nodes
Recovery: Hinted handoff → anti-entropy repair
Ref: Alex Xu Book 1, Chapter 6
```

### 4. Amazon Order Management System
```
Entities: Order, OrderItem, Product, Payment, Shipment, User
DB: PostgreSQL (ACID for order/payment), DynamoDB (catalog)
Event-driven: OrderPlaced → PaymentService → InventoryService → ShipmentService
Saga pattern (Choreography): each service publishes events, compensating transactions on failure
State machine: PENDING → CONFIRMED → PAID → SHIPPED → DELIVERED → CANCELLED
Idempotency: idempotency key on all payment APIs
```

### 5. Distributed Event Tracking System (DoorDash)
```
- Clients POST events to API Gateway → Kafka topic per event type
- Processing logic: Plugin architecture (Strategy pattern) per event type — each team owns their processor
- SLA: Kafka consumer with lag monitoring → alert if processing > SLA threshold
- Storage: Raw events in S3 (cheap, long-term), aggregated metrics in TimescaleDB
- Monitoring integration: Prometheus metrics from consumer lag → Grafana → PagerDuty
- Dead letter queue: Failed events → DLQ topic → manual reprocess
```

### 6. Multi-Broker Portfolio Platform (Amazon)
```
- Connect to multiple broker APIs (Zerodha, Groww, HDFC Securities)
- Aggregate positions across accounts in one view
- Entities: User, BrokerAccount, Position, Transaction, Portfolio
- DB: PostgreSQL for accounts/positions (consistency required)
- Broker data sync: Background jobs polling broker APIs (rate limited)
  OR webhooks from brokers (preferred)
- Cache: Redis for portfolio summary (refreshed every 30s)
- Schema: positions table with (user_id, broker_id, symbol, quantity, avg_price, current_price)
- JSON API response: aggregated across brokers
```

---

## QUICK REFERENCE — COMMON DESIGN DECISIONS

| Requirement | Choose |
|-------------|--------|
| <10ms latency for reads | Redis cache |
| 100:1 read/write ratio | Cache-aside + CDN |
| Ordered messages | Kafka with key-based partitioning |
| Exactly-once processing | Kafka transactions + idempotent consumer |
| ACID transactions | PostgreSQL/MySQL |
| Flexible schema, massive scale | Cassandra/DynamoDB |
| Full-text search | Elasticsearch |
| Binary data (images, video, audio) | S3 + CDN |
| Rate limiting | Token bucket (Redis) or API Gateway |
| Real-time updates | WebSocket / SSE / Kafka → Server push |
| Cross-service transactions | Saga pattern (not XA) |
| Distribute cache across nodes | Consistent hashing |
| Prevent DB overload on missing keys | Bloom filter |
| Multiple consumers of same event | Kafka consumer groups |
| Large file chunking | S3 multipart upload |
| Global low latency | CDN + multi-region deployment |

---

## RESOURCES (From Interview_exp.txt)

| Resource | Link | Use for |
|----------|------|---------|
| Ashish PS Framework | algomaster.io (7-step guide) | Interview structure |
| Hello Interview | hellointerview.com/learn/system-design | Deep dives + 25 worked problems |
| Alex Xu Book 1 | Drive (need your login) | Foundation — chapters 4-12 |
| Alex Xu Book 2 | Drive (need your login) | Advanced — chapters 1-13 |
| DDIA | Kleppmann PDF | Depth on replication, partitioning, consistency |
| HLD Playlist | Shrayansh Jain YouTube | Video walkthroughs |
| LLD Playlist | Shrayansh Jain YouTube | Low-level design practice |

### Alex Xu Book 1 — Priority Chapters (based on your real interviews)
- Ch 4: Design a Rate Limiter → token bucket, leaky bucket
- Ch 5: Design Consistent Hashing → Oracle asked this directly
- Ch 6: Design Key-Value Store → Oracle Round 3
- Ch 7: Design Unique ID Generator → URL shortener variant
- Ch 8: Design URL Shortener → Apple/Amazon common ask
- Ch 11: Design a News Feed → push vs pull model
- Ch 12: Design a Chat System → WebSocket, presence

### Alex Xu Book 2 — Priority Chapters
- Ch 1: Proximity Service → Uber/DoorDash location problems
- Ch 2: Nearby Friends → Real-time location
- Ch 5: Metrics Monitoring → DoorDash event tracking system
- Ch 7: Hotel Reservation System → inventory + booking patterns
- Ch 9: S3-Like Object Storage → Apple Music audio storage
