// Listing API service — MASTER_API_CONTRACT.md §§5–8, 10
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { ListResponse } from '@/api/types'
import type {
  ChequeListing,
  CreateListingRequest,
  UpdateListingRequest,
  ListingFilters,
  ModerateDecisionRequest,
  ModerationDecisionResponse,
  MarketplaceLatestListing,
} from '../types/listing'

export class ListingService {
  private static basePath = '/api/v1/listings'
  private static moderationPath = '/api/v1/moderation'
  private static marketplacePath = '/api/v1/marketplace'

  static async createListing(data: CreateListingRequest): Promise<ChequeListing> {
    try {
      const response = await apiClient.post<ChequeListing>(this.basePath + '/', data)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getMyListings(): Promise<ChequeListing[]> {
    try {
      const response = await apiClient.get<ChequeListing[]>(this.basePath + '/my/')
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getListing(id: string | number): Promise<ChequeListing> {
    try {
      const response = await apiClient.get<ChequeListing>(this.basePath + `/${id}/`)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async updateListing(
    id: string | number,
    data: UpdateListingRequest,
  ): Promise<ChequeListing> {
    try {
      const response = await apiClient.patch<ChequeListing>(this.basePath + `/${id}/`, data)
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async uploadDocument(
    listingId: string | number,
    file: File,
    documentType: string,
  ): Promise<{ id: number; document_type: string; file: string; file_size: number }> {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('document_type', documentType)
      const response = await apiClient.post(this.basePath + `/${listingId}/documents/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getAllListings(params?: ListingFilters): Promise<ChequeListing[]> {
    try {
      const response = await apiClient.get<ChequeListing[]>(this.basePath + '/', { params })
      return Array.isArray(response.data) ? response.data : []
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getMarketplaceListings(
    params?: ListingFilters,
  ): Promise<ListResponse<ChequeListing>> {
    try {
      const response = await apiClient.get<ListResponse<ChequeListing>>(
        this.marketplacePath + '/listings/',
        { params },
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getLatestMarketplaceListings(): Promise<MarketplaceLatestListing[]> {
    try {
      const response = await apiClient.get<MarketplaceLatestListing[]>(
        this.marketplacePath + '/listings/latest/',
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getModerationQueue(params?: {
    page?: number
  }): Promise<ListResponse<ChequeListing>> {
    try {
      const response = await apiClient.get<ListResponse<ChequeListing>>(
        this.moderationPath + '/queue/',
        { params },
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async moderateListing(
    id: string | number,
    data: ModerateDecisionRequest,
  ): Promise<ModerationDecisionResponse> {
    try {
      const response = await apiClient.post<ModerationDecisionResponse>(
        this.moderationPath + `/${id}/decision/`,
        data,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async resubmitListing(id: string | number): Promise<ChequeListing> {
    try {
      const response = await apiClient.post<ChequeListing>(
        this.moderationPath + `/${id}/resubmit/`,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }
}
