import { UploadForm } from './UploadForm.tsx'
import { VideoList } from './VideoList.tsx'

function App() {
  return (
    <main>
      <h1>ReelPipe</h1>
      <p>Upload a short video. ReelPipe makes a thumbnail and a 480p copy of it.</p>
      <UploadForm />
      <VideoList />
    </main>
  )
}

export default App
