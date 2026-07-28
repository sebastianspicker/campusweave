const browserGlobals = {
  AbortController: 'readonly',
  Blob: 'readonly',
  FormData: 'readonly',
  URL: 'readonly',
  clearTimeout: 'readonly',
  document: 'readonly',
  fetch: 'readonly',
  localStorage: 'readonly',
  navigator: 'readonly',
  setTimeout: 'readonly',
  window: 'readonly',
}

export default [
  {
    files: ['web/**/*.mjs', 'web/app.js'],
    languageOptions: { globals: browserGlobals },
  },
  {
    files: ['tests/test_campusweave_ui.mjs'],
    languageOptions: {
      globals: {
        URL: 'readonly',
        structuredClone: 'readonly',
      },
    },
  },
]
