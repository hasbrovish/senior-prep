# Company Interview Intelligence Report — 20 Companies
### Compiled: March 2026 | For: Jayanti Vishnoi (5.5 YOE)
### Sources: Glassdoor, LeetCode Discuss, Medium, TeamBlind, Levels.fyi, Prepfully, InterviewQuery, Exponent

---

## Table of Contents
1. [Stripe](#1-stripe)
2. [Google](#2-google)
3. [DoorDash](#3-doordash)
4. [Apple](#4-apple)
5. [Oracle](#5-oracle)
6. [Zerodha](#6-zerodha)
7. [PayPal](#7-paypal)
8. [Zomato](#8-zomato)
9. [Samsara](#9-samsara)
10. [NVIDIA](#10-nvidia)
11. [xAI](#11-xai)
12. [Tesla](#12-tesla)
13. [Bloomberg](#13-bloomberg)
14. [Deutsche Bank](#14-deutsche-bank)
15. [Anthropic](#15-anthropic)
16. [OpenAI](#16-openai)
17. [Flipkart](#17-flipkart)
18. [PhonePe](#18-phonepe)
19. [Swiggy](#19-swiggy)
20. [Razorpay](#20-razorpay)
21. [Cross-Company Analysis](#21-cross-company-analysis)
22. [Priority DSA Problems](#22-priority-dsa-problems)
23. [Priority System Design Problems](#23-priority-system-design-problems)

---

## 1. STRIPE

| Attribute | Details |
|-----------|---------|
| **Target Level** | L2 (SDE-2 equivalent) |
| **TC Range (India)** | 90-95L first year (Base ~50L + Stock ~33L/yr + Bonus ~5-10L + Joining ~7.5L) |
| **Total Rounds** | 6 rounds total |
| **Hiring Timeline** | 4-6 weeks |
| **Difficulty** | Hard (unique format, not standard LC) |
| **Rejection Rate** | High (~75-80%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Recruiter Screen | Background, motivation, role fit |
| 2 | 60 min | Technical Phone Screen | 1 coding problem with follow-ups, practical (not LC-style) |
| 3 | 60 min | Coding (Onsite) | Implementation-heavy, 1 question with 3 progressive sub-parts |
| 4 | 60 min | Bug Bash (Onsite) | Debug real Stripe-like codebase, find and fix defects, write tests |
| 5 | 60 min | System Design (Onsite) | Payments/financial systems focus |
| 6 | 45 min | Behavioral (Onsite) | Past work, collaboration, Stripe values |

### DSA Questions & Topics
- **Style**: NOT standard LeetCode. Implementation-heavy, real-world business problems
- **Difficulty**: Medium LC equivalent but more practical
- **Topics**: Arrays, Maps, Strings, Parsing, Caching
- **Example Problems**:
  - Email scheduling system
  - Log deduplication service
  - Rate limiter implementation
  - Bitmap manipulation
  - Server/API implementation
  - Data parsing with progressive complexity

### System Design Questions
- Design a sharded ledger system
- Design an event-driven payment retry system
- Design a metrics aggregation service
- Design a notification system for payments
- Design a data processing pipeline
- Integration with Stripe APIs (unique to Stripe)

### LLD / Machine Coding
- Not a separate round, but coding rounds test clean OOP, modularity
- Bug Bash round tests debugging + writing tests

### Behavioral Focus
- Stripe values: users first, think rigorously, trust and amplify, global optimization
- Emphasis on collaboration and clear communication
- Past experience with ambiguous problems

### Unique Characteristics
- **Bug Bash is unique**: Simulates production debugging with real code snippets
- Code readability valued over algorithmic cleverness
- Questions are Stripe-domain-specific (payments, subscriptions, invoicing)
- Python/Ruby/Java all accepted; Python most common
- Practice "live debugging" in open-source repos as preparation

---

## 2. GOOGLE

| Attribute | Details |
|-----------|---------|
| **Target Level** | L4 (SDE-2) / L5 (SDE-3) |
| **TC Range (India)** | L4: 55-95L (median ~74L, negotiated up to 1.38Cr); L5: 1-1.8Cr |
| **Total Rounds** | 5-6 rounds (GHA + Phone + 3-4 Onsite) |
| **Hiring Timeline** | 6-12 weeks (known for slow process) |
| **Difficulty** | Very Hard |
| **Rejection Rate** | Very High (~85-90%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 60-90 min | Google Hiring Assessment (GHA) | Online assessment, mandatory gateway |
| 2 | 30 min | Recruiter Screen | Background, level calibration |
| 3 | 45 min | Technical Phone Screen | 1-2 DSA problems, must code in Google Docs |
| 4 | 45 min | DSA Round 1 (Onsite) | 1-2 problems, medium-hard |
| 5 | 45 min | DSA Round 2 (Onsite) | 1-2 problems, medium-hard |
| 6 | 45 min | System Design (Onsite) | Mandatory for L4+, optional for L3 |
| 7 | 45 min | Googliness/Behavioral | Culture fit, leadership, collaboration |

**Note**: L4 can have either 2 DSA + 1 SD + 1 Googliness OR 3 DSA + 1 Googliness

### DSA Questions & Topics
- **Difficulty**: Medium-Hard to Hard (stricter grading than other companies)
- **Coding Time**: ~36-38 min per round (after intros)
- **Topics**: Graphs, Trees, DP, Heaps, Trie, Greedy, Intervals, Topological Sort
- **Reported Problems (India 2025)**:
  - Min Heap of size K (Top K elements)
  - Topological Sorting + BFS
  - Line Sweep Algorithm with intervals
  - String rotation grouping (group anagram variant)
  - Shortest path with teleporters (BFS/Dijkstra variant)
  - Matrix traversal problems
  - Sliding window problems
  - Segment tree / BIT problems (rare but possible)

### System Design Questions
- Design Google Maps
- Design YouTube / Video Streaming
- Design Gmail
- Design Google Docs (collaborative editing)
- Design a web crawler
- Design a distributed task scheduler

### Behavioral (Googliness) Focus
- "Tell me about a time you resolved a conflict"
- "How do you handle ambiguity?"
- Leadership without authority
- Mentoring and helping others
- Navigating organizational challenges

### Unique Characteristics
- **Hiring committee review**: Even after onsites, a committee decides (adds weeks)
- **12-month cooldown** on rejection
- Production-ready code expected: handle ALL corner cases
- In-person interviews increasingly required (anti-AI-cheating measure)
- Google Docs for coding (no autocomplete, no IDE)
- Team matching happens AFTER hiring committee approval
- Even 1000 LC problems may not be enough if unlucky with question draw

---

## 3. DOORDASH

| Attribute | Details |
|-----------|---------|
| **Target Level** | E4 (SDE-2) / E5 (SDE-3) |
| **TC Range (US)** | E4: $275K-$370K (Base ~$174K + Stock ~$99K + Bonus ~$3K) |
| **Total Rounds** | 5-6 rounds across 2 days |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Hard |
| **Rejection Rate** | High (~70-75%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Recruiter Screen | Background, role fit |
| 2 | 60 min | Technical Coding Screen | HackerRank/CoderPad, 1-2 problems |
| **Day 1 Onsite** | | | |
| 3 | 60 min | API Design / Coding | Not standard LC; lots of implementation |
| **Day 2 Onsite** | | | |
| 4 | 60 min | System Design | Resiliency-focused |
| 5 | 60 min | Debugging (CodeCraft) | Fix bugs in provided code + unit tests |
| 6 | 45 min | AI Coding Round | Newer addition (2025) |
| 7 | 45 min | Hiring Manager | Behavioral + ownership |

### DSA Questions & Topics
- **Difficulty**: Medium (6 Easy, 14 Medium, 2 Hard in their pool)
- **Topics**: Arrays, Hash Tables, BFS/DFS, DP, Grid problems, Intervals
- **Reported Problems**:
  - Design HashMap (LC #706)
  - Longest Common Prefix (LC #14)
  - Jump Game (LC #55)
  - Longest Increasing Path in Matrix (LC #329)
  - Design Browser History (LC #1472)
  - Job Scheduling (Weighted Job Scheduling variant)
  - Dasher Max Profit (DP, similar to LC #1235)
  - BFS on grid (shortest path)
  - Round Robin algorithm implementation

### System Design Questions
- Design real-time order tracking system
- Design a food delivery dispatch system
- Design DoorDash search/restaurant discovery
- Design a notification system
- Resiliency and fault tolerance emphasis

### Debugging Round (CodeCraft)
- Given buggy code + unit tests
- Must identify bugs, fix them, and explain reasoning
- Round Robin algorithm bugs are common
- Practice with templates and test-driven debugging

### Behavioral Focus
- Ownership-driven culture
- "Tell me about a time you took initiative"
- Handling ambiguity in product decisions
- Collaboration and conflict resolution

### Unique Characteristics
- **Debugging round is unique to DoorDash**
- API Design round is NOT standard LeetCode
- Problems grounded in logistics and real-time systems
- Newer AI coding round added in 2025
- 2-day onsite format

---

## 4. APPLE

| Attribute | Details |
|-----------|---------|
| **Target Level** | ICT3 (SDE-2) / ICT4 (SDE-3) |
| **TC Range (India)** | ICT3: 47-84L (median ~62L); ICT4: 65L-1.5Cr |
| **Total Rounds** | 5-7 rounds |
| **Hiring Timeline** | 4-8 weeks |
| **Difficulty** | Hard |
| **Rejection Rate** | High (~75%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Recruiter Screen | Background, level calibration |
| 2 | 45-60 min | Phone Screen | 1-2 coding problems + system design discussion |
| 3 | 45 min | Coding Round 1 (Onsite) | DSA with performance constraints |
| 4 | 45 min | Coding Round 2 (Onsite) | DSA, sometimes domain-specific |
| 5 | 45 min | System Design (Onsite) | Apple ecosystem focused |
| 6 | 45 min | Domain/Team Fit (Onsite) | Team-specific technical deep dive |
| 7 | 30-45 min | Hiring Manager | Behavioral + past work |

### DSA Questions & Topics
- **Difficulty**: Medium (rarely Hard), but strict on correctness and memory behavior
- **Topics**: Arrays, Trees, Graphs, Concurrency, Linked Lists
- **Reported Problems**:
  - Trapping Rain Water (LC #42) — confirmed from your interview_exp.txt
  - Thread-safe priority queue implementation
  - Evaluate Reverse Polish Notation (LC #150)
  - Container With Most Water (LC #11)
  - First Missing Positive (LC #41)
  - Concurrency problems (thread-safe data structures)

### System Design Questions
- Design a secure file sync for iCloud
- Design Apple Music streaming
- Design Apple Push Notification Service
- Design privacy-preserving analytics
- **CQRS pattern** — directly asked (from your interview_exp.txt)
- On-device constraints, privacy rules, energy efficiency are design constraints

### Behavioral Focus
- Collaboration across teams
- Privacy-first thinking
- Attention to user experience
- Past experience with hardware-software integration

### Unique Characteristics
- **Privacy is a design constraint from the start** (not an afterthought)
- Team-specific: iOS roles need Swift/Obj-C, OS roles need C++
- Apple ecosystem knowledge matters (iCloud, Siri, HealthKit, etc.)
- System design is Apple-specific, not generic distributed systems
- Confirm your level (ICT3 vs ICT4) BEFORE starting interviews
- IST timezone interviews for India candidates

---

## 5. ORACLE (OCI)

| Attribute | Details |
|-----------|---------|
| **Target Level** | IC3 (SDE-2) / IC4 (SDE-3) |
| **TC Range (India)** | IC3: 25-45L; IC4: 35-60L |
| **Total Rounds** | 5 rounds across 2 days |
| **Hiring Timeline** | ~30 days average |
| **Difficulty** | Medium |
| **Rejection Rate** | Moderate (~50-60%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 45-60 min | Screening Round | Resume discussion + 2 DSA questions (by PMTS/Tech Lead) |
| 2 | 60 min | Technical Round 1 | DSA + System Design |
| 3 | 60 min | Technical Round 2 | DSA + Domain Knowledge |
| 4 | 45 min | Hiring Manager Round | Hypothetical scenarios + behavioral |
| 5 | 45 min | Bar Raiser Round | Cross-team evaluation |

**Format**: 2 rounds per day, all 4 loop rounds in 2 days. You won't know the round type until it starts.

### DSA Questions & Topics
- **Difficulty**: Medium
- **Language**: Java required (they don't let you code in other languages for DSA)
- **Reported Problems**:
  - Longest Increasing Subsequence in O(n) (LC #300 variant)
  - Backtracking problems
  - Priority Queue / Heap problems
  - Array manipulation (medium difficulty)
  - HashMap internals (Java-specific deep dive)

### System Design Questions
- Design a notification system
- Design a job scheduler
- Discussion on cloud infrastructure patterns (OCI-specific)

### Behavioral Focus
- Hypothetical scenario questions
- Past project deep dives
- Team collaboration

### Unique Characteristics
- Java is mandatory for coding rounds
- Interview process described as "not industry standard" by some candidates
- Random question types — you may not know if it's DSA or SD until the round starts
- Bar Raiser round similar to Amazon
- OCI teams focus on cloud infrastructure

---

## 6. ZERODHA

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 |
| **TC Range (India)** | 30-90L (wide range; median ~50L for experienced) |
| **Total Rounds** | 3-5 rounds |
| **Hiring Timeline** | 2-4 weeks |
| **Difficulty** | Medium-Hard |
| **Rejection Rate** | High (very selective, small team) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | - | Take-home Assignment | Practical coding task |
| 2 | 60 min | Technical Round 1 | DSA + CS Fundamentals |
| 3 | 60 min | Technical Round 2 | System Design + Domain |
| 4 | 45 min | Cultural Fit / Founder Round | Values alignment |

### DSA Questions & Topics
- **Difficulty**: Medium
- **Topics**: Arrays, Strings, Linked Lists, Trees, Pattern Matching
- **Reported Problems**:
  - Array operations, subarray properties
  - String pattern matching
  - Reversing linked lists, cycle detection, merge sorted lists
  - Tree traversals (in/pre/post-order), LCA, BST balancing
  - Remove nth node from end of linked list

### System Design Questions
- Design a stock trading platform
- Design a real-time market data system
- Design order matching engine
- Financial domain systems

### Behavioral Focus
- "Be honest — acknowledge when you don't know"
- First-principles thinking
- Interest in financial markets/trading
- Small team culture fit

### Unique Characteristics
- Very small engineering team (~30-50 engineers)
- Golang + Kite Connect stack
- Strong emphasis on Golang proficiency
- Financial domain knowledge is a plus
- Remote-friendly (Bangalore HQ)
- Interviewers described as "nice"

---

## 7. PAYPAL

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 / SDE-3 |
| **TC Range (India)** | SDE-2: 24-40L; SDE-3: 35-55L |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Medium |
| **Rejection Rate** | Moderate (~50%) |

### Round Breakdown (SDE-2)

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 60-90 min | Online Assessment | HackerRank, 3 questions (easy-medium) |
| 2 | 60 min | DSA Round 1 | LC Medium/Hard |
| 3 | 60 min | DSA + System Design | Architecture discussion + coding |
| 4 | 45 min | Managerial Round | Behavioral + project deep dive |

### Round Breakdown (SDE-3)

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 60-90 min | Online Assessment | HackerEarth, 3 questions (easy-medium) |
| 2 | 45 min | System Design | Design Google Calendar/Outlook (HLD + API + DB Schema) |
| 3 | 60 min | Technical Round | DSA + Java deep dive |
| 4 | 45 min | Technical Round | Domain knowledge + architecture |
| 5 | 45 min | Managerial Round | Behavioral |

### DSA Questions & Topics
- **Difficulty**: Medium-Hard
- **Topics**: DP, Stack/Queue, String manipulation, Graphs, Topological Sort
- **Reported Problems**:
  - Find elements occurring more than once
  - Elements appearing more than n/k times in array
  - Lowest Common Ancestor (LCA) with parent pointers
  - HashMap internals (Java-specific)
  - HashMap vs HashTable differences

### System Design Questions
- Design Splitwise
- Design Google Calendar / Outlook
- Circuit breaker patterns
- Payment processing systems

### Behavioral Focus
- Project architecture deep dives
- Design trade-offs in past work
- Leadership and mentoring

### Unique Characteristics
- OA platform: HackerRank (SDE-2) or HackerEarth (SDE-3)
- Java deep-dive questions common (HashMap internals, etc.)
- Candidates can request to shuffle round order
- Backend system design knowledge expected even for frontend roles
- Chennai and Bangalore offices

---

## 8. ZOMATO

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 |
| **TC Range (India)** | 30-47L (median ~35L) |
| **Total Rounds** | 3-4 rounds |
| **Hiring Timeline** | 2-4 weeks |
| **Difficulty** | Medium |
| **Rejection Rate** | Moderate (~55%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 60 min | Technical/DSA Round | Projects + DSA + CS Fundamentals |
| 2 | 60 min | System Design / LLD | Geo-based systems, distributed systems |
| 3 | 60 min | Hiring Manager Round | Projects + design principles + DBMS |

### DSA Questions & Topics
- **Difficulty**: Medium
- **Topics**: Strings, Arrays, Tries, Rate Limiting, Redis
- **Reported Problems**:
  - Rate limiter for API gateway (optimized with Redis)
  - String/array problems with Trie optimization
  - SQL queries on schemas
  - Basic DBMS questions (isolation levels)

### System Design Questions
- Design a geo-based delivery system (Geohashing, Quad Trees)
- Design a real-time restaurant tracking system
- Design a high-availability food ordering system
- Design a rate limiter

### Behavioral Focus
- Project discussions (what, why, how)
- Websockets and authentication knowledge
- SQL vs NoSQL trade-offs
- Database indexing and isolation levels

### Unique Characteristics
- **Geo-based systems are a specialty** (geohashing, quad trees)
- Interviewers described as "chill and wholesome"
- Strong focus on SQL/DBMS knowledge
- Redis knowledge is valued
- Networking fundamentals tested (websockets, auth)
- Gurgaon HQ

---

## 9. SAMSARA

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 (Senior SWE II) |
| **TC Range** | India: 40-93L; US: $170K-$220K |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | ~20-23 days average |
| **Difficulty** | Medium |
| **Rejection Rate** | Moderate (~55%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Recruiter Screen | Background, motivation, projects |
| 2 | 60 min | Technical Coding Screen | CoderPad, practical problem-solving |
| 3 | 60 min | Onsite - Coding | DSA Medium-Hard |
| 4 | 60 min | Onsite - System Design | IoT/real-time systems |
| 5 | 45 min | Onsite - Behavioral | Culture fit, past experiences |

### DSA Questions & Topics
- **Difficulty**: Easy-Medium (practical focus)
- **Topics**: Counting Sort, String Parsing, Arrays
- **Reported Problems**:
  - Count sort variant
  - Parse string to insert HTML tags at punctuation points
  - Practical (not algorithmic-heavy) problems

### System Design Questions
- Design real-time IoT data pipeline
- Design vehicle tracking system
- Design sensor data aggregation platform
- Real-time and IoT-style systems emphasis

### Behavioral Focus
- Projects you're proud of
- Challenges faced and how you overcame them
- Alignment with Samsara's IoT mission

### Unique Characteristics
- IoT/real-time systems domain
- Go, Python, Kafka, Kubernetes are key technologies
- Practical coding problems over theoretical DSA
- Bangalore office for India roles
- Relatively fast hiring process

---

## 10. NVIDIA

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 (IC3/IC4) |
| **TC Range (India)** | IC3: 40-70L; IC4: 60-1.2Cr (median ~67L) |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | 4-6 weeks |
| **Difficulty** | Medium-Hard |
| **Rejection Rate** | Moderate (~60%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 60 min | Technical Round 1 | 3 coding questions + C++ output questions |
| 2 | 60 min | Technical Round 2 | DSA + domain-specific |
| 3 | 45 min | Logical / Math Round | Probability, selection, mathematical reasoning |
| 4 | 45 min | Project Discussion | Past work, challenges, what you learned |
| 5 | 30 min | Hiring Manager | Behavioral |

**Note**: All invites sent upfront; no elimination between rounds. Results after all rounds complete.

### DSA Questions & Topics
- **Difficulty**: Medium
- **Language**: C++ often preferred (C++ output questions on constructor/destructor)
- **Reported Problems**:
  - Kth largest element in BST (LC #230 variant)
  - Keys and Rooms (LC #841)
  - Linked list problems with scaling for k > 2
  - C++ specific: constructor/destructor output questions

### System Design Questions
- GPU pipeline design
- Parallel computing architecture
- Graphics rendering pipeline
- Domain-specific to NVIDIA's work

### Behavioral Focus
- Projects you're proud of
- Challenges faced and what you learned
- Interest in GPU/parallel computing

### Unique Characteristics
- **C++ is heavily preferred** (constructor/destructor questions)
- Math/probability round is unique
- No elimination between rounds
- GPU/CUDA/parallel computing knowledge is a huge plus
- Strong systems programming focus

---

## 11. xAI

| Attribute | Details |
|-----------|---------|
| **Target Level** | Software Engineer |
| **TC Range (US)** | $213K-$970K (median ~$660K) |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | 2-6 weeks (fast-paced) |
| **Difficulty** | Very Hard |
| **Rejection Rate** | Very High (~85%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | - | Online Assessment | Can be 100 questions (!) or standard OA |
| 2 | 15 min | Electronic Interview | Quick Q&A, concise answers expected |
| 3 | 60 min | Algorithms + DS | Strong coding under pressure |
| 4 | 60 min | System Design | Filesystem design, infrastructure |
| 5 | 60 min | Live Coding / ML | Production-level code with concurrency |

### DSA Questions & Topics
- **Difficulty**: Hard
- **Languages**: Python/C++ preferred
- **Topics**: Algorithms, Data Structures, Concurrency, Filesystem Design
- **Focus**: Problem solving + reasoning > syntax
- Production-level code implementation on the spot
- Concurrency requirements in live coding

### System Design Questions
- Filesystem design and implementation
- Distributed training infrastructure
- Real-time data processing pipelines
- AI workload orchestration

### Additional Requirements
- Calculus, Linear Algebra, Probability knowledge
- ML fundamentals (depending on role)
- Research-oriented discussion based on resume

### Unique Characteristics
- **Insane work culture**: "Coding >= x for all x" motto
- Long hours expected; urgency and speed valued
- OA can be 100 questions (unprecedented)
- 15-minute electronic interview is unique
- Very fast, flexible, deceptively deep interview process
- Production-level code expected (not interview puzzles)
- Strong Python/C++ expected

---

## 12. TESLA

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 |
| **TC Range (US)** | $120K-$200K + equity upside |
| **Total Rounds** | 5-6 rounds |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Medium (easier than FAANG) |
| **Rejection Rate** | Moderate (~55%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | - | Online Assessment (Codility) | 3 LC-style questions |
| 2 | 45-60 min | Phone Screen 1 | OA review + follow-ups + resume |
| 3 | 45-60 min | Phone Screen 2 (HM) | Behavioral, past experience, motivation |
| 4 | 45 min | Onsite - Coding 1 | DSA problem solving |
| 5 | 45 min | Onsite - Coding 2 | DSA + domain-specific |
| 6 | 45 min | Onsite - System Architecture | Design a system for given scenario |

### DSA Questions & Topics
- **Difficulty**: Easy-Medium (easier than FAANG)
- **Language**: Python strongly recommended (required for OA)
- **Topics**: Sorting, Two Pointers, Arrays, Strings, Hash Maps
- **Reported Problems**:
  - Two Sum (LC #1)
  - Reverse Linked List (LC #206)
  - Palindrome checking
  - Tesla charging station shortest distance (custom)
  - Array manipulation problems

### System Design Questions
- Design Tesla charging station network
- Design autonomous vehicle data pipeline
- Design real-time fleet management
- Focus on reasoning process, not optimal solution

### Behavioral Focus
- Passion for Tesla's mission
- Past experience and challenges
- Motivation for joining Tesla

### Unique Characteristics
- **Python required for OA** (Codility platform)
- Problems are easier than FAANG
- Tesla-specific domain problems (charging networks, fleet management)
- Reasoning process valued over optimal solutions
- Equity upside can be significant

---

## 13. BLOOMBERG

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 / SDE-3 |
| **TC Range (India)** | SDE: 40-53L; Senior SDE: 51-80L (median ~71L) |
| **Total Rounds** | 3-4 rounds (2-hour session format) |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Medium-Hard |
| **Rejection Rate** | Moderate (~55-60%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | - | Online Assessment | Coding + problem solving |
| 2 | 45-60 min | Phone Screen | DSA + behavioral |
| 3 | ~2 hours | Onsite (3 rounds in 1 session) | DSA + System Design + Behavioral |

**Onsite Sub-rounds:**

| Sub-round | Focus |
|-----------|-------|
| A | DSA: 2 medium LC or 1 medium + 1 hard |
| B | System Design: Practical, endpoint-level design |
| C | Behavioral: Bloomberg mission, genuine interest |

### DSA Questions & Topics
- **Difficulty**: Medium-Hard
- **Patterns**: Two Pointers, Backtracking, DP (higher than average), Binary Trees
- **SDE-2 Focus**: Optimization, design patterns, medium-hard problems, LLD (OOP)
- **SDE-3 Focus**: High-level scalable systems
- **Reported Problems**:
  - Binary Tree questions
  - Two Pointers problems
  - Dynamic Programming (more frequent than at other companies)
  - Backtracking problems

### System Design Questions
- Design endpoints with scalability
- Caching layers (Redis, in-memory cache)
- Financial data streaming systems
- Bloomberg Terminal features

### Behavioral Focus
- **Genuine interest in Bloomberg's mission is CRITICAL**
- Why Bloomberg specifically?
- Collaboration and communication
- This is what decides offers (not just technical skill)

### Unique Characteristics
- **Behavioral fit is make-or-break** (not just technical)
- 3 rounds often done in a single 2-hour session
- DP problems more common than at other companies
- Financial domain knowledge is a plus
- Pune and Bangalore offices in India
- SDE-2 emphasizes LLD/OOP more than HLD

---

## 14. DEUTSCHE BANK

| Attribute | Details |
|-----------|---------|
| **Target Level** | AVP (Assistant Vice President) / VP Technology |
| **TC Range (India)** | AVP: 28-46L (median ~39L); VP: 45-70L |
| **Total Rounds** | 3-4 rounds |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Easy-Medium |
| **Rejection Rate** | Low-Moderate (~40%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 90 min | Online Coding Test | 3 questions (easy, medium, hard) |
| 2 | 20 min | Situational Judgement Test (SJT) | 18 scenario-based questions |
| 3 | 60 min | Technical Interview | 2 interviewers, project deep dive, tech stack |
| 4 | 10 min | HR Round | Culture fit, salary expectations |

### DSA Questions & Topics
- **Difficulty**: Easy-Medium
- **Reported Problems**:
  - Factorial of a number
  - Middle element in linked list
  - String to integer conversion
  - Design schedulers without if-else (Strategy pattern)

### System Design Questions
- Design a scheduler for different regions
- Banking transaction systems
- Financial reporting systems

### Behavioral Focus
- Cultural fit
- Salary expectations
- Decision-making in work scenarios (SJT)

### Unique Characteristics
- **SJT (Situational Judgement Test) is unique**
- Relatively easy technical bar compared to product companies
- Focus on Java/Spring Boot for backend roles
- Pune, Bangalore, Jaipur offices
- Good for financial stability but lower TC than product companies
- Layoff concerns exist

---

## 15. ANTHROPIC

| Attribute | Details |
|-----------|---------|
| **Target Level** | Software Engineer |
| **TC Range (US)** | $550K-$759K (median ~$582K) |
| **Total Rounds** | 6 rounds |
| **Hiring Timeline** | 3-5 weeks |
| **Difficulty** | Very Hard |
| **Rejection Rate** | Very High (~85-90%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Recruiter Call | Background, motivation, role fit |
| 2 | 90 min | Take-home Coding Assessment | CodeSignal, progressive 4-level task |
| 3 | 60 min | Hiring Manager Deep Dive | Project review + technical depth |
| 4 | 45-55 min | Onsite - Coding | Implementation-heavy |
| 5 | 45-55 min | Onsite - System Design | AI infrastructure focused |
| 6 | 45-55 min | Onsite - Technical Project Deep Dive | Past work analysis |
| 7 | 45-55 min | Onsite - Behavioral | AI safety, ethics, collaboration |

### Coding Assessment Details
- **90-minute take-home on CodeSignal**
- Progressive complexity across 4 levels
- Must pass all tests at Level N to unlock Level N+1
- **Example**: Build in-memory database: L1 = SET/GET/DELETE, L2 = Filtered scans, L3 = TTL with timestamps, L4 = File compression/decompression
- Tests: clean APIs, modularity, state management, debugging, extensibility

### System Design Questions
- AI infrastructure focused (not generic)
- Novel problems with no standard "correct" answer
- Design LLM serving infrastructure
- Design model training pipeline
- Classic infrastructure problems with AI framing

### Behavioral Focus
- **AI safety-first decisions** are tested directly
- "Tell me about a time you made a safety-first decision in a project"
- AI ethics, data protection, knowledge sharing
- More conversational than traditional behavioral rounds

### Unique Characteristics
- **Take-home assessment with progressive levels is unique**
- Practical engineering skill > interview-game fluency
- Implementation-heavy: clean APIs, modularity, state management
- AI safety questions are mission-critical
- Very broad questions with incredibly in-depth follow-ups
- No standard answers; novel infrastructure problems
- Highest TC among all companies listed here (for US roles)

---

## 16. OPENAI

| Attribute | Details |
|-----------|---------|
| **Target Level** | Software Engineer (L5 equivalent) |
| **TC Range (US)** | $200K-$860K+ (base $200K-$530K + significant equity) |
| **Total Rounds** | 5-7 rounds |
| **Hiring Timeline** | ~1 month |
| **Difficulty** | Hard (rated 3.2/5) |
| **Rejection Rate** | Very High (~80-85%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 30 min | Phone Screen | HM or recruiter |
| 2 | 60 min | Coding Screen | Practical coding problems |
| 3 | 60 min | Project Review | Past work deep dive |
| 4 | 60 min | System Design | Infrastructure-level |
| 5 | 60 min | Additional Coding | Medium-Hard LC |
| 6 | 60 min | Hiring Manager/Behavioral | Culture, initiative, self-direction |

**Note**: May include pair coding, take-home, or technical tests depending on team.

### DSA Questions & Topics
- **Difficulty**: Medium-Hard
- **Style**: More practical than algorithmic; work-related problems
- **Reported Problems**:
  - Alien Dictionary (LC #269) — graph-based
  - Practical coding about the work you'll do
  - Statistics and ML questions (team-dependent)

### System Design Questions
- Design CI system (like GitHub Actions)
- Job scheduling with dependency management
- Concurrent execution models
- Model deployment infrastructure
- Fine-tuning pipeline design

### Behavioral Focus
- Self-driven, take initiative
- "How do you push things forward?"
- Strong communication and collaboration
- High-quality code and good test coverage

### Unique Characteristics
- Assessment format varies by team (pair coding, take-home, or test)
- Practical coding > pure algorithmic
- ML/Statistics questions possible depending on team
- Self-direction and initiative are heavily weighted
- Equity can 2-3x total compensation

---

## 17. FLIPKART

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 / SDE-3 |
| **TC Range (India)** | SDE-2: 30-44L (median ~34L); SDE-3: 45-65L |
| **Total Rounds** | 4 rounds |
| **Hiring Timeline** | 2-4 weeks |
| **Difficulty** | Hard |
| **Rejection Rate** | High (~70%) — "very selective, failing most engineers" |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 90 min + 30 min review | Machine Coding Round | Working code in 90 min, then 30 min review |
| 2 | 60 min | DSA Round | 3 questions, medium-hard |
| 3 | 60 min | System Design / LLD | Class diagrams, high modularity, low coupling |
| 4 | 45-60 min | Hiring Manager Round | Projects, DBMS, Kafka, indexing |

### Machine Coding Round (Critical Round)
- **90 minutes to write fully working code**
- Must follow OOP principles, SOLID design, design patterns
- Code must be easily extendable, readable, modular
- Exception handling required
- **Java is preferred language**
- **Common Problems**:
  - Snake and Ladder game
  - Parking Lot Manager
  - Tic Tac Toe
  - Splitwise
  - Token Bucket Rate Limiter
  - Trello Board
  - Movie Ticket Booking System

### DSA Questions & Topics
- **Difficulty**: Medium-Hard (3 questions in 1 round)
- **Topics**: Arrays, Trees, Graphs, DP
- **Reported**: LeetCode medium-hard problems

### System Design Questions
- Design a booking system
- Design a cache system
- Design a charging station system
- Class diagrams with high modularity and low coupling

### HM Round Topics
- Latest project deep dive
- Database indexing (B-Tree, Hash index)
- SQL vs NoSQL trade-offs
- Kafka (partitioning, consumer groups, offset management)

### Unique Characteristics
- **Machine Coding round is the most important and unique differentiator**
- Java preferred; OOP + SOLID + Design Patterns are mandatory
- Machine coding problems available on workat.tech and GitHub
- Recruiter contact often through LinkedIn Google Forms
- Bangalore HQ
- Very selective process

---

## 18. PHONEPE

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 |
| **TC Range (India)** | 44-61L first year (Base ~44L + Sign-on ~9L + Retention ~8L + ESOPs ~$50K/4yr) |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | 3-4 weeks |
| **Difficulty** | Hard |
| **Rejection Rate** | High (~65-70%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | ~60 min | Take-home Machine Coding | CodeSignal, build an application |
| 2 | 45-60 min | Machine Code Review | F2F discussion of submitted solution |
| 3 | 60 min | PSDS (Problem Solving DS) | 2 DSA problems (easy-medium) |
| 4 | 60 min | System Design | HLD: scalability, microservices, trade-offs |
| 5 | 45 min | Hiring Manager Round | Behavioral + project deep dive |

### Machine Coding Details
- Take-home on CodeSignal
- Build an application from scratch in ~1 hour
- Can make changes offline within time limit
- Code must be executable
- Followed by F2F review where design decisions are discussed

### DSA Questions & Topics
- **Difficulty**: Easy-Medium (but also LC Hard reported)
- **Reported Problems**:
  - Regex matching with '.' and '*' (LC #10)
  - Remove K Digits to get smallest number (LC #402)
  - Smallest Range Covering Elements from K Lists (LC #632)
  - 2 easy-medium problems per round

### System Design Questions
- Payment system design
- Scalability and microservices architecture
- Database trade-offs
- Real-world applicability focus

### Behavioral Focus
- Past project discussions
- Technical depth and reasoning

### Unique Characteristics
- **Take-home machine coding on CodeSignal is the entry gate**
- Machine coding review is a separate round (unique)
- DSA can range from easy to hard
- Practice 50-100 LC Hard problems recommended
- Bangalore HQ

---

## 19. SWIGGY

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 / SDE-3 |
| **TC Range (India)** | SDE-2: 30-47L (median ~35L); SDE-3: 45-60L |
| **Total Rounds** | 4-5 rounds |
| **Hiring Timeline** | 2-4 weeks |
| **Difficulty** | Medium-Hard |
| **Rejection Rate** | Moderate-High (~60%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 90 min | HackerRank OA | 2-3 medium DSA problems |
| 2 | 60 min | DSA Round 1 | Graph + Array problems |
| 3 | 60 min | DSA Round 2 / Machine Coding / LLD | Varies: can be MC or additional DSA |
| 4 | 60 min | System Design (HLD) | Food delivery domain |
| 5 | 45 min | Hiring Manager Round | Behavioral + HR |

### DSA Questions & Topics
- **Difficulty**: Medium-Hard
- **Topics**: Graphs, Arrays, Linked Lists, Recursion, Palindromes, Grids
- **Reported Problems**:
  - Tail recursion problems
  - Linked list intersection
  - Frequency counting in sorted arrays
  - Longest palindromic substring (LC #5)
  - Grid problems: finding largest possible squares by removing bars
  - Graph traversal problems

### System Design Questions
- Design a catalog system (restaurants, items, categories, variants, add-ons)
- Design a food delivery dispatch system
- Robustness and fallback mechanisms
- Real-world Swiggy domain problems

### LLD / Machine Coding
- When present, it's a separate round
- OOP + SOLID + Design Patterns expected
- Clean, modular, extensible code

### Behavioral Focus
- Past project discussions
- Handling system failures and fallbacks
- Golang experience valued

### Unique Characteristics
- **Golang experience is highly valued**
- Food delivery domain knowledge helps
- OA on HackerRank (90 min, 2-3 problems)
- Concurrency knowledge tested for experienced roles
- Bangalore HQ
- Hiring through various formats (PS/DS, MC, LLD, HM variations)

---

## 20. RAZORPAY

| Attribute | Details |
|-----------|---------|
| **Target Level** | SDE-2 |
| **TC Range (India)** | 34-41L (Base ~24-36L + ESOPs ~10-18L/4yr + Relocation ~2L) |
| **Total Rounds** | 2-3 rounds |
| **Hiring Timeline** | 2-3 weeks |
| **Difficulty** | Medium-Hard |
| **Rejection Rate** | Moderate (~55%) |

### Round Breakdown

| Round | Duration | Type | Details |
|-------|----------|------|---------|
| 1 | 90-120 min | Machine Coding Round | Implement a system from scratch |
| 2 | 60 min | LLD / HLD Round | Low-level or high-level design |
| 3 | 45 min | Manager Round | Behavioral + project discussion |

### Machine Coding Questions
- **Critical Round** — must complete all functional requirements
- **Reported Problems**:
  - Implement a Version Control System (VCS) like Git: add files, commit, branch, rollback
  - Design a Rating System (LLD)
  - Design Zepto-like system (HLD)
  - Design a URL shortener
- Code must be extensible and modular
- **AI Code Assistants (ChatGPT) allowed for prototyping** in some cases

### System Design Questions
- Design URL shortener
- Design Zepto (quick commerce)
- Design payment processing system
- LLD + HLD both tested

### Behavioral Focus
- Past project deep dives
- Technical decision-making rationale

### Unique Characteristics
- **Shortest interview process (2-3 rounds only)**
- Machine coding is the make-or-break round
- AI assistants may be allowed (confirm with recruiter)
- Extensible, modular code is heavily weighted
- Payments domain knowledge is a plus
- Bangalore HQ
- Good for Phase 1 target (mid-tier product company)

---

## 21. CROSS-COMPANY ANALYSIS

### Company Tier Classification (for Jayanti's Prep)

| Tier | Companies | Avg TC (India) | Interview Difficulty |
|------|-----------|---------------|---------------------|
| **Tier 1 (Dream)** | Google, Stripe, Apple, Anthropic, OpenAI, xAI | 62L-95L+ (India) / $500K+ (US) | Very Hard |
| **Tier 2 (Strong)** | DoorDash, Bloomberg, NVIDIA, Flipkart, PhonePe | 34L-80L | Hard |
| **Tier 3 (Target)** | Swiggy, Razorpay, Zomato, PayPal, Samsara, Tesla | 30L-47L | Medium-Hard |
| **Tier 4 (Safety)** | Oracle, Deutsche Bank, Zerodha | 25L-50L | Medium |

### Interview Format Comparison

| Company | OA | Machine Coding | DSA | System Design | LLD | Debugging | Behavioral | Total Rounds |
|---------|-----|---------------|-----|--------------|-----|-----------|-----------|-------------|
| **Stripe** | - | - | 1 | 1 | - | 1 (Bug Bash) | 1 | 6 |
| **Google** | 1 (GHA) | - | 2-3 | 1 | - | - | 1 | 5-6 |
| **DoorDash** | - | - | 2 | 1 | - | 1 (CodeCraft) | 1 | 5-6 |
| **Apple** | - | - | 2 | 1 | - | - | 1-2 | 5-7 |
| **Oracle** | - | - | 2 | 1 | - | - | 2 | 5 |
| **Zerodha** | - | 1 (take-home) | 1 | 1 | - | - | 1 | 3-5 |
| **PayPal** | 1 | - | 2 | 1 | - | - | 1 | 4-5 |
| **Zomato** | - | - | 1 | 1 | - | - | 1 | 3-4 |
| **Samsara** | - | - | 1 | 1 | - | - | 1 | 4-5 |
| **NVIDIA** | - | - | 2 | - | - | - | 1+Math | 4-5 |
| **xAI** | 1 (100Q!) | - | 1 | 1 | - | - | - | 4-5 |
| **Tesla** | 1 (Codility) | - | 2 | 1 | - | - | 1 | 5-6 |
| **Bloomberg** | 1 | - | 1 | 1 | 1 | - | 1 | 3-4 |
| **Deutsche Bank** | 1+SJT | - | 1 | - | - | - | 1 | 3-4 |
| **Anthropic** | 1 (take-home) | - | 1 | 1 | - | - | 1 | 6 |
| **OpenAI** | varies | - | 1-2 | 1 | - | - | 1 | 5-7 |
| **Flipkart** | - | 1 (90min) | 1 | 1 | - | - | 1 | 4 |
| **PhonePe** | - | 1 (take-home) | 1 | 1 | - | - | 1 | 4-5 |
| **Swiggy** | 1 (HR) | 0-1 | 1-2 | 1 | 0-1 | - | 1 | 4-5 |
| **Razorpay** | - | 1 (90-120min) | - | 1 | 1 | - | 1 | 2-3 |

### Companies That Need Machine Coding Prep
- Flipkart (90 min, Java, OOP mandatory)
- PhonePe (take-home on CodeSignal)
- Razorpay (90-120 min, extensible code)
- Swiggy (sometimes)
- Zerodha (take-home assignment)

### Companies That Need Debugging/Bug Bash Prep
- Stripe (Bug Bash round)
- DoorDash (CodeCraft round)

### Language Requirements

| Company | Required/Preferred Language |
|---------|---------------------------|
| Oracle | Java (mandatory) |
| NVIDIA | C++ (preferred) |
| Tesla | Python (mandatory for OA) |
| Flipkart | Java (preferred) |
| xAI | Python/C++ |
| Zerodha | Golang |
| Swiggy | Golang (valued) |
| Apple | Swift/Obj-C (iOS), C++ (OS) |
| Others | Java/Python both fine |

---

## 22. PRIORITY DSA PROBLEMS

### Most Frequently Asked Across All 20 Companies

| # | Problem | LC # | Companies | Difficulty |
|---|---------|------|-----------|------------|
| 1 | Two Sum | 1 | Tesla, Google, PayPal | Easy |
| 2 | LRU Cache | 146 | Apple, Stripe, Google | Medium |
| 3 | Trapping Rain Water | 42 | Apple (confirmed), Google | Hard |
| 4 | Longest Palindromic Substring | 5 | Swiggy, Bloomberg | Medium |
| 5 | Merge Intervals | 56 | Google, DoorDash, Amazon | Medium |
| 6 | Container With Most Water | 11 | Apple (confirmed) | Medium |
| 7 | First Missing Positive | 41 | Apple (confirmed) | Hard |
| 8 | Evaluate RPN | 150 | Apple (confirmed) | Medium |
| 9 | Task Scheduler | 621 | DoorDash, Amazon | Medium |
| 10 | Top K Frequent Elements | 347 | Google, NVIDIA | Medium |
| 11 | Design HashMap | 706 | DoorDash | Easy |
| 12 | Jump Game | 55 | DoorDash | Medium |
| 13 | Longest Increasing Subsequence | 300 | Oracle | Medium |
| 14 | Kth Largest in BST | 230 | NVIDIA | Medium |
| 15 | Keys and Rooms | 841 | NVIDIA | Medium |
| 16 | Longest Common Prefix | 14 | DoorDash | Easy |
| 17 | Longest Increasing Path in Matrix | 329 | DoorDash | Hard |
| 18 | Design Browser History | 1472 | DoorDash | Medium |
| 19 | Remove K Digits | 402 | PhonePe | Medium |
| 20 | Smallest Range from K Lists | 632 | PhonePe | Hard |
| 21 | Regular Expression Matching | 10 | PhonePe | Hard |
| 22 | Alien Dictionary | 269 | OpenAI | Hard |
| 23 | Reverse Linked List | 206 | Tesla, Zerodha | Easy |
| 24 | Linked List Cycle | 141 | Zerodha | Easy |
| 25 | LCA of Binary Tree | 236 | PayPal, Zerodha | Medium |

### Topic Distribution Across Companies

| Topic | Frequency | Key Companies |
|-------|-----------|---------------|
| Arrays/Strings | Very High | All companies |
| Hash Maps | Very High | All companies |
| Trees/BST | High | Google, NVIDIA, Bloomberg, PayPal |
| Graphs (BFS/DFS) | High | Google, DoorDash, Swiggy |
| Dynamic Programming | High | Google, Bloomberg, DoorDash |
| Linked Lists | Medium | Tesla, Zerodha, NVIDIA |
| Two Pointers | Medium | Tesla, Bloomberg |
| Sliding Window | Medium | Google, Stripe |
| Topological Sort | Medium | Google, PayPal |
| Intervals/Line Sweep | Medium | Google, DoorDash |
| Backtracking | Medium | Oracle, Bloomberg |
| Heap/Priority Queue | Medium | Google, Oracle, Apple |
| Trie | Low-Medium | Zomato, Google |
| Concurrency | Low-Medium | Apple, xAI |
| Segment Trees | Low | Google (rare) |

---

## 23. PRIORITY SYSTEM DESIGN PROBLEMS

### Most Frequently Asked Across All 20 Companies

| # | Problem | Companies |
|---|---------|-----------|
| 1 | Design URL Shortener | Razorpay, Generic |
| 2 | Design Notification System | Oracle, DoorDash, Stripe |
| 3 | Design Rate Limiter | Zomato, Stripe |
| 4 | Design Payment System | Stripe, Razorpay, PayPal, PhonePe |
| 5 | Design Food Delivery System | Swiggy, Zomato, DoorDash |
| 6 | Design Real-time Order Tracking | DoorDash, Swiggy |
| 7 | Design Google Calendar | PayPal |
| 8 | Design Splitwise | PayPal |
| 9 | Design iCloud File Sync | Apple |
| 10 | Design YouTube/Video Streaming | Google |
| 11 | Design Google Maps | Google |
| 12 | Design Google Docs | Google |
| 13 | Design Web Crawler | Google |
| 14 | Design CI System (GitHub Actions) | OpenAI |
| 15 | Design LLM Serving Infrastructure | Anthropic |
| 16 | Design Booking System | Flipkart |
| 17 | Design Cache System | Flipkart, Stripe |
| 18 | Design Job Scheduler | Oracle, OpenAI |
| 19 | Design Stock Trading Platform | Zerodha |
| 20 | Design IoT Data Pipeline | Samsara |

### Machine Coding Problems to Practice

| # | Problem | Companies |
|---|---------|-----------|
| 1 | Snake and Ladder | Flipkart |
| 2 | Parking Lot | Flipkart |
| 3 | Splitwise | Flipkart, PayPal |
| 4 | Tic Tac Toe | Flipkart |
| 5 | Token Bucket Rate Limiter | Flipkart |
| 6 | Trello Board | Flipkart |
| 7 | Movie Ticket Booking | Flipkart |
| 8 | Version Control System (Git) | Razorpay |
| 9 | Rating System | Razorpay |
| 10 | In-memory Database | Anthropic |

---

## JAYANTI-SPECIFIC RECOMMENDATIONS

### Phase 1 Targets (Mar-Jun 2026) — Get First Offer

**Best Fit Companies (ordered by probability of success):**
1. **Razorpay** — Only 2-3 rounds, machine coding focused, Java-friendly, payments domain aligns with your GSTN experience
2. **Zomato** — 3 rounds, medium difficulty, values Redis/caching experience (your DistCacheUtil experience)
3. **Swiggy** — Golang valued (you have Golang experience), 4-5 rounds, medium-hard
4. **PayPal** — HackerRank OA gateway, Java deep dive plays to your strength, 4 rounds
5. **Deutsche Bank** — Easiest interviews, financial domain, safety net

### Phase 2 Targets (Jun-Sep 2026) — Dream Offer

**Target Companies (ordered by desirability):**
1. **Flipkart** — Machine coding is your ticket (practice OOP/SOLID in Java), strong India presence
2. **PhonePe** — Take-home coding aligns with your style, payments domain match
3. **Stripe** — Highest TC in India (95L), bug bash + practical coding
4. **Google** — Highest bar but highest reward, heavy DSA prep needed
5. **Apple** — CQRS experience from GSTN is directly relevant
6. **Bloomberg** — DP focus + financial domain match

### Your GSTN Experience Mapping

| GSTN Experience | Maps To | Relevant Companies |
|----------------|---------|-------------------|
| DistCacheUtil (JBoss DataGrid + EhCache) | Distributed Caching SD | Stripe, Flipkart, Zomato |
| Kafka Consumer Framework + DLQ | Event-driven architecture | Stripe, Swiggy, DoorDash |
| XA Transactions (Atomikos) | Distributed transactions | Stripe, PayPal, PhonePe |
| Case Workflow Engine (Strategy + Factory) | Design Patterns / Machine Coding | Flipkart, Razorpay, PhonePe |
| 14M taxpayers, 3B invoices/year | Scale metrics for SD | Google, Apple, Stripe |
| Redis experience | Caching layer design | Zomato, Bloomberg, Stripe |

### Critical Gaps to Fill

1. **LeetCode in Java**: Switch from C++ immediately. Oracle REQUIRES Java. Flipkart PREFERS Java.
2. **Machine Coding Practice**: Flipkart, Razorpay, PhonePe all need this. Practice Snake & Ladder, Parking Lot, VCS in Java.
3. **Debugging Practice**: For Stripe and DoorDash, practice finding bugs in open-source code.
4. **Golang Brush-up**: For Zerodha and Swiggy specifically.
5. **DP Deep Dive**: Bloomberg asks more DP than average. Google can ask anything.
6. **Geo-based Systems**: For Zomato/Swiggy (geohashing, quad trees).

---

*Last updated: March 25, 2026*
*Sources: Glassdoor, LeetCode Discuss, Medium, TeamBlind, Levels.fyi, Prepfully, InterviewQuery, Exponent, GeeksforGeeks, Onsites.fyi*
