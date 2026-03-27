# System Design — Consumer Product Designs (FAANG Level)
# Twitter Feed · Google Drive · WhatsApp · Uber
# For: Jayanti Vishnoi | 5.5 YOE GSTN | Targeting Flipkart, Amazon, Swiggy, Stripe, Google

---

## HOW TO USE THIS FILE
Each design follows the exact same 45-min framework:
1. Clarify (5 min) → 2. Estimate (5 min) → 3. HLD (10 min) → 4. Deep Dive (20 min) → 5. Trade-offs (5 min)

Map every answer to your GSTN experience. "I've built something similar..." is gold.

---

# ═══════════════════════════════════════════════════════════
# DESIGN 1: Twitter / Instagram — News Feed System
# ═══════════════════════════════════════════════════════════

## Step 1: Clarify Requirements

### Functional
1. User posts a tweet (text, images, links)
2. User follows/unfollows other users
3. User sees a feed of tweets from people they follow (sorted by recency or ranking)
4. Like, retweet, reply on tweets
5. Search tweets by keyword/hashtag

### Non-Functional
- **Availability**: 99.99% (people expect feed to always load)
- **Eventual consistency**: slight delay in feed is OK
- **Latency**: Feed load < 200ms for P99
- **Scale**: 300M DAU, 500M tweets/day, 28K writes/sec, 280K reads/sec (read-heavy 10:1)

---

## Step 2: Scale Estimation

```
Users:           300M DAU, 1.5B total
Tweets/day:      500M → ~5800/sec avg, 28K/sec peak
Feed reads:      300M users × ~5 feed views/day = 1.5B reads/day → 17K/sec
Storage:
  - Text tweet: 280 chars = 280 bytes
  - 500M tweets × 280 bytes = 140 GB/day (text only)
  - With images (avg 20% have images, avg 500KB): 50B × 500KB = ~50 TB/day
  - 5-year retention: ~90 PB
Fan-out:
  - Average user has 200 followers
  - 1 tweet → 200 fan-out writes
  - 28K writes/sec × 200 = 5.6M fan-out operations/sec at peak
  - Celebrity problem: Lady Gaga has 100M followers → 1 tweet = 100M writes (can't do sync)
```

---

## Step 3: High-Level Architecture

```
       ┌──────────────┐
       │   Client     │
       └──────┬───────┘
              │
       ┌──────▼───────┐     ┌─────────────┐
       │  API Gateway │────▶│ Auth Service│
       └──────┬───────┘     └─────────────┘
              │
    ┌─────────┼──────────┬──────────────┐
    │         │          │              │
┌───▼───┐ ┌──▼────┐ ┌───▼────┐ ┌──────▼──────┐
│ Tweet │ │ Feed  │ │ Social │ │   Search    │
│Service│ │Service│ │Service │ │   Service   │
└───┬───┘ └──┬────┘ └───┬────┘ └─────────────┘
    │        │          │
    │   ┌────▼────┐     │      ┌─────────────┐
    │   │Timeline │     │      │ Notification│
    │   │  Cache  │     │      │   Service   │
    │   │ (Redis) │     │      └─────────────┘
    │   └─────────┘     │
    │                   │
┌───▼──────────┐ ┌──────▼──────┐
│  Tweet Store │ │ Social Graph│
│  (Cassandra) │ │  (MySQL +   │
└──────────────┘ │   Neo4j)    │
                 └─────────────┘
    ┌────────────────────┐
    │  Message Queue     │
    │  (Kafka)           │
    │  fan-out events    │
    └────────────────────┘
```

---

## Step 4: Deep Dives

### 4a: Feed Generation — The Core Problem

**Option A: Fan-out on Write (Push model)**
- When user tweets, immediately push tweet ID to all followers' timeline caches
- Feed read is fast: just read pre-computed cache
- Problem: celebrity with 100M followers → 100M writes on every tweet

**Option B: Fan-out on Read (Pull model)**
- When user opens feed, query who they follow → fetch their recent tweets → merge + sort
- Write is cheap, read is slow: N queries for N followed users
- Problem: user follows 1000 people → 1000 DB queries per feed refresh

**Solution: Hybrid (what Twitter actually uses)**
```
IF user has < 10K followers:
    → Fan-out on write to followers' timeline caches
ELSE (celebrity):
    → Don't fan-out. On read, fetch celebrity tweets separately + merge with pre-computed cache
```

**Timeline cache structure (Redis Sorted Set):**
```
Key:   timeline:{userId}
Value: Sorted Set of tweetIds, scored by timestamp
TTL:   24 hours (inactive users cache evicted)

ZADD timeline:userId score(timestamp) tweetId
ZREVRANGE timeline:userId 0 19  → latest 20 tweets for feed
```

### 4b: Tweet Storage (Cassandra)

```
Why Cassandra?
- Write-heavy (500M/day) — Cassandra is write-optimized (append to WAL + memtable)
- Massive scale (PBs of data) — horizontal partitioning built-in
- No complex joins needed (tweets are read by ID or by userId+time)

Tweet table:
  partition key: userId
  clustering key: tweetId (snowflake ID — encodes timestamp)
  columns: content, mediaUrl, createdAt, likeCount

This lets us query: "all tweets by user X, newest first" efficiently
```

**Snowflake ID** (why not UUID for tweetId):
```
64-bit ID = 41 bits timestamp | 10 bits machineId | 12 bits sequence
- Sortable by time (critical for feed ordering)
- No central coordination needed
- 4096 IDs/ms per machine
```

### 4c: Feed Ranking (Not Just Chronological)

Twitter moved from pure chronological to ranked feed. Signals:
- Recency (time decay)
- Engagement score (likes, retweets, replies — weighted)
- Your engagement history with this author (affinity score)
- Media: tweets with images/video rank higher

In system design interview: mention this is an ML ranking model (offline trained, online inference). The feed service calls a ranking service that scores tweet candidates.

---

## Step 5: Trade-offs

| Decision | Choice | Alternative | Reason |
|---|---|---|---|
| Feed generation | Hybrid push/pull | Pure push | Celebrity problem at pure push |
| Tweet storage | Cassandra | MySQL | Write-heavy, massive scale |
| Timeline cache | Redis Sorted Set | Memcached | Need sorted order by time |
| IDs | Snowflake | UUID | Sortable, time-embedded |
| Feed ordering | ML ranking | Chronological | Better engagement, Twitter does this |

---

## GSTN Bridge
"At GSTN, we had a similar push-based notification system — when a return was filed, we pushed notifications to multiple downstream services. The fan-out problem was similar; we used Kafka topics with consumer groups. For Twitter, the Kafka fan-out is the same pattern but at 1000x scale."

---

# ═══════════════════════════════════════════════════════════
# DESIGN 2: Google Drive / Dropbox — File Storage System
# ═══════════════════════════════════════════════════════════

## Step 1: Clarify Requirements

### Functional
1. Upload files (any type, up to 5GB)
2. Download files
3. Sync across devices (same file, multiple devices)
4. Share files/folders with other users
5. Version history (restore previous versions)

### Non-Functional
- **Availability**: 99.99%
- **Durability**: 99.999999999% (11 nines) — Google's actual guarantee
- **Consistency**: Strong consistency for metadata; eventual for sync
- **Latency**: Upload start < 500ms; download throughput-optimized

---

## Step 2: Scale Estimation

```
Users:          1B total, 500M DAU
Files:          1B users × avg 20 files = 20B files
Storage:        avg file size 500KB → 10 PB total
                new uploads: 10M/day = ~115 uploads/sec
Upload size:    10M files × 500KB = 5 TB/day new data
Metadata:       file name, path, size, type, owner, modified time, version
                Each file metadata ~500 bytes → 20B × 500 bytes = 10 TB metadata
```

---

## Step 3: High-Level Architecture

```
       ┌──────────────┐
       │  Client App  │ (Web, Desktop, Mobile)
       └──────┬───────┘
              │ HTTPS
       ┌──────▼────────┐
       │  API Gateway  │
       └──────┬────────┘
              │
    ┌─────────┼──────────────┐
    │         │              │
┌───▼──────┐ ┌▼───────────┐ ┌▼──────────┐
│Metadata  │ │  Upload    │ │  Sync     │
│ Service  │ │  Service   │ │  Service  │
└───┬──────┘ └──────┬─────┘ └─────┬─────┘
    │               │             │
┌───▼──────┐   ┌────▼──────┐  ┌──▼────────┐
│ Metadata │   │   Chunk   │  │  Notification│
│  DB      │   │  Store    │  │  Queue    │
│ (MySQL)  │   │   (S3)    │  │  (Kafka)  │
└──────────┘   └───────────┘  └───────────┘
                     │
               ┌─────▼──────┐
               │    CDN     │
               └────────────┘
```

---

## Step 4: Deep Dives

### 4a: Chunked Upload (The Key Innovation)

Why chunking?
- Large files (5GB) can't be uploaded atomically (network failure = restart)
- Deduplication: if chunk already exists, skip upload
- Parallel upload: multiple chunks uploaded concurrently

```
File upload process:
1. Client splits file into chunks (4MB each)
2. Client computes SHA-256 hash of each chunk
3. Client sends chunk hashes to server: "which of these do you have?"
4. Server responds: "I have chunks [2,5,7], send me [1,3,4,6]"
5. Client uploads only missing chunks
6. Server assembles file reference (list of chunk hashes in order)
```

**Chunk deduplication:**
```
Chunk store key: SHA-256(chunk_content)
If two files share a chunk (e.g., common header), chunk stored once
Storage savings: Google estimates 30-40% data reduction via deduplication

Metadata record:
{
  fileId: "abc123",
  name: "document.pdf",
  chunks: ["hash1", "hash2", "hash3"],  // ordered
  ownerId: "user456",
  version: 3,
  size: 12MB
}
```

### 4b: Sync Protocol (Multi-Device)

```
Problem: User edits file on laptop. How does phone know to update?

Solution: Long-polling or WebSocket per client session.

1. Client registers with Sync Service via WebSocket
2. When file changes, Upload Service sends event to Kafka:
   {userId, fileId, version, timestamp}
3. Sync Service consumes Kafka event
4. Sync Service pushes notification to all active clients for that user
5. Client pulls updated file (or delta)

Conflict resolution:
- Optimistic: last-write-wins for same file (use vector clock or timestamp)
- Google Docs: operational transformation (complex, only for real-time collaboration)
- Dropbox: creates conflict copy if concurrent edits detected
```

### 4c: Metadata Design (What Goes Where)

```
MySQL (relational) — for metadata:
  - User, File, Directory tables
  - Supports: "all files in directory X", "files shared with me"
  - Transactions for atomicity (rename dir = update all children)

S3 (object store) — for chunk data:
  - Key: SHA-256 hash of chunk
  - Value: raw chunk bytes
  - Storage classes: Standard → Standard-IA (90 days) → Glacier (1 year)
  - Multipart upload API used natively

Redis — for upload session state:
  - Track which chunks uploaded for in-progress uploads
  - TTL: 24h (incomplete uploads cleaned up)
```

---

## GSTN Bridge
"At GSTN we stored return documents in a similar pattern — metadata in MySQL (GSTIN, period, filing status, ARN), actual return data in HBase. The chunking concept maps to how we batched large invoice uploads (100K+ invoices in one GSTR-1) — we split into batches and processed chunks independently with status tracking."

---

# ═══════════════════════════════════════════════════════════
# DESIGN 3: WhatsApp — Real-Time Messaging
# ═══════════════════════════════════════════════════════════

## Step 1: Clarify Requirements

### Functional
1. 1:1 messaging (text, images, video)
2. Group messaging (up to 512 members)
3. Message delivery receipts (sent ✓, delivered ✓✓, read ✓✓ blue)
4. Online/offline status, last seen
5. Push notifications for offline users

### Non-Functional
- **Availability**: 99.99%
- **Latency**: Message delivery < 500ms when both online
- **Scale**: 2B users, 100B messages/day, ~1.15M messages/sec

---

## Step 2: Scale Estimation

```
Users:            2B total, 500M DAU
Messages/day:     100B → 1.15M/sec
Avg message:      100 bytes (text), 100KB (image)
Storage (text):   100B × 100 bytes = 10 TB/day
Storage (media):  assume 10% have images: 10B × 100KB = 1 PB/day (need CDN + compression)
Connections:      500M DAU × 1 WebSocket = 500M concurrent connections
```

---

## Step 3: High-Level Architecture

```
           ┌──────────────┐
           │   Client     │
           └──────┬───────┘
                  │ WebSocket (persistent connection)
         ┌────────▼────────┐
         │  Chat Server    │◄─── Load Balanced (consistent hashing)
         │  (WebSocket)    │
         └────────┬────────┘
                  │
        ┌─────────┼──────────────────┐
        │         │                  │
   ┌────▼────┐ ┌──▼──────┐    ┌──────▼──────┐
   │ Message │ │ Session │    │ Presence    │
   │ Service │ │ Service │    │ Service     │
   └────┬────┘ └──┬──────┘    └─────────────┘
        │         │
   ┌────▼────┐ ┌──▼──────┐
   │ Message │ │ Session │    ┌──────────────┐
   │  Store  │ │  Cache  │    │  Push Notif  │
   │(Cassand)│ │ (Redis) │    │  (APNS/FCM)  │
   └─────────┘ └─────────┘    └──────────────┘
        │
   ┌────▼────────────┐
   │  Kafka          │
   │  (delivery acks,│
   │  group fan-out) │
   └─────────────────┘
```

---

## Step 4: Deep Dives

### 4a: WebSocket Connection Management

Why WebSocket, not HTTP polling?
- Bidirectional: server can push to client without request
- Low overhead: no HTTP headers on every message
- Real-time: 500ms latency target requires persistent connection

```
Connection flow:
1. Client opens WebSocket to Chat Server (via load balancer)
2. Load balancer uses consistent hashing on userId to route to same server
   (ensures both users' connections might be on same server — check before Kafka)
3. Session Service stores: {userId → chatServerId} in Redis
   TTL: connection heartbeat-based (30s)
4. When sending message:
   - Find recipient's chatServerId from Session Service
   - If same server: direct delivery
   - If different server: route via internal message queue
   - If offline: store in Message Store, send push notification
```

### 4b: Message Delivery Guarantees

```
Delivery receipts:
✓  (gray)  = Message sent to server (producer ack from Kafka)
✓✓ (gray)  = Message delivered to recipient device (device sends ack to server)
✓✓ (blue)  = Message read (app sends read receipt when user opens chat)

"At least once" delivery:
- Message stored in Cassandra before attempting delivery
- If delivery fails: retry with exponential backoff
- Client deduplicates via messageId (idempotent receive)

Message ordering:
- Cassandra: partition key = conversationId, clustering key = messageId (Snowflake — time-sortable)
- Guarantees messages in same conversation are ordered
```

### 4c: Group Messaging at Scale

```
Challenge: WhatsApp group = up to 512 members.
If 1 message = 512 delivery operations, and groups are active...

Small groups (<= 100 members):
  - Fan-out on write: write message to each member's message queue
  - Handled via Kafka: 1 event → 512 consumer reads

Large groups (100-512):
  - Fan-out on read: members poll group message log
  - Group has single Cassandra partition (conversationId)
  - Each member tracks their lastReadOffset (like Kafka consumer offset!)

Your GSTN Kafka knowledge is directly applicable here.
```

### 4d: Presence / Last Seen

```
Online presence:
- Each Chat Server tracks connected users
- Heartbeat every 5 seconds from client
- Presence Service aggregates: {userId → lastSeen} in Redis
- TTL: 15 seconds (if no heartbeat → mark offline)

Privacy setting: "Last seen for nobody" → Presence Service doesn't publish timestamp
```

---

## GSTN Bridge
"The group fan-out problem is exactly the Kafka consumer group pattern from GSTN. Each 'group member' is a consumer in the consumer group. The message (return filing event at GSTN) fans out to all consumers (downstream services). The key insight is the same: don't wait for all consumers synchronously — fire the event to Kafka and let consumers process at their own pace."

---

# ═══════════════════════════════════════════════════════════
# DESIGN 4: Uber / Ola — Ride Sharing Platform
# ═══════════════════════════════════════════════════════════

## Step 1: Clarify Requirements

### Functional
1. Rider requests a ride (location + destination)
2. System matches rider with nearby driver
3. Driver accepts/rejects ride
4. Real-time tracking of driver location
5. Ride completion + payment + rating
6. Surge pricing during peak demand

### Non-Functional
- **Availability**: 99.99%
- **Latency**: Match driver within 3 seconds
- **Consistency**: Strong for ride state (can't double-assign driver)
- **Scale**: 25M rides/day, 5M drivers online peak

---

## Step 2: Scale Estimation

```
Rides/day:         25M → 290/sec avg, ~3000/sec peak
Drivers online:    5M peak
Driver location:   every 5 seconds → 5M / 5 = 1M location updates/sec
Rider requests:    ~290/sec
Match latency:     < 3 sec SLA
Location storage:  ephemeral (only current location matters, not history)
Analytics storage: all ride data for pricing models, ETA improvement
```

---

## Step 3: High-Level Architecture

```
Rider App              Driver App
    │                      │
    │ HTTP/WebSocket        │ WebSocket (location stream)
    ▼                      ▼
┌──────────────────────────────────────────┐
│                API Gateway               │
└───────┬──────────┬────────────┬──────────┘
        │          │            │
   ┌────▼────┐ ┌───▼──────┐ ┌──▼──────────┐
   │  Ride   │ │ Location │ │  Matching   │
   │ Service │ │ Service  │ │  Service    │
   └────┬────┘ └───┬──────┘ └──┬──────────┘
        │          │            │
   ┌────▼────┐ ┌───▼──────┐ ┌──▼──────────┐
   │  Ride   │ │Location  │ │  Surge      │
   │  DB     │ │  Store   │ │  Service    │
   │ (MySQL) │ │ (Redis   │ └─────────────┘
   └─────────┘ │  Geo)    │
               └──────────┘
        ┌──────────────────────────┐
        │    Kafka                 │
        │    ride events, payments │
        └──────────────────────────┘
```

---

## Step 4: Deep Dives

### 4a: Geospatial Indexing — Finding Nearby Drivers (Critical)

The core problem: "Find all drivers within 2km of rider at (lat, lng)"

**Option 1: Geohash**
```
Geohash encodes (lat, lng) into a base-32 string
Each character halves the precision:
  - 6 chars ≈ ±0.6km accuracy (good enough for Uber)
  - Prefix matching finds nearby cells

Driver at (12.9716, 77.5946) → Geohash: "tdr1y3"
Rider needs drivers within 2km → query geohashes tdr1y3 + its 8 neighbors

Redis GEO commands (built-in geospatial):
  GEOADD drivers 77.5946 12.9716 "driver123"
  GEORADIUS drivers 77.5946 12.9716 2 km ASC COUNT 5
  → Returns 5 nearest drivers within 2km, sorted by distance
```

**Option 2: QuadTree**
```
Recursively divide map into 4 quadrants.
If quadrant has > threshold drivers → subdivide again.
Leaf nodes store driver locations.
Find nearby: traverse tree, collect all drivers in relevant quadrants.
Better for dynamic data (drivers moving), but complex to implement.
```

**In practice:** Redis Geo (wraps Geohash) is the standard choice. Can answer "5 nearest drivers" in O(log n).

### 4b: Driver Matching Algorithm

```
1. Rider requests ride at location L
2. Matching Service queries Location Service: "Available drivers within 3km of L"
   → Redis GEORADIUS command → returns list of (driverId, distance)
3. Rank drivers by: distance + rating + ETA estimate + previous cancellation rate
4. Send ride request to top driver (async via WebSocket)
5. Driver has 10 seconds to accept
6. If reject/timeout → try next driver in ranked list
7. Once accepted → lock ride assignment in MySQL (optimistic locking with version field)

Preventing double-assignment:
  UPDATE rides SET driver_id = ? WHERE ride_id = ? AND driver_id IS NULL
  → If 0 rows affected, driver was already assigned → try next candidate
```

### 4c: Real-Time Location Tracking

```
Driver sends location update every 4 seconds via WebSocket.
That's: 5M drivers × (1 update / 4 sec) = 1.25M updates/sec

Location Service:
  - Receives location stream
  - Writes to Redis Geo (current location, ephemeral)
  - Publishes to Kafka (for ETA calculation, trip tracking, analytics)

Rider tracking active ride:
  - WebSocket subscription to ride:{rideId} channel
  - Location Service publishes driver location to that channel
  - Rider app updates map every 4 seconds
```

### 4d: Surge Pricing

```
Surge = demand / supply ratio in a geographic cell

Every 5 minutes:
  1. For each Geohash cell (city divided into ~5km² cells):
     - Count active ride requests (demand)
     - Count available drivers (supply)
  2. Surge multiplier = f(demand/supply) — typically step function:
     - ratio < 1.2 → 1.0x
     - ratio 1.2–1.5 → 1.5x
     - ratio > 2.0 → 2.0x (capped for regulation)
  3. Store surge multiplier in Redis per geohash cell, TTL 5 min
  4. Rider sees surge before confirming ride

ML-based surge: predict demand using time-of-day, weather, events → proactive surge
```

---

## GSTN Bridge
"The driver location update pattern is similar to GSTN's real-time filing status tracking. At GSTN, 14M taxpayers submit status updates (filing progress events) and we need to reflect them in near-real-time on dashboards. We used Kafka for the event stream and Redis for the current state. Uber's location stream is the same architecture — Kafka for the firehose, Redis for point-in-time queries."

---

# ═══════════════════════════════════════════════════════════
# BONUS: System Design Decision Trees
# ═══════════════════════════════════════════════════════════

## Decision Tree 1: Which Database?

```
START
  │
  ├─ Need ACID transactions for financial/ledger data?
  │    └─ YES → SQL (MySQL / PostgreSQL)
  │
  ├─ Primary access pattern: key-value lookups, no complex queries?
  │    └─ YES → Redis (if fits in memory) or DynamoDB (if large)
  │
  ├─ Write-heavy (millions/sec), large scale (TB-PB), wide-column data?
  │    └─ YES → Cassandra (time-series, user activity, messages)
  │
  ├─ Document data, flexible schema, moderate scale?
  │    └─ YES → MongoDB
  │
  ├─ Full-text search, log analytics?
  │    └─ YES → Elasticsearch
  │
  ├─ Graph relationships (social network, recommendations)?
  │    └─ YES → Neo4j
  │
  └─ Default for most CRUD apps with moderate scale?
       └─ MySQL with read replicas + Redis cache
```

## Decision Tree 2: Which Messaging System?

| Requirement | Choose |
|---|---|
| High throughput (millions/sec), durability, replayable, consumer groups | **Kafka** |
| Simple task queue, at-most-once, managed (no ops), AWS stack | **SQS** |
| Complex routing, RPC-style, ack/nack per message | **RabbitMQ** |
| Real-time pub/sub, simple, low latency, data already in Redis | **Redis Pub/Sub** |
| Fan-out to multiple subscribers, push notifications | **SNS** (+ SQS for fan-out) |
| Background jobs, priority queues, scheduled tasks | **Sidekiq / Celery / Redis** |

**Your context:** At GSTN you used Kafka for all async processing. That's the right choice for anything needing: durability, replay, consumer groups, high throughput.

## Decision Tree 3: Which Cache Strategy?

| Pattern | How it works | Use when |
|---|---|---|
| **Cache-aside** (lazy loading) | App checks cache, if miss → load from DB → populate cache | Most common. Good for read-heavy, cache misses are tolerable |
| **Read-through** | Cache sits in front of DB, auto-fetches on miss | Simplifies app code. Good for predictable access patterns |
| **Write-through** | Write to cache + DB synchronously | Strong consistency needed. Slower writes |
| **Write-behind** (write-back) | Write to cache, async flush to DB | Low-latency writes. Risk: data loss on crash |
| **Refresh-ahead** | Pre-populate cache before TTL expires | Predictable access, can't tolerate cache miss latency |

**GSTN context:** You used cache-aside with EhCache — the standard pattern. In interviews, say "we used cache-aside because our access patterns were unpredictable, and cache misses just caused a DB read — acceptable given our SLAs."

## Decision Tree 4: SQL vs NoSQL — 8 Factors

| Factor | SQL | NoSQL |
|---|---|---|
| Data relationships | Complex joins needed | Denormalized, no joins |
| Schema | Fixed, known upfront | Flexible, evolving |
| ACID needed | Yes | Eventual consistency OK |
| Scale | Vertical (+ read replicas) | Horizontal sharding |
| Query complexity | Ad-hoc queries, aggregations | Simple key-based access |
| Write pattern | Moderate | Very high write throughput |
| Data size | GB to low TB | TB to PB |
| Your team | SQL expertise | NoSQL expertise |

**Rule of thumb:** Start with SQL. Add NoSQL when SQL becomes a bottleneck. Premature NoSQL = painful migrations.

---

## Interview Tips for Consumer Product Designs

### Pivoting GSTN → Consumer Product
Never say "I only have government system experience." Instead:
- "At GSTN we had 14M taxpayers — that's 14M DAU equivalents, which maps to a mid-size consumer app."
- "Our Kafka consumer framework is the same pattern as WhatsApp's message fan-out."
- "Our distributed cache with EhCache is the same pattern as Twitter's timeline cache — just smaller scale."

### Common Mistakes at SDE-3 Level
1. **Going deep too fast** — don't start with Cassandra schema before drawing HLD
2. **Not estimating scale** — interviewer wants to see you justify your choices with numbers
3. **Ignoring failure cases** — "What happens if the matching service goes down?" should get an answer
4. **No trade-off discussion** — "I chose X" without "vs Y because..."
5. **Forgetting monitoring** — add "I'd add Prometheus metrics and alerting on P99 latency" at end

### "What would you do at 10x scale?"
Structured answer:
1. Identify the bottleneck (which component breaks first?)
2. Scale that component (horizontal + caching + partitioning)
3. Tradeoff introduced by scaling
4. Repeat until satisfied
