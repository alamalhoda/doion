import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import pluginTypescript from '@typescript-eslint/eslint-plugin'
import parserTypescript from '@typescript-eslint/parser'

export default [
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    // Parse TypeScript inside <script> blocks of .vue files
    files: ['**/*.vue'],
    languageOptions: {
      parserOptions: {
        parser: parserTypescript
      }
    },
    plugins: {
      '@typescript-eslint': pluginTypescript
    },
    rules: {
      // Single-word component names are intentional in this project (e.g. Button, Card, Nav)
      'vue/multi-word-component-names': 'off',
      // Disable base no-unused-vars in favor of the TypeScript-aware version
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn'
    }
  },
  {
    ignores: ['node_modules', 'dist', 'build', '**/*.d.ts']
  },
  {
    files: ['src/**/*.{ts,tsx}'],
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
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn'
    }
  }
]
