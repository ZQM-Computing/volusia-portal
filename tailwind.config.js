export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        volusia: {
          navy: '#0f1b2d',
          blue: '#1a3a5c',
          teal: '#0d7377',
          gold: '#c9a84c',
          sand: '#f5f0e6',
          coral: '#e07a5f',
          green: '#3d8b7d',
          slate: '#4a5568',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Source Serif Pro', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
}
