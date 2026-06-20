import type { UserRole } from '@/features/listings/types/listing'

export interface User {
  id: number
  username: string
  email: string
  is_staff: boolean
  is_superuser: boolean
  role: UserRole
  is_verified: boolean
  first_name?: string
  last_name?: string
}

export function canAccessAdmin(user: User | null): boolean {
  return user?.is_staff === true || user?.role === 'Admin' || user?.role === 'Moderator'
}

export function canAccessUser(user: User | null): boolean {
  // All authenticated users can access user area
  return !!user
}

export function isCheckHolder(user: User | null): boolean {
  return user?.role === 'CheckHolder'
}

export function isInvestor(user: User | null): boolean {
  return user?.role === 'Investor' || user?.role === 'InstitutionalInvestor'
}