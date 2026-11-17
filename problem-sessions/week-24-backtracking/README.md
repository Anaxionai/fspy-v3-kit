# Week 24: Backtracking: try, check, undo

## The pattern in five lines

1. Backtracking (building an answer one choice at a time, and undoing choices that fail) explores every possible answer but stops early on bad ones.
2. Write one recursive function: try each choice, check the rule, go one level deeper, then undo the choice.
3. Undo means you remove what you added, so the next choice starts clean. Save a copy of an answer, not the list you keep changing.
4. Reach for it when a question says "list every", "count every" or "place these under a rule", and the input is small.
5. The time is often exponential, such as O(2^n) or O(n!), so read the input limits before you start.

## Problem A (warm-up, 10 minutes): Add-ons for a meal voucher

A TiffinTrack customer has a meal voucher worth `voucher` rupees. It works only when the add-ons in the cart cost exactly that amount. Each add-on has a different price and can go in the cart at most once. List every set of add-ons that uses the voucher exactly.

```python
def addon_sets(prices: list[int], voucher: int) -> list[list[int]]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `addon_sets([20, 30, 50, 70], 100)` | `[[20, 30, 50], [30, 70]]` | 20 + 30 + 50 = 100 and 30 + 70 = 100. |
| `addon_sets([40, 60, 25], 100)` | `[[40, 60]]` | One set matches. |
| `addon_sets([10, 20, 30, 40], 50)` | `[[10, 40], [20, 30]]` | Two sets match. 10 + 20 + 30 = 60 is too much. |
| `addon_sets([15, 25], 30)` | `[]` | No set adds up to 30. The 15 add-on cannot go in twice. |
| `addon_sets([], 50)` | `[]` | There are no add-ons. |

**Rules**

- `prices` has 0 to 20 different prices. Each price is a whole number of rupees from 1 to 1,000.
- `voucher` is a whole number from 1 to 20,000.
- Each add-on goes in a set at most once. No set may appear twice in your answer.
- The order of the sets, and of the prices inside each set, does not matter. The tests sort them before they compare.
- Return `[]` when no set matches. An empty `prices` list also returns `[]`.
- Do not change the list `prices`.

## Problem B (main, 25 minutes): Seat the school group

A school books one row of seats on a RailSeat train for a trip. The teacher gives you pairs of students who must not sit next to each other. Count the different ways to seat all the students in the row.

```python
def count_seatings(students: list[str], apart: list[tuple[str, str]]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `count_seatings(["Asha", "Ravi", "Meera"], [("Asha", "Ravi")])` | `2` | Asha, Meera, Ravi and Ravi, Meera, Asha. Meera must sit in the middle. |
| `count_seatings(["Asha", "Ravi", "Meera"], [])` | `6` | No pair must sit apart, so every order works. |
| `count_seatings(["Asha", "Ravi", "Meera"], [("Asha", "Ravi"), ("Ravi", "Meera")])` | `0` | Ravi always sits next to Asha or Meera. |
| `count_seatings(["Kabir", "Diya", "Arjun", "Isha"], [("Kabir", "Diya")])` | `12` | There are 24 orders, and Kabir sits next to Diya in 12 of them. |
| `count_seatings([], [])` | `1` | There is one way to seat nobody: an empty row. |

**Rules**

- `students` has 0 to 8 different names.
- Each pair in `apart` names two different students from `students`. No pair appears twice.
- A pair must not sit in neighbouring seats, in either order.
- The seats form one straight row, so the first and the last seat are not neighbours.
- Return `1` when `students` is empty.
- Do not change the lists.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which choices do you try at each level, which rule do you check, and how do you undo a choice?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Write `first_seating(students, apart)`, which returns one valid seating as a list of names, or `None` when there is none. Stop as soon as you find one. Add two tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
