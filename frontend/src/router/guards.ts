import type { RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { ROUTES } from '@/constants/routes'
import { canAccessAdmin, canAccessUser } from '@/utils/permissions'

export function setupRouterGuards(router: any) {
  router.beforeEach(async (to: RouteLocationNormalized, _from: RouteLocationNormalized) => {
    const authStore = useAuthStore()

    // Restore auth state if needed
    if (!authStore.isAuthenticated && sessionStorage.getItem('auth_token')) {
      await authStore.restoreAuth()
    }

    // Public routes (login, 404)
    const isPublicRoute = to.path === ROUTES.LOGIN || to.matched.some(r => r.path === ROUTES.NOT_FOUND)
    if (isPublicRoute) {
      return true
    }

    // Require authentication for protected routes
    if (!authStore.isAuthenticated) {
      return ROUTES.LOGIN
    }

    // Admin routes
    if (to.path === ROUTES.ADMIN_DASHBOARD) {
      if (!canAccessAdmin(authStore.user)) {
        return ROUTES.USER_DASHBOARD
      }
      return true
    }

    // User routes
    if (to.path === ROUTES.USER_DASHBOARD) {
      if (!canAccessUser(authStore.user)) {
        return ROUTES.LOGIN
      }
      return true
    }

    return true
  })
}
