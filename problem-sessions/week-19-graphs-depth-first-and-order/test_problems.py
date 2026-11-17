"""Tests for the week 19 problem session.

Run them in this folder with: uv run --with pytest pytest -q
"""

import pytest

from problems import count_groups, run_order

# 500 friends. Friend k shares a bill with friend k + 7, so the friends split into 7 groups.
MANY_FRIENDS = [f"F{k:03}" for k in range(500)]
SEVEN_GROUPS = [(f"F{k:03}", f"F{k + 7:03}") for k in range(493)]
ONE_LINE = [(f"F{k:03}", f"F{k + 1:03}") for k in range(499)]

# The pipeline in README.md.
PIPELINE = {
    "install": [],
    "lint": ["install"],
    "unit-tests": ["install"],
    "build-image": ["lint", "unit-tests"],
    "deploy": ["build-image"],
}

# A ReelPipe pipeline with two paths that meet again.
REELPIPE = {
    "checkout": [],
    "install": ["checkout"],
    "lint": ["install"],
    "typecheck": ["install"],
    "unit-tests": ["install"],
    "build-worker": ["lint", "typecheck", "unit-tests"],
    "build-api": ["lint", "typecheck", "unit-tests"],
    "deploy": ["build-worker", "build-api"],
}


def long_pipeline(with_cycle: bool) -> dict[str, list[str]]:
    """500 jobs, listed from job499 down to job000. Job k needs job k - 1 and job k // 3.

    The chain from job499 down to job000 is 500 jobs long.
    With `with_cycle`, job000 needs job499, which closes a loop.
    """
    needs: dict[str, list[str]] = {}
    for k in range(499, 0, -1):
        needs[f"job{k:03}"] = list(dict.fromkeys([f"job{k - 1:03}", f"job{k // 3:03}"]))
    needs["job000"] = ["job499"] if with_cycle else []
    return needs


def assert_keeps_the_rules(needs: dict[str, list[str]], order: list[str]) -> None:
    assert sorted(order) == sorted(needs), "Return each job exactly once."
    position = {job: index for index, job in enumerate(order)}
    for job, needed in needs.items():
        for first in needed:
            assert position[first] < position[job], f"{first!r} must come before {job!r}."


@pytest.mark.parametrize(
    ("friends", "shared", "expected"),
    [
        pytest.param(
            ["Asha", "Ravi", "Meera", "John", "Zoya"],
            [("Asha", "Ravi"), ("Ravi", "Meera"), ("John", "Zoya")],
            2,
            id="readme-1",
        ),
        pytest.param(["Asha", "Ravi", "Meera"], [], 3, id="readme-2-no-bills"),
        pytest.param(
            ["Asha", "Ravi", "Meera", "John"],
            [("Asha", "John"), ("Meera", "Ravi"), ("John", "Meera")],
            1,
            id="readme-3-one-chain",
        ),
        pytest.param([], [], 0, id="readme-4-no-friends"),
        pytest.param(["Kiran"], [], 1, id="one-friend"),
        pytest.param(
            ["Asha", "Ravi", "Meera"],
            [("Asha", "Ravi"), ("Ravi", "Asha"), ("Asha", "Ravi")],
            2,
            id="same-pair-three-times",
        ),
        pytest.param(MANY_FRIENDS, ONE_LINE, 1, id="larger-one-line-of-500"),
        pytest.param(MANY_FRIENDS, SEVEN_GROUPS, 7, id="larger-500-friends-7-groups"),
    ],
)
def test_count_groups(friends, shared, expected):
    assert count_groups(friends, shared) == expected


@pytest.mark.parametrize(
    "needs",
    [
        pytest.param(PIPELINE, id="readme-1"),
        pytest.param({"lint": []}, id="readme-4-one-job"),
        pytest.param({}, id="readme-5-no-jobs"),
        pytest.param({"lint": [], "docs": [], "typecheck": []}, id="jobs-that-wait-for-nothing"),
        pytest.param(REELPIPE, id="paths-that-meet-again"),
        pytest.param(long_pipeline(with_cycle=False), id="larger-500-jobs"),
    ],
)
def test_run_order_keeps_the_rules(needs):
    assert_keeps_the_rules(needs, run_order(needs))


@pytest.mark.parametrize(
    "needs",
    [
        pytest.param({"migrate": ["build"], "build": ["migrate"]}, id="readme-2-two-jobs-wait-for-each-other"),
        pytest.param({"deploy": ["deploy"]}, id="readme-3-job-needs-itself"),
        pytest.param(
            {
                "install": [],
                "lint": ["install"],
                "build": ["lint", "package"],
                "package": ["sign"],
                "sign": ["build"],
            },
            id="loop-of-three-after-good-jobs",
        ),
        pytest.param(long_pipeline(with_cycle=True), id="larger-500-jobs-with-a-loop"),
    ],
)
def test_run_order_finds_a_cycle(needs):
    with pytest.raises(ValueError):
        run_order(needs)
