# Section 07/08 — Database & Distributed Systems (Q136–Q165)

## Q136: Explain database indexing — how B-Tree indexes work.

**Answer:** B-Tree is a balanced tree where each node can have multiple children. Keeps data sorted, allows searches, insertions, deletions in O(log n).

**How it works in MySQL (InnoDB):**
- **Clustered index:** Primary key. Leaf nodes contain actual row data. Table IS the index. One per table.
- **Secondary index:** Non-PK columns. Leaf nodes contain PK value (pointer back to clustered index). Two lookups for non-covering queries.
- **Covering index:** Index includes all columns needed by query. Avoids going to clustered index. `CREATE INDEX idx ON filings(gstin, status) INCLUDE (filing_date)`.

**GSTN indexing decisions:**
- Primary key on `(filing_id)` — auto-increment bigint.
- Composite index on `(gstin, filing_period, status)` — covers 80% of our queries.
- Index on `(filing_date)` for range queries in reports.
- Avoided over-indexing: each index slows writes and consumes storage. Our filing table gets ~1M inserts/day during deadlines.

### Follow-up: B-Tree vs LSM-Tree?
- **B-Tree (MySQL, PostgreSQL):** Read-optimized. Updates in-place. Good for read-heavy workloads.
- **LSM-Tree (Cassandra, HBase, RocksDB):** Write-optimized. Writes go to memtable → flush to sorted SSTable files → periodic compaction. Great for write-heavy workloads.
GSTN's HBase (for invoice matching, 300Cr+ records) uses LSM-Tree. MySQL (for filing metadata) uses B-Tree. Chose based on read/write ratio per use case.

### Follow-up: Explain the N+1 query problem.
Loading a list of N entities, then lazy-loading a relationship for each = N+1 queries. Example: load 100 filings → each filing.getTaxpayer() triggers a separate query = 101 queries.

Solutions:
1. **Join fetch:** `@Query("SELECT f FROM Filing f JOIN FETCH f.taxpayer")` — single query.
2. **@BatchSize:** `@BatchSize(size=50)` — loads 50 taxpayers at once instead of 1.
3. **@EntityGraph:** Declarative fetch plan.
4. **DTO projection:** Skip entities entirely, query exactly what you need.

We caught N+1 in GSTN's filing dashboard — went from 101 queries to 1 with join fetch. Response time: 2.3s → 120ms.

---

## Q140: Explain database sharding strategies.

**Answer:** Sharding splits data across multiple database instances for horizontal scaling.

**Strategies:**
- **Range-based:** Shard by date range or ID range. Filing records Jan-Jun → Shard A, Jul-Dec → Shard B. Problem: uneven distribution (deadline months have 3x data).
- **Hash-based:** `shard = hash(gstin) % num_shards`. Even distribution. But range queries need to hit all shards.
- **Directory-based:** Lookup table maps key → shard. Flexible but adds a lookup hop.

**GSTN approach:** We shard the HBase invoice matching table by GSTIN hash (300Cr+ invoices). MySQL filing tables are not sharded yet — vertical scaling + read replicas suffice at current scale. If we needed to shard MySQL, we'd use GSTIN-based hash sharding with a routing layer.

### Follow-up: What are the challenges of sharding?
1. **Cross-shard queries:** Queries spanning multiple shards need scatter-gather. Slow.
2. **Transactions:** No distributed transactions across shards (unless you use XA/Saga).
3. **Resharding:** Adding shards requires data migration. Consistent hashing minimizes movement.
4. **Hotspots:** Even with hash sharding, some GSTINs (large enterprises) generate disproportionate data.

---

## Q145: Explain SQL query optimization.

**Answer:**
1. **EXPLAIN ANALYZE** — Always start here. Shows query plan, actual rows scanned, time per step.
2. **Index usage** — Ensure WHERE/JOIN/ORDER BY columns are indexed. Check for index scans vs full table scans.
3. **Avoid SELECT *** — Fetch only needed columns. Helps with covering indexes.
4. **Pagination** — Use keyset pagination (`WHERE id > last_id LIMIT 50`) not OFFSET (OFFSET scans and discards rows).
5. **Batch operations** — INSERT ... VALUES (row1), (row2), (row3) instead of individual inserts.

**GSTN example:** Filing search query was doing full table scan on 50M rows (2.8s). Added composite index on (gstin, period, status), restructured the WHERE clause to match index column order → 3ms. Also switched from `OFFSET 10000 LIMIT 50` to keyset pagination → constant time regardless of page number.

---

## Q150: Explain consensus algorithms (Raft/Paxos).

**Answer:** Consensus allows distributed nodes to agree on a value even with failures.

**Raft (easier to understand):**
1. **Leader election:** Nodes are Follower/Candidate/Leader. Followers receive heartbeats from leader. If heartbeat timeout → become candidate → request votes → majority = new leader.
2. **Log replication:** Leader receives writes → appends to log → replicates to followers → once majority acknowledge → committed → applied to state machine.
3. **Safety:** Only nodes with up-to-date logs can become leader.

**Used by:** etcd (K8s), Consul, CockroachDB.

**GSTN context:** We don't implement Raft directly, but etcd (underneath Kubernetes) uses Raft for storing cluster state. Kafka uses ZooKeeper (ZAB protocol, similar to Paxos) for controller election and topic metadata — migrating to KRaft (Kafka's own Raft implementation).

---

## Q155: Explain event sourcing vs traditional CRUD.

**Answer:**
- **CRUD:** Store current state. UPDATE overwrites previous state.
- **Event Sourcing:** Store sequence of events. Current state = replay all events. Never delete/update events.

**GSTN's event sourcing for audit:**
Every filing state change is an immutable event:
```
FilingCreated(gstin, period, timestamp)
FilingDraftSaved(gstin, data, timestamp)
FilingSubmitted(gstin, timestamp)
FilingValidated(gstin, result, timestamp)
FilingAcknowledged(gstin, arn, timestamp)
```

Benefits for GSTN:
1. **Complete audit trail** — government compliance requires knowing exactly what happened when
2. **Temporal queries** — "What was this filing's status at 3:42 PM on March 15?"
3. **Replay for debugging** — reproduce any state by replaying events
4. **Event-driven architecture** — other services react to events (notifications, analytics)

Stored in Kafka (7-year retention) + batch-loaded to MySQL for queryable audit reports.

---

## Q160: Explain database replication strategies.

**Answer:**
- **Single-leader (master-slave):** All writes to leader. Replicas serve reads. Simple. GSTN MySQL uses this — 1 master + 2 read replicas for filing status queries.
- **Multi-leader:** Multiple leaders accept writes. Conflict resolution needed. Used for multi-datacenter setups.
- **Leaderless (Dynamo-style):** Write to any node. Quorum reads/writes (W + R > N). Cassandra, DynamoDB.

**Replication lag:** Time between write on leader and visibility on replica. Our MySQL replica lag is typically <100ms but can spike to 2-3s during deadline traffic. We handle this by routing reads-after-writes to the master for that specific GSTIN (read-your-writes consistency).
