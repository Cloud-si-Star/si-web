import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        // 关键：识别到 SSE 请求时，设置禁用缓冲的头
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req) => {
            // 如果是 SSE 请求，告诉上游服务器不要缓冲
            if (req.headers.accept?.includes('text/event-stream')) {
              proxyReq.setHeader('Cache-Control', 'no-cache')
              proxyReq.setHeader('Connection', 'keep-alive')
            }
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            // 确保 SSE 响应不被 Vite 中间层拦截或缓冲
            if (proxyRes.headers['content-type']?.includes('text/event-stream')) {
              // 关键：设置 X-Accel-Buffering 为 no，防止代理层缓冲
              res.setHeader('X-Accel-Buffering', 'no')
              res.setHeader('Cache-Control', 'no-cache')
              res.setHeader('Connection', 'keep-alive')
            }
          })
        }
      }
    }
  }
})
