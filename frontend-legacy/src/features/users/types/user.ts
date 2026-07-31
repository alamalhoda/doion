// User types for future CRUD feature
// This is a shell - full implementation will come in Phase 1+

import type { User } from '@/utils/permissions'

export interface UserDetail extends User {
  date_joined: string
  last_login: string | null
}

export interface CreateUserRequest {
  username: string
  email: string
  password: string
}

export interface UpdateUserRequest {
  email?: string
  first_name?: string
  last_name?: string
}
