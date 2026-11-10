import { describe, expect, it } from 'vitest'
import type { Video, VideoStatus } from './types.ts'
import { refetchInterval } from './VideoList.tsx'

// A fake `query` holding one video per status, the way TanStack Query passes it to refetchInterval.
function queryWith(...statuses: VideoStatus[]) {
  const videos = statuses.map((status, i) => ({ id: `video-${i}`, status }) as Video)
  return { state: { data: videos } }
}

// TODO(task 11): delete `.skip` from these tests when refetchInterval is written. Run: npm test
describe('refetchInterval', () => {
  it.skip('polls every 2 seconds while a video is uploaded or processing', () => {
    expect(refetchInterval(queryWith('ready', 'processing'))).toBe(2000)
    expect(refetchInterval(queryWith('uploaded'))).toBe(2000)
  })

  it.skip('stops polling when every video is ready or failed', () => {
    expect(refetchInterval(queryWith('ready', 'failed'))).toBe(false)
  })

  it.skip('does not poll before the list has loaded', () => {
    expect(refetchInterval({ state: { data: undefined } })).toBe(false)
  })
})
