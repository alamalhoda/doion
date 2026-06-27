import type { UserRole } from '@/features/listings/types/listing'

export interface User {
  id: number
  username: string
  email: string
  name?: string
  phone?: string | null
  is_staff: boolean
  is_superuser: boolean
  role: UserRole
  is_verified: boolean
}

export function canAccessAdmin(user: User | null): boolean {
  return user?.is_staff === true || user?.role === 'admin' || user?.role === 'moderator'
}

export function canAccessUser(user: User | null): boolean {
  return !!user
}

export function isCheckHolder(user: User | null): boolean {
  return user?.role === 'check_holder'
}

export function isInvestor(user: User | null): boolean {
  return user?.role === 'investor' || user?.role === 'institutional_investor'
}
