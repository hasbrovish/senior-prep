# OA Patterns, Mock Interviews & Revision Guide

## Online Assessment (OA) Common Patterns

### Pattern Distribution (2025-2026 data)
1. **Arrays/Strings** — 35% of OA questions. Two pointers, sliding window, prefix sum.
2. **Graph/Tree** — 20%. BFS/DFS, topological sort, LCA.
3. **DP** — 20%. Usually medium difficulty. Knapsack variants, subsequence problems.
4. **Binary Search** — 10%. Search on answer is the key insight.
5. **Greedy** — 10%. Interval scheduling, activity selection.
6. **Other** — 5%. Bit manipulation, math, simulation.

### OA Time Management
- Read ALL problems first (2 min)
- Start with easiest (get guaranteed score)
- For 3-problem OA: 20 min + 25 min + 35 min split
- Always submit partial solutions — partial credit is common
- Edge cases: empty input, single element, maximum constraints

### Company-Specific OA Patterns
- **Amazon:** 2 medium problems, 70 min. Array/string heavy. LP questions mixed in.
- **Google:** 2 problems, 45 min each. One medium, one hard. No multiple choice.
- **Microsoft:** 3 problems, 90 min. Easy + medium + hard progression.
- **Flipkart:** 3 problems, 90 min. Graph and DP heavy.
- **Razorpay/Juspay:** 2-3 problems, custom platform. Graph problems common for Juspay.

## Mock Interview Structure

### Technical Round (45 min)
- 5 min: Intro + problem statement
- 5 min: Clarify requirements, discuss approach
- 25 min: Code solution
- 5 min: Test with examples, edge cases
- 5 min: Complexity analysis + follow-ups

### System Design Round (45 min)
- 5 min: Requirements gathering
- 3 min: Back-of-envelope estimation
- 12 min: High-level design
- 20 min: Deep dive on 2-3 components
- 5 min: Wrap-up (bottlenecks, monitoring, evolution)

### Behavioral Round (30 min)
- 2 min per STAR story (practice with timer!)
- Prepare 8-10 stories covering: conflict, failure, leadership, ambiguity, technical decision, mentoring
- Every story should have quantified impact

## Revision Schedule (Spaced Repetition)

### Weekly Focus Areas
- **Mon:** Java Core (Q1-Q25) + 2 LeetCode
- **Tue:** Spring Boot (Q26-Q60) + 2 LeetCode
- **Wed:** Microservices/Kafka/Redis (Q91-Q135) + 2 LeetCode
- **Thu:** System Design (1 full design) + 1 LeetCode
- **Fri:** DSA patterns (focus on weak pattern) + 2 LeetCode
- **Sat:** LLD (1 full problem) + Behavioral (practice 2 stories out loud)
- **Sun:** Review week's mistakes. Weekly retro. Plan next week.

### Before Interview Day
- Night before: Read GSTN_Architecture_Reference.md. Review your 3 strongest STAR stories.
- Morning of: Quick scan of the company's Company_Questions file. Review recent LeetCode mistakes.
- Don't cram. Review, don't learn. Confidence > knowledge on interview day.

## Common Mistakes (From Your Post-Interview Analysis)

### Articulation
- **Problem:** Filler words ("um", "like", "basically") under pressure.
- **Fix:** Practice the PAUSE. 2 seconds of silence is better than "um". Record yourself.

### Flat Negatives
- **Problem:** Saying "I don't know" and stopping.
- **Fix:** Bridge technique: "I haven't worked with X directly, but I've solved a similar problem with Y..."

### Over-Explaining
- **Problem:** 5-minute answers to simple questions.
- **Fix:** PREP framework: Point → Reason → Example → Point. Answer the question, then stop. Let them ask follow-ups.

### Not Quantifying
- **Problem:** "I improved performance" (vague).
- **Fix:** "I reduced p99 latency from 2.3s to 120ms by fixing the N+1 query with a join fetch."
