# Week 12: Recursion

## The pattern in five lines

1. A recursive function (a function that calls itself) solves a smaller version of the same problem first.
2. Write the base case (an input so small that you know the answer) first, at the top of the function.
3. Every call must move closer to the base case, or the calls never stop.
4. Reach for recursion when data nests, such as lists inside lists, or when you build every choice step by step.
5. Count the calls and the work in each call. Two choices for each of n items make 2ⁿ calls, so keep n small. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Flatten spending folders

PaisaLens lets you group spends into folders, and a folder can hold smaller folders. Each folder is a list that holds amounts in paise and other folders. Return every amount as one flat list, in the order you meet them from left to right.

```python
def flatten(folder: list[int | list]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `flatten([12000, [4500, 8000], 30000])` | `[12000, 4500, 8000, 30000]` | The inner folder's amounts stay in their place. |
| `flatten([[1000, [2000, [3000]]], 4000])` | `[1000, 2000, 3000, 4000]` | Folders can sit inside folders inside folders. |
| `flatten([[], [[]], 500])` | `[500]` | Empty folders add nothing. |
| `flatten([])` | `[]` | The folder is empty. |

**Rules**

- A folder holds whole numbers and other folders, in any mix.
- There are 0 to 10,000 amounts in total. Each amount is a whole number of paise from 0 to 10,000,000.
- Folders sit at most 50 levels deep.
- Return a new list. Do not change `folder` or any folder inside it.

## Problem B (main, 25 minutes): Every way to pay with vouchers

PaisaLens keeps your gift vouchers, each worth a fixed amount in paise. A shop takes any mix of vouchers but gives no change. List every choice of vouchers whose values add up to exactly the bill.

```python
def voucher_choices(vouchers: list[int], bill: int) -> list[list[int]]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `voucher_choices([500, 1000, 1500, 2000], 2500)` | `[[500, 2000], [1000, 1500]]` | Two choices make 2500 exactly. |
| `voucher_choices([1000, 1000, 2000], 2000)` | `[[1000, 1000], [2000]]` | Two vouchers can have the same value. |
| `voucher_choices([700, 900], 1000)` | `[]` | No choice makes 1000. |
| `voucher_choices([], 500)` | `[]` | You have no vouchers. |

**Rules**

- `vouchers` has 0 to 16 items. Each item is a whole number of paise from 1 to 1,000,000.
- `bill` is a whole number of paise from 1 to 20,000,000.
- Use each voucher at most once. Keep the vouchers in each choice in the order of `vouchers`.
- Two vouchers with the same value are still different vouchers. So the same amounts can appear in two choices.
- You may return the choices in any order. The tests sort them before they compare.
- Return `[]` when no choice adds up to `bill`. An empty list also returns `[]`.
- Do not change the list `vouchers`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What is the base case, and how does each call make the problem smaller?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Change the rules of `voucher_choices` so that you can use each voucher any number of times. What must change in your recursion, and what stops it from calling itself without end?

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
