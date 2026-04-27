# Improvement notes — my submissions vs interview-standard patterns

Each entry: what I submitted, what's wrong, and the cleaner version to use going forward.
Grouped by algorithm family so related fixes reinforce each other.

---

## Tree recursion

### [#98 Validate BST](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0098-validate-binary-search-tree/solution.py)

**What I did:** post-order tuple return `(isValid, min, max)`. Four separate branch cases for (no left, no right, both, neither). ~35 lines.

**What's wrong:** post-order is the wrong direction for constraint propagation. The constraint (valid range) flows *down* from parent to child, not up. Returning min/max up just to recheck them is unnecessary work.

**Standard:** pre-order bounds — pass `(lo, hi)` down, check on entry, recurse with tightened bounds.

```python
def isValidBST(root):
    def go(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return go(node.left, lo, node.val) and go(node.right, node.val, hi)
    return go(root, float('-inf'), float('inf'))
```

---

### [#543 Diameter of Binary Tree](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0543-diameter-of-binary-tree/solution.py)

**What I did:** tuple return `(diameter, height)`. `None` node returns `(-1, -1)` — a confusing sentinel that makes `height + 1` correct only by coincidence.

**What's wrong:** diameter is a side-effect computed at each node, not something that flows up cleanly. Packaging it in the return value adds mental overhead. The `-1` sentinel for an empty node's height is non-obvious.

**Standard:** track max diameter in a nonlocal variable, return only height. Height of `None` = 0.

```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node: return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)
        return max(l, r) + 1
    height(root)
    return best
```

---

### [#230 Kth Smallest Element in a BST](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0230-kth-smallest-element-in-a-bst/solution.py)

**What I did:** `self.curr` counter + `-1` as sentinel return value for "not found yet." Early-exits by checking `leftResult != -1`.

**What's wrong:** `-1` as sentinel breaks if the tree contains `-1`. Using instance variables for traversal state is fragile. The "is left result valid?" check is extra logic that obscures the in-order structure.

**Standard:** `nonlocal` counter + `None` sentinel. Clean in-order with early stop.

```python
def kthSmallest(root, k):
    count = 0
    result = None
    def inorder(node):
        nonlocal count, result
        if not node or result is not None: return
        inorder(node.left)
        count += 1
        if count == k:
            result = node.val
            return
        inorder(node.right)
    inorder(root)
    return result
```

---

### [#257 Binary Tree Paths](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0257-binary-tree-paths/solution.py)

**What I did:** post-order — recurse into children first, prepend `root.val->` to each path returned. Creates a new list of strings at every level.

**What's wrong:** harder to read (paths are assembled backwards), creates O(n²) intermediate strings in the worst case as each path gets prepended at every ancestor.

**Standard:** pre-order — pass the current path string down, append to results at leaves.

```python
def binaryTreePaths(root):
    res = []
    def dfs(node, path):
        if not node: return
        path += str(node.val)
        if not node.left and not node.right:
            res.append(path)
        else:
            dfs(node.left, path + '->')
            dfs(node.right, path + '->')
    dfs(root, '')
    return res
```

---

## DFS (Depth-First Search) cycle detection / topological sort

### [#207 Course Schedule](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0207-course-schedule/solution.py)

**What I did:** `visiting` is a `list`. `nextCourse in visiting` is O(n) per check.

**What's wrong:** O(n) membership test inside an O(V+E) traversal makes the worst case O(V²) instead of O(V+E).

**Fix:** use a `set` for `visiting`. Keep the list only if you need ordered path reconstruction; otherwise swap it entirely.

```python
visiting = set()

# in walk:
if next_course in visiting:   # O(1) now
    ...
visiting.add(course)
...
visiting.remove(course)
```

---

### [#210 Course Schedule II](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0210-course-schedule-ii/solution.py)

**What I did:** DFS that appends to a stack, then a *second* loop re-validates the order. The `walk` function marks nodes visited immediately on entry — meaning it has no gray/black distinction and cannot detect cycles. The second loop is attempting to compensate for this.

**What's wrong:** the DFS doesn't detect cycles (no `visiting` set), making the first pass incorrect. The second validation loop is O(E) extra work and is the wrong place to catch cycles. The whole thing is fragile.

**Standard:** use Kahn's algorithm (BFS (Breadth-First Search) with indegrees). It gives topological order directly and cycle detection falls out for free.

```python
def findOrder(numCourses, prerequisites):
    edges = defaultdict(list)
    indegree = [0] * numCourses
    for c, req in prerequisites:
        edges[req].append(c)
        indegree[c] += 1

    queue = deque(i for i in range(numCourses) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in edges[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == numCourses else []
```

---

## Graph / DSU (Disjoint Set Union)

### [#684 Redundant Connection](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0684-redundant-connection/solution.py)

**What I did:** recursive `find` with path compression.

**What's wrong:** recursive `find` risks hitting Python's recursion limit on a pathological chain of n=1000 nodes before any union-by-rank kicks in. Iterative is safer and equally clear.

**Standard:** iterative `find` with two-step path compression (`parent[x] = parent[parent[x]]`).

```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]   # path compression
        x = parent[x]
    return x
```

---

## Grid DFS (Depth-First Search)

### [#200 Number of Islands](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0200-number-of-islands/solution.py)

**What I did:** separate `self.visited` 2D array (same size as grid). Also: `self.COL = len(grid)` is actually the row count — naming is reversed.

**What's wrong:** the visited array doubles memory. The reversed naming (`COL`/`ROW`) is a latent bug waiting to confuse future changes.

**Standard:** modify the grid in place — flip `"1"` to `"0"` on visit. Eliminates the visited array entirely. Acceptable in interviews unless the problem says not to mutate input.

```python
def numIslands(grid):
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'   # mark visited in-place
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

---

## Linked list

### [#141 Linked List Cycle](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0141-linked-list-cycle/solution.py)

**What I did:** advance `p2` once, then check `if not p2`, then advance again. The comparison is after both advances, inside the loop.

**What's wrong:** the guard `if not p2: return False` mid-loop is easy to misplace and obscures the loop invariant. The standard template's `while fast and fast.next` guard makes the termination condition explicit and is harder to get wrong under pressure.

**Standard:** guard both `fast` and `fast.next` in the while condition, check equality after advancing.

```python
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

---

## Grid DFS (Depth-First Search) — separate visited array (recurring)

Already noted for #200. The full scan found the same pattern in five more problems.

| Problem | Note |
|---|---|
| [#695 Max Area of Island](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0695-max-area-of-island/solution.py) | `self.visited` 2D array |
| [#1380 Number of Closed Islands](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/1380-number-of-closed-islands/solution.py) | `self.visited` 2D array |
| [#2035 Count Sub-Islands](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/2035-count-sub-islands/solution.py) | `self.visited` 2D array |
| [#463 Island Perimeter](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0463-island-perimeter/solution.py) | `self.visited` 2D array |
| [#854 Making a Large Island](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0854-making-a-large-island/solution.py) | Uses both: mutates grid to label islands AND maintains `self.visited` |

Fix is the same as #200: flip `grid[r][c] = 0` on visit. Exception: #079 Word Search correctly keeps a separate visited array because it backtracks (restores state after each DFS branch) — in-place would break there.

---

## Instance variables used as implicit function parameters

Across many solutions, state that belongs inside one function call gets stored on `self` to avoid passing it through recursion. This creates implicit coupling between the entry method and the recursive helper, and makes the code hard to follow in isolation.

Seen in: #086, #695, #1380, #2035, #463, #854 (`self.grid`, `self.visited`, `self.ROW`, `self.COL`), and #200 (`self.COL`/`self.ROW` names reversed — `COL = len(grid)` is actually rows).

**Standard:** use a nested function (closure). It sees the outer variables without them being threaded through `self`.

```python
def numIslands(self, grid):
    rows, cols = len(grid), len(grid[0])
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
    ...
```

No `self.grid`, no `self.visited`, no naming confusion.

---

## Linked list — recursive when iterative is standard

Recursion on a linked list of length n uses O(n) stack space. Several problems use recursive helpers with multi-value tuple returns where the canonical approach is iterative two-pointer or dummy-head.

| Problem | What I did | Standard |
|---|---|---|
| [#019 Remove Nth from End](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0019-remove-nth-node-from-end-of-list/solution.py) | Returns `(head, countdown)` from recursion | Two pointers with n-step gap |
| [#083 Remove Duplicates](https://github.com/SansWord/leetcode_submissions/blob/main/submissions/0083-remove-duplicates-from-sorted-list/solution.py) | Recursive with `pre` param | Single iterative pass |
| [#206 Reverse Linked List](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0206-reverse-linked-list/solution.py) | Returns `(new_head, new_tail)` from recursion | Iterative `prev, curr` swap |
| [#234 Palindrome Linked List](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0234-palindrome-linked-list/solution.py) | Recursion passes `head` as front pointer through call stack | Find midpoint → reverse second half → compare |
| [#086 Partition List](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0086-partition-list/solution.py) | `self.xNode`, `self.preX`, `self.head` as instance state | Two dummy heads, partition iteratively, reconnect |

---

## BFS (Breadth-First Search) — `list.pop(0)` instead of `deque`

`list.pop(0)` is O(n) — it shifts every element left. In BFS this makes the whole traversal O(n²).

| Problem | Issue |
|---|---|
| [#637 Average of Levels in Binary Tree](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0637-average-of-levels-in-binary-tree/solution.py) | `queue.pop(0)` in BFS loop |
| [#341 Flatten Nested List Iterator](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0341-flatten-nested-list-iterator/solution.py) | `nestedList.pop(0)` in both `pop()` and `tidyList()` |

Fix: `from collections import deque`, use `queue.popleft()`.

---

## Two-phase "generate structure → assign values" instead of direct recursion

Two problems use the same unusual pattern: first generate all possible tree *shapes* (cached), then do a second pass that assigns values by consuming a deque. The `@cache` stores `TreeNode` objects by reference — the second pass mutates those cached objects, which can corrupt the cache for subsequent calls.

| Problem | Issue | Standard |
|---|---|---|
| [#095 Unique Binary Search Trees II](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0095-unique-binary-search-trees-ii/solution.py) | `generateTreeStructures(n)` + `copyTree()` second pass | `generate(lo, hi)` — for each root value r, left from `generate(lo, r-1)`, right from `generate(r+1, hi)` |
| [#241 Different Ways to Add Parentheses](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0241-different-ways-to-add-parentheses/solution.py) | `generateBinaryTrees(n)` + `evalTree()` consuming a deque | Divide-and-conquer on the expression directly — no tree structure needed |

---

## Heap used where plain BFS suffices

[#417 Pacific Atlantic Water Flow](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0417-pacific-atlantic-water-flow/solution.py) uses `heapq` as the BFS frontier, popping cells in height order. The reachability condition (`neighbor_height >= current_height`) is correct regardless of traversal order, so the heap adds O(log n) per operation for no benefit.

Compare: [#794 Swim in Rising Water](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0794-swim-in-rising-water/solution.py) and [#407 Trapping Rain Water II](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0407-trapping-rain-water-ii/solution.py) correctly use a heap because the answer depends on processing cells in strict height order.

**Standard for #417:** plain BFS from both ocean borders inward. O(n) instead of O(n log n).

---

## O(n²) graph construction where O(n·L) pattern dictionary suffices

[#127 Word Ladder](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0127-word-ladder/solution.py) builds a full adjacency matrix by comparing every pair of words — O(n² × L). This TLEs on large inputs.

**Standard:** for each word, generate all single-char wildcard patterns (`h*t`, `ho*`, etc.) and group words by pattern — O(n × L). During BFS, look up neighbors via pattern match instead of pairwise comparison.

---

## Debug `print()` statements left in submitted code

Found in four submissions. Workflow issue: code was debugged interactively but prints weren't removed before submit.

- [#893 All Nodes Distance K in Binary Tree](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0893-all-nodes-distance-k-in-binary-tree/solution.py) — 15+ print calls
- [#685 Redundant Connection II](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0685-redundant-connection-ii/solution.py) — `print(candidateEdges)`
- [#448 Find All Numbers Disappeared in an Array](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0448-find-all-numbers-disappeared-in-an-array/solution.py) — `print(nums[i], nums[idx])`
- [#457 Circular Array Loop](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0457-circular-array-loop/solution.py) — `print(target)`

---

## Summary table

| Problem | Issue | Fix |
|---|---|---|
| [#98 Validate BST](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0098-validate-binary-search-tree/solution.py) | Post-order tuple return, 4 branch cases | Pre-order bounds propagation |
| [#543 Diameter](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0543-diameter-of-binary-tree/solution.py) | Tuple return, `-1` sentinel for empty node | `nonlocal` max, return height only |
| [#230 Kth Smallest BST](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0230-kth-smallest-element-in-a-bst/solution.py) | `-1` sentinel breaks for negative values | `None` sentinel + `nonlocal` counter |
| [#257 Binary Tree Paths](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0257-binary-tree-paths/solution.py) | Post-order bottom-up path building | Pre-order top-down path passing |
| [#530 Min Absolute Diff BST](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0530-minimum-absolute-difference-in-bst/solution.py) | Guard-before-each-branch instead of top-level None check | `if not root: return` at top, clean in-order |
| [#893 All Nodes Distance K](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0893-all-nodes-distance-k-in-binary-tree/solution.py) | Tracking `k` as return value through ancestors + debug prints | Parent map + plain BFS from target |
| [#095 Unique BSTs II](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0095-unique-binary-search-trees-ii/solution.py) | Two-phase generate+assign, cached mutable objects | Direct `generate(lo, hi)` recursion |
| [#241 Different Ways to Add Parentheses](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0241-different-ways-to-add-parentheses/solution.py) | Two-phase generate+assign | Divide-and-conquer on expression |
| [#207 Course Schedule](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0207-course-schedule/solution.py) | `visiting` list → O(n) `in` check | `visiting` set → O(1) |
| [#210 Course Schedule II](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0210-course-schedule-ii/solution.py) | No cycle detection, second validation loop | Kahn's algorithm |
| [#684 Redundant Connection](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0684-redundant-connection/solution.py) | Recursive `find` → recursion limit risk | Iterative `find` |
| [#200 Number of Islands](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0200-number-of-islands/solution.py) | Separate visited array + reversed naming | In-place grid mutation |
| [#695 Max Area of Island](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0695-max-area-of-island/solution.py) | Separate visited array | In-place grid mutation |
| [#1380 Number of Closed Islands](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/1380-number-of-closed-islands/solution.py) | Separate visited array | In-place grid mutation |
| [#2035 Count Sub-Islands](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/2035-count-sub-islands/solution.py) | Separate visited array | In-place grid mutation |
| [#141 Linked List Cycle](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0141-linked-list-cycle/solution.py) | Manual mid-loop guard on fast pointer | Standard `while fast and fast.next` |
| [#019 Remove Nth from End](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0019-remove-nth-node-from-end-of-list/solution.py) | Recursive `(head, countdown)` return | Two pointers with n-step gap |
| [#206 Reverse Linked List](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0206-reverse-linked-list/solution.py) | Recursive `(new_head, new_tail)` return | Iterative `prev, curr` swap |
| [#234 Palindrome Linked List](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0234-palindrome-linked-list/solution.py) | Recursion as front-pointer trick, O(n) stack | Find mid → reverse → compare |
| [#637 Average of Levels](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0637-average-of-levels-in-binary-tree/solution.py) | `list.pop(0)` in BFS → O(n²) | `deque.popleft()` |
| [#417 Pacific Atlantic Water Flow](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0417-pacific-atlantic-water-flow/solution.py) | Heap where plain BFS is correct | Plain BFS from borders |
| [#127 Word Ladder](https://github.com/Sansword/leetcode_submissions/blob/main/submissions/0127-word-ladder/solution.py) | O(n²×L) all-pairs graph build | O(n×L) wildcard pattern dict |
