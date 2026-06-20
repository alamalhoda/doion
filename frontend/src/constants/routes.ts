export const ROUTES = {
  // Auth
  LOGIN: '/login',
  REGISTER: '/register',
  
  // Admin
  ADMIN_DASHBOARD: '/admin',
  ADMIN_MODERATION_QUEUE: '/admin/moderation',
  
  // User - Check Holder
  USER_DASHBOARD: '/app',
  USER_LISTINGS: '/app/listings',
  USER_CREATE_LISTING: '/app/listings/create',
  USER_LISTING_DETAIL: '/app/listings/:id',
  USER_MATCHES: '/app/matches',
  USER_NOTIFICATIONS: '/app/notifications',
  WORKFLOW_PROTOTYPE: '/app/prototype',

  // Marketplace - Investor
  MARKETPLACE: '/app/marketplace',
  
  // Shared
  NOT_FOUND: '/:pathMatch(.*)*',
} as const

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES]