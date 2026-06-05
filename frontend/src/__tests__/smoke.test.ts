import { describe, it, expect } from 'vitest'
import { ROUTES } from '@/constants/routes'

describe('Phase 0 Scaffold - Smoke Tests', () => {
  it('should have auth routes defined', () => {
    expect(ROUTES.LOGIN).toBe('/login')
  })

  it('should have admin dashboard route', () => {
    expect(ROUTES.ADMIN_DASHBOARD).toBe('/admin')
  })

  it('should have user dashboard route', () => {
    expect(ROUTES.USER_DASHBOARD).toBe('/app')
  })

  it('should have not found route', () => {
    expect(ROUTES.NOT_FOUND).toBe('/:pathMatch(.*)*')
  })
})
