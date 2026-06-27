export const ROUTES = {
  // Public
  LANDING: '/',

  // Auth
  LOGIN: '/login',
  REGISTER: '/register',

  // Identity
  IDENTITY_ME: '/identity/me',
  IDENTITY_PROFILE: '/identity/profile',
  
  // Admin
  ADMIN_DASHBOARD: '/admin',
  ADMIN_MODERATION_QUEUE: '/admin/moderation',
  
  // User - Check Holder
  USER_DASHBOARD: '/app',
  USER_LISTINGS: '/app/listings',
  USER_CREATE_LISTING: '/app/listings/create',
  USER_LISTING_DETAIL: '/app/listings/:id',
  USER_MATCHES: '/app/matches',
  USER_MATCHES_DETAIL: '/app/matches/:id',
  USER_NOTIFICATIONS: '/app/notifications',
  WORKFLOW_PROTOTYPE: '/app/prototype',

  // Marketplace - Investor
  MARKETPLACE: '/app/marketplace',
  
  // Shared
  NOT_FOUND: '/:pathMatch(.*)*',
} as const

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES]