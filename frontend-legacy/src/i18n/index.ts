import { createI18n } from 'vue-i18n'
import { appConfig } from '@/config/app'
import faMessages from './locales/fa.json'
import enMessages from './locales/en.json'

const messages = {
  fa: faMessages,
  en: enMessages,
}

export const i18n = createI18n({
  locale: appConfig.defaultLocale,
  fallbackLocale: 'fa',
  messages,
  globalInjection: true,
  legacy: false,
})

export default i18n
