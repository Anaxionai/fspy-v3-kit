# Week 19: Depth-first search on graphs, groups and run order

## The pattern in five lines

1. DFS on a graph goes from a node to a neighbour it has not seen, as deep as it can, then backs up.
2. Start a new DFS from each node not yet seen. Each new start finds one connected component (a group of nodes joined by any path).
3. A topological order (an order where each node comes after everything it depends on) adds a node once all its dependencies are finished.
4. Give each node one of three states: not started, in progress or finished. Reaching an in-progress node again means a cycle (a loop).
5. Reach for it for groups, "what must come first" and loops. DFS takes O(V + E) time and O(V) extra space.

## Problem A (warm-up, 10 minutes): Bill-splitting groups

PaisaLens shows which friends have split a bill together. Two friends are in the same group when a chain of shared bills joins them. Count the groups. A friend who shared no bill is a group of one.

```python
def count_groups(friends: list[str], shared: list[tuple[str, str]]) -> int:
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `count_groups(["Asha", "Ravi", "Meera", "John", "Zoya"], [("Asha", "Ravi"), ("Ravi", "Meera"), ("John", "Zoya")])` | `2` | Asha, Ravi and Meera form one group. John and Zoya form the other. |
| `count_groups(["Asha", "Ravi", "Meera"], [])` | `3` | Nobody shared a bill, so each friend is a group of one. |
| `count_groups(["Asha", "Ravi", "Meera", "John"], [("Asha", "John"), ("Meera", "Ravi"), ("John", "Meera")])` | `1` | The chain Asha, John, Meera, Ravi joins everyone. |
| `count_groups([], [])` | `0` | There are no friends. |

**Rules**

- `friends` has 0 to 500 different names.
- `shared` has 0 to 5,000 pairs. Both names in a pair are in `friends`, and they are different names.
- A shared bill joins both friends, whichever name comes first in the pair.
- The same pair can appear more than once.
- Return `0` when `friends` is empty.
- Do not change the lists.

## Problem B (main, 25 minutes): Pipeline run order

This week you build a CI/CD pipeline (an automatic way to test and release code) for Shortly. Each job lists the jobs that must finish before it can start. Return an order that runs every job once, after all the jobs it needs. When no such order exists, raise `ValueError`.

```python
def run_order(needs: dict[str, list[str]]) -> list[str]:
```

The examples use this pipeline:

```python
pipeline = {
    "install": [],
    "lint": ["install"],
    "unit-tests": ["install"],
    "build-image": ["lint", "unit-tests"],
    "deploy": ["build-image"],
}
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `run_order(pipeline)` | `["install", "lint", "unit-tests", "build-image", "deploy"]` | One correct order. `"unit-tests"` can also come before `"lint"`. |
| `run_order({"migrate": ["build"], "build": ["migrate"]})` | raises `ValueError` | Each job waits for the other, so neither can start. |
| `run_order({"deploy": ["deploy"]})` | raises `ValueError` | A job that needs itself can never start. |
| `run_order({"lint": []})` | `["lint"]` | One job that waits for nothing. |
| `run_order({})` | `[]` | There are no jobs. |

**Rules**

- `needs` has 0 to 500 jobs. Each job lists 0 to 20 jobs that it needs.
- Every job named in a list is also a key in `needs`.
- Return each job exactly once. Any order that keeps every rule is correct, so the tests check the rules, not one fixed order.
- Raise `ValueError` when the jobs contain a cycle (a loop of jobs where each one waits for the next). A job that needs itself is a cycle too.
- Return `[]` when `needs` is empty.
- Do not change `needs`.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What must you remember about each node during the DFS, so that you visit it only once and still notice a loop?
3. Which edge cases (unusual inputs, such as an empty pipeline) could break your code? Name three.

## After the session

Change `run_order` so that its `ValueError` message names the jobs in the cycle, in order, for example `"cycle: build -> package -> sign -> build"`. Add two tests for the message.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
