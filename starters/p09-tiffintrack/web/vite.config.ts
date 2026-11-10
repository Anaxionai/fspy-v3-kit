import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // The API allows calls from http://localhost:5173 only, so stop with an error
  // if that port is busy, instead of moving to another one.
  server: { port: 5173, strictPort: true },
})
