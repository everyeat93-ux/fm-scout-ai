/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        wyscout: {
          bg: '#0a0a16',
          card: '#121226',
          cardHover: '#181832',
          border: '#1f2240',
          borderGlow: '#2a2e5c',
          neon: '#00ff88',
          cyan: '#00e5ff',
          amber: '#ffb800',
          red: '#ff3b5c',
          textMuted: '#8a8fa8',
          textLight: '#e2e8f0'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Roboto Mono', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'glow-neon': '0 0 20px -5px rgba(0, 255, 136, 0.4)',
        'glow-cyan': '0 0 20px -5px rgba(0, 229, 255, 0.4)',
        'glow-amber': '0 0 20px -5px rgba(255, 184, 0, 0.4)',
      }
    },
  },
  plugins: [],
}
