// The live table: one row per rider with their latest point.
// You will need: useEffect and useState from 'react', WS_URL from './config.ts',
// and parseMessage from './messages.ts'.
import type { ReactNode } from 'react'

/**
 * One row per rider: rider id, seq, lat, lng, and the seconds since ts.
 * The rows update as points arrive from WS_URL + '/ws/riders', in every open tab.
 *
 * Edge cases: the socket closes when the component goes away (the effect's clean-up);
 * a rider who sends a new point keeps one row.
 * TODO(task 8): write it with a WebSocket opened in a useEffect.
 * TODO(task 9): connect with connectLive() from live.ts instead, show "Live" or
 *   "Reconnecting in N s", and ignore a point when isNewer() says false.
 */
export function LiveTable(): ReactNode {
  throw new Error('TODO(task 8): show the latest point of every rider')
}
