"""Money in paise (task 8, step 3).

Each test says what to check. Write the body, then delete its skip line.

These tests need no database.
"""

import pytest


@pytest.mark.skip(reason="TODO(task 8)")
def test_parse_rupees_adds_up_exactly():
    """parse_rupees("0.10") + parse_rupees("0.20") is exactly 30, and
    parse_rupees("1234.50") is 123450. Use @pytest.mark.parametrize for more cases."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
def test_parse_rupees_refuses_bad_text():
    """Each of "12.345", "-5" and "abc" raises ValueError."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
def test_format_paise_gives_two_decimals():
    """format_paise(123450) is "1234.50" and format_paise(5) is "0.05"."""
    raise NotImplementedError("TODO(task 8): write this test")


@pytest.mark.skip(reason="TODO(task 8)")
def test_split_paise_loses_nothing():
    """split_paise(10000, 3) is [3334, 3333, 3333], and the parts of any split
    add up to the total."""
    raise NotImplementedError("TODO(task 8): write this test")
