"""Tests for the week 18 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import fewest_hops, fewest_trains

# The map and the network in README.md.
PUNE = {
    "Kothrud": ["Deccan", "Warje"],
    "Warje": ["Kothrud"],
    "Deccan": ["Kothrud", "Shivajinagar", "Swargate"],
    "Shivajinagar": ["Deccan", "Aundh", "Koregaon Park"],
    "Aundh": ["Shivajinagar", "Baner", "Wakad"],
    "Baner": ["Aundh", "Hinjewadi"],
    "Hinjewadi": ["Baner", "Wakad"],
    "Wakad": ["Hinjewadi", "Aundh"],
    "Koregaon Park": ["Shivajinagar", "Viman Nagar", "Hadapsar"],
    "Viman Nagar": ["Koregaon Park"],
    "Hadapsar": ["Koregaon Park", "Swargate"],
    "Swargate": ["Deccan", "Hadapsar"],
    "Lohegaon": [],
}

NETWORK = {
    "91001": ["CSMT", "DR", "TNA", "KYN", "PUNE"],
    "91002": ["PUNE", "DD", "SUR"],
    "91003": ["KYN", "NK", "BSL"],
    "91004": ["BSL", "AK", "NGP"],
    "91005": ["BCT", "ST", "BRC", "ADI"],
}


def grid_map(size: int) -> dict[str, list[str]]:
    """A square of size x size areas. Each area borders the areas above, below, left and right."""
    areas: dict[str, list[str]] = {}
    for row in range(size):
        for col in range(size):
            borders = []
            for r, c in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                if 0 <= r < size and 0 <= c < size:
                    borders.append(f"R{r}C{c}")
            areas[f"R{row}C{col}"] = borders
    return areas


def code(number: int) -> str:
    """Turn a number into a 3-letter station code: 0 is AAA, 1 is AAB, 26 is ABA."""
    letters = ""
    for _ in range(3):
        letters = chr(ord("A") + number % 26) + letters
        number //= 26
    return letters


def chain_network() -> dict[str, list[str]]:
    """200 trains in a line. Train k stops at stations 10k to 10k + 10, so each train meets the next.

    One express train joins station 0 to station 1000. From station 1000, trains 100 to 199 remain.
    """
    trains = {str(70000 + k): [code(10 * k + i) for i in range(11)] for k in range(200)}
    trains["12000"] = [code(0), code(1000)]
    return trains


@pytest.mark.parametrize(
    ("neighbours", "start", "end", "expected"),
    [
        pytest.param(PUNE, "Kothrud", "Baner", 4, id="readme-1"),
        pytest.param(PUNE, "Deccan", "Hadapsar", 2, id="readme-2-two-routes"),
        pytest.param(PUNE, "Wakad", "Wakad", 0, id="readme-3-same-area"),
        pytest.param(PUNE, "Baner", "Lohegaon", -1, id="readme-4-no-route"),
        pytest.param({}, "Baner", "Aundh", -1, id="readme-5-empty-map"),
        pytest.param({"Baner": []}, "Baner", "Baner", 0, id="one-area"),
        pytest.param({"Aundh": ["Baner"], "Baner": ["Aundh"]}, "Aundh", "Baner", 1, id="two-areas"),
        pytest.param(PUNE, "Hadapsar", "Kothrud", 3, id="other-direction"),
        pytest.param(PUNE, "Viman Nagar", "Hinjewadi", 5, id="loop-in-the-map"),
        pytest.param(grid_map(40), "R0C0", "R39C39", 78, id="larger-1600-areas"),
    ],
)
def test_fewest_hops(neighbours, start, end, expected):
    assert fewest_hops(neighbours, start, end) == expected


@pytest.mark.parametrize(
    ("trains", "start", "end", "expected"),
    [
        pytest.param(NETWORK, "CSMT", "PUNE", 1, id="readme-1-one-train"),
        pytest.param(NETWORK, "TNA", "SUR", 2, id="readme-2-two-trains"),
        pytest.param(NETWORK, "DR", "NGP", 3, id="readme-3-three-trains"),
        pytest.param(NETWORK, "CSMT", "ADI", -1, id="readme-4-no-journey"),
        pytest.param(NETWORK, "PUNE", "PUNE", 0, id="readme-5-same-station"),
        pytest.param({}, "PUNE", "CSMT", -1, id="readme-6-no-trains"),
        pytest.param({"91010": ["NDLS", "AGC"]}, "NDLS", "AGC", 1, id="one-train"),
        pytest.param(NETWORK, "SUR", "CSMT", 2, id="other-direction"),
        pytest.param(
            {
                "91020": ["NDLS", "GZB", "ALJN", "TDL", "AGC"],
                "91021": ["NDLS", "TDL"],
                "91022": ["TDL", "AGC"],
            },
            "NDLS",
            "AGC",
            1,
            id="one-slow-train-beats-two-fast-ones",
        ),
        pytest.param(chain_network(), code(0), code(2000), 101, id="larger-201-trains"),
    ],
)
def test_fewest_trains(trains, start, end, expected):
    assert fewest_trains(trains, start, end) == expected
