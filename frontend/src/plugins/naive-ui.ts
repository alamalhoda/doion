import type { App } from 'vue'

export function setupNaiveUI(app: App) {
  // Naive UI configuration
  // Theme will be handled via CSS variables in styles/tokens.css
  // Override any Naive UI defaults here if needed

  // Set initial theme
  const savedTheme = sessionStorage.getItem('app_theme') || 'light'
  document.documentElement.setAttribute('data-theme', savedTheme)
}

export default setupNaiveUI
