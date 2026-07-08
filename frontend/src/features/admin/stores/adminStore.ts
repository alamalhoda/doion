// Admin Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { AdminService } from '../services/adminService'
import type { AdminStats, FeatureFlag } from '../types/admin'
import { useErrorHandler } from '@/composables/useErrorHandler'
import { useToast } from '@/composables/useToast'

export const useAdminStore = defineStore('admin', () => {
  const stats = ref<AdminStats | null>(null)
  const flags = ref<FeatureFlag[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const errorHandler = useErrorHandler()
  const toast = useToast()

  async function fetchStats(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await AdminService.getStats()
      stats.value = data
    } catch (err: unknown) {
      error.value = errorHandler.getErrorMessage(err)
      errorHandler.handleError(err)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchFlags(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await AdminService.getFeatureFlags()
      flags.value = data
    } catch (err: unknown) {
      error.value = errorHandler.getErrorMessage(err)
      errorHandler.handleError(err)
    } finally {
      isLoading.value = false
    }
  }

  async function updateFlag(key: string, is_enabled: boolean): Promise<void> {
    try {
      const updated = await AdminService.updateFeatureFlag(key, is_enabled)
      const index = flags.value.findIndex(f => f.key === key)
      if (index !== -1) {
        flags.value[index] = updated
      }
    } catch (err: unknown) {
      error.value = errorHandler.getErrorMessage(err)
      errorHandler.handleError(err)
    }
  }

  return {
    stats,
    flags,
    isLoading,
    error,
    fetchStats,
    fetchFlags,
    updateFlag,
  }
})
