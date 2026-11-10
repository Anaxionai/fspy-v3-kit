import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// TODO(task 11): console.log inningsRuns, inningsWickets and oversText for
//   the first innings of `sample` (from src/sample.ts), then compare them with
//   the JSON in the browser console.

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
