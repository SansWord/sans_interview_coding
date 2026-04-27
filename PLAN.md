# Interview Coding Prep

Structured 2.5-day interview prep, pairing a pattern-refresh doc keyed to my own past solutions with a driven-by-me AI pair-programming loop.

Two rounds:
1. **Solo coding** — no AI
2. **Follow-up** — Claude Code + Zed allowed

Language: Python.

---

## Gap assessment (2026-04-26)

### Pattern readiness

| Area | Status | Note |
|---|---|---|
| Arrays / hashmap / two pointers | Ready | Rust-off only |
| Binary search | Ready | |
| Stack / intervals | Ready | |
| Graph / topo sort | Needs work | #210 is broken — no back-edge detection; re-do with Kahn's |
| Tree recursion | Needs work | Post-order by default even when pre-order is right; fix #98 first |
| Linked list | Needs work | Consistently recursive when iterative is standard; burns O(n) stack |
| BFS queue | Gap | #102 is `[new]` and not done — foundational for level-order |
| DP | Thinnest | Only one new rep (#322); no warmup problem done yet |
| Design (AI round) | Partial | #297 solid; #146 LRU not done |

### Highest-ROI problems before the interview

Do these in order — each one closes a specific pattern gap:

1. **[#98 Validate BST](https://leetcode.com/problems/validate-binary-search-tree/)** — re-solve with pre-order bounds-down (not post-order tuple return). Burns in the direction rule for tree recursion.
2. **[#206 Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) + [#019 Remove Nth from End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)** — iteratively only. Burns in the linked list template.
3. **[#198 House Robber](https://leetcode.com/problems/house-robber/) → [#322 Coin Change](https://leetcode.com/problems/coin-change/)** — do the easier warmup first, then the core rep. Minimum DP coverage.
4. **[#102 Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)** — foundational BFS, currently `[new]` and not done.
5. **[#210 Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)** — re-do with Kahn's. Current submission doesn't detect cycles correctly.

Full pattern details and standard implementations: [`improvement.md`](improvement.md).

---

## 2.5-Day Plan

### Day 1 — Warm-up + diagnostic (half day)
- [ ] 2 Easy (5 min each, pure rust-off)
- [ ] 3 Mediums on hashmap / sliding window / two pointers, 30 min time-box
- [ ] Note which patterns felt slowest

### Day 2 — Pattern drills (full day, solo-round focus)
- [ ] 6 Mediums across the core list
- [ ] Redo any peeked/struggled ones from scratch, same day

### Day 3 — AI round rehearsal (full day)
- [ ] Morning: rehearse the AI-round setup flow end-to-end on a throwaway problem (template-dir copy, plugin-disable verification, opening line)
- [ ] Mid-day: 2 mock follow-up problems, narrate out loud
- [ ] Evening: 2 more Mediums on weak patterns from Day 2

---

## Core list — solo-round focus

Before starting, **read `refresh_knowledge.md`**. It has pattern templates keyed to my own past solutions.

Legend: `[re]` = already solved in `leetcode_submissions`, re-solve from scratch without peeking. `[new]` = never solved, first pass.

Format: `[ ] #<num> <name> — pattern — actual time — notes`

### Arrays / hashmap / two pointers
- [ ] `[re]` [#1 Two Sum](https://leetcode.com/problems/two-sum/) — hashmap — __ min — warm-up
- [ ] `[re]` [#49 Group Anagrams](https://leetcode.com/problems/group-anagrams/) — hashmap —
- [ ] `[re]` [#238 Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) — prefix/suffix —
- [ ] `[re]` [#15 3Sum](https://leetcode.com/problems/3sum/) — two pointers + sort —
- [ ] `[re]` [#3 Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) — sliding window —

### Binary search
- [ ] `[re]` [#33 Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) —
- [ ] `[re]` [#34 Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) —

### Stack / intervals
- [ ] `[re]` [#20 Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) — warm-up —
- [ ] `[re]` [#56 Merge Intervals](https://leetcode.com/problems/merge-intervals/) —

### Heap / graph / tree
- [ ] `[re]` [#347 Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) — heap —
- [ ] `[re]` [#200 Number of Islands](https://leetcode.com/problems/number-of-islands/) — BFS (Breadth-First Search)/DFS (Depth-First Search) grid —
- [ ] `[re]` [#207 Course Schedule](https://leetcode.com/problems/course-schedule/) — topo sort —
- [ ] `[new]` [#102 Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) — BFS queue — **do this**, foundational
- [ ] `[re]` [#98 Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) —

### DP (Dynamic Programming)
- [ ] `[new]` [#322 Coin Change](https://leetcode.com/problems/coin-change/) — 1D DP — **do this**, one DP rep

---

## Day 3 — AI rehearsal only (skip in solo round)

Good design + iterate problems. Use these to practice driving Claude.

- [ ] `[new]` [#146 LRU Cache](https://leetcode.com/problems/lru-cache/) — design + doubly-linked list + hashmap
- [ ] `[re]` [#297 Serialize/Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) — design + DFS string encoding
- [ ] `[new]` [#212 Word Search II](https://leetcode.com/problems/word-search-ii/) — trie + backtracking (harder; use only if #146 and #297 went well)

---

## Stretch list — after the core (do later if time permits)

Ordered for after the interview; not required. Grouped by same patterns so each one deepens a rep you already have.

### Arrays / hashmap / two pointers
- [ ] [#121 Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) — one-pass min/max
- [ ] [#11 Container With Most Water](https://leetcode.com/problems/container-with-most-water/) — two pointers
- [ ] [#424 Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) — sliding window
- [ ] [#76 Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) — sliding window (harder)

### Binary search
- [ ] [#153 Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) — pair with #33
- [ ] [#875 Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) — binary search on answer

### Stack / monotonic
- [ ] [#739 Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) — monotonic stack
- [ ] [#84 Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) — monotonic stack (harder)

### Graph / tree / heap
- [ ] [#994 Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — multi-source BFS (pairs with #200)
- [ ] [#210 Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) — topo sort output (pairs with #207)
- [ ] [#543 Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/) — post-order
- [ ] [#124 Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) — post-order (harder)
- [ ] [#23 Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) — heap

### DP
- [ ] [#198 House Robber](https://leetcode.com/problems/house-robber/) — 1D DP warm-up (easier than #322)
- [ ] [#300 Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) — 1D DP + patience sort
- [ ] [#139 Word Break](https://leetcode.com/problems/word-break/) — 1D DP + set lookup

---

## Session log

Append as I go. Each entry: date, problems, how it felt, where I stalled.

### 2026-04-27
- #206 Reverse Linked List — 5 min, clean. Set up `solutions/util/test_util.py` with `ll`, `assert_ll` helpers.

### 2026-04-24
- _not yet_

---

## AI round — prompt

The prompt for the live AI-assisted round is [`CLAUDE.pair_programming.md`](CLAUDE.pair_programming.md) — portable (no language or structure assumptions), enforces a commit-only-when-I-approve workflow, and structures each request as spec → plan → TDD → verify with paired `NNN-<slug>.spec.md` / `NNN-<slug>.plan.md` files. Day 3 rehearses the full setup flow on a throwaway problem.

## Workflow reminders (live round)

- Narrate what I'm doing with Claude out loud
- Read every line Claude writes; if I can't explain a choice, reject it
- Push back at least once per problem (ask for alternative or challenge a decision)
- Type at least one edge case myself, don't use only Claude's tests
- Keep Zed split view ready; terminal with `claude` running before the round starts
