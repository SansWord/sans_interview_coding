# Refresh Knowledge — patterns keyed to my own past solutions

Read this before the core list. Each section points to a real solution I already wrote, distills the invariant, and gives a clean template. My style is good — this doc is about sharpening what I already do, not teaching new tricks.

Language: Python. Imports assumed: `from collections import defaultdict, deque, Counter`, `import heapq`.

---

## 1. Binary search — the invariant style

Yes, **this is a great pattern**. It's my strongest rust-resistant tool because it eliminates off-by-one arguments. I already use it — see [`0033-search-in-rotated-sorted-array/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0033-search-in-rotated-sorted-array/solution.py) and [`0034-find-first-and-last-position-of-element-in-sorted-array/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0034-find-first-and-last-position-of-element-in-sorted-array/solution.py).

**The invariant I use:**
- `lo = 0`, `hi = len(nums)` (exclusive upper bound)
- Loop while `lo < hi`
- On "move right" → `lo = mid + 1`
- On "move left" → `hi = mid` (NOT `mid - 1`)
- `mid = (lo + hi) // 2`

**Why the invariant works:** the answer range is always `[lo, hi)` (half-open). The loop terminates when `lo == hi`, which gives the insertion point. No off-by-one worry because the two moves are asymmetric by construction.

**Template: leftmost match (first index where `pred(x)` is true, assuming pred flips false→true once):**

```python
lo, hi = 0, len(nums)
while lo < hi:
    mid = (lo + hi) // 2
    if pred(nums[mid]):
        hi = mid           # mid is a candidate; keep it
    else:
        lo = mid + 1       # mid fails; discard it
return lo                  # lo == hi == leftmost true, or len(nums) if none
```

**Rightmost match:** search for leftmost of `not pred` and return `lo - 1`, or mirror the template.

**Mental model — predicate-based partition (universal):**

Every binary search splits the search space `[lo, hi)` into two regions, separated by `l` (== `r` at exit):

```
[lo, l)   →  left region  (predicate fails)
[r, hi)   →  right region (predicate holds)
```

The branches assign `mid` to one of the regions:
- `r = mid` → mid joins the **right** region (predicate is true for mid)
- `l = mid + 1` → mid joins the **left** region (predicate is false for mid)

When `l == r` at termination, that meeting point is the **first index of the right region** — i.e., the first index where the predicate holds (or `hi` if the right region is empty).

**Why `l == r` at exit (and `l` never overshoots `r`):**
- `mid = (l + r) // 2` always satisfies `l <= mid < r`
- `r = mid` strictly decreases r (since `mid < r`)
- `l = mid + 1` increases l but caps at r (since `mid + 1 <= r`)
- Each iteration shrinks the gap by ≥1 → eventually `l == r` exactly

**Overflow note (`mid = l + (r - l) // 2`):**
The "safe" form `l + (r - l) // 2` is **not needed in Python** — Python ints are arbitrary precision, so `(l + r) // 2` never overflows. But it's a famous interview gotcha (Joshua Bloch's 2006 post) for fixed-width integer languages: in Java/C++, `int l + int r` near `2^31` wraps to a negative value, breaking the search. If asked "what if l + r overflows?", explain you'd use `l + (r - l) // 2` in those languages, but Python doesn't have the issue. Worth knowing for language-portability discussions or coding interviews in Java/C++.

**Designing any binary search in 3 steps:**
1. Define a **monotonic predicate** `P(i)` — false for some prefix, true for the suffix.
2. Pick the search space `[lo, hi)`.
3. Apply the universal template:
   ```python
   while l < r:
       mid = (l + r) // 2
       if P(mid):
           r = mid
       else:
           l = mid + 1
   ```

At exit, `l` = first index where P holds, or `hi` if none. Always check `l < hi` before reading `nums[l]`.

**Examples of P for different problems:**

| Problem | Predicate `P(i)` |
|---------|---------------|
| Lower-bound (first ≥ target) | `nums[i] >= target` |
| Upper-bound (first > target) | `nums[i] > target` |
| Find target exactly | `nums[i] >= target`, then verify `nums[l] == target` |
| Last occurrence of target ([#34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)) | upper-bound, return `l - 1` |
| Min in rotated ([#153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)) | `nums[i] <= nums[-1]` |
| Koko bananas ([#875](https://leetcode.com/problems/koko-eating-bananas/)) | `can_finish(speed=i, h)` (binary search on answer) |
| Split array max sum | `can_split(max_sum=i, k)` |

**When the universal template doesn't apply:**
- **Rotated arrays ([#33](https://leetcode.com/problems/search-in-rotated-sorted-array/))** — predicate isn't monotonic globally; needs the sorted-half hack
- **Need both index and content of the boundary** — handle bounds check separately after the search

For ~90% of binary search problems, this single template + a well-chosen predicate is the entire solution. Stop reasoning about `<` vs `<=` or `mid` vs `mid+1` — those are encoded in the template once.

**Rotated array (like [#33](https://leetcode.com/problems/search-in-rotated-sorted-array/)):** at each step, one half `[lo, mid]` or `[mid, hi)` is sorted. Check which, then check if the target lies within that sorted half. If yes, recurse into it; else the other half. My [#33](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0033-search-in-rotated-sorted-array/solution.py) solution does this cleanly.

**First/last of target (like [#34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)):** two separate binary searches with different predicates (`val >= target` for first, `val > target` for first-past-last). Cleaner than tracking match during the search.

---

## 2. Two pointers — sorted array

Reference: [`0015-3sum/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0015-3sum/solution.py). My twoSum helper is the canonical form.

**Template:**
```python
nums.sort()
l, r = 0, len(nums) - 1
while l < r:
    s = nums[l] + nums[r]
    if s == target:
        # record, then advance past duplicates
        val = nums[l]
        while l < r and nums[l] == val:
            l += 1
    elif s < target:
        l += 1
    else:
        r -= 1
```

**3Sum trick:** outer loop fixes `nums[i]`, inner is two-sum for `-nums[i]` in `nums[i+1:]`. Skip duplicates on **both** the outer pick and the inner matches. I have this right — just keep the skip-dup pattern in muscle memory.

---

## 3. Sliding window — shrinkable

Reference: [`0003-longest-substring-without-repeating-characters/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0003-longest-substring-without-repeating-characters/solution.py). Very clean.

**Template:**
```python
l = 0
state = <set | Counter | window sum>
best = 0
for r in range(len(s)):
    # expand: include s[r]
    while <window is invalid>:
        # shrink from left
        l += 1
    # record: window [l, r] is now valid
    best = max(best, r - l + 1)
```

**Key invariant:** after the `while`, `[l, r]` is always valid. Record after the while, not inside it.

**Variants:**
- "at most K distinct" → `while len(counter) > K`
- "exactly K distinct" → `atMost(K) - atMost(K-1)`
- Fixed window → skip the while; just drop `s[r-K]` each step

---

## 4. Hashmap — grouping / counting

**Group by canonical key (e.g. [#49 Group Anagrams](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0049-group-anagrams/solution.py)):**
```python
groups = defaultdict(list)
for s in strs:
    key = ''.join(sorted(s))   # or tuple of 26 counts
    groups[key].append(s)
return list(groups.values())
```

**Frequency → heap ([my #347](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0347-top-k-frequent-elements/solution.py)):** `defaultdict(int)` count, then push `(-freq, val)` into heap for top-K. Negation trick for max-heap. Clean.

**Complement lookup ([#1 Two Sum](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0001-two-sum/solution.py)):**
```python
seen = {}   # val -> index
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

---

## 5. Stack — valid parentheses / pair matching

Reference: [`0020-valid-parentheses/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0020-valid-parentheses/solution.py).

**Template:**
```python
stack = []
pairs = {')': '(', ']': '[', '}': '{'}
for c in s:
    if c in pairs.values():
        stack.append(c)
    else:
        if not stack or stack.pop() != pairs[c]:
            return False
return not stack
```

**Generalization:** monotonic stack (daily temperatures, histogram) — keep stack invariant (e.g. strictly increasing indices). When violated, pop and settle.

---

## 6. Intervals — sort + sweep

Reference: [`0056-merge-intervals/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0056-merge-intervals/solution.py). My code is tight.

**Template:**
```python
intervals.sort()            # by start
res = [intervals[0]]
for start, end in intervals[1:]:
    if res[-1][1] < start:
        res.append([start, end])
    else:
        res[-1][1] = max(res[-1][1], end)
return res
```

**Gotcha I avoided:** `preEnd < start` (strict), not `<=`, depends on problem. For `[1,4]` and `[4,5]`: if touching counts as overlap → `<`; if not → `<=`. Know the problem's rule.

---

## 7. BFS (Breadth-First Search) — grid & tree

I don't have a clean queue-BFS reference in my submissions (I used DFS for [#200](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0200-number-of-islands/solution.py)). Learn this for [#102](https://leetcode.com/problems/binary-tree-level-order-traversal/) Level Order Traversal.

**Tree level order (for [#102 Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)):**
```python
if not root: return []
q = deque([root])
res = []
while q:
    level = []
    for _ in range(len(q)):    # <-- snapshot level size
        node = q.popleft()
        level.append(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    res.append(level)
return res
```

**The snapshot (`for _ in range(len(q))`) is the key.** It separates levels. Without it, you're doing flat BFS.

**Flat vs level-order:** same O(V+E) either way. The real skill is picking the right one:
- Need depth, distance, or grouping by generation → level-order
- Just need reachability or "visit everything" (flood fill, connected components) → flat BFS is simpler, less to implement and explain

**On grids:** the same distinction applies. The template below carries `d` (distance) in the tuple — that's level-order. Drop `d` for flat. Rotting Oranges needs `d`: the answer is the max distance reached across all rotten cells, which is the number of minutes elapsed.

**Grid BFS (multi-source, e.g. [#994 Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) / shortest path):**
```python
q = deque([(r, c, 0)])       # (row, col, dist)
seen = {(r, c)}
while q:
    r, c, d = q.popleft()
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and (nr,nc) not in seen and grid[nr][nc] != blocker:
            seen.add((nr,nc))
            q.append((nr, nc, d+1))
```

---

## 8. DFS (Depth-First Search) — grid

Reference: [`0200-number-of-islands/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0200-number-of-islands/solution.py). My style: recursive DFS with `visited[y][x]` and early return on invalid/visited/water.

**One cleanup for next time:** I can modify the grid in place (flip `"1"` to `"0"`) to avoid the visited array — common in interviews because it shows you think about space. But the visited array is clearer and safer. Either is fine.

---

## 9. DFS — cycle detection (topological sort)

Reference: [`0207-course-schedule/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0207-course-schedule/solution.py). Three-color idea implicit in my `visited` + `visiting` combo.

**Three-color DFS:**
- white (unseen) = not in any array
- gray (on current path) = in `visiting`
- black (fully explored, no cycle through it) = `visited[node] = True`

A back-edge to a gray node = cycle.

**Alternative: [Kahn's algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm) (BFS with indegrees).** Push nodes with indegree 0, pop, decrement neighbors' indegrees. If all nodes processed → no cycle. Sometimes cleaner. Have both in the toolkit for [#210](https://leetcode.com/problems/course-schedule-ii/).

```python
# Time: O(V+E) — each node and edge visited once
# Space: O(V+E) — adjacency list + indegree array + queue
def canFinish(numCourses, prerequisites):
    edges = defaultdict(list)
    indegree = [0] * numCourses
    for c, req in prerequisites:
        edges[req].append(c)
        indegree[c] += 1

    queue = deque(i for i in range(numCourses) if indegree[i] == 0)
    processed = 0
    while queue:
        node = queue.popleft()
        processed += 1
        for neighbor in edges[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return processed == numCourses  # False → cycle exists
```

To also return topological order, collect `node` into a list on each pop — the list is a valid ordering.

**Kahn's vs DFS — when to pick which:**
- Default to Kahn's for cycle detection: iterative (no recursion limit), cleaner code, gives topological order for free.
- Pick DFS when the problem is inherently path-based: reachability, connected components, cycle *path* reconstruction.

**Returning the actual cycle (path reconstruction):**

`visiting` already IS the current path. When `next_course in visiting`, slice from where `next_course` first appears:

```python
# Time: O(V+E) — each node/edge visited once; visiting.index() is O(V) but amortized fine
# Space: O(V+E) — adjacency list + visited array + recursion stack (depth ≤ V)
# change return type: None = no cycle, list = cycle found
def walk(self, course, visiting):
    visiting.append(course)
    for next_course in self.edges[course]:
        if next_course in visiting:
            start = visiting.index(next_course)
            return visiting[start:]          # the cycle
        if not self.visited[next_course]:
            result = self.walk(next_course, visiting)
            if result is not None:
                return result                # propagate unchanged
    visiting.pop()
    self.visited[course] = True
    return None
```

Once the cycle is captured at the detection point, every caller just passes it up — no one adds to it.

**Filtering by cycle length (e.g. "only cycles with 3+ nodes"):**

Both algorithms detect cycles of any length — 1 (self-loop), 2 (A→B→A), or longer. To filter:

- **DFS** — easy. The length is `len(visiting[start:])`. Add one check:
  ```python
  if next_course in visiting:
      start = visiting.index(next_course)
      cycle = visiting[start:]
      if len(cycle) >= 3:      # ignore self-loops and 2-cycles
          return cycle
  ```
- **Kahn's** — can't filter. It destroys path information as it runs. All you get is "cycle exists" — you can't know the length without additional work.

Rule of thumb: any time the problem asks you to *characterize* the cycle (length, members, minimum size), Kahn's hits a wall. Use DFS.

**Stretch: finding all unique cycles**

This is significantly harder. The DFS above finds the first cycle and exits. Three problems when extending it:
1. A single DFS doesn't find all cycles — need to restart from every node.
2. The same cycle gets discovered multiple times ([0,1,2], [1,2,0], [2,0,1] are the same).
3. Stopping early on `visited` nodes would skip cycles reachable through them.

**The canonical dedup trick:** only report a cycle when the starting node is the *minimum* node in the cycle. This ensures each cycle is found exactly once, from its lowest-numbered node. Skip any neighbor with index ≤ start.

```python
def find_all_cycles(numCourses, prerequisites):
    edges = defaultdict(list)
    for c, req in prerequisites:
        edges[req].append(c)
    all_cycles = []

    def dfs(start, current, path, in_path):
        for neighbor in edges[current]:
            if neighbor == start and len(path) > 1:
                all_cycles.append(list(path))   # found cycle back to start
            elif neighbor > start and neighbor not in in_path:
                # only visit nodes > start: each cycle reported once (from min node)
                in_path.add(neighbor)
                path.append(neighbor)
                dfs(start, neighbor, path, in_path)
                path.pop()
                in_path.remove(neighbor)

    for start in range(numCourses):
        dfs(start, start, [start], {start})
    return all_cycles
```

The `neighbor > start` constraint is the dedup mechanism. A cycle [0,1,2] is only discoverable starting from 0; from 1 or 2, neighbor 0 gets skipped.

The production algorithm for all elementary cycles is **[Johnson's algorithm](https://www.cs.tufts.edu/comp/150GA/homeworks/hw1/Johnson%2075.pdf)** (1975) — O((V+E)(C+1)) where C = number of cycles. It uses a more sophisticated blocked-node mechanism to avoid redundant searches. Unlikely in an interview, but good to name if the interviewer pushes.

---

## 10. Tree recursion — with return invariant

Reference: [`0098-validate-binary-search-tree/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0098-validate-binary-search-tree/solution.py). My tuple-return (isValid, min, max) works but has too many branches. Cleaner version:

**Validate BST via bounds (passed down, not returned up):**
```python
def isValidBST(root):
    def go(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return go(node.left, lo, node.val) and go(node.right, node.val, hi)
    return go(root, float('-inf'), float('inf'))
```

**General pattern — post-order with returned state:** each recursive call returns what the parent needs (e.g. max depth, subtree sum, is-balanced + height). Compute child results first, combine at the parent.

**Pre-order (bounds down):** pass constraints into the call (like the BST bounds).

**Know when to use which:** if the parent needs info from children → post-order. If children need info from the parent (ancestors) → pre-order with parameters.

---

## 11. Heap — top-K / k-way

Reference: [`0347-top-k-frequent-elements/solution.py`](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0347-top-k-frequent-elements/solution.py). My negation trick is correct.

**Top-K largest (size-K min-heap, O(n log k)):**
```python
h = []
for x in nums:
    heapq.heappush(h, x)
    if len(h) > k:
        heapq.heappop(h)
return h   # k largest, unordered
```

**Top-K frequent:** same pattern, push `(freq, val)` tuples.

**K-way merge (for [#23](https://leetcode.com/problems/merge-k-sorted-lists/)):** push head of each list into heap; pop smallest, push its `.next`.

---

## 12. DP — 1D (for [#322 Coin Change](https://leetcode.com/problems/coin-change/))

DP is the least-represented pattern in my recent submissions — worth extra attention.

**Template (bottom-up):**
```python
dp = [BASE] * (n + 1)
dp[0] = <base case>
for i in range(1, n + 1):
    for choice in choices:
        if valid(i, choice):
            dp[i] = combine(dp[i], dp[i - cost(choice)] + gain(choice))
return dp[n]
```

**Coin Change specifically:**
```python
def coinChange(coins, amount):
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1
```

**Three things to internalize:**
1. `dp[i]` means "minimum coins to make amount i"
2. Transition: `dp[i] = min over c of (dp[i-c] + 1)`
3. Unreachable sentinel: `amount + 1` works because you can never need more coins than `amount` (since smallest coin is ≥ 1).

**[House Robber](https://leetcode.com/problems/house-robber/) (stretch #198)** is the easier 1D DP warm-up: `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.

---

## 13. Design — LRU (Least Recently Used) Cache (for [#146 LRU Cache](https://leetcode.com/problems/lru-cache/))

Never built this. The interview-canonical structure:

**Doubly-linked list + hashmap:**
- DLL (Doubly-Linked List) ordered by recency. Head = most recent, tail = least recent.
- Hashmap `key -> node` for O(1) access.
- `get(key)`: hashmap lookup → unlink node → push to head → return val
- `put(key, val)`: if present, unlink; insert at head; if over capacity, remove tail, drop from hashmap.

**Python shortcut:** `collections.OrderedDict` already does this. Use `move_to_end(key)` on access, `popitem(last=False)` on evict. In a real interview, implement DLL by hand — shows you understand it. In the AI round, either is fine.

**DLL node sketch:**
```python
class Node:
    __slots__ = ('key', 'val', 'prev', 'next')
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None
```

Use two sentinel nodes (head, tail). Never have to check `None` when unlinking.

---

## 14. General Python interview idioms

- `Counter(nums)` over hand-rolled `defaultdict(int)` when you just need counts
- `zip(nums, nums[1:])` for adjacent pairs
- `for i, x in enumerate(nums):` over `range(len(nums))`
- `''.join(sorted(s))` as canonical anagram key (O(k log k)); or tuple of 26 counts (O(k))
- `float('inf')` and `float('-inf')` for bounds
- `@cache` from functools for top-down memoization (turn recursion into DP for free)
- List comprehension over map/filter when readability matters (always, in an interview)

---

## 15. Patterns to learn (not in core list)

Ordered by interview frequency × ROI. Do these **after** the core list, or dip in if a core problem recalls the pattern. Each has a 1-line recognition cue, a minimal template, and 2–3 practice problems (easier first).

---

### 15a. Linked list manipulation — **highest priority gap**

Linked list isn't in my recent submissions and deserves a deliberate refresh. It's near-certain in interviews, and pointer bookkeeping is where most slips happen.

**Recognize:** input is `ListNode`, question about reversal, middle, cycle, merge, or reorder.

**Two tools cover 80%:**

**1. Dummy head for building/editing lists:**
```python
dummy = ListNode(0)
tail = dummy
# ... build by tail.next = x; tail = tail.next
return dummy.next
```

**2. Fast/slow pointers:**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
# slow is now at middle (or cycle meeting point)
```

**Reverse in place:**
```python
prev, curr = None, head
while curr:
    curr.next, prev, curr = prev, curr, curr.next
return prev
```

**Practice:**
- [#206 Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) — canonical
- [#21 Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) — dummy head
- [#141 Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) — fast/slow
- [#143 Reorder List](https://leetcode.com/problems/reorder-list/) — combines all three (harder)

---

### 15b. Backtracking — subsets / permutations / combinations

[#212 Word Search II](https://leetcode.com/problems/word-search-ii/) uses this, but no simpler standalone rep. Learn the skeleton first on clean problems.

**Recognize:** "generate all", "find all paths", "partition", constraint satisfaction.

**Template:**
```python
def backtrack(path, choices):
    if is_goal(path):
        res.append(path[:])    # copy!
        return
    for i, c in enumerate(choices):
        if prune(c): continue
        path.append(c)
        backtrack(path, next_choices(choices, i))
        path.pop()              # undo
```

**The three moves:** choose → explore → un-choose. The `path.pop()` at the end is the whole pattern.

**Practice:**
- [#78 Subsets](https://leetcode.com/problems/subsets/) — simplest; include-or-not
- [#46 Permutations](https://leetcode.com/problems/permutations/) — track used set
- [#39 Combination Sum](https://leetcode.com/problems/combination-sum/) — index to avoid reuse
- [#79 Word Search](https://leetcode.com/problems/word-search/) — grid backtracking, warm-up for #212

---

### 15c. Prefix sum

**Recognize:** range sum queries, "subarray summing to K", "equal halves".

**Template:**
```python
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)
# sum of nums[i..j] = prefix[j+1] - prefix[i]
```

**Prefix + hashmap combo (the real power):** for "count subarrays with sum K", store `prefix_sum -> count` and look for `prefix[j] - K` as you go. Same idea extends to "divisible by K" (use `prefix % K`).

**Practice:**
- [#303 Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) — pure template
- [#560 Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) — prefix + hashmap (the key problem)
- [#525 Contiguous Array](https://leetcode.com/problems/contiguous-array/) — remap 0→−1, then subarray-sum-zero

---

### 15d. Greedy

**Recognize:** "minimum steps", "can you reach", "schedule", and the obvious local choice keeps working. Distinct from DP: greedy never revisits a decision; DP explores all branches.

**Key habit:** prove (or at least argue) why the greedy choice is safe. In interview, state the exchange argument: "if we didn't take this choice, we could always swap to it without making the answer worse."

**Practice:**
- [#55 Jump Game](https://leetcode.com/problems/jump-game/) — track farthest reachable
- [#45 Jump Game II](https://leetcode.com/problems/jump-game-ii/) — BFS-flavored greedy
- [#134 Gas Station](https://leetcode.com/problems/gas-station/) — classic argument: if you can't reach from A, no station between A and failure point works either
- [#435 Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) — sort by end

---

### 15e. Union-Find (DSU — Disjoint Set Union)

**Recognize:** "count connected components", "are X and Y connected", "redundant edge", problems where merging equivalence classes is the shape.

**Template (path compression + union by size, ~10 lines):**
```python
# Time: O(α(V)) per operation (practically O(1)); O(V+E) overall
# Space: O(V)
parent = list(range(n))
size = [1] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False           # already same component
    if size[ra] < size[rb]: ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True
```

**Cycle detection in undirected graphs — DSU is the natural fit.**

In an undirected graph you can't use Kahn's (designed for directed) or the three-color DFS (gray/black states don't map cleanly because every edge is bidirectional). DSU sidesteps both problems entirely:

> If you try to union two nodes that are already in the same component, the new edge creates a cycle.

```python
def has_cycle(n, edges):
    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        if not union(a, b):   # same root → cycle
            return True
    return False
```

Intuition: DSU tracks equivalence classes ("which nodes are already connected?"). The moment an edge connects two nodes that already share a root, you've closed a loop — that's a cycle.

**Why not DFS for undirected cycles?**

DFS can work on undirected graphs, but you need to track the parent to avoid treating the edge you just came from as a back-edge:

```python
def has_cycle_dfs(n, edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor == parent:
                continue              # ignore the edge we came from
            if neighbor in visited:
                return True           # back-edge → cycle
            if dfs(neighbor, node):
                return True
        return False

    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    return False
```

This works but is more fiddly than DSU. Prefer DSU when the question is purely "does a cycle exist?" in an undirected graph.

**Directed vs undirected — which tool:**

| Graph type | Cycle detection tool |
|---|---|
| Directed | Kahn's (yes/no) or DFS (path) |
| Undirected | DSU (yes/no) or DFS with parent-skip |

**When to pick DSU over DFS/BFS:** when components change over time (edges added incrementally), or when you need component representatives for many pairs. Static connectivity → DFS/BFS is usually simpler.

**Practice:**
- [#547 Number of Provinces](https://leetcode.com/problems/number-of-provinces/) — count components
- [#684 Redundant Connection](https://leetcode.com/problems/redundant-connection/) — first edge that closes a cycle (undirected, DSU is the clean solution)
- [#200 Number of Islands](https://leetcode.com/problems/number-of-islands/) — re-do it with Union-Find (I already solved it via DFS; the DSU version is a great contrast rep)
- [#261 Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) — undirected cycle + connectivity check in one pass

---

### 15f. 2D DP (grids / pairs of strings)

1D DP is in the core via [#322](https://leetcode.com/problems/coin-change/). 2D is the next step and shows up often.

**Recognize:** grid path counts, two-string alignment (edit distance, LCS (Longest Common Subsequence)), "best split point".

**Template:**
```python
# dp[i][j] = answer for state (i, j)
dp = [[BASE] * (n + 1) for _ in range(m + 1)]
# fill base row/col
for i in range(1, m + 1):
    for j in range(1, n + 1):
        dp[i][j] = combine(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
return dp[m][n]
```

**Space-optimize:** if `dp[i][j]` only depends on row `i-1`, collapse to two rows (or one if careful with order).

**Practice:**
- [#62 Unique Paths](https://leetcode.com/problems/unique-paths/) — simplest 2D DP
- [#64 Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) — weighted grid
- [#1143 Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) — string pair DP, canonical
- [#72 Edit Distance](https://leetcode.com/problems/edit-distance/) — string pair DP, harder (and extremely common)

---

### 15g. Trie

I touch Trie via [#212 Word Search II](https://leetcode.com/problems/word-search-ii/) (in Day 3 set). Learn the standalone version first — #212 combines Trie + backtracking and is overwhelming without prior Trie reps.

**Template:**
```python
class Trie:
    def __init__(self):
        self.root = {}
    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node['$'] = True    # end marker
    def search(self, word):
        node = self._walk(word)
        return bool(node and node.get('$'))
    def startsWith(self, prefix):
        return self._walk(prefix) is not None
    def _walk(self, s):
        node = self.root
        for c in s:
            if c not in node: return None
            node = node[c]
        return node
```

**Practice:**
- [#208 Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) — canonical
- [#1268 Search Suggestions System](https://leetcode.com/problems/search-suggestions-system/) — prefix walk + collect
- Then [#212 Word Search II](https://leetcode.com/problems/word-search-ii/) becomes tractable

---

### 15h. Bit manipulation

Lower priority; shows up occasionally. The XOR tricks are worth knowing in 10 minutes.

**Tricks to know:**
- `a ^ a == 0`, `a ^ 0 == a`, XOR is commutative/associative
- "find the one that appears once (others twice)" → XOR everything
- `x & (x - 1)` clears the lowest set bit → count set bits in a loop
- `x & -x` isolates the lowest set bit
- Python ints are arbitrary-precision; mask with `& 0xFFFFFFFF` to simulate 32-bit

**Practice:**
- [#136 Single Number](https://leetcode.com/problems/single-number/) — pure XOR
- [#191 Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) — `x & (x-1)` loop
- [#268 Missing Number](https://leetcode.com/problems/missing-number/) — XOR or sum

---

## 16. What to say out loud, every problem

1. Restate input/output in 1 sentence
2. Give brute force + complexity, say "but we can do better"
3. Name the pattern ("sliding window", "topo sort", "1D DP")
4. State the invariant / transition in 1 sentence before coding
5. Code
6. Trace through one example
7. Name edge cases (empty, single, duplicates, all-same, adversarial)
