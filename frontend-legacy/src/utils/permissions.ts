export type UserRole = 'check_holder' | 'investor' | 'moderator' | 'admin'

/** Current user shape from GET /api/v1/users/me/ and identity serializers */
export interface User {
  id: number
  username: string
  email: string
  name?: string
  phone?: string | null
  role: UserRole
  is_verified: boolean
  url?: string
}

export function canAccessAdmin(user: User | null): boolean {
  return user?.role === 'admin' || user?.role === 'moderator'
}

export function canAccessModeration(user: User | null): boolean {
  return user?.role === 'moderator' || user?.role === 'admin'
}

export function canAccessUser(user: User | null): boolean {
  return !!user
}

export function isCheckHolder(user: User | null): boolean {
  return user?.role === 'check_holder'
}

export function isInvestor(user: User | null): boolean {
  return user?.role === 'investor'
}
