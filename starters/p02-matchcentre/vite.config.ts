import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  // TODO(task 16): set the base option to the folder of your GitHub Pages site
  //   that serves Match Centre, so the built page finds its files there.
  plugins: [react()],
})
