import { describe, it, expect } from 'vitest'
import { ROUTES } from '@/constants/routes'

describe('Phase 1 - Identity & Landing', () => {
  it('should have register route defined', () => {
    expect(ROUTES.REGISTER).toBe('/register')
  })

  it('should have landing route at root', () => {
    expect(ROUTES.LANDING).toBe('/')
  })

  it('should have identity routes', () => {
    expect(ROUTES.IDENTITY_ME).toBe('/identity/me')
    expect(ROUTES.IDENTITY_PROFILE).toBe('/identity/profile')
  })
})
