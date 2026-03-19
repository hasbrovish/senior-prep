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

import json, sys
from datetime import date, timedelta
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────
BASE      = Path(__file__).parent
LOGS_DIR  = BASE / "logs"
PROG_FILE = LOGS_DIR / "progress.json"
START     = date(2026, 3, 19)

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
    return len(p.get("lc_done", []))

def apps_total(p):
    return len(p.get("applications", []))

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

    print(f"\n  MORNING (6–7 AM) — DSA: {w['dsa']} [{w['diff']}]")
    print(f"  Weekly target: {progress_bar(lc_wk, w['lc_target'])}")

    done_names = {e["name"].lower() for e in p.get("lc_done", [])}
    print("\n  Problems to do (this week's list):")
    for prob in w.get("lc_problems", []):
        marker = "✓" if prob.lower() in done_names else "□"
        print(f"    {marker} {prob}")

    print(f"\n  EVENING (8–9 PM) — Study Tasks:")
    for i, task in enumerate(w["tasks"], 1):
        print(f"  {i}. {task}")

    print(f"\n  ⚡ TIP: {w['tip']}")

    section("QUICK STATS")
    total_lc   = lc_total(p)
    total_apps = apps_total(p)
    phase1_lc  = 50
    phase2_lc  = 150
    lc_target  = phase2_lc if w["phase"] == 2 else phase1_lc
    app_target = 60 if w["phase"] == 2 else 30

    print(f"  LeetCode this week:  {progress_bar(lc_wk, w['lc_target'])}")
    print(f"  LeetCode total:      {progress_bar(total_lc, lc_target)}")
    print(f"  Applications sent:   {progress_bar(total_apps, app_target)}  ({total_apps} total)")
    if p.get("offers"):
        print(f"  Offers in hand:      {len(p['offers'])} 🎉 ({', '.join(o['company'] for o in p['offers'])})")

    print(f"\n  Commands: prep log | prep lc \"Problem\" | prep apply \"Company\" | prep review | prep status")
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
    print(f"\n  ⏱️  Cumulative pace: {total_lc} done vs {expected_lc} expected")
    if total_lc >= expected_lc:
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

def cmd_help():
    print("""
  Jayanti's SDE Prep Tracker — All Commands
  ══════════════════════════════════════════
  prep                          → today's plan
  prep plan                     → today's plan
  prep log                      → log what you did today
  prep status                   → full progress dashboard
  prep review                   → weekly feedback + next steps
  prep lc "Two Sum"             → mark LeetCode problem done
  prep apply "Razorpay"         → log job application
  prep offer "Razorpay" 25LPA   → log an offer received

  SETUP (one time):
    echo 'alias prep="python3 /Users/jayanti/Documents/dev/senior-prep/prep.py"' >> ~/.zshrc
    source ~/.zshrc
    # Now just type: prep
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
    elif cmd in ("help", "h", "--help"):
        cmd_help()
    else:
        print(f"  Unknown command: {cmd}. Run: prep help")
