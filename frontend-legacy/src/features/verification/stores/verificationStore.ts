import { defineStore } from 'pinia'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import { VerificationStatus, type Verification } from '@/features/verification/types/verification'

export const useVerificationStore = defineStore('verification', {
  state: () => ({
    personalInfo: {
      full_name: '',
      national_id: '',
      company_name: null as string | null,
    },
    verification: null as Verification | null,
    loading: false,
  }),
  getters: {
    isVerified: (state) => state.verification?.status === VerificationStatus.APPROVED,
    isPending: (state) => state.verification?.status === VerificationStatus.PENDING,
    isRejected: (state) => state.verification?.status === VerificationStatus.REJECTED,
  },
  actions: {
    async startVerification(formData: FormData) {
      this.loading = true
      try {
        const response = await apiClient.post<Verification>(
          '/api/v1/verifications/',
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } },
        )
        this.verification = response.data
        return this.verification
      } catch (error) {
        throw normalizeApiError(error)
      } finally {
        this.loading = false
      }
    },
    async getMyVerification() {
      this.loading = true
      try {
        const response = await apiClient.get<Verification>('/api/v1/verifications/me/')
        this.verification = response.data
        return this.verification
      } catch (error) {
        const normalized = normalizeApiError(error)
        if (normalized.code === 'NOT_FOUND_ERROR' || normalized.status === 404) {
          this.verification = null
          return null
        }
        throw normalized
      } finally {
        this.loading = false
      }
    },
  },
})
