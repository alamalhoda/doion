import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { LoginRequest, LoginResponse, RefreshTokenResponse } from '../types/auth'
import type { User } from '@/utils/permissions'

export class AuthService {
  static async login(credentials: LoginRequest): Promise<{ access: string; refresh: string }> {
    try {
      const response = await apiClient.post<LoginResponse>('/api/v1/auth/login/', credentials)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async refreshToken(refreshToken: string): Promise<string> {
    try {
      const response = await apiClient.post<RefreshTokenResponse>('/api/v1/auth/refresh/', {
        refresh: refreshToken,
      })
      return response.data.access
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/api/v1/users/me/')
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static logout(): void {
    sessionStorage.removeItem('auth_token')
    sessionStorage.removeItem('refresh_token')
  }
}
