import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { canAccessAdmin, canAccessUser, type User } from '@/utils/permissions'
import { AuthService } from '../services/authService'
import type { LoginRequest } from '../types/auth'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(sessionStorage.getItem('auth_token'))
  const refreshToken = ref<string | null>(sessionStorage.getItem('refresh_token'))
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
      const { access, refresh } = await AuthService.login(credentials)
      token.value = access
      refreshToken.value = refresh
      sessionStorage.setItem('auth_token', access)
      sessionStorage.setItem('refresh_token', refresh)

      const currentUser = await AuthService.getCurrentUser()
      user.value = currentUser
    } catch (err: unknown) {
      error.value = (err as { code?: string }).code || 'UNKNOWN'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function register(data: {
    username: string
    email: string
    name: string
    phone: string
    role: 'check_holder' | 'investor'
    password: string
    password_confirm: string
  }) {
    isLoading.value = true
    error.value = null

    try {
      await apiClient.post('/api/v1/identity/register/', data)
    } catch (err: unknown) {
      error.value = (err as { code?: string }).code || 'UNKNOWN'
      throw normalizeApiError(err)
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    AuthService.logout()
    token.value = null
    refreshToken.value = null
    user.value = null
    error.value = null
  }

  function clearAuth() {
    logout()
  }

  async function restoreAuth() {
    const storedToken = sessionStorage.getItem('auth_token')
    const storedRefreshToken = sessionStorage.getItem('refresh_token')
    if (storedToken) {
      token.value = storedToken
      refreshToken.value = storedRefreshToken
    }
    try {
      const currentUser = await AuthService.getCurrentUser()
      user.value = currentUser
      if (!token.value && currentUser) {
        token.value = 'session-based'
      }
    } catch {
      // If we have a stored token but /me/ fails, clear auth
      // If no stored token, user simply isn't logged in — that's fine
      if (token.value) {
        logout()
      }
    }
  }

  return {
    token,
    refreshToken,
    user,
    isLoading,
    error,
    isAuthenticated,
    isAdmin,
    isUser,
    login,
    register,
    logout,
    clearAuth,
    restoreAuth,
  }
})
