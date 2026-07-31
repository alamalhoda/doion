import type { App } from 'vue'
import { i18n } from '@/i18n'

export function setupI18n(app: App) {
  app.use(i18n)

  // Initialize locale direction and theme
  const locale = i18n.global.locale.value
  document.documentElement.dir = locale === 'fa' ? 'rtl' : 'ltr'
  document.documentElement.lang = locale
}

export default i18n
