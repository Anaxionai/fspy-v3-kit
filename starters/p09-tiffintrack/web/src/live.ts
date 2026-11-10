// A WebSocket that reconnects by itself, and the check that drops late or repeated points.
import type { LiveMessage, PointMessage } from './messages.ts'

/** What connectLive tells the page about the connection. */
export type LiveStatus = { state: 'live' } | { state: 'reconnecting'; inSeconds: number }

/**
 * Open a WebSocket to `url` and keep it open. After every close, try again after retryDelayMs.
 * Calls onMessage with each message (see parseMessage) and onStatus when the state changes.
 * Returns stop(), for a useEffect clean-up: it closes the socket and cancels a planned retry.
 *
 * Edge cases: a successful open starts the delays from the beginning again; after stop(),
 * nothing reconnects. Log each reconnect attempt to the console.
 * TODO(task 9): write it.
 */
export function connectLive(
  url: string,
  onMessage: (message: LiveMessage) => void,
  onStatus: (status: LiveStatus) => void,
): () => void {
  throw new Error('TODO(task 9): connect, and reconnect after a close')
}

/**
 * Milliseconds to wait before reconnect attempt `attempt` (0 is the first retry after a close).
 * 1 s for the first, then twice as long each time, never more than 30 s,
 * plus a random 0 to 0.5 s (jitter), so that many browsers do not all retry at once.
 * TODO(task 9): write it. src/live.test.ts has tests for it.
 */
export function retryDelayMs(attempt: number): number {
  throw new Error('TODO(task 9): the wait before a reconnect')
}

/**
 * True if `point` has a higher seq than the last point shown for its rider. Then it also
 * remembers that seq in `lastSeq` (rider id to seq). A late or repeated point gives false,
 * so it never shows twice and never moves a marker backwards.
 * TODO(task 9): write it. src/live.test.ts has tests for it.
 */
export function isNewer(lastSeq: Map<number, number>, point: PointMessage): boolean {
  throw new Error('TODO(task 9): drop late and repeated points')
}
