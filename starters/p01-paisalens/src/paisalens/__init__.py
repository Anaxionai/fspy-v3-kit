"""PaisaLens: see where your money went, from a UPI bank statement."""


def main() -> None:
    """Run PaisaLens. `uv run paisalens` calls this function until task 22.

    It prints the greeting that `uv init` writes, so the starter runs before
    you write any code. Replace the greeting with your own output in task 6.
    """
    # TODO(task 6): call read_statement("data/statement.csv") and print the rows
    #   kept, the first and last date, and the money out and the money in.
    # TODO(task 7): print each month's total in month order, then the top 10
    #   merchants, biggest first.
    # TODO(task 8): load rules.json once, set each row's category, print the
    #   spending by category, biggest first, with the share that is "Other", and
    #   save the category totals to data/category_totals.json.
    # TODO(task 9): print render_report(rows) in place of those prints, and write
    #   the same text to data/report.txt.
    # TODO(task 18): set tx.category on each Transaction.
    # TODO(task 20): print each subscription and what they all cost in one month.
    # TODO(task 21): make an ErrorReport, pass it to read_statement, print the
    #   number of bad rows and write them to data/errors.csv.
    # TODO(task 22): delete main(): the commands in cli.py do its work.
    print("Hello from paisalens!")
