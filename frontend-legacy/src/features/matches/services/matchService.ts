// Match service — MASTER_API_CONTRACT.md §9
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type {
  Match,
  CreateMatchRequest,
  UpdateMatchStatusRequest,
  MatchStatus,
  ListingSummary,
  UserSummary,
  SettlementType,
} from '../types/match'
import type { ListResponse } from '@/api/types'

interface RawListing {
  id: number
  bank_name?: string
  face_amount?: string | number
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
  settlement_type: SettlementType
  final_discount_rate?: string | number | null
  terms?: string | null
  message?: string | null
  created_at: string
  updated_at: string
}

function mapUser(raw: RawUser | null): UserSummary {
  return {
    id: raw?.id ?? 0,
    username: raw?.username ?? '',
    name: raw?.name ?? '',
  }
}

function mapListing(raw: RawListing | null): ListingSummary {
  return {
    id: raw?.id ?? 0,
    bank_name: raw?.bank_name ?? '',
    face_amount: raw?.face_amount != null ? String(raw.face_amount) : '0',
    due_date: raw?.due_date ?? '',
    status: raw?.status ?? '',
    created_at: raw?.created_at ?? '',
    updated_at: raw?.updated_at ?? '',
  }
}

function mapMatch(raw: RawMatch): Match {
  return {
    id: raw.id,
    listing: mapListing(raw.listing),
    investor: mapUser(raw.investor),
    check_holder: mapUser(raw.check_holder),
    status: raw.status as MatchStatus,
    settlement_type: raw.settlement_type,
    final_discount_rate:
      raw.final_discount_rate == null ? null : String(raw.final_discount_rate),
    terms: raw.terms ?? '',
    message: raw.message ?? '',
    created_at: raw.created_at,
    updated_at: raw.updated_at,
  }
}

function extractMatchList(payload: RawMatch[] | ListResponse<RawMatch>): RawMatch[] {
  if (Array.isArray(payload)) return payload
  return payload.results ?? []
}

export const MatchService = {
  async createMatch(data: CreateMatchRequest): Promise<Match> {
    try {
      const response = await apiClient.post<RawMatch>('/api/v1/matches/', {
        listing_id: data.listing_id,
        message: data.message ?? '',
      })
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async getMyMatches(params?: { page?: number }): Promise<Match[]> {
    try {
      const response = await apiClient.get<RawMatch[] | ListResponse<RawMatch>>(
        '/api/v1/matches/my/',
        { params },
      )
      return extractMatchList(response.data).map(mapMatch)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async listMatches(params?: { page?: number }): Promise<Match[]> {
    try {
      const response = await apiClient.get<RawMatch[] | ListResponse<RawMatch>>(
        '/api/v1/matches/',
        { params },
      )
      return extractMatchList(response.data).map(mapMatch)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async getMatch(id: number | string): Promise<Match> {
    try {
      const response = await apiClient.get<RawMatch>(`/api/v1/matches/${id}/`)
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async updateMatchStatus(id: number | string, data: UpdateMatchStatusRequest): Promise<Match> {
    try {
      let response
      switch (data.status) {
        case 'accepted':
          response = await apiClient.post<RawMatch>(`/api/v1/matches/${id}/accept/`)
          break
        case 'declined':
          response = await apiClient.post<RawMatch>(`/api/v1/matches/${id}/decline/`, {
            note: data.note ?? data.terms ?? '',
          })
          break
        case 'cancelled':
          response = await apiClient.post<RawMatch>(`/api/v1/matches/${id}/cancel/`)
          break
        case 'off_platform_confirmed':
          response = await apiClient.post<RawMatch>(
            `/api/v1/matches/${id}/confirm-off-platform/`,
          )
          break
        case 'settled':
        case 'pending':
        default:
          response = await apiClient.patch<RawMatch>(`/api/v1/matches/${id}/status/`, {
            status: data.status,
            final_discount_rate: data.final_discount_rate,
            terms: data.terms,
          })
          break
      }
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },

  async patchMatchStatus(id: number | string, data: UpdateMatchStatusRequest): Promise<Match> {
    try {
      const response = await apiClient.patch<RawMatch>(`/api/v1/matches/${id}/status/`, {
        status: data.status,
        final_discount_rate: data.final_discount_rate,
        terms: data.terms,
      })
      return mapMatch(response.data)
    } catch (error) {
      throw normalizeApiError(error)
    }
  },
}
