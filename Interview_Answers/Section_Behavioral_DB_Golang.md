# Behavioral (SDE-3) + Database Deep Dive + Golang
# For: Jayanti Vishnoi | 5.5 YOE GSTN | Java, Spring Boot, Golang

---

## PART 1: Behavioral Interview — Beyond Amazon LP

---

### The Universal Behavioral Framework: STARL

```
S — Situation:  Context. When, where, stakes.
T — Task:       Your specific responsibility.
A — Action:     What YOU did (not the team). Be specific.
R — Result:     Measurable outcome. Numbers when possible.
L — Learning:   What you'd do differently. Shows growth mindset.
```

**SDE-3 add: Impact**
After the result, add: "This influenced how the team approached X going forward" or "We then standardized this pattern across 3 other services."

---

### SDE-3 Behavioral Questions Deep Dive

---

**Q1. "Tell me about a time you disagreed with your tech lead/manager on a technical decision."**

Why they ask: Testing independence of thought, ability to influence up, ability to accept decisions gracefully.

**Bad answer:** "I always align with my manager's decisions."
**Also bad:** "I disagreed and they were wrong and I was right."

**Good answer framework:**
1. State the disagreement clearly (shows you have opinions)
2. How you raised it (data, not emotion)
3. What happened (you won, you lost, you found middle ground)
4. How you handled if you lost (moved on, executed well)

**Template using GSTN:**
"During our cache invalidation design, my tech lead proposed TTL-based expiry across all 70+ cache regions with a uniform 5-minute TTL. I disagreed because our reference data (GSTIN master, HSN codes) changes infrequently — a 5-minute TTL would generate unnecessary DB load. I pulled cache hit/miss metrics and DB query counts showing that high-frequency invalidation of stable data was causing 30% of our DB reads. I proposed a tiered TTL strategy — 5 min for volatile data, 6 hours for reference data, 24 hours for static master data. We discussed it, he agreed on the data, and we implemented the tiered approach. DB load dropped 22%. Learning: always bring data to technical disagreements, never just opinion."

---

**Q2. "Describe the most complex system you've designed end-to-end."**

This is your GSTN Kafka consumer framework or distributed cache story. Focus on:
- The problem scope (scale, constraints)
- The architectural decisions you made and WHY
- Trade-offs you navigated
- Outcome

"I designed the async event processing framework at GSTN that processes 14M taxpayer events including return filed, payment cleared, and ledger updates. The core challenge was reliability at scale — we needed at-least-once processing with exactly-once business outcomes (idempotency). I designed a base Consumer class with pluggable processing logic (Template Method pattern), built-in DLQ routing for failed messages after 3 retries, distributed idempotency check using Redis (messageId → processed status), and a monitoring dashboard for consumer lag. The framework processes 2M+ events/day across 8 consumer types with zero data loss in 18 months of production use."

---

**Q3. "Tell me about a time you simplified a system that had become too complex."**

"Our case workflow engine had grown to 23 if-else branches handling different GST case types (appeal, audit, assessment, refund). Each new case type required modifying the same class — it had become unmaintainable and brittle. I refactored it to use Strategy + Factory pattern. I created an ICaseCustomizer interface, moved each case type's logic to its own class, and created a CaseCustomizerFactory that returned the right strategy based on case type. The original 400-line class became 12 focused classes averaging 35 lines each. Adding a new case type is now a new class — no modification to existing code. Onboarding time for new developers on this module dropped from 2 days to 2 hours."

---

**Q4. "How have you mentored junior engineers?"**

SDE-3 signal: You think about team growth, not just your own work.

"When a junior engineer joined our team, they were assigned to add a new Kafka consumer type. Rather than doing it for them, I paired with them for the first day — I asked questions instead of giving answers: 'What do you think will happen if this consumer throws an exception?' We walked through my existing Consumer.java framework and I had them explain it back to me (Feynman technique). I reviewed their PR with detailed comments explaining the why behind each suggestion, not just 'change this.' Two months later, they independently designed and built a consumer for a new use case with zero issues in production. That's the outcome I measure mentorship by — not my knowledge transfer, but their independence."

---

**Q5. "Tell me about a time you pushed back on a deadline or feature request."**

"During peak GST filing season, the product team requested adding a new reconciliation feature with a 2-week deadline. I analyzed the work involved — it required changes to 3 services, new DB schema, and integration with the external ledger. My estimate was 5 weeks minimum for safe delivery. I documented the risk in a technical memo: what would break if rushed, the production incidents we'd likely face, and the impact during peak filing (any incident during filing season affects 14M taxpayers). I proposed a phased approach — core reconciliation in 3 weeks, edge cases in the following sprint. The product manager pushed back, but I held firm on the data. We did it in phases, and the feature launched without production issues. If we'd rushed, we'd have likely caused a filing service outage during peak."

---

**Q6. "Describe a production incident you owned."**

This is a gift question — shows ownership, debugging skill, systemic thinking.

Structure: What broke → How you found it → How you fixed it → What you changed systemically.

"Our Kafka consumer for return status updates started lagging — 200K+ messages unprocessed. Taxpayers weren't seeing their filing status update. I was on-call and immediately checked consumer lag metrics (we had Kafka consumer lag monitoring). The lag was growing, not shrinking — consumers were processing but not keeping up. I checked consumer thread count — at max. I checked the downstream DB — query times had spiked 10x due to a missing index on a new column added that morning. The fix was immediate: add the index. The permanent fix: we added query performance testing to our CI pipeline — any query without an index on filter columns would fail CI. Consumer lag cleared in 40 minutes. We also added alerting on consumer lag > 10K messages."

---

**Q7. "How do you handle tech debt vs feature velocity?"**

"I classify tech debt into three tiers: P0 (causing production incidents or security risk — fix immediately), P1 (slowing team velocity significantly — schedule in next sprint), P2 (nice to fix when opportunity arises). I keep a visible tech debt backlog with estimated impact and effort. During sprint planning, I advocate for 20% of sprint capacity for P1 tech debt. The argument I use: 'If we don't fix X, our velocity on features will be N% slower for the next quarter. That's a higher cost than fixing it now.' I quantify debt in terms of future feature cost, which product managers respond to."

---

**Q8. "Tell me about a time your design was wrong and you had to change it mid-implementation."**

"I designed the DLQ retry mechanism to retry messages immediately after failure. In production, this caused a cascade: when a downstream service was down, all DLQ messages would retry, fail, re-queue, retry again — creating a retry storm that amplified the incident. I had to stop the retries, analyze the pattern, and implement exponential backoff with jitter. The lesson: retry behavior needs to be designed for failure modes, not just happy path. I now treat retry strategy as a first-class design decision — not an afterthought. I added it as a required design checklist item for all new consumer designs."

---

### Company-Specific Behavioral Angles

**Razorpay / Stripe / Juspay (Fintech):**
- "How do you think about reliability in financial systems?" → "At GSTN we handled tax ledger operations with XA transactions — money cannot be double-counted or lost. I think about financial systems in terms of idempotency, atomicity, and audit trails. Every debit/credit must be traceable."
- "Zero-downtime deployments" → Blue-green + feature flags + database migration before code deployment

**Swiggy / Zomato (Consumer):**
- "How do you balance speed vs quality?" → "I use the 'decision reversibility' heuristic. If a decision can be reversed cheaply (feature flag, config change) → move fast. If it's hard to reverse (DB schema, API contract) → slow down and get it right."

**Flipkart / Amazon (E-commerce):**
- Customer Obsession: "Every performance optimization I made at GSTN was driven by 14M taxpayers having a better experience, not just technical elegance."

**Goldman / Morgan Stanley (Finance):**
- "How do you ensure correctness in financial calculations?" → "Double-entry bookkeeping principle at the code level. Every debit has an equal credit. We run reconciliation jobs that assert: sum(all debits) == sum(all credits) at end of day. Any discrepancy pages on-call immediately."

**Google / Atlassian (Platform):**
- Cross-team influence: "I documented our Kafka consumer framework, ran internal tech talks, and had 3 other teams adopt it — with zero code duplication. The key was making the docs great, not just the code."

---

### "Why This Company?" Templates

**Razorpay:**
"Razorpay is building India's payment infrastructure. My GSTN work gave me deep experience in financial data correctness, distributed transactions, and ledger systems — exactly what payments infrastructure needs. I want to work on systems where correctness is non-negotiable and scale is massive."

**CRED:**
"CRED has a reputation for engineering sophistication — the kind of place that cares about performance, observability, and clean architecture, not just shipping features. The premium user experience is backed by premium engineering. That's the environment I want to grow in."

**Swiggy:**
"Swiggy's real-time logistics is one of the hardest engineering problems in India — matching, routing, tracking at massive scale with sub-second decisions. My Kafka and distributed systems work is directly applicable. I want to work on problems where the system design matters as much as the business model."

**Flipkart:**
"Flipkart is Java-first at massive scale. The problems — flash sales, inventory consistency, catalog search — are the kinds of distributed systems challenges I've been preparing for. I want to be in an environment where Java depth is rewarded."

**Goldman Sachs:**
"Goldman's systems need the highest correctness guarantees in the industry. My GSTN experience with financial ledger systems, XA transactions, and audit trails is directly transferable to capital markets systems. I want to work where precision matters more than speed-to-ship."

---

### Negotiation Playbook (SDE-3 Offers)

**Offer anatomy:**
```
FAANG/Top-product offer = Base + RSU (4-year vest) + Annual Bonus + Joining Bonus

Example SDE-3 at Flipkart (2025-2026):
  Base:           ₹45L
  RSU:            ₹30L/year (4-year vest, 1-year cliff)
  Annual bonus:   15% of base = ₹6.75L
  Joining bonus:  ₹10L (one-time)
  Total Year 1:   ₹45L + ₹30L + ₹6.75L + ₹10L = ₹91.75L

Total Comp (TC) Year 2-4: ₹45L + ₹30L + ₹6.75L = ₹81.75L/year
```

**Never reveal your CTC first:**
→ "I'm targeting market rate for this level at a top product company. I'd be happy to evaluate a competitive offer from you."

**Counter-offer script:**
→ "I'm very excited about this role and team. I have [competing offer / other offers in process]. Based on Levels.fyi, the market for this level is [X range]. Can you go to [specific number]?"

**What to negotiate:**
1. Base (hardest to move at large companies)
2. **Joining bonus** (easiest to negotiate, one-time cost for company)
3. **RSU grant** (negotiate cliff — 1-year cliff is standard; ask for partial vest at 6 months if possible)
4. **Title** (SDE-2 vs SDE-3 matters for RSU band and future leverage)

**Do not:**
- Accept on the spot (always: "Can I have 48 hours to review?")
- Reveal competing offer amount (say you have one, not the number)
- Negotiate over email if you can do it by phone (warmer, faster)

---

## PART 2: Database Deep Dive

---

### EXPLAIN / EXPLAIN ANALYZE

```sql
-- Run this on any slow query
EXPLAIN SELECT g.gstin, r.period, r.status
FROM gst_returns r
JOIN gstin_master g ON g.id = r.gstin_id
WHERE r.status = 'PENDING'
ORDER BY r.due_date;

-- Output columns to care about:
-- type: 'ALL' = full table scan (BAD), 'range'/'ref'/'eq_ref' = index used (GOOD)
-- rows: estimated rows scanned — high number = problem
-- Extra: 'Using filesort' = sort not using index (may need composite index)
--        'Using temporary' = temp table created (expensive for large datasets)
--        'Using index' = covering index (great!)

-- EXPLAIN ANALYZE (MySQL 8+) — actually executes and shows real row counts:
EXPLAIN ANALYZE SELECT ...;
```

---

### Index Design — Deep Dive

**B-Tree Index Internals:**
```
B-Tree index = balanced tree of page nodes
Each page: 16KB (MySQL default)
Leaf nodes: contain actual indexed values + primary key (or row pointer)
Non-leaf: guide the search down the tree

Range query: B-Tree does single tree traversal to left bound, then sequential scan of leaf pages
This is why: WHERE created_at BETWEEN '2026-01-01' AND '2026-03-01' is efficient with index on created_at
```

**Composite Index — The Leftmost Prefix Rule:**
```sql
-- Index: (status, due_date, gstin)

-- USES index:
WHERE status = 'PENDING'                               -- leftmost prefix ✓
WHERE status = 'PENDING' AND due_date > '2026-01-01'  -- leftmost prefix + next ✓
WHERE status = 'PENDING' AND due_date > '...' AND gstin = '...' -- full index ✓

-- DOES NOT use index:
WHERE due_date > '2026-01-01'                         -- skips leftmost column ✗
WHERE gstin = '...'                                   -- skips leftmost columns ✗
WHERE status = 'PENDING' AND gstin = '...'            -- skips due_date — partial use only
```

**Covering Index:**
```sql
-- Regular query:
SELECT gstin, status, due_date FROM gst_returns WHERE status = 'PENDING';

-- Without covering index: MySQL reads index → gets PKs → goes back to table for gstin
-- With covering index on (status, due_date, gstin):
--   MySQL reads ONLY the index — never touches the main table
--   "Using index" in EXPLAIN → zero table I/O

CREATE INDEX idx_covering ON gst_returns (status, due_date, gstin);
-- Fastest possible read for this query pattern
```

**When NOT to add an index:**
```
1. Write-heavy tables: every INSERT/UPDATE/DELETE must update all indexes
   → If table has 10 writes/sec and 1 read/sec — skip the index
2. Low cardinality columns: gender ('M'/'F') — index won't help (50% of rows = gender)
   MySQL skips index if estimated rows > ~30% of table
3. Small tables (< 1000 rows): full table scan is faster than index lookup
4. Columns never in WHERE/JOIN/ORDER BY
```

---

### Transaction Isolation Levels — Deep Dive

```
Problem: concurrent transactions reading/writing same data

READ UNCOMMITTED:
  Can see: dirty reads (uncommitted data from other transactions)
  Use: never (or raw analytics where approximate is fine)

READ COMMITTED:
  Prevents: dirty reads
  Can see: non-repeatable reads (same query returns different results in same tx)
  Use: most OLTP systems, PostgreSQL default

REPEATABLE READ:
  Prevents: dirty reads, non-repeatable reads
  Can see: phantom reads (new rows appear in range query)
  Note: MySQL InnoDB default. Uses gap locks to prevent phantoms in most cases.

SERIALIZABLE:
  Prevents: all anomalies. Full isolation.
  Cost: lowest concurrency. Use sparingly.
```

**What each prevents (table):**
| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | ✗ | ✗ | ✗ |
| Read Committed | ✓ | ✗ | ✗ |
| Repeatable Read | ✓ | ✓ | Mostly ✓ (MySQL gap locks) |
| Serializable | ✓ | ✓ | ✓ |

**GSTN context:**
```
Ledger operations (tax credit/debit): use SERIALIZABLE or explicit SELECT FOR UPDATE
  → Cannot allow two transactions to read same ledger balance and both debit it

Return status updates: READ COMMITTED is fine
  → Slight inconsistency in status display is acceptable
```

---

### MySQL InnoDB Internals

**MVCC (Multi-Version Concurrency Control):**
```
InnoDB keeps multiple versions of a row.
A read transaction sees the version that was committed BEFORE its start.
Write transactions create a new version.

Result: reads don't block writes, writes don't block reads.
This is why REPEATABLE READ reads are non-blocking in MySQL.

Each row has hidden columns:
  - DB_TRX_ID: ID of transaction that last modified this row
  - DB_ROLL_PTR: pointer to undo log (previous version)
```

**Clustered Index (InnoDB):**
```
In InnoDB, the primary key IS the clustered index.
Data rows are physically stored in primary key order.
Secondary indexes: store (indexed column value → primary key)
  → Secondary index lookup = find PK in secondary index → find row in clustered index (2 lookups)

Implication: choose PRIMARY KEY carefully
  - AUTO_INCREMENT: sequential inserts, minimal B-tree rebalancing (good)
  - UUID: random inserts, heavy B-tree fragmentation (bad for write-heavy tables)
  - Composite business key (GSTIN + period): semantically meaningful, but larger secondary indexes
```

---

### Window Functions (Must-Know for SDE-3)

```sql
-- ROW_NUMBER: rank within partition
SELECT gstin, period, status,
       ROW_NUMBER() OVER (PARTITION BY gstin ORDER BY filed_at DESC) AS rn
FROM gst_returns;
-- rn=1 = most recent return for each GSTIN

-- RANK: same as ROW_NUMBER but ties get same rank (gaps after ties)
-- DENSE_RANK: same but no gaps

-- LAG / LEAD: access previous/next row's value
SELECT gstin, period, tax_liability,
       LAG(tax_liability, 1) OVER (PARTITION BY gstin ORDER BY period) AS prev_liability,
       tax_liability - LAG(tax_liability, 1) OVER (PARTITION BY gstin ORDER BY period) AS delta
FROM gst_returns;
-- Shows month-over-month change in tax liability per GSTIN

-- SUM running total:
SELECT gstin, period, tax_paid,
       SUM(tax_paid) OVER (PARTITION BY gstin ORDER BY period) AS cumulative_paid
FROM gst_returns;
```

---

### Deadlock Detection and Resolution

```sql
-- Simulate deadlock:
-- Transaction 1: UPDATE returns WHERE id=1; then UPDATE returns WHERE id=2;
-- Transaction 2: UPDATE returns WHERE id=2; then UPDATE returns WHERE id=1;
-- T1 waits for T2 to release id=2. T2 waits for T1 to release id=1. → Deadlock.

-- MySQL auto-detects and kills one transaction (the "victim").
-- Victim gets: ERROR 1213 (40001): Deadlock found when trying to get lock

-- Prevention strategies:
1. Always acquire locks in same order across all transactions
   (T1 and T2 both: id=1 first, then id=2 → no deadlock)
2. Use short transactions (hold locks for minimum time)
3. Optimistic locking: read with version, update WHERE version = read_version
   → No lock held during processing, only at UPDATE

-- Optimistic locking in Spring/Hibernate:
@Entity
public class GstReturn {
    @Version
    private int version; // Hibernate auto-increments, throws OptimisticLockException on conflict
}
```

---

### 20 Database Interview Q&As

**Q: Your query is slow. Walk me through how you'd optimize it.**
→ "EXPLAIN first. Look for type=ALL (full scan). Check rows estimate — if large, needs index. Look for Using filesort or Using temporary — may need composite index on sort column. Add index, re-EXPLAIN. If query plan looks good but still slow — check statistics (ANALYZE TABLE). If table is huge — consider partitioning or archiving old data."

**Q: Difference between optimistic and pessimistic locking.**
→ "Pessimistic: lock on read (SELECT FOR UPDATE), hold until transaction commits. Safe but low concurrency. Optimistic: no lock on read, add WHERE version = ? on update — if version changed, retry. Better concurrency, requires retry logic. Use pessimistic for high-contention data (limited inventory), optimistic for low-contention (user profile updates)."

**Q: How do you handle a table with 1B rows and slow queries?**
→ "First: index audit — are the right columns indexed? Second: partitioning — RANGE partition by date (archive old partitions). Third: archival — move data older than N years to cold storage. Fourth: sharding — distribute by hash of primary key. Fifth: caching — move hot data to Redis. Work through these in order — partitioning often solves it before sharding is needed."

**Q: What is the N+1 problem and how do you fix it?**
→ "N+1: fetching a list of N entities, then making 1 query per entity for related data = N+1 total queries. Fix in JPA: use JOIN FETCH (`SELECT r FROM Return r JOIN FETCH r.items`) or @BatchSize (batch loads related entities). Fix in raw SQL: single JOIN query instead of loop of SELECTs."

**Q: What's the difference between TRUNCATE and DELETE?**
→ "TRUNCATE: removes all rows without logging individual row deletions. DDL operation, cannot be rolled back (in MySQL). Resets AUTO_INCREMENT. Fast. DELETE: DML operation, logs each row deletion, can be rolled back, supports WHERE, triggers fire. Use TRUNCATE to empty a table fast, DELETE to remove specific rows."

---

## PART 3: Golang Deep Dive

---

### Go vs Java Mental Model

| Java | Go | Key difference |
|---|---|---|
| Thread | Goroutine | Goroutines are much lighter (2KB stack vs ~1MB for Java thread) |
| `BlockingQueue` | Channel | Channels are typed, built into language |
| Interface (explicit) | Interface (implicit) | Go: if you implement the methods, you implement the interface |
| Checked exceptions | Error return values | Go: errors are values, not exceptions |
| try-finally | defer | defer runs at function end, even on panic |
| Abstract class | Embedding | Go has no inheritance — compose with embedding |
| `null` | `nil` | Similar but Go is more explicit about nil handling |
| Generic (`<T>`) | Generics (Go 1.18+) | `func Map[T, U any](s []T, f func(T) U) []U` |

---

### Goroutines + Channels

```go
// Goroutine: lightweight concurrent function
go func() {
    fmt.Println("Running in goroutine")
}()

// Channel: typed conduit between goroutines
ch := make(chan int)       // unbuffered — sender blocks until receiver reads
ch := make(chan int, 10)   // buffered — sender blocks only when buffer full

// Producer-Consumer pattern:
func producer(ch chan<- int) { // send-only channel
    for i := 0; i < 5; i++ {
        ch <- i // send
    }
    close(ch) // signal no more values
}

func consumer(ch <-chan int) { // receive-only channel
    for val := range ch { // receives until channel closed
        fmt.Println(val)
    }
}

func main() {
    ch := make(chan int, 5)
    go producer(ch)
    consumer(ch) // runs in main goroutine
}

// Select: multiplex channels (like switch for channels)
select {
case msg := <-ch1:
    fmt.Println("from ch1:", msg)
case msg := <-ch2:
    fmt.Println("from ch2:", msg)
case <-time.After(5 * time.Second):
    fmt.Println("timeout")
}
```

**Goroutine leak — the most common Go bug:**
```go
// LEAK: goroutine blocked on channel forever
func leak() {
    ch := make(chan int)
    go func() {
        val := <-ch // blocks forever if nobody sends
        fmt.Println(val)
    }()
    // function returns, ch goes out of scope, goroutine is stuck forever
}

// FIX: use context for cancellation
func noLeak(ctx context.Context) {
    ch := make(chan int)
    go func() {
        select {
        case val := <-ch:
            fmt.Println(val)
        case <-ctx.Done(): // ctx cancelled → goroutine exits cleanly
            return
        }
    }()
}
```

---

### Context Package — Critical for Go Interviews

```go
// Context propagates: cancellation, deadlines, request-scoped values

// 1. WithCancel — manual cancellation
ctx, cancel := context.WithCancel(context.Background())
defer cancel() // ALWAYS defer cancel to prevent goroutine leak

// 2. WithTimeout — cancel after duration
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// 3. WithDeadline — cancel at specific time
deadline := time.Now().Add(5 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// 4. WithValue — attach request-scoped values (use sparingly)
ctx = context.WithValue(ctx, "requestId", "abc-123")
requestId := ctx.Value("requestId").(string)

// HTTP handler with context propagation:
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context() // already has timeout from server config

    result, err := dbQuery(ctx, "SELECT ...")
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "Request timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, "DB error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(result)
}

// DB query respects context:
func dbQuery(ctx context.Context, query string) (Result, error) {
    rows, err := db.QueryContext(ctx, query) // cancels if ctx done
    // ...
}
```

**Rule:** Context is always the FIRST parameter. Never store context in a struct.

---

### Error Handling

```go
// Go errors are values — return them, don't throw them
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// Error wrapping with context (Go 1.13+):
func processPayment(amount float64) error {
    if err := validateAmount(amount); err != nil {
        return fmt.Errorf("processPayment: %w", err) // %w wraps for unwrapping
    }
    return nil
}

// Unwrap errors:
err := processPayment(-10)
if errors.Is(err, ErrNegativeAmount) { /* exact match or wrapped match */ }

var ve *ValidationError
if errors.As(err, &ve) { /* ve is populated with the wrapped ValidationError */ }

// Custom error type:
type PaymentError struct {
    Amount float64
    Reason string
}
func (e *PaymentError) Error() string {
    return fmt.Sprintf("payment failed for ₹%.2f: %s", e.Amount, e.Reason)
}

// Sentinel errors (predefined, comparable):
var ErrInsufficientFunds = errors.New("insufficient funds")
// Use errors.Is(err, ErrInsufficientFunds) to check

// When to panic:
// ONLY for programmer errors (nil dereference, out-of-bounds, unreachable code)
// NEVER for runtime errors (network, DB, user input) — return error instead
```

---

### Sync Package

```go
import "sync"

// Mutex — mutual exclusion
var mu sync.Mutex
mu.Lock()
defer mu.Unlock()
// critical section

// RWMutex — multiple readers, single writer
var rw sync.RWMutex
rw.RLock()         // acquire read lock (multiple goroutines can hold simultaneously)
defer rw.RUnlock()
// read section

rw.Lock()          // acquire write lock (exclusive)
defer rw.Unlock()
// write section

// WaitGroup — wait for multiple goroutines
var wg sync.WaitGroup
for i := 0; i < 5; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        processItem(id)
    }(i)
}
wg.Wait() // blocks until all Done() called

// Once — run exactly once (singleton initialization)
var once sync.Once
var instance *Config
func GetConfig() *Config {
    once.Do(func() {
        instance = loadConfig()
    })
    return instance
}

// atomic — lock-free operations on simple types
import "sync/atomic"
var counter int64
atomic.AddInt64(&counter, 1)         // increment atomically
val := atomic.LoadInt64(&counter)    // read atomically
atomic.StoreInt64(&counter, 42)      // write atomically
```

---

### HTTP Service in Go

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type User struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
}

// Middleware pattern — function wrapping
func loggingMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next(w, r)
    }
}

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if token != "Bearer valid-token" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next(w, r)
    }
}

// Handler
func getUser(w http.ResponseWriter, r *http.Request) {
    user := User{ID: 1, Name: "Jayanti"}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func main() {
    mux := http.NewServeMux()

    // Apply middleware chain
    mux.HandleFunc("/users", loggingMiddleware(authMiddleware(getUser)))

    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
    }
    log.Fatal(server.ListenAndServe())
}
```

---

### 15 Go Interview Q&As

**Q: What's the difference between a goroutine and an OS thread?**
→ "Goroutines are managed by the Go runtime, not the OS. They start with ~2KB stack (vs ~1MB for OS thread) and grow dynamically. The Go scheduler multiplexes many goroutines onto a smaller number of OS threads (M:N scheduling). Context switching between goroutines is much cheaper than OS thread switching — no kernel mode transition needed."

**Q: How do you prevent goroutine leaks?**
→ "Use context for cancellation — every goroutine that blocks on I/O or channels should also select on ctx.Done(). Buffered channels where appropriate. Close channels when done (signals receivers to stop). Use tools: go test -race catches data races; pprof /debug/pprof/goroutine shows live goroutines."

**Q: Explain how channels work internally.**
→ "A channel is a typed queue with synchronization. Unbuffered: sender blocks until receiver is ready, and vice versa — a rendezvous. Buffered: sender blocks only when buffer is full, receiver blocks only when buffer is empty. Closing a channel signals receivers — receiving from closed channel returns zero value + false. The select statement multiplexes multiple channel operations."

**Q: What is a context and why is it important?**
→ "Context carries request-scoped values, cancellation signals, and deadlines across goroutine boundaries. It's how you implement request timeouts and graceful cancellation. Every IO operation (DB query, HTTP call, Kafka read) should accept and respect a context — when ctx is cancelled, the operation should abort. This is Go's answer to structured concurrency."

**Q: What's the Go memory model?**
→ "Defines when one goroutine is guaranteed to see writes from another. Channel send happens-before channel receive. Mutex unlock happens-before next lock. go statement happens-before goroutine start. Without these synchronization primitives, goroutines can see stale data — race conditions. Use the -race flag in tests to detect data races automatically."

**Q: When would you use a pointer receiver vs value receiver?**
→ "Pointer receiver (*T): when method modifies the receiver, or when receiver is large (avoid copy). Value receiver (T): for small read-only structs, for types that shouldn't be modified. Consistency rule: if any method needs pointer receiver, make all methods pointer receivers."

**Q: How do interfaces work in Go?**
→ "Implicit satisfaction — if your type has all the methods of an interface, it satisfies it. No 'implements' declaration. An interface value is (type, value) pair internally. Interface allows duck typing. Empty interface{} (or any) accepts any type. Type assertion: val.(Type) — panics if wrong type unless using two-value form: val, ok := x.(Type)."

**Q: What is the difference between new() and make()?**
→ "new(T) allocates zeroed memory for type T, returns *T. Used for value types. make(T) initializes slice, map, or channel — returns T (not pointer). These types need internal initialization (length, capacity, hash table structure) before use."

**Q: How does Go handle errors vs exceptions?**
→ "Go treats errors as values. Functions return (result, error). Caller checks error explicitly. No try-catch — errors propagate manually via return. Panic is for unrecoverable programmer errors only. This forces explicit error handling — no silent swallowing like Java's empty catch blocks. Wrap errors with fmt.Errorf('%w', err) to add context while preserving original error for errors.Is/As."

**Q: What is defer and when do you use it?**
→ "defer schedules a function call to run when the surrounding function returns — regardless of how (normal return, panic, runtime error). Used for: cleanup (defer file.Close()), mutex unlock (defer mu.Unlock()), logging at function exit. Multiple defers run in LIFO order. defer captures arguments at the time of defer call, not at execution time."
