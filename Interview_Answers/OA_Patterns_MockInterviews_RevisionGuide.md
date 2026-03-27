# OA Patterns, Mock Interviews, Revision & Study Schedules
## Comprehensive Research Guide for Jayanti's Interview Prep (March 2026)

---

# PART 1: ONLINE ASSESSMENT (OA) PATTERNS BY COMPANY

## Master OA Table

| Company | Platform | Questions | Time | Difficulty | Key Topics | Notes |
|---------|----------|-----------|------|------------|------------|-------|
| **Amazon** | HackerRank | 2 coding + work-style assessment | 70-90 min | Med-Hard | Sliding window, BFS/DFS, greedy, DP, two pointers | NOT standard textbook LC; real-world framing. 20-35% first-time pass rate. Also has work simulation. |
| **Google** | Google Docs / HackerRank | 1-2 coding | 60-90 min | Medium+ | Multi-constraint problems, edge cases, clean code | Partial credit matters. Combines multiple ideas per problem. |
| **Stripe** | HackerRank / CodeSignal | 1 problem with 3 sub-parts OR 2-3 problems | 60 min | Med-Hard | Arrays, strings, graphs, recursion, DP, real-world backend logic | Must solve Part 1 to unlock Part 2. Graded on correctness + efficiency + code clarity. |
| **Bloomberg** | HackerRank | 2 coding | 45 min | Medium | Arrays, strings, hash maps, trees, graphs, DP, recursion, divide-and-conquer | Language agnostic. No need to run code — logic > syntax. Bare-bones editor. |
| **DoorDash** | HackerRank | 2 coding (+ occasional SQL) | 90 min | Medium | Logic simulation, array/string manipulation, scheduling, graph traversal, greedy, heaps | Realistic engineering tasks. Brute-force too slow — need optimization. |
| **Flipkart** | HackerRank | 3 DSA problems | 60-90 min | Easy-Med to Med-Hard | Arrays, strings, sliding window, two pointers, trees, graphs, DP, backtracking | 1 easy-medium + 2 medium-hard. Java/Python preferred. |
| **Goldman Sachs** | HackerRank / CoderPad | 2 DSA + MCQs | 60-120 min | Med | Subarrays, strings, circular buffers, data structures, financial data patterns | Sometimes includes MCQs. Real-world financial framing. |
| **PayPal** | HackerRank | 2 coding + SQL + Java OOP MCQs | 80 min | Easy-Med | SQL (GROUP BY, HAVING, aggregates), Java OOP (abstract, inheritance), arrays, strings, DP | Easiest OA of the lot. 9 total questions but generous time. |
| **NVIDIA** | HackerRank | 2 DSA + MCQs | 75 min | Medium | Arrays, strings, trees, graphs, DP, sorting + domain-specific (CUDA, GPU, parallel computing) | C++ strongly preferred. Domain questions for GPU roles. |
| **Anthropic** | CodeSignal | 4-level progressive task | 60-90 min | Med-Hard | Implementation-heavy: bank transactions, business logic, progressive complexity | Very small question bank (~6 problems). AI use strictly prohibited. Must complete levels sequentially. |
| **OpenAI** | Varies by team | 1 problem with sub-parts | 60-75 min | Med-Hard | Production-oriented: serialization, spreadsheet APIs, graph problems, stateful components, debugging | NOT LeetCode-style. Focus on readable code, trade-offs, edge cases. May involve refactoring/debugging existing code. |

---

## Detailed Company OA Breakdowns

### Amazon OA
- **Format**: 2 coding questions (70-90 min) + Work Style Assessment + Work Simulation (role-dependent)
- **Key Patterns**: Sliding window, two pointers, BFS/DFS, greedy, DP
- **Critical Insight**: Questions are NOT standard textbook LeetCode. They wrap algorithmic challenges in real-world scenarios. Auto-grading evaluates across multiple dimensions.
- **Pass Rate**: 20-35% for technical roles (first attempt)
- **Prep**: Focus on Amazon-tagged LC problems, but practice translating real-world problems to algorithms

### Google OA
- **Format**: 1-2 coding problems on Google Docs or HackerRank
- **Key Insight**: Partial credit matters significantly. A clean solution handling most cases beats a messy brute-force. Problems combine multiple constraints rather than testing a single trick.
- **Focus**: Engineering judgment, correctness, edge cases, readable solutions
- **Prep**: Practice writing clean code without IDE autocomplete

### Stripe OA
- **Format**: 1 problem broken into 3 progressive sub-tasks (60 min) — must solve Part 1 to unlock Part 2, etc.
- **Key Insight**: Problems are real-world backend/system design logic, not pure DSA. Graded on correctness + efficiency + code clarity + edge case handling.
- **Common Problems**: Payment validation, modular arithmetic, graph reliability, revenue intervals
- **Prep**: Practice multi-part problems, focus on clean modular code

### Bloomberg OA
- **Format**: 2 problems, 45 min, HackerRank
- **Key Insight**: Language agnostic. Code does NOT need to compile — they look for logic and explanation. Bare-bones editor (no autocomplete).
- **Prep**: Practice 150-220 LC problems (Medium focus), Bloomberg-tagged. Practice without IDE.

### DoorDash OA
- **Format**: 2 coding + optional SQL, 90 min
- **Key Insight**: Mid-level difficulty but realistic engineering scenarios. Brute-force approaches deliberately too slow.
- **Common Patterns**: Sliding window (delivery windows), graph/shortest path (driver routes), DP/greedy (delivery delays), heap (K nearest), string parsing (order validation)
- **Prep**: Focus on optimization — reverse processing, two pointers, heaps

### Flipkart OA
- **Format**: 3 DSA problems, 60-90 min
- **Key Insight**: 1 easy-medium + 2 medium-hard. Process: OA -> 2 Technical -> Machine Coding -> HR
- **Common Problems**: Number of Islands, Trapping Rain Water, sliding window, two pointers
- **Prep**: Java preferred. Focus on clean optimized code + edge case testing.

### Goldman Sachs OA
- **Format**: 2 DSA + MCQs, 60-120 min (varies by region/program)
- **Key Insight**: Mixes applied problem-solving with financial domain framing (transaction patterns, risk modeling, data processing)
- **Common Problems**: Box formation, longest subarray with sum <= k, circular buffer/queue, string encoding
- **Prep**: Practice medium LC + understand real-world data processing scenarios

### PayPal OA
- **Format**: 9 questions total in 80 min — SQL + Java OOP + 2 coding problems
- **Key Insight**: Easiest OA among top companies. SQL focuses on GROUP BY, HAVING, aggregates. Java focuses on abstract classes, inheritance, encapsulation.
- **Prep**: Brush up on SQL fundamentals + Java OOP basics. Coding problems: House Robber-style DP, monotonic stack.

### NVIDIA OA
- **Format**: 2 DSA + MCQs, 75 min
- **Key Insight**: C++ strongly preferred. For GPU roles, expect CUDA/parallel computing domain questions.
- **Prep**: Practice LC medium in C++ (or Java). Understand memory hierarchies, parallelization if targeting GPU roles.

### Anthropic OA
- **Format**: 4-level progressive CodeSignal task, 60-90 min
- **Key Insight**: Very small question bank (~6 problems). Each level builds on previous. Implementation-heavy (e.g., build a bank with multiple transaction types). AI use strictly prohibited.
- **Prep**: Practice building small but complete systems. Focus on progressive complexity and clean architecture.

### OpenAI OA
- **Format**: Varies by team — 60-75 min, single problem with sub-parts
- **Key Insight**: Deliberately NOT LeetCode-style. Production-oriented — writing real code, handling edge cases, building meaningful components. May involve debugging/refactoring existing code.
- **Example Problems**: Alien Dictionary variant, KV store serialization, spreadsheet API with O(1) getCell
- **Prep**: Practice implementation problems, stateful systems, serialization. Focus on readable code and trade-offs.

---

# PART 2: MOCK INTERVIEW PLATFORMS & STRATEGIES

## Platform Comparison Table

| Platform | Type | Cost | Best For | Key Features |
|----------|------|------|----------|-------------|
| **Pramp** (now on Exponent) | Peer-to-peer, live | Free | Getting started, building confidence | Take turns as candidate/interviewer. Teaches what strong answers look like. |
| **Interviewing.io** | Live with FAANG engineers | $100-225/session | Realistic practice before real interviews | Anonymous. Senior/Staff/Principal engineers from FAANG. Detailed actionable feedback. |
| **PracHub** | AI-driven | Varies | High volume practice | Trained on thousands of real FAANG interview reports. Dynamic follow-up questions. |
| **Hello Interview** | AI + guides | Free + paid | System design + coding | Company-specific guides (OpenAI, Anthropic, etc.). Structured feedback. |
| **Exponent** | AI + peer + guides | $99/mo | All-around prep | Thousands of practice questions across coding, SD, PM. Mock interview matching. |
| **IGotAnOffer** | Coaching with FAANG engineers | $$$ | System design specifically | 4.95/5 rating from 20k+ reviews. Coaches from Google, Meta, Amazon. |
| **TechMockInterview** | Live with professionals | $$ | Targeted company prep | Professional interviewers, company-specific practice. |
| **Codemia** | Active practice platform | Varies | System design practice | Hands-on system design problems with interactive practice. |

## Mock Interview Strategy (Recommended Progression)

### Phase 1: Self-Practice (Weeks 1-4)
1. **Solo whiteboarding**: Pick a system design problem, set a 40-min timer, draw on paper/tablet
2. **Rubber duck explaining**: Talk through your DSA solution out loud as you code
3. **Record yourself**: Use phone to record your explanations, review for clarity
4. **Mirror practice**: Explain your GSTN architecture in front of a mirror (behavioral prep)

### Phase 2: Free Peer Practice (Weeks 5-8)
1. **Pramp**: 2-3 sessions/week. Both coding and system design available.
2. **LeetCode discuss**: Find study partners in discussion forums
3. **Discord communities**: Join coding interview prep servers for ad-hoc practice

### Phase 3: Paid Professional Practice (Weeks 9-12, pre-interview)
1. **Interviewing.io**: 2-3 sessions before target company interviews
2. **Company-specific coaching**: For Amazon LP rounds, system design deep dives
3. **Target**: Complete at least 5 mock interviews before real interviews (research shows this is the critical threshold)

## System Design Mock Interview Self-Practice Method

1. **Pick a problem** (e.g., "Design Uber")
2. **Set timer**: 40 minutes
3. **Follow the framework**:
   - 5-10 min: Requirements gathering (write functional + non-functional reqs)
   - 10-15 min: High-level architecture (draw boxes and arrows)
   - 15-20 min: Deep dive into 1-2 critical components
   - 5 min: Discuss trade-offs, bottlenecks, scaling
4. **Compare**: Check your design against Alex Xu / HelloInterview solutions
5. **Study the gap**: Note what you missed, add to Anki deck
6. **Redo from memory**: Next day, recreate the design without looking

---

# PART 3: REVISION & SPACED REPETITION SYSTEM

## The Science

- Spaced repetition boosts retention by 200-300% vs massed practice
- One dev: 200+ problems at 30% retention -> 80 problems with spaced reviews at 85% retention
- Key insight: Master the METHOD, not the specific answer. Derive solutions on the spot.

## Spaced Repetition Schedule for LeetCode

After solving a problem correctly:

| Review | When | Action |
|--------|------|--------|
| R1 | Next day | Solve from scratch (no looking) |
| R2 | Day 3 | Solve from scratch |
| R3 | Day 7 | Solve from scratch |
| R4 | Day 14 | Solve from scratch |
| R5 | Day 30 | Solve from scratch |
| R6 | Day 60 | Solve — if easy, you've learned it |

**Adjustment Rules**:
- If review feels very easy: double the interval (skip to next)
- If review feels hard: halve the interval (stay or go back)
- Once interval reaches 256 days: problem is learned for interview purposes

## Tools for Spaced Repetition

| Tool | Purpose | How to Use |
|------|---------|------------|
| **Anki** | Flashcards for concepts + patterns | Create cards for: pattern name, when to use, template code, time complexity |
| **DSA Prep (dsaprep.dev)** | Curated DSA with built-in spaced repetition | Filter by company (Google, Amazon, Meta). Automated tracking. |
| **Grind 75 Bot** | Telegram bot with SM2 algorithm | Sends daily LC problems based on spaced repetition schedule |
| **LeetRepeat (leetrepeat.com)** | LC-specific spaced repetition | Tracks your LC solutions and schedules reviews |
| **system-design-primer Anki deck** | 230+ system design flashcards | Import into Anki. Review 10-15 cards daily. |
| **DesignDeck (GitHub)** | 230+ system design flash cards | Open-source alternative to system-design-primer deck |

## What to Put on Anki Cards

### DSA Cards (create after solving each problem)
- **Front**: Problem name + brief description
- **Back**: Pattern used, approach in 3-4 bullet points, time/space complexity, key insight
- Do NOT put full code on cards — put the IDEA

### System Design Cards
- **Front**: "How does consistent hashing work?"
- **Back**: 3-4 bullet points explaining concept + when to use + trade-offs
- **Front**: "Design a URL shortener — what are the key components?"
- **Back**: High-level architecture diagram description + key decisions

### Java/Concept Cards
- **Front**: "What is double-checked locking?"
- **Back**: Pattern, why volatile is needed, code skeleton, when to use

## Weekly Revision Protocol

| Day | New Problems | Reviews | System Design | Behavioral |
|-----|-------------|---------|---------------|------------|
| Mon | 2 new LC | 3-4 reviews | - | - |
| Tue | 2 new LC | 3-4 reviews | Read 1 SD chapter | - |
| Wed | 2 new LC | 3-4 reviews | - | Practice 2 STAR stories |
| Thu | 2 new LC | 3-4 reviews | Design 1 system (40 min) | - |
| Fri | 1 new LC | 5-6 reviews (catch-up) | - | Practice 2 STAR stories |
| Sat | 3 new LC | 5-6 reviews | Design 1 system + compare | Mock interview (peer) |
| Sun | - | Review all flagged problems | Redo weak SD from memory | Review STAR bank |

---

# PART 4: DAILY STUDY SCHEDULES FROM SUCCESSFUL CANDIDATES

## Schedule A: Working Full-Time (Your Current Situation at GSTN)
**Total: 3-4 hours/day weekdays, 6-8 hours/day weekends = ~25-35 hrs/week**

### Weekday Schedule
```
06:00 - 06:30  Wake up, coffee, Anki review (15-20 cards)
06:30 - 07:30  LeetCode: 1 new problem + 1 review problem
07:30 - 08:30  Get ready, commute
08:30 - 18:00  GSTN work (use lunch for system design reading)
18:00 - 19:00  Commute (listen to system design podcast / review STAR stories mentally)
19:00 - 19:30  Dinner
19:30 - 20:30  System design study OR behavioral prep (alternating days)
20:30 - 21:00  LeetCode: 1 more problem or review
21:00 - 21:30  Wind down, light reading (company research)
```

### Weekend Schedule
```
07:00 - 07:30  Anki review
07:30 - 09:30  LeetCode: 3 problems (1 easy, 1 medium, 1 hard)
09:30 - 10:00  Break
10:00 - 12:00  System design: Full mock design session (40 min) + compare + study gaps
12:00 - 13:00  Lunch break
13:00 - 14:30  LLD practice OR Java deep-dive (multithreading, concurrency)
14:30 - 15:00  Break
15:00 - 16:30  Mock interview (Pramp/peer) OR behavioral STAR practice
16:30 - 17:00  Review and plan next week
17:00+         Rest, exercise, personal time
```

## Schedule B: Full-Time Prep (If You Take Leave/Resign)
**Total: 8-10 hours/day = ~60-70 hrs/week**

```
06:00 - 06:30  Wake up, Anki review (20-30 cards)
06:30 - 08:30  LeetCode Block 1: 2-3 problems (focus on weak topics)
08:30 - 09:00  Break, breakfast
09:00 - 11:00  System Design deep study (Alex Xu chapter + design from scratch)
11:00 - 11:15  Break
11:15 - 12:30  LLD practice (implement 1 design pattern or mini-system)
12:30 - 13:30  Lunch + light reading (company blogs, engineering posts)
13:30 - 15:00  LeetCode Block 2: 2 problems (contest-style, timed)
15:00 - 15:30  Break, walk
15:30 - 17:00  Mock interview OR behavioral prep (STAR stories + company research)
17:00 - 17:30  Anki review (new cards from today's study)
17:30 - 18:30  Review: re-solve problems that were hard today
18:30 - 19:30  Dinner + rest
19:30 - 20:30  Optional: watch system design video / read interview experiences
20:30+         Rest, exercise, sleep by 22:30
```

## Schedule C: "Average to Googler" Intensive 4-Week Plan
**Inspired by Milad Naseri's viral LinkedIn post**

### Week 1: Foundations
- Revise ALL data structures (arrays, linked lists, stacks, queues, trees, graphs, heaps, tries, hash maps)
- 5-6 LC easy/medium per day
- Focus: get comfortable with Java solutions, understand time/space complexity

### Week 2: Algorithms & Patterns
- Master all major algorithms (sorting, searching, BFS/DFS, DP, greedy, backtracking, divide & conquer)
- 4-5 LC medium per day + 1 hard every other day
- Focus: pattern recognition — identify which pattern fits which problem

### Week 3: System Design + Hard Problems
- System design: 2 full designs per day (one study, one from scratch)
- 3-4 LC medium/hard per day
- Focus: translate GSTN experience into system design answers

### Week 4: Mock Interviews + Revision
- 1-2 mock interviews per day (coding + system design + behavioral)
- Review ALL flagged/failed problems from weeks 1-3
- Focus: timing, communication, confidence

## Key Stats from Successful Candidates

| Candidate | Prep Duration | Hours/Day | Problems Solved | Result |
|-----------|--------------|-----------|----------------|--------|
| Steven Zhang | ~3 months | 6-8 hrs | 200+ | 18 FAANG+ offers |
| Coding Interview University (jwasham) | 8 months | 8-12 hrs | Hundreds | Google offer |
| Tech Interview Handbook author | 3 months | ~3 hrs/day (11 hrs/week) | ~100 curated | Multiple FAANG offers |
| Average successful candidate | 1-3 months | 2-3 hrs/day | 100-200 | Mid-tier to FAANG offer |

## Critical Thresholds (Research-Backed)

- **30 hours**: Bare minimum to be somewhat prepared
- **100 hours**: Well-prepared for most coding interviews
- **5 mock interviews**: Significant performance improvement milestone
- **150-200 LC problems**: Sweet spot for pattern coverage (if done with spaced repetition)
- **80 problems with spaced repetition** > 200 problems without revision

---

# PART 5: JAYANTI-SPECIFIC RECOMMENDATIONS

## Your Advantages
- 5.5 YOE at GSTN with real distributed systems experience
- Strong system design foundation (14M taxpayers, 3B invoices, Kafka, Redis, XA transactions)
- 155 LC problems already done (but 151 in C++, need Java switch)

## Your Priority Actions

### Immediate (This Week)
1. Install Anki and import system-design-primer deck (230+ cards)
2. Sign up for Pramp (free) — schedule first mock for this weekend
3. Start DSA Prep or Grind 75 Bot for spaced repetition tracking
4. Re-solve your 155 LC problems in Java (start with the 4 you already did in Java, then convert others)

### Short-Term (Weeks 1-4)
1. Follow Schedule A (working at GSTN) — target 25-30 hrs/week
2. Solve 2-3 new LC problems/day in Java + 3-4 reviews/day
3. Create Anki cards for every new problem (pattern, approach, complexity)
4. Complete 1 system design mock/week (self-practice first, then Pramp)
5. Practice 2 Amazon LP STAR stories per week (you have 22 in your bank)

### Medium-Term (Weeks 5-8)
1. Start company-specific OA prep based on where you're applying
2. Do PayPal/Goldman OAs first (easier) to build confidence
3. Practice Stripe-style multi-part problems
4. Upgrade to interviewing.io for 2-3 paid mock sessions
5. Target: 100+ LC problems in Java with spaced repetition

### Pre-Interview (Weeks 9-12)
1. Focus on target company's OA pattern from the table above
2. Do 2-3 full mock interviews per week (coding + SD + behavioral)
3. Review ALL Anki cards daily (should take 20-30 min by now)
4. Re-solve all "hard" flagged problems
5. Practice end-to-end: OA simulation -> phone screen simulation -> onsite simulation

---

## Sources

### OA Patterns
- [Stripe OA Prep Guide - Lodely](https://www.lodely.com/blog/stripe-online-assessment-2025)
- [Stripe HackerRank OA Questions](https://www.linkjob.ai/interview-questions/stripe-hackerrank-online-assessment/)
- [Stripe 2026 New Grad OA](https://programhelp.net/en/oa/stripe-2026-new-grad-oa-overview/)
- [Amazon OA Questions 2026 - AOneCode](https://aonecode.com/amazon-online-assessment-questions)
- [Amazon OA Prep Guide - Lodely](https://www.lodely.com/blog/amazon-online-assessment-2025)
- [Amazon OA Guide 2025 - Shadecoder](https://www.shadecoder.com/blogs/amazon-oa-oa1-oa2-complete-guide)
- [Amazon OA 2026 - Shadecoder](https://www.shadecoder.com/blogs/amazon-online-assessment-2026-complete-prep-guide-for-technical-non-technical-roles)
- [Google OA 2026 Guide - Shadecoder](https://www.shadecoder.com/blogs/google-online-assessment-2026-sample-questions-format-and-how-it-really-differs-from-leetcode)
- [Google OA Guide - IGotAnOffer](https://igotanoffer.com/blogs/tech/google-online-assessment)
- [Bloomberg Interview Guide - Prepfully](https://prepfully.com/interview-guides/bloomberg-software-engineer)
- [Bloomberg Interview Questions - Algo.Monster](https://algo.monster/interview-guides/bloomberg)
- [Bloomberg Interview Process - Interviewing.io](https://interviewing.io/bloomberg-interview-questions)
- [DoorDash HackerRank Questions](https://www.linkjob.ai/interview-questions/doordash-hackerrank-questions)
- [DoorDash Code Craft Interview - Lodely](https://www.lodely.com/blog/doordash-code-craft-interview-2025)
- [DoorDash Interview Guide - Algo.Monster](https://algo.monster/interview-guides/doordash)
- [DoorDash Coding Interviews 2026 - CodeJeet](https://codejeet.com/blog/how-to-crack-doordash-coding-interviews)
- [Flipkart Placement Papers 2025-2026](https://placementpapers.app/flipkart/)
- [Flipkart OA & Interview Problems - LeetCode](https://leetcode.com/discuss/interview-experience/7123054/)
- [Goldman Sachs HackerRank Test 2026](https://www.linkjob.ai/interview-questions/goldman-sachs-hackerrank-test/)
- [Goldman Sachs CoderPad Guide](https://programhelp.net/en/goldman-coderpad-interview/)
- [PayPal HackerRank Questions 2025](https://www.linkjob.ai/interview-questions/paypal-hackerrank-questions)
- [PayPal Interview Guide - Algo.Monster](https://algo.monster/interview-guides/paypal)
- [NVIDIA Interview Guide - IGotAnOffer](https://igotanoffer.com/en/advice/nvidia-software-engineer-interview)
- [NVIDIA HackerRank Test 2026](https://www.linkjob.ai/interview-questions/nvidia-hackerrank-test)
- [Anthropic AI-Resistant Evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)
- [Anthropic Original Take-Home - GitHub](https://github.com/anthropics/original_performance_takehome)
- [Anthropic CodeSignal Practice](https://www.linkjob.ai/interview-questions/codesignal-anthropic-practice/)
- [OpenAI Coding Questions - Hello Interview](https://www.hellointerview.com/blog/openai-coding-questions)
- [OpenAI Interview Guide - Exponent](https://www.tryexponent.com/guides/openai-software-engineer-interview-guide)
- [OpenAI Interview Process - Interviewing.io](https://interviewing.io/openai-interview-questions)

### Mock Interview Platforms
- [Interviewing.io](https://interviewing.io/)
- [Pramp](https://www.pramp.com/)
- [Best Mock Interview Platforms - Tech Interview Handbook](https://www.techinterviewhandbook.org/mock-interviews/)
- [Best System Design Mock Platforms - IGotAnOffer](https://igotanoffer.com/en/advice/best-system-design-mock-interview-platforms)
- [7 Best AI Mock Interview Platforms 2026 - PracHub](https://prachub.com/resources/7-best-ai-mock-interview-platforms-in-2026-ranked-by-real-engineers)
- [Hello Interview](https://www.hellointerview.com/)
- [Codemia - System Design Practice](https://codemia.io/)

### Spaced Repetition & Revision
- [DSA Prep - Spaced Repetition](https://www.dsaprep.dev/)
- [Grind 75 Bot](https://grind75bot.com/)
- [LeetCode Spaced Repetition Schedule](https://www.redgreencode.com/leetcode-tip-10-planning-a-spaced-repetition-schedule/)
- [Mastering LC with Anki](https://www.devgould.com/how-i-master-leetcode-problems-using-anki-a-personal-journey/)
- [LeetRepeat](https://leetrepeat.com)
- [System Design Primer + Anki Deck - GitHub](https://github.com/donnemartin/system-design-primer)
- [DesignDeck 230+ Flash Cards - GitHub](https://github.com/teivah/designdeck)

### Study Schedules & Success Stories
- [Coding Interview Study Plan - Tech Interview Handbook](https://www.techinterviewhandbook.org/coding-interview-study-plan/)
- [Average to Googler in Four Weeks - Milad Naseri](https://www.linkedin.com/pulse/average-googler-four-weeks-study-plan-milad-naseri)
- [18 FAANG+ Offers - Steven Zhang](https://medium.com/@stevenzhang/how-i-landed-18-faang-software-engineer-offers-after-not-interviewing-for-5-years-fc0dfc957a5d)
- [Coding Interview University - GitHub](https://github.com/jwasham/coding-interview-university)
- [How I Prepared for Google - Lyndon Duong](https://www.lyndonduong.com/coding-interview/)
- [FAANG Interview Prep - FreeCodeCamp](https://www.freecodecamp.org/news/coding-interview-prep-for-big-tech/)
- [Senior Engineer's Guide to FAANG - Interviewing.io](https://interviewing.io/guides/hiring-process)
