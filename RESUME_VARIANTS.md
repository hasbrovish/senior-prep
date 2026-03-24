# Resume Variants — Jayanti Vishnoi
## Three Targeted Versions: Fintech | Consumer Product | Finance/Banking

> All three variants use the same 5.5 YOE experience at GSTN.
> Bullets are reordered and reworded to front-load what each company type values most.
> Use the correct variant per application. Do NOT mix bullets between variants.
> Updated: March 2026

---

## VARIANT A — Fintech Resume
### Target: Razorpay, Juspay, PhonePe, Stripe India, CRED, Slice, Groww, Paytm

**Lead angle:** Financial correctness, idempotency, distributed transactions, ledger, audit trails.
Fintech interviewers care most about: "what happens when the network fails mid-payment?"

---

### Headline

Backend Engineer | Payments & Fintech | Java · Kafka · Redis | 5.5 YOE

---

### Professional Summary

Backend engineer with 5.5 years building high-throughput financial systems at GSTN — India's national GST infrastructure processing 3 billion invoices per year for 14 million taxpayers. Deep expertise in distributed transactions, idempotent event-driven payment flows, and financial data correctness at scale. Designed and owned the Kafka consumer framework handling 2M+ events/day with zero data loss across 18 months of production, and built the XA transaction layer guaranteeing ledger consistency across 8 cross-service write operations under a government compliance mandate. Seeking SDE-2/SDE-3 at a fintech company where financial correctness and system reliability are non-negotiable.

---

### Top 6 Experience Bullets (Variant A — Fintech)

- Designed and owned **XA distributed transaction framework (Atomikos JTA) across 8 microservices and 2 data stores (MySQL + HBase)**, enforcing two-phase commit for all cross-service ledger mutations affecting 14M taxpayer records — eliminated split-brain inconsistencies that previously required weekly manual reconciliation, achieving zero ledger errors over 3 years of production.

- Built a **Kafka consumer framework with idempotency controls and Dead Letter Queue (DLQ)** processing 2M+ financial events/day across 12 consumer groups; implemented Redis SET-NX deduplication (24-hour TTL), manual offset commits, and at-least-once delivery with application-layer idempotency keys — zero duplicate processing and zero data loss across 18 consecutive production months.

- Engineered **idempotent REST APIs for tax return submission using composite idempotency keys** (GSTIN + tax period + form type) backed by Redis — reduced duplicate submission errors by 94% and eliminated client-side retry complexity across 6 downstream consuming applications.

- Built a **financial audit trail subsystem capturing every lifecycle state transition** (DRAFT → SUBMITTED → PROCESSED → FILED) as immutable HBase records with timestamp, actor, and delta payload — met government-mandated 7-year data retention with full event-replay and reconstruction capability for compliance audits.

- Implemented **case resolution workflow engine (Strategy + Factory patterns) for 23 financial case types** (TDS defaults, IGST mismatches, refund disputes) with pluggable validation, ledger correction, and audit emission per case type — reduced mean time-to-resolve from 72 hours to under 4 hours for 80% of cases, zero production defects over 2 years.

- Engineered a **distributed cache layer (JBoss DataGrid + EhCache) across 45+ microservices** with write-through and read-through strategies, reducing MySQL load by 40% and cutting average response time by 35% at 500 concurrent filings/sec peak — maintained zero cache-consistency incidents across financial validation flows.

---

### Skills (Variant A — Fintech)

Payments-Critical: Java 11/17, Spring Boot, Apache Kafka (producer/consumer/DLQ/idempotent producer), Redis (distributed lock via SETNX/Redisson, rate limiting, deduplication cache), XA Transactions (Atomikos JTA), Idempotency key design, Saga pattern (orchestration)

Data Stores: MySQL (InnoDB, ACID, row locking, SELECT FOR UPDATE, query optimization), HBase, MongoDB, Redis

Infrastructure: Docker, Kubernetes (AWS EKS), AWS (EC2, RDS, ElastiCache), CI/CD (Jenkins/GitLab)

Supporting: Golang, Angular, Hibernate/JPA, REST APIs, Spring Security, Resilience4j (circuit breaker)

---

## VARIANT B — Consumer Product Resume
### Target: Swiggy, Meesho, MakeMyTrip, Zomato, Flipkart, Amazon India, Walmart Global Tech

**Lead angle:** Scale, distributed caching, event-driven architecture, microservices reliability, real-time processing.
Consumer product interviewers care most about: "how do you handle 10x Black Friday traffic?"

---

### Headline

Backend Engineer | Distributed Systems | Java · Spring Boot · Kafka | 5.5 YOE

---

### Professional Summary

Backend engineer with 5.5 years at GSTN — India's national tax infrastructure serving 14 million users at 500 transactions/second peak with 99.9% uptime. Specialized in distributed caching, Kafka-based event pipelines, and large-scale data systems processing 3 billion records annually. Built foundational platform components adopted across 45+ microservices, including a Kafka consumer framework processing 2M+ events/day and a distributed cache layer that reduced database load by 40% without a single consistency incident. Seeking SDE-2/SDE-3 to design and scale backend systems with real daily user impact.

---

### Top 6 Experience Bullets (Variant B — Consumer Product)

- Built a **multi-tier distributed caching platform (JBoss DataGrid + EhCache) adopted by 45+ microservices**, implementing write-through and read-through cache policies with TTL-based eviction — reduced downstream MySQL read load by 40%, cut P99 dashboard response time from 1.8s to 340ms, and eliminated recurring DB bottlenecks during ITR filing season peaks (500 concurrent filings/sec).

- Designed and operated a **Kafka event-driven consumer framework** consumed by 12 services processing 2M+ business events per day; implemented consumer group management, partition-based parallelism, DLQ routing after 3 retries, and consumer lag monitoring via Micrometer — maintained 99.97% pipeline uptime across 3 years of production.

- Engineered **event-driven status propagation for the GST return lifecycle** using Kafka topics as the inter-service bus — replaced synchronous HTTP calls between 8 microservices with async event streams, reduced end-to-end processing latency from 4.2s to 1.1s, and decoupled service deployments allowing independent releases.

- Led **migration of 3 microservices to Docker/K8s on AWS** with Helm-based deployments, horizontal pod autoscaling, and liveness/readiness probes — achieved 60% infrastructure cost reduction, enabled auto-scaling for 10x traffic spikes during GST filing deadlines, and reduced MTTR from 45 minutes to under 8 minutes.

- Architected **dual-storage ingestion pipeline (HBase + MySQL) for 3 billion annual invoice records**: HBase absorbs write bursts at peak ingestion; MySQL serves relational queries and joins — enabled sub-100ms read latency on 5-year invoice history without impacting write throughput for 14M active users.

- Developed **configurable case workflow engine (Strategy + Factory patterns) supporting 23 case types** with pluggable rule evaluation — reduced new case type onboarding from 3 weeks to 2 days, eliminated cross-team coordination for business rule changes, and handled 100% of dispute volume with zero cross-contamination between case types.

---

### Skills (Variant B — Consumer Product)

Distributed Systems: Java 11/17, Spring Boot, Apache Kafka (producer/consumer/DLQ, partition management), Redis (caching, pub/sub, distributed coordination), Microservices, Event-driven architecture, Horizontal scaling

Data Stores: MySQL (indexing, query optimization, connection pooling — HikariCP), HBase (columnar, time-series ingestion), MongoDB, Redis

Infrastructure: Docker, Kubernetes (Helm, HPA, health probes), AWS (EC2, RDS, ElastiCache, S3), CI/CD pipelines

Supporting: Golang, Angular, Hibernate/JPA (N+1 optimization, entity graphs), REST APIs, Resilience4j, Distributed tracing (Sleuth/Zipkin)

---

## VARIANT C — Finance / Banking Resume
### Target: Goldman Sachs, Morgan Stanley, JP Morgan, Deutsche Bank, Barclays, HSBC Technology, BNY Mellon

**Lead angle:** Java depth, correctness, compliance, ACID transactions, regulatory audit trails, financial domain expertise.
Banking interviewers care most about: "how do you guarantee correctness under failure?" and "how does this comply with audit requirements?"

---

### Headline

Backend Engineer | Financial Systems | Java · Spring Boot · MySQL | 5.5 YOE

---

### Professional Summary

Backend engineer with 5.5 years building compliance-grade financial transaction infrastructure at GSTN — the Government of India's GST platform operating under direct regulatory oversight, processing 3 billion invoice records annually for 14 million registered entities. Deep expertise in Java concurrency, XA distributed transactions (Atomikos/JTA), immutable audit ledgers, and high-correctness data pipelines in environments with zero tolerance for data loss. Proven track record: zero ledger inconsistency incidents over 3 years, zero data loss over 18 months of event processing, 99.9% uptime with no scheduled maintenance windows. Seeking SDE-2/SDE-3 to apply financial systems engineering depth in a banking or capital markets technology environment.

---

### Top 6 Experience Bullets (Variant C — Finance/Banking)

- Implemented **XA distributed transaction management (Atomikos JTA) across MySQL and HBase**, enforcing two-phase commit for cross-store ledger operations in a regulatory environment requiring zero data loss, full auditability, and deterministic rollback on partial failure — zero ledger inconsistency incidents across 3 years serving 14 million registered taxpayers.

- Designed an **immutable event-sourced audit trail for the GST return lifecycle** using HBase as the append-only store — every state transition (DRAFT, SUBMITTED, PROCESSED, REVISED, FILED) is persisted with timestamp, actor ID, and delta payload, meeting 7-year retention and full-reconstruction requirements mandated by CBIC regulatory guidelines.

- Engineered **thread-safe concurrent Java services** using ReentrantReadWriteLock for taxpayer profile cache, volatile flags for lifecycle signaling, and AtomicLong counters for throughput metrics — eliminated intermittent data corruption under high-concurrency peak filing loads, verified by formal security audit review.

- Built a **case resolution workflow engine for 23 dispute and ledger adjustment categories** (Strategy + Factory patterns) — each strategy encapsulates validation logic, business rules, and ledger correction computation with full traceability from trigger event to final ledger entry, supporting complete audit reconstruction for every resolved case.

- Architected a **dual-storage design separating OLTP and OLAP workloads** for 3 billion annual invoice records: MySQL provides ACID-compliant transactional integrity for write operations; HBase provides analytical access for compliance reporting — prevented analytical query contention from impacting critical transaction paths during statutory reporting cycles.

- Implemented **exactly-once producer semantics in Kafka** (acks=all, idempotent producer, transactional commits) with manual consumer offset management and DLQ routing — eliminated event loss and duplication in a system where every invoice record has legal standing under the GST Act, processing 2M+ legally-significant events per day.

---

### Skills (Variant C — Finance/Banking)

Financial Systems Critical: Java 11/17, Spring Boot, ACID transactions, XA/2PC (Atomikos JTA), Optimistic/Pessimistic locking (JPA @Version, SELECT FOR UPDATE), Immutable event logging, Audit trail design, Regulatory compliance

Data Stores: MySQL (InnoDB, MVCC, isolation levels, index optimization, query plans), HBase (append-only, time-series, columnar), MongoDB, Redis

Enterprise Java: Hibernate/JPA (entity lifecycle, second-level cache, N+1 optimization, batch fetching), Spring Security, Spring Batch, Java concurrency (ReentrantLock, AtomicXxx, CountDownLatch, ThreadPoolExecutor), JVM tuning (G1GC, heap sizing, thread dumps)

Infrastructure: Docker, Kubernetes, AWS (EC2, RDS), Apache Kafka, CI/CD

Supporting: Golang, Angular, REST APIs, Distributed tracing, Performance profiling (JProfiler/VisualVM)

---

## Usage Guide

| Variant | Apply To | Lead Angle | Priority Keywords |
|---|---|---|---|
| A — Fintech | Razorpay, CRED, Juspay, PhonePe, Groww, Slice, Paytm | Payments correctness, idempotency, ledger | Kafka, Redis, XA, distributed transactions, idempotency, fintech |
| B — Consumer Product | Swiggy, Meesho, MMT, Zomato, Flipkart, Walmart | Scale, caching, event-driven, microservices | Kafka, distributed cache, microservices, event-driven, Java, scale |
| C — Finance/Banking | Goldman, Morgan Stanley, JP Morgan, Deutsche, Barclays | ACID, compliance, audit, correctness, Java depth | Java, ACID, compliance, regulatory, XA, financial systems, immutable |

---

## What Changes Per Variant

- Headline (1 line)
- Professional Summary (3 lines)
- Top 6 experience bullets under the GSTN role (reordered + reworded for audience)
- Skills section (same technologies, reordered by relevance to target)

## What Stays the Same

- Name, contact details, education
- Employer name, dates, job title
- Any certifications or side projects section

---

## ATS Checklist (applies to all three variants)

- No tables, no columns, no text boxes in the actual resume file — ATS parsers cannot read them (the table above is for this guide only)
- Use plain hyphens for bullets, not Unicode bullet characters
- Spell out abbreviations on first use: "Goods & Services Tax Network (GSTN)", "Dead Letter Queue (DLQ)"
- Include exact technology names as recruiters search: "Apache Kafka" not just "Kafka", "Spring Boot" not just "Spring"
- Keep to 2 pages maximum
- Single-column layout for maximum ATS parsing compatibility
- Save as PDF from Google Docs or Word — not from Mac Pages (known ATS parsing issues with Pages PDFs)
- File name format: Jayanti_Vishnoi_Backend_Engineer_Resume.pdf

---

## Company-Specific Tailoring Notes

**Razorpay / Juspay:** Use Variant A. Add in summary: "familiar with UPI payment flow and gateway reconciliation patterns." Read their engineering blog before the interview — they sometimes ask about decisions published there.

**CRED:** Use Variant A. CRED values engineering craft — avoid performance-over-quality language. Mention the audit trail and case engine as examples of building for longevity, not just speed.

**Groww / Slice:** Use Variant A. Emphasize thread safety and concurrent correctness in your summary line — trading and credit systems are inherently concurrent. Mention BigDecimal over double for currency calculations in interviews.

**Swiggy / Zomato:** Use Variant B. Add: "experience managing peak load during time-sensitive events." They publish engineering blogs heavily — reference their tech stack decisions in cover notes.

**Meesho / Walmart:** Use Variant B. Emphasize the 45-microservice scale and the distributed cache adoption story — they care about platform engineering that multiplies team productivity.

**MakeMyTrip:** Use Variant B. The interval scheduling and hold-and-book problems are directly analogous to your GSTN work — draw those connections explicitly in cover notes and interviews.

**Goldman Sachs:** Use Variant C. Goldman values formality — avoid casual language throughout. Emphasize correctness over speed in every answer. Their HireVue is Java-heavy: deep-dive on JVM, GC algorithms, threading models.

**JP Morgan / Barclays / Deutsche Bank:** Use Variant C. Compliance framing is critical — use words like "regulatory," "audit," "reconciliation," "immutable," "deterministic." These companies know Indian regulatory environments — your GSTN context resonates directly.

---

## Interview Deflection Script (if asked why resume framing differs)

"I tailor the framing slightly for each role to surface what's most relevant to that company's domain. The underlying experience and systems are identical — I'm happy to go deep on any of these projects in whatever direction is most useful for you."
