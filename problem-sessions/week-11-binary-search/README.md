# Week 11: Binary search

## The pattern in five lines

1. Binary search (look at the middle, then drop the half that cannot hold the answer) needs sorted data.
2. Keep two ends, `low` and `high`, and look at the middle position on each step.
3. Each step halves the range, so 1,000,000 items need about 20 steps.
4. Reach for it when the list is sorted, or when you can test a guess and every bigger guess also passes.
5. It takes O(log n) steps. Searching on the answer (halving the possible answers, not a list) needs O(log r) checks for r possible answers. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): First train you can catch

RailSeat keeps the departure times of the day's trains, sorted, in minutes after midnight. The platform display needs the first train a passenger can still catch. Find the position of the first train that leaves at or after the passenger's arrival.

```python
def first_train_at_or_after(departures: list[int], arrival: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `first_train_at_or_after([300, 420, 545, 900, 1310], 500)` | `2` | The train at 545 is the first at or after 500. |
| `first_train_at_or_after([300, 420, 420, 900], 420)` | `1` | Two trains leave at 420. The first of them is at position 1. |
| `first_train_at_or_after([300, 420, 545], 1000)` | `-1` | Every train has left. |
| `first_train_at_or_after([], 600)` | `-1` | There are no trains. |

**Rules**

- `departures` has 0 to 20,000 items, sorted from earliest to latest. Each item is a whole number from 0 to 1439.
- Two or more trains can leave at the same minute.
- `arrival` is a whole number from 0 to 1439.
- Return the position of the first train that leaves at or after `arrival`. Positions start at 0.
- Return `-1` when every train leaves before `arrival`. An empty list also returns `-1`.
- Write the halving yourself. Do not use the `bisect` module.
- Do not change the list `departures`.

## Problem B (main, 25 minutes): Ticket checkers on a long train

A train has its coaches in a fixed order, and you know how many passengers sit in each coach. Each TTE (travelling ticket examiner) checks one run of neighbouring coaches. Share the coaches so that the busiest TTE checks as few passengers as possible. Return that number.

```python
def smallest_busiest_load(passengers: list[int], checkers: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `smallest_busiest_load([72, 80, 64, 90, 18, 40], 3)` | `148` | Coach 1, coaches 2 to 3 and coaches 4 to 6 give loads of 72, 144 and 148. |
| `smallest_busiest_load([50, 50, 50, 50], 2)` | `100` | Each TTE takes two coaches. |
| `smallest_busiest_load([30, 120, 45], 5)` | `120` | One TTE must check the coach of 120 alone. |
| `smallest_busiest_load([], 3)` | `0` | The train has no coaches. |

**Rules**

- `passengers` has 0 to 10,000 items. Each item is a whole number from 0 to 500.
- `checkers` is the number of TTEs, a whole number from 1 to 10,000.
- Each TTE checks one run of neighbouring coaches, in the train's order. No coach is split between two TTEs.
- A TTE may check no coaches when there are more TTEs than coaches.
- Return the smallest possible number of passengers for the busiest TTE. Return `0` for an empty list.
- Do not change the list `passengers`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. After one look at the middle, which half can you throw away, and why?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Change `smallest_busiest_load` so that it also returns where each TTE starts, as a list of coach positions. Use the smallest load you found, and walk the coaches once more.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
