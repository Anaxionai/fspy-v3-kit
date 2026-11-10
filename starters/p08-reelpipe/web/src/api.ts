import type { Video } from './types.ts'

// Where the ReelPipe API runs (task 8): uv run --env-file .env fastapi dev api/app/main.py
export const API_URL = 'http://localhost:8000'

// Every video's status record from GET /videos, newest first.
export async function listVideos(): Promise<Video[]> {
  // TODO(task 11): fetch `${API_URL}/videos` and return the parsed JSON.
  //   Throw an Error if the response is not ok, so TanStack Query shows it as an error.
  throw new Error('TODO(task 11): fetch GET /videos')
}
