# Week 27: Mock interview 2

## How a mock works

1. Your mentor or a partner plays the interviewer. Read the problem twice, then say it back in your own words.
2. Ask the interviewer at least one question before you plan, for example about empty input, equal values or the largest size.
3. Say the slow way and its Big-O, then say how you will make it faster, and why.
4. Write the code, and talk while you write it, so the interviewer can follow your thinking.
5. Run the tests, then check one example by hand. You have 20 minutes for each problem.

## Problem A (20 minutes): Wait for a cheaper fare

RailSeat shows the lowest fare from Pune to New Delhi for each of the coming days, in rupees. For each day, a customer wants to know how many days they must wait for a lower fare. Use 0 when no later day is cheaper.

```python
def days_until_cheaper(fares: list[int]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `days_until_cheaper([2400, 2100, 2300, 1900, 2000])` | `[1, 2, 1, 0, 0]` | From 2100 you wait 2 days for 1900. Nothing after 1900 is cheaper. |
| `days_until_cheaper([1500, 1500, 1400])` | `[2, 1, 0]` | An equal fare is not cheaper, so the first day waits for 1400. |
| `days_until_cheaper([1000, 1200, 1300])` | `[0, 0, 0]` | The fare only rises. |
| `days_until_cheaper([])` | `[]` | There are no days. |

**Rules**

- `fares` has 0 to 100,000 items. Each item is a whole number of rupees from 1 to 100,000.
- Only a lower fare counts. An equal fare does not.
- Return one number for each day, in the same order as `fares`.
- Return `[]` when `fares` is empty.
- Do not change the list `fares`.

## Problem B (20 minutes): Delivery clusters

TiffinTrack maps one Pune neighbourhood as a grid of blocks. `H` marks a block with an order today, and `.` marks a block without one. Blocks with orders that share a side form one cluster, and one rider serves each cluster. Return the size of every cluster, from largest to smallest.

```python
def cluster_sizes(grid: list[str]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `cluster_sizes(["HH..", "H..H", "..HH"])` | `[3, 3]` | One cluster in the top-left corner and one in the bottom-right corner. |
| `cluster_sizes(["H.H", ".H.", "H.H"])` | `[1, 1, 1, 1, 1]` | The blocks touch only at corners, so each block is its own cluster. |
| `cluster_sizes(["...", "..."])` | `[]` | There are no orders. |
| `cluster_sizes([])` | `[]` | There is no grid. |

**Rules**

- `grid` has 0 to 20 rows. Every row has the same length, from 1 to 20.
- Each character is `H` (an order) or `.` (no order).
- Two blocks share a side when one is directly above, below, left or right of the other. Blocks that touch only at a corner do not.
- Return the sizes from largest to smallest. Return `[]` when the grid is empty or has no orders.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which earlier session does this problem remind you of, and which idea from that session makes it faster?
3. Which edge cases (unusual inputs, such as equal fares or a grid with one row) could break your code? Name three.

## After the session

Change `cluster_sizes` so that blocks that touch at a corner also join a cluster. Say which README example changes and what it returns now, then add two tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
