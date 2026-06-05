import { apiClient } from './client'
import { normalizeApiError } from './errors'
import router from '@/router'
import { ROUTES } from '@/constants/routes'

export function setupInterceptors(store: any) {
  // Response interceptor
  apiClient.interceptors.response.use(
    (response) => response,
    async (error) => {
      // Check for 401 (Unauthenticated)
      if (error.response?.status === 401) {
        // Clear auth state
        store.clearAuth()

        // Redirect to login via router
        await router.push(ROUTES.LOGIN)
      }

      // Normalize and rethrow
      const normalized = normalizeApiError(error)
      return Promise.reject(normalized)
    },
  )

  // Request interceptor - attach token
  apiClient.interceptors.request.use((config) => {
    const token = sessionStorage.getItem('auth_token')
    if (token) {
      config.headers['Authorization'] = `Token ${token}`
    }
    return config
  })
}
