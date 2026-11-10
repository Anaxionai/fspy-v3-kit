"""Cleaning the merchant's name out of a bank narration.

The same merchant can be written in many ways: SWIGGY, Swiggy Limited and
BUNDL TECHNOLOGIES are one merchant. The kit's data/upi/README.md shows the
five narration layouts your statement uses.
"""


def clean_merchant(narration: str) -> str:
    """Return the merchant's name from one narration.

    Task 7 makes a first, rough version: split the narration on "/" and return
    part 3 (counting from 0), stripped and in upper case. With fewer than 4
    parts, return the whole narration, stripped.
    "UPI/DR/624513611097/BIGBASKET/ICIC/bbdaily@icici/UPI" gives "BIGBASKET".
    """
    # TODO(task 19): rewrite it with regular expressions: capture the merchant
    #   part of each of the five layouts, remove noise such as LIMITED, LTD,
    #   PVT, LLP, a .com ending, digits and extra spaces, and return the name in
    #   title case ("Swiggy"). A UPI id alone keeps the part before "@".
    raise NotImplementedError("TODO(task 7): write a first clean_merchant")


# TODO(task 19): add a dict ALIASES for names that no pattern can link, such as
#   a legal name and its brand ("Bundl Technologies" is "Swiggy"), and apply it
#   last in clean_merchant.
