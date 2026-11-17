# Week 16: Trees and depth-first search

## The pattern in five lines

1. A binary tree (nodes where each node has at most two children) starts at one root node at the top.
2. Depth-first search (DFS: follow one branch to its end, then come back and try the next) visits every node.
3. Write DFS as recursion: get the answer for the left subtree (the tree below the left child), then the right, then combine them.
4. Reach for it when the answer at a node depends on its children, or on the path from the root down to it.
5. DFS visits each node once: O(n) time, and O(h) extra space for the calls, where h is the height (the number of levels).

## Problem A (warm-up, 10 minutes): Longest invite chain

Shortly lets each new member invite at most two friends. The invite tree has the first member at the root, and a member's children are the friends they invited. Find how many members sit on the longest chain, from the root down to a leaf (a member who invited nobody).

`problems.py` gives you this `TreeNode` class. Each node holds a member id in `value`.

```python
@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def longest_chain(root: TreeNode | None) -> int:
```

The examples use these two trees:

```text
invites_1:          invites_2:

      1               10
     / \                \
    2   3                20
   /                       \
  4                         30
                              \
                               40
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `longest_chain(invites_1)` | `3` | The chain 1, 2, 4 has three members. |
| `longest_chain(invites_2)` | `4` | Each member invited one friend, so the whole tree is one chain. |
| `longest_chain(TreeNode(5))` | `1` | The root is also a leaf. |
| `longest_chain(None)` | `0` | The tree is empty. |

**Rules**

- The tree has 0 to 10,000 nodes and at most 500 levels.
- An empty tree is `None`. Return `0` for an empty tree.
- Count the members on the chain, not the links between them.
- Do not change the tree.

## Problem B (main, 25 minutes): A tour for the budget

RailSeat sells holiday tours by train. A tour starts in the root city, and after each city it goes on to one of at most two next cities. Each node holds the cost of the day in that city, in rupees. Find a complete tour, from the root to a leaf, whose costs add up to exactly the customer's budget.

```python
def tour_for_budget(root: TreeNode | None, budget: int) -> list[int]:
```

The examples use these two trees:

```text
tour_1:                        tour_2:

           900                      500
          /   \                    /   \
      1200     700              400     600
      /  \        \               \       \
   800    1500    1600            600     400
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `tour_for_budget(tour_1, 3600)` | `[900, 1200, 1500]` | 900 + 1200 + 1500 = 3600. |
| `tour_for_budget(tour_1, 3200)` | `[900, 700, 1600]` | This tour goes right at the root. |
| `tour_for_budget(tour_1, 2100)` | `[]` | 900 + 1200 = 2100, but 1200 is not a leaf, so that tour is not complete. |
| `tour_for_budget(tour_2, 1500)` | `[500, 400, 600]` | Two tours cost 1500. This one goes left at the root. |
| `tour_for_budget(None, 1000)` | `[]` | The tree is empty. |

**Rules**

- The tree has 0 to 10,000 nodes and at most 500 levels.
- Each cost is a whole number of rupees from 1 to 10,000. `budget` is a whole number from 1 to 5,000,000.
- A complete tour ends at a leaf. A tour that stops at a city with a next city does not count.
- Return the costs in tour order, from the root to the leaf.
- When more than one tour matches, return the one that goes left at the first city where the tours split.
- Return `[]` when no tour matches. Return `[]` for an empty tree.
- Do not change the tree.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What does each recursive call need from its parent, and what does it give back?
3. Which edge cases (unusual inputs, such as an empty tree) could break your code? Name three.

## After the session

Write `count_tours(root, budget)`, which returns how many complete tours cost exactly `budget`. Add two tests: one tree with no matching tour, and one tree with three matching tours.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
