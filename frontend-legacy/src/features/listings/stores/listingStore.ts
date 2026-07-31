// Listing Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ListingService } from '../services/listingService'
import type { ChequeListing, CreateListingRequest, UpdateListingRequest } from '../types/listing'
import { normalizeApiError } from '@/api/errors'

function extractErrorMessage(err: unknown): string {
  const normalized = normalizeApiError(err)
  return normalized.message || 'error.unknown'
}

export const useListingStore = defineStore('listing', () => {
  const listings = ref<ChequeListing[]>([])
  const currentListing = ref<ChequeListing | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const pendingListings = computed(() =>
    listings.value.filter((l) => l.status === 'pending_moderation'),
  )

  const publishedListings = computed(() =>
    listings.value.filter((l) => l.status === 'published'),
  )

  const matchedListings = computed(() =>
    listings.value.filter((l) => l.status === 'matched'),
  )

  async function createListing(data: CreateListingRequest): Promise<ChequeListing> {
    isLoading.value = true
    error.value = null

    try {
      const listing = await ListingService.createListing(data)
      listings.value.unshift(listing)
      return listing
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
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
      error.value = extractErrorMessage(err)
    } finally {
      isLoading.value = false
    }
  }

  async function updateListing(id: string | number, data: UpdateListingRequest): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await ListingService.updateListing(id, data)
      const index = listings.value.findIndex((l) => l.id === Number(id))
      if (index !== -1) {
        listings.value[index] = updated
      }
      if (currentListing.value?.id === Number(id)) {
        currentListing.value = updated
      }
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchListing(id: string | number): Promise<ChequeListing> {
    isLoading.value = true
    error.value = null

    try {
      const listing = await ListingService.getListing(id)
      currentListing.value = listing
      return listing
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAllListings(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await ListingService.getAllListings()
      listings.value = data.filter((l) => l.status === 'pending_moderation')
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchModerationQueue(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await ListingService.getModerationQueue()
      listings.value = data.results
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
    } finally {
      isLoading.value = false
    }
  }

  async function resubmitListing(id: string | number): Promise<ChequeListing> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await ListingService.resubmitListing(id)
      const index = listings.value.findIndex((l) => l.id === Number(id))
      if (index !== -1) {
        listings.value[index] = updated
      }
      if (currentListing.value?.id === Number(id)) {
        currentListing.value = updated
      }
      return updated
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
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
    fetchListing,
    fetchAllListings,
    fetchModerationQueue,
    resubmitListing,
  }
})
