"""
Java DSA Daily Drill Engine.

Selects 3 targeted problems daily based on:
  - Current week's topic from the 26-week plan
  - Company trends from intel DB (what companies asked recently)
  - Your weakest patterns (from lc_done struggle data)
  - Java-specific priority (problems you've only done in C++)

Usage:
  from intel.drill import get_drill, mark_drill_done, get_drill_history
"""

from datetime import date
import json

# ─── NeetCode 150 with Company Tags ──────────────────────────────────────────
# Format: (lc_id, name, difficulty, pattern, companies[], java_tip)
NEETCODE_150 = [
    # Arrays & Hashing
    (1,    "Two Sum",                       "easy",   "arrays",         ["amazon","google","microsoft","adobe"], "HashMap<Integer,Integer> map"),
    (242,  "Valid Anagram",                 "easy",   "arrays",         ["amazon","microsoft"],                  "int[26] freq array"),
    (217,  "Contains Duplicate",            "easy",   "arrays",         ["amazon","google"],                     "HashSet<Integer>"),
    (238,  "Product of Array Except Self",  "medium", "arrays",         ["amazon","google","microsoft"],         "int[] prefix, suffix"),
    (271,  "Encode and Decode Strings",     "medium", "arrays",         ["google","amazon"],                     "length-prefix encoding"),
    (128,  "Longest Consecutive Sequence",  "medium", "arrays",         ["amazon","google","flipkart"],          "HashSet, iterate only starts"),
    (36,   "Valid Sudoku",                  "medium", "arrays",         ["amazon","microsoft"],                  "Set<String> for rows/cols/boxes"),
    (347,  "Top K Frequent Elements",       "medium", "arrays",         ["amazon","google","flipkart"],          "PriorityQueue<int[]> or bucket sort"),
    (49,   "Group Anagrams",                "medium", "arrays",         ["amazon","google","microsoft"],         "HashMap with sorted key"),

    # Two Pointers
    (167,  "Two Sum II",                    "medium", "two-pointers",   ["amazon","goldman"],                    "int left=0, right=n-1"),
    (15,   "3Sum",                          "medium", "two-pointers",   ["amazon","google","microsoft"],         "sort + two pointers, skip dupes"),
    (11,   "Container With Most Water",     "medium", "two-pointers",   ["amazon","google","flipkart"],          "greedy: move smaller pointer"),
    (42,   "Trapping Rain Water",           "hard",   "two-pointers",   ["amazon","google","goldman","apple"],   "maxLeft[i], maxRight[i] arrays"),
    (125,  "Valid Palindrome",              "easy",   "two-pointers",   ["amazon","microsoft"],                  "Character.isLetterOrDigit()"),

    # Sliding Window
    (3,    "Longest Substring Without Repeating","medium","sliding-window",["amazon","google","microsoft"],      "HashMap<Character,Integer> + left ptr"),
    (424,  "Longest Repeating Character Replacement","medium","sliding-window",["amazon","google"],             "int[26] count, max freq trick"),
    (567,  "Permutation in String",         "medium", "sliding-window", ["amazon","microsoft"],                  "int[26] arrays, exact match"),
    (76,   "Minimum Window Substring",      "hard",   "sliding-window", ["amazon","google","flipkart"],          "int[128] need[], have, formed"),
    (239,  "Sliding Window Maximum",        "hard",   "sliding-window", ["amazon","google"],                     "Deque<Integer> monotonic decreasing"),

    # Stack
    (20,   "Valid Parentheses",             "easy",   "stack",          ["amazon","google","microsoft"],         "Deque<Character> stack"),
    (150,  "Evaluate Reverse Polish Notation","medium","stack",         ["amazon","goldman","apple"],            "Deque<Integer> operand stack"),
    (155,  "Min Stack",                     "medium", "stack",          ["amazon","goldman","microsoft"],        "Deque<int[]> store [val, currentMin]"),
    (739,  "Daily Temperatures",            "medium", "stack",          ["amazon","google"],                     "Deque<Integer> monotonic decreasing"),
    (84,   "Largest Rectangle in Histogram","hard",   "stack",          ["amazon","google","flipkart"],          "Deque<Integer> monotonic increasing"),

    # Binary Search
    (704,  "Binary Search",                 "easy",   "binary-search",  ["amazon","google","microsoft"],         "int lo=0,hi=n-1; mid=(lo+hi)>>>1"),
    (74,   "Search a 2D Matrix",            "medium", "binary-search",  ["amazon","google"],                     "flatten: row=mid/n, col=mid%n"),
    (875,  "Koko Eating Bananas",           "medium", "binary-search",  ["amazon","google","flipkart"],          "binary search on answer"),
    (33,   "Search in Rotated Sorted Array","medium", "binary-search",  ["amazon","microsoft","google"],         "identify sorted half first"),
    (153,  "Find Minimum in Rotated Array", "medium", "binary-search",  ["amazon","microsoft"],                  "target is always less than rightmost"),
    (4,    "Median of Two Sorted Arrays",   "hard",   "binary-search",  ["amazon","google","goldman"],           "binary search on smaller array partitions"),

    # Linked List
    (206,  "Reverse Linked List",           "easy",   "linked-list",   ["amazon","microsoft","flipkart"],        "prev=null, curr, next iteratively"),
    (21,   "Merge Two Sorted Lists",        "easy",   "linked-list",   ["amazon","microsoft","google"],          "dummy head, merge in place"),
    (141,  "Linked List Cycle",             "easy",   "linked-list",   ["amazon","microsoft"],                   "slow/fast (Floyd's)"),
    (19,   "Remove Nth Node From End",      "medium", "linked-list",   ["amazon","microsoft","google"],          "two pointers gap of N"),
    (143,  "Reorder List",                  "medium", "linked-list",   ["amazon","google"],                      "find mid, reverse second, merge"),
    (146,  "LRU Cache",                     "medium", "linked-list",   ["amazon","google","flipkart","goldman"], "LinkedHashMap(cap,0.75f,true) or DLL+Map"),
    (23,   "Merge K Sorted Lists",          "hard",   "linked-list",   ["amazon","google","microsoft","goldman"],"PriorityQueue<ListNode> by val"),

    # Trees
    (226,  "Invert Binary Tree",            "easy",   "trees",         ["amazon","google","microsoft"],          "swap left/right, recurse"),
    (104,  "Maximum Depth of Binary Tree",  "easy",   "trees",         ["amazon","microsoft"],                   "1 + max(left, right)"),
    (543,  "Diameter of Binary Tree",       "easy",   "trees",         ["amazon","google","flipkart"],           "int[] maxDiam, return left+right"),
    (110,  "Balanced Binary Tree",          "easy",   "trees",         ["amazon","microsoft"],                   "height=-1 sentinel for unbalanced"),
    (100,  "Same Tree",                     "easy",   "trees",         ["amazon","microsoft"],                   "null checks then val+recurse"),
    (102,  "Binary Tree Level Order Traversal","medium","trees",        ["amazon","microsoft","google"],          "Queue<TreeNode>, poll per level"),
    (98,   "Validate Binary Search Tree",   "medium", "trees",         ["amazon","microsoft","google"],          "pass min/max bounds down"),
    (230,  "Kth Smallest in BST",           "medium", "trees",         ["amazon","google","goldman"],            "in-order traversal, count"),
    (105,  "Construct Tree from Preorder+Inorder","medium","trees",     ["amazon","google"],                     "HashMap for inorder index"),
    (124,  "Binary Tree Maximum Path Sum",  "hard",   "trees",         ["amazon","google","flipkart","goldman"], "int[] maxSum global, return one-branch"),
    (297,  "Serialize/Deserialize Binary Tree","hard","trees",         ["amazon","google"],                      "BFS with null markers"),

    # Heap / Priority Queue
    (703,  "Kth Largest Element in Stream", "easy",   "heap",          ["amazon","google"],                      "PriorityQueue min-heap size k"),
    (1046, "Last Stone Weight",             "easy",   "heap",          ["amazon"],                               "PriorityQueue reverseOrder()"),
    (973,  "K Closest Points to Origin",   "medium", "heap",          ["amazon","google","flipkart"],            "PriorityQueue<int[]> by dist"),
    (215,  "Kth Largest Element in Array",  "medium", "heap",          ["amazon","google","microsoft","goldman"], "min-heap size k  OR  quickselect"),
    (621,  "Task Scheduler",               "medium", "heap",          ["amazon","google","apple"],               "int[26] freq, maxFreq + count trick"),
    (355,  "Design Twitter",               "medium", "heap",          ["amazon","microsoft"],                    "PriorityQueue<int[]>, HashMap<userId,List>"),
    (295,  "Find Median from Data Stream", "hard",   "heap",          ["amazon","google","goldman"],             "maxHeap (lower) + minHeap (upper)"),

    # Graphs
    (200,  "Number of Islands",            "medium", "graphs",         ["amazon","google","microsoft","flipkart"],"DFS with visited[][] or mark '0'"),
    (133,  "Clone Graph",                  "medium", "graphs",         ["amazon","google","microsoft"],           "HashMap<Node,Node> + BFS"),
    (695,  "Max Area of Island",           "medium", "graphs",         ["amazon","google"],                       "DFS count cells, track global max"),
    (417,  "Pacific Atlantic Water Flow",  "medium", "graphs",         ["amazon","google"],                       "BFS from both oceans, find intersection"),
    (207,  "Course Schedule",              "medium", "graphs",         ["amazon","google","flipkart"],            "topological sort + cycle detection"),
    (210,  "Course Schedule II",           "medium", "graphs",         ["amazon","google"],                       "DFS post-order OR Kahn's BFS"),
    (684,  "Redundant Connection",         "medium", "graphs",         ["amazon","google"],                       "Union-Find"),
    (127,  "Word Ladder",                  "hard",   "graphs",         ["amazon","google"],                       "BFS, replace each char, use Set"),

    # Dynamic Programming
    (70,   "Climbing Stairs",              "easy",   "dp",            ["amazon","google","microsoft"],            "dp[i] = dp[i-1] + dp[i-2]"),
    (746,  "Min Cost Climbing Stairs",     "easy",   "dp",            ["amazon","google"],                        "dp[i] = min(dp[i-1],dp[i-2])+cost[i]"),
    (198,  "House Robber",                 "medium", "dp",            ["amazon","google","microsoft"],            "dp[i] = max(dp[i-1], dp[i-2]+nums[i])"),
    (213,  "House Robber II",              "medium", "dp",            ["amazon","google"],                        "run House Robber on [0..n-2] and [1..n-1]"),
    (5,    "Longest Palindromic Substring","medium", "dp",            ["amazon","google","microsoft","goldman"],  "expand around center OR dp[i][j]"),
    (647,  "Palindromic Substrings",       "medium", "dp",            ["amazon","google"],                        "expand around center"),
    (91,   "Decode Ways",                  "medium", "dp",            ["amazon","microsoft","flipkart"],          "dp[i]: check 1-digit and 2-digit"),
    (139,  "Word Break",                   "medium", "dp",            ["amazon","google","microsoft"],            "Set<String> dict, dp[i] = any valid split"),
    (300,  "Longest Increasing Subsequence","medium","dp",            ["amazon","google","goldman"],              "patience sort + binary search O(nlogn)"),
    (416,  "Partition Equal Subset Sum",   "medium", "dp",            ["amazon","google","flipkart"],             "boolean[] dp size sum/2+1"),
    (72,   "Edit Distance",                "medium", "dp",            ["amazon","google","goldman"],              "dp[i][j] = 1+min(insert,delete,replace)"),
    (312,  "Burst Balloons",               "hard",   "dp",            ["amazon","google"],                        "interval DP, last balloon in range"),
    (10,   "Regular Expression Matching",  "hard",   "dp",            ["amazon","google"],                        "dp[i][j] covers s[0..i-1] with p[0..j-1]"),

    # Greedy
    (121,  "Best Time to Buy and Sell Stock","easy", "greedy",        ["amazon","google","goldman","flipkart"],   "track minPrice, maxProfit"),
    (55,   "Jump Game",                    "medium", "greedy",        ["amazon","google","microsoft"],            "track maxReach, check if i <= maxReach"),
    (45,   "Jump Game II",                 "medium", "greedy",        ["amazon","google"],                        "greedily pick furthest reach each level"),
    (134,  "Gas Station",                  "medium", "greedy",        ["amazon","google"],                        "total>=0 means solution exists; reset start"),
    (846,  "Hand of Straights",            "medium", "greedy",        ["amazon","google"],                        "TreeMap, fill groups from smallest"),
    (763,  "Partition Labels",             "medium", "greedy",        ["amazon","google","microsoft"],            "lastIndex[char], grow partition"),

    # Intervals
    (57,   "Insert Interval",              "medium", "intervals",     ["amazon","google","microsoft"],            "three phases: before, overlap, after"),
    (56,   "Merge Intervals",              "medium", "intervals",     ["amazon","google","microsoft","goldman"],  "sort by start, merge if overlap"),
    (435,  "Non-Overlapping Intervals",    "medium", "intervals",     ["amazon","google"],                        "sort by end, greedy keep non-overlapping"),
    (1851, "Minimum Interval to Include Query","hard","intervals",    ["amazon","google"],                        "sort + PriorityQueue + offline queries"),

    # Backtracking
    (78,   "Subsets",                      "medium", "backtracking",  ["amazon","google","microsoft"],            "for loop + recurse OR bitmask"),
    (39,   "Combination Sum",              "medium", "backtracking",  ["amazon","google"],                        "backtrack with remaining target"),
    (40,   "Combination Sum II",           "medium", "backtracking",  ["amazon","google"],                        "sort, skip duplicates at same level"),
    (46,   "Permutations",                 "medium", "backtracking",  ["amazon","microsoft","google"],            "swap in-place + backtrack"),
    (131,  "Palindrome Partitioning",      "medium", "backtracking",  ["amazon","google"],                        "isPalin[i][j] precompute, backtrack"),
    (51,   "N-Queens",                     "hard",   "backtracking",  ["amazon","google"],                        "boolean[] col, diag1, diag2"),
    (79,   "Word Search",                  "medium", "backtracking",  ["amazon","microsoft","apple"],             "DFS with visited mark, restore"),

    # Bit Manipulation
    (136,  "Single Number",               "easy",   "bit-manipulation",["amazon","microsoft"],                   "XOR all elements"),
    (191,  "Number of 1 Bits",            "easy",   "bit-manipulation",["amazon","microsoft"],                   "n & (n-1) drops lowest set bit"),
    (338,  "Counting Bits",               "easy",   "bit-manipulation",["amazon","google"],                      "dp[i] = dp[i>>1] + (i&1)"),
    (268,  "Missing Number",              "easy",   "bit-manipulation",["amazon","google","microsoft"],           "XOR 0..n with all elements"),
    (190,  "Reverse Bits",                "easy",   "bit-manipulation",["amazon","microsoft"],                   "shift and OR in loop"),
    (371,  "Sum of Two Integers",         "medium", "bit-manipulation",["amazon","microsoft","google"],           "a^b sum without carry, (a&b)<<1 carry"),

    # Math & Geometry
    (202,  "Happy Number",                "easy",   "math",           ["amazon","microsoft"],                    "fast/slow pointers or Set"),
    (66,   "Plus One",                    "easy",   "math",           ["amazon","google"],                       "iterate from end, handle carry"),
    (50,   "Pow(x, n)",                   "medium", "math",           ["amazon","google","goldman"],             "fast exponentiation: x^n = x^(n/2) * x^(n/2)"),
    (43,   "Multiply Strings",            "medium", "math",           ["amazon","google","goldman"],             "int[m+n] result, add digit products"),
    (2013, "Detect Squares",              "medium", "math",           ["amazon","google"],                       "HashMap count + iterate all points"),
]

# ─── Explicit Problem IDs per Week (from MASTER_16H_WARPLAN.md) ──────────────
# Use these as the primary drill list when current week matches.
# Problems not in NEETCODE_150 (e.g. LC #876, #82, #83) are shown as URL-only.
WEEK_PROBLEMS = {
    1:  [1, 3, 11, 15, 121, 125, 167, 209, 238, 283, 424, 567],        # Arrays, Two Pointers, Sliding Window
    2:  [206, 21, 141, 142, 234, 876, 92, 82, 83, 160],                 # Linked Lists, Recursion
    3:  [20, 155, 232, 739, 84, 85, 496, 503, 901, 907],                # Stacks, Queues
    4:  [104, 102, 103, 199, 543, 124, 236, 235, 112, 113, 116, 226],   # Binary Trees
    5:  [98, 230, 450, 701, 215, 347, 373, 378, 502, 632],              # BST, Heap
    6:  [200, 207, 210, 417, 547, 684, 695, 733, 994, 1091],            # Graphs
    7:  [17, 39, 40, 46, 47, 51, 52, 78],                               # Backtracking
    8:  [70, 198, 213, 322, 518, 300, 1143, 516, 647, 5, 139, 140],     # DP Part 1
    9:  [62, 63, 64, 72, 97, 115, 118, 119, 120, 174],                  # DP Part 2
    10: [208, 211, 212, 421, 648, 676, 677, 745],                       # Tries
    11: [55, 45, 134, 135, 316, 406, 435, 452, 136, 137, 260, 268],     # Greedy, Bit Manipulation
    # Weeks 12-13: Mock/Polish — use pattern-based selection (no fixed list)
    14: [4, 23, 25, 41, 42, 76, 84, 85, 149, 154],                     # Hard DSA Ramp
    15: [312, 514, 664, 689, 730, 741, 818, 903, 920, 975],             # Hard DP
    16: [269, 329, 332, 399, 444, 753, 787, 815, 864, 947],             # Hard Graphs
    17: [28, 151, 165, 214, 336, 459, 572, 686],                        # String Algorithms
    21: [149, 224, 227, 282, 301, 330, 381, 432],                       # Math + Hard
}


# ─── Pattern → Week Mapping (aligns with WEEKS dict in prep.py) ──────────────
WEEK_PATTERNS = {
    1:  ["arrays"],
    2:  ["two-pointers", "sliding-window"],
    3:  ["arrays", "linked-list"],
    4:  ["stack", "binary-search"],
    5:  ["trees"],
    6:  ["trees", "heap"],
    7:  ["dp"],
    8:  ["graphs"],
    9:  ["heap", "greedy"],
    10: ["arrays", "linked-list", "stack"],
    11: ["backtracking", "trees"],
    12: ["binary-search", "sliding-window"],
    13: ["two-pointers", "sliding-window", "dp"],
    14: ["greedy", "intervals"],
    15: ["arrays", "two-pointers", "sliding-window"],
    16: ["binary-search", "linked-list"],
    17: ["graphs"],
    18: ["dp"],
    19: ["heap", "intervals"],
    20: ["backtracking", "bit-manipulation"],
    21: ["dp", "graphs"],
    22: ["heap", "bit-manipulation"],
    23: ["arrays", "dp"],
    24: ["graphs", "backtracking"],
    25: ["dp"],
    26: ["arrays", "linked-list", "trees", "graphs"],
}


def get_drill(week_num: int = None, company: str = None, java_count: int = 0,
              limit: int = 3) -> list[dict]:
    """
    Select today's drill problems.

    Selection logic (priority order):
    1. WEEK_PROBLEMS: explicit warplan problem IDs for this week (if defined)
    2. Pattern-based scoring from WEEK_PATTERNS + company trends
    3. Easy/medium bias when java_count < 30
    4. Hard problems for Phase 2 (week 15+)
    """
    if week_num is None:
        from datetime import date
        start = date(2026, 3, 19)
        delta = (date.today() - start).days
        week_num = min(max(1, delta // 7 + 1), 26)

    # ── If this week has an explicit warplan problem list, use those IDs ──────
    week_ids = WEEK_PROBLEMS.get(week_num)
    if week_ids:
        lc_id_index = {p[0]: p for p in NEETCODE_150}
        selected = []
        for lc_id in week_ids:
            if len(selected) >= limit:
                break
            if lc_id in lc_id_index:
                selected.append(lc_id_index[lc_id])
            else:
                # Problem not in NEETCODE_150 — create a stub entry
                name = f"LC #{lc_id}"
                selected.append((lc_id, name, "medium", "unknown", [], "check LC"))
        return [_format_drill_problem(p, java_count) for p in selected]

    # ── Fallback: pattern-based scoring ──────────────────────────────────────
    trending_patterns = _get_trending_patterns(company)
    week_pats = WEEK_PATTERNS.get(week_num, ["arrays"])

    scored = []
    for problem in NEETCODE_150:
        lc_id, name, diff, pattern, companies, java_tip = problem
        score = 0

        if pattern in week_pats:
            score += 3
        if pattern in trending_patterns:
            score += 2
        if company and company.lower() in [c.lower() for c in companies]:
            score += 2

        if java_count < 30:
            if diff == "easy":
                score += 2
            elif diff == "medium":
                score += 1

        if week_num >= 15 and diff == "hard":
            score += 1

        scored.append((score, problem))

    diff_order = {"easy": 0, "medium": 1, "hard": 2}
    scored.sort(key=lambda x: (-x[0], diff_order.get(x[1][2], 1)))

    selected = []
    used_patterns = set()
    for score, problem in scored:
        lc_id, name, diff, pattern, companies, java_tip = problem
        if len(selected) >= limit:
            break
        selected.append(problem)
        used_patterns.add(pattern)

    return [_format_drill_problem(p, java_count) for p in selected]


def _get_trending_patterns(company: str = None) -> list[str]:
    """Get patterns that are trending in intel DB."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        if company:
            rows = conn.execute("""
                SELECT topics FROM experience_rounds er
                JOIN experiences e ON er.experience_id = e.id
                WHERE LOWER(e.company) LIKE ? AND er.topics IS NOT NULL
                ORDER BY e.date_scraped DESC LIMIT 50
            """, (f"%{company.lower()}%",)).fetchall()
        else:
            rows = conn.execute("""
                SELECT topics FROM experience_rounds
                WHERE topics IS NOT NULL
                ORDER BY rowid DESC LIMIT 100
            """).fetchall()
        conn.close()

        import json
        pattern_map = {
            "graph": "graphs", "bfs": "graphs", "dfs": "graphs", "topological": "graphs",
            "dp": "dp", "dynamic": "dp",
            "tree": "trees", "binary tree": "trees", "bst": "trees",
            "heap": "heap", "priority queue": "heap",
            "sliding window": "sliding-window",
            "two pointer": "two-pointers",
            "binary search": "binary-search",
            "backtrack": "backtracking",
            "stack": "stack",
            "linked list": "linked-list",
        }
        trending = {}
        for row in rows:
            try:
                topics = json.loads(row[0]) if row[0] else []
                for t in topics:
                    t_lower = t.lower()
                    for keyword, pat in pattern_map.items():
                        if keyword in t_lower:
                            trending[pat] = trending.get(pat, 0) + 1
            except Exception:
                pass
        return sorted(trending.keys(), key=lambda k: -trending[k])[:3]
    except Exception:
        return []


def _format_drill_problem(problem: tuple, java_count: int) -> dict:
    lc_id, name, diff, pattern, companies, java_tip = problem
    java_priority = java_count < 30
    return {
        "lc_id":        lc_id,
        "name":         name,
        "difficulty":   diff,
        "pattern":      pattern,
        "companies":    companies,
        "java_tip":     java_tip,
        "url":          f"https://leetcode.com/problems/{name.lower().replace(' ', '-').replace('/', '-')}/",
        "java_priority": java_priority,
        "note":         f"SOLVE IN JAVA — only {java_count} Java problems so far" if java_priority else "",
    }


def print_drill(week_num: int = None, company: str = None, java_count: int = 0):
    """Print today's drill problems in a formatted way."""
    if week_num is None:
        start = date(2026, 3, 19)
        delta = (date.today() - start).days
        week_num = min(max(1, delta // 7 + 1), 26)

    # For warplan weeks, show the full problem list (not just 3)
    week_ids = WEEK_PROBLEMS.get(week_num)
    limit = len(week_ids) if week_ids else 3
    problems = get_drill(week_num=week_num, company=company, java_count=java_count, limit=limit)

    print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  JAVA DSA DAILY DRILL — {date.today().strftime('%A, %B %d'):<32}║
  ╚══════════════════════════════════════════════════════════╝
""")

    if java_count < 30:
        gap = 30 - java_count
        print(f"  🔴 Java Gap: {java_count}/30 problems — solve ALL of these in Java today\n")
    else:
        print(f"  ✅ Java base: {java_count} problems. Keep going!\n")

    for i, p in enumerate(problems, 1):
        diff_color = "🟢" if p["difficulty"] == "easy" else ("🟡" if p["difficulty"] == "medium" else "🔴")
        companies_str = ", ".join(p["companies"][:3])
        print(f"  {i}. {diff_color} [{p['difficulty'].upper()}] #{p['lc_id']} — {p['name']}")
        print(f"     Pattern:   {p['pattern']}")
        print(f"     Companies: {companies_str}")
        print(f"     Java tip:  {p['java_tip']}")
        if p.get("note"):
            print(f"     ⚠️  {p['note']}")
        print(f"     URL: {p['url']}")
        print()

    print(f"  Target time: ~90 minutes total (~30 min each)")
    print(f"  Rule: Code in Java. Think aloud. Check complexity after.")
    print()
    print(f"  Mark done:  prep drill done \"Problem Name\"")
    print(f"  Get hints:  prep drill hint \"Problem Name\"")
    print()


def get_drill_history(limit: int = 7) -> list[dict]:
    """Get recent drill completion history from DB."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        rows = conn.execute("""
            SELECT * FROM drill_sessions
            ORDER BY date_done DESC LIMIT ?
        """, (limit,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def mark_drill_done(problem_name: str, time_mins: int = 0,
                    struggled: bool = False, language: str = "java") -> bool:
    """Log a drill completion to the DB."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        conn.execute("""
            INSERT INTO drill_sessions
            (date_done, problem_name, time_mins, struggled, language)
            VALUES (?, ?, ?, ?, ?)
        """, (str(date.today()), problem_name, time_mins, int(struggled), language))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_drill_stats() -> dict:
    """Get drill statistics for progress tracking."""
    try:
        from intel.db import get_conn
        conn = get_conn()
        total = conn.execute("SELECT COUNT(*) FROM drill_sessions").fetchone()[0]
        java  = conn.execute("SELECT COUNT(*) FROM drill_sessions WHERE language='java'").fetchone()[0]
        streak_rows = conn.execute("""
            SELECT DISTINCT date_done FROM drill_sessions
            ORDER BY date_done DESC LIMIT 30
        """).fetchall()
        conn.close()

        # Calculate streak
        streak = 0
        today = date.today()
        dates = [date.fromisoformat(r[0]) for r in streak_rows]
        for i, d in enumerate(dates):
            expected = today - __import__('datetime').timedelta(days=i)
            if d == expected:
                streak += 1
            else:
                break

        return {"total": total, "java": java, "streak": streak}
    except Exception:
        return {"total": 0, "java": 0, "streak": 0}
