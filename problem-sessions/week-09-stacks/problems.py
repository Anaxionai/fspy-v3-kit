"""Week 9 problem session: stacks.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def brackets_match(rule: str) -> bool:
    """Return True when every bracket in `rule` is matched correctly.

    The brackets are (), [] and {}. Ignore every other character. Every
    opening bracket needs a closing bracket of the same kind, later in the
    text. A pair that opens inside another pair must also close inside it.

    Return True when the rule has no brackets, including "".
    """
    raise NotImplementedError


def overs_until_bigger(runs: list[int]) -> list[int]:
    """For each over, return how many overs later a bigger over comes.

    `runs` holds the runs scored in each over, in order. A bigger over has
    more runs, not the same number. Use 0 for an over that no later over
    beats.

    Return a list of the same length as `runs`. Return [] for an empty list.
    Do not change `runs`.
    """
    raise NotImplementedError
