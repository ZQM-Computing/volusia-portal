import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { copyFileSync, mkdirSync, existsSync } from 'fs'

// Plugin to copy data directory to dist
function copyDataPlugin() {
  return {
    name: 'copy-data',
    closeBundle() {
      const dataDir = resolve(__dirname, 'data')
      const distDataDir = resolve(__dirname, 'dist/data')
      if (!existsSync(distDataDir)) {
        mkdirSync(distDataDir, { recursive: true })
      }
      const files = ['indicators.json', 'economic.json', 'demographics.json', 'climate.json', 'datasets.json', 'map-layers.json', 'stakeholders.json', 'news.json', 'health.json']
      files.forEach(f => {
        try {
          copyFileSync(resolve(dataDir, f), resolve(distDataDir, f))
        } catch (e) {
          console.warn(`Could not copy ${f}:`, e.message)
        }
      })
      console.log('Data files copied to dist/data/')
    }
  }
}

export default defineConfig({
  plugins: [react(), copyDataPlugin()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
  },
})
