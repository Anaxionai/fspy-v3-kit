# Week 9: Stacks

## The pattern in five lines

1. A stack (a pile where you add and remove items at the top only) is a Python list with `append` and `pop`.
2. The last item you push (add to the top) is the first item you pop (take off the top).
3. Push when something opens or starts to wait. Pop when it closes or its wait ends.
4. Reach for a stack when items match in pairs, or when a later item settles an earlier one.
5. `append` and `pop` at the end of a list are O(1), so one pass with a stack is O(n) time and O(n) space. See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Brackets in a filter rule

PaisaLens lets you write a filter such as `(food or [travel and {rail}])`. Before it runs a filter, it checks the brackets. Write that check.

```python
def brackets_match(rule: str) -> bool:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `brackets_match("(food or [travel and {rail}])")` | `True` | Each pair closes after every pair that opened inside it. |
| `brackets_match("(food or [travel)]")` | `False` | The `)` comes before the `[` has closed. |
| `brackets_match("((dinner)")` | `False` | One `(` never closes. |
| `brackets_match("")` | `True` | Empty text has no brackets to match. |

**Rules**

- `rule` has 0 to 100,000 characters.
- The brackets are `()`, `[]` and `{}`. Ignore every other character.
- Every opening bracket needs a closing bracket of the same kind, later in the text.
- A pair that opens inside another pair must also close inside it.
- Return `True` when the rule has no brackets. The empty string also returns `True`.

## Problem B (main, 25 minutes): Overs until a bigger over

Match Centre shows the runs scored in each over. For each over, the commentators want to know how long the batting side waited for a bigger over. Count how many overs later the next over with more runs came.

```python
def overs_until_bigger(runs: list[int]) -> list[int]:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `overs_until_bigger([6, 4, 9, 3, 2, 12])` | `[2, 1, 3, 2, 1, 0]` | After the first over (6 runs), the third over (9 runs) is the next bigger one. |
| `overs_until_bigger([8, 8, 10])` | `[2, 1, 0]` | An over with the same runs is not bigger. |
| `overs_until_bigger([15, 11, 7])` | `[0, 0, 0]` | No over is followed by a bigger one. |
| `overs_until_bigger([])` | `[]` | No overs were bowled. |

**Rules**

- `runs` has 0 to 100,000 items. Each item is a whole number from 0 to 50.
- For each over, find the next later over with more runs. Return how many overs later it comes.
- Use `0` for an over that no later over beats.
- Return a list of the same length as `runs`. Return `[]` for an empty list.
- Do not change the list `runs`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which items have you seen but not settled yet, and in what order will you settle them?
3. Which edge cases (unusual inputs, such as an empty list) could break your code? Name three.

## After the session

Change `brackets_match` so that it returns the position of the first bracket that breaks the rules, or `-1` when every bracket matches. Decide what to return when an opening bracket never closes. Add three tests.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
