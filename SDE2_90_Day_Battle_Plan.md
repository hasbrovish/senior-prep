# SDE-2 INTERVIEW BATTLE PLAN (25-35 LPA)
## 90-Day Structured Preparation — Jayanti (hasbrovish)

---

## TARGET COMPANIES (Filtered for India, 25-35 LPA, Backend/Java roles)

### Tier A — High Probability (25-30 LPA) — Apply first, weeks 5-7
These companies actively hire Java/Spring backend SDE-2s with 4-6 YOE from service company backgrounds:

| Company | Why Realistic | Interview Style |
|---------|--------------|-----------------|
| Flipkart | Heavy Java hiring, machine coding focus | MC + DSA + HLD + HM |
| Swiggy | Loves backend engineers, binary search heavy | OA + DSA + HLD + HM |
| Razorpay | Fintech, values system reliability | DSA + LLD + HLD + Culture |
| PhonePe | Payments infra, Kafka/Redis heavy | DSA + LLD + HLD + HM |
| Groww | Fintech, scaling fast | DSA + System Design + HM |
| CRED | Values clean code, design patterns | MC + DSA + HLD + Bar Raiser |
| Zomato | Hyperlocal systems, scaling | OA + DSA + HLD + HM |
| Meesho | E-commerce, high scale | DSA + LLD + HLD + HM |
| Paytm | Payments, Java backend heavy | DSA + System Design + HM |
| Freshworks | SaaS, India HQ, 26 LPA SDE-2 | DSA + LLD + HLD + HM |
| Intuit India | Operational excellence focus | OA + Coding + Design + Ops |
| SAP Labs | Enterprise, 34 LPA SDE-2 | DSA + Design + HM |
| Atlassian India | Strong engineering culture | DSA + Values + Design |
| BrowserStack | Testing infra, India company | DSA + System Design + HM |
| Udaan | B2B commerce, scaling | MC + DSA + HLD + HM |
| ClearTax | Tax domain (GSTN experience = gold) | DSA + Domain + HLD |

### Tier B — Stretch (30-40 LPA) — Apply weeks 8-12
Higher bar, but your GSTN experience at scale is a differentiator:

| Company | CTC Range | Interview Style |
|---------|-----------|-----------------|
| Amazon (L5) | 35-60+ LPA | OA + 4-5 Loop rounds (DSA + LLD + HLD + LP + Bar Raiser) |
| Microsoft (L61) | 30-45 LPA | OA + 3 Tech (DSA + LLD + HLD) + AA Round |
| Google (L4) | 35-55 LPA | Phone Screen + 4-5 Onsite (DSA heavy + Googleyness) |
| Uber India (L4) | 32-50 LPA | CodeSignal + MC + DSA + HLD + HM + Bar Raiser (6 rounds) |
| Adobe | 30-40 LPA | OA + 3-4 Tech rounds + HM |
| Salesforce | 33 LPA | DSA + Design + Behavioral |
| Walmart Labs | 28-35 LPA | DSA + LLD + HLD + HM |
| Goldman Sachs | 30-45 LPA | OA + Tech (Java deep) + Design + HM |
| JP Morgan | 28-38 LPA | OA + DSA + Spring Boot + Design + HM |
| PayPal | 35 LPA | DSA + System Design + HM |
| Rippling | 35 LPA | DSA + MC + Design |
| DE Shaw | 40 LPA | DSA Heavy + System Design |

---

## INTERVIEW ROUND BREAKDOWN (What SDE-2 Actually Tests)

Based on 2025-2026 interview experiences from LeetCode Discuss, Glassdoor, and Medium:

### Round 1: Online Assessment (OA) — 60-90 minutes
- **What**: 2-3 DSA problems on HackerRank/CodeSignal/Codility
- **Difficulty**: 1 Easy + 1 Medium, or 2 Mediums
- **Bar**: Solve both with all test cases passing
- **Companies**: Amazon, Microsoft, Flipkart, Swiggy, Uber, Intuit, Goldman Sachs

### Round 2: DSA Coding Round(s) — 45-60 minutes each
- **What**: 1-2 problems, code on shared editor or CoderPad
- **Difficulty**: Medium to Hard
- **Expected**: Working code + optimal time/space complexity + dry run
- **You MUST**: Think aloud, ask clarifying questions, discuss trade-offs
- **Companies ask 1-2 DSA rounds**: Most companies

### Round 3: Machine Coding / LLD Round — 60-90 minutes
- **What**: Build a small system from scratch with working code
- **Expected**: Clean OOP code in Java, SOLID principles, design patterns, extensible
- **Format varies**:
  - Flipkart: 90 min coding + 30 min code walkthrough next day
  - Uber: Machine coding with concurrency/multithreading
  - Others: 60 min LLD discussion + partial implementation
- **Key companies**: Flipkart, Uber, CRED, Swiggy, PhonePe, Razorpay

### Round 4: High-Level Design (HLD) — 45-60 minutes
- **What**: Design a large-scale distributed system
- **Expected**: Requirements → Estimations → API → Data Model → Architecture → Deep Dives → Trade-offs
- **You MUST**: Drive the conversation, draw diagrams, discuss CAP theorem, caching strategies, database choices
- **This is THE differentiator for SDE-2 vs SDE-1**

### Round 5: Behavioral / Hiring Manager — 30-60 minutes
- **What**: Past projects deep dive, STAR stories, leadership scenarios
- **Amazon-specific**: Leadership Principles (Customer Obsession, Ownership, Disagree & Commit)
- **Microsoft-specific**: AA Round (As Appropriate) with senior leadership
- **Expected**: Authentic stories with real tension and impact

---

## THE NON-NEGOTIABLE NUMBERS

### DSA Target: 200 problems in 12 weeks

| Week | Problems/Week | Difficulty Mix | Running Total |
|------|--------------|----------------|---------------|
| 1-3 | 12/week | 70% Medium, 30% Easy | 36 |
| 4-7 | 14/week | 80% Medium, 20% Hard | 92 |
| 8-10 | 16/week | 70% Medium, 30% Hard | 140 |
| 11-12 | 14/week | Company-specific mix | 168-200 |

**That's 2 problems per day. Non-negotiable. In Java only.**

### The 12 Patterns You Must Master (in priority order)

Based on 2025-2026 FAANG interview data — ~87% of questions use these patterns:

| # | Pattern | Problems to Solve | Key LeetCode Problems |
|---|---------|-------------------|----------------------|
| 1 | **Arrays + Hashing** | 20 | Two Sum, Group Anagrams, Top K Frequent, Product of Array Except Self |
| 2 | **Two Pointers** | 15 | 3Sum, Container With Most Water, Trapping Rain Water |
| 3 | **Sliding Window** | 15 | Longest Substring Without Repeating, Minimum Window Substring, Max Points from Cards |
| 4 | **Binary Search** | 15 | Search in Rotated Array, Koko Eating Bananas, Median of Two Sorted Arrays, Painters Partition |
| 5 | **Trees (BFS/DFS)** | 20 | Right View, Diameter, LCA, Serialize/Deserialize, Kth Smallest in BST |
| 6 | **Graphs (BFS/DFS)** | 20 | Number of Islands, Course Schedule (Topo Sort), Cheapest Flights K Stops, Alien Dictionary |
| 7 | **Dynamic Programming** | 25 | Climbing Stairs → Coin Change → Longest Common Subsequence → Edit Distance → Knapsack → DP on Strings |
| 8 | **Linked Lists** | 10 | Reverse, Merge Two Sorted, Detect Cycle, LRU Cache, Copy Random Pointer |
| 9 | **Stack/Monotonic Stack** | 10 | Valid Parentheses, Daily Temperatures, Next Greater Element, Min Stack |
| 10 | **Heap/Priority Queue** | 10 | Kth Largest, Merge K Sorted Lists, Top K Frequent, Find Median from Data Stream |
| 11 | **Backtracking** | 10 | Subsets, Permutations, N-Queens, Word Search, Combination Sum |
| 12 | **Intervals + Greedy** | 10 | Merge Intervals, Insert Interval, Meeting Rooms II, Non-overlapping Intervals |

**Total: ~180 targeted problems across 12 patterns**

### LLD: 10 Must-Do Problems (in priority order)

These appear repeatedly across Flipkart, Uber, Swiggy, CRED, Amazon, Microsoft:

| # | Problem | Key Concepts | Companies |
|---|---------|-------------|-----------|
| 1 | **Parking Lot System** | Singleton, Factory, Strategy pattern, SOLID | Amazon, Microsoft, most |
| 2 | **LRU Cache** | HashMap + DoublyLinkedList, Thread safety | Microsoft, Amazon, Google |
| 3 | **BookMyShow / Movie Booking** | Concurrency, seat locking, payment flow | Flipkart, Amazon, Intuit |
| 4 | **Splitwise / Expense Sharing** | Graph (debt simplification), Observer pattern | CRED, Flipkart, Razorpay |
| 5 | **Snake and Ladder** | State machine, Strategy pattern | Flipkart, Swiggy |
| 6 | **Elevator System** | State pattern, Scheduling strategies | Amazon, Microsoft |
| 7 | **E-commerce with Loyalty/Cart** | Factory, Strategy, extensible pricing | Flipkart, Meesho, Udaan |
| 8 | **Rate Limiter** | Sliding window, Token bucket, Thread safety | JP Morgan, Uber, Amazon |
| 9 | **Notification Service** | Observer, Strategy, Template pattern | PayPal, PhonePe |
| 10 | **File System / Logger** | Composite pattern, Chain of Responsibility | Microsoft, Google |

**For each problem, you must**:
- Write complete working Java code (not pseudocode)
- Apply SOLID principles explicitly
- Use at least 2 design patterns with justification
- Handle concurrency where applicable
- Be able to extend the design in a 30-min code walkthrough

### HLD: 12 Must-Do System Designs (in priority order)

| # | System | Key Concepts Tested | Companies That Ask |
|---|--------|--------------------|--------------------|
| 1 | **URL Shortener** | Hashing, DB choice, caching, analytics | Amazon, Microsoft, 40% of HLD interviews |
| 2 | **Rate Limiter** | Token bucket, sliding window, distributed | JP Morgan, Amazon, Uber |
| 3 | **Chat System (WhatsApp)** | WebSockets, message queue, E2E encryption | Amazon, Uber, Meta |
| 4 | **Notification System** | Kafka, push vs pull, priority queues, templating | PhonePe, Amazon, Swiggy |
| 5 | **News Feed / Twitter** | Fan-out, Kafka, Cassandra, push vs pull hybrid | Microsoft, Amazon, Meta |
| 6 | **Ride Sharing (Uber/Ola)** | Geospatial DB, quadtrees, WebSockets, matching | Uber, Swiggy, Zomato |
| 7 | **E-commerce (Amazon/Flipkart)** | Search, inventory, cart, payments, microservices | Flipkart, Amazon, Meesho |
| 8 | **Online Coding Platform (LeetCode)** | Code execution sandbox, WebSockets, queuing | Amazon, Microsoft |
| 9 | **Distributed Cache** | Consistent hashing, LRU eviction, replication | Microsoft, Amazon, Google |
| 10 | **Payment System** | ACID, idempotency, saga pattern, reconciliation | Razorpay, PhonePe, Paytm |
| 11 | **Food Delivery System** | ETA, logistics optimization, real-time tracking | Swiggy, Zomato, Uber Eats |
| 12 | **Tax Filing System (GSTN-anchored)** | Your secret weapon — high throughput, Kafka, Redis, HBase at 14M users | ClearTax, Intuit, any company |

**For each design, practice this framework out loud (45 min)**:
1. **Requirements** (5 min): Functional + Non-functional, ask clarifying questions
2. **Estimations** (5 min): DAU, QPS, storage, bandwidth
3. **API Design** (5 min): REST endpoints, request/response
4. **Data Model** (5 min): Schema, SQL vs NoSQL choice with reasoning
5. **High-Level Architecture** (10 min): Draw components, load balancer, CDN, cache, DB, message queue
6. **Deep Dives** (10 min): The hard parts — consistency, fault tolerance, scaling bottlenecks
7. **Trade-offs** (5 min): CAP theorem application, alternatives considered

### STAR Stories: 6 Minimum (Amazon needs 8-10)

Prepare these scenarios with specific, real examples from GSTN:

| Scenario | Your GSTN Story Angle |
|----------|----------------------|
| **Led a technically complex project** | Kafka pipeline handling 100K concurrent GST filings |
| **Disagreed with someone senior** | Architecture decision on Redis vs HBase for caching |
| **Delivered under tight deadline** | GST deadline month, system handling 10x traffic spike |
| **Fixed a critical production issue** | Debugging under pressure, root cause analysis |
| **Improved a process/system** | Performance optimization, reducing latency or cost |
| **Mentored someone / helped the team** | Onboarding juniors, code review culture |
| **Customer obsession** (Amazon) | User-facing impact of your tax filing reliability work |
| **Learned something new quickly** | Golang marketplace project or GenAI POC |

---

## WEEK-BY-WEEK SCHEDULE

### PHASE 1: FOUNDATION RESET (Weeks 1-4)

**Daily Rhythm — 10 hours/day**

| Time | Activity | Details |
|------|----------|---------|
| 6:00-7:00 AM | Yoga + Pranayama | Non-negotiable. Physical health = interview performance |
| 7:00-7:30 AM | Review yesterday | Redo 1 problem you struggled with yesterday |
| 7:30-10:30 AM | DSA (3 hrs) | 2 LeetCode Mediums in Java. Timer: 30 min per problem |
| 10:30-11:00 AM | Break + Walk | |
| 11:00-1:00 PM | Java + Spring Boot (2 hrs) | Core concepts + build small microservice project |
| 1:00-2:00 PM | Lunch + Rest | |
| 2:00-4:00 PM | DSA review + Programming Pathshala (2 hrs) | Pattern study + video lessons |
| 4:00-4:30 PM | Break | |
| 4:30-6:00 PM | LLD Practice (1.5 hrs) | Start week 2: 1 LLD problem per week |
| 6:00-7:00 PM | SPEAK PRACTICE (1 hr) | Record yourself explaining today's DSA solution + one Java concept. 3 minutes each, review recording |
| 7:00-8:00 PM | Dinner + Recharge | |
| 8:00-9:00 PM | STAR Stories + Behavioral prep (1 hr) | Write and practice 1 STAR story per day |
| 9:00-9:30 PM | Tomorrow's plan | Write down exactly what you'll study tomorrow |

**Week 1 Focus**: Arrays, Strings, HashMap — 12 problems. Java syntax comfort (Collections, Streams, Lambda). Revise Spring Boot annotations (@RestController, @Service, @Repository, @Value, @Profile)

**Week 2 Focus**: Two Pointers, Sliding Window — 12 problems. Spring Boot: Build a REST API with MySQL + CRUD. Start LLD Problem #1 (Parking Lot)

**Week 3 Focus**: Binary Search, Sorting — 12 problems. Spring Boot: Add Redis caching + Kafka messaging to your project. LLD Problem #2 (LRU Cache)

**Week 4 Focus**: Linked Lists, Stacks, Queues — 12 problems. Spring Boot: Spring Security basics, Exception handling, Logging (SLF4J/Logback). LLD Problem #3 (BookMyShow)

### PHASE 2: LEVEL UP (Weeks 5-8)

**Start applying to Tier A companies by Week 5-6**

| Time | Activity | Details |
|------|----------|---------|
| 7:00-10:00 AM | DSA (3 hrs) | 2 problems (Medium/Hard mix) |
| 10:30-12:30 PM | HLD Study + Practice (2 hrs) | 1 system design per week, study + practice out loud |
| 1:30-3:30 PM | LLD Practice (2 hrs) | 1 LLD problem per week, full working Java code |
| 4:00-5:30 PM | Java Deep Dive (1.5 hrs) | Concurrency, Multithreading, JVM internals, GC |
| 5:30-6:30 PM | Mock Interview OR Speak Practice (1 hr) | Alternate: Mock Mon/Wed/Fri, Speak Tue/Thu |
| 8:00-9:00 PM | Company research + Applications (1 hr) | Apply to 3-5 companies per week |

**Week 5**: Trees (BFS/DFS) — 14 problems. HLD: URL Shortener. LLD: Splitwise. Start applying.
**Week 6**: Graphs — 14 problems. HLD: Rate Limiter. LLD: Elevator System. 2 mock interviews this week.
**Week 7**: Dynamic Programming (Easy→Medium) — 14 problems. HLD: Chat System. LLD: E-commerce Cart.
**Week 8**: DP continued + Heaps — 14 problems. HLD: Notification System. LLD: Rate Limiter code.

### PHASE 3: INTERVIEW MODE (Weeks 9-12)

**You should have active interview processes by now**

| Time | Activity | Details |
|------|----------|---------|
| 7:00-9:00 AM | DSA maintenance (2 hrs) | 1-2 problems, focus on company-tagged problems |
| 9:30-11:30 AM | HLD Practice (2 hrs) | Continue new designs + revisit previous ones out loud |
| 12:30-2:00 PM | Company-specific prep (1.5 hrs) | Study tech blog, Glassdoor reviews, LeetCode Discuss for that company |
| 2:30-4:00 PM | Mock Interviews (1.5 hrs) | 3-4 mocks per week (Pramp, Interviewing.io, peers) |
| 4:30-5:30 PM | Weak area deep dive (1 hr) | Whatever gaps mocks reveal |
| 6:00-7:00 PM | STAR stories rehearsal | Practice until they're natural, not memorized |

**Week 9**: Backtracking + Intervals — 14 problems. HLD: News Feed. HLD: Ride Sharing.
**Week 10**: Mixed hard problems — 16 problems. HLD: Payment System. HLD: Food Delivery.
**Week 11**: Company-specific grinding. HLD: Distributed Cache. Revisit all 10 LLDs.
**Week 12**: Light practice. Focus on mocks, rest before interviews, confidence building.

---

## JAVA DEEP KNOWLEDGE CHECKLIST (SDE-2 Expected)

You need to know these cold — interviewers will probe:

### Core Java (Week 1-4)
- [ ] Collections Framework: HashMap internals, ConcurrentHashMap, TreeMap, LinkedHashMap, PriorityQueue
- [ ] Generics: Bounded types, wildcards, type erasure
- [ ] Exception handling: Checked vs unchecked, custom exceptions, try-with-resources
- [ ] Java 8+: Streams, Lambda, Functional interfaces, Optional, CompletableFuture
- [ ] Strings: String pool, StringBuilder vs StringBuffer, immutability
- [ ] equals() and hashCode() contract
- [ ] Comparable vs Comparator

### Concurrency & Multithreading (Week 5-8)
- [ ] Thread lifecycle, Runnable vs Callable
- [ ] synchronized, volatile, atomic variables
- [ ] ReentrantLock, ReadWriteLock, Semaphore
- [ ] ExecutorService, ThreadPoolExecutor
- [ ] Producer-Consumer pattern
- [ ] ConcurrentHashMap, CopyOnWriteArrayList, BlockingQueue
- [ ] Deadlock detection and prevention
- [ ] CompletableFuture chaining

### JVM Internals (Week 6-8)
- [ ] Memory model: Heap, Stack, Metaspace
- [ ] Garbage Collection: G1, ZGC, tuning
- [ ] ClassLoader hierarchy
- [ ] JIT compilation basics

### Spring Boot (Week 1-6)
- [ ] IoC and DI: @Autowired, @Qualifier, @Primary, constructor injection
- [ ] Bean lifecycle and scopes (singleton, prototype, request, session)
- [ ] @Configuration, @Bean, @Component, @Service, @Repository
- [ ] Spring Profiles and @Value annotation
- [ ] REST: @RestController, @RequestMapping, @PathVariable, @RequestBody
- [ ] Exception handling: @ControllerAdvice, @ExceptionHandler
- [ ] Spring Security: Authentication, Authorization, JWT
- [ ] Spring Data JPA: Repository pattern, custom queries, pagination
- [ ] Logging: SLF4J + Logback configuration
- [ ] Actuator endpoints for monitoring
- [ ] Testing: @SpringBootTest, @MockBean, Mockito

### Distributed Systems Concepts (Week 5-10)
- [ ] CAP Theorem and its practical implications
- [ ] Consistent Hashing
- [ ] Database sharding and partitioning
- [ ] Kafka: Topics, partitions, consumer groups, exactly-once semantics
- [ ] Redis: Data structures, caching patterns, pub/sub, TTL
- [ ] Load balancing: Round robin, least connections, consistent hashing
- [ ] API Gateway patterns
- [ ] Circuit breaker, retry, and timeout patterns
- [ ] Database indexing: B-Tree, Hash, Composite
- [ ] SQL vs NoSQL: When to use which
- [ ] Message queue patterns: Pub/Sub, Point-to-Point, Dead Letter Queue

---

## RESOURCES (Free + Paid)

### DSA
- LeetCode (Free tier is enough, Premium for company tags is worth it)
- NeetCode.io — Pattern-organized video solutions
- Programming Pathshala (you already have access)
- Sean Prashad's LeetCode Patterns: seanprashad.com/leetcode-patterns

### LLD
- GitHub: github.com/kumaransg/LLD (curated LLD problems with Java code)
- workat.tech/machine-coding (Flipkart/Uber/Swiggy style problems)
- Concept && Coding (YouTube) — LLD playlist

### HLD
- System Design Primer (GitHub): github.com/donnemartin/system-design-primer
- ByteByteGo (Alex Xu) — YouTube channel + System Design Interview books
- Grokking System Design (Educative) — if budget allows
- Gaurav Sen (YouTube) — System design in Hindi/English

### Mock Interviews
- Pramp.com (Free peer mocks)
- Interviewing.io (Free for first few)
- Find DSA/Design practice partners on LeetCode Discuss

### Behavioral
- Amazon Leadership Principles: amazon.jobs/content/en/our-workplace/leadership-principles
- STAR Method guide: amazon.jobs/content/en/how-we-hire/interview-loop

---

## DAILY NON-NEGOTIABLE CHECKLIST

Print this and check off every single day:

- [ ] Woke up by 6 AM
- [ ] Yoga/Pranayama/Surya Namaskar done
- [ ] 2 LeetCode problems solved in Java (timed, 30 min each)
- [ ] 1 new concept studied (Java/Spring/System Design)
- [ ] Spoke out loud for minimum 15 minutes (recorded)
- [ ] Tracked progress in spreadsheet
- [ ] Planned tomorrow before sleeping

---

## THE MINDSET CONTRACT (Sign this with yourself)

1. **I will not add GenAI, AWS certs, or any other track for 90 days.** Java + DSA + Design only.
2. **I will not skip a single day.** Bad days get reduced effort, not zero effort.
3. **I will start applying by week 5**, even if I don't feel ready.
4. **I will treat the first 2-3 interviews as paid mock interviews.** No pressure.
5. **I will not compare myself to LinkedIn posts.** My only metric is me vs. last week.
6. **I will record myself speaking every day** because articulation is my biggest gap.
7. **I will ask for help when stuck** — from Claude, from peers, from communities. Asking isn't weakness.
8. **I will take care of my body.** Sleep 7+ hours. Yoga daily. Eat well. A burnt-out brain fails interviews.
9. **I will remember**: CodeChef 4-star, CodeVita Top 1%, GSTN at 14M users — I have the foundation. I just need to rebuild the confidence.
10. **90 days from today, I will have a 25-35 LPA offer.** That's the mission.

---

*Generated: March 28, 2026*
*Start Date: March 31, 2026 (Monday)*
*Target: June 28, 2026*

**Jai Shree Krishna. Ab shuru karte hain.** 🚀
