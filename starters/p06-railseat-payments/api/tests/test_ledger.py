"""The double-entry ledger (task 12, step 10).

Each test says what to check. Write the body, then delete its skip line.
"""

import pytest

pytestmark = pytest.mark.anyio


@pytest.mark.skip(reason="TODO(task 12)")
async def test_a_capture_adds_two_rows_that_sum_to_zero(client):
    """After a signed capture, the rows with txn_key capture:<payment id> are two:
    +amount on mockpay_clearing, -amount on ticket_sales."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_an_unknown_account_raises(client):
    """post(..., debit="cash", ...) raises ValueError, and so does an amount of 0."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_a_negative_payout_posts_the_other_way(client):
    """A report with net_payout_paise -5000 debits mockpay_clearing and credits bank
    with 5000."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
async def test_importing_one_day_twice_adds_no_rows(client):
    """Import the same day twice (fake report): the second run posts nothing."""
    raise NotImplementedError("TODO(task 12): write this test")
