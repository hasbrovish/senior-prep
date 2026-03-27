# SECTIONS 7-8: DATABASE & DISTRIBUTED SYSTEMS — Interview Answers (Q136–Q165)
## With GSTN Codebase References

---

# SECTION 7: DATABASE & SQL (Q136–Q150)

### Q136. Indexing — B-tree vs Hash indexes? Composite indexes? Covering indexes?

**Answer:**

**B-tree Index (default in MySQL InnoDB):**
- Balanced tree — O(log n) for search, range queries, sorting
- Supports: `=`, `<`, `>`, `BETWEEN`, `LIKE 'prefix%'`, `ORDER BY`
- **GSTN**: Index on `GSTIN`, `RETURN_PERIOD`, `FILING_DATE`

**Hash Index:**
- O(1) for exact match only
- No range queries, no sorting
- Used internally by MySQL for hash joins, Memory engine

**Composite Index:**
```sql
-- Left-most prefix rule: (gstin, return_period, status)
CREATE INDEX idx_gst_prd_status ON GST_RETURN(gstin, return_period, status);

-- This index helps:
WHERE gstin = '29AAACG1234A1ZD'                        -- ✓ (leftmost)
WHERE gstin = '29AAACG1234A1ZD' AND return_period = '042024'  -- ✓
WHERE gstin = '29AAACG1234A1ZD' AND return_period = '042024' AND status = 'FILED' -- ✓

-- This index does NOT help:
WHERE return_period = '042024'    -- ✗ (skipped leftmost)
WHERE status = 'FILED'            -- ✗ (skipped leftmost)
```

**Covering Index:** Index contains all columns needed by query → no table lookup needed.
```sql
-- If query only needs gstin and status:
CREATE INDEX idx_covering ON GST_RETURN(gstin, status);
-- SELECT gstin, status FROM GST_RETURN WHERE gstin = '29XXX'
-- Index-only scan — never touches table data!
```

**GSTN with 100M+ records:** Proper indexing is critical. Without index on GSTIN, a full table scan on 100M rows takes minutes. With B-tree index: milliseconds.

---

### Q137. EXPLAIN/ANALYZE — reading execution plans?

**Answer:**

```sql
EXPLAIN SELECT * FROM GST_RETURN WHERE gstin = '29AAACG1234A1ZD' AND return_period = '042024';
```

| Key Column | Meaning | Good/Bad |
|-----------|---------|----------|
| `type: const/eq_ref` | Primary key/unique lookup | **Best** |
| `type: ref` | Non-unique index lookup | Good |
| `type: range` | Index range scan | Good |
| `type: index` | Full index scan | OK |
| `type: ALL` | **Full table scan** | **Bad — add index!** |
| `rows` | Estimated rows examined | Lower = better |
| `Extra: Using index` | Covering index (index-only scan) | **Best** |
| `Extra: Using filesort` | Additional sort needed | Expensive |
| `Extra: Using temporary` | Temp table created | Very expensive |

**Optimization checklist:**
1. Check `type` — if `ALL`, add index
2. Check `rows` — if high, index isn't selective enough
3. Check `Extra` — avoid filesort and temporary
4. Use `EXPLAIN ANALYZE` (MySQL 8.0.18+) for actual execution times

---

### Q138. ACID properties with GSTN example?

**Answer:**

Using GST payment processing as example:

| Property | Definition | GSTN Example |
|----------|-----------|-------------|
| **Atomicity** | All or nothing | Payment deduction from cash ledger + challan creation → both succeed or both rollback |
| **Consistency** | DB moves from one valid state to another | Total tax collected = sum of all individual payments (invariant maintained) |
| **Isolation** | Concurrent transactions don't interfere | Two simultaneous payments from same GSTIN don't double-deduct |
| **Durability** | Committed data survives crashes | Once payment is confirmed, it persists even if server crashes |

```java
// GSTN ensures ACID with @Transactional
@Transactional(value = "transactionManagerItcLedger", 
              propagation = Propagation.REQUIRES_NEW, 
              rollbackFor = Exception.class)
public void processPayment(PaymentVO payment) {
    // Atomicity: both operations in same transaction
    ledgerRepository.debitCashLedger(payment.getGstin(), payment.getAmount());
    challanRepository.createChallan(payment);
    // If createChallan fails → debitCashLedger is also rolled back
}
```

---

### Q139. Normalization vs Denormalization?

**Answer:**

| Normal Form | Rule | Example |
|-------------|------|---------|
| **1NF** | Atomic values, no repeating groups | Each column has single value |
| **2NF** | 1NF + no partial dependency on composite key | All non-key columns depend on full PK |
| **3NF** | 2NF + no transitive dependency | Non-key columns don't depend on other non-key columns |
| **BCNF** | Every determinant is a candidate key | Stricter 3NF |

**When we denormalized in GSTN:**
- **Dashboard/MIS reports**: Pre-aggregated tables for frequently queried metrics (total returns filed per state per month). Normalized query would JOIN 4+ tables.
- **Search optimization**: Denormalized data in Solr indexes for full-text search (`SolrDIHFwk`)
- **Caching layer**: Redis stores denormalized taxpayer profiles (joined from registration + returns + ledger tables)

---

### Q140. Connection pooling — HikariCP?

**Answer:**

```yaml
# application.yml — HikariCP configuration
spring:
  datasource:
    hikari:
      maximum-pool-size: 20       # Max connections
      minimum-idle: 5             # Min idle connections
      idle-timeout: 300000        # 5 min — close idle connections
      connection-timeout: 30000   # 30s — wait for connection before error
      max-lifetime: 1800000       # 30 min — recycle connections
      leak-detection-threshold: 60000  # 60s — log warning if connection not returned
```

**GSTN test configuration:**
```properties
# From application-test.properties
bo.db.initialSize.R1=5    # Initial pool size
bo.db.maxActive.R1=10     # Max active connections
```

**Pool size formula:** `connections = (core_count * 2) + effective_spindle_count`
- For 4-core server with SSD: (4 * 2) + 1 = **9 connections** per instance
- For 100K concurrent requests across 20 instances: 9 * 20 = **180 total connections** to DB

**GSTN multi-datasource pooling:**
```java
// DataSourceFactory creates HikariDataSource for each db/shard
public DataSource createDataSource(String dbIdentifier, String shard) {
    HikariDataSource ds = new HikariDataSource();
    ds.setJdbcUrl(url);
    ds.setMaximumPoolSize(maxPoolSize);
    return ds;
}
```

---

### Q141. Read replicas — master-slave replication?

**Answer:**

```
                    ┌─────────────────┐
     Writes ──────→│  Master (Primary) │
                    └────────┬────────┘
                    Replication (async/semi-sync)
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ Replica 1 │  │ Replica 2 │  │ Replica 3 │
       └──────────┘  └──────────┘  └──────────┘
              ▲              ▲              ▲
     Reads ───┴──────────────┴──────────────┘
```

**Routing in GSTN using RoutingDataSource:**
```java
// GSTN's routing datasource — routes reads/writes to appropriate shard
public class RoutingDataSource extends AbstractRoutingDataSource {
    @Override
    protected Object determineCurrentLookupKey() {
        return DbType.getCurrentDb(); // ThreadLocal determines shard
    }
}

// Service sets routing before query
public void setDbRouting(String stateCd) {
    DbType.setCurrentDb(stateCd);  // Route to state-specific DB
}

// DataSourceAutoConfig dynamically registers routing datasources
private DataSource routingDS = dataSourceFactory.createRoutingDataSource(dbIdentifier);
```

---

### Q142. Sharding strategies?

**Answer:**

| Strategy | How | Pros | Cons |
|----------|-----|------|------|
| **Range-based** | GSTIN 01-09 → Shard 1, 10-19 → Shard 2 | Simple, range queries easy | **Hotspots** (some states busier) |
| **Hash-based** | hash(GSTIN) % N → Shard N | Even distribution | No range queries, resharding hard |
| **Directory-based** | Lookup table maps key → shard | Flexible | Single point of failure |

**GSTN approach:** State-based sharding (a form of range-based):
```java
// Each state has its own database/schema
// GSTIN prefix = state code (first 2 digits)
// 29AAACG1234A1ZD → State 29 (Karnataka) → DB shard for Karnataka

public void setDbRouting(String stateCd) {
    DbType.setCurrentDb(stateCd); // Routes to state-specific database
}
```

This makes sense because:
- GST is state-level — most queries are state-scoped
- Tax officers access their own state's data
- Cross-state queries are rare and handled by aggregation services

---

### Q143. Table partitioning?

**Answer:**

```sql
-- GSTN: Partition return data by filing period (monthly)
CREATE TABLE GST_RETURN (
    id BIGINT,
    gstin VARCHAR(15),
    return_period VARCHAR(6),
    filed_date DATETIME,
    status VARCHAR(20)
) PARTITION BY RANGE (YEAR(filed_date) * 100 + MONTH(filed_date)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    -- ... monthly partitions
);

-- Query with partition pruning:
SELECT * FROM GST_RETURN WHERE filed_date BETWEEN '2024-04-01' AND '2024-04-30';
-- Only scans p202404, ignores ALL other partitions!
```

**Benefits for GSTN:**
- Queries for specific month only scan that month's partition
- Old data can be archived by dropping old partitions
- Improved INSERT performance (writes go to latest partition)
- Each partition can have separate indexes

---

### Q144. Stored procedures vs application-level logic?

**Answer:**

| | Stored Procedures | Application Logic |
|--|---|---|
| Performance | **Less network roundtrips** | More roundtrips |
| Debugging | Hard (DB-specific tools) | **Easy** (IDE, breakpoints, logs) |
| Portability | **DB vendor lock-in** | **Portable** across DBs |
| Testing | Difficult to unit test | **Easy** with JUnit/Mockito |
| Versioning | Hard in Git | **Easy** with Git |
| Scalability | **Vertical only** (DB server) | **Horizontal** (add app servers) |

**GSTN:** Primarily application-level logic in Java services. Critical for: testability, portability across database shards, and horizontal scaling. Some complex reporting queries may use stored procedures for performance.

---

### Q145. Database locking?

**Answer:**

| Lock Type | Scope | Concurrency | Use Case |
|-----------|-------|-------------|----------|
| **Row-level** | Single row | **High** | `SELECT ... FOR UPDATE` |
| **Table-level** | Entire table | **Low** | DDL operations, LOCK TABLES |
| **Shared (S)** | Read lock | Multiple readers OK | SELECT with lock |
| **Exclusive (X)** | Write lock | Only one holder | INSERT, UPDATE, DELETE |

**MySQL deadlock detection:**
- InnoDB automatically detects deadlocks
- Rolls back the "cheaper" transaction (fewer locks held)
- Application catches `DeadlockLoserDataAccessException` and retries

---

### Q146. Slow query optimization?

**Answer:**

1. **Enable slow query log**: `slow_query_log=1`, `long_query_time=1` (>1 second)
2. **EXPLAIN the query** — check for full table scans
3. **Add missing indexes** — on WHERE, JOIN, ORDER BY columns
4. **Optimize query**:
   - Avoid `SELECT *` — only fetch needed columns
   - Avoid `LIKE '%prefix'` — can't use index
   - Avoid functions on indexed columns: `WHERE YEAR(date) = 2024` → `WHERE date BETWEEN '2024-01-01' AND '2024-12-31'`
5. **Check for N+1** — use JOIN FETCH in JPA
6. **Pagination** — don't fetch millions of rows
7. **Denormalize** — for complex reporting queries
8. **Partition** — for time-series data

---

### Q147. MySQL vs PostgreSQL?

**Answer:**

| Feature | MySQL | PostgreSQL |
|---------|-------|------------|
| JSON support | Basic | **Advanced (JSONB, indexable)** |
| Full-text search | Built-in | **Better (tsvector)** |
| Concurrency | MVCC (InnoDB) | **MVCC (better implementation)** |
| Replication | Master-slave, Group | **Logical replication, streaming** |
| Extensions | Limited | **Rich (PostGIS, pg_trgm)** |
| Performance | **Faster for simple reads** | Better for complex queries |

**Why GSTN chose MySQL:** Proven at scale, strong InnoDB engine, mature replication, broad team expertise, well-supported by cloud providers.

---

### Q148. SQL joins?

**Answer:**

```sql
-- INNER JOIN — only matching rows from both tables
SELECT r.gstin, r.period, p.amount
FROM GST_RETURN r INNER JOIN PAYMENT p ON r.id = p.return_id;

-- LEFT JOIN — all from left + matching from right (NULL if no match)
SELECT r.gstin, r.period, p.amount
FROM GST_RETURN r LEFT JOIN PAYMENT p ON r.id = p.return_id;
-- Shows returns even without payment

-- Self-join — table joins with itself
SELECT e.name AS employee, m.name AS manager
FROM EMPLOYEE e JOIN EMPLOYEE m ON e.manager_id = m.id;
```

**Performance:** JOINs on indexed foreign keys are efficient. JOIN is typically faster than correlated subquery.

---

### Q149. Subqueries vs JOINs?

**Answer:**

```sql
-- SUBQUERY (slower — executes inner query for each outer row)
SELECT * FROM GST_RETURN WHERE gstin IN (
    SELECT gstin FROM REGISTRATION WHERE state_code = '29'
);

-- JOIN (faster — single execution plan)
SELECT r.* FROM GST_RETURN r 
JOIN REGISTRATION reg ON r.gstin = reg.gstin 
WHERE reg.state_code = '29';
```

**Rule:** JOINs are usually faster because the optimizer can choose optimal join strategy. Subqueries are easier to read for EXISTS/NOT EXISTS patterns.

---

### Q150. Materialized views?

**Answer:**

A **pre-computed query result** stored as a table. Must be manually refreshed.

```sql
-- Create materialized view for GSTN MIS reporting
CREATE MATERIALIZED VIEW mv_monthly_filing_stats AS
SELECT state_code, return_type, DATE_FORMAT(filed_date, '%Y-%m') as filing_month,
       COUNT(*) as total_filed, SUM(tax_amount) as total_tax
FROM GST_RETURN
GROUP BY state_code, return_type, filing_month;

-- Refresh periodically
REFRESH MATERIALIZED VIEW mv_monthly_filing_stats;
```

**Note:** MySQL doesn't natively support materialized views. GSTN achieves this via:
- Pre-aggregated summary tables (refreshed by batch jobs)
- Solr indexes (via SolrDIHFwk) for search
- Redis cache for frequently accessed aggregations

---

# SECTION 8: DISTRIBUTED SYSTEMS CONCEPTS (Q151–Q165)

### Q151. CAP Theorem?

**Answer:**

**CAP:** In a distributed system, during a network **Partition** (P), you must choose between **Consistency** (C) and **Availability** (A).

| Priority | Systems | Behavior during partition |
|----------|---------|-------------------------|
| **CP** (Consistency + Partition tolerance) | HBase, MongoDB (strong mode), ZooKeeper | Rejects requests until consistency restored |
| **AP** (Availability + Partition tolerance) | Cassandra, DynamoDB, DNS | Returns potentially stale data |
| **CA** | Traditional RDBMS (single node) | Not applicable for distributed systems |

**GSTN priorities:**
- **Filing/Payment**: **CP** — cannot accept inconsistent data (duplicate filing, wrong balance)
- **Dashboard/MIS**: **AP** — slightly stale data is acceptable for reports
- **Session cache (Redis)**: **AP** — if cache is partitioned, serve from available node

---

### Q152. Consistent Hashing?

**Answer:**

**Problem:** Simple `hash(key) % N` → if N changes (add/remove server), ALL keys must be remapped.

**Consistent Hashing:** Arrange hash space in a ring. Each server owns a section. When a server is added/removed, only keys in that section are remapped (1/N of keys instead of all).

```
Hash Ring (0 to 2^32):
    Server A at position 1000
    Server B at position 5000
    Server C at position 9000
    
    Key "GSTIN-29XXX" → hash = 3000 → clockwise → Server B
    Key "GSTIN-07XXX" → hash = 7000 → clockwise → Server C
    
    Add Server D at position 7500:
    Only keys between 7000-7500 move from C to D
```

**Used in:** Redis Cluster (16384 hash slots), Kafka partition assignment, CDN caching.

---

### Q153–Q154. Leader Election and Consensus?

**Leader Election:** One node is "leader" that coordinates operations. Algorithms: Bully algorithm, Ring-based. Tools: ZooKeeper (`ZAB`), etcd (`Raft`).

**GSTN Context:** Kafka brokers elect partition leaders. ZooKeeper/KRaft manages Kafka cluster coordination.

**Consensus (Raft):** Ensures all nodes agree on the same state. Leader sends log entries → followers replicate → majority acknowledges → committed. Used by etcd (K8s state store), Kafka KRaft.

---

### Q155. Idempotency?

**Answer:**

**Idempotency:** Processing the same request multiple times produces the same result as processing it once.

```java
// GSTN: Prevent duplicate return filing
public void fileReturn(ReturnVO returnVO) {
    // Idempotency key = GSTIN + period + return type
    String idempotencyKey = returnVO.getGstin() + ":" + returnVO.getPeriod() + ":" + returnVO.getType();
    
    // Check if already processed
    if (redis.exists("filed:" + idempotencyKey)) {
        LOGGER.info("Return already filed, skipping duplicate: {}", idempotencyKey);
        return; // Idempotent — no side effect
    }
    
    // Process filing
    processReturn(returnVO);
    
    // Mark as processed with TTL
    redis.setex("filed:" + idempotencyKey, 86400, "FILED");
}
```

**Strategies:**
1. **Idempotency key** — client sends unique key, server checks before processing
2. **Database unique constraint** — `UNIQUE(gstin, period, return_type)` prevents duplicates
3. **Status check** — check current state before processing
4. **Kafka consumer offset** — manual commit after processing

---

### Q156. Rate Limiting algorithms?

**Answer:**

| Algorithm | How | Pros | Cons |
|-----------|-----|------|------|
| **Token Bucket** | Tokens added at fixed rate, consumed per request | Allows bursts | Slightly complex |
| **Leaky Bucket** | Requests drain at fixed rate | Smooth output | No burst support |
| **Fixed Window** | Count requests in fixed time windows | Simple | Boundary spike (2x at window boundary) |
| **Sliding Window** | Weighted combination of current + previous window | **Best accuracy** | More memory |

**For GSTN API rate limiting:** Sliding Window with Redis. During filing deadline, limit per-GSTIN requests to prevent abuse while allowing legitimate traffic.

---

### Q157. Load Balancing algorithms?

**Answer:**

| Algorithm | How | Best For |
|-----------|-----|----------|
| **Round Robin** | Sequential distribution | Equal-capacity servers |
| **Weighted Round Robin** | Based on server capacity | Mixed-capacity servers |
| **Least Connections** | Route to least busy server | Varying request duration |
| **IP Hash** | Same client → same server | Session affinity |
| **Consistent Hashing** | Minimal remapping on scale | Dynamic server pool |

**GSTN:** Kubernetes uses Round Robin by default via kube-proxy. For sticky sessions (if needed), IP Hash.

---

### Q158. Back-pressure?

**Answer:**

When a consumer can't keep up with the producer, it signals the producer to slow down.

**Strategies:**
1. **Buffering** — Queue messages (Kafka) → consumer processes at own pace
2. **Dropping** — Drop oldest/newest when buffer full
3. **Blocking** — Producer blocks until consumer catches up (Kafka: `max.block.ms`)
4. **Scaling** — Auto-scale consumers (K8s HPA based on consumer lag)

**GSTN:** During filing deadline, Kafka buffer handles traffic spikes. If consumer lag increases, we scale consumer instances.

---

### Q159. Distributed caching challenges?

**Answer:**

1. **Consistency** — Cache might serve stale data after DB update → use TTL + event-driven invalidation
2. **Cache crash** — All requests hit DB (thundering herd) → use circuit breaker, graceful degradation
3. **Hot keys** — One GSTIN cached on one node, overwhelmed → use local cache + distributed cache
4. **Serialization** — Ensure serialization/deserialization is consistent across service versions

---

### Q160. Distributed lock vs database lock?

**Answer:**

| | Distributed Lock (Redis) | Database Lock (SELECT FOR UPDATE) |
|--|---|---|
| Scope | Across services/processes | Within single DB connection |
| Performance | **Faster** (in-memory) | Slower (disk I/O) |
| Failure mode | Lock expires (TTL) | Connection closes → lock released |
| Use case | Cross-service coordination | Single-service data integrity |
| Drawback | **No fencing** (default) — process can continue after lock expires | Blocks DB connections |

---

### Q161–Q165. Bloom Filter, WAL, Gossip, Split Brain, Clock Skew

**Q161. Bloom Filter:** Probabilistic data structure — "definitely not in set" or "probably in set". Use case: check if GSTIN exists before expensive DB lookup. False positives possible, false negatives impossible.

**Q162. Write-Ahead Log (WAL):** Write operation to log BEFORE applying to data. If crash occurs, replay log for recovery. Used by: MySQL InnoDB (redo log), Kafka (commit log), PostgreSQL (WAL).

**Q163. Gossip Protocol:** Each node periodically exchanges state with random peers. Eventually, all nodes know the state of all others. Used by: Cassandra, Redis Cluster, Consul.

**Q164. Split Brain:** Network partition causes two groups to each think they're the leader. Prevention: quorum-based voting (majority must agree), fencing tokens, STONITH (Shoot The Other Node In The Head).

**Q165. Clock Skew:** Different machines have slightly different clocks. Solutions: NTP synchronization, Lamport timestamps (logical clocks), Vector clocks (causal ordering), Google TrueTime (bounded uncertainty). For GSTN: use server-generated timestamps, not client timestamps.
