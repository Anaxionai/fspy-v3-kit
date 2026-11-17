"""Tests for the week 16 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import TreeNode, longest_chain, tour_for_budget


def chain(length: int) -> TreeNode | None:
    """Build a chain of `length` nodes. Each node has one right child."""
    root = None
    for value in range(length, 0, -1):
        root = TreeNode(value, None, root)
    return root


def full_tree(levels: int, value: int, left_value: int, right_value: int) -> TreeNode | None:
    """Build a tree with every level full. Left children hold `left_value`, right children `right_value`."""
    if levels == 0:
        return None
    return TreeNode(
        value,
        full_tree(levels - 1, left_value, left_value, right_value),
        full_tree(levels - 1, right_value, left_value, right_value),
    )


def full_tree_with_tail() -> TreeNode | None:
    """A full tree of 9 levels (511 nodes). A chain of 40 more nodes hangs from its leftmost leaf."""
    root = full_tree(9, 1, 2, 3)
    node = root
    while node.left is not None:
        node = node.left
    node.left = chain(40)
    return root


# The two trees drawn in README.md.
INVITES_1 = TreeNode(1, TreeNode(2, TreeNode(4)), TreeNode(3))
INVITES_2 = TreeNode(10, None, TreeNode(20, None, TreeNode(30, None, TreeNode(40))))

TOUR_1 = TreeNode(
    900,
    TreeNode(1200, TreeNode(800), TreeNode(1500)),
    TreeNode(700, None, TreeNode(1600)),
)
TOUR_2 = TreeNode(
    500,
    TreeNode(400, None, TreeNode(600)),
    TreeNode(600, None, TreeNode(400)),
)

# 10 levels, 1,023 nodes. The root and every left child cost 100; every right child costs 200.
# Each complete tour costs 1000 plus 100 for each right turn.
BIG_TOUR = full_tree(10, 100, 100, 200)


@pytest.mark.parametrize(
    ("root", "expected"),
    [
        pytest.param(INVITES_1, 3, id="readme-1"),
        pytest.param(INVITES_2, 4, id="readme-2-one-long-chain"),
        pytest.param(TreeNode(5), 1, id="readme-3-one-node"),
        pytest.param(None, 0, id="readme-4-empty-tree"),
        pytest.param(TreeNode(1, TreeNode(2), TreeNode(3)), 2, id="root-with-two-leaves"),
        pytest.param(
            TreeNode(1, TreeNode(2), TreeNode(3, None, TreeNode(4, TreeNode(5)))),
            4,
            id="longest-chain-on-the-right",
        ),
        pytest.param(chain(450), 450, id="chain-of-450"),
        pytest.param(full_tree_with_tail(), 49, id="larger-551-nodes"),
    ],
)
def test_longest_chain(root, expected):
    assert longest_chain(root) == expected


@pytest.mark.parametrize(
    ("root", "budget", "expected"),
    [
        pytest.param(TOUR_1, 3600, [900, 1200, 1500], id="readme-1"),
        pytest.param(TOUR_1, 3200, [900, 700, 1600], id="readme-2-goes-right"),
        pytest.param(TOUR_1, 2100, [], id="readme-3-stops-before-a-leaf"),
        pytest.param(TOUR_2, 1500, [500, 400, 600], id="readme-4-two-tours-match"),
        pytest.param(None, 1000, [], id="readme-5-empty-tree"),
        pytest.param(TOUR_1, 2900, [900, 1200, 800], id="leftmost-leaf"),
        pytest.param(TreeNode(750), 750, [750], id="one-node-matches"),
        pytest.param(TreeNode(750), 700, [], id="one-node-does-not-match"),
        pytest.param(BIG_TOUR, 1300, [100] * 7 + [200] * 3, id="larger-three-right-turns"),
        pytest.param(BIG_TOUR, 1950, [], id="larger-no-match"),
    ],
)
def test_tour_for_budget(root, budget, expected):
    assert tour_for_budget(root, budget) == expected
