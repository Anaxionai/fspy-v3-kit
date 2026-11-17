"""Week 25 problem session: SQL interview questions.

Write each query between its triple quotes. The tests run it on SQLite,
which comes with Python. Write SQL that also runs on PostgreSQL.
Run the tests with: uv run --with pytest pytest -q
"""

# Problem A: every user with 3 or more cancelled bookings.
# Columns, in order: user_id, cancelled, cancelled_paise.
# Sort by cancelled (largest first), then by user_id.
QUERY_A = """
"""

# Problem B: the two trains with the most confirmed bookings on each journey date.
# Columns, in order: journey_date, train_no, name, confirmed_bookings, day_rank.
# On a tie, the smaller train_no comes first. Sort by journey_date, then by day_rank.
QUERY_B = """
"""
