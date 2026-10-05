# DAY 1 — APRIL 30, 2026 — START RIGHT NOW

## Before 12 PM Today — Do These 5 Things

### 1. Create GitHub Repos (30 min)
Go to github.com/jayantivishnoi and create 3 repos:
```
dsa-java          — "LeetCode solutions in Java, organized by pattern | 90-day prep"
system-designs    — "System design sketches with capacity estimates | SDE-2/3 prep"
lld-java          — "Machine coding implementations in Java | LLD interview prep"
```
Add a profile README (copy template from 90_DAY_COMPLETE_WARPLAN_APR30_JUL28.md → GitHub section)

### 2. Update LinkedIn (20 min)
Change headline to:
```
Backend Engineer | Java · Spring Boot · Kafka · Redis · Distributed Systems | 5.5 YOE | Open to SDE-2/SDE-3
```
Turn on "Open to Work" → visible to recruiters only
Add: Open to SDE-2/SDE-3 at product companies, Bengaluru preferred, open to remote

### 3. Start AWS CCP Study (1 hr)
Go to: https://explore.skillbuilder.aws (free)
Search: "AWS Cloud Practitioner Essentials"
Complete Module 1 today (Introduction to Amazon Web Services)

### 4. Solve Today's 2 LeetCode Problems (90 min)
Both in JAVA. Commit to dsa-java GitHub repo.
```
Problem 1: #1 Two Sum — arrays/TwoSum.java
Problem 2: #217 Contains Duplicate — arrays/ContainsDuplicate.java
```
Template for every solution:
```java
// Problem: Two Sum (LC #1)
// Pattern: Arrays + Hashing
// Time: O(n) | Space: O(n)
// Approach: HashMap to store complement
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}
```

### 5. Read java_qa OOP questions (30 min)
```bash
cd /Users/jayanti/Documents/dev/senior-prep
python3 prep.py jqa oop
```
You already studied OOP on Apr 9 — just quickly review the P0 questions to refresh.

---

## Today's Full Schedule

```
Now – 12:00  → Tasks 1-4 above (GitHub + LinkedIn + AWS + 2 LeetCode)
12:00–13:00  → Lunch
13:00–14:30  → Programming Pathshala: Module 3 (Binary Search) — watch 3 videos
14:30–15:30  → Java Theory: prep jqa strings (read all P0 questions)
15:30–16:30  → AWS CCP study (Module 2: Cloud Benefits)
16:30–17:00  → Walk/break
17:00–17:30  → Write your 2 LP stories aloud:
               Story 1: Ownership (the XA transaction decision at GSTN)
               Story 2: Customer Obsession (zero fund misappropriation)
17:30–19:00  → Read: 90_DAY_COMPLETE_WARPLAN_APR30_JUL28.md fully (your new bible)
19:00–20:00  → HLD Sketch: URL Shortener (requirements → estimation → API → DB → architecture)
               Use paper or Excalidraw (excalidraw.com)
20:00–21:00  → Connect with 10 engineers at target companies on LinkedIn:
               Search "Software Engineer Razorpay" / "Backend Engineer CRED" / "SDE PhonePe"
               Send connection request with the template message
21:00–21:30  → Plan tomorrow: write down exactly which 2 LeetCode problems (#238 + #242)
21:30–22:00  → Review. Sleep by 22:30.
```

---

## Week 1 Problem List (Memorize This)

| Day | Morning Problem | Evening Problem | Pattern |
|-----|----------------|-----------------|---------|
| Day 1 (Apr 30) | #1 Two Sum | #217 Contains Duplicate | Arrays + Hashing |
| Day 2 (May 1) | #238 Product of Array Except Self | #242 Valid Anagram | Arrays |
| Day 3 (May 2) | #49 Group Anagrams | #347 Top K Frequent | HashMap + Heap |
| Day 4 (May 3) | #11 Container With Most Water | #15 3Sum | Two Pointers |
| Day 5 (May 4) | #167 Two Sum II | #3 Longest Substring | Two Pointers + Sliding Window |
| Day 6 (May 5) | #424 Longest Repeating Char | #567 Permutation in String | Sliding Window |
| Day 7 (May 6) | #121 Best Time Buy/Sell Stock | #209 Min Size Subarray Sum | Sliding Window |

---

## The One Thing to Remember

Your GSTN experience — XA transactions, Kafka DLQ, 15.2M taxpayers — is worth 3x any tutorial
project on any other candidate's resume. The goal is NOT to learn new things from scratch.
The goal is to TRANSLATE what you already built at GSTN into interview language.

**Start. Now. Not tomorrow.**

---
*Day 1 of 90 | April 30, 2026*
