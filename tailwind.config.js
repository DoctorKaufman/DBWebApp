/** @type {import('tailwindcss').Config} */

import plugin from 'tailwindcss/plugin';

export const darkMode = 'class';
export const content = [
  "./templates/**/*.html",
  "./app/**/*.html",
  "./node_modules/flowbite/**/*.js"
];
export const theme = {
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
    backgroundImage: {
      'custom-gradient': 'linear-gradient(to bottom, #1f2937, #26303f, #1f2937, #26303f, #26303f, #26303f, #26303f, #1f2937, #26303f, #1f2937)',
    }
  },
};
export const plugins = [
  require('flowbite/plugin'),
  require('@tailwindcss/forms'),

  plugin(function ({ addComponents, addBase, theme }) {
    addComponents({
      '.custom-scrollbar::-webkit-scrollbar': {
        width: '5px',
        height: '3px',
        borderRadius: '2px',
      },
      '.custom-scrollbar::-webkit-scrollbar-track': {
        background: theme('colors.gray.200'),
        borderRadius: '50px',
      },
      '.custom-scrollbar::-webkit-scrollbar-thumb': {
        background: theme('colors.gray.400'),
        borderRadius: '50px',
      },
      '.custom-scrollbar::-webkit-scrollbar-thumb:hover': {
        background: theme('colors.gray.500'),
      },

      // Dark theme scrollbar styles
      '.dark .custom-scrollbar::-webkit-scrollbar-track': {
        background: theme('colors.gray.800'),
      },
      '.dark .custom-scrollbar::-webkit-scrollbar-thumb': {
        background: theme('colors.gray.500'),
      },
      '.dark .custom-scrollbar::-webkit-scrollbar-thumb:hover': {
        background: theme('colors.gray.400'),
      },

      '.dotted-line': {
        // Dotted line configurations
        height: '2px',
        backgroundSize: '10px 2px',
        backgroundRepeat: 'repeat-x',
        backgroundImage: `radial-gradient(circle, ${theme('colors.gray.500')} 20%, transparent 20%)`,
      },
    });
  }),
];



