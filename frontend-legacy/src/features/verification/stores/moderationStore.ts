import { defineStore } from 'pinia'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { Verification } from '@/features/verification/types/verification'

export const useModerationStore = defineStore('moderation', {
  state: () => ({
    kycQueue: [] as Verification[],
    loading: false,
  }),
  actions: {
    async getKycQueue() {
      this.loading = true
      try {
        const response = await apiClient.get<Verification[] | { results: Verification[] }>(
          '/api/v1/moderation/kyc/',
        )
        const data = response.data
        this.kycQueue = Array.isArray(data) ? data : (data.results ?? [])
        return this.kycQueue
      } catch (error) {
        throw normalizeApiError(error)
      } finally {
        this.loading = false
      }
    },
    async approveKyc(verificationId: string | number) {
      try {
        await apiClient.post(`/api/v1/moderation/kyc/${verificationId}/decision/`, {
          decision: 'approve',
        })
      } catch (error) {
        throw normalizeApiError(error)
      }
    },
    async rejectKyc(
      verificationId: string | number,
      rejectionCode: string,
      rejectionNote: string,
    ) {
      try {
        await apiClient.post(`/api/v1/moderation/kyc/${verificationId}/decision/`, {
          decision: 'reject',
          rejection_code: rejectionCode,
          rejection_note: rejectionNote,
        })
      } catch (error) {
        throw normalizeApiError(error)
      }
    },
  },
})
