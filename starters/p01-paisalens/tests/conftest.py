"""Shared pytest fixtures: every test file in tests/ can use them by name."""

# TODO(task 23): first make tests/data/mini_statement.csv: the real header and
#   10 rows from your statement, in date order, with 2 broken rows. Then write
#   two fixtures here:
#   - mini_path: the path of that file, found from the folder of this
#     conftest.py, so the tests work from any folder;
#   - loaded: uses mini_path and returns what load_all gives for the file:
#     the transactions and the error report.
