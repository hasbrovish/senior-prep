# Modern Java, Observability & CQRS

## Modern Java Features (11-21)
- **Records (16):** Immutable DTOs. `record GSTINKey(String gstin, String period) {}` — replaces boilerplate.
- **Sealed classes (17):** `sealed class FilingStatus permits Draft, Submitted, Validated {}` — exhaustive pattern matching.
- **Pattern matching (16+):** `if (obj instanceof Filing f) { use f directly }` — no casting.
- **Text blocks (15):** Multi-line strings with `"""`. Clean SQL/JSON templates.
- **Virtual threads (21):** Millions of lightweight threads. `Thread.ofVirtual().start(...)`. Game-changer for I/O-bound services.
- **Switch expressions (14):** `var result = switch(status) { case ACTIVE -> "active"; default -> "unknown"; };`

## Observability at GSTN
- **Metrics (Prometheus):** Counter (request count), Gauge (active connections), Histogram (latency distribution), Summary (p50/p95/p99).
- **Logging (ELK):** Structured JSON, MDC (traceId, gstin, requestId), async appender.
- **Tracing (Micrometer/Sleuth):** Distributed tracing across microservices. TraceId propagated via HTTP headers.
- **Three pillars together:** Metric alert (p99 spike) → find traceId in logs → trace request across services → pinpoint slow service.

## CQRS at GSTN
- **Command side:** Filing writes → MySQL (normalized, ACID).
- **Query side:** Filing reads → Redis cache (denormalized, fast) + Elasticsearch (full-text search).
- **Sync:** Kafka events propagate writes to read models. Eventually consistent.
- **Why:** Read and write patterns are completely different. Writes need ACID. Reads need speed + flexibility (search, filtering, sorting).
