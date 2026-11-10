# RailSeat at scale: performance notes

Every number here was measured on this laptop with the settings under "How measured".
Plans are pasted as text from `EXPLAIN (ANALYZE, BUFFERS)`.

## Summary

<!-- TODO(task 13): one row per endpoint of the five slowest. Every number must match
     a section below: Baseline, a Fix, Pagination, N+1 or Search. -->

| Endpoint | Change made | p95 before (ms) | p95 after (ms) | Speed-up |
|---|---|---|---|---|

## Data

<!-- TODO(task 7): paste `SELECT count(*) FROM bookings;`, the count per status, the
     size from `\dt+ bookings` and how long the load took. -->

## Baseline

<!-- TODO(task 8): at least six GET endpoints, all with the same k6 settings. Mark the
     five slowest by p95, each with the SQL statement behind it. -->

| Endpoint | p50 (ms) | p95 (ms) | Requests per second | Slowest SQL |
|---|---|---|---|---|

## How measured

<!-- TODO(task 8): the k6 settings, the data size, and your laptop's CPU and RAM. -->

## Fix 1

<!-- TODO(task 9): the statement, the plan `Before`, the index you added, the plan
     `After`, and one line on what changed. Add `## Fix 2`, `## Fix 3` and so on the
     same way: at least three indexes, one composite and one partial. -->

## Index sizes

<!-- TODO(task 9): paste `\di+` for your new indexes. -->

## Pagination

<!-- TODO(task 10): page 1 and page 5,000 with OFFSET, then the same depth with keyset. -->

## N+1

<!-- TODO(task 10): the statement count and the time of one request, before and after the fix. -->

## Search

<!-- TODO(task 11): the plan of the full-text search next to the plan of `ILIKE '%mum%'`. -->

## Ask RailSeat

<!-- TODO(task 13): p50 and p95 of 10 calls of POST /ask, one after another (not k6),
     and the time of the embedding call, the database query and the chat call. -->

## What it cost

<!-- TODO(task 13): the size of every index you added, and one sentence on what indexes
     do to inserts. -->

## Not fixed

<!-- TODO(task 13): one slow thing you left, and why. -->
