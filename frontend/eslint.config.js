import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import pluginTypescript from '@typescript-eslint/eslint-plugin'
import parserTypescript from '@typescript-eslint/parser'

export default [
  js.configs.recommended,
  pluginVue.configs['vue3-recommended'],
  {
    ignores: ['node_modules', 'dist', 'build']
  },
  {
    files: ['src/**/*.{ts,tsx,vue}'],
    languageOptions: {
      parser: parserTypescript,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
      }
    },
    plugins: {
      '@typescript-eslint': pluginTypescript
    },
    rules: {
      'vue/multi-word-component-names': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn'
    }
  }
]
