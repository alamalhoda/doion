import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { LoginRequest, LoginResponse } from '../types/auth'
import type { User } from '@/utils/permissions'

export class AuthService {
  static async login(credentials: LoginRequest): Promise<{ token: string }> {
    try {
      const response = await apiClient.post<LoginResponse>('/api/auth-token/', credentials)
      return { token: response.data.token }
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getCurrentUser(token: string): Promise<User> {
    try {
      const response = await apiClient.get<User>('/api/users/me/', {
        headers: { Authorization: `Token ${token}` },
      })
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static logout(): void {
    sessionStorage.removeItem('auth_token')
  }
}
