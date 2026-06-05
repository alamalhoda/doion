import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { canAccessAdmin, canAccessUser, type User } from '@/utils/permissions'
import { AuthService } from '../services/authService'
import type { LoginRequest } from '../types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(sessionStorage.getItem('auth_token'))
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => canAccessAdmin(user.value))
  const isUser = computed(() => canAccessUser(user.value))

  async function login(credentials: LoginRequest) {
    isLoading.value = true
    error.value = null

    try {
      const { token: newToken } = await AuthService.login(credentials)
      token.value = newToken
      sessionStorage.setItem('auth_token', newToken)

      // Fetch current user
      const currentUser = await AuthService.getCurrentUser(newToken)
      user.value = currentUser
    } catch (err: any) {
      error.value = err.code || 'UNKNOWN'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    AuthService.logout()
    token.value = null
    user.value = null
    error.value = null
  }

  function clearAuth() {
    logout()
  }

  async function restoreAuth() {
    const storedToken = sessionStorage.getItem('auth_token')
    if (storedToken) {
      try {
        const currentUser = await AuthService.getCurrentUser(storedToken)
        token.value = storedToken
        user.value = currentUser
      } catch {
        logout()
      }
    }
    // Return even if no token - this allows app to mount without auth
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    isUser,
    login,
    logout,
    clearAuth,
    restoreAuth,
  }
})
