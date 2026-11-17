# Week 10: Queues and a window that slides

## The pattern in five lines

1. A queue (a line where the first item in is the first item out) in Python is `collections.deque`.
2. `append` adds at the back and `popleft` removes from the front, both in O(1) time. A list's `pop(0)` is O(n).
3. A sliding window (a run of neighbouring items that moves along the list) takes in the new item and drops the oldest.
4. Reach for a window when a question asks about recent items, such as the last 60 seconds, or the best run in a row.
5. Each item enters the window once and leaves once, so the walk is O(n), not O(n × k) for a window of k items. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Clicks in the last minute

Shortly's rate limiter (the code that blocks a link that gets too many clicks too fast) needs a count of recent clicks. You get the time of each click, in seconds, in order. For each click, count the clicks in the 60 seconds that end at that click.

```python
def clicks_in_last_minute(times: list[int]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `clicks_in_last_minute([0, 10, 59, 60, 125])` | `[1, 2, 3, 3, 1]` | At second 60, the window is seconds 1 to 60, so the click at 0 has left. |
| `clicks_in_last_minute([30, 30, 30])` | `[1, 2, 3]` | Clicks in the same second all count. |
| `clicks_in_last_minute([0, 100, 200])` | `[1, 1, 1]` | Each click is alone in its minute. |
| `clicks_in_last_minute([])` | `[]` | There are no clicks. |

**Rules**

- `times` has 0 to 100,000 items. Each item is a whole number of seconds from 0 to 1,000,000,000.
- `times` never goes down: each time is equal to or greater than the one before.
- For a click at second `t`, count that click and the earlier clicks in the list with a time from `t - 59` to `t`.
- Return a list of the same length as `times`. Return `[]` for an empty list.
- Do not change the list `times`.

## Problem B (main, 25 minutes): Longest run of days within a limit

PaisaLens shows how much you spent on each day, in paise. You want the longest run of days in a row whose total spending stays within a limit. Return how many days that run lasts.

```python
def longest_within_limit(spends: list[int], limit: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `longest_within_limit([20000, 5000, 15000, 40000, 10000, 10000, 5000], 30000)` | `3` | The last three days cost 25000 together. |
| `longest_within_limit([1000, 1000, 1000], 5000)` | `3` | All three days fit. |
| `longest_within_limit([60000, 75000], 50000)` | `0` | Each day alone costs more than the limit. |
| `longest_within_limit([], 10000)` | `0` | There are no days. |

**Rules**

- `spends` has 0 to 100,000 items. Each item is a whole number of paise from 0 to 10,000,000. A day with no spending is 0.
- `limit` is a whole number of paise from 0 to 1,000,000,000.
- A run is one or more days next to each other. Its total must be less than or equal to `limit`.
- Return the number of days in the longest run. Return `0` when no single day fits. An empty list also returns `0`.
- Do not change the list `spends`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What enters the window, what leaves it, and what do you keep up to date as it slides?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Write `best_week(spends)`, which returns the highest total for any 7 days in a row. Keep the window total up to date as it slides, with no call to `sum` inside the loop.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
