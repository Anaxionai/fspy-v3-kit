"""Tests for the week 14 problem session.

Run them in this folder with: uv run --with pytest pytest -q

Each test replays a list of steps on one cache. A step is either
("put", code, url) or ("get", code). The test compares what every
`get` returned with the expected list.
"""

import pytest

from problems import LeastRecentCache, OldestFirstCache

DELHI = "https://example.com/delhi"
DELHI_NEW = "https://example.com/delhi-new"
MUMBAI = "https://example.com/mumbai"
MUMBAI_NEW = "https://example.com/mumbai-new"
CHENNAI = "https://example.com/chennai"
KOLKATA = "https://example.com/kolkata"


def link(code: str) -> str:
    return f"https://example.com/{code}"


def replay(cache, steps: list[tuple]) -> list[str | None]:
    """Run each step on `cache` and return what every `get` returned."""
    answers = []
    for step in steps:
        if step[0] == "put":
            cache.put(step[1], step[2])
        else:
            answers.append(cache.get(step[1]))
    return answers


# 1,005 steps on a cache with room for 500 links. After 1,000 puts it holds
# c500 to c999. Then c500 is read, and one more link arrives.
MANY_LINKS = [("put", f"c{n}", link(f"c{n}")) for n in range(1000)] + [
    ("get", "c499"),
    ("get", "c500"),
    ("put", "c1000", link("c1000")),
    ("get", "c500"),
    ("get", "c501"),
]

README_OLDEST_FIRST = [
    ("get", "dl7"),
    ("put", "dl7", DELHI),
    ("put", "mb2", MUMBAI),
    ("get", "dl7"),
    ("put", "ch9", CHENNAI),
    ("get", "dl7"),
    ("put", "mb2", MUMBAI_NEW),
    ("put", "kl5", KOLKATA),
    ("get", "mb2"),
    ("get", "ch9"),
]

README_LEAST_RECENT = [
    ("get", "dl7"),
    ("put", "dl7", DELHI),
    ("put", "mb2", MUMBAI),
    ("get", "dl7"),
    ("put", "ch9", CHENNAI),
    ("get", "mb2"),
    ("put", "dl7", DELHI_NEW),
    ("put", "kl5", KOLKATA),
    ("get", "ch9"),
    ("get", "dl7"),
]

# The same steps give different answers in the two caches.
GET_THEN_FULL = [
    ("put", "a1", link("a1")),
    ("put", "b2", link("b2")),
    ("get", "a1"),
    ("put", "c3", link("c3")),
    ("get", "a1"),
    ("get", "b2"),
    ("get", "c3"),
]


@pytest.mark.parametrize(
    ("capacity", "steps", "expected"),
    [
        pytest.param(
            2, README_OLDEST_FIRST, [None, DELHI, None, None, CHENNAI], id="readme-scenario"
        ),
        pytest.param(3, [("get", "dl7")], [None], id="empty-cache"),
        pytest.param(
            1,
            [("put", "a1", link("a1")), ("put", "b2", link("b2")), ("get", "a1"), ("get", "b2")],
            [None, link("b2")],
            id="room-for-one-link",
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("get", "a1"),
                ("get", "b2"),
            ],
            [link("a1"), link("b2")],
            id="same-put-twice-takes-one-place",
        ),
        pytest.param(
            2, GET_THEN_FULL, [link("a1"), None, link("b2"), link("c3")], id="get-does-not-refresh"
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("put", "a1", "https://example.com/changed"),
                ("put", "c3", link("c3")),
                ("get", "a1"),
                ("get", "b2"),
            ],
            [None, link("b2")],
            id="changed-url-keeps-its-age",
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("get", "zz"),
                ("put", "c3", link("c3")),
                ("get", "a1"),
                ("get", "b2"),
                ("get", "c3"),
            ],
            [None, None, link("b2"), link("c3")],
            id="miss-changes-nothing",
        ),
        pytest.param(
            3,
            [("put", code, link(code)) for code in ["a1", "b2", "c3", "d4", "e5"]]
            + [("get", code) for code in ["a1", "b2", "c3", "d4", "e5"]],
            [None, None, link("c3"), link("d4"), link("e5")],
            id="oldest-leave-in-order",
        ),
        pytest.param(
            500, MANY_LINKS, [None, link("c500"), None, link("c501")], id="larger-1005-steps"
        ),
    ],
)
def test_oldest_first_cache(capacity, steps, expected):
    assert replay(OldestFirstCache(capacity), steps) == expected


@pytest.mark.parametrize(
    ("capacity", "steps", "expected"),
    [
        pytest.param(
            2, README_LEAST_RECENT, [None, DELHI, None, None, DELHI_NEW], id="readme-scenario"
        ),
        pytest.param(3, [("get", "dl7")], [None], id="empty-cache"),
        pytest.param(
            1,
            [("put", "a1", link("a1")), ("put", "b2", link("b2")), ("get", "a1"), ("get", "b2")],
            [None, link("b2")],
            id="room-for-one-link",
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("get", "a1"),
                ("get", "a1"),
                ("get", "a1"),
                ("put", "c3", link("c3")),
                ("get", "b2"),
                ("get", "a1"),
                ("get", "c3"),
            ],
            [link("a1"), link("a1"), link("a1"), None, link("a1"), link("c3")],
            id="same-get-three-times",
        ),
        pytest.param(
            2, GET_THEN_FULL, [link("a1"), link("a1"), None, link("c3")], id="get-is-a-use"
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("put", "a1", "https://example.com/changed"),
                ("put", "c3", link("c3")),
                ("get", "b2"),
                ("get", "a1"),
            ],
            [None, "https://example.com/changed"],
            id="changed-url-is-a-use",
        ),
        pytest.param(
            2,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("get", "zz"),
                ("put", "c3", link("c3")),
                ("get", "a1"),
                ("get", "b2"),
            ],
            [None, None, link("b2")],
            id="miss-changes-nothing",
        ),
        pytest.param(
            3,
            [
                ("put", "a1", link("a1")),
                ("put", "b2", link("b2")),
                ("put", "c3", link("c3")),
                ("get", "a1"),
                ("get", "b2"),
                ("put", "d4", link("d4")),
                ("get", "c3"),
                ("get", "a1"),
                ("put", "e5", link("e5")),
                ("get", "b2"),
                ("get", "d4"),
            ],
            [link("a1"), link("b2"), None, link("a1"), None, link("d4")],
            id="longer-mix",
        ),
        pytest.param(
            500, MANY_LINKS, [None, link("c500"), link("c500"), None], id="larger-1005-steps"
        ),
    ],
)
def test_least_recent_cache(capacity, steps, expected):
    assert replay(LeastRecentCache(capacity), steps) == expected
