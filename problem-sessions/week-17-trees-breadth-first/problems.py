"""Week 17 problem session: trees level by level, and binary search trees.

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


def staff_by_level(root: TreeNode | None) -> list[list[int]]:
    """Return the staff ids level by level, from the root level down.

    Return one list for each level. Within a level, list the ids from left
    to right.

    Return [] for an empty tree (`None`). Do not change the tree.
    """
    raise NotImplementedError


def is_valid_bst(root: TreeNode | None) -> bool:
    """Return True when the tree is a valid binary search tree.

    Every id in a node's left subtree must be smaller than the node's id.
    Every id in its right subtree must be larger. Two equal ids anywhere in
    the tree make it invalid.

    Return True for an empty tree (`None`). Do not change the tree.
    """
    raise NotImplementedError
