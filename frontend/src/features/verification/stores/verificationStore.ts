import { defineStore } from 'pinia'
import { apiClient } from '@/api/client'
import { VerificationStatus } from '@/features/verification/types/verification'

export const useVerificationStore = defineStore('verification', {
  state: () => ({
    personalInfo: {
      full_name: '',
      national_id: '',
      company_name: null as string | null,
    },
    verification: null as any,
    loading: false,
  }),
  getters: {
    isVerified: (state) => state.verification?.status === VerificationStatus.APPROVED,
    isPending: (state) => state.verification?.status === VerificationStatus.PENDING,
    isRejected: (state) => state.verification?.status === VerificationStatus.REJECTED,
  },
  actions: {
    async startVerification(data: { full_name: string; national_id: string; company_name?: string }) {
      this.loading = true
      try {
        const response = await apiClient.post('/verifications/', data)
        this.verification = response.data
      } finally {
        this.loading = false
      }
    },
    async getMyVerification() {
      this.loading = true
      try {
        const response = await apiClient.get('/verifications/me/')
        this.verification = response.data
        return this.verification
      } finally {
        this.loading = false
      }
    },
  },
})