# DSA in Java — Pattern Templates + DP Complete Guide
# For Java Backend Engineer (SDE-2/SDE-3) | Transitioning from C++
# Companies: Razorpay, CRED, Flipkart, Amazon, Swiggy, Stripe, Google

---

## SECTION 1: Java DSA Cheat Sheet — C++ → Java Translation

### Collections Side-by-Side

| C++ | Java | Notes |
|---|---|---|
| `vector<int>` | `List<Integer>` / `int[]` | Use `int[]` for fixed size, `ArrayList<>` for dynamic |
| `set<int>` | `TreeSet<Integer>` | Sorted. Use `HashSet<>` if order doesn't matter (O(1)) |
| `unordered_set<int>` | `HashSet<Integer>` | O(1) avg add/contains |
| `map<int,int>` | `TreeMap<Integer,Integer>` | Sorted by key |
| `unordered_map<int,int>` | `HashMap<Integer,Integer>` | O(1) avg |
| `priority_queue<int>` | `PriorityQueue<Integer>` | Min-heap by default! (opposite of C++) |
| `priority_queue<int, vector<int>, greater<int>>` | `PriorityQueue<>(Collections.reverseOrder())` | Max-heap in Java |
| `stack<int>` | `Deque<Integer> stack = new ArrayDeque<>()` | Use Deque, not Stack class |
| `queue<int>` | `Queue<Integer> q = new LinkedList<>()` | or `ArrayDeque<>` |
| `deque<int>` | `Deque<Integer> dq = new ArrayDeque<>()` | |
| `pair<int,int>` | `int[]` or `new int[]{a, b}` | No Pair class in standard Java |
| `sort(arr, arr+n)` | `Arrays.sort(arr)` | |
| `sort(v.begin(), v.end(), cmp)` | `Arrays.sort(arr, (a,b) -> a-b)` | Lambda comparator |

### Critical Java DSA Pitfalls (C++ devs hit these)

```java
// PITFALL 1: Integer overflow in comparators
// BAD (overflow when a is MIN_VALUE):
Arrays.sort(arr, (a, b) -> a - b);
// GOOD:
Arrays.sort(arr, Integer::compare);
// OR: Arrays.sort(arr, (a, b) -> Integer.compare(a, b));

// PITFALL 2: Java PriorityQueue is MIN-heap (C++ is MAX-heap)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();           // min at top
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder()); // max at top

// PITFALL 3: == vs .equals() for Integer objects
Integer a = 127, b = 127; // a == b is TRUE (cached)
Integer c = 128, d = 128; // c == d is FALSE (not cached!) → use c.equals(d)

// PITFALL 4: Autoboxing cost in hot loops
// BAD: List<Integer> in tight loop
List<Integer> list = new ArrayList<>();
for (int i : list) { } // each iteration unboxes — adds up

// PITFALL 5: String concatenation in loop
// BAD:
String s = "";
for (char c : chars) s += c; // O(n²) — creates new String each time
// GOOD:
StringBuilder sb = new StringBuilder();
for (char c : chars) sb.append(c); // O(n)
String result = sb.toString();

// PITFALL 6: Arrays.sort on primitives vs objects
int[] arr = {3,1,2};
Arrays.sort(arr);                    // OK — sorts ascending
Integer[] arr2 = {3,1,2};
Arrays.sort(arr2, (a,b) -> b-a);    // Can use lambda on Integer[] (object), not int[]
```

### Commonly Used Java Methods in DSA

```java
// String
s.charAt(i)               // character at index
s.toCharArray()           // char[]
s.substring(i, j)         // [i, j) — end exclusive
String.valueOf(charArr)   // char[] → String
s.split("")               // split into individual chars

// Arrays
Arrays.fill(arr, val)     // fill all with val
Arrays.copyOfRange(arr, from, to)  // [from, to)
Arrays.asList(1, 2, 3)   // List from varargs

// Collections
Collections.sort(list)
Collections.reverse(list)
Collections.frequency(list, val)
Collections.nCopies(n, val)       // List of n copies of val

// Math
Math.max(a, b), Math.min(a, b)
Math.abs(x)
(int) Math.ceil(a / (double) b)   // ceiling division
Integer.MAX_VALUE, Integer.MIN_VALUE
```

---

## SECTION 2: Pattern Templates — "When I see X, I write Y"

---

### Pattern 1: Sliding Window (Fixed Size)

**Trigger:** "subarray/substring of size k", "maximum/minimum of window"

```java
public int slidingWindowFixed(int[] arr, int k) {
    int windowSum = 0, result = 0;

    // Initialize first window
    for (int i = 0; i < k; i++) windowSum += arr[i];
    result = windowSum;

    // Slide window
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i];         // add new element
        windowSum -= arr[i - k];     // remove old element
        result = Math.max(result, windowSum);
    }
    return result;
}
```

**Examples:** Maximum Sum Subarray of Size K, Find All Anagrams (#438), Permutation in String (#567)

---

### Pattern 2: Sliding Window (Variable Size)

**Trigger:** "longest/shortest subarray/substring satisfying condition"

```java
public int slidingWindowVariable(int[] arr, int target) {
    int left = 0, result = 0, windowState = 0;

    for (int right = 0; right < arr.length; right++) {
        // Expand: add arr[right] to window
        windowState += arr[right];

        // Shrink: while condition violated, move left
        while (windowState > target) {
            windowState -= arr[left];
            left++;
        }

        // Update result (window is valid here)
        result = Math.max(result, right - left + 1);
    }
    return result;
}
```

**Examples:** Longest Substring Without Repeating (#3), Minimum Window Substring (#76), Longest Repeating Char Replacement (#424)

---

### Pattern 3: Two Pointers (Opposite Direction)

**Trigger:** "sorted array", "sum equals target", "palindrome"

```java
public List<List<Integer>> twoSum(int[] sorted, int target) {
    List<List<Integer>> result = new ArrayList<>();
    int left = 0, right = sorted.length - 1;

    while (left < right) {
        int sum = sorted[left] + sorted[right];
        if (sum == target) {
            result.add(Arrays.asList(sorted[left], sorted[right]));
            left++; right--;
            // Skip duplicates if needed:
            while (left < right && sorted[left] == sorted[left-1]) left++;
        } else if (sum < target) left++;
        else right--;
    }
    return result;
}
```

**Examples:** 3Sum (#15), Container With Most Water (#11), Trapping Rain Water (#42)

---

### Pattern 4: Fast & Slow Pointers

**Trigger:** "cycle in linked list", "find middle of linked list", "nth from end"

```java
// Detect cycle
public boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;
    }
    return false;
}

// Find middle
public ListNode findMiddle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow; // slow is at middle
}
```

---

### Pattern 5: Binary Search (Standard + On Answer Space)

**Trigger:** "sorted array", "find minimum X such that condition holds"

```java
// Standard binary search
public int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2; // avoid overflow
        if (arr[mid] == target)      return mid;
        else if (arr[mid] < target)  lo = mid + 1;
        else                         hi = mid - 1;
    }
    return -1;
}

// Binary search on answer (most powerful variant)
// "Find minimum X such that canAchieve(X) is true"
public int binarySearchOnAnswer(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canAchieve(mid)) hi = mid;  // mid might be answer, narrow right
        else                 lo = mid + 1;
    }
    return lo;
}
// canAchieve() must be monotonic: false,false,...,true,true,true
```

**Examples:** Koko Eating Bananas (#875), Find Min in Rotated Array (#153), Search in Rotated (#33)

---

### Pattern 6: BFS (Level-Order / Multi-Source)

**Trigger:** "shortest path", "minimum steps", "levels", "closest"

```java
// Standard BFS
public int bfs(int[][] grid, int startR, int startC) {
    int rows = grid.length, cols = grid[0].length;
    Queue<int[]> queue = new LinkedList<>();
    boolean[][] visited = new boolean[rows][cols];
    int steps = 0;
    int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};

    queue.offer(new int[]{startR, startC});
    visited[startR][startC] = true;

    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            int[] curr = queue.poll();
            // Process curr...

            for (int[] d : dirs) {
                int nr = curr[0] + d[0], nc = curr[1] + d[1];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols
                        && !visited[nr][nc] && grid[nr][nc] != 0) {
                    visited[nr][nc] = true;
                    queue.offer(new int[]{nr, nc});
                }
            }
        }
        steps++;
    }
    return steps;
}

// Multi-source BFS: add ALL sources to queue before starting
// e.g., Rotting Oranges (#994) — all rotten oranges are sources
```

---

### Pattern 7: DFS + Backtracking

**Trigger:** "all possible combinations/permutations/subsets", "generate all..."

```java
// Backtracking template
public void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
    // Base case (optional — or add current at every step for subsets)
    result.add(new ArrayList<>(current));  // for subsets: add here

    for (int i = start; i < nums.length; i++) {
        // Skip duplicates: if (i > start && nums[i] == nums[i-1]) continue;

        current.add(nums[i]);           // choose
        backtrack(nums, i + 1, current, result); // explore (i+1 for subsets, i for combos with reuse)
        current.remove(current.size()-1); // unchoose
    }
}
```

**Examples:** Subsets (#78), Combination Sum (#39), Permutations (#46), Palindrome Partitioning (#131)

---

### Pattern 8: Monotonic Stack

**Trigger:** "next greater element", "largest rectangle", "daily temperatures"

```java
// Next Greater Element to the right
public int[] nextGreater(int[] arr) {
    int n = arr.length;
    int[] result = new int[n];
    Arrays.fill(result, -1);
    Deque<Integer> stack = new ArrayDeque<>(); // stores indices

    for (int i = 0; i < n; i++) {
        // Pop while current element is greater than stack top
        while (!stack.isEmpty() && arr[i] > arr[stack.peek()]) {
            int idx = stack.pop();
            result[idx] = arr[i];
        }
        stack.push(i);
    }
    return result;
}
```

**Examples:** Daily Temperatures (#739), Largest Rectangle in Histogram (#84), Trapping Rain Water (#42)

---

### Pattern 9: Prefix Sum

**Trigger:** "subarray sum equals k", "range sum queries"

```java
// Subarray sum equals k
public int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> prefixCount = new HashMap<>();
    prefixCount.put(0, 1); // empty prefix
    int sum = 0, count = 0;

    for (int num : nums) {
        sum += num;
        // If (sum - k) exists as a prefix sum, those subarrays sum to k
        count += prefixCount.getOrDefault(sum - k, 0);
        prefixCount.merge(sum, 1, Integer::sum);
    }
    return count;
}
```

---

### Pattern 10: Top-K Elements (Heap)

**Trigger:** "K largest", "K most frequent", "K closest"

```java
// K largest elements
public int[] kLargest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>(); // min at top

    for (int num : nums) {
        minHeap.offer(num);
        if (minHeap.size() > k) minHeap.poll(); // remove smallest
    }
    // Heap contains k largest
    return minHeap.stream().mapToInt(Integer::intValue).toArray();
}

// K most frequent
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int n : nums) freq.merge(n, 1, Integer::sum);

    PriorityQueue<Map.Entry<Integer,Integer>> heap =
        new PriorityQueue<>(Comparator.comparingInt(Map.Entry::getValue));

    for (var entry : freq.entrySet()) {
        heap.offer(entry);
        if (heap.size() > k) heap.poll();
    }
    return heap.stream().mapToInt(Map.Entry::getKey).toArray();
}
```

---

### Pattern 11: Union-Find (Disjoint Set)

**Trigger:** "connected components", "number of islands with merges", "redundant connection"

```java
public class UnionFind {
    private final int[] parent, rank;

    public UnionFind(int n) {
        parent = new int[n];
        rank   = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    public int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]); // path compression
        return parent[x];
    }

    public boolean union(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return false; // already connected

        // Union by rank
        if (rank[px] < rank[py]) parent[px] = py;
        else if (rank[px] > rank[py]) parent[py] = px;
        else { parent[py] = px; rank[px]++; }
        return true;
    }

    public boolean connected(int x, int y) { return find(x) == find(y); }
}
```

---

### Pattern 12: Trie

**Trigger:** "prefix search", "word search", "autocomplete"

```java
public class Trie {
    private static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd;
    }

    private final TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return node.isEnd;
    }

    public boolean startsWith(String prefix) {
        TrieNode node = root;
        for (char c : prefix.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return false;
            node = node.children[idx];
        }
        return true;
    }
}
```

---

## SECTION 3: Dynamic Programming — Complete Guide

### DP Recognition Framework

**Is it DP?** Ask these 4 questions:
1. Can the problem be broken into **overlapping subproblems**?
2. Does the optimal solution contain **optimal solutions to subproblems** (optimal substructure)?
3. Is the answer to a subproblem **reusable** (computed once, used many times)?
4. Is there a **recurrence relation** you can write?

If yes to all → DP.

**Top-down vs Bottom-up:**
- Top-down (memoization): easier to write, follows natural recursion. Start here.
- Bottom-up (tabulation): better space (often), avoids stack overflow for deep recursion.

**The 4 questions before writing any DP:**
1. What is the "state"? (What uniquely describes a subproblem?)
2. What is the recurrence relation? (How does state[i] depend on previous states?)
3. What is the base case?
4. What is the final answer? (Which state?)

---

### DP Problem 1: 0/1 Knapsack

**State:** `dp[i][w]` = max value using first i items with capacity w
**Recurrence:** `dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])` if `wt[i] <= w`

```java
// Bottom-up — O(n*W) time, O(n*W) space
public int knapsack(int[] weights, int[] values, int capacity) {
    int n = weights.length;
    int[][] dp = new int[n + 1][capacity + 1];

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= capacity; w++) {
            dp[i][w] = dp[i-1][w]; // don't take item i
            if (weights[i-1] <= w) {
                dp[i][w] = Math.max(dp[i][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]); // take item i
            }
        }
    }
    return dp[n][capacity];
}

// Space-optimized: O(W) — traverse w backwards
public int knapsackOptimized(int[] weights, int[] values, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weights.length; i++) {
        for (int w = capacity; w >= weights[i]; w--) { // backwards!
            dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
        }
    }
    return dp[capacity];
}
```

**Variant — Subset Sum:** Can we pick numbers that sum to target?
```java
// dp[j] = true if subset with sum j is achievable
boolean[] dp = new boolean[target + 1];
dp[0] = true;
for (int num : nums)
    for (int j = target; j >= num; j--)
        dp[j] = dp[j] || dp[j - num];
return dp[target];
```

---

### DP Problem 2: Coin Change (Minimum Coins — #322)

**State:** `dp[amount]` = min coins to make amount
**Recurrence:** `dp[i] = min over all coins c: dp[i-c] + 1`

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1); // "infinity"
    dp[0] = 0;

    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
// Time: O(amount * coins), Space: O(amount)
```

---

### DP Problem 3: Longest Common Subsequence (#1143)

**State:** `dp[i][j]` = LCS of s1[0..i-1] and s2[0..j-1]
**Recurrence:**
- if `s1[i-1] == s2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

```java
public int longestCommonSubsequence(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i-1) == s2.charAt(j-1))
                dp[i][j] = dp[i-1][j-1] + 1;
            else
                dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);
        }
    }
    return dp[m][n];
}
```

---

### DP Problem 4: House Robber (#198)

```java
public int rob(int[] nums) {
    if (nums.length == 1) return nums[0];
    int prev2 = 0, prev1 = 0;
    for (int num : nums) {
        int curr = Math.max(prev1, prev2 + num);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

// House Robber II (circular — #213): run rob() on [0..n-2] and [1..n-1], take max
public int robCircular(int[] nums) {
    if (nums.length == 1) return nums[0];
    return Math.max(
        rob(Arrays.copyOfRange(nums, 0, nums.length - 1)),
        rob(Arrays.copyOfRange(nums, 1, nums.length))
    );
}
```

---

### DP Problem 5: Longest Increasing Subsequence (#300)

```java
// O(n²) — straightforward
public int lis(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    int max = 1;

    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
        }
        max = Math.max(max, dp[i]);
    }
    return max;
}

// O(n log n) — patience sorting (tails array)
public int lisOptimal(int[] nums) {
    List<Integer> tails = new ArrayList<>();
    for (int num : nums) {
        int lo = 0, hi = tails.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (tails.get(mid) < num) lo = mid + 1;
            else hi = mid;
        }
        if (lo == tails.size()) tails.add(num);
        else tails.set(lo, num);
    }
    return tails.size();
}
```

---

### DP Problem 6: Jump Game II (#45)

```java
// Greedy DP — O(n)
public int jump(int[] nums) {
    int jumps = 0, currentEnd = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i == currentEnd) {
            jumps++;
            currentEnd = farthest;
        }
    }
    return jumps;
}
```

---

### DP Problem 7: Word Break (#139)

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;

    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j] && dict.contains(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[n];
}
```

---

### DP Problem 8: Longest Palindromic Substring (#5)

```java
// Expand around center — O(n²) time, O(1) space
public String longestPalindrome(String s) {
    int start = 0, maxLen = 1;

    for (int i = 0; i < s.length(); i++) {
        // Odd length palindromes
        int len1 = expand(s, i, i);
        // Even length palindromes
        int len2 = expand(s, i, i + 1);
        int len = Math.max(len1, len2);

        if (len > maxLen) {
            maxLen = len;
            start = i - (len - 1) / 2;
        }
    }
    return s.substring(start, start + maxLen);
}

private int expand(String s, int l, int r) {
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
        l--; r++;
    }
    return r - l - 1;
}
```

---

## SECTION 4: Graph Algorithms in Java

### BFS — Shortest Path (Unweighted)

```java
public int shortestPath(int[][] graph, int src, int dst) {
    // graph[i] = list of neighbors of node i
    Queue<Integer> queue = new LinkedList<>();
    Set<Integer> visited = new HashSet<>();
    queue.offer(src);
    visited.add(src);
    int dist = 0;

    while (!queue.isEmpty()) {
        int size = queue.size();
        for (int i = 0; i < size; i++) {
            int node = queue.poll();
            if (node == dst) return dist;
            for (int neighbor : graph[node]) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    queue.offer(neighbor);
                }
            }
        }
        dist++;
    }
    return -1;
}
```

### Topological Sort (Kahn's Algorithm — BFS)

```java
public int[] topoSort(int n, int[][] edges) {
    int[] inDegree = new int[n];
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

    for (int[] e : edges) {
        adj.get(e[0]).add(e[1]);
        inDegree[e[1]]++;
    }

    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++) if (inDegree[i] == 0) queue.offer(i);

    int[] order = new int[n];
    int idx = 0;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        order[idx++] = node;
        for (int neighbor : adj.get(node)) {
            if (--inDegree[neighbor] == 0) queue.offer(neighbor);
        }
    }
    return idx == n ? order : new int[]{}; // empty = cycle detected
}
```

### Dijkstra's Algorithm

```java
public int[] dijkstra(int n, int[][] edges, int src) {
    List<int[]>[] adj = new List[n]; // adj[u] = {v, weight}
    for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
    for (int[] e : edges) {
        adj[e[0]].add(new int[]{e[1], e[2]});
        adj[e[1]].add(new int[]{e[0], e[2]});
    }

    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
    pq.offer(new int[]{src, 0});

    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int node = curr[0], d = curr[1];
        if (d > dist[node]) continue; // stale entry

        for (int[] neighbor : adj[node]) {
            int next = neighbor[0], weight = neighbor[1];
            if (dist[node] + weight < dist[next]) {
                dist[next] = dist[node] + weight;
                pq.offer(new int[]{next, dist[next]});
            }
        }
    }
    return dist;
}
```

---

## SECTION 5: Interview Strategy

### The 35-Minute Problem-Solving Framework

```
0–2 min   → Read carefully. Clarify ambiguities. Ask about edge cases (empty array? negative numbers? duplicates?)
2–5 min   → Think out loud: "My first instinct is brute force — O(n²). Let me see if I can do better."
5–10 min  → Identify the pattern. Tell the interviewer: "This looks like a sliding window problem."
10–25 min → Code the solution. Talk through each step.
25–30 min → Test with 1–2 examples by hand. Include an edge case.
30–35 min → Analyze time and space complexity. Mention possible optimizations.
```

### When to Say "Brute Force First"
- Always mention brute force first — shows you understand the problem
- Then say: "I think we can optimize this because [reason]"
- Code the optimal solution, not brute force (unless you're stuck)

### Handling "I'm Stuck"
1. Restate the problem in your own words
2. Try a small example by hand
3. Think about simpler/smaller version of the problem
4. Ask: "Should I think about this differently? I've been trying X approach..."
5. Look for a pattern: sorted? → binary search. Tree? → DFS. Shortest path? → BFS.

### Explaining Complexity
```
"This runs in O(n log n) because we sort first (n log n) and then do a single pass (n)."
"Space complexity is O(n) for the HashMap that stores at most n entries."
"We can optimize space to O(1) if we modify the input array in-place, but that's destructive."
```

---

## SECTION 6: Top 30 Must-Do Problems (Java)

### P0 — From Real Apple/Oracle/Amazon/DoorDash Interviews

| # | Problem | LC # | Pattern | Difficulty | Why |
|---|---|---|---|---|---|
| 1 | LRU Cache | 146 | DLL + HashMap | Medium | Apple Screening — must know cold |
| 2 | Trapping Rain Water | 42 | Two Pointers / Mono Stack | Hard | Amazon Round 4 |
| 3 | Task Scheduler | 621 | Greedy + Heap | Medium | Oracle Round 2 |
| 4 | First Missing Positive | 41 | Cyclic Sort | Hard | Amazon Round 3 |
| 5 | Evaluate Reverse Polish Notation | 150 | Stack | Medium | Amazon Round 3 |
| 6 | Container With Most Water | 11 | Two Pointers | Medium | Oracle Screening |

### P1 — Core Patterns (Do These Next)

| # | Problem | LC # | Pattern | Difficulty |
|---|---|---|---|---|
| 7 | Two Sum | 1 | HashMap | Easy |
| 8 | Longest Substring Without Repeating | 3 | Sliding Window | Medium |
| 9 | Merge Intervals | 56 | Sort + Sweep | Medium |
| 10 | Binary Search | 704 | Binary Search | Easy |
| 11 | Number of Islands | 200 | BFS/DFS | Medium |
| 12 | Clone Graph | 133 | BFS + HashMap | Medium |
| 13 | Course Schedule | 207 | Topological Sort | Medium |
| 14 | Word Search | 79 | DFS + Backtracking | Medium |
| 15 | Combination Sum | 39 | Backtracking | Medium |
| 16 | Top K Frequent Elements | 347 | Heap | Medium |
| 17 | Find Median from Data Stream | 295 | Two Heaps | Hard |
| 18 | Merge K Sorted Lists | 23 | K-way Merge + Heap | Hard |

### P2 — DP Focus

| # | Problem | LC # | Pattern | Difficulty |
|---|---|---|---|---|
| 19 | Climbing Stairs | 70 | DP | Easy |
| 20 | Coin Change | 322 | DP Unbounded Knapsack | Medium |
| 21 | Longest Increasing Subsequence | 300 | DP | Medium |
| 22 | Word Break | 139 | DP | Medium |
| 23 | Unique Paths | 62 | DP Grid | Medium |
| 24 | Jump Game II | 45 | Greedy DP | Medium |
| 25 | House Robber | 198 | DP | Medium |

### P3 — Advanced

| # | Problem | LC # | Pattern | Difficulty |
|---|---|---|---|---|
| 26 | Serialize/Deserialize Binary Tree | 297 | BFS + Design | Hard |
| 27 | Word Search II | 212 | Trie + Backtracking | Hard |
| 28 | Largest Rectangle in Histogram | 84 | Monotonic Stack | Hard |
| 29 | Minimum Window Substring | 76 | Sliding Window | Hard |
| 30 | Design Twitter (simplified) | 355 | Heap + HashMap | Medium |
