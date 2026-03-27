# FAANG-Level Advanced Questions (SDE-2/SDE-3)

## Advanced Java
### Q: Explain the Java Memory Model's happens-before guarantees.
Program order → monitor lock → volatile read/write → thread start/join → transitive. Without these, compiler/CPU can reorder instructions. Double-checked locking was broken pre-Java 5 because JIT reordered object initialization.

### Q: How does ConcurrentHashMap achieve thread safety without locking the whole map?
Java 8+: CAS for bucket updates, synchronized only on individual bins during collision traversal. Reads are lock-free (volatile). Size maintained via LongAdder-style striped counting.

### Q: Explain virtual threads and when they help.
Lightweight JVM-managed threads. Millions can run simultaneously. Perfect for I/O-bound (DB calls, HTTP calls) — each request gets its own cheap thread instead of sharing from a bounded thread pool. NOT helpful for CPU-bound work.

## Advanced System Design
### Q: How would you design a system for exactly-once processing at scale?
Idempotent consumers + deduplication. Each event has unique ID. Before processing, check processed_events table. Process + mark processed in same DB transaction. If consumer crashes and retries, dedup catches it. Simpler and more reliable than Kafka transactions.

### Q: Explain the tradeoffs of microservices at your scale.
Benefits: independent deployment (different teams ship independently), technology flexibility (Go for workflow, Java for APIs), isolated failures (circuit breaker). Costs: distributed system complexity (network failures, eventual consistency), operational overhead (50+ pods to monitor), debugging across services (need distributed tracing).

### Q: How do you handle schema evolution in event-driven systems?
Avro + Schema Registry. Rules: only backward-compatible changes (add optional fields, never remove/rename required fields). Old consumers ignore unknown fields. New consumers handle missing optional fields with defaults. Breaking change = new topic + migration.

## Advanced Behavioral
### Q: How do you influence without authority?
Kafka migration story. Led cross-team migration as an IC, not manager. Built data-driven case, framed as solving THEIR problems, co-designed with each team, managed incremental rollout. Influence = data + empathy + shared ownership.

### Q: What's a time you had to make a decision with incomplete information?
Filing deadline crisis. Couldn't spend hours analyzing — had 30 minutes. Made quick decision based on available signals (Grafana dashboards showed DB connection saturation). Applied targeted fix (config change, not code change). Monitored closely. Post-crisis did thorough root cause analysis. Key: speed of safe decision, not perfect decision.
