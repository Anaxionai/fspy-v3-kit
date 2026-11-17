"""Week 20 problem session: intervals that overlap.

Write your solutions in this file. Use the standard library only.
Run the tests with: uv run --with pytest pytest -q
"""


def can_do_all(windows: list[tuple[int, int]]) -> bool:
    """Return True when no two delivery windows overlap.

    Each window is (start, end) in minutes after midnight. Two windows
    overlap when one starts before the other ends. Touching windows, where
    one ends at the minute the next starts, do not overlap.

    Return True when `windows` is empty. Do not change `windows`.
    """
    raise NotImplementedError


def held_periods(holds: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return the periods when at least one seat was on hold.

    Each hold is (start, end) in minutes after midnight, in any order. Join
    holds that overlap or touch. Return the periods as tuples, sorted by
    start.

    Return [] when `holds` is empty. Do not change `holds`.
    """
    raise NotImplementedError
