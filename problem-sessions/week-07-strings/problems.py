"""Week 7 problem session: walking a string and normalising text.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def is_palindrome(label: str) -> bool:
    """Return True when `label` reads the same forwards and backwards.

    Compare letters and digits only, and ignore every other character.
    A capital letter and its small letter count as the same.
    Return True when the label has no letters or digits, including "".
    """
    raise NotImplementedError


def look_alike_groups(codes: list[str]) -> list[list[str]]:
    """Return the groups of codes that are anagrams of each other.

    Two codes look alike when they hold the same characters, each the same
    number of times, in any order. Capital and small letters count as the
    same character. Keep each code exactly as it was written.

    Return only groups with two or more codes. Order the groups by their
    first code in `codes`, and keep the order of `codes` inside each group.
    Return [] when no codes look alike. Do not change `codes`.
    """
    raise NotImplementedError
