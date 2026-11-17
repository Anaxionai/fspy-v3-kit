# Week 22: Dynamic programming in one dimension

## The pattern in five lines

1. Dynamic programming (DP: solve each smaller problem once and remember its answer) fits when the same smaller problems come back again and again.
2. First write the answer for size `i` using the answers for smaller sizes. This rule is the recurrence (the formula that links each size to smaller sizes).
3. Then fill a list from the smallest size up, so each answer is ready before you need it. Set the first one or two values by hand.
4. Reach for it when a plain recursion solves the same smaller problem many times, or when a greedy rule fails on a small example.
5. A one-dimensional table takes O(n) time and O(n) space. Python stops recursion at about 1,000 nested calls, so prefer a loop for long inputs.

## Problem A (warm-up, 10 minutes): Climb the footbridge

The footbridge at Pune Junction has `steps` steps. A porter (a worker who carries luggage) starts on the ground and climbs one or two steps at a time. Some steps are broken, and he must never stand on one. Count the different ways he can reach the top step.

```python
def ways_to_climb(steps: int, broken: list[int]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `ways_to_climb(4, [])` | `5` | 1+1+1+1, 1+1+2, 1+2+1, 2+1+1 and 2+2. |
| `ways_to_climb(5, [3])` | `2` | He must jump from step 2 to step 4. The ways are 1+1+2+1 and 2+2+1. |
| `ways_to_climb(3, [1, 2])` | `0` | He cannot get past steps 1 and 2. |
| `ways_to_climb(0, [])` | `1` | He is already at the top, and that counts as one way. |

**Rules**

- `steps` is a whole number from 0 to 90.
- `broken` holds 0 to `steps` different step numbers, each from 1 to `steps`. The ground is step 0 and is never broken.
- Return `0` when the top step is broken.
- Return `1` when `steps` is 0.
- Do not change the list `broken`.

## Problem B (main, 25 minutes): Best pay without back-to-back shifts

A TiffinTrack rider sees the pay for each delivery shift today, in order, in rupees. A safety rule says a rider must rest after each shift, so the rider cannot work two neighbouring shifts. Find the most pay the rider can earn today.

```python
def best_pay(shifts: list[int]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `best_pay([300, 500, 450, 200])` | `750` | Work the first and third shifts: 300 + 450. |
| `best_pay([500, 600, 500])` | `1000` | Work the first and last shifts. Taking the best-paid shift, 600, first gives only 600. |
| `best_pay([600, 100, 100, 600])` | `1200` | The first and last shifts are not neighbours. |
| `best_pay([450])` | `450` | There is one shift. |
| `best_pay([])` | `0` | There are no shifts. |

**Rules**

- `shifts` has 0 to 10,000 items. Each item is a whole number of rupees from 0 to 5,000.
- Two shifts are neighbours when they sit next to each other in the list.
- The rider can skip any number of shifts in a row.
- Return `0` when `shifts` is empty.
- Do not change the list `shifts`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What is the answer for size `i`, written with the answers for smaller sizes?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Change `best_pay` so that the shifts form a loop: the last shift of the day and the first shift count as neighbours. Add two tests, one where this rule changes the answer.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
