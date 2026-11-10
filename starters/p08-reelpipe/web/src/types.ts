// The four statuses a video moves through: uploaded, then processing, then ready or failed.
export type VideoStatus = 'uploaded' | 'processing' | 'ready' | 'failed'

// One status record from GET /videos: the JSON in status/<video_id>.json.
export type Video = {
  id: string
  status: VideoStatus
  error?: string // set when the status is "failed"
  // TODO(task 11): add the other fields your status record has, such as the output keys and a time.
}

// What POST /uploads returns (task 8).
export type UploadResponse = {
  video_id: string
  upload_url: string
  headers: Record<string, string>
}
