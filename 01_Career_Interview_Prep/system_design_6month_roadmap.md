# 6-Month System Design Mastery Roadmap
### From Zero to Designing Systems End-to-End

---

## THE CORE PHILOSOPHY

System design is not about memorizing architectures. It is about developing **judgment** — the ability to look at a problem and know *why* one approach works better than another. This 6-month plan builds that judgment layer by layer, the way a builder learns foundations before walls before roofs.

**The 3 pillars you are building:**
1. **Vocabulary** — knowing what tools exist (databases, caches, queues, protocols)
2. **Reasoning** — knowing *when and why* to pick one tool over another
3. **Communication** — explaining your decisions clearly under interview pressure

---

## HOW TO USE THIS PLAN

- Each month has a **theme**, weekly breakdown, and specific deliverables
- Every week has 3 components: **Read → Build → Present**
- **Read** = theory (books, articles, videos)
- **Build** = hands-on design exercises (written on paper/doc, not code)
- **Present** = explain out loud for 30-40 minutes as if in an interview
- Total daily commitment: **1.5 to 2 hours** (weekdays), **3-4 hours** (weekends)
- You do NOT need to code anything for system design — this is about thinking and designing

---

## MONTH 1: THE BUILDING BLOCKS
### Theme: Learn every component that systems are made of

You cannot design a house if you do not know what bricks, cement, wires, and pipes are. Month 1 is about learning every building block deeply enough that you understand what it does, when you use it, and what its tradeoffs are.

---

### Week 1: How the Internet Actually Works

**What to learn:**
- What happens when you type a URL in the browser (DNS → TCP → HTTP → Server → Response)
- HTTP/HTTPS — methods, status codes, headers, cookies, sessions
- REST API design — resources, endpoints, HTTP verbs, status codes, pagination
- How a basic web application works: Client → Load Balancer → App Server → Database

**Resources:**
| Resource | Link |
|----------|------|
| "What happens when you type google.com" (GitHub) | https://github.com/alex/what-happens-when |
| ByteByteGo — "How does the internet work?" | YouTube: ByteByteGo |
| HTTP crash course (Traversy Media) | YouTube: Traversy Media |
| REST API Design Best Practices | https://restfulapi.net |

**Daily tasks:**
- Day 1-2: Read "what happens when" article + watch ByteByteGo video
- Day 3-4: Study REST API design — methods, pagination, versioning, error handling
- Day 5: Draw the full flow of a request from browser to database and back on paper
- Weekend: Write a 1-page summary in your own words. Explain it out loud to yourself.

**Deliverable:** You should be able to draw and explain the complete journey of a web request on a whiteboard.

---

### Week 2: Databases — The Foundation of Everything

**What to learn:**
- Relational databases (PostgreSQL, MySQL) — tables, joins, indexes, ACID properties
- NoSQL databases — types: document (MongoDB), key-value (Redis, DynamoDB), wide-column (Cassandra), graph (Neo4j)
- When to use SQL vs NoSQL — the actual decision framework
- Indexing — B-tree indexes, hash indexes, composite indexes
- What "normalization" and "denormalization" mean and when you pick each

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 2 — Data Models and Query Languages | Book |
| DDIA Chapter 3 — Storage and Retrieval | Book |
| ByteByteGo — "SQL vs NoSQL" | YouTube |
| Hussein Nasser — "Database Indexing Explained" | YouTube |
| Alex Xu — System Design Vol 1, Chapter on databases | Book |

**Daily tasks:**
- Day 1-2: Read DDIA Chapter 2 (take notes in your own words)
- Day 3-4: Read DDIA Chapter 3 (focus on B-trees and LSM trees)
- Day 5: Watch ByteByteGo "SQL vs NoSQL" video, make a comparison chart
- Weekend: Design a database schema for an e-commerce site (users, products, orders, reviews). Decide what should be SQL and what should be NoSQL. Write down WHY for each choice.

**Deliverable:** A decision framework: "I use SQL when ___. I use NoSQL when ___. I use Redis when ___. I use Cassandra when ___." with real reasoning, not just memorized rules.

---

### Week 3: Caching, CDNs, and Load Balancing

**What to learn:**
- Why caching exists — reducing latency, reducing database load
- Caching strategies: Cache-aside, Read-through, Write-through, Write-back, Write-around
- Cache eviction: LRU, LFU, FIFO — when to use which
- Redis vs Memcached — differences and when to choose each
- Cache invalidation — the hardest problem (TTL, event-based, versioning)
- CDN — what it is, how it works, when to use it (static content, video streaming, global users)
- Load balancers — L4 vs L7, algorithms (Round Robin, Least Connections, IP Hash, Consistent Hashing)

**Resources:**
| Resource | Link |
|----------|------|
| Alex Xu Vol 1 — Chapter on caching + CDN | Book |
| ByteByteGo — "Caching strategies" | YouTube |
| ByteByteGo — "What is a CDN?" | YouTube |
| System Design Primer — Load Balancing section | https://github.com/donnemartin/system-design-primer |
| Gaurav Sen — "Load Balancing" | YouTube |

**Daily tasks:**
- Day 1-2: Study all 5 caching strategies. For each, draw a diagram and write when you would use it.
- Day 3: Study CDN. Draw how a request flows when CDN is present vs absent.
- Day 4-5: Study load balancing. Understand L4 vs L7 difference with real examples.
- Weekend: Answer this question out loud: "You have an API that reads from a database and it is slow. Walk me through every layer of caching and optimization you would add, and in what order."

**Deliverable:** You can explain all 5 caching strategies with diagrams, pick the right one for a given scenario, and explain CDN and load balancer placement.

---

### Week 4: Message Queues, Async Processing, and Protocols

**What to learn:**
- Synchronous vs Asynchronous communication — when to use each
- Message queues — Kafka, RabbitMQ, SQS: what each is good at
- Pub/Sub pattern
- Event-driven architecture — why it matters for decoupling services
- Communication protocols — REST vs gRPC vs GraphQL vs WebSocket
- When to use each protocol (REST for CRUD, gRPC for internal service-to-service, WebSocket for real-time, GraphQL for flexible queries)

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 11 — Stream Processing | Book |
| ByteByteGo — "Kafka vs RabbitMQ vs SQS" | YouTube |
| Gaurav Sen — "Message Queues" | YouTube |
| ByteByteGo — "gRPC vs REST" | YouTube |
| Martin Fowler — Event-Driven Architecture | https://martinfowler.com |

**Daily tasks:**
- Day 1-2: Study message queues. Understand Kafka (log-based, high throughput, replay) vs RabbitMQ (traditional queue, routing) vs SQS (managed, simple).
- Day 3: Study Pub/Sub pattern and event-driven architecture.
- Day 4-5: Study REST vs gRPC vs GraphQL vs WebSocket. Make a comparison table.
- Weekend: Design the notification system for an app like Instagram. When someone likes your photo, how does the notification reach you? Draw the full async flow.

**Deliverable:** Given any two services that need to communicate, you can pick the right protocol and justify it. You understand when to make something synchronous vs asynchronous.

---

### Month 1 Checkpoint

By the end of Month 1, you should be able to:
- Draw the architecture of any basic web application
- Pick the right database for a given problem and explain why
- Choose and explain caching strategies
- Design async communication between services
- Explain load balancing, CDN, and basic scaling

**Self-test:** Draw the architecture of "Design a URL Shortener" using everything you learned. You should be able to cover: API design, database choice, caching layer, how reads and writes work, and how to scale it.

---

## MONTH 2: DISTRIBUTED SYSTEMS FUNDAMENTALS
### Theme: Understand what happens when one machine is not enough

This is where most people get stuck. Month 2 takes you from "I know the building blocks" to "I understand how systems behave when they are distributed across many machines."

---

### Week 5: Scaling — Vertical, Horizontal, and Everything In Between

**What to learn:**
- Vertical scaling (bigger machine) vs Horizontal scaling (more machines)
- Stateless vs Stateful services — why stateless is easier to scale
- Database scaling: Read replicas, sharding (horizontal partitioning), vertical partitioning
- Sharding strategies: Hash-based, Range-based, Directory-based
- Problems with sharding: cross-shard queries, rebalancing, hotspots
- Connection pooling (HikariCP, PgBouncer)

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 6 — Partitioning | Book |
| Alex Xu Vol 1 — Scaling chapter | Book |
| Gaurav Sen — "Database Sharding" | YouTube |
| ByteByteGo — "Horizontal vs Vertical Scaling" | YouTube |

**Weekly deliverable:** Design how you would scale a database that is currently handling 1M users to handle 100M users. Write down every step and tradeoff.

---

### Week 6: Replication and Consistency

**What to learn:**
- Why we replicate data (availability, fault tolerance, read scaling)
- Replication models: Single-leader, Multi-leader, Leaderless (Dynamo-style)
- Consistency models: Strong consistency, Eventual consistency, Causal consistency
- CAP Theorem — what it actually means (and what it does NOT mean)
- ACID vs BASE
- Quorum reads and writes: W + R > N for strong consistency
- Conflict resolution: Last-Write-Wins, Vector Clocks, CRDTs

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 5 — Replication (THE most important chapter) | Book |
| DDIA Chapter 7 — Transactions | Book |
| ByteByteGo — "CAP Theorem" | YouTube |
| Jordan Has No Life — DDIA Chapter 5 walkthrough | YouTube |
| Gaurav Sen — "Consistent Hashing" | YouTube |

**Weekly deliverable:** Explain this scenario: "Your e-commerce site uses eventual consistency. A customer places an order, then immediately checks their order history and does not see it. Why? How do you fix it? What are the tradeoffs of each fix?"

---

### Week 7: Consistent Hashing, Failure Detection, and Consensus

**What to learn:**
- Consistent Hashing — how it works, virtual nodes, why it matters for distributed caches and databases
- Failure Detection — heartbeat, gossip protocol, Phi Accrual Failure Detector
- Leader Election — why it is needed, how Raft and Paxos work at a high level
- Bloom Filters — what they are, false positives vs false negatives, use cases
- Merkle Trees — how they help with data synchronization
- Distributed Locks — why they are hard, Redlock algorithm

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 8 — The Trouble with Distributed Systems | Book |
| DDIA Chapter 9 — Consistency and Consensus | Book |
| Alex Xu Vol 1 — Consistent Hashing chapter | Book |
| MIT 6.824 — Raft lecture | YouTube / MIT OCW |
| ByteByteGo — "Bloom Filters" | YouTube |

**Weekly deliverable:** You are asked: "Design a distributed cache like Memcached across 10 servers. How do you decide which server holds which key? What happens when a server goes down? How do you detect failures? How do you rebalance?" Answer all of this on paper.

---

### Week 8: Rate Limiting, API Gateway, and Microservices Patterns

**What to learn:**
- Rate Limiting algorithms: Token Bucket, Leaky Bucket, Fixed Window, Sliding Window Log, Sliding Window Counter
- API Gateway — what it does (routing, authentication, rate limiting, load balancing)
- Microservices vs Monolith — real tradeoffs, not just buzzwords
- Service Discovery
- Circuit Breaker pattern — why it prevents cascading failures
- Bulkhead pattern
- SAGA pattern — how to handle distributed transactions
- CQRS pattern — when reads and writes have different needs

**Resources:**
| Resource | Link |
|----------|------|
| Alex Xu Vol 1 — Rate Limiter chapter | Book |
| Alex Xu Vol 1 — API Gateway | Book |
| Martin Fowler — Microservices, Circuit Breaker, SAGA | https://martinfowler.com |
| ByteByteGo — "Rate Limiting" | YouTube |
| Chris Richardson — Microservices Patterns | Book (optional) |

**Weekly deliverable:** Design a Rate Limiter service that can handle 10,000 requests per second. Choose the algorithm, explain the storage, explain how it works in a distributed setting (multiple API servers).

---

### Month 2 Checkpoint

By the end of Month 2, you should be able to:
- Explain every distributed systems concept that comes up in interviews
- Understand replication, partitioning, consistency, and consensus
- Design distributed caching, rate limiting, and service communication
- Discuss tradeoffs (consistency vs availability, latency vs throughput, simplicity vs scalability)

**Self-test:** Design a "Key-Value Store like DynamoDB." Cover partitioning (consistent hashing), replication (quorum), failure detection (gossip), conflict resolution (vector clocks), and read/write paths.

---

## MONTH 3: THE DESIGN FRAMEWORK
### Theme: Learn the structured approach to solve ANY design problem

This month, you stop learning individual concepts and start learning how to *combine them* into complete system designs. You will develop a repeatable framework.

---

### Week 9-10: The Framework

**The 7-step framework you will use for every design:**

**Step 1: Requirements Gathering (3-5 minutes in interview)**
- Functional requirements: What does the system DO? (3-5 bullet points)
- Non-functional requirements: What qualities must it have? (scalability, latency, availability, consistency, durability)
- Scale estimation: How many users? How much data? Reads per second? Writes per second?
- Constraints: Any specific technology requirements?

**Step 2: Back-of-Envelope Estimation (2-3 minutes)**
- DAU (Daily Active Users)
- QPS (Queries Per Second) = DAU × actions per day / 86400
- Storage = users × data per user × retention period
- Bandwidth = QPS × average response size
- Memory for cache = QPS × response size × cache duration (use 80/20 rule)

**Key numbers to memorize:**
| Metric | Value |
|--------|-------|
| 1 day | 86,400 seconds (~100K) |
| 1 month | ~2.5 million seconds |
| 1 year | ~31.5 million seconds |
| 1 KB | 1,000 bytes |
| 1 MB | 1,000 KB |
| 1 GB | 1,000 MB |
| 1 TB | 1,000 GB |
| 1 char | 1 byte (ASCII) / 2-4 bytes (UTF-8) |
| 1 UUID | 128 bits = 16 bytes |
| 1 URL | ~100 bytes |
| 1 tweet-sized text | ~300 bytes |
| 1 image (compressed) | ~300 KB |
| 1 minute of video (HD) | ~50 MB |
| Network bandwidth (within datacenter) | ~10 Gbps |
| SSD random read | ~100 microseconds |
| Memory read | ~100 nanoseconds |
| Disk seek | ~10 milliseconds |

**Step 3: API Design (3-5 minutes)**
- Define the external-facing APIs
- RESTful endpoints with HTTP methods
- Request/response schemas
- Pagination, authentication, versioning

**Step 4: Data Model (5 minutes)**
- Identify entities and relationships
- Choose SQL vs NoSQL for each entity (with reason)
- Define schemas/tables
- Identify indexes needed
- Estimate data size

**Step 5: High-Level Architecture (5-10 minutes)**
- Draw the boxes: Client → API Gateway → Services → Database
- Add load balancers, caches, message queues as needed
- Show read path and write path separately
- Identify which components are stateless vs stateful

**Step 6: Deep Dives (10-15 minutes)**
- Pick 2-3 critical components and go deep
- This is where you show your real knowledge
- Common deep dives: database schema, caching strategy, data pipeline, notification flow, search, real-time features

**Step 7: Bottlenecks, Scaling, and Tradeoffs (5 minutes)**
- What breaks at 10x scale? 100x?
- Single points of failure
- Tradeoffs you made and alternatives
- Monitoring and alerting

**Practice this week:**
- Day 1-3: Read Alex Xu Vol 1 Chapters 1-4 (the framework chapters)
- Day 4-5: Watch 3 HelloInterview or Exponent system design walkthroughs on YouTube
- Weekend: Design "URL Shortener" using this exact 7-step framework. Time yourself to 40 minutes. Record yourself explaining it.

---

### Week 11-12: Practice Designs (Beginner Level)

Do one design every 2 days using the framework. Write it out fully on paper or in a doc.

| Design | Key Concepts Tested |
|--------|-------------------|
| Design a URL Shortener | Hashing, base62, read-heavy system, analytics, caching |
| Design a Paste Bin | Similar to URL shortener but with large text storage, object storage (S3) |
| Design a Rate Limiter | Token bucket, distributed counting, Redis |
| Design a Notification System | Push, email, SMS, message queue, priority, templates |
| Design a News Feed (basic) | Fan-out on write vs fan-out on read, caching, ranking |
| Design a Chat System (basic) | WebSocket, message storage, online/offline, delivery status |

**For each design, fill in this template:**

```
SYSTEM: [Name]
DATE: [Date]

1. FUNCTIONAL REQUIREMENTS
   - FR1:
   - FR2:
   - FR3:

2. NON-FUNCTIONAL REQUIREMENTS
   - Scale: ___ DAU, ___ QPS
   - Latency: < ___ms for reads
   - Availability: ___% uptime
   - Consistency: Strong / Eventual (and why)

3. ESTIMATION
   - QPS: ___
   - Storage: ___
   - Bandwidth: ___
   - Cache memory: ___

4. API DESIGN
   [endpoints]

5. DATA MODEL
   [tables/collections with fields]

6. HIGH-LEVEL ARCHITECTURE
   [draw or describe]

7. DEEP DIVES
   - Deep Dive 1: ___
   - Deep Dive 2: ___

8. TRADEOFFS & SCALING
   - Tradeoff 1: ___
   - What breaks at 100x: ___
```

---

### Month 3 Checkpoint

By the end of Month 3, you should be able to:
- Apply the 7-step framework to any design problem
- Complete a full design in 40 minutes
- Do back-of-envelope calculations quickly
- Know the common design patterns for basic systems

**Self-test:** Set a timer for 40 minutes. Design a "Twitter/X" from scratch. Cover posting tweets, news feed, follow/unfollow, search, and notifications. Hit all 7 steps.

---

## MONTH 4: REAL INTERVIEW DESIGNS
### Theme: Practice the exact problems asked at top companies

This is where you move from "I can design simple systems" to "I can design the systems that Apple, Amazon, Oracle, and DoorDash actually ask about."

---

### Week 13-14: Designs From Your Interview Data

| Design | Company | Focus Areas | Resources |
|--------|---------|------------|-----------|
| Design Apple Music | Apple | Audio streaming, adaptive bitrate (HLS), CDN for media, music metadata DB, search, playlist management, offline mode | Alex Xu Vol 2 — similar to "Design YouTube" |
| Design URL Shortener | Apple | You already did this in Month 3 — now add analytics, custom URLs, expiration, abuse prevention | Alex Xu Vol 1 Chapter |
| Design Distributed Cache | Oracle | Consistent hashing, replication, eviction policies, quorum reads/writes, cache warming, hot key handling | Alex Xu Vol 1 — Consistent Hashing |
| Design Key-Value Store | Oracle | LSM tree, WAL, memtable, SSTables, compaction strategies, replication, partitioning | DDIA Chapter 3 + Alex Xu Vol 1 |

**How to practice each design:**
1. Spend 10 minutes gathering requirements (write them down)
2. Spend 5 minutes on estimation
3. Spend 25 minutes designing (API, data model, architecture, deep dives)
4. Spend 10 minutes on tradeoffs and scaling
5. Then read the reference solution (Alex Xu or HelloInterview)
6. Compare — what did you miss? Why?
7. Redo the design 3 days later without looking at notes

---

### Week 15-16: More Interview Designs

| Design | Company | Focus Areas | Resources |
|--------|---------|------------|-----------|
| Design Order Management System | Apple | Order state machine, SAGA pattern for distributed transactions, payment integration, inventory management, eventual consistency | Study SAGA pattern deeply |
| Design Multi-Broker Portfolio Platform | Amazon | Multi-tenancy, data aggregation from multiple external APIs, real-time price updates (WebSocket), schema design for portfolio/holdings/transactions | Alex Xu Vol 2 — "Design Stock Exchange" for inspiration |
| Design Application Monitoring & Alerting | DoorDash | Event ingestion at scale (Kafka), time-series database (InfluxDB, Prometheus), rule engine, alerting pipeline, SLA management, dashboards | Alex Xu Vol 2 — similar to "Design Metrics Monitoring" |

**Additional designs to practice:**
| Design | Why It Matters |
|--------|---------------|
| Design a Web Crawler | Covers distributed coordination, politeness, URL frontier, deduplication |
| Design Google Maps | Covers graph algorithms, location services, caching, tiles |
| Design a Search Autocomplete | Covers Trie data structure, ranking, caching, real-time updates |
| Design a Payment System | Covers exactly-once processing, idempotency, reconciliation, ACID |

---

### Month 4 Checkpoint

By the end of Month 4, you should be able to:
- Design any of the 10+ systems above from memory
- Handle deep-dive questions on any component
- Explain tradeoffs confidently
- Complete a full design in 35-40 minutes

**Self-test:** Have someone (or use Exponent/HelloInterview) give you a random design problem. Complete it in 40 minutes without notes.

---

## MONTH 5: ADVANCED CONCEPTS + DEEP DIVES
### Theme: Go deeper than other candidates on critical topics

This is the month that separates "good" from "great." Most candidates can draw boxes and arrows. You will understand what happens *inside* those boxes.

---

### Week 17-18: Database Deep Dives

**Topics:**
- How a B-tree index works internally — pages, splitting, rebalancing
- How an LSM tree works — memtable, WAL, SSTables, compaction (leveled vs size-tiered)
- When to use B-tree (reads) vs LSM tree (writes)
- Database isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable
- How PostgreSQL implements MVCC (Multi-Version Concurrency Control)
- How to design schemas for read-heavy vs write-heavy workloads
- Denormalization strategies and materialized views
- Time-series databases (InfluxDB, TimescaleDB) — when and why
- Full-text search (Elasticsearch) — inverted index, relevance scoring

**Resources:**
| Resource | Link |
|----------|------|
| DDIA Chapter 3 (re-read with deeper focus) | Book |
| DDIA Chapter 7 — Transactions | Book |
| Hussein Nasser — "PostgreSQL MVCC" | YouTube |
| ByteByteGo — "LSM Tree vs B-Tree" | YouTube |

**Weekly deliverable:** Explain in writing: "You need to design a database for a system that handles 50,000 writes per second and 200,000 reads per second. Walk through your complete thought process — storage engine, schema, indexes, replication, caching."

---

### Week 19-20: Infrastructure Deep Dives

**Topics:**
- Kafka internals — partitions, consumer groups, offsets, exactly-once semantics, log compaction
- How Kafka achieves high throughput (sequential writes, zero-copy, batching)
- Redis internals — data structures, persistence (RDB, AOF), Redis Cluster, Pub/Sub
- Kubernetes basics — pods, services, deployments, horizontal pod autoscaler (know enough to discuss)
- CI/CD pipeline design
- Monitoring stack — Prometheus (metrics), Grafana (visualization), ELK (logs), Jaeger (tracing)
- SLA, SLO, SLI — what they mean and how to design for them
- Disaster recovery — RPO (Recovery Point Objective) and RTO (Recovery Time Objective)

**Resources:**
| Resource | Link |
|----------|------|
| Kafka: The Definitive Guide (Confluent — free online) | https://www.confluent.io/resources/kafka-the-definitive-guide-v2/ |
| ByteByteGo — "Kafka Architecture" | YouTube |
| Redis University (free courses) | https://university.redis.io |
| DDIA Chapter 11 — Stream Processing | Book |

**Weekly deliverable:** Design a real-time data pipeline that ingests 1 million events per second, processes them, stores them, and allows querying within 5 seconds of ingestion. Cover every component.

---

### Month 5 Checkpoint

By the end of Month 5, you should be able to:
- Explain database internals (B-tree, LSM tree, MVCC) at the level Oracle and Apple ask
- Design data pipelines and explain Kafka internals
- Discuss monitoring, alerting, SLAs
- Handle any "go deeper" follow-up in an interview

---

## MONTH 6: MOCK INTERVIEWS + REFINEMENT
### Theme: Practice under real conditions until it feels natural

You now have the knowledge. Month 6 is about converting knowledge into *performance under pressure*.

---

### Week 21-22: Solo Practice

**Daily routine:**
1. Pick a random design from the list of 20+ you have practiced
2. Set a timer for 40 minutes
3. Open a blank page
4. Design the system, speaking out loud as you go
5. Record yourself (phone audio is fine)
6. Listen back and identify: Where did I pause? What did I forget? Where was my explanation unclear?

**Designs to rotate through:**
URL Shortener, Distributed Cache, Key-Value Store, Apple Music, Order Management, News Feed, Chat System, Rate Limiter, Notification System, Web Crawler, Payment System, Search Autocomplete, Monitoring System, Portfolio Platform, Uber/Ride Sharing, Hotel Booking, Ticket Booking, Video Streaming (YouTube), File Storage (Google Drive/Dropbox), Social Network (Facebook)

**Focus on these common interviewer follow-ups:**
- "What happens if this component goes down?"
- "How would you handle a hot partition / hot key?"
- "What if you need to support 10x the current load?"
- "What is the tradeoff you made here? What is the alternative?"
- "How would you migrate from the current design to the new one?"
- "How do you ensure data consistency between these two services?"
- "Walk me through the read path / write path."

---

### Week 23-24: Mock Interviews with Others

**Where to get mock interviews:**
| Platform | What It Offers | Link |
|----------|---------------|------|
| Pramp | Free mock interviews with peers | https://www.pramp.com |
| Interviewing.io | Mock interviews with real engineers | https://interviewing.io |
| Exponent | System design mocks with structured feedback | https://www.tryexponent.com |
| HelloInterview | AI-powered system design practice | https://www.hellointerview.com |
| Discord communities | Find partners in NeetCode Discord, CS Career Hub | Search Discord |
| IGotAnOffer | Mock interviews with ex-FAANG | https://igotanoffer.com |

**Schedule:**
- 3 mock system design interviews per week minimum
- After each mock, write down: What went well? What did I struggle with? What concept do I need to revisit?
- Revisit weak areas immediately — do not let gaps accumulate

**The night before any real interview:**
- Do NOT cram new material
- Review your 7-step framework
- Review your 3 best designs (the ones you are most confident on)
- Sleep well

---

## KEY RESOURCES — COMPLETE LIST (Priority Order)

### Books (Must-Read)

| # | Book | What You Get | When to Read |
|---|------|-------------|--------------|
| 1 | **Designing Data-Intensive Applications (DDIA)** — Martin Kleppmann | Deep understanding of databases, replication, partitioning, transactions, consistency, batch/stream processing | Month 1-2 (primary), revisit Month 5 |
| 2 | **System Design Interview Vol 1** — Alex Xu | 13 structured designs + framework | Month 2-3 |
| 3 | **System Design Interview Vol 2** — Alex Xu | Advanced: proximity service, stock exchange, hotel reservation, metrics monitoring | Month 4-5 |

### YouTube Channels (In Order of Usefulness)

| Channel | Best For | Link |
|---------|----------|------|
| **ByteByteGo** | Visual explanations of every concept, quick 5-10 min videos | https://youtube.com/@ByteByteGo |
| **NeetCode** | System design walkthroughs (his system design playlist) | https://youtube.com/@NeetCode |
| **Jordan Has No Life** | Goes through DDIA chapter by chapter — best if DDIA feels too dense | https://youtube.com/@jordanhasnolife5163 |
| **Gaurav Sen** | Deep conceptual dives (consistent hashing, sharding, etc.) | https://youtube.com/@gaborsen |
| **Hussein Nasser** | Database internals, networking, backend deep dives | https://youtube.com/@haborsen |
| **Exponent** | Full mock system design interviews | https://youtube.com/@tryexponent |
| **IGotAnOffer** | Mock interviews with ex-FAANG engineers | YouTube: IGotAnOffer |
| **System Design Fight Club** | Engineers debating system designs | YouTube |

### Free Online Resources

| Resource | Link |
|----------|------|
| System Design Primer (GitHub) — comprehensive free guide | https://github.com/donnemartin/system-design-primer |
| HelloInterview — system design practice problems with solutions | https://www.hellointerview.com |
| ByteByteGo Newsletter — weekly system design concepts | https://blog.bytebytego.com |
| High Scalability Blog — real architecture case studies | http://highscalability.com |
| InfoQ — architecture articles and talks | https://www.infoq.com |
| Martin Fowler's Blog — patterns (CQRS, Event Sourcing, Microservices) | https://martinfowler.com |
| AWS Architecture Blog — real-world cloud architectures | https://aws.amazon.com/blogs/architecture/ |

### Architecture Case Studies (Learn How Real Companies Built Their Systems)

| Company | System | What You Learn |
|---------|--------|---------------|
| Netflix | Video streaming, microservices | CDN, adaptive bitrate, Zuul, Eureka, Hystrix |
| Uber | Ride matching, dispatch | Geospatial indexing, real-time matching, supply/demand |
| Twitter | Timeline, fan-out | Fan-out on write vs read, caching at scale |
| Instagram | Photo feed, stories | Sharding, Cassandra, Django at scale |
| Discord | Real-time messaging | WebSocket, message storage, Elixir, Cassandra→ScyllaDB migration |
| Slack | Messaging, search | Real-time messaging, search infrastructure |
| Stripe | Payment processing | Idempotency, exactly-once processing, audit trails |

Search for "[Company Name] engineering blog" to find their architecture articles.

---

## LEARNING STYLE TIPS FOR YOUR SITUATION

Since you mentioned struggling with focus and being in isolation, here are specific tactics:

### 1. The "Explain to a Wall" Technique
After every study session, stand up and explain what you learned out loud for 5 minutes. Pretend you are teaching someone. This is the single most effective way to find gaps in your understanding. If you cannot explain it simply, you do not understand it yet.

### 2. The Design Journal
Keep a physical notebook (not digital). For every design you do, draw it by hand. Hand-drawing forces slower thinking, which creates deeper understanding. Date every entry. In 6 months you will look back and see visible progress — this is motivating when progress feels invisible.

### 3. One Concept Per Day Rule
On days when you have no energy for a full study session, just learn ONE concept. Watch one 10-minute ByteByteGo video. Read one section of DDIA. Draw one diagram. This keeps the chain alive even on bad days.

### 4. The Study Partner
Find ONE person preparing for system design interviews on Discord (NeetCode, CS Career Hub) or Reddit (r/leetcode). Do weekly calls where you give each other a design problem and critique each other's answers. This simulates the real interview and breaks isolation.

### 5. Use AI as Your Interview Partner
Come to me (or any Claude session) and say: "Give me a system design problem and then critique my answer." I can simulate the interviewer role, ask follow-ups, point out gaps, and help you practice.

---

## MONTHLY PROGRESS TRACKER

| Month | Theme | Key Milestone |
|-------|-------|--------------|
| 1 | Building Blocks | Can draw and explain any basic web architecture |
| 2 | Distributed Systems | Can explain consistency, replication, partitioning, consensus |
| 3 | The Framework | Can complete a full design in 40 minutes using the 7-step framework |
| 4 | Real Interview Designs | Can design 10+ systems that actual companies ask about |
| 5 | Advanced Deep Dives | Can handle any "go deeper" follow-up question |
| 6 | Mock Interviews | Can perform under pressure, explain clearly, handle curveballs |

---

## FINAL NOTE

System design is not a test of memorization. It is a test of **thinking**. Every senior engineer who interviews you is looking for one thing: "Does this person think about problems the way I do?"

That thinking develops through repetition — not repetition of answers, but repetition of the *process* of breaking down a problem, making decisions, and justifying tradeoffs.

Do not try to memorize 50 system designs. Instead, deeply understand 10-15, and you will be able to design anything they throw at you, because the patterns repeat.

You have 6 months. That is more than enough. Most people who crack these interviews prepared for 3-4 months. You have time on your side. Use it well.
