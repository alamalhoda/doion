import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAdminStore } from '../stores/adminStore'
import { AdminService } from '../services/adminService'

vi.mock('../services/adminService', () => ({
  AdminService: {
    getStats: vi.fn(),
    getFeatureFlags: vi.fn(),
    updateFeatureFlag: vi.fn(),
    toggleFeatureFlag: vi.fn(),
  },
}))

vi.mock('@/composables/useToast', () => ({
  useToast: () => ({
    showToast: vi.fn(),
  }),
}))

describe('adminStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('initial state', () => {
    it('should have empty initial state', () => {
      const store = useAdminStore()

      expect(store.stats).toBeNull()
      expect(store.flags).toEqual([])
      expect(store.isLoading).toBe(false)
      expect(store.error).toBeNull()
    })
  })

  describe('fetchStats', () => {
    it('should populate stats and toggle loading', async () => {
      const store = useAdminStore()
      const mockStats = {
        listings: { total: 10, published: 5, pending_moderation: 3, rejected: 1, expired: 1, matched: 0 },
        users: { total: 20, kyc_pending: 2, kyc_approved: 18 },
        verifications: { pending: 2 },
        notifications: { unread: 5 },
      }
      vi.mocked(AdminService.getStats).mockResolvedValue(mockStats)

      await store.fetchStats()

      expect(store.stats).toEqual(mockStats)
      expect(store.isLoading).toBe(false)
      expect(store.error).toBeNull()
    })

    it('should set error on failure', async () => {
      const store = useAdminStore()
      vi.mocked(AdminService.getStats).mockRejectedValue(new Error('API error'))

      await store.fetchStats()

      expect(store.error).toBeTruthy()
      expect(store.isLoading).toBe(false)
    })

    it('should toggle isLoading true then false', async () => {
      const store = useAdminStore()
      let resolvePromise: (value: unknown) => void
      const promise = new Promise(resolve => { resolvePromise = resolve })
      vi.mocked(AdminService.getStats).mockReturnValue(promise as Promise<unknown>)

      const fetchPromise = store.fetchStats()
      expect(store.isLoading).toBe(true)

      resolvePromise!({ listings: { total: 0, published: 0, pending_moderation: 0, rejected: 0, expired: 0, matched: 0 }, users: { total: 0, kyc_pending: 0, kyc_approved: 0 }, verifications: { pending: 0 }, notifications: { unread: 0 } })
      await fetchPromise

      expect(store.isLoading).toBe(false)
    })
  })

  describe('fetchFlags', () => {
    it('should populate flags', async () => {
      const store = useAdminStore()
      const mockFlags = [{ key: 'flag1', description: 'Desc', is_enabled: true, is_system: false }]
      vi.mocked(AdminService.getFeatureFlags).mockResolvedValue(mockFlags)

      await store.fetchFlags()

      expect(store.flags).toEqual(mockFlags)
      expect(store.isLoading).toBe(false)
    })
  })

  describe('updateFlag', () => {
    it('should update flag in local state', async () => {
      const store = useAdminStore()
      store.flags = [{ key: 'flag1', description: 'Desc', is_enabled: false, is_system: false }]
      const updated = { key: 'flag1', description: 'Desc', is_enabled: true, is_system: false }
      vi.mocked(AdminService.updateFeatureFlag).mockResolvedValue(updated)

      await store.updateFlag('flag1', true)

      expect(store.flags[0].is_enabled).toBe(true)
    })
  })
})
