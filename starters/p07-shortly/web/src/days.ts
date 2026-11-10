import type { DayClicks } from './api'

// Fills the gaps in a link's clicks per day (task 21), so the page shows one row per day.
//
// Input: per_day from GET /links/{code}/stats, sorted by day ("YYYY-MM-DD").
// Output: the same days, plus every missing day between the first and the last,
//   with clicks 0, all in date order. An empty list gives an empty list.
// Edge case: count days in UTC (Date.UTC, getUTCDate), so a time zone never skips or repeats a day.
export function fillDays(perDay: DayClicks[]): DayClicks[] {
  throw new Error(`TODO(task 21): fill the missing days between ${perDay.length} entries`)
}
