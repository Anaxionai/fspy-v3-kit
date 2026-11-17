"""Week 16 problem session: trees and depth-first search.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""

from dataclasses import dataclass


@dataclass
class TreeNode:
    """One node of a binary tree. Do not change this class."""

    value: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


def longest_chain(root: TreeNode | None) -> int:
    """Return how many members sit on the longest chain from the root to a leaf.

    `root` is the first member of a Shortly invite tree. A leaf is a member
    who invited nobody. Count the members on the chain, not the links.

    Return 0 for an empty tree (`None`). Do not change the tree.
    """
    raise NotImplementedError


def tour_for_budget(root: TreeNode | None, budget: int) -> list[int]:
    """Return the costs of a complete tour that adds up to exactly `budget`.

    Each node holds the cost of one day of a RailSeat tour, in rupees. A
    complete tour runs from the root to a leaf. Return its costs in tour
    order, from the root to the leaf.

    When more than one tour matches, return the one that goes left at the
    first city where the tours split. Return [] when no tour matches, and
    for an empty tree. Do not change the tree.
    """
    raise NotImplementedError
