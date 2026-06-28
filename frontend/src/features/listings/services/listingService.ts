// Listing API service
import { apiClient } from '@/api/client'
import type { ChequeListing, CreateListingRequest, UpdateListingRequest, ListingFilters } from '../types/listing'

export class ListingService {
  private static basePath = '/api/v1/listings'

  static async createListing(data: CreateListingRequest): Promise<ChequeListing> {
    const response = await apiClient.post(this.basePath + '/', data)
    return response.data
  }

  static async getMyListings(): Promise<ChequeListing[]> {
    const response = await apiClient.get(this.basePath + '/my/')
    return response.data
  }

  static async getListing(id: string | number): Promise<ChequeListing> {
    const response = await apiClient.get(this.basePath + `/${id}/`)
    return response.data
  }

  static async updateListing(id: string | number, data: UpdateListingRequest): Promise<ChequeListing> {
    const response = await apiClient.patch(this.basePath + `/${id}/`, data)
    return response.data
  }

  static async deleteListing(id: string | number): Promise<void> {
    await apiClient.delete(this.basePath + `/${id}/`)
  }

  static async uploadDocument(listingId: string | number, file: File, documentType: string): Promise<void> {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('document_type', documentType)
    await apiClient.post(this.basePath + `/${listingId}/documents/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }

  static async getAllListings(params?: ListingFilters & { page?: number; page_size?: number }): Promise<ChequeListing[]> {
    const response = await apiClient.get(this.basePath + '/', { params })
    return response.data
  }

  static async getMarketplaceListings(params?: ListingFilters & { page?: number; page_size?: number }): Promise<ChequeListing[]> {
    const response = await apiClient.get(this.basePath + '/', { params })
    return response.data
  }
}