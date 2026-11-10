"""Finding subscriptions: payments that repeat about once a month."""

from paisalens.models import Subscription


def is_monthly(gaps: list[int]) -> bool:
    """Return True when every gap, in days, is between 25 and 35.

    Months differ in length and the payment day moves a little, so the rule
    allows a window around 30 days. One gap outside it gives False.
    """
    raise NotImplementedError("TODO(task 20): write is_monthly")


def find_recurring(transactions) -> list[Subscription]:
    """Return one Subscription for each merchant that is paid every month.

    Only debits count. A merchant needs at least 3 payments, and the gaps
    between neighbouring payments (in days) must pass is_monthly.
    Each Subscription holds the last amount, the average gap, the number of
    payments, the last date, and the next date: the last date plus the
    average gap.
    """
    raise NotImplementedError("TODO(task 20): write find_recurring")
