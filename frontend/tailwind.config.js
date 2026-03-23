/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aqua: {
          50:  '#edfcfa',
          100: '#d0f8f3',
          200: '#a5f0e8',
          300: '#6de3d9',
          400: '#2dccc4',
          500: '#14b0aa',
          600: '#0e8e89',
          700: '#0d716d',
          800: '#0e5a57',
          900: '#104b48',
        },
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        }
      }
    },
  },
  plugins: [],
}
