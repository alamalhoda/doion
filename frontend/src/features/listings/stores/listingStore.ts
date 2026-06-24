// Listing Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ListingService } from '../services/listingService'
import type { ChequeListing, CreateListingRequest, ListingFilters, UpdateListingRequest } from '../types/listing'

export const useListingStore = defineStore('listing', () => {
  const listings = ref<ChequeListing[]>([])
  const currentListing = ref<ChequeListing | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const pendingListings = computed(() => 
    listings.value.filter(l => l.status === 'pending_moderation')
  )

  const publishedListings = computed(() => 
    listings.value.filter(l => l.status === 'published')
  )

  const matchedListings = computed(() => 
    listings.value.filter(l => l.status === 'matched')
  )

  async function createListing(data: CreateListingRequest): Promise<ChequeListing> {
    isLoading.value = true
    error.value = null

    try {
      const listing = await ListingService.createListing(data)
      listings.value.unshift(listing)
      return listing
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMyListings(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await ListingService.getMyListings()
      listings.value = data
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  async function updateListing(id: string, data: UpdateListingRequest): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await ListingService.updateListing(id, data)
      const index = listings.value.findIndex(l => l.id === id)
      if (index !== -1) {
        listings.value[index] = updated
      }
      if (currentListing.value?.id === id) {
        currentListing.value = updated
      }
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function deleteListing(id: string): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      await ListingService.deleteListing(id)
      listings.value = listings.value.filter(l => l.id !== id)
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchListing(id: string): Promise<ChequeListing> {
    isLoading.value = true
    error.value = null

    try {
      const listing = await ListingService.getListing(id)
      currentListing.value = listing
      return listing
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMarketplaceListings(params?: ListingFilters & { page?: number; page_size?: number }): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await ListingService.getMarketplaceListings(params)
      listings.value = data
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAllListings(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await ListingService.getAllListings({ status: 'pending_moderation' })
      listings.value = [...listings.value, ...data]
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  return {
    listings,
    currentListing,
    isLoading,
    error,
    pendingListings,
    publishedListings,
    matchedListings,
    createListing,
    fetchMyListings,
    updateListing,
    deleteListing,
    fetchListing,
    fetchMarketplaceListings,
    fetchAllListings,
  }
})