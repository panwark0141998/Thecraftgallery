/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fcfaf6',
          100: '#f5efe6',
          500: '#e29b59',
          600: '#c78848',
          700: '#8c5a2b',
          800: '#543618',
          900: '#2b2521',
        },
        sidebar: '#2b2521'
      }
    },
  },
  plugins: [],
}
