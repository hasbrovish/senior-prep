# SYSTEM DESIGN (HLD) - ANSWER TEMPLATE & EVALUATION GUIDE

## 🎯 STRONG HIRE SIGNALS (What Interviewers Score)

| Signal | Strong Hire | Hire | No Hire |
|--------|-------------|------|---------|
| **Drives Discussion** | Leads independently | Good with guidance | Waits for prompts |
| **Requirements** | 5+ clarifying Qs | Some questions | Jumps to design |
| **Estimations** | Accurate (within 2x) | Reasonable | Off by 10x+ |
| **Design** | Scalable, complete | Works with gaps | Doesn't meet reqs |
| **Deep Dive** | Expert in 1+ areas | Good knowledge | Surface only |
| **Trade-offs** | Proactive discussion | When prompted | Doesn't recognize |
| **Production Exp** | References real work | Some experience | Textbook only |

---

## 📝 40-MINUTE FRAMEWORK (Follow Every Time)

### PHASE 1: REQUIREMENTS (5 minutes)

```
"Let me make sure I understand what we're building..."

FUNCTIONAL REQUIREMENTS:
□ "What are the core features?" (List 3-5)
□ "Who are the primary users?"
□ "What's the most critical user flow?"
□ "Any features explicitly OUT of scope?"

NON-FUNCTIONAL REQUIREMENTS:
□ "What's our expected scale? DAU/MAU?"
□ "Latency requirements? p99 < 200ms?"  
□ "Availability target? 99.9% = 8.7 hrs downtime/year"
□ "Consistency model? Strong or eventual?"
□ "Any regulatory requirements? GDPR, PCI?"

SAY: "Let me summarize the requirements before moving on:
- Core features: X, Y, Z
- Scale: N million users, M QPS
- Latency: < X ms, Availability: Y%"
```

### PHASE 2: ESTIMATIONS (5 minutes)

```
"Let me do some back-of-envelope calculations..."

TEMPLATE:
┌─────────────────────────────────────────────────┐
│ Users:                                           │
│   DAU = X million                               │
│   Actions/user/day = Y                          │
│                                                  │
│ Traffic:                                         │
│   QPS = (DAU × actions) / 86400                 │
│   Peak QPS = 3 × average QPS                    │
│   Read:Write ratio = typically 10:1             │
│                                                  │
│ Storage:                                         │
│   Per record = Z bytes                          │
│   Daily new records = DAU × actions             │
│   Storage/year = daily × 365 × record_size     │
│                                                  │
│ Bandwidth:                                       │
│   Bandwidth = QPS × payload_size                │
└─────────────────────────────────────────────────┘

EXAMPLE (Twitter-like):
- 500M DAU, 5 tweets read/user/day
- Read QPS = 500M × 5 / 86400 ≈ 30K QPS
- Peak = 90K QPS
- Tweet size = 280 chars + metadata ≈ 1KB
- Bandwidth = 30K × 1KB = 30 MB/s
```

### PHASE 3: HIGH-LEVEL DESIGN (10 minutes)

```
"Here's my high-level architecture..."

DRAW (in this order):
┌──────┐    ┌─────┐    ┌───────────┐    ┌──────────────┐
│Client│───►│ CDN │───►│Load       │───►│API Gateway   │
└──────┘    └─────┘    │Balancer   │    └──────────────┘
                       └───────────┘            │
                                                ▼
                       ┌────────────────────────────────┐
                       │        Service Layer           │
                       │  ┌─────┐ ┌─────┐ ┌─────┐     │
                       │  │Svc A│ │Svc B│ │Svc C│     │
                       │  └─────┘ └─────┘ └─────┘     │
                       └────────────────────────────────┘
                                    │
                       ┌────────────┼────────────┐
                       ▼            ▼            ▼
                   ┌───────┐   ┌───────┐   ┌───────────┐
                   │ Cache │   │  DB   │   │Msg Queue  │
                   │(Redis)│   │Primary│   │ (Kafka)   │
                   └───────┘   └───────┘   └───────────┘

API DESIGN:
- "POST /api/v1/[resource] - Create"
- "GET /api/v1/[resource]/{id} - Read"
- "PUT /api/v1/[resource]/{id} - Update"
- "DELETE /api/v1/[resource]/{id} - Delete"

SAY:
"I'm using REST for its simplicity. For internal service 
communication, we could use gRPC for better performance."
```

### PHASE 4: DEEP DIVE (15 minutes)

```
"Let me dive deeper into the key components..."

DATABASE:
□ Choice: "I'd use [PostgreSQL/MongoDB/Cassandra] because..."
  - SQL: ACID needed, complex queries, relationships
  - NoSQL: Scale, flexible schema, denormalized reads
□ Schema: Draw 2-3 main tables with key fields
□ Indexing: "Index on [field] for [query pattern]"
□ Sharding: "Shard by [user_id/timestamp] because..."

CACHING:
□ Strategy: "Cache-aside for read-heavy workloads"
□ What to cache: "Frequently accessed, rarely changed data"
□ TTL: "X minutes balances freshness vs hit rate"
□ Invalidation: "On write, invalidate cache key"

SCALING:
□ Horizontal: "Add more instances behind load balancer"
□ Database: "Read replicas for reads, primary for writes"
□ Caching: "Consistent hashing to distribute cache"

MESSAGE QUEUE:
□ When: "Async processing, decoupling services"
□ How: "Kafka for durability, partitioned by [key]"
□ Ordering: "Within partition, guaranteed order"
```

### PHASE 5: BOTTLENECKS & TRADE-OFFS (5 minutes)

```
"Let me address potential issues..."

SINGLE POINTS OF FAILURE:
□ "Database → Add replicas with automatic failover"
□ "Cache → Redis cluster with replication"
□ "Load Balancer → Multiple LBs with health checks"

TRADE-OFFS DISCUSSED:
□ "Consistency vs Availability: Choosing [X] because..."
□ "Latency vs Throughput: Optimizing for [X]"
□ "Cost vs Performance: [X] is cost-effective at our scale"

SCALING DISCUSSION:
□ "To handle 10× load: [specific changes]"
□ "To handle 100× load: [architectural changes]"

SAY:
"The main trade-off is [X] vs [Y]. Given our requirements 
for [Z], I'm choosing [X] because..."
```

---

## 🔥 STRONG HIRE PHRASES (Use These!)

### Requirements Phase:
- "Before I design, let me understand the scale..."
- "What's more critical: latency or throughput?"
- "Should I focus on read optimization or write optimization?"

### Estimation Phase:
- "Let me walk through the math..."
- "At this scale, we're looking at roughly..."
- "This tells me we need to optimize for..."

### Design Phase:
- "I'm adding this component because..."
- "The data flows like this..."
- "For high availability, I'd add..."

### Deep Dive Phase:
- "In my experience at GSTN, we handled similar scale by..."
- "The reason I chose [X] over [Y] is..."
- "One thing that could go wrong here is..."

### Trade-offs Phase:
- "The trade-off here is [X] vs [Y]. Given our constraints..."
- "This is similar to how [Netflix/Uber/Twitter] solves it"
- "If we needed to scale 100×, we'd need to..."

---

## ⚠️ RED FLAGS TO AVOID

| Red Flag | What to Do Instead |
|----------|---------------------|
| Jumping to design without requirements | "Let me first understand the scale..." |
| Not doing estimations | "Let me calculate the numbers..." |
| Only talking, not drawing | Always draw as you explain |
| Surface-level answers | Deep dive into at least one component |
| Not discussing trade-offs | "The trade-off here is..." |
| Getting defensive when challenged | "That's a good point. Let me reconsider..." |
| Generic textbook answers | "In my experience..." |

---

## 📊 SYSTEMS QUICK REFERENCE

| System | Key Components | Key Challenges |
|--------|----------------|----------------|
| **URL Shortener** | Counter/Hash, Cache, Analytics | Read-heavy, Collision |
| **Rate Limiter** | Token bucket, Redis INCR | Distributed counting |
| **Chat** | WebSocket, Message store, Presence | Ordering, Delivery |
| **News Feed** | Fan-out, Timeline cache, Ranking | Celebrity problem |
| **Video** | CDN, Transcoding, Chunking | Bandwidth, Storage |
| **Search** | Inverted index, Trie, Ranking | Relevance, Speed |
| **Ride Share** | Geospatial index, Matching | Real-time, ETA |
| **Payments** | Ledger, Idempotency, Reconcile | ACID, Fraud |

---

## 📝 ESTIMATION CHEAT SHEET

```
TIME CONVERSIONS:
- 1 day = 86,400 seconds ≈ 100K seconds
- 1 month ≈ 2.5M seconds
- 1 year ≈ 30M seconds

DATA SIZES:
- 1 char = 1-2 bytes (UTF-8)
- 1 int = 4-8 bytes
- 1 UUID = 16 bytes
- 1 timestamp = 8 bytes
- Average tweet = 1 KB
- Average image = 200 KB
- Average video = 50 MB/min

SCALE REFERENCES:
- 1M QPS = Very large (Google scale)
- 100K QPS = Large (Netflix, Twitter)
- 10K QPS = Medium-large
- 1K QPS = Medium
- 100 QPS = Small-medium

LATENCY TARGETS:
- User-facing API: < 200ms p99
- Internal API: < 50ms p99
- Database query: < 10ms
- Cache hit: < 1ms
```

---

## 📝 SELF-ASSESSMENT CHECKLIST

After each practice session:

```
□ Did I gather all requirements before designing?
□ Did I do back-of-envelope calculations?
□ Did I draw a clear high-level diagram?
□ Did I design proper APIs?
□ Did I deep dive into at least one component?
□ Did I discuss database choice with reasoning?
□ Did I cover caching strategy?
□ Did I identify bottlenecks/SPOFs?
□ Did I discuss trade-offs proactively?
□ Did I connect to my real experience?
```

**Score: ___/10**

- 9-10: Strong Hire level
- 7-8: Hire level
- 5-6: Lean Hire
- 0-4: Need more practice
