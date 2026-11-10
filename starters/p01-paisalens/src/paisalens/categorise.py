"""Sorting payments into categories, with rules kept in a JSON file.

rules.json maps a lower-case pattern to a category, such as
"swiggy": "Food delivery". Copy the kit's data/upi/rules-example.json into
paisalens/ as rules.json in task 8.
"""


def load_rules(path: str) -> dict[str, str]:
    """Read the rules file at `path` and return it as a dict.

    Keys are lower-case patterns and values are categories. The dict keeps the
    order of the file, and that order matters in categorise.
    """
    raise NotImplementedError("TODO(task 8): write load_rules")


def categorise(tx, rules: dict[str, str]) -> str:
    """Return the category of the first pattern found in the narration.

    Compare in lower case. The first match wins, so "refund" must come before
    "amazon": an Amazon refund is not shopping. Return "Other" when no pattern
    matches.
    tx is one row dict until task 18, then one Transaction.
    """
    # TODO(task 18): read tx.narration in place of tx["narration"].
    raise NotImplementedError("TODO(task 8): write categorise")
