"""Week 12 problem session: recursion.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def flatten(folder: list[int | list]) -> list[int]:
    """Return every amount in `folder` as one flat list, from left to right.

    A folder is a list of whole numbers and other folders, in any mix.
    Folders sit at most 50 levels deep.

    Return a new list. Do not change `folder` or any folder inside it.
    """
    raise NotImplementedError


def voucher_choices(vouchers: list[int], bill: int) -> list[list[int]]:
    """Return every choice of vouchers whose values add up to exactly `bill`.

    Use each voucher at most once, and keep each choice in the order of
    `vouchers`. Two vouchers with the same value are different vouchers.
    The choices can come in any order.

    Return [] when no choice adds up to `bill`, and for an empty list.
    Do not change `vouchers`.
    """
    raise NotImplementedError
