# Week 26: Mock interview 1

## How a mock works

1. Your mentor or a partner plays the interviewer. Read the problem twice, then say it back in your own words.
2. Ask the interviewer at least one question before you plan, for example about empty input, negative numbers or the largest size.
3. Say the slow way and its Big-O, then say how you will make it faster, and why.
4. Write the code, and talk while you write it, so the interviewer can follow your thinking.
5. Run the tests, then check one example by hand. You have 20 minutes for each problem.

## Problem A (20 minutes): Stretches that add up to a target

PaisaLens shows the net change in your account for each day, in paise: money in minus money out. A stretch is one or more days in a row. Count the stretches whose changes add up to exactly `target`.

```python
def count_stretches(changes: list[int], target: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `count_stretches([300, -300, 300, -300], 0)` | `4` | Days 1 to 2, days 2 to 3, days 3 to 4 and days 1 to 4 each add up to 0. |
| `count_stretches([500, 200, -200, 700], 700)` | `3` | Days 1 to 2, day 4 alone, and days 2 to 4 (200 - 200 + 700). |
| `count_stretches([100, 100], 300)` | `0` | The largest stretch adds up to 200. |
| `count_stretches([], 0)` | `0` | There are no days, so there are no stretches. |

**Rules**

- `changes` has 0 to 10,000 items. Each item is a whole number of paise from -1,000,000 to 1,000,000, so it can be negative or 0.
- `target` is a whole number from -1,000,000,000 to 1,000,000,000.
- A stretch has at least one day, and its days sit next to each other in the list.
- Count every stretch that matches, even when two stretches share days.
- Return `0` when `changes` is empty.
- Do not change the list `changes`.

## Problem B (20 minutes): The slowest encoder that is on time

ReelPipe must encode every video in its queue within `hours` hours. An encoder set to speed `s` handles `s` minutes of video in one hour, and it works on one video at a time. A video always takes a whole number of hours: a 45-minute video at speed 20 takes 3 hours. Find the smallest whole-number speed that finishes every video on time.

```python
def slowest_speed(videos: list[int], hours: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `slowest_speed([12, 45, 30, 8], 7)` | `15` | At speed 15 the videos take 1 + 3 + 2 + 1 = 7 hours. At speed 14 they take 1 + 4 + 3 + 1 = 9. |
| `slowest_speed([12, 45, 30, 8], 4)` | `45` | Each video must take one hour, so the speed must cover the 45-minute video. |
| `slowest_speed([12, 45, 30, 8], 100)` | `1` | At speed 1 the videos take 95 hours, which is on time. |
| `slowest_speed([60], 4)` | `15` | 60 minutes in 4 hours. |
| `slowest_speed([], 5)` | `0` | There is nothing to encode. |

**Rules**

- `videos` has 0 to 10,000 items. Each item is a whole number of minutes from 1 to 1,000,000.
- `hours` is a whole number from the number of videos up to 1,000,000,000, so some speed is always on time.
- A video of `m` minutes at speed `s` takes `m / s` hours, rounded up to a whole number. The encoder starts the next video at the start of the next hour.
- Return `0` when `videos` is empty.
- Do not change the list `videos`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which earlier session does this problem remind you of, and which idea from that session makes it faster?
3. Which edge cases (unusual inputs, such as negative numbers or an empty list) could break your code? Name three.

## After the session

Write `longest_stretch(changes, target)`, which returns the number of days in the longest stretch that adds up to `target`, or `0` when no stretch does. Add two tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
