// One customer's order page, opened as http://localhost:5173/?order=<id> (task 18).
// You will need: useEffect and useState from 'react', API_URL and WS_URL from './config.ts',
// connectLive from './live.ts', and the message types from './messages.ts'.
import type { ReactNode } from 'react'

/**
 * Reads the order id from ?order=<id> in the address, then shows the four statuses:
 * done ones with their time, the current one in bold, later ones grey.
 * Below them: the rider's latest position and its age in seconds.
 * It updates live from WS_URL + '/ws/orders/' + id, with no page reload: first the
 * snapshot message, then each status and point message.
 *
 * TODO(task 18): write it.
 * TODO(task 20): every 15 seconds, fetch API_URL + '/orders/' + id and show
 *   "Arriving in about N min" from its eta_minutes. Clear the timer in the clean-up.
 */
export function OrderTracker(): ReactNode {
  throw new Error('TODO(task 18): show the order timeline, live')
}
