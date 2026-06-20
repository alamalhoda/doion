import { type Router } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { canAccessAdmin, canAccessUser } from '@/utils/permissions'
import { ROUTES } from '@/constants/routes'

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to, _from) => {
    const authStore = useAuthStore()
    const isAuthenticated = authStore.isAuthenticated
    const user = authStore.user

    // Public routes
    if (to.meta.public) {
      if (isAuthenticated && to.path === ROUTES.LOGIN) {
        return canAccessAdmin(user) ? ROUTES.ADMIN_DASHBOARD : ROUTES.USER_DASHBOARD
      }
      return true
    }

    // Protected routes
    if (!isAuthenticated) {
      return ROUTES.LOGIN
    }

    // Admin routes
    if (to.meta.requiresAdmin) {
      if (!canAccessAdmin(user)) {
        return ROUTES.USER_DASHBOARD
      }
      return true
    }

    // User routes
    if (to.meta.requiresUser) {
      if (!canAccessUser(user)) {
        return ROUTES.ADMIN_DASHBOARD
      }
      return true
    }

    // Default redirect based on role
    if (to.path === ROUTES.ADMIN_DASHBOARD || to.path === ROUTES.USER_DASHBOARD) {
      return canAccessAdmin(user) ? ROUTES.ADMIN_DASHBOARD : ROUTES.USER_DASHBOARD
    }

    return true
  })
}
