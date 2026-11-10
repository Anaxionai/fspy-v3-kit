import type { Video } from './types.ts'

// The part of TanStack Query's `query` object that refetchInterval reads.
type VideosQuery = { state: { data?: Video[] } }

// How long to wait before fetching GET /videos again, in milliseconds, or false to stop polling.
// TanStack Query calls it after each fetch.
export function refetchInterval(query: VideosQuery): number | false {
  // TODO(task 11): return 2000 while any video is "uploaded" or "processing",
  //   and false when none is (also before the list has loaded).
  throw new Error('TODO(task 11): poll every 2000 ms only while a video is in progress')
}

// The list of videos and their statuses.
export function VideoList() {
  // TODO(task 11): load the list with
  //   useQuery({ queryKey: ['videos'], queryFn: listVideos, refetchInterval })
  //   and show one row per video with its <StatusBadge>. For "failed", show the record's error.
  //   For "ready", show the names of the two output files.
  //   Until then it shows a fixed line, so the app starts in tasks 8 to 10.
  return (
    <section aria-labelledby="videos-heading">
      <h2 id="videos-heading">Your videos</h2>
      <p>Your videos appear here after task 11.</p>
    </section>
  )
}
