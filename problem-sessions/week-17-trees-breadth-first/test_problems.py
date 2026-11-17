"""Tests for the week 17 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import TreeNode, is_valid_bst, staff_by_level


def numbered_tree(number: int, last: int) -> TreeNode | None:
    """Build a full tree numbered level by level: node k has children 2k and 2k + 1."""
    if number > last:
        return None
    return TreeNode(number, numbered_tree(2 * number, last), numbered_tree(2 * number + 1, last))


def balanced_bst(low: int, high: int) -> TreeNode | None:
    """Build a valid BST that holds every id from `low` to `high`."""
    if low > high:
        return None
    middle = (low + high) // 2
    return TreeNode(middle, balanced_bst(low, middle - 1), balanced_bst(middle + 1, high))


def right_chain(length: int) -> TreeNode | None:
    """Build a chain 1, 2, 3, ... where each node is the right child of the one before."""
    root = None
    for value in range(length, 0, -1):
        root = TreeNode(value, None, root)
    return root


def bst_with_one_bad_id() -> TreeNode | None:
    """A valid BST of ids 1 to 1,023, then the largest id in the root's left subtree becomes 600.

    600 is larger than its parent, so the local check passes. It is also larger than the root, 512.
    """
    root = balanced_bst(1, 1023)
    node = root.left
    while node.right is not None:
        node = node.right
    node.value = 600
    return root


# The trees drawn in README.md.
TEAM_1 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3, None, TreeNode(6)))
TEAM_2 = TreeNode(7, TreeNode(8, None, TreeNode(9)))

BOOKINGS_1 = TreeNode(50, TreeNode(30, TreeNode(20), TreeNode(40)), TreeNode(70, None, TreeNode(90)))
BOOKINGS_2 = TreeNode(50, TreeNode(30, TreeNode(20), TreeNode(60)), TreeNode(70))
BOOKINGS_3 = TreeNode(50, TreeNode(50))


@pytest.mark.parametrize(
    ("root", "expected"),
    [
        pytest.param(TEAM_1, [[1], [2, 3], [4, 5, 6]], id="readme-1"),
        pytest.param(TEAM_2, [[7], [8], [9]], id="readme-2-one-per-level"),
        pytest.param(TreeNode(5), [[5]], id="readme-3-one-node"),
        pytest.param(None, [], id="readme-4-empty-tree"),
        pytest.param(right_chain(3), [[1], [2], [3]], id="right-children-only"),
        pytest.param(
            TreeNode(1, TreeNode(2, TreeNode(4, TreeNode(8))), TreeNode(3, None, TreeNode(7))),
            [[1], [2, 3], [4, 7], [8]],
            id="uneven-branches",
        ),
        pytest.param(TreeNode(5, TreeNode(5), TreeNode(5)), [[5], [5, 5]], id="same-id-repeated"),
        pytest.param(
            numbered_tree(1, 1023),
            [list(range(2**level, 2 ** (level + 1))) for level in range(10)],
            id="larger-1023-nodes",
        ),
    ],
)
def test_staff_by_level(root, expected):
    assert staff_by_level(root) == expected


@pytest.mark.parametrize(
    ("root", "expected"),
    [
        pytest.param(BOOKINGS_1, True, id="readme-1-valid"),
        pytest.param(BOOKINGS_2, False, id="readme-2-grandchild-breaks-the-rule"),
        pytest.param(BOOKINGS_3, False, id="readme-3-equal-ids"),
        pytest.param(TreeNode(42), True, id="readme-4-one-node"),
        pytest.param(None, True, id="readme-5-empty-tree"),
        pytest.param(TreeNode(10, TreeNode(15)), False, id="left-child-too-large"),
        pytest.param(
            TreeNode(50, TreeNode(30), TreeNode(70, TreeNode(45), TreeNode(80))),
            False,
            id="right-subtree-holds-a-smaller-id",
        ),
        pytest.param(right_chain(300), True, id="chain-of-300"),
        pytest.param(balanced_bst(1, 1023), True, id="larger-1023-nodes-valid"),
        pytest.param(bst_with_one_bad_id(), False, id="larger-1023-nodes-one-bad-id"),
    ],
)
def test_is_valid_bst(root, expected):
    assert is_valid_bst(root) is expected
