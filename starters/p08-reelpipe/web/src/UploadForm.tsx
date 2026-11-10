import { useState } from 'react'

// Upload one video straight to the bucket, and return its video_id.
async function uploadVideo(file: File): Promise<string> {
  // TODO(task 8): POST { filename, content_type, size } to `${API_URL}/uploads` (API_URL is in api.ts).
  //   Then send the file itself straight to the bucket with
  //   fetch(upload_url, { method: 'PUT', body: file, headers }), using the API's headers unchanged.
  // TODO(task 9): after the PUT succeeds, POST to `${API_URL}/uploads/${video_id}/complete`.
  // Throw an Error with a clear message if any response is not ok.
  throw new Error(`TODO(task 8): upload ${file.name} with a presigned URL`)
}

export function UploadForm() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  async function upload() {
    if (!file) return
    setBusy(true)
    setMessage(`Uploading ${file.name}...`)
    try {
      const videoId = await uploadVideo(file)
      setMessage(`Uploaded ${file.name} as ${videoId}.`)
      // TODO(task 11): invalidate the ['videos'] query here, so the new video appears at once.
    } catch (error) {
      setMessage(error instanceof Error ? error.message : String(error))
    } finally {
      setBusy(false)
    }
  }

  return (
    <form
      className="upload"
      onSubmit={(event) => {
        event.preventDefault()
        void upload()
      }}
    >
      <label htmlFor="video-file">Choose a short video from your phone</label>
      <input
        id="video-file"
        type="file"
        accept="video/*"
        onChange={(event) => setFile(event.target.files?.[0] ?? null)}
      />
      <button type="submit" disabled={!file || busy}>
        {busy ? 'Uploading...' : 'Upload'}
      </button>
      <p role="status">{message}</p>
    </form>
  )
}
