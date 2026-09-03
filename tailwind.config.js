export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
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
