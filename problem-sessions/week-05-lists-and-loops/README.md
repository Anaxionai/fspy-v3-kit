# Week 5: One pass over a list

## The pattern in five lines

1. Walk the list once, from the first item to the last.
2. Keep a running total (the sum of the items so far) in one variable.
3. Keep a best-so-far (the best answer among the items so far) in another variable.
4. Reach for this pattern when a question asks for a total, a highest, a lowest or a first.
5. One pass takes O(n) time and O(1) extra space. Read [the Big-O page](../big-o.md) first.

## Problem A (warm-up, 10 minutes): Balls to reach the target

Match Centre records the runs from each ball while a team chases a target. You have the list of runs, in the order of the balls. Find how many balls the team needs to reach the target.

```python
def balls_to_reach(runs: list[int], target: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `balls_to_reach([1, 4, 0, 6, 2], 10)` | `4` | The totals are 1, 5, 5 and 11. The fourth ball passes 10. |
| `balls_to_reach([4, 6], 10)` | `2` | The total is exactly 10 after two balls. |
| `balls_to_reach([0, 1, 2, 0], 7)` | `-1` | The total is 3 after the last ball. |
| `balls_to_reach([], 5)` | `-1` | The team faced no balls. |

**Rules**

- `runs` has 0 to 10,000 items. Each item is a whole number from 0 to 6.
- `target` is a whole number from 1 to 100,000.
- The team reaches the target when its total is equal to or greater than `target`.
- Return `-1` when the team never reaches the target. An empty list also returns `-1`.
- Do not change the list `runs`.

## Problem B (main, 25 minutes): Biggest rise in balance

PaisaLens records your account balance at the end of each day, in paise. You want to know the biggest rise from one day to any later day. A rise counts only when the higher balance comes after the lower balance.

```python
def biggest_rise(balances: list[int]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `biggest_rise([50000, 42000, 61000, 39000, 55000])` | `19000` | The balance rises from 42000 to 61000. |
| `biggest_rise([80000, 30000, 45000, 20000])` | `15000` | The balance rises from 30000 to 45000. The 80000 comes too early to count. |
| `biggest_rise([90000, 70000, 70000, 10000])` | `0` | The balance never rises. |
| `biggest_rise([])` | `0` | The list has no days. |

**Rules**

- `balances` has 0 to 10,000 items. Each item is a whole number of paise from 0 to 1,000,000,000.
- The two days of a rise can be next to each other or far apart.
- Return `0` when the balance never rises.
- Return `0` when the list has fewer than two items.
- Do not change the list `balances`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which values must you remember as you walk the list, so that one pass is enough?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Change `biggest_rise` so that it returns the two positions of the rise, as `(low_day, high_day)`. Decide what to return when the balance never rises. Add two tests for your choice.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
