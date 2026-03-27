# Behavioral, Database & Golang Questions

## Behavioral Questions

### "Why are you leaving Infosys?"
"I've had great experience at Infosys — 5.5 years building government-scale systems. But I want to work on products where I can see direct user impact and iterate faster. GSTN's release cycles are quarterly; I want to ship weekly. I'm looking for a team where I can grow into a technical leadership role."

### "Where do you see yourself in 3 years?"
"Leading a backend team at a product company, owning a critical system end-to-end — from architecture decisions to production operations. I want to mentor engineers and influence technical direction, not just write code."

### "What's your biggest weakness?"
"I tend to want to understand everything deeply before starting — which sometimes slows me down. I've been actively working on this by timeboxing research phases and building iteratively. My prep system is an example — I could have spent weeks planning the perfect system, but instead I built v1 in a week and iterate daily."

## Database Deep Dive

### Explain ACID properties with examples
- **Atomicity:** All or nothing. GSTN filing submission: if validation fails, the entire transaction rolls back — no partial filing.
- **Consistency:** DB moves from one valid state to another. Constraints (foreign keys, check constraints) prevent invalid data.
- **Isolation:** Concurrent transactions don't interfere. Isolation levels: READ_UNCOMMITTED → READ_COMMITTED → REPEATABLE_READ → SERIALIZABLE. GSTN uses READ_COMMITTED (default) for most queries, SERIALIZABLE for ledger updates.
- **Durability:** Once committed, data survives crashes. Write-ahead log (WAL) ensures this.

### Explain database connection pooling
HikariCP (Spring Boot default). Maintains pool of pre-created connections. Thread takes connection from pool → uses it → returns it. Avoids expensive connection creation per request. GSTN: max pool size 150, connection timeout 5s, idle timeout 30s. The memory leak incident was caused by missing timeout — connections held indefinitely.

## Golang

### Why Go for the workflow engine?
1. **Goroutines:** Lightweight (2KB stack vs 1MB Java thread). Can run thousands for parallel state evaluations.
2. **Static typing:** State machine definition errors caught at compile time.
3. **Single binary:** No JVM startup time, smaller container image, simpler deployment.
4. **Performance:** Lower memory footprint. 60% latency reduction vs Java version.

### Goroutines vs Java threads
Goroutines are multiplexed onto OS threads by Go's scheduler (M:N threading). 2KB initial stack (grows dynamically) vs 1MB fixed Java thread stack. Can run millions vs thousands. Communication via channels (CSP model) instead of shared memory + locks.

### Channel patterns
```go
ch := make(chan Filing, 100) // buffered channel
go func() { ch <- filing }() // send
result := <-ch                // receive

// Select for multiplexing
select {
case f := <-filingCh: process(f)
case <-ctx.Done(): return // cancellation
case <-time.After(5*time.Second): timeout()
}
```

### Context for cancellation
`context.WithTimeout()`, `context.WithCancel()`. Propagate cancellation through goroutine chains. Every GSTN Go service function takes `ctx context.Context` as first parameter.
