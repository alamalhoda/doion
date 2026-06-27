import { type Router } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { canAccessAdmin, canAccessUser } from '@/utils/permissions'
import { ROUTES } from '@/constants/routes'

const PUBLIC_ROUTES = [ROUTES.LOGIN, ROUTES.REGISTER]

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const authStore = useAuthStore()
    const isAuthenticated = authStore.isAuthenticated
    const user = authStore.user

    console.log('[Guard]', {
      to: to.path,
      isAuthenticated,
      hasUser: !!user,
      role: user?.role,
      token: !!authStore.token,
    })

    if (to.meta.public || PUBLIC_ROUTES.includes(to.path)) {
      if (isAuthenticated) {
        return canAccessAdmin(user) ? ROUTES.ADMIN_DASHBOARD : ROUTES.USER_DASHBOARD
      }
      return true
    }

    if (!isAuthenticated) {
      return ROUTES.LOGIN
    }

    if (to.meta.requiresAdmin) {
      if (!canAccessAdmin(user)) {
        return ROUTES.USER_DASHBOARD
      }
      return true
    }

    if (to.meta.requiresUser) {
      if (!canAccessUser(user)) {
        return ROUTES.ADMIN_DASHBOARD
      }
      return true
    }

    return true
  })
}
