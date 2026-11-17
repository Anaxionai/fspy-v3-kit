# Week 13: Nodes and pointers

## The pattern in five lines

1. A linked list (a chain of nodes, where each node points to the next one) has no positions, only pointers.
2. You reach a node only by walking from the head (the first node), so finding item k costs O(k).
3. To change the chain, change the `next` pointers. Save `node.next` in a variable before you overwrite it.
4. Reach for this pattern when a question is about a chain of nodes: reverse it, find its middle, or check it for a loop.
5. One walk is O(n) time. Extra pointers cost O(1) space, while a set of visited nodes costs O(n). See [the Big-O page](../big-o.md).

## Problem A (warm-up, 10 minutes): Reverse a route

RailSeat stores each train's route as a linked list. Each node holds a station code, and `head` is the first stop. The return train runs the same route backwards. Reverse the chain by changing the pointers, and return the new first stop.

```python
@dataclass(eq=False)
class Node:
    value: str
    next: "Node | None" = None


def reverse_route(head: Node | None) -> Node | None:
```

**Examples**

In the examples, `NDLS -> AGC` means a node with value `"NDLS"` whose `next` is a node with value `"AGC"`. `None` is an empty route.

| Route given | Route returned | Why |
|---|---|---|
| `NDLS -> AGC -> GWL -> BPL` | `BPL -> GWL -> AGC -> NDLS` | Every pointer now points the other way. |
| `MAS -> SBC` | `SBC -> MAS` | The last stop becomes the first. |
| `PUNE` | `PUNE` | A route of one stop stays the same. |
| `None` | `None` | An empty route stays empty. |

**Rules**

- A route has 0 to 10,000 stops. Each value is a station code of 2 to 5 capital letters.
- Two stops can have the same station code.
- Change the `next` pointers only. Do not create new nodes, and do not change any `value`.
- Return the new first stop. Return `None` for an empty route.

## Problem B (main, 25 minutes): Find where a route loops

RailSeat's route editor has a bug: it can point a later stop back to an earlier stop. That route has a loop (a chain that never reaches `None`), so it never ends. Find the position where the loop begins, counting the first stop as 0. Return `-1` when the route ends normally.

```python
def loop_start(head: Node | None) -> int:
```

**Examples**

In the examples, `back to AGC` means that the last stop shown points back to the earlier `AGC` node.

| Route given | Returns | Why |
|---|---|---|
| `NDLS -> AGC -> GWL -> BPL -> back to AGC` | `1` | The loop begins at `AGC`, the stop at position 1. |
| `MAS -> SBC -> back to MAS` | `0` | The whole route is a loop. |
| `ADI -> BRC -> ADI -> BCT` | `-1` | Two stops share the code `ADI`, but the route ends. |
| `None` | `-1` | An empty route has no loop. |

**Rules**

- A route has 0 to 10,000 stops. Two stops can have the same station code.
- When a route has a loop, one stop's `next` points back to an earlier stop or to itself.
- Return the position of the first stop that the walk reaches a second time. Positions start at 0.
- Return `-1` when the route ends with `None`. An empty route also returns `-1`.
- Do not change the route. Leave every `next` pointer as it is.

## Say it aloud

Answer these three questions aloud for each problem before you write code.

1. What is the slow way to solve it, and what is its Big-O?
2. Which nodes must you remember at each step, and in which variables?
3. Which edge cases (unusual inputs, such as an empty route) could break your code? Name three.

## After the session

Write `middle_stop(head)`, which returns the middle stop of a route in one walk. Use two pointers that move at different speeds. Decide which stop to return when the route has an even number of stops.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with `NotImplementedError` until you write your solutions in `problems.py`. Do not change `test_problems.py`.
