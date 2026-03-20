#!/usr/bin/env python3
"""
Jayanti's SDE-2/SDE-3 Daily Prep Tracker

  python3 prep.py                    → today's plan (default)
  python3 prep.py log                → log what you did today
  python3 prep.py status             → full progress dashboard
  python3 prep.py review             → weekly feedback + suggestions
  python3 prep.py lc "Two Sum"       → mark LeetCode problem done
  python3 prep.py apply "Razorpay"   → log job application
  python3 prep.py offer "Razorpay"   → log an offer received
  python3 prep.py help               → all commands

SETUP (run once):
  echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
  source ~/.zshrc
  # Now just type: prep
"""

import json, sys, urllib.request, urllib.error
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────
BASE             = Path(__file__).parent
LOGS_DIR         = BASE / "logs"
PROG_FILE        = LOGS_DIR / "progress.json"
START            = date(2026, 3, 19)
LEETCODE_USER    = "hasbrovish95"
LC_API           = "https://leetcode.com/graphql"

# ─── 26-Week Plan Data ────────────────────────────────────────────────────────
WEEKS = {
  1:  {"theme":"Resume + Profile Setup",
       "phase":1, "month":1,
       "dsa":"Arrays, Strings", "diff":"Easy", "lc_target":7,
       "lc_problems":["Two Sum","Valid Anagram","Contains Duplicate",
                      "Best Time to Buy and Sell Stock","Valid Palindrome",
                      "Reverse String","Majority Element"],
       "tasks":[
         "Finalize resume: 6 STAR bullets from GSTN (GSTN_Complete Part 2)",
         "LinkedIn: headline, About section, 3 project descriptions, Open to Work ON",
         "GitHub: Kafka Pipeline skeleton + README (GSTN_Complete Part 10, Project 3)",
         "Read GSTN_Complete Part 1 — pick your top 3 code walkthroughs to narrate"],
       "tip":"This week is positioning, not studying. A weak resume kills every chance before it starts."},

  2:  {"theme":"Java Core Internals",
       "phase":1, "month":1,
       "dsa":"Two Pointers, Sliding Window", "diff":"Easy", "lc_target":7,
       "lc_problems":["Two Sum II","3Sum","Move Zeroes","Longest Substring Without Repeating",
                      "Max Consecutive Ones","Minimum Size Subarray Sum","Valid Palindrome II"],
       "tasks":[
         "Read Section_01_Java_Core.md fully — mark every question you can't answer (Q1-Q25)",
         "Deep dive: HashMap internals (treeify at 8, load factor 0.75, Java 8 tree bins)",
         "Write code: CompletableFuture parallel API calls (allOf + exceptionally)",
         "Flashcards: GC types (G1GC vs ZGC vs Serial), JVM memory zones"],
       "tip":"ConcurrentHashMap vs Collections.synchronizedMap() is asked in nearly every Java SDE-2 round."},

  3:  {"theme":"Spring Boot + Hibernate Deep Dive",
       "phase":1, "month":1,
       "dsa":"HashMap problems, Linked Lists", "diff":"Easy", "lc_target":7,
       "lc_problems":["Reverse Linked List","Merge Two Sorted Lists","Linked List Cycle",
                      "Group Anagrams","Intersection of Two Linked Lists",
                      "Remove Duplicates from Sorted List","Middle of the Linked List"],
       "tasks":[
         "Read Section_02_Spring_Boot.md — focus on @Transactional proxy + propagation",
         "Read Section_03_Hibernate_JPA.md — N+1 problem, 1st vs 2nd level cache",
         "Write 2-min script: explain GSTN ledger @Transactional(REQUIRES_NEW) out loud",
         "Q26–Q90 in question bank — mark shaky ones, add to revision list"],
       "tip":"Your XA transaction + ledger experience is a differentiator. Every Spring question can be answered with a GSTN example."},

  4:  {"theme":"Microservices + Kafka + Redis + First Applications",
       "phase":1, "month":1,
       "dsa":"Stack, Queue, Binary Search", "diff":"Easy", "lc_target":7,
       "lc_problems":["Valid Parentheses","Min Stack","Binary Search","First Bad Version",
                      "Implement Queue using Stacks","Daily Temperatures","Search Insert Position"],
       "tasks":[
         "Read Section_04_05_06_Microservices_Kafka_Redis.md",
         "Deep dive: your DistCacheUtil — explain its design in 3 minutes",
         "Deep dive: your Consumer.java DLQ pattern — this is production gold",
         "APPLY NOW: Razorpay, Juspay, CRED, MakeMyTrip, Meesho — 5 applications TODAY"],
       "tip":"Applications are the most procrastinated task. Set a 2-hour timer and apply to 5. No further prep needed to click Apply."},

  5:  {"theme":"Review + Mock Interview 1",
       "phase":1, "month":1,
       "dsa":"Review + backlog", "diff":"Easy", "lc_target":7,
       "lc_problems":["Climbing Stairs","Fibonacci Number","Pascal Triangle","Symmetric Tree",
                      "Maximum Depth of Binary Tree","Invert Binary Tree","Merge Sorted Array"],
       "tasks":[
         "Mock Interview: Round 4 (Past Work Deep Dive) from GSTN_Complete Part 3 — record yourself",
         "Watch recording. Find your 3 weakest moments. Fix them this week.",
         "Complete any incomplete tasks from Weeks 1-4",
         "Follow up on Week 4 applications — email or LinkedIn message"],
       "tip":"You learn more from 1 badly-done mock than 2 weeks of reading. Do it even if you feel unprepared."},

  6:  {"theme":"Low-Level Design (LLD)",
       "phase":1, "month":2,
       "dsa":"Trees — BFS, DFS, traversals", "diff":"Easy/Medium", "lc_target":7,
       "lc_problems":["Binary Tree Inorder Traversal","Binary Tree Level Order Traversal",
                      "Path Sum","Binary Tree Right Side View",
                      "Count Good Nodes in Binary Tree","Validate BST","Kth Smallest in BST"],
       "tasks":[
         "SOLID principles: write 1 Java code example for each (S, O, L, I, D)",
         "LLD Practice: Design a Parking Lot — UML → Java classes",
         "LLD Practice: Design a Vending Machine",
         "Review trackers-docs/LLD_Master_Interview_Sheet_v2.xlsx"],
       "tip":"Strategy pattern (your CaseCustomizerFactory at GSTN) is your strongest LLD example — reference it in every round."},

  7:  {"theme":"System Design — Mid-Tier Level",
       "phase":1, "month":2,
       "dsa":"Dynamic Programming Easy", "diff":"Medium", "lc_target":7,
       "lc_problems":["Climbing Stairs","Coin Change","House Robber","Min Cost Climbing Stairs",
                      "Unique Paths","Jump Game","Decode Ways"],
       "tasks":[
         "Read Section_21_SystemDesign_DeepDive_With_Answers.md",
         "Practice: Rate Limiter — token bucket vs sliding window (draw + explain)",
         "Practice: Notification System (YOUR CommunicationService from GSTN — strongest design)",
         "Memorise: 5-step framework: requirements → scale → high-level → deep dive → failure"],
       "tip":"Mid-tier companies want CLEAR THINKING, not Google-scale. Spend 5 min on requirements before drawing anything."},

  8:  {"theme":"Databases + Distributed Systems",
       "phase":1, "month":2,
       "dsa":"Graphs — BFS, DFS", "diff":"Medium", "lc_target":7,
       "lc_problems":["Number of Islands","Clone Graph","Course Schedule","Pacific Atlantic Water Flow",
                      "Max Area of Island","Rotting Oranges","Surrounded Regions"],
       "tasks":[
         "Read Section_07_08_Database_DistributedSystems.md — Q136–Q165",
         "Deep dive: HBase row key design GSTIN|Period|ReturnType — your best DB example",
         "Practice: CAP theorem — give 3 real-world trade-off examples",
         "Deep dive: MySQL ACID + isolation levels — map to GSTN ledger operations"],
       "tip":"'When would you use NoSQL vs SQL?' — Your GSTN HBase + MySQL combo IS the perfect answer."},

  9:  {"theme":"Cloud + Docker + K8s + Testing",
       "phase":1, "month":2,
       "dsa":"Heap / Priority Queue", "diff":"Medium", "lc_target":7,
       "lc_problems":["Kth Largest Element in Array","Top K Frequent Elements",
                      "Find Median from Data Stream","Task Scheduler","K Closest Points to Origin",
                      "Reorganize String","Last Stone Weight"],
       "tasks":[
         "Read Section_09_10_11_Patterns_Docker_CICD.md + Section_12_13_14_15 Cloud section",
         "Read Section_16_17_18_19 — Testing section (JUnit + Mockito + integration tests)",
         "AWS: EC2, S3, RDS, ElastiCache, SQS/SNS, Lambda — 1 use case for each, out loud",
         "Docker: multi-stage builds, image layers, compose — can you explain without googling?"],
       "tip":"Map GSTN deployment to Docker/K8s even if you used bare-metal. 'We containerised microservices' is a safe framing."},

  10: {"theme":"Behavioral + Interview Acceleration",
       "phase":1, "month":2,
       "dsa":"Mixed — solidify weak areas", "diff":"Medium", "lc_target":7,
       "lc_problems":["LRU Cache","Design HashMap","Min Stack","Implement Trie","Word Search",
                      "Generate Parentheses","Letter Combinations of Phone Number"],
       "tasks":[
         "Write all 6 STAR stories in full (see MASTER_6MONTH_PROGRAMME.md — Behavioral section)",
         "Read GSTN_Complete Part 5.1 — Amazon Leadership Principles mapping",
         "Applications push: 25+ total by end of this week — use referrals wherever possible",
         "LinkedIn: Message 5 ex-GSTN colleagues at target companies asking for referrals"],
       "tip":"Behavioral rounds eliminate more SDE-2 candidates than DSA. Your GSTN peak-filing + ledger incident stories are powerful — use them."},

  11: {"theme":"Full Mock Interview Week",
       "phase":1, "month":3,
       "dsa":"Backtracking, Recursion", "diff":"Medium", "lc_target":7,
       "lc_problems":["Combination Sum","Word Search","Subsets","Permutations",
                      "Combination Sum II","Subsets II","Palindrome Partitioning"],
       "tasks":[
         "Mock Round 1: Java Deep Dive — 45 min timed (GSTN_Complete Part 3.1)",
         "Mock Round 3: System Design — do 1 from your must-know list end-to-end",
         "Mock Round 4: Past Work Deep Dive — record and watch",
         "After each mock: write down every weak point within 1 hour. Fix the top 3."],
       "tip":"Every stumble in a mock is a gift — it's a question you will not stumble on in the real interview."},

  12: {"theme":"Interview Blitz — Active Rounds",
       "phase":1, "month":3,
       "dsa":"Mixed Medium", "diff":"Medium", "lc_target":7,
       "lc_problems":["Search in Rotated Sorted Array","Find Minimum in Rotated Sorted Array",
                      "Koko Eating Bananas","Time Based Key-Value Store",
                      "Capacity to Ship Packages","Min Eating Speed","Find Peak Element"],
       "tasks":[
         "Active interviews this week — treat each as learning, not judgment",
         "After every interview: log all questions asked within 1 hour",
         "Identify repeating questions — drill them immediately",
         "Research CTC ranges: Glassdoor + Levels.fyi for your target companies"],
       "tip":"If not getting callbacks: resume issue. If failing rounds: identify which round and drill it specifically."},

  13: {"theme":"Interview Blitz — Refine + Close",
       "phase":1, "month":3,
       "dsa":"Medium/Hard", "diff":"Medium/Hard", "lc_target":7,
       "lc_problems":["Trapping Rain Water","Container With Most Water",
                      "Largest Rectangle in Histogram","Minimum Window Substring",
                      "Sliding Window Maximum","Longest Consecutive Sequence","Word Break"],
       "tasks":[
         "Aim for 3 final rounds this week — push all pending applications",
         "Shore up any gaps from interview feedback in weeks 11-12",
         "Prepare 5 smart questions to ask every interviewer (signal seniority)",
         "Expand list if needed: Walmart Global Tech, Publicis Sapient, Nagarro"],
       "tip":"Smart questions signal seniority: 'How does your team handle backward compatibility in API changes?' or 'What's your biggest scaling challenge right now?'"},

  14: {"theme":"Close First Offer",
       "phase":1, "month":3,
       "dsa":"Catchup + maintain habit", "diff":"Medium", "lc_target":7,
       "lc_problems":["Jump Game II","Gas Station","Merge Intervals","Non-Overlapping Intervals",
                      "Meeting Rooms II","Minimum Number of Arrows to Burst Balloons","Hand of Straights"],
       "tasks":[
         "Negotiate any pending offers — counter is ALWAYS appropriate at SDE-2 level",
         "Offer negotiation script: 'I'm very excited — can I have 48 hours to consider?'",
         "Never reveal current CTC. Say: 'I'm targeting market rate for this level.'",
         "Accept only if it meets your minimum bar. Do NOT stop Phase 2 prep."],
       "tip":"Never accept on the spot. Every SDE-2 offer has at least 10-15% negotiation room. Ask even if it feels awkward."},

  15: {"theme":"Phase 2 Start — DSA Serious Mode",
       "phase":2, "month":4,
       "dsa":"Arrays, Strings — NeetCode 150 revisit", "diff":"Medium/Hard", "lc_target":10,
       "lc_problems":["Product of Array Except Self","Maximum Subarray","Spiral Matrix",
                      "Set Matrix Zeroes","Rotate Image","Valid Sudoku",
                      "Longest Palindromic Substring","Palindromic Substrings",
                      "Encode and Decode Strings","Find All Duplicates in Array"],
       "tasks":[
         "Phase 1 offer in hand. Mental reset: Phase 2 starts NOW. Different gear.",
         "2 hours DSA daily from this week — non-negotiable. Morning 1 + Evening 1.",
         "Redo all failed NeetCode problems from Weeks 1-9 — one full session this weekend",
         "FAANG system design: Design Twitter Feed (fan-out on write vs read)"],
       "tip":"Phase 2 is about excellence, not safety. DSA is the biggest differentiator at FAANG — raise your floor."},

  16: {"theme":"Binary Search + Linked List Mastery",
       "phase":2, "month":4,
       "dsa":"Binary Search, Linked Lists", "diff":"Medium/Hard", "lc_target":10,
       "lc_problems":["Reorder List","Remove Nth Node From End","Linked List Cycle II",
                      "Copy List with Random Pointer","Add Two Numbers","Reverse Nodes in K-Group",
                      "Merge K Sorted Lists","Find the Duplicate Number",
                      "Median of Two Sorted Arrays","Maximum Profit in Job Scheduling"],
       "tasks":[
         "Read Section_20_FAANG_SDE2_SDE3_Advanced.md — full read",
         "Implement LRU Cache from scratch in Java (HashMap + DoublyLinkedList — memorise this)",
         "LLD Practice: Design Elevator System, Design Hotel Booking",
         "System Design: Design Google Drive (chunked upload, sync, conflict resolution)"],
       "tip":"LRU Cache implementation is asked at Amazon, Flipkart, Goldman Sachs. Have it memorized cold."},

  17: {"theme":"Graphs Mastery + Golang Brush-up",
       "phase":2, "month":4,
       "dsa":"Graphs — advanced", "diff":"Medium/Hard", "lc_target":10,
       "lc_problems":["Course Schedule II","Number of Connected Components","Redundant Connection",
                      "Word Ladder","Alien Dictionary","Network Delay Time","Swim in Rising Water",
                      "Cheapest Flights Within K Stops","Min Cost to Connect All Points",
                      "Reconstruct Itinerary"],
       "tasks":[
         "Graphs: Dijkstra, Topological Sort, Union-Find — implement + understand all three",
         "LLD Practice: Design Chess Game, Design Food Delivery App (Swiggy LLD)",
         "Golang: goroutines, channels, select, context package — 2 hrs focused session",
         "System Design: Design Uber (geospatial indexing, driver matching, surge pricing)"],
       "tip":"Graphs are asked at Google, Flipkart, Swiggy (delivery routing). Code BFS + DFS from scratch without references."},

  18: {"theme":"Dynamic Programming Patterns",
       "phase":2, "month":4,
       "dsa":"DP — 0/1 Knapsack, LCS, Edit Distance", "diff":"Medium/Hard", "lc_target":10,
       "lc_problems":["Longest Common Subsequence","Edit Distance","Distinct Subsequences",
                      "Longest Increasing Subsequence","Partition Equal Subset Sum","Target Sum",
                      "Interleaving String","Coin Change II",
                      "Buy and Sell Stock with Cooldown","Burst Balloons"],
       "tasks":[
         "DP: 1D patterns (house robber), 2D patterns (LCS, edit distance) — 2 per day",
         "LLD Practice: Design Pub-Sub system (map it to your Kafka consumer framework)",
         "Golang: error handling (errors.Is, errors.As, custom errors), basic HTTP server",
         "System Design: Design WhatsApp (WebSocket, message queue, read receipts, scale)"],
       "tip":"DP is where most candidates give up. The pattern recognition COMES with practice — trust the process and do 2 daily."},

  19: {"theme":"Hard Problems Mode",
       "phase":2, "month":5,
       "dsa":"Hard problems — timed sessions", "diff":"Hard", "lc_target":10,
       "lc_problems":["Trapping Rain Water","N-Queens","Word Search II","Serialize Deserialize BT",
                      "Binary Tree Max Path Sum","Regular Expression Matching","Wildcard Matching",
                      "Maximum Profit in Job Scheduling","Alien Dictionary","Burst Balloons"],
       "tasks":[
         "2 hard LeetCode daily — 40 min each then review optimal. Timed, no hints.",
         "LeetCode weekly contest: Saturday — participate, track your rank over time",
         "Amazon: check Glassdoor + Blind for recent interview questions at your target team",
         "System Design: Distributed Rate Limiter (Goldman Sachs asks this heavily)"],
       "tip":"Hard problems test decomposition. If stuck at 15 min: write what you DO know. The insight comes from committing to partial solutions."},

  20: {"theme":"Hard Problems + Amazon Prep",
       "phase":2, "month":5,
       "dsa":"Hard — Amazon style", "diff":"Hard", "lc_target":10,
       "lc_problems":["K Closest Points to Origin","Random Pick with Weight","Design Twitter",
                      "Design Search Autocomplete","Find Median from Data Stream",
                      "LFU Cache","Sliding Window Median","Count of Range Sum",
                      "Maximum Gap","Design In-Memory File System"],
       "tasks":[
         "Amazon: map your 6 STAR stories to the 14 Leadership Principles — write it out",
         "Amazon system design: Package delivery tracking + real-time notification system",
         "Flipkart: Flash sale system design (inventory + rate limiting + order queue)",
         "Practice narrating any design as a story: 'The problem was X, I chose Y because Z'"],
       "tip":"Amazon's top LPs in SDE-2 rounds: Ownership, Dive Deep, Deliver Results. Have 2 strong STAR stories for each."},

  21: {"theme":"Goldman Sachs + Fintech Deep Prep",
       "phase":2, "month":5,
       "dsa":"Company-specific patterns", "diff":"Hard", "lc_target":10,
       "lc_problems":["Largest Rectangle in Histogram","Minimum Window Substring",
                      "Substring with Concatenation of All Words","Longest Substring K Distinct",
                      "Minimum Number of Refueling Stops","Jump Game III","Dungeon Game",
                      "Cherry Pickup","Regular Expression Matching","Maximum Rectangle"],
       "tasks":[
         "Goldman: JVM deep — lock internals (biased → thin → fat), GC tuning, off-heap",
         "Goldman: Concurrency — ReentrantLock vs synchronized, Phaser, StampedLock",
         "PhonePe/Razorpay: Idempotency, distributed transactions, audit trail design",
         "Your GSTN tax ledger = payments domain. Frame it: 'I built financial settlement logic at scale.'"],
       "tip":"Goldman goes very deep on Java. Expect: 'Explain lock-free programming' and 'How does G1GC concurrent marking work?'"},

  22: {"theme":"Google + Swiggy + Final Product Prep",
       "phase":2, "month":5,
       "dsa":"Google-style — elegance + optimal", "diff":"Hard", "lc_target":10,
       "lc_problems":["Design Add and Search Words DS","Word Search II","Implement Trie",
                      "Closest BST Value II","Count of Range Sum","Strange Printer",
                      "Zuma Game","Maximum Gap","Burst Balloons","Hard Interval Problems"],
       "tasks":[
         "Google: clean code + optimal time/space. Always mention complexity unprompted.",
         "Swiggy/Zomato: 'How would you improve Swiggy's search?' — product thinking round",
         "Read 1 engineering blog post from PhonePe and 1 from Swiggy engineering",
         "System Design: Real-time order tracking + surge pricing (Uber/Swiggy style)"],
       "tip":"Google: if you give brute force, they WILL ask for optimal. Lead with approach, not code."},

  23: {"theme":"Final Polish + Dream Applications Push",
       "phase":2, "month":6,
       "dsa":"NeetCode 150 — gap completion", "diff":"Mixed", "lc_target":14,
       "lc_problems":["Review all failed hard problems","Redo top failed mediums",
                      "3 timed mock contests this week","Fill any NeetCode 150 gaps"],
       "tasks":[
         "Apply: Amazon, Flipkart, Goldman Sachs, PhonePe, Swiggy, Google, Microsoft NOW",
         "Spend 1 week getting referrals — LinkedIn → find GSTN alumni at target companies",
         "Polish GitHub Kafka Pipeline project — make it production-grade and demo-ready",
         "3 full system designs end-to-end on paper (no notes, timed 45 min each)"],
       "tip":"Referral message template: 'Hi [name], I'm Jayanti, ex-GSTN backend engineer with 5.5 YOE. Would you be open to referring me for SDE-2/SDE-3 at [company]?'"},

  24: {"theme":"Dream Interviews — Active Rounds",
       "phase":2, "month":6,
       "dsa":"Maintain + mock contests", "diff":"Mixed", "lc_target":14,
       "lc_problems":["Daily 2 problems — stay sharp","Mock contest weekends",
                      "Review any patterns that resurface in interviews"],
       "tasks":[
         "Active final rounds at dream companies — stay composed, stay rested",
         "After every round: log all questions within 1 hour",
         "Offer negotiation: research Levels.fyi for exact RSU + base for your YOE",
         "Never reveal Phase 1 CTC first. 'I'm targeting market rate for this level.'"],
       "tip":"If you have Phase 1 offer in hand, you negotiate from strength. 'I have a competing offer at X — can you match?'"},

  25: {"theme":"Close Dream Offer",
       "phase":2, "month":6,
       "dsa":"Light — 1 problem daily", "diff":"Mixed", "lc_target":7,
       "lc_problems":["1 medium daily — stay warm","No hard grind this week — mental energy > problems"],
       "tasks":[
         "Final rounds — sleep 8 hours the night before every interview",
         "Negotiate: RSU cliff, joining bonus, sign-on, title (SDE-2 vs SDE-3 matters)",
         "Compare all offers holistically: base, RSU, bonus, growth, team, product",
         "Choose the one that maximises long-term trajectory, not just Day 1 CTC"],
       "tip":"8 hours sleep the night before final rounds matters more than one more practice problem at this stage."},

  26: {"theme":"Dream Offer Accepted — You Did It",
       "phase":2, "month":6,
       "dsa":"Wind down", "diff":"Easy", "lc_target":3,
       "lc_problems":["3 easy problems to stay warm"],
       "tasks":[
         "Offer accepted and negotiated. Take 2-3 weeks off before joining.",
         "Document your learnings in this repo — close the loop",
         "Share your journey on LinkedIn (anonymously if preferred) — pay it forward",
         "The discipline you built over 6 months is the real compound asset."],
       "tip":"You earned this. The habits built here — DSA daily, consistent learning, structured prep — serve you your entire career."},
}

# ─── Progress Management ──────────────────────────────────────────────────────
def load_progress():
    LOGS_DIR.mkdir(exist_ok=True)
    if PROG_FILE.exists():
        return json.loads(PROG_FILE.read_text())
    return {"lc_done": [], "applications": [], "daily_logs": {}, "topics_done": [], "offers": []}

def save_progress(p):
    LOGS_DIR.mkdir(exist_ok=True)
    PROG_FILE.write_text(json.dumps(p, indent=2, default=str))

# ─── Helpers ─────────────────────────────────────────────────────────────────
def week_num():
    days = (date.today() - START).days
    return max(1, min(26, days // 7 + 1))

def day_num():
    return max(1, (date.today() - START).days + 1)

def progress_bar(done, total, width=20):
    if total == 0:
        return "[" + "░" * width + "] 0/0"
    filled = round(done / total * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {done}/{total}"

def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print("─" * 60)

def lc_done_this_week(p, wk):
    wk_start = START + timedelta(days=(wk - 1) * 7)
    wk_end   = wk_start + timedelta(days=7)
    return sum(1 for e in p.get("lc_done", [])
               if wk_start <= date.fromisoformat(e["date"]) < wk_end)

def lc_total(p):
    """Returns the highest known LC count — synced from LeetCode or manually logged."""
    synced = p.get("lc_sync", {}).get("total", 0)
    manual = len(p.get("lc_done", []))
    return max(synced, manual)

def lc_today_count(p):
    """How many LC submissions today per LeetCode calendar."""
    return p.get("lc_sync", {}).get("today_submissions", 0)

def apps_total(p):
    return len(p.get("applications", []))

# ═══════════════════════════════════════════════════════════════════════════════
# STUDY PROTOCOLS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# ── Topic Registry ─────────────────────────────────────────────────────────────
TOPICS = {
    "java-core":     {"label": "Java Core",             "file": "Section_01_Java_Core.md",                      "q": "Q1–Q25",   "aliases": ["java","javacore","jc"]},
    "spring-boot":   {"label": "Spring Boot",           "file": "Section_02_Spring_Boot.md",                    "q": "Q26–Q60",  "aliases": ["spring","sb"]},
    "hibernate":     {"label": "Hibernate / JPA",       "file": "Section_03_Hibernate_JPA.md",                  "q": "Q61–Q90",  "aliases": ["jpa","orm"]},
    "microservices": {"label": "Microservices",         "file": "Section_04_05_06_Microservices_Kafka_Redis.md", "q": "Q91–Q135", "aliases": ["ms","micro"]},
    "kafka":         {"label": "Apache Kafka",          "file": "Section_04_05_06_Microservices_Kafka_Redis.md", "q": "Q91–Q135", "aliases": ["kfk"]},
    "redis":         {"label": "Redis / Caching",       "file": "Section_04_05_06_Microservices_Kafka_Redis.md", "q": "Q91–Q135", "aliases": ["cache"]},
    "database":      {"label": "Database & SQL",        "file": "Section_07_08_Database_DistributedSystems.md",  "q": "Q136–Q165","aliases": ["db","sql"]},
    "distributed":   {"label": "Distributed Systems",  "file": "Section_07_08_Database_DistributedSystems.md",  "q": "Q136–Q165","aliases": ["dist","ds"]},
    "patterns":      {"label": "Design Patterns",       "file": "Section_09_10_11_Patterns_Docker_CICD.md",      "q": "Q166–Q210","aliases": ["dp","design"]},
    "cloud":         {"label": "Cloud / AWS / Docker",  "file": "Section_12_13_14_15_Cloud_Network_Design_Go.md","q": "Q211–Q250","aliases": ["aws","docker"]},
    "golang":        {"label": "Golang",                "file": "Section_12_13_14_15_Cloud_Network_Design_Go.md","q": "Q241–Q250","aliases": ["go"]},
    "testing":       {"label": "Testing & Behavioral",  "file": "Section_16_17_18_19_Testing_Behavioral_Scenarios.md","q": "Q251–Q296","aliases": ["test","behav"]},
    "system-design": {"label": "System Design",        "file": "Section_21_SystemDesign_DeepDive_With_Answers.md","q": "Extra",   "aliases": ["sd","hld"]},
    "lld":           {"label": "Low-Level Design",      "file": "trackers-docs/LLD_Master_Interview_Sheet_v2.xlsx","q": "Extra",   "aliases": ["lowlevel"]},
    "behavioral":    {"label": "Behavioral / STAR",     "file": "GSTN_Complete_SDE2_SDE3_InterviewPrep.md",      "q": "Part 3,5","aliases": ["star","lp"]},
}

# Spaced repetition intervals by confidence score (days until next review)
SR_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}

# ── Active Recall Quiz Bank ────────────────────────────────────────────────────
QUIZ = {
    "java-core": [
        {"q": "How does HashMap work internally in Java 8? What changed from Java 7?",
         "hint": "Bucket array → LinkedList. Java 8: treeify at 8 → TreeMap O(log n). Load factor 0.75. hash = key.hashCode() ^ (h>>>16). Resize at 75% capacity."},
        {"q": "ConcurrentHashMap vs Collections.synchronizedMap() — internal difference?",
         "hint": "Java 7: 16 segments, each a separate lock. Java 8: CAS + synchronized only on bin head. synchronizedMap wraps entire map with 1 lock → worse concurrency."},
        {"q": "Explain CompletableFuture.allOf() vs anyOf(). How do you handle exceptions?",
         "hint": "allOf: wait for ALL. anyOf: wait for FIRST. Exceptions: thenApply won't catch, use exceptionally() or handle(). Chain: supplyAsync → thenApply → exceptionally."},
        {"q": "GC types: when would you use G1GC vs ZGC in a low-latency tax service?",
         "hint": "G1GC: default Java 9+, predictable pause times (<200ms). ZGC: <10ms pauses, for latency-critical. At GSTN: G1GC with -Xms/-Xmx tuning. ZGC if < 1ms needed."},
        {"q": "What is ThreadLocal? How would you use it in GSTN's microservices context?",
         "hint": "Per-thread storage. Use case: store request context (userId, correlationId) without passing through every method. Risk: memory leak in thread pools — always remove()."},
    ],
    "spring-boot": [
        {"q": "How does @Transactional work at the JVM level? What is the proxy mechanism?",
         "hint": "Spring creates a CGLIB/JDK proxy. Calls go through TransactionInterceptor. Only works on public methods. Self-invocation bypasses proxy — use AopContext.currentProxy() or inject self."},
        {"q": "REQUIRED vs REQUIRES_NEW propagation — when did you use each at GSTN?",
         "hint": "REQUIRED: join existing TX. REQUIRES_NEW: suspend current, start fresh (your GSTN ledger: always REQUIRES_NEW so ledger TX doesn't roll back main flow). NESTED: savepoint."},
        {"q": "How does Spring Boot auto-configuration work? What is spring.factories?",
         "hint": "META-INF/spring.factories lists EnableAutoConfiguration classes. Each has @Conditional. SpringApplication → ConfigurationClassParser → loads beans conditionally."},
        {"q": "Explain the Spring bean lifecycle from instantiation to destruction.",
         "hint": "Instantiate → populate properties → setBeanName (Aware) → BeanPostProcessor.before → @PostConstruct / afterPropertiesSet → BeanPostProcessor.after → ready → @PreDestroy / destroy."},
        {"q": "How does @Async work? What thread pool does it use and how do you configure it?",
         "hint": "Creates proxy. Default pool: SimpleAsyncTaskExecutor (new thread per task — NEVER use in prod). Configure ThreadPoolTaskExecutor bean with pool size. Return CompletableFuture."},
    ],
    "kafka": [
        {"q": "Kafka exactly-once semantics — how does your GSTN Consumer.java achieve it?",
         "hint": "enable.idempotence=true on producer. transactional.id set. Consumer: isolation.level=read_committed. Manual offset commit AFTER successful processing. Your DLQ pattern handles failures without duplicate processing."},
        {"q": "Consumer group rebalancing — what happens to uncommitted offsets?",
         "hint": "Rebalance triggered by: new consumer join, consumer leave, partition change. Uncommitted offsets → re-processed by new owner (at-least-once). CooperativeStickyAssignor minimises rebalance scope."},
        {"q": "Kafka partition key strategy — how did you design it for GSTN?",
         "hint": "Key=GSTIN → same taxpayer's events go to same partition → ordering guaranteed. Risk: hot partitions if GSTIN distribution is uneven. Use consistent hashing or add suffix."},
        {"q": "What is consumer lag and how do you monitor it in production?",
         "hint": "Lag = latest offset - committed offset. Monitor: kafka-consumer-groups.sh --describe. Or JMX: kafka.consumer:type=consumer-fetch-manager-metrics,records-lag-max. Alert on lag > threshold."},
        {"q": "Explain your DLQ (Dead Letter Queue) 3-tier error handling pattern.",
         "hint": "main-topic → on error → error-topic (retry 3x with backoff) → on failure → DLQ (manual investigation). Scheduled job retries error-topic. DLQ never retried automatically — needs human review."},
    ],
    "system-design": [
        {"q": "Design a Rate Limiter — token bucket vs sliding window. Which for GSTN APIs?",
         "hint": "Token bucket: allows burst (GSTN filing windows need this). Sliding window: smoother but more memory. For GSTN: token bucket per GSTIN with Redis. Key: GSTIN:api, value: count+timestamp. Lua script for atomicity."},
        {"q": "Walk through your GST Return Filing System design. Start with requirements.",
         "hint": "FR: file return, validate, calculate tax. NFR: 14M users, peak 500 RPS, 7yr retention, <2s. Stack: Stateless API → Kafka → HBase (returns) + MySQL (ledger) + Solr (search). Cache: JDG for GSTIN session."},
        {"q": "Design a Notification System at GSTN scale. How did you build it?",
         "hint": "Kafka fan-out: topic per channel (email/SMS/push). Template engine with personalisation. Async dispatch workers. Audit table in MySQL (every notification logged). Retry with exponential backoff. Rate limiting per GSTIN."},
        {"q": "Explain the Customizer Pattern (Strategy + Factory) from your GSTN codebase.",
         "hint": "CaseCustomizerFactory.getCustomizer(caseType) → returns AppealTranCaseCustomizer or AdjudicationCaseCustomizer. Each implements beforeCreateCase()/afterCreateCase(). Open/Closed Principle — add new case type without changing factory logic."},
        {"q": "How would you design a distributed ledger for tax credits? Trade-offs?",
         "hint": "MySQL for current balance (ACID, REQUIRES_NEW TX). HBase for full history (petabyte scale). XA transaction across both. Idempotency key prevents double-credit. Reconciliation batch job daily. Your exact GSTN architecture."},
    ],
    "behavioral": [
        {"q": "Tell me about the most complex technical problem you solved at GSTN.",
         "hint": "XA distributed transaction across Appeal + Ledger + Notification services. Situation: inconsistency between appeal state and tax credit. Action: Atomikos JTA, REQUIRES_NEW propagation, compensation logic. Result: ACID compliance at 14M user scale."},
        {"q": "Describe a time you disagreed with your team's technical decision.",
         "hint": "Structure: Situation (what was being decided), Your concern (technical reason), How you raised it (data/prototype), Outcome (either changed or respected decision with learning). Show: collaborative disagreement, not ego."},
        {"q": "Tell me about a production incident you were involved in.",
         "hint": "Structure: What broke (specific), How detected (monitoring/user report), Your immediate action, Root cause found (within X hours), Fix deployed, Post-mortem changes. Show ownership. Never blame others. Show learning."},
        {"q": "How do you explain your GSTN experience to a product company interviewer?",
         "hint": "Lead with scale: 14M users, 3B invoices/year. Lead with complexity: XA transactions, distributed caching, Kafka exactly-once. Translate: 'tax ledger = payment settlement, same consistency guarantees.' End with: 'Production Java distributed systems at national scale.'"},
    ],
    "database": [
        {"q": "B-tree vs Hash index — when would you use each? Give GSTN examples.",
         "hint": "B-tree: range queries, ORDER BY, LIKE prefix. GSTN: idx on (gstin, period, status). Hash: exact match only, O(1). GSTN: never used as MySQL InnoDB doesn't support hash. Covering index: include all SELECT columns to avoid table lookup."},
        {"q": "Explain isolation levels. Which does GSTN's ledger use and why?",
         "hint": "READ UNCOMMITTED (dirty read) → READ COMMITTED (default MySQL) → REPEATABLE READ (MySQL InnoDB default) → SERIALIZABLE. GSTN ledger: REPEATABLE READ or SERIALIZABLE for financial consistency. Trade-off: higher isolation = more lock contention."},
        {"q": "HBase row key design — how did you design it for GSTN returns?",
         "hint": "Key: GSTIN|PERIOD|RETURN_TYPE. Why: groups all returns for one taxpayer together (range scan). Risk: GSTIN hotspot (all 14M filers active July 31) → add salt prefix. Column families: return_data (immutable), status (mutable)."},
    ],
    "lld": [
        {"q": "Design a Parking Lot — walk through classes, interfaces, and patterns used.",
         "hint": "ParkingLot (Singleton) → ParkingFloor[] → ParkingSpot[]. VehicleType enum. Ticket (entry/exit time, spot). PaymentSystem Strategy (cash/card/online). Observer: SpotObserver notifies display board. Factory: SpotFactory."},
        {"q": "Implement LRU Cache with O(1) get and put. Which data structures?",
         "hint": "HashMap<key, Node> + DoublyLinkedList. get: HashMap lookup → move node to head → O(1). put: if exists → update + move to head; else → add to head + add to map; if capacity exceeded → remove tail + remove from map. All O(1)."},
        {"q": "Design a Pub-Sub system — map it to your GSTN Kafka consumer framework.",
         "hint": "Publisher → Topic → Subscriber (implements MessageProcessor). Your Consumer.java: abstract process(message), concrete processors per event type. Registry maps topic → processor list. Error handling: retry → error-topic → DLQ. Exactly-once via idempotency key."},
    ],
}

# ── SR Helpers ─────────────────────────────────────────────────────────────────
def resolve_topic(raw):
    """Resolve alias or partial name to canonical topic key."""
    raw = raw.lower().strip().replace(" ", "-")
    if raw in TOPICS:
        return raw
    for key, meta in TOPICS.items():
        if raw in meta.get("aliases", []) or raw in key:
            return key
    return None

def sr_next(confidence, current_interval_days=None):
    """Calculate next review date based on confidence (1–5)."""
    base  = SR_INTERVALS.get(confidence, 7)
    # If reviewing again and still confident, extend interval
    if current_interval_days and confidence >= 4:
        base = min(int(current_interval_days * 1.8), 60)
    return date.today() + timedelta(days=base)

def sr_due(p):
    """Return list of (topic_key, meta, sr_data) due for review today or overdue."""
    today = date.today()
    due   = []
    sr    = p.get("spaced_repetition", {})
    for key, meta in TOPICS.items():
        data = sr.get(key)
        if data:
            next_d = date.fromisoformat(data["next"])
            if next_d <= today:
                due.append((key, meta, data))
    return sorted(due, key=lambda x: x[2]["next"])

def sr_upcoming(p, days=7):
    """Topics coming up for review in the next N days."""
    today = date.today()
    cutoff = today + timedelta(days=days)
    upcoming = []
    sr = p.get("spaced_repetition", {})
    for key, meta in TOPICS.items():
        data = sr.get(key)
        if data:
            next_d = date.fromisoformat(data["next"])
            if today < next_d <= cutoff:
                upcoming.append((key, meta, data, next_d))
    return sorted(upcoming, key=lambda x: x[3])

# ─── Commands ─────────────────────────────────────────────────────────────────
def cmd_plan():
    p    = load_progress()
    wk   = week_num()
    dn   = day_num()
    w    = WEEKS.get(wk, WEEKS[26])
    today_str = date.today().strftime("%A, %B %d, %Y")
    lc_wk = lc_done_this_week(p, wk)

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         JAYANTI — SDE-2/SDE-3 PREP TRACKER             ║")
    print(f"║  Day {dn:<4} of 184 │ Week {wk:<2} │ Phase {w['phase']} │ Month {w['month']}           ║")
    print(f"║  {today_str:<56}║")
    print("╚══════════════════════════════════════════════════════════╝")

    section(f"WEEK {wk}: {w['theme']}")

    # ── Day-of-week context ────────────────────────────────────────────────────
    day_name = date.today().strftime("%A")
    day_focus = {
        "Monday":    ("New topic — first read + code examples",       "Gaurav Sen / ByteByteGo — 1 SD video"),
        "Tuesday":   ("Deep dive — internals + source code",          "PP Java Springboot — 1 module lesson"),
        "Wednesday": ("Q&A — question bank practice (prep question)", "LLD: Techie Content video + 1 design"),
        "Thursday":  ("System Design — draw + explain aloud",         "Hello Interview — SD mock round"),
        "Friday":    ("Weak area review — prep bugs",                 "Arpit Bhayani microservices deep dive"),
        "Saturday":  ("Mock interview — full timed round (prep mock)","PP DSA track — 3-5 problems"),
        "Sunday":    ("prep retro — reflect + plan next week",        "prep sr — review queue + plan"),
    }
    eve_focus, aft_topic = day_focus.get(day_name, ("Deep study", "Video resource"))

    # ── Problems checklist ─────────────────────────────────────────────────────
    done_names = {e["name"].lower() for e in p.get("lc_done", [])}
    probs_todo  = [p_ for p_ in w.get("lc_problems", []) if p_.lower() not in done_names]
    probs_done  = [p_ for p_ in w.get("lc_problems", []) if p_.lower() in done_names]

    # ── SR due today ───────────────────────────────────────────────────────────
    due_today = sr_due(p)

    print(f"\n  {'─'*58}")
    print(f"  ⏰  YOUR 13-HOUR PLAN TODAY — {day_name.upper()}")
    print(f"  {'─'*58}")

    # Window 1: 5AM–8AM
    print(f"\n  🌅  5:00 AM – 8:00 AM │ MORNING POWER BLOCK (3 hours)")
    sr_note = f"  ← {len(due_today)} topic(s) DUE TODAY" if due_today else ""
    print(f"  ├─ 5:00  prep sr                 → SR review queue{sr_note}")
    lc_prob = probs_todo[0] if probs_todo else (probs_done[0] if probs_done else w['dsa'])
    print(f"  ├─ 5:15  LeetCode: \"{lc_prob}\"")
    print(f"  │         [{w['diff']}]  ⚠️  Code in JAVA on LeetCode  (45 min)")
    print(f"  ├─ 6:00  prep quiz {list(TOPICS.keys())[wk % len(TOPICS)]}    → active recall (30 min)")
    print(f"  └─ 6:30  PP Java Springboot: Module 11 — 1 lesson   (90 min)")

    # Window 2: 2PM–4PM
    print(f"\n  ☀️   2:00 PM – 4:00 PM │ AFTERNOON DEEP WORK (2 hours)")
    section_file = w.get("tasks", [""])[0][:50] if w.get("tasks") else ""
    print(f"  ├─ 2:00  Read: {section_file}")
    print(f"  │         (Interview_Answers section for Week {wk})")
    print(f"  ├─ 3:15  prep study <topic> <1-5>  → log confidence")
    print(f"  └─ 3:30  {aft_topic}  (30 min)")

    # Window 3: 6PM–2AM
    lc_prob2 = probs_todo[1] if len(probs_todo) > 1 else f"{w['dsa']} — medium/hard"
    print(f"\n  🌙  6:00 PM – 2:00 AM │ EVENING MARATHON (8 hours)")
    print(f"  ├─  6:00  LeetCode: \"{lc_prob2}\"  (Java, 60 min)")
    print(f"  ├─  7:00  LLD: Techie Content — 1 video + problem  (60 min)")
    print(f"  ├─  8:00  Hello Interview: System Design mock         (60 min)")
    print(f"  ├─  9:00  {eve_focus}")
    print(f"  │         (90 min — tonight's tasks below)")
    print(f"  ├─ 10:30  prep mock java       → Java mock round     (45 min)")
    print(f"  ├─ 11:15  prep apply [company] → 2 applications      (30 min)")
    print(f"  ├─ 12:00  prep bugs + prep sr  → review failures     (30 min)")
    print(f"  ├─  1:00  Arpit Bhayani / blog reading               (45 min)")
    print(f"  └─  1:45  prep log             → log today           (15 min)")

    # ── Tonight's tasks ────────────────────────────────────────────────────────
    print(f"\n  📚  TONIGHT'S STUDY TASKS:")
    for i, task in enumerate(w["tasks"], 1):
        print(f"  {i}. {task}")

    # ── LC checklist ───────────────────────────────────────────────────────────
    print(f"\n  💻  THIS WEEK'S LC PROBLEMS  [{w['dsa']}]  {progress_bar(lc_wk, w['lc_target'])}")
    for prob in w.get("lc_problems", []):
        marker = "✓" if prob.lower() in done_names else "□"
        print(f"    {marker} {prob}")

    if due_today:
        print(f"\n  🔴  SR DUE TODAY:")
        for key, meta, data in due_today:
            print(f"    • {meta['label']}  (confidence was {data['confidence']}/5 on {data['last']})")
        print(f"    → prep quiz <topic>  then  prep study <topic> <1-5>")

    print(f"\n  ⚡  TIP: {w['tip']}")

    section("QUICK STATS")
    total_lc   = lc_total(p)
    total_apps = apps_total(p)
    phase1_lc  = 50
    phase2_lc  = 150
    # If already past Phase 1 target, always show against Phase 2 target
    lc_target  = phase2_lc if (w["phase"] == 2 or total_lc >= phase1_lc) else phase1_lc
    app_target = 60 if w["phase"] == 2 else 30

    print(f"  LeetCode this week:  {progress_bar(lc_wk, w['lc_target'])}")
    print(f"  LeetCode total:      {progress_bar(total_lc, lc_target)}")
    print(f"  Applications sent:   {progress_bar(total_apps, app_target)}  ({total_apps} total)")
    if p.get("offers"):
        print(f"  Offers in hand:      {len(p['offers'])} 🎉 ({', '.join(o['company'] for o in p['offers'])})")

    # Show synced LC badge if available
    lc_sync = p.get("lc_sync", {})
    if lc_sync:
        streak = lc_sync.get("streak", 0)
        streak_icon = "🔥" if streak >= 3 else ("✅" if streak >= 1 else "❌")
        today_subs = lc_sync.get("today_submissions", 0)
        last_sync = lc_sync.get("last_sync", "never")
        print(f"\n  LeetCode streak:     {streak} day(s) {streak_icon}   |   Today's submissions: {today_subs}   |   Last sync: {last_sync}")
    else:
        print(f"\n  💡 Run: prep sync  — to connect your LeetCode profile (hasbrovish95)")

    print(f"\n  Commands: prep log | prep lc \"Problem\" | prep apply \"Company\" | prep sync | prep review")
    print()

def cmd_log():
    p = load_progress()
    today = str(date.today())
    print(f"\n  Logging for {today}")
    print("  What did you do today? (one item per line, blank line to finish)\n")
    entries = []
    while True:
        try:
            line = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        entries.append(line)

    if not entries:
        print("  Nothing logged.")
        return

    if today not in p["daily_logs"]:
        p["daily_logs"][today] = []
    p["daily_logs"][today].extend(entries)
    save_progress(p)

    print(f"\n  ✅ Logged {len(entries)} item(s):")
    for e in entries:
        print(f"     • {e}")

    # Quick hint if no LeetCode mention
    text = " ".join(entries).lower()
    if not any(kw in text for kw in ["leetcode", "lc", "solved", "problem", "easy", "medium", "hard"]):
        print(f"\n  💡 No LeetCode logged today. Use: prep lc \"Problem Name\" to track it.")
    else:
        wk  = week_num()
        done = lc_done_this_week(p, wk)
        target = WEEKS[wk]["lc_target"]
        print(f"\n  📊 LeetCode this week: {progress_bar(done, target)}")
    print()

def cmd_lc(problem_name):
    p = load_progress()
    done_names = {e["name"].lower() for e in p.get("lc_done", [])}
    if problem_name.lower() in done_names:
        print(f"\n  ℹ️  '{problem_name}' already marked done.\n")
        return
    p["lc_done"].append({"name": problem_name, "date": str(date.today())})
    save_progress(p)
    wk      = week_num()
    done_wk = lc_done_this_week(p, wk)
    target  = WEEKS[wk]["lc_target"]
    total   = lc_total(p)
    print(f"\n  ✅ LeetCode: {problem_name}")
    print(f"  This week:  {progress_bar(done_wk, target)}")
    print(f"  All time:   {total} problems solved")
    if done_wk >= target:
        print(f"\n  🔥 Week {wk} DSA target hit! Do 1 bonus problem this weekend.")
    print()

def cmd_apply(company):
    p = load_progress()
    p["applications"].append({"company": company, "date": str(date.today()), "status": "Applied"})
    save_progress(p)
    total = apps_total(p)
    wk    = week_num()
    print(f"\n  ✅ Application logged: {company}  (total: {total})")
    if wk <= 3:
        print(f"  Getting your list ready — apply to 5+ companies in Week 4.")
    elif wk == 4 and total < 3:
        print(f"  ⚠️  Only {total} application(s). Apply to 5 more today.")
    elif wk <= 14 and total < (wk - 3) * 3:
        print(f"  ⚠️  Slightly behind pace. Target ~{(wk - 3) * 3}+ applications by now.")
    print()

def cmd_offer(company, ctc=""):
    p = load_progress()
    p.setdefault("offers", []).append({"company": company, "ctc": ctc, "date": str(date.today())})
    save_progress(p)
    print(f"\n  🎉 OFFER LOGGED: {company}")
    if ctc:
        print(f"  CTC: {ctc}")
    if WEEKS[week_num()]["phase"] == 1:
        print(f"\n  Phase 1 complete! Start Phase 2 immediately.")
        print(f"  This offer is your leverage — not your ceiling.")
    else:
        print(f"\n  DREAM OFFER! You earned every bit of this.")
    print()

def cmd_status():
    p      = load_progress()
    wk     = week_num()
    dn     = day_num()
    total_lc   = lc_total(p)
    total_apps = apps_total(p)
    total_logs = len(p.get("daily_logs", {}))

    weekly_lc = {}
    for entry in p.get("lc_done", []):
        d   = date.fromisoformat(entry["date"])
        w_n = max(1, ((d - START).days // 7) + 1)
        weekly_lc[w_n] = weekly_lc.get(w_n, 0) + 1

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              PROGRAMME PROGRESS DASHBOARD               ║")
    print("╚══════════════════════════════════════════════════════════╝")

    section("OVERALL")
    print(f"  Programme Day:     {dn} / 184")
    print(f"  Current Week:      {wk} / 26")
    print(f"  Phase:             {WEEKS[wk]['phase']}  ({'Getting first offer' if WEEKS[wk]['phase'] == 1 else 'Dream role prep'})")
    print(f"  LeetCode solved:   {total_lc}")
    print(f"  Applications sent: {total_apps}")
    print(f"  Days logged:       {total_logs}")

    if p.get("offers"):
        section("OFFERS IN HAND 🎉")
        for o in p["offers"]:
            ctc_str = f" — {o['ctc']}" if o.get("ctc") else ""
            print(f"  {o['date']}  {o['company']}{ctc_str}")

    section("WEEKLY LEETCODE TRACKER")
    for w_n in range(1, min(wk + 2, 27)):
        done   = weekly_lc.get(w_n, 0)
        target = WEEKS[w_n]["lc_target"]
        theme  = WEEKS[w_n]["theme"][:28]
        if w_n < wk:
            flag = "✓" if done >= target else ("~" if done > 0 else "✗")
        elif w_n == wk:
            flag = "→"
        else:
            flag = " "
        print(f"  W{w_n:2} {flag} {progress_bar(done, target, 12)}  {theme}")

    # LeetCode sync summary
    lc_sync = p.get("lc_sync", {})
    if lc_sync:
        section("LEETCODE PROFILE — hasbrovish95")
        easy, medium, hard = lc_sync.get("easy",0), lc_sync.get("medium",0), lc_sync.get("hard",0)
        streak = lc_sync.get("streak", 0)
        streak_icon = "🔥" if streak >= 3 else ("✅" if streak >= 1 else "❌")
        print(f"  Total: {lc_sync.get('total',0)}  │  Easy: {easy}  Medium: {medium}  Hard: {hard}")
        print(f"  Streak: {streak} day(s) {streak_icon}  │  Active days: {lc_sync.get('total_active_days',0)}")
        print(f"  Beats: Easy {lc_sync.get('beats_easy','?')}%  Medium {lc_sync.get('beats_medium','?')}%  Hard {lc_sync.get('beats_hard','?')}%")
        print(f"  Last sync: {lc_sync.get('last_sync','never')}  │  Run: prep sync  to refresh")

    section("RECENT APPLICATIONS")
    apps = sorted(p.get("applications", []), key=lambda x: x["date"], reverse=True)
    if not apps:
        print("  No applications logged yet.")
    else:
        for a in apps[:6]:
            print(f"  {a['date']}  {a['company']}  [{a.get('status','Applied')}]")
        if len(apps) > 6:
            print(f"  ... and {len(apps) - 6} more")
    print()

def cmd_review():
    p     = load_progress()
    wk    = week_num()
    w     = WEEKS.get(wk, WEEKS[26])
    lc_wk = lc_done_this_week(p, wk)
    target = w["lc_target"]
    total_apps = apps_total(p)
    total_lc   = lc_total(p)
    logs_count = len(p.get("daily_logs", {}))
    days_elapsed = day_num()

    print()
    section(f"WEEK {wk} REVIEW + FEEDBACK")

    # DSA
    print(f"\n  📊 DSA Progress: {progress_bar(lc_wk, target)}")
    if lc_wk == 0:
        print("  ❌ Zero LeetCode this week. This is the highest priority habit.")
        print("     Action: 1 easy problem tonight, right now, before anything else.")
    elif lc_wk < target * 0.5:
        print(f"  ⚠️  Behind target. Need {target - lc_wk} more by Sunday.")
        print("     Action: Swap 1 evening topic session for DSA this week.")
    elif lc_wk < target:
        print(f"  📈 Close — {target - lc_wk} more to hit weekly target.")
    else:
        print("  ✅ Weekly DSA target hit! Do 1-2 bonus problems this weekend.")

    # Applications
    print(f"\n  📬 Applications: {total_apps} total")
    if wk <= 3:
        print("  Applications start Week 4. Prepare resume now.")
    elif wk == 4 and total_apps == 0:
        print("  ❌ Week 4 and zero applications. Apply to 3 companies TODAY.")
        print("     Razorpay → Juspay → CRED. Takes 10 min each.")
    elif wk > 4 and total_apps < max(1, (wk - 3)) * 3:
        print(f"  ⚠️  Below pace. For Week {wk}, aim for {(wk - 3) * 3}+ applications.")
        print("     Action: 1 hour this weekend dedicated only to applications.")
    else:
        print(f"  ✅ {total_apps} applications — good cadence.")

    # Pace vs expected
    expected_lc = sum(WEEKS[w_]["lc_target"] for w_ in range(1, wk))
    lc_sync = p.get("lc_sync", {})
    lc_note = f" (LeetCode: {lc_sync['total']} total)" if lc_sync else ""
    print(f"\n  ⏱️  Cumulative pace: {total_lc} done{lc_note} vs {expected_lc} programme expected")
    if total_lc >= 150:
        print(f"  🏆 150+ problems solved — you've cleared the Phase 2 DSA target early!")
        print(f"     Focus: quality over quantity. Redo weak patterns. Do mock contests.")
    elif total_lc >= expected_lc:
        print(f"  ✅ On track or ahead. Keep the habit.")
    elif total_lc >= expected_lc * 0.75:
        print(f"  📈 Slightly behind by {expected_lc - total_lc} problems. Recoverable this week.")
    else:
        deficit = expected_lc - total_lc
        print(f"  ❌ Behind by {deficit} problems. Recovery mode: double DSA this weekend.")

    # Consistency
    log_rate = logs_count / max(days_elapsed, 1)
    print(f"\n  📓 Consistency: {logs_count}/{days_elapsed} days logged ({log_rate:.0%})")
    if log_rate < 0.4:
        print("  ⚠️  Low logging rate. Logging = accountability. 2 min at end of day.")

    # Next week preview
    next_wk = min(wk + 1, 26)
    print(f"\n  🎯 NEXT WEEK (Week {next_wk}): {WEEKS[next_wk]['theme']}")
    print(f"     DSA: {WEEKS[next_wk]['lc_target']} problems — {WEEKS[next_wk]['dsa']}")
    print(f"     Top task: {WEEKS[next_wk]['tasks'][0]}")
    print()

def _lc_graphql(query, variables=None):
    """Call LeetCode GraphQL API. Returns parsed JSON or None on failure."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        LC_API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode()
            if raw.strip().startswith("<"):   # got HTML (Cloudflare block)
                return None
            return json.loads(raw)
    except Exception:
        return None


def cmd_sync(silent=False):
    """Fetch stats from LeetCode profile and update progress.json."""
    p = load_progress()
    today = str(date.today())

    if not silent:
        print(f"\n  🔄 Syncing LeetCode profile: {LEETCODE_USER} ...")

    # ── 1. Fetch submission stats + calendar ──────────────────────────────────
    stats_query = """
    query($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats {
          acSubmissionNum { difficulty count }
        }
        problemsSolvedBeatsStats { difficulty percentage }
        languageProblemCount { languageName problemsSolved }
        userCalendar(year: %d) {
          streak totalActiveDays submissionCalendar
        }
      }
    }
    """ % date.today().year

    data = _lc_graphql(stats_query, {"username": LEETCODE_USER})

    if not data or not data.get("data", {}).get("matchedUser"):
        if not silent:
            print("  ❌ Could not reach LeetCode API. Check your internet connection.")
            print(f"     Profile URL: https://leetcode.com/u/{LEETCODE_USER}")
        return

    user  = data["data"]["matchedUser"]
    stats = {s["difficulty"]: s["count"] for s in user["submitStats"]["acSubmissionNum"]}
    beats = {b["difficulty"]: round(b["percentage"], 1) for b in user.get("problemsSolvedBeatsStats", [])}
    langs = {l["languageName"]: l["problemsSolved"] for l in user.get("languageProblemCount", [])}
    cal   = user.get("userCalendar", {})
    streak        = cal.get("streak", 0)
    total_active  = cal.get("totalActiveDays", 0)

    # Count today's submissions from calendar
    today_ts  = int(datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())
    sub_cal   = json.loads(cal.get("submissionCalendar", "{}"))
    today_subs = sub_cal.get(str(today_ts), 0)

    total  = stats.get("All", 0)
    easy   = stats.get("Easy", 0)
    medium = stats.get("Medium", 0)
    hard   = stats.get("Hard", 0)

    # ── 2. Detect delta since last sync ───────────────────────────────────────
    prev   = p.get("lc_sync", {})
    delta  = total - prev.get("total", 0)

    # ── 3. Save to progress.json ──────────────────────────────────────────────
    p["lc_sync"] = {
        "username":         LEETCODE_USER,
        "total":            total,
        "easy":             easy,
        "medium":           medium,
        "hard":             hard,
        "streak":           streak,
        "total_active_days": total_active,
        "today_submissions": today_subs,
        "beats_easy":       beats.get("Easy", 0),
        "beats_medium":     beats.get("Medium", 0),
        "beats_hard":       beats.get("Hard", 0),
        "java_problems":    langs.get("Java", 0),
        "cpp_problems":     langs.get("C++", 0),
        "python_problems":  langs.get("Python3", langs.get("Python", 0)),
        "go_problems":      langs.get("Go", 0),
        "languages":        langs,
        "last_sync":        today,
    }

    # Auto-log today if there were new problems solved
    if delta > 0:
        if today not in p["daily_logs"]:
            p["daily_logs"][today] = []
        p["daily_logs"][today].append(
            f"[LeetCode sync] {delta} new problem(s) solved (total: {total})"
        )

    save_progress(p)

    if silent:
        return

    # ── 4. Display results ────────────────────────────────────────────────────
    section(f"LEETCODE SYNC — {LEETCODE_USER}")
    print(f"\n  ✅ Synced successfully  (last sync: {today})")
    print()
    print(f"  Total solved:   {total:>4}  {progress_bar(total, 150)}")
    print(f"  Easy:           {easy:>4}  (beats {beats.get('Easy', '?')}% of users)")
    print(f"  Medium:         {medium:>4}  (beats {beats.get('Medium', '?')}% of users)")
    print(f"  Hard:           {hard:>4}  (beats {beats.get('Hard', '?')}% of users)")
    print()
    streak_icon = "🔥" if streak >= 3 else ("✅" if streak >= 1 else "❌")
    print(f"  Current streak: {streak} day(s) {streak_icon}")
    print(f"  Total active days: {total_active}")
    print(f"  Submissions today: {today_subs}")

    if delta > 0:
        print(f"\n  📈 {delta} new problem(s) solved since last sync — auto-logged!")
    elif delta == 0 and prev:
        print(f"\n  No new problems since last sync.")

    # Encouragement based on stats
    print()
    if streak == 0:
        print("  ⚠️  Streak is 0. Solve 1 problem today to start a new streak.")
    elif streak >= 7:
        print(f"  🔥 {streak}-day streak! Don't break it — 1 problem today keeps it alive.")

    if hard >= 10:
        print(f"  💪 {hard} hard problems solved — you're in strong territory for FAANG DSA.")
    elif medium >= 50:
        print(f"  📈 {medium} mediums done. Start adding 1 hard per week now.")

    print(f"\n  Profile: https://leetcode.com/u/{LEETCODE_USER}")
    print()


def cmd_check():
    """Smart coach — health check across all prep signals with personalised advice."""
    import subprocess

    # Silent sync to get fresh data
    cmd_sync(silent=True)
    p  = load_progress()
    wk = week_num()
    dn = day_num()
    w  = WEEKS.get(wk, WEEKS[26])

    lc_sync    = p.get("lc_sync", {})
    today      = str(date.today())
    total      = lc_sync.get("total", lc_total(p))
    easy       = lc_sync.get("easy", 0)
    medium     = lc_sync.get("medium", 0)
    hard       = lc_sync.get("hard", 0)
    streak     = lc_sync.get("streak", 0)
    java_cnt   = lc_sync.get("java_problems", 0)
    cpp_cnt    = lc_sync.get("cpp_problems", 0)
    today_subs = lc_sync.get("today_submissions", 0)
    total_apps = apps_total(p)
    lc_wk      = lc_done_this_week(p, wk)
    target_wk  = w["lc_target"]
    logs_count = len(p.get("daily_logs", {}))
    log_rate   = logs_count / max(dn, 1)
    last_sync  = lc_sync.get("last_sync", "")

    # Days into current week (0 = Monday of this week)
    days_into_wk    = max(1, (date.today() - (START + timedelta(days=(wk - 1) * 7))).days)
    expected_by_now = round(target_wk * days_into_wk / 7)

    # ── Build signal list ──────────────────────────────────────────────────────
    # Each signal: (label, icon, detail, is_critical)
    signals = []

    # 1. LeetCode streak
    if streak == 0:
        signals.append(("LeetCode streak",     "❌", "Broken — solve 1 problem RIGHT NOW",          True))
    elif streak >= 7:
        signals.append(("LeetCode streak",     "🔥", f"{streak} days — outstanding!",               False))
    else:
        signals.append(("LeetCode streak",     "✅", f"{streak} day(s) active",                     False))

    # 2. Weekly DSA pace
    if lc_wk == 0 and days_into_wk >= 2:
        signals.append(("Weekly DSA",          "❌", f"0/{target_wk} — haven't started this week",  True))
    elif lc_wk < expected_by_now:
        signals.append(("Weekly DSA",          "⚠️", f"{lc_wk}/{target_wk} — {expected_by_now - lc_wk} behind pace", False))
    else:
        signals.append(("Weekly DSA",          "✅", f"{lc_wk}/{target_wk} — on pace",              False))

    # 3. Java practice — CRITICAL gap (151 C++, 3 Java)
    if total > 30 and java_cnt < 10:
        signals.append(("Java DSA (language!)", "❌", f"Only {java_cnt} Java problems ({cpp_cnt} C++) — interviewers want Java", True))
    elif java_cnt < 30:
        signals.append(("Java DSA (language!)", "⚠️", f"{java_cnt} Java problems — aim for 30+ before interviews", False))
    else:
        signals.append(("Java DSA (language!)", "✅", f"{java_cnt} Java problems — good",            False))

    # 4. Hard problem ratio vs phase
    if wk >= 15 and hard < 20:
        signals.append(("Hard problems",       "⚠️", f"Only {hard} hard — Phase 2 needs 40+",       False))
    elif hard >= 30:
        signals.append(("Hard problems",       "✅", f"{hard} hard — strong FAANG prep",             False))
    else:
        signals.append(("Hard problems",       "✅" if wk < 15 else "⚠️", f"{hard} hard problems",  False))

    # 5. Medium depth (should be majority)
    if total > 50 and medium < total * 0.4:
        signals.append(("Medium depth",        "⚠️", f"Only {medium} mediums ({total} total) — raise the floor", False))
    else:
        signals.append(("Medium depth",        "✅", f"{medium} mediums — solid",                   False))

    # 6. Applications
    if wk <= 3:
        signals.append(("Applications",        "✅", "Starts Week 4 — focus on resume now",         False))
    elif wk == 4 and total_apps == 0:
        signals.append(("Applications",        "❌", "Week 4 — apply to 5 companies TODAY",         True))
    elif wk > 4 and total_apps < max(1, (wk - 3)) * 3:
        gap = max(1, (wk - 3)) * 3 - total_apps
        signals.append(("Applications",        "⚠️", f"{total_apps} sent — {gap} behind pace",     False))
    else:
        signals.append(("Applications",        "✅", f"{total_apps} sent — good cadence",           False))

    # 7. Daily log consistency
    if log_rate < 0.3:
        signals.append(("Daily logging",       "⚠️", f"{logs_count}/{dn} days ({log_rate:.0%}) — build this habit", False))
    else:
        signals.append(("Daily logging",       "✅", f"{logs_count}/{dn} days ({log_rate:.0%})",    False))

    # 8. Today's activity
    if today_subs > 0:
        signals.append(("Today's LeetCode",    "✅", f"{today_subs} submission(s) already today",   False))
    else:
        signals.append(("Today's LeetCode",    "⚠️" if streak > 0 else "❌",
                         "0 submissions today — don't break your streak",                            streak == 0))

    # 9. Sync freshness
    if last_sync != today:
        signals.append(("Data freshness",      "⚠️", f"Last synced: {last_sync or 'never'} — run: prep sync", False))
    else:
        signals.append(("Data freshness",      "✅", "Synced today",                                False))

    # ── Display ────────────────────────────────────────────────────────────────
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║              PREP COACH — HEALTH CHECK                 ║")
    print(f"║  {date.today().strftime('%A, %B %d, %Y'):<30}  Day {dn}/184 │ Week {wk}/26  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print(f"  {'SIGNAL':<26} {'STATUS':<5}  DETAIL")
    print(f"  {'─'*58}")

    criticals, warnings = [], []
    for label, icon, detail, is_crit in signals:
        print(f"  {label:<26} {icon:<5}  {detail}")
        if is_crit or icon == "❌":
            criticals.append((label, detail))
        elif icon == "⚠️":
            warnings.append((label, detail))

    # ── Top priority action ────────────────────────────────────────────────────
    print(f"\n  {'─'*58}")
    if criticals:
        print(f"\n  🚨 FIX TODAY ({len(criticals)} critical issue(s)):")
        for label, detail in criticals[:2]:
            print(f"     [{label}] {detail}")
    elif warnings:
        print(f"\n  ⚠️  WATCH THIS WEEK ({len(warnings)} warning(s)):")
        for label, detail in warnings[:2]:
            print(f"     [{label}] {detail}")
    else:
        print(f"\n  ✅ All signals green — excellent discipline!")

    # ── Personalised coach note ────────────────────────────────────────────────
    section("COACH NOTE")

    if java_cnt < 10 and total > 30:
        print(f"""
  🔴 MOST IMPORTANT THING RIGHT NOW: Switch to Java on LeetCode.

  You have {total} problems solved — {cpp_cnt} in C++, {java_cnt} in Java.
  Every company you're targeting (Amazon, Flipkart, Goldman, PhonePe) will
  ask you to write code LIVE in Java. Your C++ fluency won't transfer under
  interview pressure.

  How to fix: LeetCode → any problem → Code → change language to Java.
  Goal: 30 Java problems in the next 3 weeks. Start with problems you've
  already solved in C++ — the logic is the same, just Java syntax.

  This single change improves your interview performance more than 20 new
  problems solved in C++.""")

    elif streak == 0:
        print(f"""
  🔴 STREAK IS BROKEN — This is how prep falls apart.

  A broken streak doesn't mean failure. It means today matters more.
  Open LeetCode right now. Solve the easiest problem on your list.
  It takes 15 minutes. The habit is worth more than the problem.

  Your stats are strong ({total} problems, {medium} mediums, {hard} hard).
  Don't let inconsistency erase the foundation you've built.""")

    elif wk >= 4 and total_apps < 5:
        print(f"""
  🟡 YOU HAVE THE SKILLS — START APPLYING.

  {total} LeetCode problems solved. Strong GSTN experience. Good foundation.
  But zero applications means zero chances.

  Real interviews teach you more than any practice session.
  Even a rejection tells you: which round, which topic, what to fix.

  Action this week: Apply to 5 companies. Razorpay, Juspay, CRED,
  MakeMyTrip, Meesho. Each takes 10 minutes on their career site.
  Set a 1-hour timer and do all 5 today.""")

    elif hard < 15 and wk >= 10:
        print(f"""
  🟡 HARD PROBLEMS: TIME TO PUSH.

  {medium} mediums is solid. But with {hard} hard problems, you'll hit a wall
  in Phase 2 FAANG rounds. The jump from Medium to Hard feels massive at
  first — then the patterns start clicking.

  Action: Add 1 Hard problem per week starting now.
  Pick from: Trapping Rain Water, Binary Tree Max Path Sum, Word Search II.
  Spend 40 min, then read the approach. Don't just give up and read — try.""")

    elif streak >= 7 and log_rate > 0.7 and total_apps > 10:
        print(f"""
  ✅ EXCELLENT DISCIPLINE.

  {streak}-day streak. {total} problems. {total_apps} applications. {log_rate:.0%} logging rate.
  This is what cracking top companies looks like from the inside.

  Keep the daily habit. Add 1 mock interview this weekend.
  The compound effect of this consistency will show up in interviews.""")

    else:
        print(f"""
  📊 CURRENT STATE:
  {total} LeetCode solved ({easy}E / {medium}M / {hard}H) │ Streak: {streak}d │ {total_apps} applications

  You're on track. The biggest risk at your stage is inconsistency —
  2-3 days off breaks momentum that took weeks to build.

  One thing to push this week: {criticals[0][0] if criticals else (warnings[0][0] if warnings else 'mock interview')}""")

    print()
    print(f"  Run: prep sync    → refresh LeetCode data")
    print(f"  Run: prep review  → weekly progress + actions")
    print()


def cmd_notify(ntype):
    """Send a macOS notification. Called by launchd scheduled jobs."""
    import subprocess

    # Silent sync for fresh data
    cmd_sync(silent=True)
    p  = load_progress()
    wk = week_num()
    dn = day_num()
    w  = WEEKS.get(wk, WEEKS[26])

    lc_sync    = p.get("lc_sync", {})
    streak     = lc_sync.get("streak", 0)
    today_subs = lc_sync.get("today_submissions", 0)
    java_cnt   = lc_sync.get("java_problems", 0)
    total      = lc_sync.get("total", 0)
    lc_wk      = lc_done_this_week(p, wk)
    today      = str(date.today())

    if ntype == "morning":
        title = f"SDE Prep — Day {dn}/184  (Week {wk})"
        if streak == 0:
            body = f"⚠️ Streak BROKEN! Open LeetCode now. {w['dsa']} today."
        elif today_subs > 0:
            body = f"🔥 {streak}-day streak! {today_subs} done already. Evening topic: {w['theme'][:35]}"
        elif java_cnt < 10 and total > 30:
            body = f"🎯 DSA in JAVA today (only {java_cnt} Java problems!). {w['dsa']}"
        else:
            body = f"🎯 {streak}d streak | Today: {w['dsa']} [{w['diff']}] | Target: {w['lc_target']}/wk"

    elif ntype == "evening":
        logs_today = bool(p.get("daily_logs", {}).get(today))
        lc_done_today = today_subs > 0
        if not lc_done_today and streak > 0:
            title = "⚠️ SDE Prep — Streak at risk!"
            body  = f"No LeetCode today — {streak}d streak will break! Solve 1 problem now."
        elif not logs_today:
            title = "📚 SDE Prep — Evening Study Time"
            body  = f"Topic: {w['theme'][:40]}. Log your day: prep log"
        else:
            title = "📚 SDE Prep — Evening Study Time"
            body  = f"Great work today! Topic: {w['theme'][:35]}"

    elif ntype == "weekly":
        lc_wk  = lc_done_this_week(p, wk)
        target = w["lc_target"]
        apps   = apps_total(p)
        title  = f"📊 Weekly Review — Week {wk}/26"
        if lc_wk < target:
            body = f"DSA: {lc_wk}/{target} ⚠️ | Apps: {apps} | Run: prep review"
        else:
            body = f"DSA: {lc_wk}/{target} ✅ | Apps: {apps} | Great week! prep review"

    elif ntype == "terminal":
        # Short one-liner shown when terminal opens
        streak_icon = "🔥" if streak >= 3 else ("✅" if streak >= 1 else "❌")
        java_warn   = f" | ⚠️ Switch to Java!" if java_cnt < 10 and total > 30 else ""
        print(f"\n  ── Prep Tracker: Day {dn}/184 │ Week {wk} │ Streak {streak}d {streak_icon} │ LC {total} solved{java_warn}")
        print(f"     Today: {w['dsa']} [{w['diff']}]  │  prep plan  for full details\n")
        return

    else:
        return

    script = f'display notification "{body}" with title "{title}" sound name "Ping"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def cmd_sr():
    """Show spaced repetition review queue."""
    p = load_progress()
    due      = sr_due(p)
    upcoming = sr_upcoming(p, days=7)
    sr       = p.get("spaced_repetition", {})
    never    = [k for k in TOPICS if k not in sr]

    section("SPACED REPETITION QUEUE")
    print()

    if due:
        print(f"  🔴 DUE NOW ({len(due)} topic(s)):")
        for key, meta, data in due:
            overdue  = (date.today() - date.fromisoformat(data["next"])).days
            tag      = f"  ({overdue}d overdue)" if overdue > 0 else "  (due today)"
            conf_bar = "★" * data["confidence"] + "☆" * (5 - data["confidence"])
            print(f"    • {meta['label']:<26} Confidence: {conf_bar}{tag}")
            print(f"      Last: {data['last']}  │  File: {meta['file']}")
        print()
        print(f"  → prep study <topic> <1-5>   mark reviewed + schedule next")
        print(f"  → prep quiz  <topic>         quiz yourself first")
    else:
        print(f"  ✅ Nothing due today — great discipline!")

    if upcoming:
        print(f"\n  📅 COMING UP (next 7 days):")
        for key, meta, data, next_d in upcoming:
            days_left = (next_d - date.today()).days
            print(f"    • {meta['label']:<26} in {days_left}d  ({next_d})")

    if never:
        print(f"\n  📚 NOT YET ADDED TO SR ({len(never)} topics):")
        for key in never:
            print(f"    • {TOPICS[key]['label']:<26} prep study {key} <1-5>")

    print()


def cmd_study(topic_raw, confidence_raw):
    """Log a topic as studied with confidence score, schedule next review."""
    p   = load_progress()
    key = resolve_topic(topic_raw)
    if not key:
        print(f"\n  ❌ Unknown topic: '{topic_raw}'")
        print(f"  Available: {', '.join(TOPICS.keys())}")
        return

    try:
        confidence = int(confidence_raw)
        if not 1 <= confidence <= 5:
            raise ValueError()
    except (ValueError, TypeError):
        print(f"\n  ❌ Confidence must be 1–5  (1=no idea  3=shaky  5=nailed it)")
        return

    meta  = TOPICS[key]
    today = str(date.today())
    sr    = p.setdefault("spaced_repetition", {})
    prev  = sr.get(key, {})
    prev_interval = (date.today() - date.fromisoformat(prev["last"])).days if prev.get("last") else None
    next_review   = sr_next(confidence, prev_interval)

    sr[key] = {
        "confidence":  confidence,
        "last":        today,
        "next":        str(next_review),
        "study_count": prev.get("study_count", 0) + 1,
    }
    save_progress(p)

    conf_label = {1: "no idea 😰", 2: "vague 😕", 3: "shaky 🤔", 4: "solid 💪", 5: "nailed it 🔥"}
    days_till  = (next_review - date.today()).days
    print(f"\n  ✅ Logged: {meta['label']}  ({conf_label[confidence]})")
    print(f"  📅 Next review: {next_review}  ({days_till} day(s) from now)")
    print(f"  📊 Study count: {sr[key]['study_count']}x")
    if confidence <= 2:
        print(f"\n  ⚠️  Low confidence — re-read {meta['file']} tonight")
        print(f"     Focus on: {meta['q']}")
    elif confidence == 3:
        print(f"\n  💡 Shaky — try: prep teach {key}  to solidify")
    print()


def cmd_teach(topic_raw):
    """Feynman technique — explain a topic as if teaching a junior engineer."""
    key = resolve_topic(topic_raw)
    if not key:
        print(f"\n  ❌ Unknown topic: '{topic_raw}'")
        print(f"  Available: {', '.join(TOPICS.keys())}")
        return

    meta = TOPICS[key]
    teach_prompts = {
        "java-core":     ["How does HashMap handle collisions in Java 8 vs Java 7?",
                          "When does GC run and which GC types exist?",
                          "What is the Java Memory Model — happens-before?"],
        "spring-boot":   ["How does @Transactional work at the proxy level?",
                          "What is Spring auto-configuration (spring.factories)?",
                          "How does Spring Security filter chain work?"],
        "kafka":         ["How does a consumer group partition assignment work?",
                          "What guarantees Kafka's exactly-once semantics?",
                          "What causes consumer lag and how do you monitor it?"],
        "system-design": ["What are the components of a scalable URL shortener?",
                          "How would you design a rate limiter at GSTN scale?",
                          "CAP theorem — what does it mean practically?"],
        "database":      ["How does a B-tree index work?",
                          "What is the N+1 problem in Hibernate and how to fix it?",
                          "When would you denormalise a table?"],
        "behavioral":    ["STAR format — what does each letter mean?",
                          "Name 3 leadership principles you show at GSTN.",
                          "Explain your biggest technical win in 2 minutes."],
        "lld":           ["How would you design an LRU Cache?",
                          "Strategy vs Factory pattern — key difference?",
                          "SOLID principles — give 1 concrete example of each."],
        "microservices": ["How does circuit breaker prevent cascading failures?",
                          "Saga vs 2PC for distributed transactions — trade-offs?",
                          "How do you handle partial failures in a microservice call?"],
        "redis":         ["Redis vs Memcached — when to choose which?",
                          "What is Redis eviction policy and how did you configure it at GSTN?",
                          "How does JBoss DataGrid differ from standard Redis?"],
        "distributed":   ["CAP theorem — what does GSTN prioritise and why?",
                          "How does consistent hashing distribute load?",
                          "What is vector clock? When is it used?"],
        "hibernate":     ["1st level vs 2nd level cache in Hibernate?",
                          "LAZY vs EAGER loading — which caused issues at GSTN?",
                          "How does @Transactional(REQUIRES_NEW) behave with Hibernate sessions?"],
        "patterns":      ["Strategy + Factory pattern — your GSTN CaseCustomizer example?",
                          "Observer pattern — where in GSTN codebase?",
                          "When to use Singleton vs Prototype Spring bean?"],
        "cloud":         ["Docker vs VM — key difference for production?",
                          "Kubernetes: Pod vs Deployment vs Service — when to use each?",
                          "AWS EC2 vs Lambda — when to use each?"],
        "golang":        ["Go goroutines vs OS threads — how are they different?",
                          "Channel vs Mutex — when to use each?",
                          "How does Go handle errors differently from Java?"],
        "testing":       ["Unit vs Integration vs E2E — define the boundaries?",
                          "How to test a Kafka consumer?",
                          "Mockito mock vs spy — difference and use case?"],
    }
    prompts = teach_prompts.get(key, ["What is it?", "How does it work internally?", "When would you use it?"])

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  TEACH-IT PROTOCOL — {meta['label']:<36}║
  ╚══════════════════════════════════════════════════════════╝

  INSTRUCTIONS (Feynman Technique):
  1. Open a blank note / grab paper
  2. Set a 5-minute timer
  3. Explain "{meta['label']}" as if teaching a junior engineer
     who has NEVER heard of it before
  4. Be specific — code snippets, diagrams, examples
  5. After 5 min: check your gaps vs {meta['file']}
  6. The gaps you find = exactly what interviewers will probe

  REFERENCE:  {meta['file']}  │  {meta['q']}

  GUIDING QUESTIONS:""")
    for i, q in enumerate(prompts, 1):
        print(f"    {i}. {q}")

    print(f"""
  After teaching:
    prep study {key} <1-5>   → log confidence score
    prep quiz  {key}          → verify with quiz questions
""")


def cmd_bug(description):
    """Log a stumbling block or failure pattern to the bug journal."""
    p     = load_progress()
    today = str(date.today())
    wk    = week_num()
    bugs  = p.setdefault("bug_journal", [])

    entry = {"date": today, "week": wk, "description": description, "topic": None}
    for key, meta in TOPICS.items():
        if key in description.lower() or meta["label"].lower() in description.lower():
            entry["topic"] = key
            break

    bugs.append(entry)
    save_progress(p)

    print(f"\n  ✅ Bug logged (#{len(bugs)}): {description}")
    if entry["topic"]:
        print(f"  📎 Auto-tagged: {TOPICS[entry['topic']]['label']}")
    print(f"  📊 Total in journal: {len(bugs)}")
    print(f"\n  View all: prep bugs")
    print(f"  This builds your personal failure-pattern map — review weekly.\n")


def cmd_bugs():
    """View bug journal with frequency analysis."""
    p    = load_progress()
    bugs = p.get("bug_journal", [])

    section("BUG JOURNAL — FAILURE PATTERN TRACKER")

    if not bugs:
        print("\n  No bugs logged yet.")
        print("  When you blank on a question or get a wrong answer, run:")
        print("    prep bug \"<what you got wrong>\"")
        print("  This builds your personal weak-area map.\n")
        return

    topic_count = {}
    for bug in bugs:
        t = bug.get("topic") or "untagged"
        topic_count[t] = topic_count.get(t, 0) + 1

    print(f"\n  Total entries: {len(bugs)}")
    print(f"\n  📊 WEAK AREAS (by frequency):")
    for topic, cnt in sorted(topic_count.items(), key=lambda x: -x[1]):
        label = TOPICS.get(topic, {}).get("label", topic)
        bar   = "█" * cnt + "░" * max(0, 5 - cnt)
        print(f"    {label:<26} {bar} ({cnt}x)")

    print(f"\n  📝 RECENT ENTRIES (last 10):")
    for bug in bugs[-10:][::-1]:
        tag = f"  [{TOPICS[bug['topic']]['label']}]" if bug.get("topic") else ""
        print(f"    {bug['date']}  {bug['description']}{tag}")

    top_topic = max(topic_count, key=topic_count.get)
    if top_topic != "untagged":
        print(f"\n  🎯 Most common weak area: {TOPICS[top_topic]['label']}")
        print(f"     Action: prep quiz {top_topic}")
    print()


def cmd_interview_log(company):
    """Structured interview logging — questions, outcome, action items."""
    p     = load_progress()
    today = str(date.today())
    wk    = week_num()

    print(f"\n  📝 INTERVIEW LOG — {company}")
    print(f"  ─────────────────────────────────────────")
    print(f"  Enter details. Press Enter when done with each field.\n")

    def ask(label, default=""):
        try:
            val = input(f"  {label}: ").strip()
        except EOFError:
            val = ""
        return val or default

    round_type = ask("Round type (DSA/SD/LLD/Behavioral/HR)", "Unknown")
    outcome    = ask("Outcome (cleared/rejected/pending)", "pending")
    questions  = ask("Questions asked (brief summary)")
    went_well  = ask("What went well")
    struggled  = ask("What you struggled with")
    todo       = ask("Action items to fix (comma-separated)")

    entry = {
        "date": today, "week": wk, "company": company,
        "round": round_type, "outcome": outcome,
        "questions": questions, "went_well": went_well,
        "struggled": struggled, "todo": todo,
    }

    p.setdefault("interviews", []).append(entry)

    if struggled:
        p.setdefault("bug_journal", []).append({
            "date": today, "week": wk,
            "description": f"[{company} {round_type}] {struggled[:100]}",
            "topic": None,
        })

    save_progress(p)

    outcome_icon = "✅" if "clear" in outcome.lower() else ("❌" if "reject" in outcome.lower() else "⏳")
    print(f"\n  {outcome_icon} Logged: {company} — {round_type}  [{outcome}]")
    if todo:
        print(f"\n  🎯 Action items:")
        for item in todo.split(","):
            print(f"     • {item.strip()}")
    print(f"\n  View history: prep interviews\n")


def cmd_interviews():
    """View interview history and failure pattern analysis."""
    p          = load_progress()
    interviews = p.get("interviews", [])

    section("INTERVIEW LOG — HISTORY & PATTERNS")

    if not interviews:
        print("\n  No interviews logged yet.")
        print("  After each round, run: prep interview-log \"Company Name\"")
        print("  Track every question — builds a personal question bank.\n")
        return

    total    = len(interviews)
    cleared  = sum(1 for i in interviews if "clear" in i.get("outcome","").lower())
    rejected = sum(1 for i in interviews if "reject" in i.get("outcome","").lower())

    print(f"\n  Total rounds:  {total}")
    print(f"  Cleared: {cleared}  │  Rejected: {rejected}  │  Pending: {total-cleared-rejected}")
    if cleared + rejected > 0:
        print(f"  Pass rate:     {cleared/(cleared+rejected)*100:.0f}%")

    companies = {}
    for iv in interviews:
        companies.setdefault(iv["company"], []).append(iv)

    print(f"\n  📊 BY COMPANY:")
    for company, ivs in sorted(companies.items()):
        icons = ["✅" if "clear" in i.get("outcome","").lower() else ("❌" if "reject" in i.get("outcome","").lower() else "⏳") for i in ivs]
        print(f"    {company:<22} {' '.join(icons)}  ({', '.join(i['round'] for i in ivs)})")

    all_struggled = " ".join(i.get("struggled","") for i in interviews)
    if all_struggled.strip():
        hits = [meta["label"] for key, meta in TOPICS.items()
                if key in all_struggled.lower() or meta["label"].lower() in all_struggled.lower()]
        if hits:
            print(f"\n  ⚠️  RECURRING STRUGGLE AREAS:")
            for t in hits[:5]:
                print(f"    • {t}")

    print(f"\n  📝 RECENT ROUNDS:")
    for iv in interviews[-5:][::-1]:
        icon = "✅" if "clear" in iv.get("outcome","").lower() else ("❌" if "reject" in iv.get("outcome","").lower() else "⏳")
        print(f"  {icon} {iv['date']}  {iv['company']} — {iv['round']}  [{iv['outcome']}]")
        if iv.get("todo"):
            print(f"       → {iv['todo'][:80]}")
    print()


def cmd_java():
    """Java language gap tracker — problems to redo in Java."""
    p        = load_progress()
    lc_sync  = p.get("lc_sync", {})
    java_cnt = lc_sync.get("java_problems", 0)
    cpp_cnt  = lc_sync.get("cpp_problems", 0)
    total    = lc_sync.get("total", 0)
    wk       = week_num()
    w        = WEEKS.get(wk, WEEKS[1])

    section("JAVA LANGUAGE TRACKER")
    print(f"\n  Current:  {java_cnt} Java  │  {cpp_cnt} C++  │  {total} total")
    print(f"  {'─'*50}")

    if java_cnt < 30:
        gap = 30 - java_cnt
        print(f"""
  🔴 CRITICAL GAP: Only {java_cnt} Java problems.

  Every interview will require live Java coding.
  Your C++ fluency will NOT transfer under pressure.
  Target: 30 Java problems in the next 3 weeks ({gap} to go).
""")
    else:
        print(f"\n  ✅ {java_cnt} Java problems — solid foundation.")
        print(f"     Keep ratio: aim for 80% Java going forward.\n")

    print(f"  THIS WEEK'S PROBLEMS — redo in Java if previously done in C++:")
    for prob in w["lc_problems"]:
        print(f"    □ {prob}")

    print(f"""
  JAVA PATTERNS TO MASTER (most common in interviews):
    □ HashMap / HashSet  (LinkedHashMap for LRU)
    □ PriorityQueue  (min: PriorityQueue<>  max: reverseOrder())
    □ Deque / Stack  (use ArrayDeque, NOT Stack class)
    □ StringBuilder  (never String + in loops)
    □ Arrays.sort() / Collections.sort() with lambda
    □ Stream API: filter → map → collect

  ON LEETCODE:  Select problem → Code → change language to Java
  Goal:  5 Java problems this week — even easy ones done in C++.
  Run:   prep sync  → update your Java count after solving
""")


def cmd_quiz(topic_raw):
    """Active recall quiz — random question from a topic's bank."""
    import random

    key = resolve_topic(topic_raw) if topic_raw else None

    if key and key not in QUIZ:
        print(f"\n  No quiz questions for '{topic_raw}' yet.")
        print(f"  Available: {', '.join(QUIZ.keys())}\n")
        return

    if not key:
        key = random.choice(list(QUIZ.keys()))

    meta = TOPICS.get(key, {})
    q    = random.choice(QUIZ[key])

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  ACTIVE RECALL — {meta.get('label', key):<39}║
  ╚══════════════════════════════════════════════════════════╝

  QUESTION:  {q['q']}

  ── Think for 60 seconds before reading the hint ─────────""")

    try:
        input("\n  [Press Enter to reveal hint]")
    except EOFError:
        pass

    print(f"\n  HINT / KEY POINTS:\n  {q['hint']}\n")
    print(f"  ─────────────────────────────────────────────────────────")

    try:
        conf_raw = input("\n  How well did you know this? (1=no idea  3=shaky  5=nailed): ").strip()
        if conf_raw.isdigit() and 1 <= int(conf_raw) <= 5:
            cmd_study(key, conf_raw)
        else:
            print()
    except EOFError:
        print()

    print(f"  Run: prep quiz {key}  → another question from this topic")
    print(f"  Run: prep sr          → see your full review queue\n")


def cmd_focus(mins):
    """Pomodoro-style focus timer."""
    import time

    try:
        duration = int(mins)
    except (ValueError, TypeError):
        duration = 25

    wk = week_num()
    w  = WEEKS.get(wk, WEEKS[1])

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║         FOCUS SESSION — {duration} MINUTES                       ║
  ╚══════════════════════════════════════════════════════════╝
  Week {wk}: {w['theme']}
  Topic:  {w['dsa']}  [{w['diff']}]

  RULES:  Phone face-down  │  one task  │  no distractions

  Starting in""", end=" ", flush=True)

    try:
        for i in range(3, 0, -1):
            print(f"{i}...", end=" ", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        return

    print("\n\n  GO! 🎯\n")
    total_secs = duration * 60

    try:
        start = time.time()
        while True:
            elapsed   = int(time.time() - start)
            remaining = total_secs - elapsed
            if remaining <= 0:
                break
            m, s  = divmod(remaining, 60)
            filled = int(elapsed / total_secs * 40)
            bar    = "█" * filled + "░" * (40 - filled)
            print(f"\r  [{bar}] {m:02d}:{s:02d} remaining  ", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        elapsed_m = int((time.time() - start) / 60)
        print(f"\n\n  Session stopped at {elapsed_m} min. Good work!")
        return

    print(f"\n\n  ⏰ DONE! {duration} minutes complete.")
    print(f"  Take a 5-min break: stand up, water, walk.")
    print(f"  Then: prep log  to record what you did.\n")

    try:
        import subprocess
        subprocess.run(
            ["osascript", "-e", f'display notification "Focus session complete! Take a 5-min break." with title "⏰ {duration}min Focus Done" sound name "Glass"'],
            capture_output=True
        )
    except Exception:
        pass


def cmd_retro():
    """Structured weekly retrospective — review, reflect, plan."""
    p     = load_progress()
    wk    = week_num()
    today = str(date.today())

    lc_sync  = p.get("lc_sync", {})
    total    = lc_sync.get("total", lc_total(p))
    streak   = lc_sync.get("streak", 0)
    java_cnt = lc_sync.get("java_problems", 0)
    lc_wk    = lc_done_this_week(p, wk)
    target   = WEEKS[min(wk, 26)]["lc_target"]
    apps     = apps_total(p)
    bugs     = p.get("bug_journal", [])
    wk_bugs  = [b for b in bugs if b.get("week") == wk]
    sr_data  = p.get("spaced_repetition", {})
    next_wk  = min(wk + 1, 26)
    nw       = WEEKS[next_wk]

    lc_icon  = "✅" if lc_wk >= target else "⚠️"
    str_icon = "🔥" if streak >= 3 else ("✅" if streak >= 1 else "❌")
    app_icon = "✅" if apps > 0 and wk > 3 else ("─" if wk <= 3 else "⚠️")

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║       WEEKLY RETROSPECTIVE — Week {wk}/26                      ║
  ║       {date.today().strftime('%A, %B %d, %Y'):<28}               ║
  ╚══════════════════════════════════════════════════════════╝

  ── THIS WEEK'S NUMBERS ──────────────────────────────────""")

    print(f"  DSA this week:   {lc_wk}/{target}  {lc_icon}")
    print(f"  Streak:          {streak}d  {str_icon}")
    print(f"  Java problems:   {java_cnt}  {'✅' if java_cnt >= 30 else '⚠️ (target: 30+)'}")
    print(f"  Applications:    {apps} total  {app_icon}")
    print(f"  Bugs logged:     {len(wk_bugs)} this week  ({len(bugs)} total)")
    print(f"  SR topics:       {len(sr_data)} topics tracked")

    print(f"""
  ── REFLECTION PROMPTS (answer in your journal — 10 min) ─

  1. What is the ONE thing you did best this week?
     (Be specific: not "studied hard" but "understood Kafka rebalancing deeply")

  2. What topic confused you most this week?
     → Log it: prep bug "<what you got wrong>"

  3. Did you do a mock interview this week?
     (If no — schedule one for this weekend. It's the single highest-ROI activity.)

  4. What is ONE specific change you'll make next week?
     (Not "study more" — something concrete like "30 min Java DSA every morning")

  5. Java gap check: {java_cnt} Java problems.  Target: 30+
     {"✅ On track" if java_cnt >= 30 else "⚠️ Switch more problems to Java next week."}

  ── NEXT WEEK (Week {next_wk}) PREVIEW ─────────────────────────

  Theme:    {nw['theme']}
  DSA:      {nw['dsa']}  [{nw['diff']}]  │  Target: {nw['lc_target']} problems
  Key task: {nw['tasks'][0]}""")

    upcoming = sr_upcoming(p, days=7)
    if upcoming:
        print(f"\n  SR Reviews due next week: {len(upcoming)}")
        for key, meta, data, next_d in upcoming[:3]:
            print(f"    • {meta['label']:<26} {next_d}")

    p.setdefault("retros", []).append({
        "date": today, "week": wk,
        "lc_wk": lc_wk, "target": target,
        "streak": streak, "apps": apps,
    })
    save_progress(p)

    print(f"""
  ── COMMANDS TO START NEXT WEEK ─────────────────────────
  prep sr              → spaced repetition review queue
  prep java            → Java gap tracker
  prep check           → full health check
  prep interview-log   → log any interview from this week
  prep bug "<topic>"   → log a stumbling block

  🎯 The goal isn't a perfect week. It's a better week than last.
""")


def _parse_question_bank():
    """Parse GSTN_Interview_QuestionBank_296Q.md into a list of (num, section, text)."""
    qfile = BASE / "GSTN_Interview_QuestionBank_296Q.md"
    if not qfile.exists():
        return []
    import re
    questions = []
    current_section = "General"
    for line in qfile.read_text(encoding="utf-8").splitlines():
        sec_m = re.match(r"^##\s+SECTION\s+\d+[:\s]+(.+)", line, re.I)
        if sec_m:
            current_section = sec_m.group(1).strip().rstrip(".")
            continue
        q_m = re.match(r"^Q(\d+)\.\s+(.+)", line)
        if q_m:
            questions.append({
                "num":     int(q_m.group(1)),
                "section": current_section,
                "text":    q_m.group(2).strip(),
            })
    return questions


def cmd_question(topic_raw=None):
    """Random question from the 296-question bank — verbal practice mode."""
    import random, time

    questions = _parse_question_bank()
    if not questions:
        print("\n  ❌ Could not read GSTN_Interview_QuestionBank_296Q.md\n")
        return

    # Filter by topic if given
    if topic_raw:
        key = resolve_topic(topic_raw)
        # Map topic keys to section keywords
        section_map = {
            "java-core":     ["java core", "java"],
            "spring-boot":   ["spring boot", "spring"],
            "hibernate":     ["hibernate", "jpa"],
            "microservices": ["microservice"],
            "kafka":         ["kafka"],
            "redis":         ["redis", "caching"],
            "database":      ["database", "sql"],
            "distributed":   ["distributed"],
            "patterns":      ["pattern", "design pattern"],
            "cloud":         ["cloud", "aws", "docker"],
            "golang":        ["golang", "go"],
            "testing":       ["testing", "behavioral"],
            "system-design": ["system design"],
            "lld":           ["low-level", "lld"],
            "behavioral":    ["behavioral", "testing"],
        }
        kws = section_map.get(key, [topic_raw.lower()]) if key else [topic_raw.lower()]
        filtered = [q for q in questions if any(kw in q["section"].lower() for kw in kws)]
        pool = filtered if filtered else questions
    else:
        pool = questions

    q = random.choice(pool)

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  QUESTION BANK — Verbal Practice Mode                   ║
  ╚══════════════════════════════════════════════════════════╝

  Q{q['num']}.  [{q['section']}]

  {q['text']}

  ── Answer out loud. 90 seconds. No notes. ───────────────""")

    try:
        input("\n  [Press Enter when done answering]")
    except EOFError:
        pass

    # Confidence check
    try:
        conf = input("\n  How did you answer? (1=blanked  3=partial  5=nailed): ").strip()
        if conf.isdigit() and 1 <= int(conf) <= 5:
            p = load_progress()
            p.setdefault("question_scores", []).append({
                "date": str(date.today()), "q_num": q["num"],
                "section": q["section"], "confidence": int(conf),
            })
            save_progress(p)
            labels = {1: "Blank → add to prep bug + re-read section",
                      2: "Weak → re-read section tonight",
                      3: "Partial → prep teach the gap",
                      4: "Good → review in 4 days",
                      5: "Nailed → review in 16 days"}
            print(f"\n  {labels.get(int(conf), '')}")
            if int(conf) <= 2:
                p2 = load_progress()
                p2.setdefault("bug_journal", []).append({
                    "date": str(date.today()), "week": week_num(),
                    "description": f"Q{q['num']}: {q['text'][:80]}",
                    "topic": None,
                })
                save_progress(p2)
                print(f"  Auto-logged to bug journal.")
    except EOFError:
        pass

    print(f"\n  prep question               → another random question")
    print(f"  prep question <topic>       → topic-specific question")
    print(f"  prep question {q['num'] + 1}         → next question (Q{q['num'] + 1})\n")


def cmd_week_summary():
    """Export this week's progress as a shareable text snapshot."""
    p    = load_progress()
    wk   = week_num()
    dn   = day_num()
    w    = WEEKS[min(wk, 26)]
    today = str(date.today())

    lc_sync  = p.get("lc_sync", {})
    total    = lc_sync.get("total", lc_total(p))
    streak   = lc_sync.get("streak", 0)
    java_cnt = lc_sync.get("java_problems", 0)
    lc_wk    = lc_done_this_week(p, wk)
    target   = w["lc_target"]
    apps     = apps_total(p)

    # This week's LC problems done
    done_this_week = [
        e for e in p.get("lc_done", [])
        if e.get("week") == wk or (
            e.get("date") and e["date"] >= str(date.today() - timedelta(days=date.today().weekday()))
        )
    ]

    # This week's SR
    sr = p.get("spaced_repetition", {})
    sr_studied = [(k, v) for k, v in sr.items() if v.get("last", "") >= str(date.today() - timedelta(days=7))]

    # Bugs this week
    bugs_wk = [b for b in p.get("bug_journal", []) if b.get("week") == wk]

    # Interviews this week
    ivs_wk = [i for i in p.get("interviews", []) if i.get("week") == wk]

    summary = f"""
╔══════════════════════════════════════════════════════════╗
║         WEEK {wk}/26 SUMMARY — {today}                  ║
╚══════════════════════════════════════════════════════════╝

PROGRAMME:  Day {dn}/184  │  Phase {w['phase']}  │  Month {w['month']}
THEME:      {w['theme']}

── DSA ──────────────────────────────────────────────────
  This week:  {lc_wk}/{target}  {'✅' if lc_wk >= target else '⚠️'}
  All time:   {total} problems  (Java: {java_cnt}  ← must be 30+)
  Streak:     {streak} days  {'🔥' if streak >= 3 else '✅' if streak >= 1 else '❌'}
"""
    if done_this_week:
        summary += "  Problems done this week:\n"
        for e in done_this_week[-7:]:
            summary += f"    ✓ {e.get('name', '?')}\n"

    summary += f"""
── SPACED REPETITION ────────────────────────────────────
  Topics studied this week:  {len(sr_studied)}
"""
    for key, data in sr_studied[:5]:
        label = TOPICS.get(key, {}).get("label", key)
        summary += f"    • {label:<26} confidence {data['confidence']}/5\n"

    summary += f"""
── BUG JOURNAL ──────────────────────────────────────────
  Bugs logged this week:  {len(bugs_wk)}
"""
    for b in bugs_wk[-3:]:
        summary += f"    • {b['description'][:60]}\n"

    summary += f"""
── APPLICATIONS ─────────────────────────────────────────
  Total sent:  {apps}
"""
    recent_apps = [a for a in p.get("applications", []) if a.get("week") == wk]
    for a in recent_apps[-3:]:
        summary += f"    • {a['company']} ({a.get('date', '?')})\n"

    summary += f"""
── INTERVIEWS ───────────────────────────────────────────
  This week: {len(ivs_wk)}
"""
    for iv in ivs_wk:
        icon = "✅" if "clear" in iv.get("outcome","").lower() else ("❌" if "reject" in iv.get("outcome","").lower() else "⏳")
        summary += f"  {icon} {iv['company']} — {iv['round']} [{iv['outcome']}]\n"

    summary += f"""
── NEXT WEEK ────────────────────────────────────────────
  Week {min(wk+1, 26)}: {WEEKS[min(wk+1, 26)]['theme']}
  DSA:  {WEEKS[min(wk+1, 26)]['dsa']}  [{WEEKS[min(wk+1, 26)]['diff']}]  │  Target: {WEEKS[min(wk+1, 26)]['lc_target']} problems

  Paste this in Notion / WhatsApp / journal.
  It becomes your weekly accountability record.
"""
    print(summary)

    # Save to file
    summary_path = BASE / "logs" / f"week_{wk:02d}_summary.txt"
    LOGS_DIR.mkdir(exist_ok=True)
    summary_path.write_text(summary)
    print(f"  Also saved to: {summary_path}\n")


def cmd_mock(round_type_raw=None):
    """Timed mock interview round — simulates a real 45-minute interview."""
    import time, random

    round_map = {
        "java":      ("Java Deep Dive",       45, "java-core"),
        "dsa":       ("DSA / Problem Solving", 45, None),
        "sd":        ("System Design",         45, "system-design"),
        "lld":       ("Low-Level Design",      45, "lld"),
        "behavioral":("Behavioral / STAR",     30, "behavioral"),
        "kafka":     ("Kafka / Messaging",     30, "kafka"),
        "full":      ("Full Interview Loop",   90, None),
    }

    rt_key = (round_type_raw or "java").lower().replace("-", "")
    if rt_key not in round_map:
        print(f"\n  Available round types: {', '.join(round_map.keys())}")
        rt_key = "java"

    round_label, duration, topic_key = round_map[rt_key]
    wk = week_num()
    w  = WEEKS.get(wk, WEEKS[1])

    # Pick questions
    if rt_key == "dsa":
        # Pull from this week's LC problems
        problems = w.get("lc_problems", [])
        q_list = [{"q": f"Solve: {p}", "hint": f"Topic: {w['dsa']} [{w['diff']}]. Code in Java."} for p in problems[:3]]
    elif rt_key == "full":
        q_list = []
        for tk in ["java-core", "system-design", "behavioral"]:
            if QUIZ.get(tk):
                q_list.append(random.choice(QUIZ[tk]))
    elif topic_key and QUIZ.get(topic_key):
        all_q = QUIZ[topic_key]
        q_list = random.sample(all_q, min(3, len(all_q)))
    else:
        q_list = [random.choice(q) for tk, qs in QUIZ.items() for q in [qs] if qs][:3]

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  MOCK INTERVIEW — {round_label:<38}║
  ║  Duration: {duration} minutes  │  Week {wk}/26                     ║
  ╚══════════════════════════════════════════════════════════╝

  RULES (simulate the real thing):
  • No notes, no IDE, no Google
  • Think out loud — interviewers want to hear your reasoning
  • If stuck: state your approach, ask a clarifying question
  • Code in Java if it's a coding round

  Starting in 3 seconds...
""")

    try:
        for i in [3, 2, 1]:
            print(f"  {i}...", end=" ", flush=True)
            time.sleep(1)
        print("\n\n  🎯 BEGIN\n")
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        return

    session_start = time.time()
    results = []

    time_per_q = (duration * 60) // max(len(q_list), 1)

    for i, q in enumerate(q_list, 1):
        q_start = time.time()
        q_mins  = time_per_q // 60

        print(f"  ── QUESTION {i}/{len(q_list)} ({'~' + str(q_mins) + ' min'}) ────────────────────────────────")
        print(f"\n  {q['q']}\n")

        try:
            input(f"  [Working... Press Enter when done or when time is up]")
        except EOFError:
            pass

        elapsed = int(time.time() - q_start)
        print(f"\n  HINT / IDEAL ANSWER KEY:\n  {q['hint']}\n")

        try:
            score = input(f"  Self-score (1=didn't get it  3=partial  5=nailed): ").strip()
            score = int(score) if score.isdigit() and 1 <= int(score) <= 5 else 3
        except (EOFError, ValueError):
            score = 3

        results.append({"q": q["q"][:60], "score": score, "time_secs": elapsed})
        print(f"  Time on this question: {elapsed // 60}m {elapsed % 60}s\n")

    # ── Session summary ────────────────────────────────────────────────────────
    total_elapsed = int(time.time() - session_start)
    avg_score     = sum(r["score"] for r in results) / max(len(results), 1)

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  MOCK COMPLETE — {round_label:<39}║
  ╚══════════════════════════════════════════════════════════╝

  Total time:   {total_elapsed // 60}m {total_elapsed % 60}s
  Avg score:    {avg_score:.1f}/5  {'✅' if avg_score >= 4 else '⚠️' if avg_score >= 3 else '❌'}
  Questions:    {len(results)}

  ── PER-QUESTION BREAKDOWN:""")

    for i, r in enumerate(results, 1):
        icon = "✅" if r["score"] >= 4 else ("⚠️" if r["score"] == 3 else "❌")
        print(f"  {i}. {icon} Score {r['score']}/5  │  {r['time_secs']//60}m {r['time_secs']%60}s  │  {r['q']}")

    print(f"""
  ── WHAT TO DO NOW:""")
    if avg_score < 3:
        print(f"  ❌ Score below 3 — re-read the section, do prep teach <topic>, retry tomorrow")
    elif avg_score < 4:
        print(f"  ⚠️  Score {avg_score:.1f} — identify which question dragged you down. Add to prep bug.")
    else:
        print(f"  ✅ Score {avg_score:.1f} — solid round! Try a harder mock next time: prep mock full")

    # Log to interviews
    p = load_progress()
    p.setdefault("interviews", []).append({
        "date": str(date.today()), "week": wk,
        "company": "MOCK", "round": round_label,
        "outcome": f"score {avg_score:.1f}/5",
        "questions": " | ".join(r["q"] for r in results),
        "went_well": "", "struggled": "", "todo": "",
    })
    save_progress(p)
    print(f"\n  Logged to interview history.\n  Run: prep mock {rt_key}   → do it again tomorrow\n")


def cmd_help():
    print("""
  Jayanti's SDE Prep Tracker — All Commands
  ══════════════════════════════════════════

  DAILY:
  prep                           → today's plan
  prep plan                      → today's plan
  prep log                       → log what you did today
  prep check                     → smart health check + coach advice
  prep sync                      → sync LeetCode stats (hasbrovish95)

  DSA / LEETCODE:
  prep lc "Two Sum"              → mark LeetCode problem done
  prep java                      → Java language gap tracker
  prep quiz <topic>              → active recall quiz (random if no topic)
  prep focus [mins]              → Pomodoro timer (default: 25 min)

  SPACED REPETITION:
  prep sr                        → show review queue (due today + upcoming)
  prep study <topic> <1-5>       → log topic studied + schedule next review
  prep teach <topic>             → Feynman teach-it protocol

  BUG JOURNAL:
  prep bug "description"         → log a stumbling block / failure pattern
  prep bugs                      → view bug journal + weak area analysis

  INTERVIEWS:
  prep interview-log "Company"   → structured interview logging
  prep interviews                → interview history + pattern analysis

  APPLICATIONS:
  prep apply "Razorpay"          → log job application
  prep offer "Razorpay" 25LPA    → log an offer received

  QUESTION BANK (296 questions):
  prep question                  → random question from 296-question bank
  prep question <topic>          → topic-specific question (verbal practice)

  MOCK INTERVIEW:
  prep mock java                 → Java deep dive (45 min)
  prep mock dsa                  → DSA / problem solving (45 min)
  prep mock sd                   → System Design (45 min)
  prep mock lld                  → Low-Level Design (45 min)
  prep mock behavioral           → Behavioral / STAR (30 min)
  prep mock kafka                → Kafka / messaging (30 min)
  prep mock full                 → Full interview loop (90 min)

  PROGRESS & REVIEW:
  prep status                    → full progress dashboard
  prep review                    → weekly feedback + next steps
  prep retro                     → weekly retrospective
  prep week-summary              → export week summary (paste to Notion / journal)

  COMPANY RESEARCH:
  cat DEEP_RESEARCH_INTERVIEW_PATTERNS_2025_2026.md  → 54-company research report
  cat COMPANY_ANALYSIS.md                             → company tiers + salary

  RESOURCES:
  cat RESOURCES.md               → week-by-week playlist + PP module mapping

  TOPICS for study/quiz/teach/sr/question:
    java-core  spring-boot  hibernate  microservices  kafka  redis
    database   distributed  patterns   cloud  golang  testing
    system-design  lld  behavioral

  YOUR SCHEDULE (13 hours/day):
    5:00–8:00 AM   → Morning power block  (DSA + SR + PP Java)
    2:00–4:00 PM   → Afternoon deep work  (study section + SD video)
    6:00 PM–2:00AM → Evening marathon     (LC #2, LLD, Hello Interview, mock, apply)

  SETUP (one time):
    echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
    source ~/.zshrc
    """)

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    cmd  = args[0].lower() if args else "plan"

    if cmd in ("plan", "p", ""):
        cmd_plan()
    elif cmd in ("log", "l"):
        cmd_log()
    elif cmd in ("status", "s", "stats"):
        cmd_status()
    elif cmd in ("review", "r"):
        cmd_review()
    elif cmd == "lc":
        if len(args) < 2:
            print("  Usage: prep lc \"Problem Name\"")
        else:
            cmd_lc(" ".join(args[1:]))
    elif cmd == "apply":
        if len(args) < 2:
            print("  Usage: prep apply \"Company Name\"")
        else:
            cmd_apply(" ".join(args[1:]))
    elif cmd == "offer":
        if len(args) < 2:
            print("  Usage: prep offer \"Company Name\" [CTC]")
        else:
            ctc = args[2] if len(args) > 2 else ""
            cmd_offer(args[1], ctc)
    elif cmd in ("sync", "lcsync", "leetcode"):
        cmd_sync()
    elif cmd in ("check", "coach", "c"):
        cmd_check()
    elif cmd == "notify":
        ntype = args[1] if len(args) > 1 else "morning"
        cmd_notify(ntype)
    elif cmd in ("sr", "srs", "spaced"):
        cmd_sr()
    elif cmd in ("study", "studied"):
        if len(args) < 3:
            print("  Usage: prep study <topic> <1-5>")
            print("  Example: prep study kafka 4")
        else:
            cmd_study(args[1], args[2])
    elif cmd in ("teach", "feynman"):
        if len(args) < 2:
            print("  Usage: prep teach <topic>")
        else:
            cmd_teach(args[1])
    elif cmd in ("bug",):
        if len(args) < 2:
            print("  Usage: prep bug \"what you got wrong or couldn't answer\"")
        else:
            cmd_bug(" ".join(args[1:]))
    elif cmd in ("bugs", "buglog", "journal"):
        cmd_bugs()
    elif cmd in ("interview-log", "interviewlog", "interview"):
        company = " ".join(args[1:]) if len(args) > 1 else "Unknown Company"
        cmd_interview_log(company)
    elif cmd in ("interviews", "iv"):
        cmd_interviews()
    elif cmd in ("java", "javacheck"):
        cmd_java()
    elif cmd in ("quiz", "q"):
        topic = args[1] if len(args) > 1 else None
        cmd_quiz(topic)
    elif cmd in ("focus", "pomo", "timer"):
        mins = args[1] if len(args) > 1 else "25"
        cmd_focus(mins)
    elif cmd in ("retro", "retrospective", "weekly-retro"):
        cmd_retro()
    elif cmd in ("question", "qbank", "qb", "q296"):
        topic = args[1] if len(args) > 1 else None
        cmd_question(topic)
    elif cmd in ("week-summary", "weeksummary", "summary", "weekly"):
        cmd_week_summary()
    elif cmd in ("mock", "mockinterview", "simulate"):
        rt = args[1] if len(args) > 1 else "java"
        cmd_mock(rt)
    elif cmd in ("help", "h", "--help"):
        cmd_help()
    else:
        print(f"  Unknown command: {cmd}. Run: prep help")
