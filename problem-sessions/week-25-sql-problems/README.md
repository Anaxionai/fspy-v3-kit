# Week 25: SQL interview questions

## The pattern in five lines

1. `GROUP BY` makes one row for each group. `WHERE` filters rows before the grouping, and `HAVING` filters the groups after it.
2. A CTE (common table expression, `WITH name AS (...)`) gives one step of a query a name, so you can build the answer in readable steps.
3. A window function (a calculation across related rows that keeps every row), such as `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`, numbers the rows inside each group.
4. Reach for these when a question says "for each", "at least", "top two in each" or "running total".
5. The database plans the work, but say the cost aloud anyway: grouping or sorting n rows costs about O(n log n).

## The tables and the sample data

The tests run your query on SQLite, which comes with Python. The same SQL runs on PostgreSQL, where you learnt CTEs and window functions in week 18. Use only `SELECT`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `WITH`, window functions and `ORDER BY`. Do not use date functions, because SQLite and PostgreSQL name them differently.

```sql
CREATE TABLE trains (
    train_no TEXT PRIMARY KEY,        -- for example '91001'
    name TEXT NOT NULL,
    from_station TEXT NOT NULL,
    to_station TEXT NOT NULL
);
CREATE TABLE journeys (               -- one run of a train on one date
    journey_id INTEGER PRIMARY KEY,
    train_no TEXT NOT NULL REFERENCES trains (train_no),
    journey_date TEXT NOT NULL        -- 'YYYY-MM-DD', for example '2026-10-01'
);
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY,
    journey_id INTEGER NOT NULL REFERENCES journeys (journey_id),
    user_id INTEGER NOT NULL,
    amount_paise INTEGER NOT NULL,    -- 45000 paise is 450 rupees
    status TEXT NOT NULL              -- 'confirmed' or 'cancelled'
);
```

The sample data has 4 trains, 7 journeys and 28 bookings.

| train_no | name | from_station | to_station |
|---|---|---|---|
| 91001 | Deccan Link | CSMT | PUNE |
| 91002 | Konkan Breeze | CSMT | MAO |
| 91003 | Narmada Mail | BCT | BPL |
| 91004 | Vidarbha Link | CSMT | NGP |

| journey_id | train_no | journey_date |
|---|---|---|
| 1 | 91001 | 2026-10-01 |
| 2 | 91002 | 2026-10-01 |
| 3 | 91003 | 2026-10-01 |
| 4 | 91001 | 2026-10-02 |
| 5 | 91002 | 2026-10-02 |
| 6 | 91004 | 2026-10-02 |
| 7 | 91003 | 2026-10-03 |

| booking_id | journey_id | user_id | amount_paise | status |
|---|---|---|---|---|
| 1 | 1 | 105 | 45000 | confirmed |
| 2 | 1 | 107 | 45000 | confirmed |
| 3 | 1 | 108 | 52000 | confirmed |
| 4 | 1 | 101 | 45000 | cancelled |
| 5 | 2 | 103 | 120000 | confirmed |
| 6 | 2 | 105 | 95000 | confirmed |
| 7 | 2 | 107 | 120000 | confirmed |
| 8 | 2 | 102 | 120000 | cancelled |
| 9 | 2 | 104 | 95000 | cancelled |
| 10 | 3 | 101 | 60000 | confirmed |
| 11 | 3 | 101 | 60000 | cancelled |
| 12 | 3 | 102 | 60000 | cancelled |
| 13 | 3 | 104 | 75000 | cancelled |
| 14 | 3 | 106 | 60000 | cancelled |
| 15 | 4 | 108 | 45000 | confirmed |
| 16 | 4 | 101 | 45000 | cancelled |
| 17 | 4 | 103 | 90000 | cancelled |
| 18 | 5 | 103 | 120000 | confirmed |
| 19 | 5 | 105 | 95000 | confirmed |
| 20 | 5 | 104 | 120000 | cancelled |
| 21 | 6 | 105 | 155000 | confirmed |
| 22 | 6 | 107 | 155000 | confirmed |
| 23 | 6 | 108 | 130000 | confirmed |
| 24 | 6 | 103 | 155000 | confirmed |
| 25 | 6 | 102 | 155000 | cancelled |
| 26 | 7 | 105 | 60000 | confirmed |
| 27 | 7 | 101 | 60000 | cancelled |
| 28 | 7 | 103 | 75000 | cancelled |

## Problem A (warm-up, 10 minutes): Users who cancel again and again

RailSeat suspects that some accounts book seats and then cancel them, to block other passengers. List every user with 3 or more cancelled bookings. Show how many they cancelled and the total amount of those bookings.

```python
QUERY_A = """
"""
```

Return these columns, in this order: `user_id`, `cancelled` (the number of cancelled bookings) and `cancelled_paise` (their total `amount_paise`).

**Examples**

| Data | Returns | Why |
|---|---|---|
| The sample data | `(101, 4, 210000)`, `(102, 3, 335000)`, `(104, 3, 290000)` | Users 102 and 104 tie on 3, so the smaller `user_id` comes first. User 103 cancelled only 2. |
| Only bookings 8, 12 and 25 | `(102, 3, 335000)` | 120000 + 60000 + 155000 = 335000. |
| An empty `bookings` table | no rows | Nobody has cancelled anything. |

**Rules**

- Count only bookings whose `status` is `'cancelled'`.
- Keep a user only when they have 3 or more cancelled bookings.
- Sort by `cancelled`, largest first. When two users tie, the smaller `user_id` comes first.
- Return no rows when `bookings` is empty. The tests also use up to 400 bookings.

## Problem B (main, 25 minutes): Top two trains on each date

The operations team wants to know which trains are busiest on each date. For each `journey_date`, find the two trains with the most confirmed bookings, and number them 1 and 2.

```python
QUERY_B = """
"""
```

Return these columns, in this order: `journey_date`, `train_no`, `name`, `confirmed_bookings` and `day_rank` (1 for the busiest train on that date, 2 for the next).

**Examples**

| Data | Returns | Why |
|---|---|---|
| The sample data | the 5 rows below | 2026-10-03 has only one train, so it has only one row. |
| Only booking 10 | `("2026-10-01", "91003", "Narmada Mail", 1, 1)` | One confirmed booking gives one row. |
| Only booking 11 | no rows | A cancelled booking does not count. |
| An empty `bookings` table | no rows | There are no bookings to count. |

The 5 rows for the sample data:

```text
("2026-10-01", "91001", "Deccan Link",   3, 1)
("2026-10-01", "91002", "Konkan Breeze", 3, 2)
("2026-10-02", "91004", "Vidarbha Link", 4, 1)
("2026-10-02", "91002", "Konkan Breeze", 2, 2)
("2026-10-03", "91003", "Narmada Mail",  1, 1)
```

On 2026-10-01, trains 91001 and 91002 both have 3 confirmed bookings, so the smaller train number gets rank 1. Train 91003 has 5 bookings that day, but 4 of them are cancelled.

**Rules**

- Count only bookings whose `status` is `'confirmed'`.
- A train with no confirmed bookings on a date does not appear for that date.
- Rank the trains on each date separately: the most confirmed bookings first. When two trains tie, the smaller `train_no` comes first.
- Keep ranks 1 and 2 only. A date with one busy train has one row.
- Sort by `journey_date`, then by `day_rank`.
- Return no rows when `bookings` is empty.

## Say it aloud

Answer these three questions aloud for each problem before you write the query.

1. What is the slow way to get this answer, for example with a subquery for every row, and what does it cost?
2. Which rows do you filter before grouping, which groups do you filter after, and what does each CTE hold?
3. Which edge cases (unusual data, such as a tie or a date with one train) could break your query? Name three.

## After the session

Write `QUERY_C`: a running total of confirmed `amount_paise` for each `journey_date`, in `booking_id` order. Use `SUM(...) OVER (PARTITION BY ... ORDER BY ...)`. Check it by hand against the sample data for 2026-10-02.

## Run the tests

Open a terminal in this folder and run:

```bash
uv run --with pytest pytest -q
```

Every test fails with "QUERY_A is empty" or "QUERY_B is empty" until you write your queries in `problems.py`. Do not change `test_problems.py`.
