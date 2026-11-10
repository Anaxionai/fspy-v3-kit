import type { ReactNode } from 'react'
import type { VideoStatus } from './types.ts'

// One label for a video's status: a word and a colour. Colour alone is not enough, as you learned in P2.
export function StatusBadge({ status }: { status: VideoStatus }): ReactNode {
  // TODO(task 11): show each of the four statuses (uploaded, processing, ready, failed)
  //   as its word, with its own colour.
  throw new Error(`TODO(task 11): show a word and a colour for "${status}"`)
}
