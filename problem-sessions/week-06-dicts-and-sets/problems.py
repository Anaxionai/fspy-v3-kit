"""Week 6 problem session: counting and fast lookup with a dict or set.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def first_repeat(pnrs: list[str]) -> str:
    """Return the PNR of the earliest request that repeats an earlier request.

    `pnrs` holds the PNR of each booking request, in the order they arrive.
    Return "" when no PNR repeats. An empty list returns "".
    Do not change `pnrs`.
    """
    raise NotImplementedError


def matching_pair(spends: list[int], payment: int) -> tuple[int, int]:
    """Return the positions of the two spends that add up to `payment`.

    `spends` holds amounts in paise. Return the positions as a tuple, smaller
    position first. The two spends must be at different positions. At most
    one pair adds up to `payment`.

    Return (-1, -1) when no pair adds up to `payment`, or when the list has
    fewer than two items. Do not change `spends`.
    """
    raise NotImplementedError
