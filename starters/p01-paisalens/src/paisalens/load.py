"""Reading the statement CSV into Python.

The columns are date, narration, upi_ref, debit, credit and balance. The kit's
data/upi/README.md explains each one, and what is messy on purpose.
"""

# Transaction is the dataclass you write in task 18. Until then it is empty.
from paisalens.models import Transaction


def to_paise(text: str) -> int:
    """Turn rupee text from the statement into whole paise.

    "119.00" gives 11900 and "64400.00" gives 6440000.
    An empty amount, "", gives 0: a debit row has an empty credit.
    Use whole numbers only. Never use float: it cannot hold every paisa exactly.
    """
    raise NotImplementedError("TODO(task 6): write to_paise")


def is_broken(row: dict) -> bool:
    """Say whether a row from csv.DictReader is broken and must be skipped.

    True when debit and credit are both empty, or when an amount is not a
    number, such as "Rs.855/-". One empty amount is normal.
    False for a good row.
    """
    # TODO(task 18): also return True for a date that cannot exist, such as
    #   31/09/2026: try to read it with strptime and catch the ValueError.
    # TODO(task 21): delete is_broken. parse_row raises BadRow instead.
    raise NotImplementedError("TODO(task 6): write is_broken")


def read_statement(path: str) -> list[dict]:
    """Read the statement CSV at `path` and return its good rows.

    Each good row is the dict from csv.DictReader, with three integer amounts
    added from to_paise: debit_paise, credit_paise and balance_paise.
    A broken row is not kept and does not stop the program: print
    "Skipping line N:" and the row, where N is its line number in the file.
    The header is line 1, so the first row is line 2.
    """
    # TODO(task 7): give each good row row["merchant"] from clean_merchant, and
    #   skip a row whose upi_ref you have already kept (keep them in a set).
    #   An empty upi_ref, as on a salary row, is never a repeat.
    # TODO(task 18): return a list of Transaction objects, one from parse_row
    #   for each good row.
    # TODO(task 21): change the signature to read_statement(path, report). Send
    #   every row to parse_row, catch BadRow, and record each bad row with
    #   report.add(line, reason, row). A repeat gets the reason "duplicate upi_ref".
    raise NotImplementedError("TODO(task 6): write read_statement")


def parse_row(row: dict) -> Transaction:
    """Turn one row from csv.DictReader into a Transaction.

    The date text, such as "21/09/2026" (day/month/year), becomes a
    datetime.date. The amounts become integer paise with to_paise, and the
    merchant comes from clean_merchant.
    """
    # TODO(task 21): for a bad row, raise BadRow with a clear reason instead:
    #   "bad date '31/09/2026'", "no amount" or "bad amount 'Rs.855/-'".
    #   Catch each ValueError and raise BadRow in its place.
    raise NotImplementedError("TODO(task 18): write parse_row")
