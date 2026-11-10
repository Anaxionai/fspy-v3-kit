"""The PaisaLens command line: import, report and export.

Typer is installed with the starter. Until task 22 the `paisalens` command
still runs main() in __init__.py; task 22 points it at `app` below.
"""

import typer

from paisalens.errors import ErrorReport
from paisalens.models import Transaction

app = typer.Typer()


def load_all(statement: str) -> tuple[list[Transaction], ErrorReport]:
    """Read, clean and categorise the statement at the path `statement`.

    Return the good transactions, each with its merchant and category, and the
    ErrorReport that holds the bad rows. Call your existing functions here;
    do not copy their code. If the file does not exist, print a clear message
    and exit with code 1 (typer.Exit), not a traceback.
    """
    raise NotImplementedError("TODO(task 22): write load_all")


# TODO(task 22): add the three commands below, each taking the statement path
#   as an argument and calling your existing functions:
#   - "import": prints the number of transactions, the first and last date and
#     the number of bad rows, and writes the bad rows to data/errors.csv.
#     Python does not allow a function called import, so give Typer the
#     command's name and call the function something else.
#   - "report": prints the subscriptions (found from all months) and the text
#     report. A --month option, such as --month 2026-03, limits the report to
#     that month.
#   - "export", with an --out option (data/export.csv by default): one CSV row
#     per transaction with date, merchant, category, debit_paise and credit_paise.
#   Give each command a one-line docstring: Typer shows it in --help.
# TODO(task 24): make "report" print month_table and category_table with a Rich
#   Console, and add a --plain option that prints the old text report instead.
