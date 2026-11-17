# Week 17: Trees level by level, and binary search trees

## The pattern in five lines

1. Breadth-first search (BFS: visit the nodes level by level, nearest first) uses a queue (a line where the first item in is the first out).
2. Put the root in a `collections.deque`, take nodes from the front, and add their children at the back.
3. To keep the levels apart, count the nodes in the queue at the start of each round, and take exactly that many.
4. A binary search tree (BST) keeps smaller values to the left of each node and larger values to the right. A search goes one way at each node.
5. BFS takes O(n) time and O(w) extra space, where w is the widest level. A BST search takes O(h), where h is the height.

## Problem A (warm-up, 10 minutes): Staff chart, level by level

TiffinTrack's Pune team forms a tree. The city lead is the root, and each person manages at most two people. List the staff ids level by level, from the top down. Within a level, list them from left to right.

`problems.py` gives you the same `TreeNode` class as last week. Each node holds a staff id in `value`.

```python
@dataclass
class TreeNode:
    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def staff_by_level(root: TreeNode | None) -> list[list[int]]:
```

The examples use these two trees:

```text
team_1:              team_2:

        1               7
      /   \            /
     2     3          8
    / \     \          \
   4   5     6          9
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `staff_by_level(team_1)` | `[[1], [2, 3], [4, 5, 6]]` | The tree has three levels. |
| `staff_by_level(team_2)` | `[[7], [8], [9]]` | Each level has one person. |
| `staff_by_level(TreeNode(5))` | `[[5]]` | The city lead manages nobody. |
| `staff_by_level(None)` | `[]` | The tree is empty. |

**Rules**

- The tree has 0 to 10,000 nodes and at most 500 levels.
- Return one list for each level, from the root level down.
- Within a level, list the ids from left to right.
- Return `[]` for an empty tree (`None`).
- Do not change the tree.

## Problem B (main, 25 minutes): Check the booking tree

RailSeat keeps today's booking ids in a BST. Every id in a node's left subtree (the tree below its left child) must be smaller than the node's id. Every id in its right subtree must be larger. An import script had a bug, so check whether the tree is still a valid BST.

```python
def is_valid_bst(root: TreeNode | None) -> bool:
```

The examples use these three trees:

```text
bookings_1:            bookings_2:            bookings_3:

        50                     50                  50
       /  \                   /  \                /
     30    70               30    70            50
    /  \     \             /  \
  20    40    90         20    60
```

**Examples**

| Call | Returns | Why |
|---|---|---|
| `is_valid_bst(bookings_1)` | `True` | Every node keeps the rule. |
| `is_valid_bst(bookings_2)` | `False` | 60 sits in the left subtree of 50, but 60 is larger than 50. |
| `is_valid_bst(bookings_3)` | `False` | Booking ids must be different, so 50 cannot sit below 50. |
| `is_valid_bst(TreeNode(42))` | `True` | One node keeps the rule. |
| `is_valid_bst(None)` | `True` | An empty tree breaks no rule. |

**Rules**

- The tree has 0 to 10,000 nodes and at most 500 levels.
- Each booking id is a whole number from 1 to 10,000,000.
- The rule covers the whole subtree, not only a node's own children.
- Two equal ids anywhere in the tree make it invalid.
- Return `True` for an empty tree (`None`).
- Do not change the tree.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. What must you keep in the queue, or pass down to each node, so that one visit per node is enough?
3. Which edge cases (unusual inputs, such as an empty tree) could break your code? Name three.

## After the session

Write `zigzag_levels(root)`. It lists level 1 (the root) from left to right and level 2 from right to left, then keeps switching direction at each level. Add two tests, one with three levels and one with an empty tree.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
