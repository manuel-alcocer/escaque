import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// The API host is configurable so the same build works against a local backend,
// docker compose, or the ingress in the cluster.
const API_TARGET = process.env.VITE_API_PROXY || 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': { target: API_TARGET, changeOrigin: true },
      '/media': { target: API_TARGET, changeOrigin: true },
    },
  },
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        // The board libraries are used by nearly every route, so they get their
        // own cacheable chunk instead of being duplicated per lazy view.
        manualChunks(id) {
          if (id.includes('chessground') || id.includes('chess.js')) return 'board'
          return undefined
        },
      },
    },
  },
})
