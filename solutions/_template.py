"""
#<num> <Problem Name>
https://leetcode.com/problems/<slug>/

Pattern: <hashmap | sliding window | two pointers | ...>
Time limit: <30 min>   Actual: <__ min>
Date: YYYY-MM-DD

---
Restate (1 sentence):
    Given ..., return ...

Approach:
    <invariant / transition in 1 sentence>

Complexity:
    Time:  O(...)
    Space: O(...)

Edge cases considered:
    - empty input
    - single element
    - duplicates
    - <adversarial: input that catches the tricky branch — e.g. Two Sum with [3,3] target=6, should return [0,1] not [0,0]>
"""

from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        # TODO
        pass


# ---- inline tests ----
if __name__ == "__main__":
    s = Solution()

    # happy path
    assert s.solve([1, 2, 3]) == 0, "happy path"

    # empty
    assert s.solve([]) == 0, "empty"

    # single element
    assert s.solve([5]) == 0, "single"

    # duplicates
    assert s.solve([2, 2, 2]) == 0, "duplicates"

    # adversarial
    assert s.solve([-1, 0, 1]) == 0, "adversarial"

    print("ok")
