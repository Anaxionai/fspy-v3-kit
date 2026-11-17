"""Tests for the week 13 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

from itertools import product
from string import ascii_uppercase

import pytest

from problems import Node, loop_start, reverse_route

# 2,000 made-up station codes of 4 capital letters: SAAA, SAAB, SAAC and so on.
MANY_STATIONS = ["S" + "".join(trio) for trio in product(ascii_uppercase, repeat=3)][:2000]


def make_nodes(values: list[str], loop_to: int | None = None) -> list[Node]:
    """Build a route and return its nodes in order.

    When `loop_to` is a position, the last stop points back to that stop.
    """
    nodes = [Node(value) for value in values]
    for here, after in zip(nodes, nodes[1:]):
        here.next = after
    if nodes and loop_to is not None:
        nodes[-1].next = nodes[loop_to]
    return nodes


def first_of(nodes: list[Node]) -> Node | None:
    return nodes[0] if nodes else None


def values_of(head: Node | None) -> list[str]:
    """Walk a route that ends and return its station codes."""
    values = []
    while head is not None and len(values) <= 20_000:
        values.append(head.value)
        head = head.next
    return values


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        pytest.param(
            ["NDLS", "AGC", "GWL", "BPL"], ["BPL", "GWL", "AGC", "NDLS"], id="readme-1"
        ),
        pytest.param(["MAS", "SBC"], ["SBC", "MAS"], id="readme-2-two-stops"),
        pytest.param(["PUNE"], ["PUNE"], id="readme-3-one-stop"),
        pytest.param([], [], id="readme-4-empty-route"),
        pytest.param(["ADI", "BRC", "ADI"], ["ADI", "BRC", "ADI"], id="same-code-twice"),
        pytest.param(["HWH", "DHN", "GAYA"], ["GAYA", "DHN", "HWH"], id="three-stops"),
        pytest.param(MANY_STATIONS, MANY_STATIONS[::-1], id="larger-2000-stops"),
    ],
)
def test_reverse_route(values, expected):
    result = reverse_route(first_of(make_nodes(values)))
    assert values_of(result) == expected


def test_reverse_route_reuses_the_nodes():
    nodes = make_nodes(["NDLS", "AGC", "BPL"])
    result = reverse_route(nodes[0])
    assert result is nodes[2]
    assert nodes[2].next is nodes[1]
    assert nodes[1].next is nodes[0]
    assert nodes[0].next is None


@pytest.mark.parametrize(
    ("values", "loop_to", "expected"),
    [
        pytest.param(["NDLS", "AGC", "GWL", "BPL"], 1, 1, id="readme-1"),
        pytest.param(["MAS", "SBC"], 0, 0, id="readme-2-whole-route-loops"),
        pytest.param(["ADI", "BRC", "ADI", "BCT"], None, -1, id="readme-3-same-code-no-loop"),
        pytest.param([], None, -1, id="readme-4-empty-route"),
        pytest.param(["PUNE"], None, -1, id="one-stop-no-loop"),
        pytest.param(["PUNE"], 0, 0, id="one-stop-points-to-itself"),
        pytest.param(["NDLS", "AGC", "GWL"], 2, 2, id="last-stop-points-to-itself"),
        pytest.param(["ADI", "BRC", "ADI", "BCT"], 2, 2, id="same-code-before-the-loop"),
        pytest.param(MANY_STATIONS, 1000, 1000, id="larger-2000-stops"),
    ],
)
def test_loop_start(values, loop_to, expected):
    assert loop_start(first_of(make_nodes(values, loop_to))) == expected


def test_loop_start_keeps_the_route():
    nodes = make_nodes(["NDLS", "AGC", "GWL", "BPL"], loop_to=1)
    loop_start(nodes[0])
    assert nodes[0].next is nodes[1]
    assert nodes[1].next is nodes[2]
    assert nodes[2].next is nodes[3]
    assert nodes[3].next is nodes[1]
