"""Week 13 problem session: nodes and pointers.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""

from dataclasses import dataclass


@dataclass(eq=False)
class Node:
    """One stop on a route: a station code and a pointer to the next stop.

    `eq=False` means two nodes are equal only when they are the same node.
    So you can keep nodes in a set or use them as dict keys.
    """

    value: str
    next: "Node | None" = None


def reverse_route(head: Node | None) -> Node | None:
    """Reverse the route and return its new first stop.

    Change the `next` pointers only. Do not create new nodes, and do not
    change any `value`. Return None for an empty route.
    """
    raise NotImplementedError


def loop_start(head: Node | None) -> int:
    """Return the position where the route's loop begins, or -1 for no loop.

    The first stop is at position 0. Return the position of the first stop
    that the walk reaches a second time. Return -1 when the route ends with
    None, and for an empty route. Do not change any `next` pointer.
    """
    raise NotImplementedError
