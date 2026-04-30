# Interview Preparation Guide — Study Plan & Deep Concepts
### Jayanti Vishnoi | SDE-2 / SDE-3 Target | 5.6 Years GSTN
### How to prepare, what to study, and how to talk about your work confidently

---

## PART 1: THE HONEST FRAMING — How to Talk About Your Role

### The Reality
You worked on a **large, existing system**. You didn't build it from scratch. You implemented **specific CRs (change requests)** that added significant new features to an already complex codebase. This is **normal for 90% of SDE-2/SDE-3 roles** — interviewers know this.

### The Golden Rule
**Never claim you designed the entire system. Instead, claim deep ownership of the features you built WITHIN the system.**

### Three Phrases That Work

| Instead of saying... | Say this... |
|---|---|
| "I designed the whole litigation platform" | "I designed and implemented the subsequent order financial engine — a 12-scenario matrix — within our existing litigation platform" |
| "I built the case management framework" | "I extended the existing case management framework by creating a new customizer for waiver scheme types, proving the framework's extensibility" |
| "I implemented caching and multi-tenant" | "I work within a multi-tenant architecture daily. I built counter APIs for the BO dashboard that leverage the existing two-tier cache and DB routing patterns" |

### When They Ask "Did You Build This From Scratch?"
**Honest answer template:**
> "The [framework/pattern] was already in place when I joined. What I built was [specific feature] using that framework. The complexity wasn't in creating the framework itself — it was in implementing the [12-scenario matrix / 7-order lifecycle / etc.] correctly within it, because each scenario has different financial implications across 3 databases."

This answer:
- Shows honesty (builds trust)
- Redirects to YOUR complexity (which is genuinely hard)
- Demonstrates you understand the bigger picture

---

## PART 2: STUDY PLAN — What to Learn & In What Order

### Week 1: Core Java & Spring Boot (Foundation)

**Study these until you can explain without looking:**

#### Java Core
- [ ] **Generics:** `<T extends Comparable<T>>`, type erasure, bounded wildcards (`? extends`, `? super`)
- [ ] **Collections internals:** HashMap (bucket array → linked list → red-black tree at 8), ConcurrentHashMap (segment locking → CAS), ArrayList vs LinkedList time complexities
- [ ] **Multithreading:** `synchronized` vs `ReentrantLock`, `volatile` (visibility guarantee), `CompletableFuture`, thread pool sizing (CPU-bound vs IO-bound)
- [ ] **Exception handling:** checked vs unchecked, when to use custom exceptions (your code uses `GSTLogicalException` for business errors, `GSTRuntimeException` for system errors)
- [ ] **Streams & Lambdas:** `filter().map().collect()`, `reduce()`, `groupingBy()` — your code uses `transList.stream().filter(itm -> itm.getTransDesc().startsWith("Transfer")).findFirst()`
- [ ] **Memory model:** Stack vs Heap, GC generations (Young → Old), G1GC basics

**Practice:** Explain each concept with an example from YOUR code.
- "We use ConcurrentHashMap in our local cache because multiple request threads read it concurrently"
- "We use streams to filter transaction lists — `transList.stream().filter()` to find transfer entries"

#### Spring Boot
- [ ] **IoC & DI:** `@Component`, `@Service`, `@Repository`, `@Autowired` — constructor injection vs field injection
- [ ] **Bean lifecycle:** `@PostConstruct` (your code uses this for cache loading), `@PreDestroy`
- [ ] **Transaction management:** `@Transactional`, propagation types (REQUIRED, REQUIRES_NEW, NESTED), isolation levels (READ_COMMITTED, REPEATABLE_READ)
- [ ] **AOP:** `@Aspect`, `@Around`, `@Before` — your platform uses GstAopFwk for cross-cutting logging
- [ ] **Profiles & Configuration:** `@Profile`, `@Value`, externalized config (your Properties/ folder)

**How your code uses Spring:**
```
Your WaiverLdgrUpdServiceImpl uses:
  @Service                          → Spring manages lifecycle
  @Transactional(REQUIRED)          → DB transaction boundary
  @Autowired DemandDAO              → DI injects DAO
  
Your ConfigStore uses:
  @PostConstruct                    → Loads 100+ reference types at startup
  
Your AppealValidations uses:
  @Component                        → Shared validation bean injected everywhere
```

---

### Week 2: Design Patterns & Your Code Patterns

**The 6 patterns that appear in your resume (know them COLD):**

#### 1. Strategy Pattern
```
WHAT: Define a family of algorithms, encapsulate each one, make them interchangeable
YOUR CODE: CaseCustomizer interface → AppealCaseCustomizer, AdjudicationCaseCustomizer,
           WaiverSchemeFolderItemCustomizer (YOU created this one)
WHY IT MATTERS: Each case type (appeal, waiver, adjudication) has different lifecycle rules.
           Strategy pattern lets each type have its own logic without polluting others.

INTERVIEW ANSWER:
"We use Strategy pattern for case lifecycle management. The CaseCustomizer interface
defines hooks like beforeCreate() and afterCreate(). Each case type — appeal, waiver,
adjudication — implements these hooks differently. When I added waiver scheme support,
I created WaiverSchemeFolderItemCustomizer implementing the interface. The framework
code didn't change at all — I just added one new strategy class."
```

#### 2. Factory Pattern
```
WHAT: Create objects without exposing creation logic. Client uses factory method.
YOUR CODE: CaseCustomizerFactory.getCustomizer(caseTypeCd) → returns correct strategy
WHY: Runtime resolution — the case type comes from the request, not hardcoded.

INTERVIEW ANSWER:
"CaseCustomizerFactory takes a caseTypeCd string and returns the right CaseCustomizer.
When I onboarded waiver scheme, I added one mapping: 'WAIVER' → WaiverSchemeFolderItemCustomizer.
That's the Factory + Strategy combination — Open/Closed Principle in practice."
```

#### 3. Facade Pattern
```
WHAT: Simplified interface to a complex subsystem
YOUR CODE: CaseHandler is the Facade. It hides CaseService, CaseCustomizerFactory,
           transaction management, validation from the caller.
WHY: Controllers call caseHandler.addCaseFolderItem() — one method. Behind it:
     factory resolution → validation → pre-hook → DB persist → post-hook → notification.

INTERVIEW ANSWER:
"CaseHandler acts as a Facade. The controller calls one method — addCaseFolderItem().
Internally, it resolves the customizer via factory, runs pre-hooks, persists to DB,
runs post-hooks, and triggers notifications. The controller doesn't know any of this."
```

#### 4. Template Method Pattern
```
WHAT: Define skeleton of algorithm in base class, let subclasses override specific steps
YOUR CODE: GenericCaseCustomizer (base class) defines the order of operations.
           Subclasses override specific steps.
WHY: The lifecycle sequence (validate → create → notify) is the same for all case types.
     Only the implementation of each step differs.

INTERVIEW ANSWER:
"GenericCaseCustomizer defines the template: validate, then create, then notify.
Each subclass overrides what's different. AppealCaseCustomizer overrides the create
step to handle appeal-specific demand logic. The sequence is always the same."
```

#### 5. Observer Pattern (Event-Driven)
```
WHAT: When state changes, notify all dependent objects
YOUR CODE: Kafka post-commit events — after order issuance, Kafka message triggers
           email/SMS notifications asynchronously
WHY: Order issuance shouldn't wait for email to send. Decouple via event.

INTERVIEW ANSWER:
"After order issuance commits to DB, we publish a Kafka event. The communication
service consumes it asynchronously and sends email/SMS. The order flow doesn't
wait for notification delivery — if email fails, the order is still valid."
```

#### 6. Double-Entry Ledger Pattern
```
WHAT: Every financial operation creates two entries (debit + credit) that must balance
YOUR CODE: NonReturnLiabLedger — every demand operation creates DR or CR entries.
           Outstanding = Σ(DR) - Σ(CR). Negative = refund due.
WHY: Auditability. You can always reconstruct the demand balance by replaying entries.
     No mutable "balance" field that can get corrupted.

INTERVIEW ANSWER:
"We use a double-entry ledger for all demand financials. When an appeal order is
confirmed, we create a DEBIT entry in the new demand and a REDUCTION entry in the
old demand. Outstanding balance is always computed as sum(debits) minus sum(credits).
If any value goes negative, it means the government owes the taxpayer — we handle
that with Transfer-In/Transfer-Out entries to rebalance."
```

---

### Week 3: Distributed Systems Concepts

**These come up in EVERY SDE-2/SDE-3 interview. Learn them with YOUR examples.**

#### Concurrency Control (YOUR Bullet 2)

**TOCTOU (Time-Of-Check-Time-Of-Use) Race Condition:**
```
PROBLEM:
  Thread A: reads case.status = OPEN → proceeds to issue order
  Thread B: reads case.status = OPEN → proceeds to issue order (SAME CASE)
  Thread A: writes order → sets status = ORDER_ISSUED
  Thread B: writes order → sets status = ORDER_ISSUED (DUPLICATE!)

YOUR SOLUTION (3 layers):
  Layer 1: Redis SETNX (API boundary)
    → SET caseId IF NOT EXISTS, TTL=30s
    → Second request fails fast before any DB work
    → TTL prevents deadlock if holder crashes
    
  Layer 2: JPA @Version (DB layer)
    → Case entity has version field
    → UPDATE cases SET status='ORDER_ISSUED', version=6 WHERE id=123 AND version=5
    → If someone else already made version=6, this affects 0 rows → exception
    
  Layer 3: XA/Atomikos 2PC (cross-DB atomicity)
    → 3 databases must all commit or all rollback
    → Phase 1: PREPARE (all 3 say yes)
    → Phase 2: COMMIT (coordinator tells all 3 to commit)
```

**Study questions to answer:**
- Why not just Redis lock? → If Redis fails, you need a DB-level safety net
- Why not just @Version? → Wasted work — you'd do all the computation before discovering conflict at commit
- Why not Saga? → No acceptable intermediate state. Can't show "order issued" while ledger hasn't updated
- What if coordinator crashes between PREPARE and COMMIT? → Recovery log replay. Atomikos writes to disk before sending COMMIT.

#### CAP Theorem
```
WHAT: In a distributed system, you can have at most 2 of: Consistency, Availability, Partition tolerance
YOUR SYSTEM: CP for financial operations (consistency > availability — better to reject than corrupt data)
             AP for read-heavy dashboard queries (stale counts are acceptable)

INTERVIEW ANSWER:
"For order issuance, we're CP — if the system can't guarantee consistency across
all 3 databases, we reject the operation. For dashboard counters, we're AP —
showing slightly stale counts is fine, availability matters more."
```

#### Database Sharding (YOUR Bullet 4)
```
YOUR APPROACH: 28 state-based shards via AbstractRoutingDataSource
SHARD KEY: stateCd (from GSTIN — first 2 digits)
ROUTING: ThreadLocal → AbstractRoutingDataSource → correct DataSource

Study questions:
- Cross-shard queries? → "Rare. Most operations are state-scoped. For national reports,
  we aggregate shard results asynchronously."
- Hot shard? → "Maharashtra has the most taxpayers. Mitigated by jurisdiction-level
  partitioning within the shard + read replicas for dashboards."
- Rebalancing? → "Not needed yet. 28 shards = 28 states is a natural, stable partition."
```

#### Caching (YOUR Bullet 4)
```
TWO-TIER ARCHITECTURE:
  Tier 1: JVM in-process (@PostConstruct)
    → 100+ reference types: case type codes, status mappings, jurisdiction lists
    → Zero network hop. Loaded once at startup. Never changes mid-request.
    → RISK: Stale data if master changes → mitigated by periodic refresh or restart
    
  Tier 2: Redis distributed (DistCacheFwk)
    → 40+ shared types: session data, cross-instance shared state
    → TTL-based eviction (e.g., 30 min TTL)
    → Network hop but consistent across all instances

Study questions:
- Cache invalidation? → "JVM cache: app restart or scheduled refresh. Redis: TTL eviction.
  For reference data that changes quarterly, TTL of 24h is fine."
- Thundering herd? → "If Redis key expires, all instances hit DB simultaneously.
  Mitigated by jittered TTL (add random seconds) or cache-aside with lock."
- Cache-aside vs read-through? → "We use cache-aside. Application checks cache first,
  on miss goes to DB, then populates cache."
```

---

### Week 4: Database & JPA Deep Dive

#### JPA / Hibernate Concepts You Must Know
```
1. N+1 Problem:
   → Fetching parent entity loads N children with N separate queries
   → YOUR FIX: @EntityGraph or JOIN FETCH in JPQL
   → "In our counter API, I use a single GROUP BY query instead of N separate counts"

2. @Transactional Propagation:
   → REQUIRED (default): join existing or create new
   → REQUIRES_NEW: always new (independent commit/rollback)
   → YOUR CODE: WaiverLdgrUpdServiceImpl uses REQUIRED — joins the outer XA transaction

3. Optimistic vs Pessimistic Locking:
   → Optimistic (@Version): no DB lock, check at commit time. Good for low contention.
   → Pessimistic (SELECT FOR UPDATE): DB lock on read. Good for high contention.
   → YOUR CODE uses optimistic (@Version on Case entity) because order conflicts are rare

4. Entity States:
   → Transient → Persistent (managed) → Detached → Removed
   → YOUR CODE: Case entity is loaded (persistent), modified, and committed within @Transactional

5. Lazy vs Eager Loading:
   → Lazy: load collection only when accessed (default for @OneToMany)
   → Eager: load immediately (default for @ManyToOne)
   → LazyInitializationException if accessing lazy outside transaction
```

#### SQL You Must Know
```
- Indexing: B-tree (range queries) vs Hash (equality). Composite index order matters.
- EXPLAIN plan: How to read it (Seq Scan bad, Index Scan good)
- GROUP BY optimization: Your counter API uses GROUP BY status for efficient aggregation
- Transaction isolation: READ COMMITTED (your system) prevents dirty reads but allows phantom reads
```

---

## PART 3: DOMAIN KNOWLEDGE — The GST Litigation Business

**Interviewers WILL ask "explain the domain." Have a 2-minute pitch ready.**

### The 2-Minute Domain Pitch
```
"I work on India's GST (Goods and Services Tax) platform — GSTN — which serves
15.2 million active taxpayers across 28 state jurisdictions.

My module is Litigation — specifically the Appeal lifecycle. Here's the business flow:

1. Tax officer issues a demand order (DRC-07) saying 'you owe X rupees'
2. Taxpayer disagrees → files first appeal (APL-01) → goes to Appellate Authority
3. Appellate Authority can CONFIRM, MODIFY, or REJECT the demand
4. Each outcome has different financial implications — new demands created,
   old demands closed, balances transferred between demand accounts
5. Taxpayer can also file second-tier appeal (APL-03) → Appellate Tribunal (GSTAT)
6. We also have a Waiver Scheme (SPL01-SPL07) where taxpayers can apply for
   waiver of penalty/interest under special government schemes

The complexity is in the financial engine — each order outcome triggers a chain
of ledger entries (debits, credits, transfers) across multiple demand accounts.
When both appeals are active simultaneously, you get 12 possible outcome
combinations, each with different financial rules."
```

### Key Terms to Know

| Term | What it means | Where you use it |
|---|---|---|
| DRC-07 | Original demand order — "you owe money" | The D1 in your scenarios |
| APL-01 | First appeal application by taxpayer | Appeal case creation |
| APL-03 | Second-tier appeal to Appellate Tribunal | Simultaneous appeal scenario |
| APL-04 | Order passed on appeal (confirm/modify/reject) | Your 12-scenario engine |
| SPL-01 to SPL-07 | Waiver scheme order types | Your waiver lifecycle |
| DRC-03 | Payment challan — evidence of payment | Waiver payment tracking |
| GSTIN | 15-digit taxpayer ID (first 2 = state code) | Shard key for multi-tenant |
| Outstanding | Amount taxpayer still owes = Σ(DR) − Σ(CR) | Core financial calculation |
| Demand Stay | Freeze demand while appeal is being heard | Your admission logic |
| Demand Settled | Outstanding = 0, demand fully paid/closed | Terminal state |

---

## PART 4: SCENARIO WALKTHROUGHS — Practice These Out Loud

### Walkthrough 1: "Walk me through what happens when an appeal is confirmed"

**Practice saying this fluently (60-90 seconds):**

> "When the Appellate Authority passes an order confirming the original demand, here's what my code does:
> 
> First, the system closes the original demand — sets its status to FIRST_APPEAL_ORDER_ISSUED_DEMAND_CLOSED. This is because the appeal order supersedes the original.
> 
> Second, we create a NEW demand with the disputed amount — this is the appeal order's demand (D2). We insert a DEBIT entry in D2's ledger for the full disputed amount.
> 
> Third, we reduce the disputed amount from D1 by inserting a REDUCTION entry. This is the double-entry part — D2 gets a debit, D1 gets a corresponding credit.
> 
> Fourth, we check D1's outstanding balance. If any minor head (IGST tax, interest, penalty, fee, other — 20 fields total across 4 tax types) goes negative, it means the taxpayer overpaid on D1. We transfer that negative balance from D1 to D2 using Transfer-Out (from D1) and Transfer-In (to D2) entries.
> 
> If this is a SIMULTANEOUS appeal (both APL01 and APL03 active), we also credit the admitted pre-deposit amount from D1 to D2.
> 
> All of this happens in a single XA transaction across 3 databases — if any step fails, everything rolls back."

### Walkthrough 2: "What happens when a void order (SPL06) is issued?"

> "SPL06 voids a previously approved waiver. Here's the flow:
> 
> The waiver approval (SPL05) had inserted a REDUCTION_TRANS credit entry that reduced the taxpayer's outstanding demand. The void order needs to reverse this.
> 
> First, we insert a compensating DEBIT_TRANS entry — this reverses the credit from SPL05, restoring the outstanding balance to what it was before the waiver.
> 
> Second, we restore the demand status. We don't hardcode a status — we read from `origOrdDmdStatusBfrSpl06`, which stores the exact status the demand was in before the waiver was applied. This is important because the demand could have been in any state — CREATED, FIRST_APPEAL_ISSUED, RECTIFICATION_ISSUED — and we need to restore exactly that state.
> 
> Third, we update the recovery case status to RECOVERABLE, because the waiver is now void and the demand is active again.
> 
> This is a classic compensating transaction pattern — instead of deleting the original credit, we add a counterbalancing debit. This preserves the full audit trail."

### Walkthrough 3: "How does your multi-tenant routing work?"

> "We serve 28 state jurisdictions, each with its own database shard.
> 
> At the API layer, every request carries a state code — either from the GSTIN (first 2 digits) or explicitly in the request header.
> 
> In the controller, I call `DbContextHolder.setDbType(stateCd)`. This stores the state code in a ThreadLocal variable — so it's scoped to the current request thread.
> 
> Spring's AbstractRoutingDataSource has a method called `determineCurrentLookupKey()` which reads that ThreadLocal. Based on the value, it routes to the correct DataSource — the connection pool for that state's database.
> 
> In the finally block, I call `DbContextHolder.clearDbType()`. This is CRITICAL in a thread-pooled server like Tomcat — if I don't clear it, the next request that reuses this thread will be routed to the wrong state's database.
> 
> This is a classic request-scoped context propagation pattern using ThreadLocal."

---

## PART 5: TOUGH QUESTIONS & HOW TO HANDLE THEM

### Q: "Why didn't you use [X technology] instead?"

**Template:** "We evaluated [X], but chose [Y] because [specific trade-off]. [X] would have been better for [scenario], but our use case was [scenario]."

| Question | Answer |
|---|---|
| "Why XA 2PC instead of Saga?" | "Saga requires compensating transactions and accepts intermediate states. For legal tax orders, we can't have a state where the order is issued but the ledger isn't updated — that's a compliance violation. XA gives us atomicity at the cost of latency, which is acceptable for low-frequency order issuance (not high-throughput)." |
| "Why Redis lock instead of DB lock?" | "DB-level pessimistic locks (SELECT FOR UPDATE) work within a single DB. Our check spans multiple databases and services. Redis provides a cross-instance, cross-service distributed lock. Plus, we fail fast at the API boundary before doing expensive DB work." |
| "Why ThreadLocal instead of request attribute?" | "Both work. ThreadLocal is cleaner for framework code that doesn't have access to HttpServletRequest — like our AbstractRoutingDataSource. It's a well-established Spring pattern." |
| "Why JVM cache and Redis, not just Redis?" | "Reference data (case types, status codes) never changes during a request. JVM cache gives zero network latency for these. Redis adds 1-2ms per call — for 100+ reference lookups per request, that's 100-200ms wasted network time." |

### Q: "What was the hardest bug you faced?"

**Have 2-3 real stories ready. Structure: Problem → Investigation → Root Cause → Fix → Learning.**

**Example story (ThreadLocal leak):**
> "We had a production issue where some requests were hitting the wrong state's database — an officer in Maharashtra was seeing Karnataka's data.
> 
> Investigation: It only happened under load, not in dev. That pointed to a thread-pool issue.
> 
> Root cause: A new endpoint was missing `DbContextHolder.clearDbType()` in its finally block. Under load, Tomcat reuses threads. Thread 5 serves Maharashtra, sets ThreadLocal to MH. If clearDbType isn't called, the next request on thread 5 goes to MH regardless.
> 
> Fix: Added clearDbType() in finally block. Also added a servlet filter that automatically clears ThreadLocal after every request as a safety net.
> 
> Learning: ThreadLocal in thread-pooled servers is dangerous. Always clear in finally, and add framework-level safety nets."

### Q: "What would you do differently if you were redesigning this?"

> "Three things:
> 1. **Event sourcing for the ledger** — instead of computing outstanding from sum of entries every time, maintain a materialized view. The double-entry ledger is already an event log; we just don't have the projection layer.
> 2. **Replace XA 2PC with Saga + Outbox** for non-critical flows — XA has scalability limits. For things like email notifications, Saga with an outbox pattern would be more resilient.
> 3. **Better observability** — structured logging with correlation IDs across all 3 databases so we can trace a single order issuance through all its ledger entries."

---

## PART 6: CONCEPTS CHEAT SHEET — Quick Revision Before Interview

### SOLID Principles (With YOUR Examples)
```
S - Single Responsibility
    AppealValidations → only validation logic
    AppealOrderItemCustomizer → only order processing logic
    
O - Open/Closed
    CaseCustomizer framework → open for extension (new customizer),
    closed for modification (CaseHandler doesn't change)
    YOUR PROOF: WaiverSchemeFolderItemCustomizer added, zero framework changes
    
L - Liskov Substitution
    Any CaseCustomizer implementation can replace another
    CaseHandler doesn't care which specific customizer it's calling
    
I - Interface Segregation
    CaseCustomizer (case-level hooks) vs CaseFolderItemCustomizer (item-level hooks)
    Not one giant interface
    
D - Dependency Inversion
    CaseHandler depends on CaseCustomizer interface, not AppealCaseCustomizer concrete class
    Factory resolves at runtime
```

### Transaction Concepts
```
ACID:
  Atomicity    → XA 2PC ensures all-or-nothing across 3 DBs
  Consistency  → Demand Outstanding = Σ(DR) - Σ(CR) always holds
  Isolation    → @Transactional(isolation = READ_COMMITTED)
  Durability   → DB commit = persisted to disk

Distributed Transaction Patterns:
  2PC (yours)  → Coordinator + Participants, PREPARE/COMMIT
  Saga         → Sequence of local transactions + compensating actions
  Outbox       → Write event to DB table, separate process publishes to Kafka
  
When to use which:
  2PC   → Strong consistency needed, low throughput (your order issuance)
  Saga  → High throughput, eventual consistency OK (e-commerce checkout)
  Outbox → Reliable event publishing without 2PC overhead
```

### Caching Patterns
```
Cache-Aside (yours):
  App checks cache → miss → query DB → put in cache → return
  
Read-Through:
  App asks cache → cache queries DB on miss → returns
  
Write-Through:
  App writes to cache → cache writes to DB → return
  
Write-Behind:
  App writes to cache → cache asynchronously writes to DB (eventual)
  
YOUR SYSTEM:
  JVM cache = cache-aside, populated at @PostConstruct
  Redis cache = cache-aside via DistCacheFwk
```

### Microservice Communication
```
Synchronous (REST):
  Your system uses REST between modules (LitigationAPI → LedgerAPI)
  Trade-off: Simple but coupling + latency chain
  
Asynchronous (Kafka):
  Your system uses Kafka for post-commit events (notifications)
  Trade-off: Decoupled but eventual consistency
  
YOUR ANSWER when asked "sync vs async":
"We use sync REST for operations that need immediate consistency — like ledger
updates during order issuance. We use async Kafka for operations where eventual
delivery is fine — like email notifications after order is committed."
```

---

## PART 7: DAILY STUDY SCHEDULE (4 Weeks)

| Day | Morning (1.5 hr) | Evening (1.5 hr) |
|---|---|---|
| **Week 1** | | |
| Mon | Java Collections internals | Practice: explain HashMap to a whiteboard |
| Tue | Java Concurrency (synchronized, locks, volatile) | Practice: explain TOCTOU with your Redis example |
| Wed | Java Streams & Lambdas | Practice: write 5 stream operations from your code |
| Thu | Spring Boot DI, Bean lifecycle, @PostConstruct | Practice: draw your ConfigStore loading flow |
| Fri | Spring @Transactional, propagation, isolation | Practice: explain XA 2PC with your 3 DB example |
| Sat | Revision: Java + Spring Boot concepts | Practice: explain all 5 resume bullets out loud |
| Sun | Read Resume_Bullets_Explainer.md end-to-end | Mock: record yourself explaining Bullet 1 |
| **Week 2** | | |
| Mon | Design Patterns: Strategy, Factory (with your code) | Practice: draw CaseCustomizerFactory flow |
| Tue | Design Patterns: Facade, Template Method, Observer | Practice: explain CaseHandler as Facade |
| Wed | SOLID Principles with your examples | Practice: explain Open/Closed with WaiverScheme |
| Thu | Double-entry ledger: DR, CR, outstanding calculation | Practice: walk through confirm-reject scenario |
| Fri | Compensating transactions, idempotency | Practice: walk through SPL06 void scenario |
| Sat | JPA: N+1, lazy/eager, @Version, entity states | Practice: explain optimistic locking with Case entity |
| Sun | Revision: all patterns + read Explainer.md again | Mock: record yourself explaining Bullets 2 & 3 |
| **Week 3** | | |
| Mon | Distributed systems: CAP, consistency models | Practice: explain CP vs AP for your system |
| Tue | Caching: patterns, invalidation, thundering herd | Practice: explain two-tier cache design |
| Wed | Database: indexing, sharding, partitioning | Practice: explain 28-shard routing with ThreadLocal |
| Thu | Kafka: producers, consumers, partitions, offsets | Practice: explain post-commit notification flow |
| Fri | System Design: URL shortener or rate limiter | Practice: draw HLD with boxes and arrows |
| Sat | System Design: design a litigation case mgmt system | Practice: use your own system as the answer |
| Sun | Revision: distributed systems | Mock: record Bullets 4 & 5 |
| **Week 4** | | |
| Mon | Tough questions practice (Part 5 of this doc) | Mock: "Why not Saga?", "Hardest bug?" |
| Tue | Domain knowledge pitch (2-minute pitch) | Mock: explain GST litigation to a non-tech person |
| Wed | Code walkthrough: read AppealOrderItemCustomizer | Mock: "Walk me through updateDemandStatus()" |
| Thu | Code walkthrough: read WaiverSchemeFolderItemCustomizer | Mock: "Walk me through waiver approval flow" |
| Fri | Full mock: all 5 bullets + 10 tough questions | Mock: 45-minute simulated interview |
| Sat | Weak areas revision | Finalize 3 "hardest bug" stories |
| Sun | Light review, rest, confidence building | Read Resume_Bullets_Final.md one last time |

---

## PART 8: THE 10 MOST LIKELY INTERVIEW QUESTIONS (With Your Answers)

### 1. "Tell me about a complex system you've worked on."
→ Use the 2-minute domain pitch (Part 3) + transition to Bullet 1

### 2. "What's the most technically challenging thing you've built?"
→ Bullet 1 (12-scenario engine). "The complexity wasn't just the number of scenarios — it was ensuring financial correctness across all of them. Each scenario has different ledger entries, and the outstanding balance must always equal sum of debits minus sum of credits."

### 3. "How did you handle concurrency?"
→ Bullet 2 (3-layer defense). Walk through Redis → @Version → XA.

### 4. "How do you handle errors and edge cases?"
→ SPL06 void order story. "We don't delete the approval credit — we add a compensating debit. This preserves audit trail. And we snapshot the original status before waiver so we can restore it exactly, not guess."

### 5. "Describe a design pattern you've used in production."
→ Strategy + Factory. CaseCustomizer → CaseCustomizerFactory. "Proof: I onboarded waiver scheme with zero framework changes."

### 6. "How do you design for scalability?"
→ Bullet 4. Multi-tenant sharding + two-tier cache + counter API design.

### 7. "Have you worked with distributed transactions?"
→ Bullet 2. XA/Atomikos 2PC. Explain the 3 databases, PREPARE/COMMIT phases, and why Saga doesn't work for legal orders.

### 8. "How do you ensure data consistency?"
→ Double-entry ledger + idempotency guards (check status != SETTLED before write) + XA atomicity.

### 9. "What would you improve about your current system?"
→ Event sourcing for ledger, Saga + Outbox for non-critical flows, structured observability with correlation IDs.

### 10. "Walk me through a code flow end-to-end."
→ Use Walkthrough 1 or 2 from Part 4. Practice until you can do it in 90 seconds.

---

## PART 9: CONFIDENCE BUILDERS

### Things You Genuinely Know Better Than Most SDE-2 Candidates
1. **Financial domain** — most devs have never implemented double-entry ledger accounting
2. **Multi-database transactions** — most devs only work with one DB per service
3. **State machine complexity** — 12 scenarios with inter-dependent financial outcomes is rare
4. **Government-scale platform** — 15.2M taxpayers, 28 jurisdictions, legal compliance
5. **Plugin architecture in production** — you've seen Strategy+Factory work at scale with 20+ types

### What Makes Your Experience Unique
- You didn't just "use Spring Boot" — you implemented complex financial logic WITHIN Spring Boot
- You didn't just "use Redis" — you used it for distributed mutual exclusion
- You didn't just "write APIs" — you wrote APIs that create immutable financial audit trails
- You didn't just "extend a framework" — you proved the framework's extensibility by onboarding an entirely new business domain

### Final Mindset
> **You are not claiming to be the architect of the whole platform. You are claiming to be the engineer who implemented the hardest recent features — subsequent orders (12 scenarios), waiver lifecycle (7 order types), and the financial engine underneath both. That is 95 files of complex, production-grade, financially-correct code. That is SDE-2/SDE-3 work.**

---

*Last Updated: April 2026*
*Companion to: Resume_Bullets_Final.md (v2) + Resume_Bullets_Explainer.md*
