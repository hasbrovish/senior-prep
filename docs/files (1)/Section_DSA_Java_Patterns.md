# DSA Patterns in Java — Interview Ready

## Pattern 1: Two Pointers / Sliding Window

### Template: Variable-size Sliding Window
```java
int left = 0, maxLen = 0;
Map<Character, Integer> freq = new HashMap<>();
for (int right = 0; right < s.length(); right++) {
    freq.merge(s.charAt(right), 1, Integer::sum);
    while (/* window invalid */) {
        char leftChar = s.charAt(left);
        freq.merge(leftChar, -1, Integer::sum);
        if (freq.get(leftChar) == 0) freq.remove(leftChar);
        left++;
    }
    maxLen = Math.max(maxLen, right - left + 1);
}
```
**Problems:** Longest Substring Without Repeating, Minimum Window Substring, Max Consecutive Ones III, Fruit Into Baskets.

### Template: Two Pointer (sorted array)
```java
int lo = 0, hi = arr.length - 1;
while (lo < hi) {
    int sum = arr[lo] + arr[hi];
    if (sum == target) { /* found */ lo++; hi--; }
    else if (sum < target) lo++;
    else hi--;
}
```
**Problems:** Two Sum II, 3Sum, Container With Most Water, Trapping Rain Water.

---

## Pattern 2: Binary Search

### Template: Search on Answer
```java
int lo = minPossible, hi = maxPossible;
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (condition(mid)) hi = mid;
    else lo = mid + 1;
}
return lo;
```
**Problems:** Koko Eating Bananas, Split Array Largest Sum, Aggressive Cows, Capacity To Ship Packages.

### Must-know variations
- Search in Rotated Array: compare mid with endpoints to find sorted half
- Find Peak: compare mid with mid+1
- Median of Two Sorted Arrays: binary search on partition point

---

## Pattern 3: BFS / DFS

### BFS Template (shortest path, unweighted)
```java
Queue<int[]> q = new LinkedList<>();
boolean[][] vis = new boolean[m][n];
q.offer(new int[]{sr, sc, 0});
vis[sr][sc] = true;
int[][] dirs = {{0,1},{0,-1},{1,0},{-1,0}};
while (!q.isEmpty()) {
    int[] cur = q.poll();
    if (cur[0] == tr && cur[1] == tc) return cur[2];
    for (int[] d : dirs) {
        int nr = cur[0]+d[0], nc = cur[1]+d[1];
        if (nr>=0 && nr<m && nc>=0 && nc<n && !vis[nr][nc] && grid[nr][nc]!='#') {
            vis[nr][nc] = true;
            q.offer(new int[]{nr, nc, cur[2]+1});
        }
    }
}
```
**Problems:** Number of Islands, Rotten Oranges, Word Ladder, Shortest Path in Binary Matrix.

### Topological Sort (Kahn's BFS)
```java
int[] indegree = new int[n];
for (int[] e : edges) indegree[e[1]]++;
Queue<Integer> q = new LinkedList<>();
for (int i = 0; i < n; i++) if (indegree[i] == 0) q.offer(i);
List<Integer> order = new ArrayList<>();
while (!q.isEmpty()) {
    int node = q.poll();
    order.add(node);
    for (int neighbor : adj.get(node)) {
        if (--indegree[neighbor] == 0) q.offer(neighbor);
    }
}
// order.size() < n → cycle exists
```
**Problems:** Course Schedule I & II, Alien Dictionary, Task Scheduler.

---

## Pattern 4: Dynamic Programming

### Framework
1. Define state: dp[i] or dp[i][j] = ?
2. Recurrence: how does current relate to smaller states?
3. Base case
4. Bottom-up iteration order
5. Space optimization (2D → 1D if only using previous row)

### Core Problems
**LCS:** `dp[i][j] = s1[i-1]==s2[j-1] ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1])`
**0/1 Knapsack:** `dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])`
**Edit Distance:** `dp[i][j] = s1[i]==s2[j] ? dp[i-1][j-1] : 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])`
**LIS:** O(n²) DP or O(n log n) with patience sorting (binary search on tails array)
**Coin Change:** `dp[i] = min(dp[i], dp[i-coin]+1)` for each coin

---

## Pattern 5: Trees

### Key technique: Recursive DFS returning info upward
```java
int maxPathSum = Integer.MIN_VALUE;
int dfs(TreeNode node) {
    if (node == null) return 0;
    int left = Math.max(0, dfs(node.left));
    int right = Math.max(0, dfs(node.right));
    maxPathSum = Math.max(maxPathSum, left + right + node.val); // path through node
    return Math.max(left, right) + node.val; // single path upward
}
```
**Problems:** Max Path Sum, Diameter, LCA, Validate BST, Serialize/Deserialize.

---

## Pattern 6: Heap / Priority Queue

### Top-K template
```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>(); // K largest → min-heap of size K
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll();
}
```

### Running Median (Two Heaps)
```java
PriorityQueue<Integer> lo = new PriorityQueue<>(Collections.reverseOrder()); // max-heap
PriorityQueue<Integer> hi = new PriorityQueue<>(); // min-heap
// Balance: lo.size() == hi.size() or lo.size() == hi.size() + 1
```
**Problems:** Merge K Sorted Lists, Kth Largest Element, Find Median from Data Stream.

---

## Pattern 7: Monotonic Stack
```java
Stack<Integer> stack = new Stack<>();
int[] result = new int[n];
Arrays.fill(result, -1);
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && nums[i] > nums[stack.peek()])
        result[stack.pop()] = nums[i];
    stack.push(i);
}
```
**Problems:** Next Greater Element, Largest Rectangle in Histogram, Daily Temperatures.

---

## Pattern 8: Union-Find
```java
int[] parent, rank;
int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
void union(int a, int b) {
    int pa = find(a), pb = find(b);
    if (pa == pb) return;
    if (rank[pa] < rank[pb]) parent[pa] = pb;
    else if (rank[pa] > rank[pb]) parent[pb] = pa;
    else { parent[pb] = pa; rank[pa]++; }
}
```
**Problems:** Number of Connected Components, Redundant Connection, Accounts Merge.

---

## Java-Specific DSA Tips
- Use `int[]` not `Integer[]` in tight loops (avoid autoboxing GC pressure)
- `ArrayDeque` > `Stack` and `LinkedList` for stack/queue (no resizing overhead)
- `PriorityQueue` is min-heap by default. Max-heap: `new PriorityQueue<>(Collections.reverseOrder())`
- `Map.merge()` and `Map.getOrDefault()` for clean frequency counting
- `Arrays.sort(arr, (a,b) -> a[0]-b[0])` for custom sorting — but beware integer overflow, use `Integer.compare()` for safety
- `StringBuilder` for string building in loops (not `+`)
- `Collections.unmodifiableList()` for returning read-only views
