import { type Router } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { canAccessAdmin, canAccessUser } from '@/utils/permissions'
import { ROUTES } from '@/constants/routes'
import { useVerificationStore } from '@/features/verification/stores/verificationStore'

const PUBLIC_ROUTES = [ROUTES.LOGIN, ROUTES.REGISTER]

export function setupRouterGuards(router: Router) {
  router.beforeEach(async (to) => {
    const authStore = useAuthStore()
    const verificationStore = useVerificationStore()
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

    // KYC-specific guards
    if (to.path.startsWith(ROUTES.VERIFICATION_KYC_START)) {
      const verification = await verificationStore.getMyVerification()

      if (!verification || verification.status === 'rejected') {
        return true
      }

      if (verification.status === 'approved' && to.path !== ROUTES.VERIFICATION_KYC_STATUS) {
        return ROUTES.USER_DASHBOARD
      }
    }

    // Check KYC status for listing creation
    if (to.path === ROUTES.USER_CREATE_LISTING) {
      const verification = await verificationStore.getMyVerification()
      if (!verification || verification.status !== 'approved') {
        return `${ROUTES.VERIFICATION_KYC_START}?redirect=${encodeURIComponent(to.fullPath)}`
      }
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
