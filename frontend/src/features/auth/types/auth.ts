import { User } from '@/utils/permissions'

export interface LoginRequest {
  identifier: string
  password: string
}

export interface LoginResponse {
  access: string
  refresh: string
}

export interface RefreshTokenRequest {
  refresh: string
}

export interface RefreshTokenResponse {
  access: string
}

export interface AuthState {
  token: string | null
  refreshToken: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}