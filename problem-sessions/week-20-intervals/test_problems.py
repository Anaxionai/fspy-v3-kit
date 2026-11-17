"""Tests for the week 20 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import can_do_all, held_periods

# 1,440 one-minute windows, one for every minute of the day, listed from the last minute to the first.
EVERY_MINUTE = [(minute, minute + 1) for minute in range(1439, -1, -1)]

# The same 1,440 windows, plus one 2-minute window that overlaps two of them.
EVERY_MINUTE_PLUS_ONE = EVERY_MINUTE + [(700, 702)]

# 3,000 holds in 12 blocks. Block b covers minutes 120b to 120b + 58, and the blocks are mixed together.
TWELVE_BLOCKS = [(120 * b + j % 50, 120 * b + j % 50 + 9) for j in range(250) for b in range(12)]
TWELVE_PERIODS = [(120 * b, 120 * b + 58) for b in range(12)]


@pytest.mark.parametrize(
    ("windows", "expected"),
    [
        pytest.param([(720, 750), (780, 810), (750, 770)], True, id="readme-1-touching-is-fine"),
        pytest.param([(1140, 1170), (1080, 1150)], False, id="readme-2-overlap"),
        pytest.param([(600, 660), (610, 620)], False, id="readme-3-one-inside-another"),
        pytest.param([], True, id="readme-4-empty-list"),
        pytest.param([(480, 510)], True, id="one-window"),
        pytest.param([(480, 510), (480, 510)], False, id="same-window-twice"),
        pytest.param([(800, 830), (740, 770), (770, 800)], True, id="touching-chain-out-of-order"),
        pytest.param([(900, 960), (600, 660), (950, 1000)], False, id="overlap-far-apart-in-the-list"),
        pytest.param(EVERY_MINUTE, True, id="larger-1440-windows"),
        pytest.param(EVERY_MINUTE_PLUS_ONE, False, id="larger-1441-windows-one-overlap"),
    ],
)
def test_can_do_all(windows, expected):
    before = list(windows)
    assert can_do_all(windows) is expected
    assert windows == before, "Do not change the list `windows`."


@pytest.mark.parametrize(
    ("holds", "expected"),
    [
        pytest.param([(600, 610), (605, 615), (630, 640)], [(600, 615), (630, 640)], id="readme-1"),
        pytest.param([(700, 710), (600, 620), (610, 650)], [(600, 650), (700, 710)], id="readme-2-out-of-order"),
        pytest.param([(600, 610), (610, 620)], [(600, 620)], id="readme-3-touching-holds-join"),
        pytest.param([(500, 600), (520, 530)], [(500, 600)], id="readme-4-one-inside-another"),
        pytest.param([], [], id="readme-5-empty-list"),
        pytest.param([(600, 610)], [(600, 610)], id="one-hold"),
        pytest.param([(610, 620), (600, 700), (650, 660)], [(600, 700)], id="one-long-hold-covers-all"),
        pytest.param([(600, 650), (610, 620), (640, 700)], [(600, 700)], id="short-hold-inside-then-overlap"),
        pytest.param([(0, 1), (1439, 1440)], [(0, 1), (1439, 1440)], id="first-and-last-minute"),
        pytest.param(TWELVE_BLOCKS, TWELVE_PERIODS, id="larger-3000-holds"),
    ],
)
def test_held_periods(holds, expected):
    before = list(holds)
    assert held_periods(holds) == expected
    assert holds == before, "Do not change the list `holds`."
