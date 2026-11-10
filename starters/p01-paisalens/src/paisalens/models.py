"""The data PaisaLens works with, as dataclasses.

Both classes are empty in the starter. You give them their fields in
task 18 (Transaction) and task 20 (Subscription).
"""

from dataclasses import dataclass


@dataclass
class Transaction:
    """One good row of the statement, with named and typed fields."""

    # TODO(task 18): add the eight fields, in this order: the date (a
    #   datetime.date), the narration and the upi_ref (text), the debit, credit
    #   and balance in paise (whole numbers), then merchant and category (text,
    #   with an empty default). Fields with a default must come last.


@dataclass
class Subscription:
    """A payment that repeats about once a month, as find_recurring finds it."""

    # TODO(task 20): add the fields merchant (text), amount_paise, every_days
    #   and count (whole numbers), and last_date and next_date (datetime.date).
