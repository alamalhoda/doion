import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { canAccessAdmin, canAccessUser, type User, type UserRole } from '@/utils/permissions'
import { AuthService } from '../services/authService'
import type { AuthUserPayload, LoginRequest, RegisterRequest } from '../types/auth'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'

function mapAuthUserToUser(payload: AuthUserPayload, previous?: User | null): User {
  return {
    id: payload.id,
    username: payload.username,
    email: payload.email,
    name: payload.name,
    phone: payload.phone ?? null,
    role: payload.role as UserRole,
    is_verified: previous?.is_verified ?? false,
    url: previous?.url,
  }
}

function persistTokens(access: string, refresh: string) {
  sessionStorage.setItem('auth_token', access)
  sessionStorage.setItem('refresh_token', refresh)
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${access}`
}

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
      const response = await AuthService.login(credentials)
      token.value = response.access
      refreshToken.value = response.refresh
      persistTokens(response.access, response.refresh)
      user.value = mapAuthUserToUser(response.user)

      try {
        const currentUser = await AuthService.getCurrentUser()
        user.value = currentUser
      } catch {
        // Keep role/phone from login payload if /me is temporarily unavailable
      }
    } catch (err: unknown) {
      error.value = (err as { code?: string }).code || 'UNKNOWN'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function register(data: RegisterRequest) {
    isLoading.value = true
    error.value = null

    try {
      const response = await AuthService.register(data)
      token.value = response.access
      refreshToken.value = response.refresh
      persistTokens(response.access, response.refresh)
      user.value = mapAuthUserToUser({
        ...response.user,
        phone: data.phone ?? null,
      })

      try {
        const currentUser = await AuthService.getCurrentUser()
        user.value = currentUser
      } catch {
        // Keep register payload mapping if /me fails
      }
    } catch (err: unknown) {
      error.value = (err as { code?: string }).code || 'UNKNOWN'
      throw normalizeApiError(err)
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    AuthService.logout()
    delete apiClient.defaults.headers.common['Authorization']
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
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
    }
    try {
      const currentUser = await AuthService.getCurrentUser()
      user.value = currentUser
      if (!token.value && currentUser) {
        token.value = 'session-based'
      }
    } catch {
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
