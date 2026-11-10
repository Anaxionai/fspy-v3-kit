"""Money in RailSeat: whole paise as `int`, never `float` (P6 add-on, task 8).

₹1,234.50 is 123450 paise. Convert only at the edges (text in, text out) and keep
`int` everywhere else: in the database (BigInteger), in Python and in JSON.
"""


def parse_rupees(text: str) -> int:
    """Turn rupee text into whole paise: "1234.50" gives 123450, "0.1" gives 10 (step 1).

    - Use `decimal.Decimal`, never `float`.
    - Raise ValueError for a negative amount, more than two decimals ("12.345")
      or text that is not a number (step 2).
    """
    raise NotImplementedError("TODO(task 8): convert rupee text to paise with Decimal")


def format_paise(paise: int) -> str:
    """Turn paise into rupee text with two decimals: 123450 gives "1234.50" (step 1).

    5 gives "0.05". Use `divmod`, not division.
    """
    raise NotImplementedError("TODO(task 8): format paise as rupee text with divmod")


def split_paise(total: int, parts: int) -> list[int]:
    """Split `total` paise into `parts` whole amounts that add up to `total` exactly (step 2).

    The leftover paise go to the first parts: `split_paise(10000, 3)` is
    `[3334, 3333, 3333]`. `parts` below 1 raises ValueError.
    """
    raise NotImplementedError("TODO(task 8): split the total without losing a paisa")
