// Calls to Shortly's API (task 21).
// The base URL comes from VITE_API_URL in web/.env (copy web/.env.example).
export const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8080'

// One day of clicks. day is a date in India time, such as "2026-12-01".
export type DayClicks = { day: string; clicks: number }

// The answer of GET /links/{code}/stats.
export type LinkStats = {
  code: string
  target_url: string
  clicks: number
  created_at: string
  per_day: DayClicks[]
}

// One row of GET /stats/top.
export type TopLink = { code: string; clicks: number }

// GET /links/{code}/stats. Throws an Error when the answer is not OK (404 for an unknown code).
export async function fetchStats(code: string): Promise<LinkStats> {
  throw new Error(`TODO(task 21): fetch ${API_URL}/links/${code}/stats`)
}

// GET /stats/top?limit=... Throws an Error when the answer is not OK.
export async function fetchTop(limit = 10): Promise<TopLink[]> {
  throw new Error(`TODO(task 21): fetch ${API_URL}/stats/top?limit=${limit}`)
}
