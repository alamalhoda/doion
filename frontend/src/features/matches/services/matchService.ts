// Real Match service - connects to Phase 6 Matching API
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { Match, CreateMatchRequest, UpdateMatchStatusRequest, MatchStatus, ListingSummary, UserSummary } from '../types/match'

interface RawListing {
  id: number
  bank_name?: string
  face_amount?: number
  due_date?: string
  status?: string
  created_at?: string
  updated_at?: string
}

interface RawUser {
  id: number
  username: string
  name?: string
}

interface RawMatch {
  id: number
  listing: RawListing | null
  investor: RawUser | null
  check_holder: RawUser | null
  status: string
  settlement_type: 'off_platform' | 'escrow' | 'principal_ledger'
  final_discount_rate?: number | null
  terms?: string | null
  message?: string | null
  created_at: string
  updated_at: string
}

function mapUser(raw: RawUser | null): UserSummary | undefined {
  if (!raw) return undefined
  return { id: String(raw.id), username: raw.username, full_name: raw.name }
}

function mapListing(raw: RawListing | null): ListingSummary | undefined {
  if (!raw) return undefined
  return {
    id: String(raw.id),
    bank_name: raw.bank_name ?? '',
    face_amount: raw.face_amount ?? 0,
    due_date: raw.due_date ?? '',
    status: raw.status ?? '',
    created_at: raw.created_at ?? '',
    updated_at: raw.updated_at ?? '',
  }
}

function mapMatch(raw: RawMatch): Match {
  return {
    id: String(raw.id),
    listing_id: raw.listing ? String(raw.listing.id) : '',
    investor_id: raw.investor ? String(raw.investor.id) : '',
    check_holder_id: raw.check_holder ? String(raw.check_holder.id) : '',
    status: raw.status as MatchStatus,
    settlement_type: raw.settlement_type,
    final_discount_rate: raw.final_discount_rate ?? null,
    terms: raw.terms ?? null,
    message: raw.message ?? null,
    created_at: raw.created_at,
    updated_at: raw.updated_at,
    listing: mapListing(raw.listing),
    investor: mapUser(raw.investor),
    check_holder: mapUser(raw.check_holder),
  }
}

export const MatchService = {
  async createMatch(data: CreateMatchRequest): Promise<Match> {
    try {
      const response = await apiClient.post<RawMatch>('/api/v1/matches/', {
        listing_id: Number(data.listing_id as string),
        message: data.message ?? '',
      })
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async getMyMatches(): Promise<Match[]> {
    try {
      const response = await apiClient.get<RawMatch[] | { results: RawMatch[] }>('/api/v1/matches/')
      const payload = response.data
      const rawList = Array.isArray(payload) ? payload : (payload as { results: RawMatch[] }).results ?? []
      return rawList.map(mapMatch)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async getMatch(id: string): Promise<Match> {
    try {
      const response = await apiClient.get<RawMatch>(`/api/v1/matches/${id}/`)
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async updateMatchStatus(id: string, data: UpdateMatchStatusRequest): Promise<Match> {
    try {
      let url = ''
      let body: Record<string, unknown> = {}
      switch (data.status) {
        case 'accepted':
          url = `/api/v1/matches/${id}/accept/`
          break
        case 'declined':
          url = `/api/v1/matches/${id}/decline/`
          body = { note: data.terms ?? '' }
          break
        case 'cancelled':
          url = `/api/v1/matches/${id}/cancel/`
          break
        case 'off_platform_confirmed':
          url = `/api/v1/matches/${id}/confirm-off-platform/`
          break
        case 'settled':
          // No dedicated backend action for final settlement; treated as confirm-off-platform
          url = `/api/v1/matches/${id}/confirm-off-platform/`
          break
        default:
          throw new Error(`Unsupported match status transition: ${data.status}`)
      }
      const response = await apiClient.post<RawMatch>(url, body)
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },
}
