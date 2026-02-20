/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        cream: '#FAF9F6',
        surface: '#FFFFFF',
        border: '#E8E6E1',
        'text-primary': '#1D1D1B',
        'text-secondary': '#71706C',
        'text-tertiary': '#9C9B97',
        accent: '#C4422B',
        'accent-light': '#FEF2F0',
        blue: '#2563EB',
        'blue-light': '#EFF6FF',
        green: '#059669',
        'green-light': '#ECFDF5',
        gold: '#D97706',
        'gold-light': '#FFFBEB',
        purple: '#7C3AED',
        'purple-light': '#F5F3FF',
      },
      fontFamily: {
        sans: ['"Inter"', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"SF Mono"', 'monospace'],
        serif: ['"Newsreader"', '"Georgia"', 'serif'],
      },
      fontSize: {
        '2xs': ['0.65rem', { lineHeight: '1rem' }],
      },
      maxWidth: {
        content: '720px',
        wide: '960px',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-out forwards',
        'slide-up': 'slideUp 0.6s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
