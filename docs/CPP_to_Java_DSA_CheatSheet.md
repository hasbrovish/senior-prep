# C++ to Java DSA Cheat Sheet
### Complete Reference for Competitive Programming & LeetCode
### Jayanti Vishnoi | March 2026

---

# 1. C++ STL → Java Collections (Complete Mapping)

| C++ STL | Java Equivalent | Notes |
|---------|----------------|-------|
| `vector<int>` | `ArrayList<Integer>` | Dynamic array. Use `int[]` for CP (faster) |
| `array<int,N>` | `int[] arr = new int[N]` | Fixed size. PREFER for CP over ArrayList |
| `pair<int,int>` | `int[] {a, b}` | No Pair class! Use `int[2]` or `Map.Entry` |
| `map<K,V>` | `TreeMap<K,V>` | Sorted by key. O(log n) operations |
| `unordered_map<K,V>` | `HashMap<K,V>` | Unsorted. O(1) avg. USE THIS for most CP |
| `set<int>` | `TreeSet<Integer>` | Sorted. Has `ceiling()`, `floor()`, `higher()`, `lower()` |
| `unordered_set<int>` | `HashSet<Integer>` | Unsorted. O(1) add/contains/remove |
| `priority_queue` (max) | `new PriorityQueue<>(Collections.reverseOrder())` | Java PQ is MIN heap by default! |
| `priority_queue` (min) | `new PriorityQueue<>()` | This is the DEFAULT in Java |
| `stack<int>` | `Deque<Integer> s = new ArrayDeque<>()` | Don't use Stack class (legacy, slow) |
| `queue<int>` | `Deque<Integer> q = new ArrayDeque<>()` | `offer/poll/peek` for Queue ops |
| `deque<int>` | `ArrayDeque<Integer>` | `offerFirst/offerLast`, `pollFirst/pollLast` |
| `multiset<int>` | `TreeMap<Integer,Integer>` | Store freq as value. No direct equivalent |
| `bitset<N>` | `BitSet bs = new BitSet(N)` | `bs.set(i)`, `bs.get(i)`, `bs.and/or/xor` |

> **WARNING:** Java PriorityQueue is MIN HEAP by default (opposite of C++). For max heap: `new PriorityQueue<>(Collections.reverseOrder())`

---

# 2. Common Operations — C++ vs Java

| C++ | Java |
|-----|------|
| `sort(v.begin(), v.end())` | `Arrays.sort(arr)` or `Collections.sort(list)` |
| `sort(v.begin(), v.end(), cmp)` | `Arrays.sort(arr, (a,b) -> Integer.compare(a[0],b[0]))` |
| `reverse(v.begin(), v.end())` | `Collections.reverse(list)` |
| `lower_bound(v.begin(), v.end(), x)` | `TreeSet.ceiling(x)` or `Arrays.binarySearch(arr, x)` |
| `upper_bound(v.begin(), v.end(), x)` | `TreeSet.higher(x)` |
| `v.push_back(x)` | `list.add(x)` |
| `v.size()` | `arr.length` (array) or `list.size()` (collection) |
| `v.empty()` | `list.isEmpty()` |
| `memset(arr, 0, sizeof(arr))` | `Arrays.fill(arr, 0)` |
| `max(a, b)` | `Math.max(a, b)` |
| `min(a, b)` | `Math.min(a, b)` |
| `abs(x)` | `Math.abs(x)` |
| `pow(a, b)` | `Math.pow(a, b)` — returns double! Cast: `(int)Math.pow(a,b)` |
| `swap(a, b)` | No built-in. `int tmp=a; a=b; b=tmp;` |
| `to_string(n)` | `String.valueOf(n)` or `Integer.toString(n)` |
| `stoi(s)` | `Integer.parseInt(s)` |
| `s.substr(i, len)` | `s.substring(i, i+len)` — (start, end) NOT (start, length)! |
| `s[i]` | `s.charAt(i)` — Strings are IMMUTABLE in Java |
| `cout << x` | `System.out.println(x)` — Use StringBuilder for fast output |
| `cin >> x` | `BufferedReader + StringTokenizer` — Scanner is TOO SLOW |

---

# 3. Fast I/O Template (CRITICAL — TLE Without This)

```java
import java.io.*;
import java.util.*;

public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] arr = new int[n];
        for (int i = 0; i < n; i++)
            arr[i] = Integer.parseInt(st.nextToken());
        
        // Fast output
        StringBuilder sb = new StringBuilder();
        sb.append(result).append("\n");
        System.out.print(sb);
    }
}
```

> **WARNING:** NEVER use Scanner for competitive programming. It's 10x slower than BufferedReader. For LeetCode, I/O is handled automatically — but for CodeVita, CodeChef, Codeforces, always use BufferedReader.

---

# 4. HashMap / HashSet — Used in 70% of Problems

```java
// Frequency Count (MOST COMMON PATTERN)
Map<Integer, Integer> freq = new HashMap<>();
for (int num : arr) {
    freq.put(num, freq.getOrDefault(num, 0) + 1);
    // Shorter alternative:
    freq.merge(num, 1, Integer::sum);
}

// Check existence & get with default
map.containsKey(key);           // O(1)
map.getOrDefault(key, 0);      // Returns 0 if key missing — VERY useful

// Iterate over map
for (Map.Entry<String, Integer> e : map.entrySet()) {
    e.getKey();
    e.getValue();
}

// HashSet
Set<Integer> seen = new HashSet<>();
seen.add(5);
seen.contains(5);    // true
seen.remove(5);
```

---

# 5. PriorityQueue (Heap) — Min vs Max

```java
// MIN heap (default) — smallest at top
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// MAX heap — largest at top
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// Custom comparator (sort by 2nd element of pair)
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);

// Operations
pq.offer(x);     // add — O(log n)
pq.poll();        // remove top — O(log n)
pq.peek();        // view top — O(1)
pq.size();        // size
pq.isEmpty();     // check empty

// TOP K PATTERN: Find K largest → use MIN heap of size K
PriorityQueue<Integer> minH = new PriorityQueue<>();
for (int num : arr) {
    minH.offer(num);
    if (minH.size() > k) minH.poll();
}
// minH now has K largest elements
```

---

# 6. Stack & Queue — Always Use ArrayDeque

```java
// STACK (LIFO)
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);     // add to top
stack.pop();       // remove from top
stack.peek();      // view top
stack.isEmpty();

// QUEUE (FIFO)
Deque<Integer> queue = new ArrayDeque<>();
queue.offer(1);    // add to back
queue.poll();      // remove from front
queue.peek();      // view front
queue.isEmpty();

// DEQUE (both ends)
Deque<Integer> dq = new ArrayDeque<>();
dq.offerFirst(1);   dq.offerLast(2);
dq.pollFirst();      dq.pollLast();
dq.peekFirst();      dq.peekLast();
```

> **TIP:** NEVER use `java.util.Stack` (legacy, synchronized, slow). Always use ArrayDeque.

---

# 7. String Operations — BIGGEST Difference from C++

```java
// Strings are IMMUTABLE — every modification creates a new object
String s = "hello";
char c = s.charAt(0);              // 'h' — NOT s[0]
int len = s.length();              // NOT size()
String sub = s.substring(1, 3);    // "el" — [start, end) NOT (start, length)
boolean eq = s1.equals(s2);        // NEVER use == for string comparison

// String to char array (for sorting, manipulation)
char[] chars = s.toCharArray();
Arrays.sort(chars);
String sorted = new String(chars);

// StringBuilder — USE THIS for string manipulation in loops
StringBuilder sb = new StringBuilder("hello");
sb.append('x');           // add to end
sb.reverse();             // reverse in-place
sb.deleteCharAt(i);       // remove char at index
sb.insert(i, 'x');        // insert at index
sb.charAt(i);             // get char
sb.setCharAt(i, 'c');     // set char
String result = sb.toString();

// Conversions
int num = Integer.parseInt("123");
String str = String.valueOf(123);
String bin = Integer.toBinaryString(10);    // "1010"
String[] parts = "1,2,3".split(",");        // ["1", "2", "3"]

// Character operations
int digit = c - '0';       // char '5' → int 5
int index = c - 'a';       // char 'c' → int 2
boolean isDigit = Character.isDigit(c);
boolean isLetter = Character.isLetterOrDigit(c);
char lower = Character.toLowerCase(c);
```

> **WARNING:** String concatenation in a loop is O(n²). ALWAYS use StringBuilder. `s += 'x'` in a loop of 100K iterations = TLE.

---

# 8. Sorting with Custom Comparators

```java
// Sort primitive array
Arrays.sort(arr);                    // ascending
Arrays.sort(arr, 0, k);             // sort first k elements only

// Sort Integer array descending (NOT int[] — only works with wrapper)
Integer[] arr2 = {3, 1, 4};
Arrays.sort(arr2, Collections.reverseOrder());

// Sort 2D array by first element
int[][] intervals = {{1,3},{2,6},{8,10}};
Arrays.sort(intervals, (a, b) -> a[0] - b[0]);

// Sort by first element, then by second
Arrays.sort(arr, (a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);

// Sort list of strings by length
words.sort(Comparator.comparingInt(String::length));

// Multi-level sort with Comparator chaining
list.sort(Comparator.comparing(Person::getAge)
    .thenComparing(Person::getName)
    .reversed());
```

> **WARNING — OVERFLOW TRAP:** `(a, b) -> a - b` can overflow for large ints! Use `(a, b) -> Integer.compare(a, b)` for safety.

---

# 9. Array Operations Quick Reference

```java
// Initialize
int[] arr = new int[n];                      // zeros by default
int[] arr = {1, 2, 3, 4, 5};                // literal
int[][] grid = new int[m][n];               // 2D array (zeros)
boolean[] visited = new boolean[n];          // false by default

// Fill
Arrays.fill(arr, -1);                       // fill entire array
Arrays.fill(dp, Integer.MAX_VALUE);          // common in DP init

// Fill 2D array
for (int[] row : dp) Arrays.fill(row, -1);

// Copy
int[] copy = Arrays.copyOf(arr, arr.length);
int[] sub = Arrays.copyOfRange(arr, 1, 4);   // index 1 to 3 (end exclusive)

// Binary Search (array MUST be sorted)
int idx = Arrays.binarySearch(arr, target);
// If not found: returns -(insertion_point) - 1

// ArrayList ↔ int[] conversion
int[] arr = list.stream().mapToInt(Integer::intValue).toArray();
List<Integer> list = Arrays.stream(arr).boxed().collect(Collectors.toList());
```

---

# 10. TreeMap / TreeSet — Sorted Containers (C++ map/set equivalent)

```java
TreeSet<Integer> ts = new TreeSet<>();
ts.add(5); ts.add(3); ts.add(8);

ts.ceiling(4);     // 5  — smallest >= 4  (like lower_bound)
ts.floor(4);       // 3  — largest <= 4
ts.higher(5);      // 8  — smallest > 5   (like upper_bound)
ts.lower(5);       // 3  — largest < 5
ts.first();        // 3  — smallest element
ts.last();         // 8  — largest element
ts.subSet(3, 8);   // {3, 5} — range [3, 8)
ts.headSet(5);     // {3} — elements < 5
ts.tailSet(5);     // {5, 8} — elements >= 5

TreeMap<Integer, String> tm = new TreeMap<>();
tm.ceilingKey(x);     tm.floorKey(x);
tm.higherKey(x);      tm.lowerKey(x);
tm.firstKey();        tm.lastKey();
tm.ceilingEntry(x);   // returns Map.Entry
```

> **TIP:** `ceiling()` = C++ `lower_bound`, `higher()` = C++ `upper_bound`

---

# 11. Essential DSA Templates

## Binary Search

```java
int lo = 0, hi = n - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;      // AVOID (lo + hi) / 2 — overflow!
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
// After loop: lo = insertion point (first element >= target)
```

## BFS Template (Grid)

```java
Queue<int[]> queue = new ArrayDeque<>();
boolean[][] visited = new boolean[m][n];
queue.offer(new int[]{startRow, startCol});
visited[startRow][startCol] = true;
int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};

while (!queue.isEmpty()) {
    int[] curr = queue.poll();
    for (int[] d : dirs) {
        int nr = curr[0] + d[0], nc = curr[1] + d[1];
        if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {
            visited[nr][nc] = true;
            queue.offer(new int[]{nr, nc});
        }
    }
}
```

## DFS Template (Adjacency List)

```java
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
// Add edges: graph.get(u).add(v);

boolean[] visited = new boolean[n];

void dfs(int node) {
    visited[node] = true;
    for (int neighbor : graph.get(node)) {
        if (!visited[neighbor]) dfs(neighbor);
    }
}
```

## Sliding Window Template

```java
int left = 0, maxLen = 0;
Map<Character, Integer> window = new HashMap<>();
for (int right = 0; right < s.length(); right++) {
    char c = s.charAt(right);
    window.merge(c, 1, Integer::sum);
    
    while (/* window invalid */) {
        char leftChar = s.charAt(left);
        window.merge(leftChar, -1, Integer::sum);
        if (window.get(leftChar) == 0) window.remove(leftChar);
        left++;
    }
    maxLen = Math.max(maxLen, right - left + 1);
}
```

## Union-Find (Disjoint Set Union)

```java
int[] parent, rank;

void init(int n) {
    parent = new int[n]; rank = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
}

int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);  // path compression
    return parent[x];
}

void union(int x, int y) {
    int px = find(x), py = find(y);
    if (px == py) return;
    if (rank[px] < rank[py]) parent[px] = py;          // union by rank
    else if (rank[px] > rank[py]) parent[py] = px;
    else { parent[py] = px; rank[px]++; }
}
```

## Dijkstra's Algorithm

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]); // {node, dist}
int[] dist = new int[n];
Arrays.fill(dist, Integer.MAX_VALUE);
dist[src] = 0;
pq.offer(new int[]{src, 0});

while (!pq.isEmpty()) {
    int[] curr = pq.poll();
    int u = curr[0], d = curr[1];
    if (d > dist[u]) continue;                // skip outdated entries
    for (int[] edge : graph.get(u)) {          // edge = {neighbor, weight}
        int v = edge[0], w = edge[1];
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            pq.offer(new int[]{v, dist[v]});
        }
    }
}
```

---

# 12. DP Initialization Patterns

```java
// 1D DP — minimization
int[] dp = new int[n + 1];
Arrays.fill(dp, Integer.MAX_VALUE);
dp[0] = 0;

// 2D DP — memoization
int[][] dp = new int[m + 1][n + 1];
for (int[] row : dp) Arrays.fill(row, -1);    // -1 = unvisited

// Memoization with HashMap (sparse state space)
Map<String, Integer> memo = new HashMap<>();
String key = i + "," + j + "," + k;           // encode state as string
if (memo.containsKey(key)) return memo.get(key);

// Boolean DP (subset sum, etc.)
boolean[] dp = new boolean[target + 1];
dp[0] = true;

// LCS template
int[][] dp = new int[m + 1][n + 1];
for (int i = 1; i <= m; i++)
    for (int j = 1; j <= n; j++)
        if (s1.charAt(i-1) == s2.charAt(j-1))
            dp[i][j] = dp[i-1][j-1] + 1;
        else
            dp[i][j] = Math.max(dp[i-1][j], dp[i][j-1]);

// Knapsack template
for (int i = 1; i <= n; i++)
    for (int w = W; w >= weight[i]; w--)       // reverse for 0-1 knapsack
        dp[w] = Math.max(dp[w], dp[w - weight[i]] + value[i]);
```

---

# 13. Graph Representation

```java
// Adjacency List — UNWEIGHTED (most common)
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
graph.get(u).add(v);         // directed edge u → v
graph.get(v).add(u);         // add this too for undirected

// Adjacency List — WEIGHTED
List<List<int[]>> graph = new ArrayList<>();     // int[] = {neighbor, weight}
for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
graph.get(u).add(new int[]{v, weight});

// Adjacency Matrix (dense graphs / Floyd-Warshall)
int[][] dist = new int[n][n];
for (int[] row : dist) Arrays.fill(row, Integer.MAX_VALUE / 2);
for (int i = 0; i < n; i++) dist[i][i] = 0;

// Edge List (for Kruskal's / sorting edges)
int[][] edges = new int[m][3];     // {u, v, weight}
Arrays.sort(edges, (a, b) -> a[2] - b[2]);    // sort by weight
```

---

# 14. Math & Bit Manipulation

```java
// Constants
Integer.MAX_VALUE       // 2147483647 (2^31 - 1)
Integer.MIN_VALUE       // -2147483648 (-2^31)
Long.MAX_VALUE          // 9223372036854775807
(int) 1e9 + 7           // 1000000007 (common MOD)

// GCD & LCM
int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
long lcm(long a, long b) { return a / gcd(a, b) * b; }   // divide first to avoid overflow

// Fast Power with MOD
long power(long base, long exp, long mod) {
    long result = 1;
    base %= mod;
    while (exp > 0) {
        if ((exp & 1) == 1) result = result * base % mod;
        exp >>= 1;
        base = base * base % mod;
    }
    return result;
}

// Bit operations (same as C++)
x & 1                           // check if odd
x >> 1                          // divide by 2
x << 1                          // multiply by 2
x & (x - 1)                    // remove lowest set bit
Integer.bitCount(x)             // count set bits (popcount)
Integer.numberOfLeadingZeros(x)
Integer.highestOneBit(x)
```

---

# 15. CRITICAL Java Gotchas — These WILL Bite You

| Gotcha | Details |
|--------|---------|
| **Integer == vs equals** | `Integer a=128, b=128; a==b` is **FALSE**! Cache only covers -128 to 127. ALWAYS use `a.equals(b)` |
| **int overflow** | `int a=100000; a*a` **OVERFLOWS!** Use: `(long)a * a`. Also: `mid = lo + (hi-lo)/2` not `(lo+hi)/2` |
| **String == vs equals** | `s1==s2` checks REFERENCE. `s1.equals(s2)` checks CONTENT. ALWAYS use `.equals()` |
| **PriorityQueue = MIN heap** | Opposite of C++! For max heap: `new PriorityQueue<>(Collections.reverseOrder())` |
| **String immutability** | `s += 'x'` in a loop = O(n²). Use `StringBuilder` for any string building |
| **Array vs ArrayList** | `int[]` is faster (primitives). `ArrayList<Integer>` auto-boxes. Prefer `int[]` for CP |
| **substring(start, end)** | END is exclusive! `s.substring(1,3)` = chars at index 1,2. Different from C++ `substr(start, LENGTH)` |
| **No unsigned types** | Java has NO unsigned int/long. Use `long` for large values |
| **Division truncates to 0** | Java: `-7/2 = -3` (toward zero). Ceiling div: `(a + b - 1) / b` |
| **2D array init** | `int[][] dp = new int[m][n]` = all zeros. For -1: `for (int[] row : dp) Arrays.fill(row, -1)` |
| **Char to int** | `char c='5'; int d = c - '0';` → 5. `char c='c'; int i = c - 'a';` → 2 |
| **Modular arithmetic** | `long result = ((long)a * b) % MOD;` Negative mod fix: `((a % MOD) + MOD) % MOD` |
| **Collections.reverseOrder()** | Only works with `Integer[]`, NOT `int[]`. Primitive arrays can't use Comparator |
| **Array equality** | `arr1 == arr2` checks reference. Use `Arrays.equals(arr1, arr2)` for content |
| **List of arrays in Set** | `int[]` doesn't override equals/hashCode. Use `Arrays.hashCode()` or convert to String key |

---

# 16. Quick Reference Card

| What | Java Code |
|------|-----------|
| Array sort | `Arrays.sort(arr)` |
| Custom sort (2D) | `Arrays.sort(arr, (a,b) -> Integer.compare(a[0], b[0]))` |
| HashMap freq count | `map.merge(key, 1, Integer::sum)` |
| HashMap default value | `map.getOrDefault(key, 0)` |
| Min Heap | `new PriorityQueue<>()` |
| Max Heap | `new PriorityQueue<>(Collections.reverseOrder())` |
| Stack | `Deque<> s = new ArrayDeque<>()` → `push/pop/peek` |
| Queue | `Deque<> q = new ArrayDeque<>()` → `offer/poll/peek` |
| String char access | `s.charAt(i)` NOT `s[i]` |
| String compare | `s1.equals(s2)` NEVER use `==` |
| String building | `StringBuilder sb = new StringBuilder()` |
| Binary search mid | `mid = lo + (hi - lo) / 2` |
| Avoid int overflow | `(long) a * b` |
| Ceiling division | `(a + b - 1) / b` |
| Char to digit | `c - '0'` |
| Char to index | `c - 'a'` |
| Modular arithmetic | `((long)a * b) % MOD` |
| Negative mod fix | `((a % MOD) + MOD) % MOD` |
| 2D array fill -1 | `for (int[] row : dp) Arrays.fill(row, -1)` |
| lower_bound equivalent | `TreeSet.ceiling(x)` |
| upper_bound equivalent | `TreeSet.higher(x)` |
| Pair (no built-in) | `new int[]{a, b}` |
| Infinity for int | `Integer.MAX_VALUE / 2` (avoid overflow on addition) |
| Graph adjacency list | `List<List<Integer>> g = new ArrayList<>()` |
| Read int (fast I/O) | `Integer.parseInt(br.readLine().trim())` |
| Read line tokens | `StringTokenizer st = new StringTokenizer(br.readLine())` |

---

# 17. The "10 Problem Bridge" — Solve These First in Java

| # | LeetCode Problem | Java Concept Practiced |
|---|-----------------|----------------------|
| 1 | Two Sum (Easy) | HashMap, array iteration |
| 2 | Valid Parentheses (Easy) | Stack (ArrayDeque), charAt |
| 3 | Merge Two Sorted Lists (Easy) | ListNode, while loop, references |
| 4 | Best Time to Buy Stock (Easy) | Math.max/min, array traversal |
| 5 | Binary Tree Level Order (Medium) | Queue (BFS), ArrayList, `List<List<>>` |
| 6 | Top K Frequent Elements (Medium) | HashMap freq + PriorityQueue |
| 7 | Merge Intervals (Medium) | Arrays.sort with comparator, 2D array |
| 8 | Word Search (Medium) | 2D boolean[], DFS/backtracking, charAt |
| 9 | LRU Cache (Medium) | HashMap + DoublyLinkedList or LinkedHashMap |
| 10 | Sliding Window Maximum (Hard) | Deque (ArrayDeque), offerLast/pollFirst |

---

> **How to use this file:** Keep it open in a split screen while solving LeetCode. After 15-20 problems, you won't need it anymore. The gap between C++ CP and Java CP is just syntax — your DSA knowledge transfers directly.
