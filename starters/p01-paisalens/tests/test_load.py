"""Tests for load.py. You write them: the starter gives only the plan."""

# TODO(task 10): write test functions that call the real to_paise and is_broken
#   and check each result with assert (6 or more tests across test_load.py,
#   test_clean.py and test_categorise.py):
#   - to_paise: "119.00", "64400.00", and an empty amount "";
#   - is_broken: a good row, a row whose debit is "Rs.855/-", and a row with
#     both amounts empty.
#   Import what you test, for example: from paisalens.load import to_paise
# TODO(task 21): replace the is_broken tests. Check with pytest.raises that
#   parse_row raises BadRow for a bad date and for a bad amount.
# TODO(task 23): use the loaded fixture to check the exact number of good rows,
#   and the line number and reason of each problem in the report. Add one
#   parametrised test with at least 4 broken rows and the reason for each.
