import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // The API and the bucket allow uploads from http://localhost:5173 only (their CORS rules).
  // strictPort stops Vite with an error if 5173 is busy, instead of moving to another port.
  server: { port: 5173, strictPort: true },
})
