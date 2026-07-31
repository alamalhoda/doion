import type { User } from '@/utils/permissions'

export interface LoginRequest {
  identifier: string
  password: string
}

export interface AuthUserPayload {
  id: number
  username: string
  email: string
  name: string
  role: 'check_holder' | 'investor' | 'moderator' | 'admin'
  phone?: string | null
}

export interface LoginResponse {
  access: string
  refresh: string
  user: AuthUserPayload
}

export interface RefreshTokenRequest {
  refresh: string
}

export interface RefreshTokenResponse {
  access: string
  refresh: string
  user: AuthUserPayload
}

export interface RegisterRequest {
  username: string
  email?: string
  password: string
  password_confirm: string
  name?: string
  phone?: string
  role: 'check_holder' | 'investor'
}

export interface RegisterResponse {
  access: string
  refresh: string
  user: {
    id: number
    username: string
    email: string
    name: string
    role: 'check_holder' | 'investor'
  }
}

export interface AuthState {
  token: string | null
  refreshToken: string | null
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}
