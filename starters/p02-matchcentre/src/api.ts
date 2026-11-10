// Reading the replay server from the course kit (tools/cricket-replay).

import type { MatchMeta, MatchState } from './types'

/** Where the replay server runs on your computer. */
export const FEED_URL = 'http://localhost:8765'

/**
 * GET /live: the match so far, with the balls grouped by innings.
 * Throws an Error when the answer is not ok, such as a 404 or a 500.
 */
export async function fetchLive(): Promise<MatchState> {
  throw new Error('TODO(task 13): write fetchLive')
}

/**
 * GET /meta: the teams, the venue and the other match details.
 * Throws an Error when the answer is not ok.
 */
export async function fetchMeta(): Promise<MatchMeta> {
  throw new Error('TODO(task 13): write fetchMeta')
}
