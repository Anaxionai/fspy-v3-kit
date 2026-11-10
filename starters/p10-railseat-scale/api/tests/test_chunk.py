"""Splitting the travel rules (task 12, step 3).

Each test says what to check. Write the body, then delete its skip line.

These tests need no database.
"""

import pytest

# Three rules copied from the kit's travel-rules.md, in its layout.
SAMPLE = """# RailSeat travel rules

Words used in the rules:

- **Fare:** the price of one passenger's ticket, before any fee.

## Luggage

### Rule 15: Free luggage
Each adult passenger may carry this much luggage free: 1A 60 kg, 2A 45 kg, 3A 35 kg, SL 30 kg, CC 20 kg. A child aged 4 to 11 may carry half of the adult amount.

### Rule 16: Extra luggage
You may carry up to 30 kg more than your free amount. Pay ₹15 for each extra kilogram for every 500 km of the journey, or part of 500 km. Pay at the luggage counter before the train leaves.

## Pets

### Rule 38: Which pets may travel
Only dogs and cats may travel. They travel only in 1A, and only when your group books the whole cabin of 2 or 4 berths.
"""


@pytest.mark.skip(reason="TODO(task 12)")
def test_one_chunk_per_rule():
    """split_rules(SAMPLE) gives 3 rules numbered 15, 16 and 38, in that order."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
def test_titles_and_text():
    """Rule 38's title is "Which pets may travel", and its text starts with "Only dogs"."""
    raise NotImplementedError("TODO(task 12): write this test")


@pytest.mark.skip(reason="TODO(task 12)")
def test_text_has_no_headings():
    """No rule's text holds "##", "Words used" or the next rule."""
    raise NotImplementedError("TODO(task 12): write this test")
