module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './core/templates/**/*.{html,js}',
    './node_modules/flowbite/**/*.{html,js}',
  ],
  safelist: [
    'bg-gray-900/50',
    'dark:bg-gray-900/80',
    'fixed',
    'inset-0',
    'z-30',
  ],
  theme: {
    extend: {
      colors: {
        skyblue: '#F2F6FF',
        darkblue: '#3B39A7',
        bgdarkblue: '#0F1F45',
        bglightblue: '#1F2873',
        navy: '#4456A2',
        bggray: '#F8F9FB'
      },
      fontFamily: {
        'body': [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'Noto Sans',
          'sans-serif',
          'Apple Color Emoji',
          'Segoe UI Emoji',
          'Segoe UI Symbol',
          'Noto Color Emoji'
        ],
        'sans': [
          'Inter',
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'Noto Sans',
          'sans-serif',
          'Apple Color Emoji',
          'Segoe UI Emoji',
          'Segoe UI Symbol',
          'Noto Color Emoji'
          // other fallback fonts
        ]
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
