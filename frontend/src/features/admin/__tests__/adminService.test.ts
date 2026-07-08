import { describe, it, expect, vi, beforeEach } from 'vitest'
import { AdminService } from '../services/adminService'
import type { AdminStats, FeatureFlag } from '../types/admin'

// Mock apiClient
const mockGet = vi.fn()
const mockPatch = vi.fn()

vi.mock('@/api/client', () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    patch: (...args: unknown[]) => mockPatch(...args),
  },
}))

vi.mock('@/api/errors', () => ({
  normalizeApiError: (error: unknown) => error,
}))

const basePath = '/api/v1/compliance'

const mockStats: AdminStats = {
  listings: {
    total: 10,
    published: 5,
    pending_moderation: 3,
    rejected: 1,
    expired: 1,
    matched: 0,
  },
  users: {
    total: 20,
    kyc_pending: 2,
    kyc_approved: 18,
  },
  verifications: {
    pending: 2,
  },
  notifications: {
    unread: 5,
  },
}

const mockFlag: FeatureFlag = {
  key: 'new_feature',
  description: 'Enable new feature',
  is_enabled: true,
  is_system: false,
}

describe('AdminService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getStats', () => {
    it('should fetch admin stats', async () => {
      mockGet.mockResolvedValue({ data: mockStats })

      const result = await AdminService.getStats()

      expect(mockGet).toHaveBeenCalledWith(basePath + '/stats/')
      expect(result).toEqual(mockStats)
      expect(result.listings.total).toBe(10)
    })

    it('should throw on error', async () => {
      mockGet.mockRejectedValue(new Error('Network error'))

      await expect(AdminService.getStats()).rejects.toThrow('Network error')
    })
  })

  describe('getFeatureFlags', () => {
    it('should fetch feature flags list', async () => {
      mockGet.mockResolvedValue({ data: [mockFlag] })

      const result = await AdminService.getFeatureFlags()

      expect(mockGet).toHaveBeenCalledWith(basePath + '/feature-flags/')
      expect(result).toHaveLength(1)
      expect(result[0].key).toBe('new_feature')
    })

    it('should return empty array when no flags', async () => {
      mockGet.mockResolvedValue({ data: [] })

      const result = await AdminService.getFeatureFlags()

      expect(result).toEqual([])
    })
  })

  describe('getFeatureFlag', () => {
    it('should fetch a single feature flag', async () => {
      mockGet.mockResolvedValue({ data: mockFlag })

      const result = await AdminService.getFeatureFlag('new_feature')

      expect(mockGet).toHaveBeenCalledWith(basePath + '/feature-flags/new_feature/')
      expect(result.key).toBe('new_feature')
    })
  })

  describe('updateFeatureFlag', () => {
    it('should patch a feature flag', async () => {
      const updated = { ...mockFlag, is_enabled: false }
      mockPatch.mockResolvedValue({ data: updated })

      const result = await AdminService.updateFeatureFlag('new_feature', false)

      expect(mockPatch).toHaveBeenCalledWith(basePath + '/feature-flags/new_feature/', { is_enabled: false })
      expect(result.is_enabled).toBe(false)
    })
  })
})
