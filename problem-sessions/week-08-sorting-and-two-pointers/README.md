# Week 8: Sort with a key, then two pointers

## The pattern in five lines

1. Sort first. `sorted(items, key=...)` sorts by any value you choose, and a tuple key sorts by two values.
2. Then place two pointers (positions you move along the list), often one at each end.
3. Move one pointer at a time, based on what you see, until the two pointers meet.
4. Reach for this pattern when you need a pair whose total must stay under a limit or come close to a target.
5. The sort is O(n log n) and the walk is O(n), so the whole method is O(n log n). See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Trains in departure order

RailSeat lists the trains from NDLS to BCT. Passengers want them in order of departure time, earliest first. When two trains leave at the same time, show the cheaper one first.

```python
def departure_order(trains: list[tuple[str, str, int]]) -> list[str]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `departure_order([("12951", "16:35", 345000), ("12009", "06:20", 128500), ("22209", "16:35", 298000)])` | `["12009", "22209", "12951"]` | Two trains leave at 16:35, so the cheaper one goes first. |
| `departure_order([("11007", "05:10", 41000), ("11009", "05:10", 41000)])` | `["11007", "11009"]` | The time and the fare are the same, so keep the given order. |
| `departure_order([("12127", "23:55", 52000), ("12125", "00:05", 52000)])` | `["12125", "12127"]` | 00:05 comes before 23:55. |
| `departure_order([])` | `[]` | There are no trains. |

**Rules**

- `trains` has 0 to 100,000 items. Each item is a tuple `(number, departs, fare)`.
- `number` is a train number of 5 digits, such as `"12951"`.
- `departs` is a 24-hour time of 5 characters, from `"00:00"` to `"23:59"`.
- `fare` is a whole number of paise from 0 to 10,000,000.
- Sort by `departs`, earliest first. When two trains have the same `departs`, put the lower `fare` first.
- When two trains have the same `departs` and the same `fare`, keep them in the order of `trains`.
- Return the train numbers only. Return `[]` for an empty list.
- Do not change the list `trains`.

## Problem B (main, 25 minutes): Two gifts within a budget

Meera has a budget for two Diwali gifts, one for each parent. Her PaisaLens wishlist has the price of each gift, in paise. Find the largest total of two different gifts that is not more than her budget.

```python
def best_pair_total(prices: list[int], budget: int) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `best_pair_total([49900, 129900, 89900, 25000], 150000)` | `139800` | 49900 + 89900 fits. 129900 + 25000 is 154900, which is over. |
| `best_pair_total([60000, 40000, 60000], 120000)` | `120000` | Two gifts can have the same price, and the total can equal the budget. |
| `best_pair_total([90000, 80000], 150000)` | `-1` | The only pair costs 170000. |
| `best_pair_total([], 100000)` | `-1` | The wishlist is empty. |

**Rules**

- `prices` has 0 to 100,000 items. Each item is a whole number of paise from 1 to 10,000,000.
- `budget` is a whole number of paise from 1 to 20,000,000.
- The two gifts must be different items in the list, but they can have the same price.
- Return the largest total of two gifts that is less than or equal to `budget`.
- Return `-1` when every pair costs more than `budget`. A list with fewer than two items also returns `-1`.
- Do not change the list `prices`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What does a sorted list tell you that the unsorted list cannot?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Write `best_three_total(prices, budget)` for three different gifts. Sort once, fix the first gift, then use two pointers for the other two. What is its Big-O?

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
