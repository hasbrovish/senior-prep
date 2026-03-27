# Amazon Leadership Principles — STAR Answer Bank
# Jayanti Vishnoi | 5.5 YOE | GSTN
# Every Amazon round has 2 LP questions. Bar Raiser is dedicated behavioral.

## HOW TO USE
- Each LP has GSTN-based STAR stories (Situation → Task → Action → Result)
- 2–3 minutes max per story when spoken
- Use Quick Reference at bottom to pick the right story per LP

---

## 1. CUSTOMER OBSESSION

### Story A — Cache Reliability for 14M Taxpayers
**S:** During peak filing (GSTR-1 monthly deadline), our cache layer (JBoss DataGrid + EhCache) caused stale ITC calculation results for taxpayers.
**T:** Fix cache consistency without increasing latency — any slowdown directly hurt taxpayer experience.
**A:** Profiled invalidation patterns. Redesigned DistCacheUtil: write-through for financial data, write-behind only for non-critical reads. Added cache version headers for debugging.
**R:** Eliminated stale data complaints next filing cycle. Cache hit ratio held at 85%+. Impact: all 14M taxpayers.

### Story B — CQRS to Fix 8–12s Query Latency
**S:** Taxpayers querying GSTR-2A saw 8–12s responses at peak. Ministry escalations came in — politically sensitive.
**T:** Get latency under 2s without disrupting the write pipeline serving 3B invoices/year.
**A:** Introduced read replicas, separated query model from command model (CQRS). Added composite indexes on read replica. Coordinated with 3 teams to keep replica lag under 500ms.
**R:** Response dropped to under 1.5s. Zero consistency complaints post-deploy. Ministry escalations stopped.

---

## 2. OWNERSHIP

### Story A — Kafka DLQ Framework Adopted Org-Wide
**S:** Multiple GSTN teams were silently losing Kafka messages on consumer failure. I owned only the Return filing consumer, but 8+ services had the same broken retry pattern.
**T:** Fix ours, but also solve the org-wide problem.
**A:** Built a generic Kafka consumer framework: configurable retry, exponential backoff, DLQ routing. Documented it, presented to architecture team, helped 3 other teams onboard — all outside my sprint scope.
**R:** Adopted by 5 teams in 2 months. Zero message loss incidents org-wide for 6 months.

### Story B — 2AM Production Incident (Not My On-Call)
**S:** Month-end filing peak. OOM crashes in invoice validation service at 2AM. ~50,000 active sessions affected. On-call engineer was struggling.
**T:** I was not on-call but saw the alert.
**A:** Joined the bridge call, diagnosed heap dumps — static HashMap retention in validator cache. Provided fix (weak references + eviction), coordinated deploy, stayed till 4AM ensuring stability.
**R:** System recovered in 45 minutes. No data loss. I wrote the post-mortem and added memory leak detection to CI pipeline.

---

## 3. INVENT AND SIMPLIFY

### Story A — Case Workflow Engine (Strategy + Factory)
**S:** GSTN appeal processing had 12 case types, each with separate if-else chains spanning 800+ lines. Adding a new case type = 2 weeks + regression risk.
**T:** Make new case types addable in days, not weeks.
**A:** Designed Strategy + Factory pattern workflow engine. Each case type = self-contained class implementing a common interface. Config-driven routing replaced hardcoded chains.
**R:** New case type onboarding: 2 weeks → 2 days. Defect rate on routing dropped to near-zero. 60% reduction in cyclomatic complexity.

### Story B — Config Drift Detection (3 Days, No New Tools)
**S:** 45+ microservices with Spring Boot configs across environments. Config drift caused 3 prod incidents in one quarter.
**T:** Detect drift automatically without buying a dedicated config management tool.
**A:** Wrote a Spring Boot Actuator-based scanner: compared /env endpoints across environments, diffed properties, posted alerts to Slack via webhook. Built in 3 days.
**R:** Caught 2 drift issues before they reached prod in the first month. Saved the tool purchase budget.

---

## 4. ARE RIGHT, A LOT

### Story A — XA Transactions vs Saga (I Was Right)
**S:** Architecture proposed XA 2-phase commit across 3 services for ledger operations.
**T:** Validate or challenge the approach with data.
**A:** Built Atomikos XA prototype, load tested at 500 TPS (our peak). XA added 300ms per transaction. Presented comparison: XA vs Saga with compensation. Made the case for Saga.
**R:** Team adopted Saga for new services. XA limited to legacy. Significant latency saved at peak filing.

### Story B — Kafka Hot Partition Root Cause
**S:** Consumer lag spikes on certain partitions. Team suspected network issues.
**T:** Diagnose the actual root cause.
**A:** Analyzed partition distribution — large taxpayers (1M+ invoices) distributed round-robin were causing hot partitions. Recommended GSTN-ID based key partitioning with custom partitioner bucketing large filers separately.
**R:** Consumer lag reduced 70%. Rebalancing events dropped significantly. I was right despite initial pushback.

---

## 5. LEARN AND BE CURIOUS

### Story A — Self-Taught Golang for Reconciliation Service
**S:** Team chose Golang for a new high-performance reconciliation service. I had zero production Go experience.
**T:** Get productive quickly and deliver production-quality code.
**A:** Spent 3 weekends learning Go (goroutines, channels, context, error patterns). Built a toy Kafka consumer first. Then contributed the reconciliation service's core matching algorithm with goroutine pooling and context cancellation.
**R:** Service delivered on time. Positively reviewed by senior Go engineer. I now maintain Go components alongside Java.

### Story B — Read DDIA on My Own, Applied Immediately
**S:** My role was Spring Boot feature dev. I wanted to understand why our distributed transactions were unreliable.
**T:** Self-study distributed systems without formal guidance.
**A:** Read "Designing Data-Intensive Applications" over 2 months (evenings). Identified that our service used read-your-own-writes without accounting for replica lag. Raised this in architecture review.
**R:** Replica lag issue patched. I became the team's go-to for distributed consistency questions. Knowledge applied in 3 design decisions over the next year.

---

## 6. HIRE AND DEVELOP THE BEST

### Story A — Mentoring Junior on Heap Dump Debugging
**S:** New grad assigned to debug Hibernate session memory issue. Stuck for 2 days.
**T:** Help them resolve it AND build lasting debugging skills.
**A:** Walked them through heap dump analysis step by step. Explained Hibernate session lifecycle, GC roots, VisualVM usage. Made them drive the fix while I guided.
**R:** Resolved in 4 hours. 3 months later, independently debugging similar issues. Cited this as most valuable learning from first year.

### Story B — Kafka Internals Tech Talk (18 Engineers, 3 Teams)
**S:** Team had surface-level Kafka knowledge, making suboptimal decisions on partitions, acks, consumer groups.
**T:** Raise the team's Kafka knowledge bar.
**A:** Prepared 45-min internal talk: "Kafka in Production — What the Docs Don't Tell You." Covered real GSTN incidents, config trade-offs, consumer group rebalancing.
**R:** 18 engineers attended across 3 teams. Two teams changed Kafka configs post-talk. Positive feedback from architect.

---

## 7. INSIST ON THE HIGHEST STANDARDS

### Story A — Blocked Shortcut in Invoice Validation
**S:** Under ministry deadline pressure, team member proposed skipping schema validation for bulk invoice uploads "just this release."
**T:** Decide: accept shortcut or push back?
**A:** Pushed back. Explained cascading failure risk. Proposed async validation with rejection queue as alternative. Volunteered to implement it in the remaining time.
**R:** Async path shipped on time. Zero invalid invoices processed. The shortcut would have corrupted millions of ITC claims.

### Story B — Raised Code Review Standards
**S:** PR reviews were rubber-stamps. Several bugs escaped to prod that review should have caught.
**T:** Raise quality without creating resentment.
**A:** Created 1-page PR checklist (thread safety, null handling, exception handling, test coverage). Modeled the behavior with detailed comments. Proposed 2 meaningful approvals in team retro.
**R:** Team adopted the checklist. Bug escape rate dropped. Code review became a learning activity.

---

## 8. THINK BIG

### Story — Proposed Event-Driven Architecture (Became 12-Month Initiative)
**S:** GSTN's appeal processing was synchronous REST chains — slow, tightly coupled, fragile.
**T:** Propose a significant architectural shift, not just incremental fixes.
**A:** Built a Kafka-based event-driven PoC. Showed 3x load handling with better fault tolerance. Presented to senior architects with metrics.
**R:** PoC approved. I led design for first 3 services in the migration. It became a 12-month org initiative.

---

## 9. BIAS FOR ACTION

### Story — Weekend Production Fix (Didn't Wait for Monday)
**S:** Friday evening. Bug causing incorrect IGST calculation for inter-state invoices. Needed to be fixed before Monday morning filing rush.
**T:** Wait or act now?
**A:** Validated fix locally, wrote tests, got one colleague review via WhatsApp, deployed to staging, verified, got team lead approval, deployed to prod by Saturday morning.
**R:** Fixed before any taxpayer affected. Zero Monday escalations. Documented the decision-making in incident report.

---

## 10. FRUGALITY

### Story — Avoided License Upgrade by Optimizing Cache
**S:** JBoss DataGrid licensing costs rising. Team proposing a larger license upgrade.
**T:** Reduce cost without degrading performance.
**A:** Analyzed cache access patterns. Found 30% of cached objects had zero hit rate after 5 minutes. Added TTL policies, reduced heap requirement by 25%. Migrated 3 non-critical caches to Redis (open source) without performance regression.
**R:** Avoided the license upgrade. Reduced infrastructure cost. Documented the Redis migration pattern for future teams.

---

## 11. EARN TRUST

### Story — Wrote Honest Post-Mortem on My Own Bug
**S:** A bug I introduced caused incorrect tax computation for ~200 taxpayers over 2 days.
**T:** Write a complete, honest post-mortem even though it reflected poorly on me.
**A:** Full post-mortem: root cause (null handling flaw in tax slab lookup), impact (200 taxpayers, auto-corrected), 5 preventive measures. Presented to team and senior management.
**R:** All 5 measures implemented. Trust increased rather than decreased. Team shifted toward more honest incident reporting.

---

## 12. DIVE DEEP

### Story — Root-Caused Kafka Lag to GC, Not Kafka
**S:** Consumer lag growing intermittently. Infra team blamed Kafka. No one could find root cause.
**T:** Go deeper.
**A:** Correlated lag spikes with deployment timeline. Found spikes matched GC pause events in consumer JVM — not Kafka. Profiled with VisualVM, found large intermediate collections created per message causing GC pressure.
**R:** Fixed object allocation. GC pause time reduced 80%. Consumer lag became stable. Infra team updated runbook: "check consumer GC before escalating to Kafka team."

---

## 13. HAVE BACKBONE; DISAGREE AND COMMIT

### Story — MongoDB Pushback (Documented Risk Materialized Later)
**S:** Tech lead proposed MongoDB for invoice ledger data "for flexibility." I believed this was wrong for ACID-required transactional data.
**T:** Make my case, then commit if overruled.
**A:** Wrote comparison doc: MongoDB multi-document transactions vs MySQL for our access patterns. Shared in design review. Was overruled. Documented my objection as a risk in the design doc. Then fully committed to making MongoDB work correctly.
**R:** 6 months later, the documented risk materialized (multi-document transaction edge case). MySQL adopted for next similar module. Being right mattered less than being heard and documenting it.

---

## 14. DELIVER RESULTS

### Story A — Ministry Deadline: P0+P1 Shipped 2 Days Early
**S:** Ministry of Finance hard deadline: HSN code validation live before April 1st filing cycle. 6 weeks. Scope underestimated at project start.
**T:** Deliver on time despite scope creep.
**A:** Triaged into P0/P1/P2. Negotiated P2 to next sprint. Paired with QA to parallelize testing. Removed blockers daily.
**R:** P0+P1 shipped 2 days before deadline. P2 in next sprint. Zero filing-day issues. Contributed to my last promotion.

### Story B — 99.97% Uptime on 3B Invoices/Year
**S:** GSTN processes ~3B invoices annually. Filing window downtime = direct taxpayer + ministry SLA impact.
**T:** Maintain 99.9%+ uptime on the invoice pipeline I owned.
**A:** Circuit breakers, bulkheads, graceful degradation. Blue-green zero-downtime deployments. Load testing before each peak cycle. Runbooks for every known failure mode.
**R:** 99.97% uptime over 18 months. Only 1 unplanned outage, resolved in 23 minutes.

---

## QUICK REFERENCE — STORY-TO-LP MAPPING

| Story | Primary LP | Good for Secondary |
|-------|-----------|-------------------|
| Cache redesign (DistCacheUtil) | Customer Obsession | Dive Deep |
| CQRS for query latency | Customer Obsession | Deliver Results |
| Kafka DLQ framework | Ownership | Invent & Simplify |
| 2AM production incident | Ownership | Bias for Action |
| Case workflow engine | Invent & Simplify | Think Big |
| Config drift detection | Invent & Simplify | Frugality |
| XA vs Saga | Are Right A Lot | Backbone |
| Kafka hot partition | Are Right A Lot | Dive Deep |
| Self-taught Golang | Learn & Be Curious | Deliver Results |
| Read DDIA, applied it | Learn & Be Curious | Are Right A Lot |
| Mentored junior engineer | Hire & Develop Best | Earn Trust |
| Kafka tech talk | Hire & Develop Best | Think Big |
| Blocked validation shortcut | Highest Standards | Backbone |
| Code review checklist | Highest Standards | Hire & Develop Best |
| Event-driven PoC | Think Big | Invent & Simplify |
| Weekend production fix | Bias for Action | Ownership |
| Cache cost optimization | Frugality | Ownership |
| Honest post-mortem | Earn Trust | Highest Standards |
| GC root cause (Kafka lag) | Dive Deep | Are Right A Lot |
| MongoDB pushback | Backbone | Are Right A Lot |
| Ministry deadline delivery | Deliver Results | Bias for Action |
| 3B invoices uptime | Deliver Results | Ownership |

---

## AMAZON-SPECIFIC TIPS

1. Each interview round = 2 LP questions at the start
2. Bar Raiser round = 3rd follow-up on same story is common ("what would you do differently?")
3. Always use "I", not "we" — they want YOUR contribution
4. End every story: "What I learned from this was..."
5. Keep metrics front and center: "14M taxpayers", "3B invoices", "70% lag reduction"
6. Prepare for: "Tell me about a time you failed" — use the post-mortem story
7. Prepare for: "Tell me about a time you disagreed" — use XA vs Saga or MongoDB stories
