# Week 20: Intervals that overlap

## The pattern in five lines

1. An interval (a stretch of time with a start and an end) is a pair `(start, end)`.
2. Sort the intervals by start, so that intervals that can overlap sit next to each other.
3. Walk the sorted list once and keep the end of the current block. Each next interval joins the block or starts a new one.
4. Reach for it for bookings, holds or time windows. First ask whether two intervals that touch (one ends where the next starts) overlap.
5. The sort is O(n log n) and the walk is O(n), so the total is O(n log n) time.

## Problem A (warm-up, 10 minutes): Can one rider take every order?

A TiffinTrack rider in Pune has accepted delivery windows for today. Each window is `(start, end)` in minutes after midnight, so `(720, 750)` runs from 12:00 to 12:30. The rider can do one delivery at a time. Check that no two windows overlap.

```python
def can_do_all(windows: list[tuple[int, int]]) -> bool:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `can_do_all([(720, 750), (780, 810), (750, 770)])` | `True` | One window ends at 750 and the next starts at 750. Touching windows do not overlap. |
| `can_do_all([(1140, 1170), (1080, 1150)])` | `False` | The window from 1080 to 1150 runs into the window from 1140 to 1170. |
| `can_do_all([(600, 660), (610, 620)])` | `False` | The second window sits inside the first. |
| `can_do_all([])` | `True` | The rider has no deliveries. |

**Rules**

- `windows` has 0 to 10,000 windows, in any order.
- In each window, `0 <= start < end <= 1440`.
- Two windows overlap when one starts before the other ends. Touching windows do not overlap.
- Return `True` when `windows` is empty.
- Do not change the list `windows`.

## Problem B (main, 25 minutes): Merge seat holds

RailSeat holds seats in coach S4 while customers pay. Each hold is `(start, end)` in minutes after midnight, and holds from different customers can overlap. The operations team wants the periods when at least one seat in S4 was on hold. Merge the holds into these periods.

```python
def held_periods(holds: list[tuple[int, int]]) -> list[tuple[int, int]]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `held_periods([(600, 610), (605, 615), (630, 640)])` | `[(600, 615), (630, 640)]` | The first two holds overlap. The third starts after a gap. |
| `held_periods([(700, 710), (600, 620), (610, 650)])` | `[(600, 650), (700, 710)]` | The holds can come in any order. |
| `held_periods([(600, 610), (610, 620)])` | `[(600, 620)]` | Touching holds join, because the coach had a hold all the time. |
| `held_periods([(500, 600), (520, 530)])` | `[(500, 600)]` | The second hold sits inside the first. |
| `held_periods([])` | `[]` | There are no holds. |

**Rules**

- `holds` has 0 to 10,000 holds, in any order.
- In each hold, `0 <= start < end <= 1440`.
- Join holds that overlap or touch. `(600, 610)` and `(610, 620)` become `(600, 620)`.
- Return the periods as tuples, sorted by start. No two periods in your answer may overlap or touch.
- Return `[]` when `holds` is empty.
- Do not change the list `holds`. The tests check this.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Once the list is sorted, what must you remember from the intervals before the current one?
3. Which edge cases (unusual inputs, such as touching intervals) could break your code? Name three.

## After the session

Write `most_at_once(holds)`, which returns the largest number of holds active at the same moment. Touching holds are not active at the same moment. Add two tests for it.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
