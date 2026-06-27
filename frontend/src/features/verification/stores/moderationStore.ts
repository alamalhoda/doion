import { defineStore } from 'pinia'
import { apiClient } from '@/api/client'

export const useModerationStore = defineStore('moderation', {
  state: () => ({
    kycQueue: [] as any[],
    loading: false,
  }),
  actions: {
    async getKycQueue() {
      this.loading = true
      try {
        const response = await apiClient.get('/moderation/kyc/')
        this.kycQueue = response.data.results || response.data
        return this.kycQueue
      } finally {
        this.loading = false
      }
    },
    async approveKyc(verificationId: string) {
      await apiClient.post(`/moderation/kyc/${verificationId}/decision/`, {
        decision: 'approve',
      })
    },
    async rejectKyc(verificationId: string, rejectionCode: string, rejectionNote: string) {
      await apiClient.post(`/moderation/kyc/${verificationId}/decision/`, {
        decision: 'reject',
        rejection_code: rejectionCode,
        rejection_note: rejectionNote,
      })
    },
  },
})