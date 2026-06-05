export interface User {
  id: number
  username: string
  email: string
  is_staff: boolean
  is_superuser: boolean
}

export function canAccessAdmin(user: User | null): boolean {
  return user?.is_staff === true
}

export function canAccessUser(user: User | null): boolean {
  // All authenticated users can access user area
  return !!user
}
