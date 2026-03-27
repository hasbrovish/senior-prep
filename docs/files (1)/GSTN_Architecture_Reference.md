# GSTN Architecture Reference — Your Strongest Interview Asset

## System Overview

GSTN (Goods and Services Tax Network) is India's government tax infrastructure serving 14M registered taxpayers with 100K+ concurrent requests during filing deadlines. I've worked on this for 5.5 years across Java microservices, Golang workflow engines, and GenAI POCs.

## Architecture Components

### API Layer
- **API Gateway:** Rate limiting (Redis token bucket per GSTIN), JWT authentication, request routing
- **Load Balancer:** Kubernetes Ingress with sticky sessions for filing workflows
- **WAF:** Web Application Firewall for SQL injection, XSS, DDoS protection

### Microservices (45+ services)
- **Filing Service:** Core tax return submission. Spring Boot, MySQL. Handles form validation, draft save/load, final submission to Kafka.
- **Validation Service:** Business rule engine. Validates tax calculations, GSTIN status, compliance rules. Consumes from Kafka, publishes validation results.
- **Notification Service:** Multi-channel (SMS, Email, Push). Priority-based Kafka consumers. Template engine for multilingual (Hindi, English, regional).
- **Ledger Service:** Financial ledger for all tax transactions. ACID guaranteed. 300Cr+ invoices in HBase + MySQL.
- **Appeal/Litigation Service:** Case management for tax disputes. Strategy + Factory pattern for 10+ case types.
- **Workflow Service:** Golang-based finite state machine. Manages multi-step processes (filing, registration, refund). State definitions in YAML.

### Data Layer
- **MySQL:** Primary transactional store. Master + 2 read replicas. Stores filing metadata, taxpayer profiles, tax rules.
- **HBase:** Invoice matching (300Cr+ records, GSTR-2A reconciliation). LSM-tree based, optimized for write-heavy batch loads.
- **Redis Cluster:** 6 nodes (3 masters, 3 replicas). Caching (filing status, taxpayer profiles), rate limiting, distributed locks, session management.
- **MongoDB:** Document store for flexible schemas — filing drafts (schema varies by return type), audit configuration.

### Event Infrastructure
- **Kafka:** 5-broker cluster. Central event bus for all service communication. Topics: filing-events, taxpayer-events, notification-triggers, audit-log. Partitioned by GSTIN hash for ordering guarantees.
- **Schema Registry:** Avro schemas for backward-compatible event evolution.

### Caching Strategy
- **L1 (Caffeine):** Per-pod, in-memory, ~10K entries. Tax rules, static config. TTL 5 min. Invalidated via Kafka events.
- **L2 (Redis):** Distributed. Filing status (5min TTL), taxpayer profiles (1hr TTL), rate limit counters, sessions.
- **Pattern:** Cache-aside default. Cache warm before deadline periods.

### Monitoring & Observability
- **ELK Stack:** Structured JSON logging (LogstashEncoder). MDC: traceId, gstin, requestId. Cross-service request tracing.
- **Prometheus + Grafana:** Request latency (p50/p95/p99), JVM heap, GC pauses, Kafka consumer lag, Redis hit ratio.
- **Alerting:** PagerDuty integration. Alerts on: p99 > 500ms, error rate > 1%, Kafka lag > 10K, Redis connection count > 80%.

### Deployment
- **Kubernetes:** 50+ pods across filing, validation, notification services. HPA scales based on CPU + custom metrics (Kafka lag).
- **CI/CD:** Jenkins pipelines. Build → unit test → integration test (TestContainers) → staging → canary (5% traffic) → full rollout.
- **Blue/Green Deployment:** Zero-downtime deployments. Critical during filing season.

## Key Technical Decisions & Tradeoffs

### Why Kafka over REST for inter-service communication?
REST caused cascading failures during peak load. Kafka decouples: filing service publishes, validation service consumes at its own pace. Zero data loss during spikes — messages queue in Kafka until consumers catch up.

### Why MySQL over NoSQL for filing data?
Tax data is highly relational (taxpayer → filings → line items → tax computations). ACID guarantees non-negotiable for government compliance. Considered MongoDB for filing drafts (schema flexibility) — used it for that. But core transactional data stays in MySQL.

### Why Golang for workflow engine?
Goroutines for lightweight concurrency in parallel state evaluations. Static typing catches state machine definition errors at compile time. Single binary deployment — no JVM overhead. Replaced 3000 lines of Java spaghetti with 800 lines of Go + 200-line YAML.

### Why JBoss DataGrid + EhCache?
Distributed caching across 45+ microservices. ~40% DB load reduction. EhCache for L1 (hot data in-process), DataGrid for L2 (shared across nodes). Later migrated DataGrid components to Redis for simpler operations.

## Scale Numbers (Memorize These)
- 14M registered taxpayers
- 100K+ concurrent users during filing deadlines
- 33K peak QPS
- 300Cr+ (3 billion+) invoices in HBase
- 45+ microservices
- 5 Kafka brokers, 6 Redis nodes
- p99 latency < 500ms for submission, < 200ms for status check
- 8.4 TB/year new filing data
- 7-year audit trail retention
- 10x traffic spike in last 3 days before deadline

## How to Use This in Interviews

Every technical question can be answered with a GSTN example:
- **Caching?** "At GSTN, we use a two-layer cache: Caffeine L1 + Redis L2..."
- **Message queues?** "We migrated from sync REST to Kafka, reducing cascading failures to zero..."
- **Database?** "Our ledger handles 300Cr+ invoices across MySQL + HBase..."
- **Monitoring?** "We use ELK + Prometheus with MDC-based distributed tracing..."
- **Scaling?** "During filing deadlines, K8s HPA scales our filing pods from 10 to 50..."
- **Failure handling?** "Our circuit breaker opens after 50% error rate, and Kafka buffers requests until recovery..."
