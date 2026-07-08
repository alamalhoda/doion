// Admin API service
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { AdminStats, FeatureFlag } from '../types/admin'

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

  static async getFeatureFlags(): Promise<FeatureFlag[]> {
    try {
      const response = await apiClient.get<FeatureFlag[]>(this.basePath + '/feature-flags/')
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getFeatureFlag(key: string): Promise<FeatureFlag> {
    try {
      const response = await apiClient.get<FeatureFlag>(this.basePath + `/feature-flags/${key}/`)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async updateFeatureFlag(key: string, is_enabled: boolean): Promise<FeatureFlag> {
    try {
      const response = await apiClient.patch<FeatureFlag>(this.basePath + `/feature-flags/${key}/`, { is_enabled })
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }
}
