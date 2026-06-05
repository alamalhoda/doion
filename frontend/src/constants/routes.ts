export const ROUTES = {
  LOGIN: '/login',
  ADMIN_DASHBOARD: '/admin',
  USER_DASHBOARD: '/app',
  NOT_FOUND: '/:pathMatch(.*)*',
} as const

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES]
