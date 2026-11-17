# Week 21: Greedy choices, and why they are safe

## The pattern in five lines

1. A greedy algorithm (one that takes the best-looking choice at each step and never goes back) is often a sort, then one pass.
2. The hard part is the proof: say why your choice can never be worse than any other choice.
3. The usual proof is an exchange: take any best answer, swap in your greedy choice, and show the answer is still as good.
4. Reach for it when a choice now never limits later choices more than the other options would. Test your rule on small cases first, because many greedy rules are wrong.
5. Most greedy solutions take O(n log n) time for the sort, then O(n) for the pass.

## Problem A (warm-up, 10 minutes): Most videos on the free plan

ReelPipe's free plan encodes up to `free_minutes` of video each day. Each upload in the queue has a length in whole minutes. You may pick any uploads, in any order. Find the largest number of uploads that fit in the free minutes.

```python
def most_videos(lengths: list[int], free_minutes: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `most_videos([12, 5, 30, 8], 25)` | `3` | 5 + 8 + 12 = 25, which fits exactly. |
| `most_videos([40, 10, 10, 25], 50)` | `3` | 10 + 10 + 25 = 45. Picking 40 first leaves room for only one more upload. |
| `most_videos([60, 45], 30)` | `0` | Each upload is longer than 30 minutes. |
| `most_videos([], 100)` | `0` | The queue is empty. |

**Rules**

- `lengths` has 0 to 10,000 items. Each item is a whole number of minutes from 1 to 600.
- `free_minutes` is a whole number from 0 to 1,000,000.
- The total length of the uploads you pick must be equal to or less than `free_minutes`.
- Return `0` when `lengths` is empty.
- Do not change the list `lengths`.

## Problem B (main, 25 minutes): Most bookings for one retiring room

RailSeat rents out one retiring room (a rest room for passengers) at Pune Junction by the hour. Each request is `(start, end)` in hours after Monday 00:00. The room takes one guest at a time. Find the largest number of requests the room can accept with no two overlapping.

```python
def most_bookings(requests: list[tuple[int, int]]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `most_bookings([(0, 10), (2, 4), (4, 8), (9, 12)])` | `3` | Accept (2, 4), (4, 8) and (9, 12). One guest leaves at 4 and the next arrives at 4. |
| `most_bookings([(0, 6), (5, 8), (7, 14)])` | `2` | Accept (0, 6) and (7, 14). Taking the shortest request, (5, 8), first leaves room for nothing else. |
| `most_bookings([(0, 50), (1, 3), (3, 5)])` | `2` | Accept (1, 3) and (3, 5). Taking the earliest start, (0, 50), first gives only 1. |
| `most_bookings([(20, 30), (5, 25), (28, 40), (30, 36)])` | `2` | For example, accept (5, 25) and (30, 36). No three requests fit together. |
| `most_bookings([])` | `0` | There are no requests. |

**Rules**

- `requests` has 0 to 10,000 requests, in any order.
- In each request, `0 <= start < end <= 168`.
- Two requests overlap when one starts before the other ends. Touching requests do not overlap.
- Return `0` when `requests` is empty.
- Do not change the list `requests`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which choice will you make first, and why can that choice never be a mistake?
3. Which edge cases (unusual inputs, such as an exact fit) could break your code? Name three.

## After the session

Change `most_bookings` so that it returns the accepted requests themselves, sorted by start. When two answers are equally large, return any one of them. Add two tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
