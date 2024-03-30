/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./app/**/*.html",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      animation: {
        'gradient': 'gradient 8s linear infinite',
        'blobs': 'gradient 14s linear infinite',
      },
      keyframes: {
        'gradient': {
          to: { 'background-position': '300% center' },
        }
      },
      // this was harder than I expected 🥲
      backgroundImage: {
        'custom-gradient': 'linear-gradient(to bottom, #1f2937, #26303f, #1f2937, #26303f, #26303f, #26303f, #1f2937, #26303f, #1f2937)',
      }
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/forms'),
  ],
}



