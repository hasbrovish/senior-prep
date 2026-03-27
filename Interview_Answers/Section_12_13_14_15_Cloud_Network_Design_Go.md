# SECTIONS 12-15: CLOUD, NETWORKING, SYSTEM DESIGN, GOLANG — Interview Answers (Q206–Q248)
## With GSTN Codebase References

---

# SECTION 12: CLOUD / AWS (Q206–Q220)

### Q206. AWS services mapping to GSTN?

**Answer:**

| AWS Service | GSTN Usage |
|------------|-----------|
| **EC2** | Application servers running Spring Boot services |
| **EKS** | Kubernetes cluster for containerized microservices |
| **RDS (MySQL)** | Primary database (multi-AZ, read replicas) |
| **ElastiCache (Redis)** | Distributed caching (session, reference data) |
| **S3** | Return document storage, backups, static content |
| **SQS/SNS** | Notification queuing (alternative to Kafka for specific flows) |
| **CloudWatch** | Monitoring, logging, alerting |
| **IAM** | Service roles, access policies |
| **VPC** | Network isolation (public/private subnets) |
| **Lambda** | Event-driven processing (lightweight tasks) |
| **Route 53** | DNS for api.gst.gov.in |
| **CloudFront** | CDN for taxpayer portal |
| **KMS** | Key management for encryption |

---

### Q207. EC2 instance types?

**Answer:**

| Family | Optimized For | GSTN Use |
|--------|-------------|----------|
| **t3/t3a** | General purpose (burstable) | Dev/QA environments |
| **m5/m6i** | General purpose (balanced) | Most API services |
| **c5/c6i** | **Compute optimized** | Validation, calculation services |
| **r5/r6i** | **Memory optimized** | Report generation, bulk processing |
| **i3** | Storage optimized | Database servers |

**GSTN choice:** `m5.xlarge` (4 vCPU, 16GB) for most services. `c5.2xlarge` for compute-heavy validation during filing. `r5.2xlarge` for MIS/reporting.

---

### Q208. S3 — storage classes and GSTN usage?

**Answer:**

| Storage Class | Access | Cost | GSTN Use |
|--------------|--------|------|----------|
| **Standard** | Frequent | $$$  | Active return documents, recent filings |
| **Standard-IA** | Infrequent | $$  | Returns older than 3 months |
| **Glacier** | Archive | $   | Audit trail, returns older than 1 year |
| **Glacier Deep** | Rare access | ¢   | Legal records (7+ year retention) |

```java
// Presigned URLs for secure document download
// Taxpayer downloads return acknowledgment via time-limited URL
URL presignedUrl = s3Client.generatePresignedUrl(
    "gstn-returns-bucket", 
    "returns/29AAACG1234A1ZD/GSTR1/042024.json",
    expiration  // URL valid for 15 minutes
);
```

**Lifecycle policies:** Automatically transition objects: Standard → IA (after 90 days) → Glacier (after 1 year) → delete (after 7 years per compliance).

---

### Q209. SQS vs SNS vs Kafka?

**Answer:**

| | SQS | SNS | Kafka |
|--|---|---|---|
| Model | **Queue** (point-to-point) | **Pub/Sub** (fan-out) | **Log** (replay, consumer groups) |
| Retention | 14 days max | No retention | **Configurable** (days/weeks) |
| Replay | No | No | **Yes** |
| Ordering | FIFO queues | No | **Per-partition** |
| Throughput | Thousands/sec | Millions/sec | **Millions/sec** |
| Use case | Task queues, decoupling | Notifications to multiple subscribers | **Event streaming** (GSTN) |

**GSTN uses Kafka** for event processing because of replay capability, ordering guarantees, and high throughput during filing season.

---

### Q210. AWS Lambda — serverless?

**Answer:**

| Aspect | Detail |
|--------|--------|
| Cold start | 100ms-5s (depends on language/size) |
| Concurrency | Default 1000/account, can request more |
| Timeout | Max 15 minutes |
| Memory | 128MB - 10GB |

**When appropriate:** Short-lived event processing, scheduled tasks, image resizing, API backends with variable traffic.

**When NOT appropriate:** Long-running processes, stateful applications, low-latency requirements, heavy compute.

**GSTN:** Lambda for lightweight processing (notification formatting, file format conversion). Core filing services need persistent connections (DB, Kafka) → better suited for EKS/EC2.

---

### Q211-Q220. ECS/EKS, CloudWatch, IAM, VPC, RDS, Auto Scaling, ElastiCache, Bedrock, Cost, Well-Architected

**Q211. ECS vs EKS:** EKS preferred for GSTN — K8s ecosystem, portability across clouds, rich tooling. ECS is simpler but AWS-locked.

**Q212. CloudWatch:** Log groups per service. Alarms for: HTTP 5xx rate > 1%, response time p99 > 2s, CPU > 80%. SNS notification to on-call team.

**Q213. IAM Least Privilege:** Each service has its own IAM role. ReturnAPI role: read/write to returns-bucket S3, read from RDS. It cannot access payment data. Service-to-service auth via IAM roles for service accounts (IRSA in EKS).

**Q214. VPC Architecture:**
```
VPC (10.0.0.0/16)
├── Public Subnets (10.0.1.0/24)  — ALB, NAT Gateway, Bastion
├── Private Subnets (10.0.10.0/24) — Application pods (EKS)
└── DB Subnets (10.0.20.0/24)     — RDS, ElastiCache
Security Groups: App → DB (port 3306 only), ALB → App (port 8080)
```

**Q215. RDS:** Multi-AZ for failover (automatic in < 60s). Read replicas for dashboard/report queries. Automated daily backups with 7-day retention. MySQL 8.0 engine.

**Q216. Auto Scaling:** Target tracking policy — maintain CPU at 70%. During filing deadline: min 10, max 100 instances. Scheduled scaling — pre-scale before known peak hours.

**Q217. ElastiCache (Redis):** Cluster mode enabled for sharding. Multi-AZ with automatic failover. Used for session management, OTP caching, taxpayer data caching.

**Q218. AWS Bedrock:** POC for AI-powered features — intelligent form filling assistance, anomaly detection in filings, automated query responses for taxpayer support.

**Q219. Cost Optimization:**
- Reserved Instances for baseline load (40-60% savings)
- Spot Instances for batch processing (up to 90% savings)
- Right-sizing based on CloudWatch metrics
- S3 lifecycle policies for cost-effective storage
- Cleanup unused EBS volumes, snapshots, old AMIs

**Q220. Well-Architected (5 pillars):**
1. **Operational Excellence** — Automation, monitoring, runbooks
2. **Security** — IAM, encryption, compliance (most important for GSTN — government data)
3. **Reliability** — Multi-AZ, auto-scaling, disaster recovery
4. **Performance Efficiency** — Right instance types, caching, CDN
5. **Cost Optimization** — Reserved, Spot, right-sizing

---

# SECTION 13: NETWORKING & SECURITY (Q221–Q230)

### Q221. HTTP/1.1 vs HTTP/2 vs HTTP/3?

**Answer:**

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---------|---------|--------|--------|
| Transport | TCP | TCP | **QUIC (UDP-based)** |
| Multiplexing | No (one request per connection) | **Yes** (multiple streams) | Yes |
| Header compression | No | **HPACK** | **QPACK** |
| Server push | No | Yes | No |
| Head-of-line blocking | Yes (TCP level) | Yes (TCP level) | **No** (per-stream) |
| Connection setup | TCP + TLS = 2-3 RTT | TCP + TLS = 2-3 RTT | **1 RTT** (0-RTT resume) |

**GSTN:** HTTP/2 between API Gateway and clients. HTTP/1.1 or gRPC between internal services.

---

### Q222. HTTPS — TLS handshake?

**Answer:**

```
Client → Server: ClientHello (supported cipher suites, TLS version)
Server → Client: ServerHello (chosen cipher), Server Certificate
Client: Verify certificate (CA chain), generate pre-master secret
Client → Server: Encrypted pre-master secret (using server's public key)
Both: Derive session keys from pre-master secret
Client → Server: Finished (encrypted with session key)
Server → Client: Finished (encrypted with session key)
--- Encrypted communication begins ---
```

**GSTN:** All taxpayer-facing APIs use HTTPS. Internal services may use mTLS (mutual TLS) for service-to-service authentication. Certificates managed in `Commons/Certs/` directory (separate certs per environment: dev, sit, uat, prod).

---

### Q223-Q225. TCP/UDP, DNS, REST vs gRPC vs GraphQL

**Q223. TCP vs UDP:** TCP for HTTP/REST (reliable, ordered). UDP for real-time streaming, DNS queries. QUIC uses UDP with TCP-like reliability built on top.

**Q224. DNS Resolution:**
```
Browser → DNS Resolver → Root NS → .in NS → gst.gov.in NS → IP
    → Route 53 → CloudFront/ALB → K8s Ingress → Service → Pod
```

**Q225. REST vs gRPC vs GraphQL:**
| | REST | gRPC | GraphQL |
|--|---|---|---|
| Protocol | HTTP/JSON | **HTTP/2 + Protobuf** | HTTP/JSON |
| Speed | Good | **Fastest** (binary, streaming) | Varies |
| Contract | OpenAPI/Swagger | **Strict .proto files** | Schema |
| Use case | External APIs | **Internal microservice** | Frontend flexibility |

GSTN uses REST for external taxpayer APIs. gRPC could optimize internal service-to-service calls.

---

### Q226. OAuth2 and OpenID Connect?

**Answer:**

| Grant Type | Use Case |
|-----------|----------|
| **Authorization Code** | Web apps (GST portal — user login) |
| **Client Credentials** | Service-to-service (GSP ↔ GSTN) |
| **PKCE** | Mobile/SPA (GST mobile app) |

```
GSP (GST Suvidha Provider) OAuth2 flow:
1. GSP requests access_token using client_id + client_secret
2. GSTN validates credentials → returns JWT access_token
3. GSP includes JWT in API calls
4. GSTN validates JWT → allows/denies access
```

GSTN's `GspSecurityAutoConfiguration` handles GSP OAuth2 integration.

---

### Q227. OWASP Top 10 Prevention?

**Answer:**

| Vulnerability | Prevention in GSTN |
|--------------|-------------------|
| **SQL Injection** | JPA parameterized queries (`@Param`), never concatenate user input into SQL |
| **XSS** | Input validation, output encoding, Content-Security-Policy header |
| **CSRF** | Disabled for stateless REST APIs (JWT-based, no cookies) |
| **Broken Auth** | JWT with expiry, token invalidation in `GspAuthToknLogRepository` |
| **Sensitive Data** | HTTPS everywhere, encrypt at rest (KMS), mask GSTIN in logs |
| **Broken Access Control** | RBAC via `RoleAccessMapEntity`, per-GSTIN authorization |
| **Security Misconfig** | Disable Swagger in prod, restrict actuator endpoints |
| **Vulnerable Components** | Regular dependency scanning, update libraries |
| **SSRF** | Validate URLs, whitelist allowed domains for callbacks |

---

### Q228-Q230. API Security, Encryption, Load Balancing

**Q228. GSTN API Security layers:**
1. **API Gateway** — Rate limiting, IP whitelisting
2. **JWT Authentication** — Token validation
3. **RBAC Authorization** — Role-based access
4. **Input Validation** — AOP validators, @Valid
5. **Encryption** — TLS in transit, AES at rest

**Q229. Encryption:**
- Symmetric (AES-256): Fast, for data at rest. Same key for encrypt/decrypt.
- Asymmetric (RSA): Slow, for key exchange and digital signatures. Public/private key pair.
- At rest: RDS encryption, S3 server-side encryption
- In transit: TLS 1.2/1.3

**Q230. Load Balancing:**
- **L4** (Transport): TCP/UDP level, fast, no content inspection. Network Load Balancer (NLB).
- **L7** (Application): HTTP level, content-based routing, SSL termination. Application Load Balancer (ALB).
- GSTN: ALB for external traffic (path-based routing), kube-proxy for internal (Round Robin).

---

# SECTION 14: SYSTEM DESIGN (Q231–Q240)

### Q231. Design a Tax Filing System (GSTN)?

**Answer:**

```
Architecture:
┌─────────────┐     ┌──────────────┐     ┌─────────────────────────┐
│ Taxpayer     │────→│ API Gateway  │────→│ Microservices           │
│ Portal/App   │     │ (Rate limit, │     │ ├── Registration Service │
└─────────────┘     │  Auth, Route)│     │ ├── Return Filing Svc    │
                    └──────────────┘     │ ├── Payment Service       │
┌─────────────┐           │              │ ├── Ledger Service        │
│ GSP Partners│───────────┘              │ ├── Notification Service  │
└─────────────┘                          │ └── Dashboard Service     │
                                         └──────────┬────────────────┘
                                                     │
                    ┌────────────┐  ┌───────┐  ┌─────┴──────┐
                    │ Kafka      │  │ Redis │  │ MySQL      │
                    │ (Events)   │  │(Cache)│  │(Sharded    │
                    └────────────┘  └───────┘  │by state)   │
                                               └────────────┘
Key Design Decisions:
- API versioning: /v1.0/taxpayerapi/...
- Sharding by state (2-digit GSTIN prefix)
- Kafka for event-driven async processing
- Redis for session + reference data caching
- HPA for deadline traffic spikes (3x → 50x pods)
- Read replicas for dashboard/MIS queries
```

**Scale numbers:**
- 14M+ registered taxpayers
- 1B+ invoices processed monthly
- 30M+ returns filed per month
- Peak: 200K+ concurrent users during deadline

---

### Q232-Q240. Rate Limiter, Notification, URL Shortener, etc.

**Q232. Rate Limiter Design:**
- Redis Sorted Set with timestamp scoring
- Sliding window: count requests in last 60 seconds per GSTIN
- Distributed: all API instances share Redis counter
- Config: 100 requests/minute for taxpayers, 1000/minute for GSPs

**Q233. Notification System:**
```
Filing Event → Kafka → Notification Consumer
    → Priority Queue (deadline reminders = high priority)
    → Template Engine (SMS/Email template)
    → Delivery (SMS gateway / Email SMTP)
    → Retry on failure (exponential backoff)
    → DLQ for permanent failures
    → Deduplication (Redis set of sent notification IDs)
```

**Q234. URL Shortener:** Base62 encoding of auto-increment ID. Use cache for hot redirects. 301 (permanent) vs 302 (temporary) redirect.

**Q235. Distributed Cache:** Consistent hashing for key distribution. LRU eviction. Replication for HA. GSTN's `DistCacheFwk` abstracts Redis operations.

**Q236. File Storage:** Metadata in MySQL, files in S3. Chunked upload for large files. Presigned URLs for secure download.

**Q237. Payment Processing:**
- Idempotency key per payment request (prevent double charge)
- Pessimistic locking on ledger balance
- Saga: debit ledger → create challan → generate receipt (compensate on failure)
- Reconciliation batch job (daily)

**Q238. Logging/Monitoring:**
```
Application → SLF4J/Logback → Log files
    → Filebeat/Fluentd → Elasticsearch → Kibana (search/visualization)
    → Micrometer → Prometheus → Grafana (dashboards/alerts)
    → Custom health indicators → K8s probes
```

**Q239. Auth System:** JWT + Redis session store. Access token (15 min TTL) + Refresh token (7 days). RBAC with roles stored in DB. Token blacklisting in Redis on logout.

**Q240. Search System:** Inverted index (Elasticsearch/Solr). GSTN uses `SolrDIHFwk` for search. Index taxpayer data (GSTIN, name, state). TF-IDF for relevance scoring.

---

# SECTION 15: GOLANG (Q241–Q248)

### Q241. Why Go over Java?

**Answer:**

| Aspect | Go | Java |
|--------|-----|------|
| Startup | **< 1 second** | 5-15 seconds (JVM warmup) |
| Memory | **10-50 MB** | 200-500 MB (JVM overhead) |
| Binary | **Single static binary** | JAR + JVM |
| Concurrency | **Goroutines** (lightweight, 2KB stack) | Threads (heavy, 1MB stack) |
| Deployment | Copy binary, run | Install JVM, configure classpath |
| Best for | CLI tools, high-concurrency services, proxies | Enterprise apps, complex business logic |

**When I chose Go (Infosys MarketPlace):** Needed a high-concurrency API gateway with minimal resource usage. Go's goroutines handled 100K+ concurrent connections efficiently.

---

### Q242. Goroutines vs Java Threads?

**Answer:**

| | Goroutine | Java Thread |
|--|---|---|
| Stack size | **2KB** (grows dynamically) | **1MB** (fixed) |
| Creation cost | **Microseconds** | Milliseconds |
| Context switch | **User-space** (Go scheduler) | **Kernel-space** (OS scheduler) |
| Count | **Millions** | Thousands (before Virtual Threads) |
| Scheduling | **M:N** (M goroutines on N OS threads) | 1:1 (one thread = one OS thread) |

```go
// Launch 100K goroutines — trivial in Go
for i := 0; i < 100000; i++ {
    go processRequest(i)  // Each goroutine ~ 2KB
}
// Total memory: ~200MB. In Java threads: ~100GB
```

**Java 21 Virtual Threads** narrows this gap significantly.

---

### Q243-Q248. Channels, Interfaces, Error Handling, GC, MongoDB+GraphQL, net/http

**Q243. Channels:**
```go
// Unbuffered — synchronous (sender blocks until receiver ready)
ch := make(chan string)

// Buffered — async up to capacity
ch := make(chan string, 100)

go func() { ch <- "message" }()  // Send
msg := <-ch                        // Receive
```

**Q244. Go Interfaces (Duck Typing):**
```go
type Validator interface {
    Validate(data string) error
}
// Any struct with Validate method implicitly implements Validator — no "implements" keyword
```

**Q245. Error Handling:**
```go
result, err := processReturn(gstin)
if err != nil {
    return fmt.Errorf("failed to process return: %w", err)  // Wrap error
}
```
No exceptions — explicit error checking at every step. More verbose but no hidden errors.

**Q246. Go GC:** Concurrent, tri-color mark-and-sweep. Sub-millisecond pauses (typically < 500μs). Simpler than JVM GC — no generational, no tuning needed.

**Q247. MongoDB + GraphQL (Infosys MarketPlace):**
- MongoDB for flexible product schema (nested documents, no JOIN needed)
- GraphQL for frontend to request exactly what it needs (avoid over-fetching)
- Go server with `graphql-go` library resolving queries against MongoDB

**Q248. Go net/http:**
```go
http.HandleFunc("/api/returns", func(w http.ResponseWriter, r *http.Request) {
    gstin := r.URL.Query().Get("gstin")
    data := getReturnData(gstin)
    json.NewEncoder(w).Encode(data)
})
http.ListenAndServe(":8080", nil)
```
Go's standard library is production-ready — no framework needed for simple REST APIs.
