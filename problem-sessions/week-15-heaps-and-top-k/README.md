# Week 15: Heaps and the top k

## The pattern in five lines

1. A heap (a list kept in an order where the smallest item is always at position 0) lives in the `heapq` module.
2. `heapq.heappush` and `heapq.heappop` take O(log n) time, and `heapq.heapify` turns a list into a heap in O(n).
3. The smallest item comes out first. For the biggest first, push a negative number, such as `-clicks`.
4. Reach for a heap when you need the next smallest item again and again, or the top k of many items.
5. The top k by heap costs O(n + k log n), against O(n log n) to sort everything. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Lowest free seat

RailSeat gives each new booking in a coach the lowest free seat number. Seats are numbered from 1 to `seat_count`, and all are free at the start. A request of `0` is a new booking. Any other request is the number of a seat that a passenger cancelled, so it is free again.

```python
def give_seats(seat_count: int, requests: list[int]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `give_seats(3, [0, 0, 0])` | `[1, 2, 3]` | Each booking gets the lowest free seat. |
| `give_seats(3, [0, 0, 1, 0, 0])` | `[1, 2, 1, 3]` | Seat 1 is cancelled, so the third booking gets it. |
| `give_seats(1, [0, 0])` | `[1, -1]` | The coach is full for the second booking. |
| `give_seats(5, [])` | `[]` | There are no requests. |

**Rules**

- `seat_count` is a whole number from 1 to 100,000.
- `requests` has 0 to 100,000 items. Each item is `0` or a seat number from 1 to `seat_count`.
- A cancelled seat is always a seat that is booked at that moment.
- Return the seat given to each booking, in order. A booking that finds no free seat gets `-1`.
- Cancellations add nothing to the answer.
- Do not change the list `requests`.

## Problem B (main, 25 minutes): Top links by clicks

Shortly's analytics page shows the top 10 links by clicks. The click log has one short code for each click. Return the k codes with the most clicks, most clicks first. When two codes have the same number of clicks, put them in alphabetical order.

```python
def top_links(clicks: list[str], k: int) -> list[str]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `top_links(["dl7", "mb2", "dl7", "ch9", "mb2", "dl7"], 2)` | `["dl7", "mb2"]` | `dl7` has 3 clicks and `mb2` has 2. |
| `top_links(["pq1", "ab3", "pq1", "ab3", "zz9"], 2)` | `["ab3", "pq1"]` | Both have 2 clicks, so alphabetical order decides. |
| `top_links(["kl5", "kl5"], 3)` | `["kl5"]` | There is one code, so the answer is shorter than 3. |
| `top_links([], 10)` | `[]` | There are no clicks. |

**Rules**

- `clicks` has 0 to 1,000,000 items. Each code has 1 to 10 small letters and digits.
- `k` is a whole number from 1 to 1,000.
- Return at most `k` codes, most clicks first.
- When two codes have the same number of clicks, the one that comes first in alphabetical order goes first. Python's `<` on strings gives this order, with digits before letters.
- Return fewer than `k` codes when there are fewer than `k` different codes. Return `[]` for an empty list.
- Do not change the list `clicks`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which item must come out first each time, and what will you push so that the heap puts it on top?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

The analytics page refreshes every minute while clicks keep arriving. Write a class `TopLinks` with `add_click(code)` and `top(k)`. Which method should be fast, and why?

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
