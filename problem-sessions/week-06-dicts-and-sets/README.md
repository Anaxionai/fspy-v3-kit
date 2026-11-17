# Week 6: Counting and fast lookup with a dict or set

## The pattern in five lines

1. Walk the list once and remember what you have seen in a dict or a set.
2. A set answers "have I seen this before?" in O(1) time, with no second loop.
3. A dict maps each item to something you need later, such as a count or a position.
4. Reach for this pattern when a question asks about repeats, counts or a matching pair.
5. It takes O(n) time and O(n) extra space, against O(n²) for a loop inside a loop. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): First repeated PNR

RailSeat receives booking requests one after another. Each request carries a PNR (the 10-character booking number), and a PNR should arrive only once. A repeat means a passenger pressed "Book" twice. Find the first request that repeats an earlier PNR, and return that PNR.

```python
def first_repeat(pnrs: list[str]) -> str:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `first_repeat(["RS4K7Q2M9A", "RS8B1N5T3C", "RS4K7Q2M9A"])` | `"RS4K7Q2M9A"` | The third request repeats the first. |
| `first_repeat(["RS4K7Q2M9A", "RS8B1N5T3C", "RS8B1N5T3C", "RS4K7Q2M9A"])` | `"RS8B1N5T3C"` | The third request is the first repeat. The fourth request comes later. |
| `first_repeat(["RS4K7Q2M9A", "RS8B1N5T3C", "RS2D6W0Y8E"])` | `""` | Every PNR arrives once. |
| `first_repeat([])` | `""` | There are no requests. |

**Rules**

- `pnrs` has 0 to 100,000 items. Each PNR has 10 characters: capital letters and digits.
- Return the PNR of the earliest request that repeats an earlier request.
- Return `""` (an empty string) when no PNR repeats. An empty list also returns `""`.
- Do not change the list `pnrs`.

## Problem B (main, 25 minutes): Two spends that match a payment

Ravi owes you for two of your spends, and he sent one UPI payment to cover both. PaisaLens has the list of your spends, in paise. Find the two spends whose amounts add up to Ravi's payment.

```python
def matching_pair(spends: list[int], payment: int) -> tuple[int, int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `matching_pair([45000, 120000, 65000, 30000], 95000)` | `(2, 3)` | 65000 + 30000 is 95000. |
| `matching_pair([20000, 50000, 20000], 40000)` | `(0, 2)` | Two different spends can have the same amount. |
| `matching_pair([50000, 10000], 100000)` | `(-1, -1)` | One spend cannot count twice. |
| `matching_pair([], 50000)` | `(-1, -1)` | There are no spends. |

**Rules**

- `spends` has 0 to 100,000 items. Each item is a whole number of paise from 1 to 10,000,000.
- `payment` is a whole number of paise from 2 to 20,000,000.
- At most one pair of spends adds up to `payment`.
- Return the two positions as a tuple, smaller position first. Positions start at 0.
- The two spends must be at different positions, but they can have the same amount.
- Return `(-1, -1)` when no pair adds up to `payment`. A list with fewer than two items also returns `(-1, -1)`.
- Do not change the list `spends`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What should a dict or a set remember for you, so that one pass is enough?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Write `count_pairs(spends, payment)`. It counts every pair of positions whose amounts add up to `payment`, with no limit on how many pairs exist. Use a dict that counts each amount. Add two tests where one amount appears three times.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
