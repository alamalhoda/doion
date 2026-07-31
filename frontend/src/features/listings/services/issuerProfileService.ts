// Issuer Profile API — MASTER_API_CONTRACT.md §7
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { IssuerProfile } from '../types/listing'

export interface CreateIssuerProfileRequest {
  national_or_company_id: string
  name: string
}

export class IssuerProfileService {
  private static basePath = '/api/v1/issuer-profiles'

  static async list(): Promise<IssuerProfile[]> {
    try {
      const response = await apiClient.get<IssuerProfile[] | { results: IssuerProfile[] }>(
        this.basePath + '/',
      )
      const data = response.data
      return Array.isArray(data) ? data : (data.results ?? [])
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async create(data: CreateIssuerProfileRequest): Promise<IssuerProfile> {
    try {
      const response = await apiClient.post<IssuerProfile>(this.basePath + '/', data)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async get(id: number | string): Promise<IssuerProfile> {
    try {
      const response = await apiClient.get<IssuerProfile>(this.basePath + `/${id}/`)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async update(
    id: number | string,
    data: Partial<CreateIssuerProfileRequest>,
  ): Promise<IssuerProfile> {
    try {
      const response = await apiClient.patch<IssuerProfile>(this.basePath + `/${id}/`, data)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async remove(id: number | string): Promise<void> {
    try {
      await apiClient.delete(this.basePath + `/${id}/`)
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  /** Find existing issuer by national/company id, or create one. */
  static async findOrCreate(data: CreateIssuerProfileRequest): Promise<IssuerProfile> {
    const existing = await this.list()
    const match = existing.find(
      (p) => p.national_or_company_id === data.national_or_company_id,
    )
    if (match) return match
    return this.create(data)
  }
}
