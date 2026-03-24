# Distributed Event Processing Pipeline with DLQ and Retry

A production-grade event processing system demonstrating at-least-once delivery, dead letter queue handling, idempotency via Redis, and consumer lag monitoring. Built with Spring Boot 3.2, Apache Kafka, Redis, and MySQL.

This is a public, stripped-down version of the same architectural patterns I implemented at GSTN to process 3B+ invoices/year across 14M taxpayers.

---

## Architecture

```
                         ┌─────────────────────────────────────────────────────┐
                         │                  KAFKA CLUSTER                       │
                         │                                                       │
  ┌──────────────┐       │   ┌─────────────────┐     ┌───────────────────────┐ │
  │   REST API   │──────▶│   │  order-events   │────▶│   OrderEventConsumer  │ │
  │  /api/orders │       │   │   (3 partitions)│     │   (concurrency=3)     │ │
  └──────────────┘       │   └─────────────────┘     └──────────┬────────────┘ │
         │               │                                       │              │
         ▼               │                                       │ fail 3x      │
  ┌──────────────┐       │   ┌─────────────────┐     ┌──────────▼────────────┐ │
  │OrderEvent    │       │   │ order-events-dlq│◀────│   DLQ Publisher       │ │
  │Producer      │       │   │  (1 partition)  │     │   (retry exhausted)   │ │
  └──────────────┘       │   └─────────────────┘     └───────────────────────┘ │
                         │          │                                            │
                         └──────────┼────────────────────────────────────────── ┘
                                    │
              ┌─────────────────────┼──────────────────────┐
              │                     │                       │
              ▼                     ▼                       ▼
     ┌────────────────┐   ┌─────────────────┐   ┌──────────────────┐
     │  Redis Cache   │   │     MySQL        │   │  DLQ Consumer    │
     │ (Idempotency   │   │  order_events   │   │  (logs + persists│
     │  NX EX 86400)  │   │  dead_letters   │   │  dead_letters)   │
     └────────────────┘   └─────────────────┘   └──────────────────┘
```

---

## Features

| Feature | Implementation |
|---|---|
| At-least-once delivery | Manual offset commit (`AckMode.MANUAL`) |
| Exactly-once semantics | Idempotent producer (`enable.idempotence=true`, `acks=all`) |
| DLQ after 3 retries | Retry counter in consumer, publishes to `order-events-dlq` |
| Idempotency check | Redis `SET orderId NX EX 86400` before processing |
| Consumer lag monitoring | Micrometer + `/actuator/prometheus` |
| Processing rate | `Counter` metric `pipeline.orders.processed` |
| Error rate | `Counter` metric `pipeline.orders.failed` |
| DLQ rate | `Counter` metric `pipeline.orders.dlq` |

---

## Tech Stack

- **Spring Boot 3.2** — web, actuator, data-jpa, data-redis
- **Apache Kafka 3.6** — event streaming backbone
- **Redis 7** — idempotency store (SET NX)
- **MySQL 8** — persistent order + dead-letter storage
- **Docker Compose** — local environment
- **Micrometer + Prometheus** — metrics

---

## How to Run

### Prerequisites
- Docker + Docker Compose
- Java 21+
- Maven 3.9+

### Start infrastructure
```bash
docker-compose up -d
```

### Build and run the app
```bash
mvn clean package -DskipTests
java -jar target/kafka-pipeline-1.0.0.jar
```

### Send a test event
```bash
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "orderId": "ORD-001",
    "userId": "USR-42",
    "amount": 1500.00,
    "eventType": "ORDER_PLACED"
  }'
```

### Trigger a DLQ scenario (duplicate event = idempotency block, bad amount = processing failure)
```bash
# Send same orderId twice — second will be blocked by Redis idempotency check
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"orderId": "ORD-001", "userId": "USR-42", "amount": 1500.00, "eventType": "ORDER_PLACED"}'

# Negative amount triggers simulated failure → retries → DLQ
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"orderId": "ORD-999", "userId": "USR-42", "amount": -1.00, "eventType": "ORDER_PLACED"}'
```

### Check metrics
```bash
curl http://localhost:8080/actuator/prometheus | grep pipeline
```

---

## Metrics Exposed

```
# HELP pipeline_orders_processed_total Total orders successfully processed
pipeline_orders_processed_total 142.0

# HELP pipeline_orders_failed_total Total orders that failed processing
pipeline_orders_failed_total 3.0

# HELP pipeline_orders_dlq_total Total orders sent to DLQ
pipeline_orders_dlq_total 1.0

# Kafka consumer lag (via kafka.consumer.fetch-manager-metrics)
kafka_consumer_records_lag_max{...} 0.0
```

---

## Interview Talking Points

### "Walk me through this project"

> "This is a public version of the Kafka consumer framework I built at GSTN. At GSTN, we processed 3B invoices per year with strict financial correctness requirements — no event could be lost or double-processed. I've reproduced the same guarantees here: at-least-once delivery via manual offset commit, idempotency via Redis SET NX, and a DLQ for events that exhaust retries. The main difference is scale: GSTN had multi-datacenter replication, here we have a single broker. The code patterns are identical."

### "What is at-least-once delivery and why did you choose it over exactly-once?"

> "Exactly-once in Kafka requires transactional producers and consumers, which adds significant latency overhead. At GSTN and here, I chose at-least-once delivery (manual offset commit) combined with application-level idempotency via Redis. This is the industry-standard approach: let the transport layer deliver at-least-once, handle deduplication at the application layer. The Redis key has a 24-hour TTL, which matches our business SLA."

### "How does the DLQ work?"

> "After 3 failed processing attempts, the consumer publishes the raw event to `order-events-dlq`. A separate DLQ consumer reads that topic and persists to a `dead_letters` table with the failure reason and timestamp. This allows ops teams to inspect, fix the underlying issue, and replay. This is identical to what I built at GSTN — we had a GSTN-DLQ topic that ops could replay after data corrections."

### "What happens if the Redis check itself fails?"

> "Good question. If Redis is unavailable, we fail open — the event proceeds to processing. This is a deliberate trade-off: we'd rather process a duplicate than drop an event in a financial system. The MySQL insert has a unique constraint on `order_id`, so the DB provides a second idempotency layer. At GSTN we made the same decision."

### Maps to GSTN Experience

| GSTN Pattern | This Project |
|---|---|
| Multi-partition Kafka consumer framework | `OrderEventConsumer` with `concurrency=3` |
| DLQ (GSTN-DLQ topic) | `order-events-dlq` + `DlqConsumer` |
| EhCache/JBoss DataGrid for idempotency | Redis `SET NX EX 86400` |
| XA transactions for ledger consistency | MySQL unique constraint as second guard |
| Kafka consumer lag alerting (Grafana) | `/actuator/prometheus` + consumer lag metrics |
| Manual offset commit on success | `AckMode.MANUAL` + `acknowledgment.acknowledge()` |

---

## Project Structure

```
kafka-pipeline/
├── docker-compose.yml
├── pom.xml
├── README.md
└── src/
    └── main/
        ├── java/com/jayanti/pipeline/
        │   ├── KafkaPipelineApplication.java
        │   ├── config/
        │   │   ├── KafkaConfig.java
        │   │   └── RedisConfig.java
        │   ├── model/
        │   │   └── OrderEvent.java
        │   ├── producer/
        │   │   └── OrderEventProducer.java
        │   ├── consumer/
        │   │   ├── OrderEventConsumer.java
        │   │   └── DlqConsumer.java
        │   ├── service/
        │   │   └── OrderProcessingService.java
        │   └── repository/
        │       ├── OrderEventRepository.java
        │       └── DeadLetterRepository.java
        └── resources/
            └── application.yml
```
