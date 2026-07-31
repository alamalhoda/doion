export const appConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '',
  appName: import.meta.env.VITE_APP_NAME || 'Doion',
  defaultLocale: (import.meta.env.VITE_DEFAULT_LOCALE || 'fa') as 'fa' | 'en',
} as const

export type AppConfig = typeof appConfig
