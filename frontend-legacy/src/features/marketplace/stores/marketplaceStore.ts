// Marketplace Pinia store
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ListingService } from '../../listings/services/listingService'
import type { ChequeListing } from '../../listings/types/listing'
import { normalizeApiError } from '@/api/errors'

export interface MarketplaceFilters {
  risk_tier?: 'low' | 'medium' | 'high'
  min_amount?: number
  max_amount?: number
  max_days_to_due?: number
  issuer_type?: 'legal' | 'natural'
  bank_name?: string
}

export const useMarketplaceStore = defineStore('marketplace', () => {
  const listings = ref<ChequeListing[]>([])
  const totalCount = ref(0)
  const page = ref(1)
  /** Fixed by backend PAGE_SIZE=20; page_size query is not supported */
  const pageSize = ref(20)
  const filters = ref<MarketplaceFilters>({})
  const sortBy = ref<string>('-created_at')
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchListings(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const params: Record<string, unknown> = {
        page: page.value,
        ordering: sortBy.value,
      }

      if (filters.value.risk_tier) {
        params.risk_tier = filters.value.risk_tier
      }
      if (filters.value.min_amount !== undefined) {
        params.min_amount = filters.value.min_amount
      }
      if (filters.value.max_amount !== undefined) {
        params.max_amount = filters.value.max_amount
      }
      if (filters.value.max_days_to_due !== undefined) {
        params.max_days_to_due = filters.value.max_days_to_due
      }
      if (filters.value.issuer_type) {
        params.issuer_type = filters.value.issuer_type
      }
      if (filters.value.bank_name) {
        params.bank_name = filters.value.bank_name
      }

      const data = await ListingService.getMarketplaceListings(params)
      listings.value = data.results
      totalCount.value = data.count
    } catch (err: unknown) {
      error.value = normalizeApiError(err).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  function setFilter(key: keyof MarketplaceFilters, value: unknown): void {
    filters.value = { ...filters.value, [key]: value }
    page.value = 1
  }

  function setSort(value: string): void {
    sortBy.value = value
    page.value = 1
  }

  function setPage(value: number): void {
    page.value = value
  }

  function resetFilters(): void {
    filters.value = {}
    sortBy.value = '-created_at'
    page.value = 1
  }

  return {
    listings,
    totalCount,
    page,
    pageSize,
    filters,
    sortBy,
    isLoading,
    error,
    fetchListings,
    setFilter,
    setSort,
    setPage,
    resetFilters,
  }
})
