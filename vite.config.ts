import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  root: "./app",
  resolve: {
    alias: [{
      find: "@/", replacement: "/",
    }]
  },
  plugins: [svelte()],
})
