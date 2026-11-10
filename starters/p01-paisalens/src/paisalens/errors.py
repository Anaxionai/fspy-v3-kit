"""Bad rows: your own exception and the error report.

Your statement has exactly 4 broken rows on purpose: a bad date, no amount,
a text amount and a duplicate. In task 21 they are listed, not skipped.
"""

# TODO(task 21): define BadRow here: your own exception for a row that cannot
#   be read. parse_row raises it with the reason as its message.


class ErrorReport:
    """Collects the bad rows of a statement: line number, reason and row."""

    def __init__(self) -> None:
        """Start with no problems recorded."""
        raise NotImplementedError("TODO(task 21): start an empty list, self.problems")

    def add(self, line: int, reason: str, row: dict) -> None:
        """Record one bad row: its line number in the file, why it is bad, and the row."""
        raise NotImplementedError("TODO(task 21): write ErrorReport.add")

    def write_csv(self, path: str) -> None:
        """Write every bad row to a CSV file with the columns line, reason and row."""
        raise NotImplementedError("TODO(task 21): write ErrorReport.write_csv")
