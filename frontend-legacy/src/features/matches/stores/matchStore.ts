// Match Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { MatchService } from '../services/matchService'
import type { Match, CreateMatchRequest, UpdateMatchStatusRequest } from '../types/match'

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

  const completedMatches = computed(() =>
    matches.value.filter(m => m.status === 'declined' || m.status === 'cancelled' || m.status === 'off_platform_confirmed' || m.status === 'settled')
  )

  async function createMatch(data: CreateMatchRequest): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const match = await MatchService.createMatch(data)
      matches.value.unshift(match)
      return match
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
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
      error.value = (err as { message?: string }).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  async function updateMatchStatus(id: number | string, data: UpdateMatchStatusRequest): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const updated = await MatchService.updateMatchStatus(id, data)
      const numericId = Number(id)
      const index = matches.value.findIndex(m => m.id === numericId)
      if (index !== -1) {
        matches.value[index] = updated
      }
      if (currentMatch.value?.id === numericId) {
        currentMatch.value = updated
      }
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMatch(id: number | string): Promise<Match> {
    isLoading.value = true
    error.value = null

    try {
      const match = await MatchService.getMatch(id)
      currentMatch.value = match
      return match
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
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
    completedMatches,
    createMatch,
    fetchMyMatches,
    updateMatchStatus,
    fetchMatch,
  }
})