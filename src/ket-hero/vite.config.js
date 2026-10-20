import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Builds one self-mounting script (dist/ket-hero.js) for the existing static page.
export default defineConfig({
  plugins: [react()],
  define: { 'process.env.NODE_ENV': JSON.stringify('production') },
  build: {
    lib: { entry: 'src/embed.jsx', name: 'KetHero', formats: ['iife'], fileName: () => 'ket-hero.js' },
    copyPublicDir: true,
    sourcemap: false,
    chunkSizeWarningLimit: 1500,
    // GSAP comes from the page (one ScrollTrigger instance for the whole page, so the
    // hero's pin and the page's own pins are measured together, in order)
    rollupOptions: {
      external: ['gsap', 'gsap/ScrollTrigger'],
      output: { globals: { gsap: 'gsap', 'gsap/ScrollTrigger': 'ScrollTrigger' } },
    },
  },
})
