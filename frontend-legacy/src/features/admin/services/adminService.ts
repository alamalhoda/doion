// Admin API service — MASTER_API_CONTRACT.md §12
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { ListResponse } from '@/api/types'
import type { AdminStats, FeatureFlag, AuditEvent } from '../types/admin'

export class AdminService {
  private static basePath = '/api/v1/compliance'

  static async getStats(): Promise<AdminStats> {
    try {
      const response = await apiClient.get<AdminStats>(this.basePath + '/stats/')
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getFeatureFlags(params?: { page?: number }): Promise<FeatureFlag[]> {
    try {
      const response = await apiClient.get<FeatureFlag[] | ListResponse<FeatureFlag>>(
        this.basePath + '/feature-flags/',
        { params },
      )
      const data = response.data
      return Array.isArray(data) ? data : (data.results ?? [])
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getFeatureFlag(key: string): Promise<FeatureFlag> {
    try {
      const response = await apiClient.get<FeatureFlag>(
        this.basePath + `/feature-flags/${key}/`,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async updateFeatureFlag(key: string, is_enabled: boolean): Promise<FeatureFlag> {
    try {
      const response = await apiClient.patch<FeatureFlag>(
        this.basePath + `/feature-flags/${key}/`,
        { is_enabled },
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async toggleFeatureFlag(key: string): Promise<FeatureFlag> {
    try {
      const response = await apiClient.post<FeatureFlag>(
        this.basePath + `/feature-flags/${key}/toggle/`,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getAuditEvents(params?: {
    page?: number
    page_size?: number
  }): Promise<ListResponse<AuditEvent>> {
    try {
      const response = await apiClient.get<ListResponse<AuditEvent>>(
        this.basePath + '/audit/',
        { params },
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }
}
