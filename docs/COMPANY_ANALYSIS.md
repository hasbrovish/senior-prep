# SDE-2/SDE-3 Company Analysis — Backend Focus
# Top 100+ Companies: Interview Format, Expectations, Salary, Pass Rates
# Based on 2024–2026 interview data (Glassdoor, Blind, Leetcode Discuss, company blogs)
# Jayanti's Profile: 5.5 YOE | GSTN | Java, Spring Boot, Kafka, Redis, Golang

---

## HOW TO USE THIS DOCUMENT

```
PHASE 1 (Months 1–3): Focus on Tier 3 + Tier 2 companies.
PHASE 2 (Months 4–6): Focus on Tier 1 + Tier 2 companies.

This document tells you:
  1. What each tier asks (DSA level, SD depth, Java depth)
  2. Which companies to prioritise given YOUR stack
  3. Realistic pass rates (overestimating kills prep, underestimating kills motivation)
  4. What skills ACTUALLY matter vs what you think matter
  5. How to use your GSTN experience as an asset at each tier
```

---

## OVERALL SKILLS MAP — What You Need at Each Tier

| Skill             | Tier 3 (Phase 1) | Tier 2 (Phase 2 early) | Tier 1 (Phase 2 peak) |
|---|---|---|---|
| DSA               | LeetCode Easy-Medium | Medium, some Hard | Medium-Hard, timed |
| System Design     | Mid-scale, 1 component deep | Multi-component, trade-offs | Full distributed, bottlenecks |
| LLD               | 1 design problem | 2 design problems | Clean OOP, SOLID, patterns |
| Java Depth        | Spring Boot, Transactional, basics | Concurrency, JVM basics | JVM internals, GC tuning, lock escalation |
| Behavioral        | 3 STAR stories | 6 STAR stories | 14 Amazon LPs mapped |
| Golang            | Not required | Nice to have | Required at Google/Uber |

---

## TIER 1 — Dream Roles | Hardest | Highest Pay
### Pass Rate: 3–12% from application to offer

These companies run 4–6 rounds. DSA is eliminatory. System design must show distributed thinking.
Your GSTN experience is relevant but must be framed in product engineering language.

---

### 1. Google (SWE L4 / L5)
**Rounds:** 1 Phone screen → 5 onsite (2 DSA + 1 SD + 1 Googleyness/Behavioral + 1 varies)
**DSA:** Hard. Clean code + optimal solution expected. Always ask for complexity.
**System Design:** Distributed systems at massive scale (Bigtable, Spanner, Borg concepts help)
**Java:** Not Java-specific. Golang preferred for some teams.
**Behavioral:** "Googleyness" — collaborative, humble, curious
**Salary (India L4):** ₹40–80L base + RSU ₹80–200L over 4 years
**Pass rate from apply:** ~3–5%
**Your edge:** Kafka distributed processing at national scale, HBase data access patterns
**Weakness to fix:** DSA Hard level + Golang fluency
**Tip:** Google cares about algorithmic elegance. Brute force + "can you optimize?" is their pattern.

---

### 2. Meta (SWE E4/E5) — limited India presence, Hyderabad team
**Rounds:** Recruiter screen → 2 coding + 1 SD + 1 Behavioral
**DSA:** Medium-Hard. Focus on arrays, strings, graphs, DP.
**System Design:** Product-focused (social graph, feed systems, messaging at scale)
**Behavioral:** "How do you move fast?" — Meta loves execution speed
**Salary:** Similar to Google India
**Pass rate:** ~4–6%
**Your edge:** Event-driven architecture, async processing
**Tip:** Meta explicitly wants candidates who have shipped high-impact features. Frame GSTN as "serving 14M users with < 2s SLA during peak."

---

### 3. Microsoft (SDE-2 / SDE-3) — Hyderabad is large centre
**Rounds:** HR screen → 4 technical (2 DSA + 1 SD + 1 PM/Behavioral)
**DSA:** Medium level. Sometimes easier than Amazon. Focus on trees, arrays, OOP.
**System Design:** Azure-flavored but general SD knowledge works
**Java:** Not Java-specific. C#/Java/Python all acceptable.
**Behavioral:** Growth mindset ("What did you learn?"), collaboration
**Salary (SDE-2):** ₹30–55L base + RSUs
**Pass rate:** ~8–12%
**Your edge:** Microservices, distributed caching — Microsoft Teams/Azure teams love this
**Tip:** Microsoft rounds often have "design a component" not full system design — focus on API design + data model.

---

### 4. Amazon (SDE-2) — Largest FAANG hiring in India
**Rounds:** OA (2 coding + work simulation) → Phone screen → 4-5 onsite
**DSA:** Medium. Arrays, trees, graphs, DP. Amazon OA is hackerrank-style.
**System Design:** Scalable, highly available. "Amazon scale" thinking.
**Behavioral:** 14 Leadership Principles. Non-negotiable. Every round has LP questions.
**Java:** Spring Boot, concurrency — asked at SDE-2 level
**Salary (SDE-2 Bangalore):** ₹35–65L base + ₹60–120L RSU over 4 years
**Pass rate from OA to offer:** ~10–15%
**Your edge:** Distributed systems, idempotency, Kafka DLQ — Amazon loves resilience patterns
**Must prep:** Map your 6 STAR stories to LP: Ownership, Dive Deep, Deliver Results, Customer Obsession
**Tip:** Amazon hiring bar varies hugely by team. Retail tech easier; AWS, Advertising harder.

---

### 5. Flipkart (SDE-2 / SDE-3) — India's strongest product company
**Rounds:** OA → 4-5 technical rounds (2 DSA + 1 LLD + 1 HLD + 1 Managerial)
**DSA:** Medium-Hard. Java-specific implementation often expected.
**System Design:** E-commerce scale (catalog, inventory, order mgmt, flash sales)
**LLD:** Heavy. Parking lot, hotel booking, inventory system.
**Java:** Deep. Concurrency, Collections internals, GC, design patterns.
**Behavioral:** Product mindset + execution under scale
**Salary (SDE-2 Bangalore):** ₹35–60L total
**Pass rate:** ~8–12%
**Your edge:** Your distributed caching + workflow engine maps perfectly to Flipkart's tech
**Tip:** Flipkart is Java-first. Prepare for "implement this in Java, walk me through your design choices."

---

### 6. Goldman Sachs (SDE-2 / Associate)
**Rounds:** HireVue video → 3–4 technical (Java coding + concurrency + system design)
**DSA:** Medium. Less focus on algorithmic tricks, more on implementation correctness.
**Java:** DEEPEST Java questions in any company. JVM, GC, lock internals, off-heap.
**System Design:** Financial domain: ledger systems, trading systems, order matching.
**No behavioral round** in most cases (rare LP-style questions)
**Salary (SDE-2 Bangalore):** ₹35–65L + bonus (15–40% variable is significant)
**Pass rate:** ~10–15%
**Your edge:** GSTN tax ledger = financial domain. XA transactions + distributed consistency.
**Must know:** Biased lock → thin lock → fat lock escalation. G1GC concurrent marking. ReentrantLock vs synchronized internals.
**Tip:** Goldman asks "How would you improve this code?" on live Java code. Practice code review aloud.

---

### 7. Morgan Stanley (SDE-2 / Technology Analyst)
**Rounds:** Similar to Goldman — 3–4 rounds, Java-heavy
**DSA:** Medium. Data structures focused.
**Java:** Deep concurrency (same level as Goldman)
**System Design:** Risk calculation, order management, real-time data pipelines
**Salary:** ₹30–55L + bonus
**Pass rate:** ~12–18%
**Your edge:** Same as Goldman — financial data + GSTN ledger maps perfectly

---

### 8. Zerodha (Backend Engineer)
**Rounds:** Unique process — technical assessment + culture fit + deep work sample
**DSA:** Less formal DSA. More problem-solving with their actual tech challenges.
**Tech:** Go (Golang) is primary language. Python secondary.
**System Design:** Trading systems, order books, real-time portfolio calculation
**Salary:** ₹25–50L (not FAANG money but extraordinary work quality)
**Pass rate:** ~5–8% (very selective culture fit)
**Your edge:** Golang experience at GSTN is critical here
**Tip:** Zerodha hires for depth over breadth. Show you've read their engineering blog (Rainmatter Foundation, Kite blog).

---

## TIER 2 — Top Product Companies | Strong but Reachable
### Pass Rate: 12–25% from first technical round to offer

These companies run 3–4 rounds. Mid-level DSA is sufficient. Strong SD + depth on past work wins.

---

### 9. PhonePe (SDE-2 Backend)
**Stack:** Java, Spring Boot, Kafka, MySQL, Redis — IDENTICAL to your GSTN stack
**Rounds:** OA → 2-3 technical + 1 managerial
**DSA:** Medium. Not as heavy as FAANG.
**System Design:** Payments: UPI rails, wallet, ledger, idempotency, reconciliation
**Java:** Spring Boot + concurrency medium depth
**Salary:** ₹30–55L
**Pass rate:** ~15–20%
**Your edge:** Your stack is literally their stack. Your GSTN ledger IS a payments ledger.
**MUST FRAME:** "At GSTN, I built distributed ledger operations for tax credit settlement across 14M taxpayers — this is conceptually identical to payment settlement in UPI."
**Tip:** PhonePe loves idempotency, retry patterns, distributed consistency. Nail these.

---

### 10. Razorpay (SDE-2 Backend)
**Stack:** Java, Golang, Kafka, MySQL
**Rounds:** Take-home assignment → 3 technical + 1 HR
**DSA:** Medium. Sometimes take-home instead of whiteboard.
**System Design:** Payment gateway, payout systems, webhook delivery, reconciliation
**Salary:** ₹28–50L
**Pass rate:** ~15–22%
**Your edge:** Same as PhonePe. Financial domain + your stack.
**Tip:** Razorpay interviews often include a take-home assignment. Treat it like a production PR.

---

### 11. Swiggy (SDE-2 / SDE-3 Backend)
**Stack:** Java, Golang, Kafka, Cassandra, Redis
**Rounds:** OA → 3-4 technical rounds
**DSA:** Medium-Hard. Graphs are common (delivery routing!).
**System Design:** Real-time order tracking, delivery partner assignment, surge pricing, catalog
**Product round:** "How would you improve Swiggy's search?" — product thinking
**Salary:** ₹28–55L
**Pass rate:** ~15–20%
**Your edge:** Event-driven architecture, Kafka consumer patterns
**Tip:** Swiggy asks "Why do you want to work at Swiggy?" seriously. Know their product.

---

### 12. Zomato (SDE-2 Backend)
**Similar to Swiggy.** Slightly easier DSA bar.
**Salary:** ₹25–50L
**Pass rate:** ~18–25%
**Tip:** Zomato values product-first thinking. Frame your GSTN work as: "I built backend systems that directly impacted millions of end-users."

---

### 13. CRED (SDE-2 Backend)
**Stack:** Kotlin/Java, Golang, Kafka, PostgreSQL
**Rounds:** 3-4 rounds, culture-fit heavy
**DSA:** Medium
**System Design:** Credit card management, rewards engine, payment flows
**Salary:** ₹28–50L + ESOPs
**Pass rate:** ~18–25%
**Tip:** CRED is design-quality-obsessed. Show your code is clean and your thinking is structured.

---

### 14. Juspay (SDE-2 Backend)
**Stack:** Haskell/Purescript/Java — unusual but Java backend exists
**Rounds:** 3 rounds: DSA + System Design + Behavioral
**DSA:** Medium
**System Design:** Payment orchestration, routing, retry, idempotency
**Salary:** ₹25–45L
**Pass rate:** ~20–28%
**Your edge:** Payments domain knowledge from GSTN

---

### 15. Meesho (SDE-2 Backend)
**Stack:** Java, Spring Boot, MySQL, Kafka
**Rounds:** 3-4 rounds
**DSA:** Medium
**System Design:** E-commerce for Tier 2/3 India — catalog, orders, seller platform
**Salary:** ₹25–45L
**Pass rate:** ~20–28%
**Tip:** Meesho values scale on low-cost infra. Frame your GSTN government infra constraints as a positive.

---

### 16. Uber India (SDE-2)
**Stack:** Java, Go, distributed systems
**Rounds:** 4-5 rounds including system design
**DSA:** Medium-Hard
**System Design:** Maps, routing, matching, surge, payments
**Salary:** ₹35–60L
**Pass rate:** ~10–18%

---

### 17. Atlassian (SDE-2) — Bengaluru
**Rounds:** 4-5 rounds, values-heavy
**DSA:** Medium. Not the hardest.
**System Design:** Collaboration tools scale (Jira, Confluence)
**Behavioral:** "Ship it" + "open company, no bullshit" values — must research
**Salary:** ₹35–65L + RSUs (Atlassian stock has been volatile)
**Pass rate:** ~15–20%
**Tip:** Atlassian does a "values interview" round. Research their 5 values. They will literally ask "Tell me about a time you demonstrated [value]."

---

## TIER 3 — Phase 1 Targets | Achievable with Current Prep
### Pass Rate: 25–45% — These should be your first callbacks

---

### 18–30. Phase 1 Target Companies

| Company | Stack | DSA Level | SD Level | Salary Range | Notes |
|---|---|---|---|---|---|
| Walmart Global Tech | Java | Medium | Mid | ₹22–40L | Good for first offer. Values reliability. |
| ThoughtWorks | Java/Any | Easy-Medium | Mid | ₹18–35L | Code quality + pairing culture |
| Publicis Sapient | Java | Easy-Medium | Basic | ₹18–32L | Good stepping stone |
| Nagarro | Java | Easy | Basic | ₹16–28L | High callback rate |
| Persistent Systems | Java | Easy-Medium | Mid | ₹18–30L | Strong Java focus |
| MakeMyTrip | Java | Medium | Mid | ₹22–40L | Travel domain, good culture |
| OLA (Ola Cabs) | Java/Go | Medium | Mid | ₹22–40L | Post-IPO stabilising |
| Paytm | Java | Medium | Mid | ₹20–38L | Fintech + payments align |
| Browserstack | Java/Go | Medium | Mid | ₹25–45L | SaaS, good engineering culture |
| Freshworks | Java | Medium | Mid | ₹22–40L | SaaS, structured interviews |
| Nykaa | Java | Easy-Medium | Basic | ₹18–32L | Growing tech team |
| Urban Company | Java | Medium | Mid | ₹20–35L | Hyperlocal, growing |
| Dunzo (if still hiring) | Go/Java | Medium | Mid | ₹18–30L | Delivery + logistics |

---

## WHAT ACTUALLY GETS YOU REJECTED (Real Data)

### DSA Round
```
Most common fail reasons at SDE-2 level:
1. Cannot code BFS/DFS from scratch without hints (asked at 80% of companies)
2. Brute force only — cannot optimize when prompted (asked at 90%)
3. Off-by-one errors in binary search (surprisingly common)
4. Cannot explain time/space complexity verbally
5. Solving unfamiliar DP in 45 min without pattern recognition

Fix: 150 problems done > 300 problems barely attempted.
     10 core patterns mastered > 50 patterns superficially known.
```

### System Design Round
```
Most common fail reasons:
1. Jumping to solution without clarifying requirements (eliminated at FAANG)
2. Can describe components but cannot explain WHY each component (trade-offs)
3. Cannot estimate: "How many servers would you need?"
4. Never mentions failure modes, retries, idempotency
5. Cannot go deep on ONE component when interviewer probes

Fix: Use the 5-step framework EVERY TIME:
     Requirements → Scale → High-level → Deep dive → Failure
```

### Java/Technical Round
```
Most common fail reasons:
1. Cannot explain their OWN code under scrutiny
2. Knows @Transactional works, cannot explain what happens at JVM level
3. Cannot explain the difference between Thread.sleep() and wait()
4. Good theory but cannot write a working Kafka consumer from memory
5. Over-relies on Spring magic without understanding internals

Fix: Explain EVERY concept you've written as if teaching a junior.
```

### Behavioral Round
```
Most common fail reasons:
1. Vague stories ("we built a system" vs specific impact with numbers)
2. No conflict or challenge — everything went smoothly (unbelievable)
3. Cannot explain trade-off decisions clearly
4. No "I" statements — team credit without personal contribution
5. Defensive when interviewer challenges your past decisions

Fix: Every story needs: Situation → Specific Action → Measurable Result
     "reduced latency by 40%" > "improved performance significantly"
```

---

## DSA SKILLS REQUIRED BY TIER

### Tier 3 (Phase 1 — Must be solid before applying)
- Arrays, Strings: Two Sum, Sliding Window, Two Pointers ✓
- Linked Lists: Reverse, Merge, Cycle detection ✓
- Stacks/Queues: Valid Parentheses, Min Stack ✓
- Binary Search: Basic + "binary search on answer" ✓
- Trees: BFS, DFS, Level Order, Path Sum ✓
- HashMap problems: Group Anagrams, Frequency count ✓
- **Target: 50 problems (mostly Easy-Medium)**

### Tier 2 (Phase 2 early)
Everything in Tier 3 PLUS:
- Graphs: BFS/DFS, cycle detection, topological sort, Dijkstra ✓
- Dynamic Programming: 1D (house robber, climbing stairs) + 2D (LCS) ✓
- Heap/Priority Queue: Top-K, median, task scheduler ✓
- Backtracking: Subsets, Permutations, Combination Sum ✓
- LRU Cache implementation in code ✓
- **Target: 100 problems (Medium majority)**

### Tier 1 (Phase 2 peak)
Everything above PLUS:
- Hard DP: Edit distance, distinct subsequences, burst balloons
- Hard Graphs: Alien dictionary, network delay, swim in rising water
- Design problems: LFU Cache, Twitter, Autocomplete
- Interval problems: Merge, non-overlapping, minimum arrows
- String matching: Minimum window, substring with concatenation
- **Target: 150+ problems (30%+ Hard)**

---

## SYSTEM DESIGN EXPECTATIONS BY TIER

### Tier 3 — Mid-scale thinking
- Design a URL Shortener (hashing, redirection, analytics)
- Design a Rate Limiter (token bucket, sliding window)
- Design a Job Queue (priority, retry, DLQ)
- Design a Notification System ← you built this at GSTN
- **Not expected:** Google/Twitter scale, global distribution

### Tier 2 — Multi-service + trade-offs
- All Tier 3 designs PLUS:
- Design a Payment Gateway (idempotency, distributed transactions)
- Design a Food Delivery System (tracking, assignment, surge)
- Design a Messaging System (WebSocket, delivery guarantees)
- Design a Product Catalog (search, inventory, consistency)
- **Expected:** Trade-off discussion, failure handling, basic capacity estimation

### Tier 1 — Full distributed system
- All Tier 2 PLUS:
- Design Twitter/Instagram (fan-out on write vs read, CDN, ranking)
- Design Google Drive (chunked upload, versioning, conflict resolution)
- Design Uber (geospatial, matching, surge pricing)
- Design WhatsApp (WebSocket, message ordering, multi-device sync)
- Design a Distributed Rate Limiter / Key-Value Store / Search Engine
- **Expected:** Precise capacity estimation, deep dive on 2 components, monitoring, global scale

---

## SALARY REALITY CHECK (Bangalore, March 2026)

```
Role            Range (Total)    Top 25%       Notes
─────────────────────────────────────────────────────────
Tier 3 SDE-2    ₹18–35L         ₹30–40L       Base heavy, low/no equity
Tier 2 SDE-2    ₹25–55L         ₹45–60L       Mix of base + ESOP
Tier 1 SDE-2    ₹35–80L         ₹60–100L+     Base + RSU (RSU is 40-60% of total)
Goldman/MS SDE-2 ₹35–65L        ₹55–70L       High variable bonus (15-40%)

Note: FAANG India RSU = US stock (AMZN, GOOG etc). At current valuations,
₹60L RSU over 4 years = ₹15L/year pre-tax. This is why total comp matters.

Source: Levels.fyi, Glassdoor India, Blind India thread (2025-2026)
```

---

## YOUR GSTN EXPERIENCE — How to Frame It at Each Tier

### At Tier 3 (Phase 1 targets)
- Lead with scale: "I built systems serving 14M taxpayers"
- Lead with production: "Production Java Spring Boot microservices, not greenfield"
- Lead with domain: "Government-grade reliability — five 9s availability"

### At Tier 2 (Fintech companies)
- Map GSTN → payments: "Tax ledger = settlement ledger. Same consistency guarantees."
- "We processed ₹3 Lakh Crore+ in tax credits. Consistency was non-negotiable."
- "Kafka consumers with DLQ + exactly-once semantics — same patterns as payment pipelines."

### At Tier 1 (FAANG)
- Frame for impact: "Serving 3B+ invoice verifications per year at < 2s latency"
- Frame for scale: "45+ microservices sharing 32 common frameworks — internal platform engineering"
- Frame for complexity: "XA distributed transactions across 4 services with Atomikos JTA"

---

## THE OVERPREP TRUTH

```
Most candidates either under-prep or over-prep in the wrong areas.

Under-prep:   DSA (biggest gap for GSTN engineers moving to product)
              LLD (never practiced end-to-end designs)
              Behavioral (underestimated at every level)

Over-prep:    Framework/library knowledge nobody asks about
              Memorizing theory without coding it
              Reading system design articles without drawing + explaining aloud

The right bar:
  → 150 LeetCode well-understood > 300 barely done
  → 5 system designs explained end-to-end > 20 read
  → 6 STAR stories polished to 2-min each > 15 vague ones
  → Can code a working solution in 35 min under pressure > perfect solutions in 2 hours

Overprep that helps: More applications early. Every rejected interview teaches more
than 3 days of extra study. Apply early, iterate fast.
```

---

## COMPANY-SPECIFIC RECENT QUESTIONS (2024–2026)

### Amazon (SDE-2)
- DSA: "Given a list of meetings, find minimum number of meeting rooms required"
- DSA: "Design a system that finds the median of a data stream"
- SD: "Design Amazon's package tracking system with real-time updates"
- SD: "Design a distributed ID generator (Snowflake-style)"
- LP: "Tell me about a time you disagreed with your manager. What did you do?"
- LP: "Describe a situation where you had to deliver under impossible deadlines."

### Flipkart (SDE-2)
- DSA: "Serialize and deserialize a binary tree"
- DSA: "Given a stream of integers, find top K frequent in last N seconds"
- LLD: "Design an inventory management system with reservations and rollbacks"
- SD: "Design Flipkart's flash sale system — handle 10K purchases in 60 seconds"
- Java: "Explain how ConcurrentHashMap handles concurrent writes in Java 8+"
- Java: "How does @Transactional work internally? What happens if you call a @Transactional method from within the same bean?"

### Goldman Sachs (SDE-2)
- Java: "Explain the lock escalation path in JVM — biased, thin, fat lock"
- Java: "How would you implement a thread-safe singleton without using synchronized?"
- Java: "What is false sharing in CPU cache? How does it affect Java concurrent code?"
- Coding: "Implement a thread-safe bounded blocking queue from scratch"
- Coding: "Design an LRU cache with O(1) get and put using only standard Java"
- SD: "Design a distributed rate limiter used in trading systems"

### PhonePe (SDE-2)
- SD: "Design a UPI payment flow — from request to settlement"
- SD: "How would you ensure exactly-once processing in a payment Kafka consumer?"
- Java: "How does Kafka consumer group rebalancing work? What happens to uncommitted offsets?"
- Java: "Explain two-phase locking vs MVCC. When would you use each?"
- Behavioral: "Tell me about a production incident you caused and how you handled it."

### Swiggy (SDE-2)
- DSA: "Find the shortest path for a delivery partner visiting N restaurants"
- DSA: "Design a data structure supporting insert, delete, and getRandom in O(1)"
- SD: "Design Swiggy's real-time order tracking system"
- SD: "How would you implement surge pricing? What data do you need?"
- Product: "How would you improve Swiggy's search experience for Tier 2 cities?"

---

*Last updated: March 2026 | Sources: Glassdoor, Blind, Leetcode Discuss, Engineering blogs*
*Update this file after each interview — your own data is the most valuable.*
