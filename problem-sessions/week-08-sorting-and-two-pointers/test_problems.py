"""Tests for the week 8 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import best_pair_total, departure_order

# 1,440 trains, one for each minute of the day, given latest first.
ALL_DAY = [(f"{10000 + minute}", f"{minute // 60:02d}:{minute % 60:02d}", 50000) for minute in range(1440)]
ALL_DAY_LATEST_FIRST = ALL_DAY[::-1]
ALL_DAY_NUMBERS = [number for number, _departs, _fare in ALL_DAY]

# 2,000 prices: 100, 200, 300 and so on up to 200000 paise.
# Every total is a multiple of 100, so the best total under 250050 is 250000.
MANY_PRICES = [100 * k for k in range(1, 2001)]


@pytest.mark.parametrize(
    ("trains", "expected"),
    [
        pytest.param(
            [("12951", "16:35", 345000), ("12009", "06:20", 128500), ("22209", "16:35", 298000)],
            ["12009", "22209", "12951"],
            id="readme-1-same-time-cheaper-first",
        ),
        pytest.param(
            [("11007", "05:10", 41000), ("11009", "05:10", 41000)],
            ["11007", "11009"],
            id="readme-2-same-time-and-fare",
        ),
        pytest.param(
            [("12127", "23:55", 52000), ("12125", "00:05", 52000)],
            ["12125", "12127"],
            id="readme-3-midnight",
        ),
        pytest.param([], [], id="readme-4-empty-list"),
        pytest.param([("12301", "16:50", 420000)], ["12301"], id="one-train"),
        pytest.param(
            [("12801", "09:00", 90000), ("12802", "09:00", 70000), ("12803", "09:00", 80000)],
            ["12802", "12803", "12801"],
            id="same-time-three-fares",
        ),
        pytest.param(
            [("16001", "07:45", 50000), ("16003", "07:45", 50000), ("16002", "07:45", 50000)],
            ["16001", "16003", "16002"],
            id="three-equal-trains-keep-given-order",
        ),
        pytest.param(
            [("19001", "08:00", 10000), ("19002", "07:59", 99000)],
            ["19002", "19001"],
            id="time-matters-more-than-fare",
        ),
        pytest.param(ALL_DAY_LATEST_FIRST, ALL_DAY_NUMBERS, id="larger-1440-trains"),
    ],
)
def test_departure_order(trains, expected):
    assert departure_order(trains) == expected


def test_departure_order_keeps_the_list():
    trains = [("12952", "17:00", 300000), ("12010", "06:00", 120000)]
    departure_order(trains)
    assert trains == [("12952", "17:00", 300000), ("12010", "06:00", 120000)]


@pytest.mark.parametrize(
    ("prices", "budget", "expected"),
    [
        pytest.param([49900, 129900, 89900, 25000], 150000, 139800, id="readme-1"),
        pytest.param([60000, 40000, 60000], 120000, 120000, id="readme-2-same-price-twice"),
        pytest.param([90000, 80000], 150000, -1, id="readme-3-every-pair-too-dear"),
        pytest.param([], 100000, -1, id="readme-4-empty-list"),
        pytest.param([5000], 100000, -1, id="one-gift"),
        pytest.param([30000, 70000, 10000], 100000, 100000, id="exactly-the-budget"),
        pytest.param([25000, 25000, 25000, 25000], 60000, 50000, id="all-prices-equal"),
        pytest.param([40000, 90000], 80000, -1, id="no-gift-counts-twice"),
        pytest.param(MANY_PRICES, 250050, 250000, id="larger-2000-prices"),
    ],
)
def test_best_pair_total(prices, budget, expected):
    assert best_pair_total(prices, budget) == expected


def test_best_pair_total_keeps_the_list():
    prices = [30000, 10000, 20000]
    best_pair_total(prices, 45000)
    assert prices == [30000, 10000, 20000]
