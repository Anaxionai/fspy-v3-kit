# Week 23: Dynamic programming with two-dimensional tables

## The pattern in five lines

1. Some problems need a table with two dimensions: the rows and columns of a grid, or the letters of two words.
2. Cell `[i][j]` holds the answer to a smaller problem, for example the first `i` letters of one word and the first `j` of the other.
3. Fill each cell from cells you have already filled, usually the cell above, the cell to the left and the cell diagonally above-left.
4. Reach for it when a problem compares two strings, or moves through a grid one cell at a time. Fill the first row and column by hand.
5. A table with m rows and n columns takes O(m × n) time and O(m × n) space.

## Problem A (warm-up, 10 minutes): Routes through Hinjewadi

A TiffinTrack rider crosses a grid of lanes in Hinjewadi. The kitchen is at the top-left junction and the customer is at the bottom-right junction. To save time, the rider moves only right or down. Some junctions are closed for road works. Count the different routes.

```python
def count_routes(grid: list[str]) -> int:
```

Each string is one row of junctions: `.` is open and `#` is closed.

**Examples**

| Call | Returns | Why |
|---|---|---|
| `count_routes(["...", "...", "..."])` | `6` | Every route makes 2 moves right and 2 moves down, in some order. |
| `count_routes(["...", ".#.", "..."])` | `2` | The closed middle junction leaves the two routes along the edges. |
| `count_routes(["..#.", "....", "#...", "...."])` | `12` | Two corners are closed, but 12 routes still reach the customer. |
| `count_routes(["#..", "...", "..."])` | `0` | The kitchen's own junction is closed. |
| `count_routes([])` | `0` | There is no grid. |

**Rules**

- `grid` has 0 to 100 rows. Every row has the same length, from 1 to 100.
- Each character is `.` (open) or `#` (closed).
- The rider starts at the top-left junction, ends at the bottom-right junction, and moves only right or down.
- Return `0` when `grid` is empty, or when the first or the last junction is closed.
- Return `1` for a grid with one open junction.
- The answer can be very large. Python's `int` has no size limit, so return the exact number.

## Problem B (main, 25 minutes): Fix a station name

RailSeat's station search must cope with typing mistakes. One edit adds a letter, removes a letter or changes one letter into another. Find the fewest edits that turn what the customer typed into a real station name.

```python
def edit_distance(typed: str, name: str) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `edit_distance("bhopl", "bhopal")` | `1` | Add the letter `a`. |
| `edit_distance("nagpure", "nagpur")` | `1` | Remove the last `e`. |
| `edit_distance("kanpur", "jaipur")` | `2` | Change `k` to `j` and `n` to `i`. |
| `edit_distance("madgaon", "margao")` | `2` | Change `d` to `r`, then remove the last `n`. |
| `edit_distance("pune", "pune")` | `0` | The names already match. |
| `edit_distance("", "agra")` | `4` | Add all four letters. |

**Rules**

- `typed` and `name` each have 0 to 300 characters.
- They use lowercase letters `a` to `z` and spaces. A space counts as a letter.
- Each edit costs 1: add one letter, remove one letter, or change one letter into another.
- Return `len(name)` when `typed` is empty, and `len(typed)` when `name` is empty.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What does one cell of your table mean, and which cells do you build it from?
3. Which edge cases (unusual inputs, such as an empty string) could break your code? Name three.

## After the session

Change `edit_distance` so that changing a letter costs 2, while adding or removing a letter still costs 1. Find a pair of names whose answer changes, and add two tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
