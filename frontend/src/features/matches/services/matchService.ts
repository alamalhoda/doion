// Match API service
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type { Match, CreateMatchRequest, DeclineMatchRequest } from '../types/match'

export class MatchService {
  private static basePath = '/api/v1/matches'

  private static async request<T>(promise: Promise<{ data: T }>): Promise<T> {
    try {
      return (await promise).data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async createMatch(data: CreateMatchRequest): Promise<Match> {
    return this.request(apiClient.post(this.basePath + '/', data))
  }

  static async getMyMatches(): Promise<Match[]> {
    return this.request(apiClient.get(this.basePath + '/'))
  }

  static async getMatch(id: string | number): Promise<Match> {
    return this.request(apiClient.get(this.basePath + `/${id}/`))
  }

  static async acceptMatch(id: string | number): Promise<Match> {
    return this.request(apiClient.post(this.basePath + `/${id}/accept/`))
  }

  static async declineMatch(id: string | number, note?: string): Promise<Match> {
    return this.request(apiClient.post(this.basePath + `/${id}/decline/`, { note } as DeclineMatchRequest))
  }

  static async cancelMatch(id: string | number): Promise<Match> {
    return this.request(apiClient.post(this.basePath + `/${id}/cancel/`))
  }

  static async confirmOffPlatform(id: string | number): Promise<Match> {
    return this.request(apiClient.post(this.basePath + `/${id}/confirm-off-platform/`))
  }
}
