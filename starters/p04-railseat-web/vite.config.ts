import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
// TODO(task 14): import tailwindcss from '@tailwindcss/vite', and add
// tailwindcss() to the plugins list below. The package is already installed.

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Your API allows only the origin http://localhost:5173 (CORS, task 9).
    // If port 5173 is busy, stop with an error instead of moving to 5174.
    port: 5173,
    strictPort: true,
  },
})
