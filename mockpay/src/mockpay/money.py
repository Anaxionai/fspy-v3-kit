"""Money helpers. Money is always a whole number of paise (an int), never a float.

₹12.50 is 1250 paise. Floats cannot hold most decimal fractions exactly
(0.1 + 0.2 != 0.3), so all maths here is integer maths.
"""

FEE_PERCENT = 2  # MockPay keeps 2% of every captured payment


def fee_paise(amount_paise: int) -> int:
    """MockPay's fee for one payment: 2% of it, rounded to the nearest paisa.

    Exactly half a paisa rounds up: 2% of 125 paise is 2.5, so the fee is 3.
    (Python's round() would give 2, because it rounds halves to the even number.)
    Adding 50 before the whole-number division by 100 does the rounding.
    """
    return (amount_paise * FEE_PERCENT + 50) // 100


def format_inr(paise: int) -> str:
    """Show paise as rupees with Indian digit groups: 12345678 -> '₹1,23,456.78'."""
    sign = "-" if paise < 0 else ""
    rupees, rest = divmod(abs(paise), 100)
    digits = str(rupees)
    if len(digits) > 3:
        # The last three digits form one group; the rest go in groups of two.
        head, tail = digits[:-3], digits[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        groups.insert(0, head)
        digits = ",".join([*groups, tail])
    return f"{sign}₹{digits}.{rest:02d}"
