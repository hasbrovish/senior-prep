# DSA INTERVIEW - ANSWER TEMPLATE & EVALUATION GUIDE

## 🎯 STRONG HIRE SIGNALS (What Interviewers Score)

| Signal | Strong Hire | Hire | No Hire |
|--------|-------------|------|---------|
| **Pattern Recognition** | Identifies in 2-3 min | Needs hints | Cannot identify |
| **Code Quality** | Bug-free first attempt | 1-2 small bugs | Major bugs |
| **Complexity** | States proactively | Knows when asked | Wrong analysis |
| **Edge Cases** | Handles without prompting | Handles most | Misses all |
| **Optimization** | Offers improvements | Can optimize if asked | Cannot optimize |
| **Communication** | Thinks aloud clearly | Good enough | Goes silent |

---

## 📝 ANSWER TEMPLATE (Follow This Every Time)

### STEP 1: CLARIFY (1-2 minutes)
```
"Before I dive in, let me clarify a few things..."

ASK THESE:
□ What's the input size/constraints? (Helps choose O(n²) vs O(n log n))
□ Is the input sorted? Are duplicates allowed?
□ What should I return if no solution exists?
□ Can I modify the input array in-place?
□ Any memory constraints I should know about?
```

### STEP 2: PATTERN RECOGNITION (1-2 minutes)
```
"This problem reminds me of [PATTERN] because..."

PATTERN TRIGGERS:
├── Sorted array + target → Two Pointers / Binary Search
├── Subarray with constraint → Sliding Window  
├── Build all combinations → Backtracking
├── "Minimum/Maximum of X" → DP or Binary Search
├── Optimal substructure + overlapping → DP
├── Graph connectivity → BFS/DFS/Union-Find
├── Stream of data + median → Two Heaps
├── Next greater/smaller → Monotonic Stack
├── Prefix operations → Trie
└── Dependencies/ordering → Topological Sort
```

### STEP 3: APPROACH (2-3 minutes)
```
"Here's my approach..."

DO:
✓ Explain algorithm in plain English first
✓ Walk through with a small example (draw if whiteboard)
✓ State time & space complexity BEFORE coding
✓ Mention any trade-offs

SAY:
"I'll use [PATTERN] which gives us O(X) time and O(Y) space.
Let me walk through with this example... [trace through]
Does this approach sound good before I start coding?"
```

### STEP 4: CODE (15-20 minutes)
```
"Let me code this up..."

DO:
✓ Write clean, readable code
✓ Use meaningful variable names (not i, j, k everywhere)
✓ Talk through your logic as you write
✓ Leave space for edge case handling

IF STUCK:
"Let me think about this for a moment..."
"I'm considering whether to use X or Y here because..."
"Actually, I need to handle the case where..."

AVOID:
✗ Going silent for > 30 seconds
✗ Writing without explaining
✗ Rushing through
```

### STEP 5: TEST (3-5 minutes)
```
"Let me trace through with an example..."

TEST ORDER:
1. Given example (verify basic logic)
2. Edge case: empty input []
3. Edge case: single element [5]
4. Edge case: all same elements [3,3,3]
5. Edge case: negative numbers (if applicable)

SAY:
"Walking through with [example]...
At this step, variable X equals Y...
Result is Z, which matches expected output."
```

### STEP 6: OPTIMIZE (if time remains)
```
"The current solution is O(X). If we needed to optimize..."

OPTIONS:
- "We could use a HashMap to reduce time from O(n²) to O(n)"
- "Sorting first gives us O(n log n) but enables two-pointer"
- "We could trade space for time by caching..."
```

---

## 🔥 POWER PHRASES (Use These!)

### Starting:
- "Before I jump in, let me make sure I understand the problem..."
- "This looks like a [pattern] problem because..."

### While Coding:
- "I'm using this data structure because..."
- "The key insight here is..."
- "Let me think about what happens when..."

### When Stuck:
- "Let me step back and think about this differently..."
- "I'm considering two approaches: X vs Y..."
- "I think I'm overcomplicating this. The simpler approach would be..."

### After Coding:
- "Before I trace through, let me verify the edge cases..."
- "The time complexity is O(X) because... and space is O(Y) because..."
- "If we needed to optimize further, we could..."

---

## ⚠️ RED FLAGS TO AVOID

| Red Flag | What to Do Instead |
|----------|---------------------|
| Going silent when stuck | "Let me think about this..." then verbalize |
| Diving into code without plan | Always explain approach first |
| Not testing code | Always trace through examples |
| Saying "I don't know" and stopping | "I'd approach finding out by..." |
| Arguing with interviewer | "That's a good point. Let me reconsider..." |
| Overconfidence: "This is easy" | Stay humble, respect the problem |

---

## 📊 PATTERN QUICK REFERENCE

| Pattern | Time Signal | Space | Key Data Structure |
|---------|-------------|-------|-------------------|
| Two Pointers | O(n) | O(1) | Array, sorted |
| Sliding Window | O(n) | O(k) | Array, HashMap |
| Binary Search | O(log n) | O(1) | Sorted array |
| BFS | O(V+E) | O(V) | Queue |
| DFS | O(V+E) | O(V) | Stack/Recursion |
| Two Heaps | O(log n) | O(n) | Min-heap, Max-heap |
| Monotonic Stack | O(n) | O(n) | Stack |
| Trie | O(m) | O(n*m) | Trie node |
| Union Find | O(α(n))≈O(1) | O(n) | Parent array |
| DP | O(n*m) | O(n) or O(n*m) | Array/Table |

---

## 📝 SELF-ASSESSMENT CHECKLIST (After Each Practice)

After every problem, score yourself:

```
□ Did I identify the pattern within 3 minutes?
□ Did I explain my approach before coding?
□ Did I state complexity before coding?
□ Was my code bug-free on first attempt?
□ Did I test with multiple examples?
□ Did I handle all edge cases?
□ Did I think aloud throughout?
□ Could I optimize if asked?
```

**Score: ___/8**

- 7-8: Strong Hire level
- 5-6: Hire level (keep practicing)
- 3-4: Lean Hire (focus on weak areas)
- 0-2: More practice needed
