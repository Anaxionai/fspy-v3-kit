"""Fares and the cancellation fee (P6 add-on). Flat fares by coach class, in paise."""

# The classes match the kit's seed data (coaches.csv): SL, 3A, 2A, 1A and CC.
FARES_PAISE = {"SL": 45000, "3A": 120000, "2A": 175000, "1A": 295000, "CC": 95000}

CANCELLATION_FEE_PERCENT = 25


def fare_for(coach_class: str) -> int:
    """The fare in paise for a coach class, from FARES_PAISE (task 8, step 4).

    An unknown class raises ValueError: never invent a price.
    """
    raise NotImplementedError("TODO(task 8): look the fare up")


def refund_split(fare_paise: int) -> tuple[int, int]:
    """Return `(refund_paise, fee_paise)` for a cancelled, paid booking (task 13, step 4).

    The fee is CANCELLATION_FEE_PERCENT of the fare in whole paise, rounded down,
    and refund plus fee equals the fare. For 120000 the fee is 30000 and the
    refund 90000.
    """
    raise NotImplementedError(
        "TODO(task 13): work out the fee and the refund in integer paise"
    )
