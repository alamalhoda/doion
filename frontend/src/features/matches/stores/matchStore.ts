// Match Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { MatchService } from '../services/matchService'
import type { Match, CreateMatchRequest, DeclineMatchRequest } from '../types/match'

function extractErrorMessage(err: unknown): string {
  const anyErr = err as { response?: { data?: { error?: { message?: string } } } }
  return anyErr?.response?.data?.error?.message || (err as Error).message || 'error.unknown'
}

export const useMatchStore = defineStore('match', () => {
  const matches = ref<Match[]>([])
  const currentMatch = ref<Match | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const pendingMatches = computed(() =>
    matches.value.filter(m => m.status === 'pending')
  )

  const acceptedMatches = computed(() =>
    matches.value.filter(m => m.status === 'accepted')
  )

  const declinedMatches = computed(() =>
    matches.value.filter(m => m.status === 'declined')
  )

  const cancelledMatches = computed(() =>
    matches.value.filter(m => m.status === 'cancelled')
  )

  const offPlatformConfirmedMatches = computed(() =>
    matches.value.filter(m => m.status === 'off_platform_confirmed')
  )

  const settledMatches = computed(() =>
    matches.value.filter(m => m.status === 'settled')
  )

  const terminalMatches = computed(() =>
    matches.value.filter(m =>
      m.status === 'declined' ||
      m.status === 'cancelled' ||
      m.status === 'off_platform_confirmed' ||
      m.status === 'settled'
    )
  )

  async function createMatch(data: CreateMatchRequest): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const match = await MatchService.createMatch(data)
      matches.value.unshift(match)
      return match
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMyMatches(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const data = await MatchService.getMyMatches()
      matches.value = data
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
    } finally {
      isLoading.value = false
    }
  }

  async function acceptMatch(id: string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await MatchService.acceptMatch(id)
      const index = matches.value.findIndex(m => m.id === id)
      if (index !== -1) {
        matches.value[index] = updated
      }
      if (currentMatch.value?.id === id) {
        currentMatch.value = updated
      }
      return updated
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function declineMatch(id: string, note?: string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await MatchService.declineMatch(id, note)
      const index = matches.value.findIndex(m => m.id === id)
      if (index !== -1) {
        matches.value[index] = updated
      }
      if (currentMatch.value?.id === id) {
        currentMatch.value = updated
      }
      return updated
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function cancelMatch(id: string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await MatchService.cancelMatch(id)
      const index = matches.value.findIndex(m => m.id === id)
      if (index !== -1) {
        matches.value[index] = updated
      }
      if (currentMatch.value?.id === id) {
        currentMatch.value = updated
      }
      return updated
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function confirmOffPlatform(id: string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await MatchService.confirmOffPlatform(id)
      const index = matches.value.findIndex(m => m.id === id)
      if (index !== -1) {
        matches.value[index] = updated
      }
      if (currentMatch.value?.id === id) {
        currentMatch.value = updated
      }
      return updated
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMatch(id: string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const match = await MatchService.getMatch(id)
      currentMatch.value = match
      return match
    } catch (err: unknown) {
      error.value = extractErrorMessage(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    matches,
    currentMatch,
    isLoading,
    error,
    pendingMatches,
    acceptedMatches,
    declinedMatches,
    cancelledMatches,
    offPlatformConfirmedMatches,
    settledMatches,
    terminalMatches,
    createMatch,
    fetchMyMatches,
    acceptMatch,
    declineMatch,
    cancelMatch,
    confirmOffPlatform,
    fetchMatch,
  }
})
