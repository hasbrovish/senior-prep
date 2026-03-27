# Amazon LP STAR Bank — Behavioral Stories Mapped to Leadership Principles

## LP1: Customer Obsession → Filing Deadline Crisis

**SITUATION:** During quarterly GSTR-1 deadline, 12x traffic spike caused 504 timeouts. 14M taxpayers facing government-mandated deadline with penalties for missing it.

**TASK:** Identify bottleneck and restore service within 30 minutes.

**ACTION:** Checked Grafana → DB connection pool maxed (150/150). Recent code change removed connection timeout. Applied config fix: 5s timeout + idle eviction. Deployed incrementally (one pod → verify → all pods). Post-crisis: proposed mandatory load testing before every deadline.

**RESULT:** Service restored in 22 minutes. Zero data loss (Kafka buffered). Post-mortem led to org-wide mandatory load testing adoption.

**LP Signal:** Put customer (taxpayer) impact first. Fastest safe fix over perfect fix.

---

## LP2: Ownership → Kafka Migration

**SITUATION:** Synchronous REST between 5 microservices caused cascading failures during peak load. Notification pipeline down for hours.

**TASK:** Propose and lead migration to event-driven architecture. Cross-team effort (3 teams, 5 services).

**ACTION:** Built data-driven case (73% of failures = downstream REST timeouts). Evaluated Kafka vs RabbitMQ vs SQS. Designed incremental migration (dual-write → migrate consumers → remove REST). Ran design reviews, addressed team concerns.

**RESULT:** Zero-downtime migration over 2 months. Notification p99: 30s → 2s. Cascading failures eliminated. Kafka now used by 8+ additional services.

**LP Signal:** Owned it end-to-end. Didn't wait for someone to assign it.

---

## LP3: Invent and Simplify → Golang FSM

**SITUATION:** Tax return workflow was 3000 lines of if-else spaghetti. Nobody wanted to modify it. Adding a new case type took 2 weeks.

**TASK:** Design a maintainable workflow engine.

**ACTION:** Chose finite state machine pattern + Go for lightweight concurrency. State definitions in YAML (non-engineers can read). Table-driven tests for 100% transition coverage.

**RESULT:** 800 lines Go + 200-line YAML replaced 3000 lines Java. New states via config (not code). 60% latency reduction. Team members who'd never used Go could add states by editing YAML.

**LP Signal:** Didn't just fix the code — reinvented the approach.

---

## LP4: Are Right, A Lot → Setting Professional Boundaries

**SITUATION:** Senior technologist made inappropriate demands before my official onboarding date — expected early work start, unofficial meetings.

**TASK:** Protect boundaries without creating hostile dynamic.

**ACTION:** Documented everything with timestamps. Responded formally stating official start date and proper channels. Escalated to reporting manager with documentation. Kept tone factual.

**RESULT:** Removed from project (my desired outcome). No career damage. Reinforced that early boundary-setting prevents larger problems.

**LP Signal:** Made the right call despite short-term risk. Used data (documentation) to support position.

---

## LP5: Learn and Be Curious → GenAI POC

**SITUATION:** No one on team had GenAI experience. Infosys wanted to explore retail AI applications.

**TASK:** Build a Digital Shelf AI Agent POC using AWS Bedrock.

**ACTION:** Self-taught foundation model concepts. Built multi-tool AI agent: Bedrock (Claude) for reasoning, SerpAPI for search, Playwright for web scraping, vision models for product page analysis. Handled rate limiting, timeouts, prompt engineering for structured output.

**RESULT:** POC approved. Positioned as team's GenAI resource. Learned end-to-end AI pipeline including failure modes and limitations.

**LP Signal:** Didn't wait for training. Learned by building.

---

## LP6: Hire and Develop the Best → Mentoring

**SITUATION:** Two junior developers joined GSTN team. Struggled with microservices concepts and production debugging.

**TASK:** Accelerate their ramp-up while maintaining project velocity.

**ACTION:** Created mini knowledge-sharing sessions (30 min, 2x/week). Paired programming on real Kafka consumer tasks. Built debugging runbook for common production issues. Let them own a small microservice (notification preferences).

**RESULT:** Both independently productive within 6 weeks (usual ramp: 10-12 weeks). One now owns the notification service. Debugging runbook adopted by entire team.

---

## LP7: Insist on the Highest Standards → Production Memory Leak

**SITUATION:** Filing service OOM after ~3 days uptime. Quick restarts were buying time but not solving root cause.

**TASK:** Find and fix before next filing deadline (5 days away).

**ACTION:** Systematic investigation: GC logging → heap dump → Eclipse MAT analysis → found ConcurrentHashMap with 2.3M entries (session cache with silently dead cleanup task). Fixed: wrapped cleanup in try-catch + alerting, replaced with Caffeine (bounded, auto-evicting), added heap usage alerts at 70%/85%.

**RESULT:** Fix deployed 2 days before deadline. Zero OOM since. Caffeine cache became standard pattern across GSTN services.

**LP Signal:** Didn't accept the band-aid (restart). Found and fixed root cause.

---

## LP8: Think Big → Interview Prep System

**SITUATION:** On bench at Infosys. Could have just passively waited for allocation.

**TASK:** Use the time productively to level up for top-tier companies.

**ACTION:** Built a comprehensive interview prep system: CLI tracker with spaced repetition (SM-2 algorithm), 296-question bank mapped to my experience, FastAPI web portal with AI coaching, Kafka pipeline demo project, structured 26-week plan targeting Phase 1 (mid-tier) then Phase 2 (FAANG).

**RESULT:** Transformed bench period from idle time to structured preparation targeting Google/Anthropic/Stripe level roles.

---

## General STAR Tips

### Bridge Technique (for gaps)
"I haven't worked with [X] directly, but I solved a similar problem with [Y]. Here's how I'd approach [X]..."

### SDE-3 vs SDE-2 Differentiation
- SDE-2: "I fixed the bug" → SDE-3: "I fixed the bug AND prevented the class of bugs"
- SDE-2: "I built it" → SDE-3: "I identified the need, aligned teams, built it, measured impact"
- SDE-2: "It works" → SDE-3: "It works, it's monitored, documented, and the team can maintain it without me"

### Known Anti-Patterns to Avoid (From Post-Interview Analysis)
- Filler words under pressure → Practice the PAUSE
- Flat "no" answers → Always bridge
- Over-explaining → Answer asked question, then stop
- Not quantifying → Every impact needs a number
