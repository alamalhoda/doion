// Mock Match service - will be replaced with real API calls
import type { Match, CreateMatchRequest, UpdateMatchStatusRequest } from '../types/match'

export const MatchService = {
  async createMatch(data: CreateMatchRequest): Promise<Match> {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const mockMatch: Match = {
      id: `match_${Date.now()}`,
      listing_id: data.listing_id,
      investor_id: 'investor_1',
      check_holder_id: 'holder_1',
      status: 'pending',
      settlement_type: 'off_platform',
      final_discount_rate: data.proposed_discount_rate || null,
      terms: null,
      message: data.message || null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    
    return mockMatch
  },

  async getMyMatches(): Promise<Match[]> {
    // Mock API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    return [
      {
        id: 'match_1',
        listing_id: 'listing_1',
        investor_id: 'investor_1',
        check_holder_id: 'holder_1',
        status: 'pending',
        settlement_type: 'off_platform',
        final_discount_rate: 8.5,
        terms: null,
        message: 'درخواست خرید چک با تخفیف پیشنهادی',
        created_at: '2024-01-15T10:30:00Z',
        updated_at: '2024-01-15T10:30:00Z',
        listing: {
          id: 'listing_1',
          face_amount: 50000000,
          due_date: '2024-06-30',
          status: 'published',
          title: 'چک شرکت الف',
        },
      },
      {
        id: 'match_2',
        listing_id: 'listing_2',
        investor_id: 'investor_1',
        check_holder_id: 'holder_2',
        status: 'accepted',
        settlement_type: 'off_platform',
        final_discount_rate: 12.0,
        terms: 'توافق شده - انتقال چک در حال انجام',
        message: 'پذیرش پیشنهاد با تخفیف 12%',
        created_at: '2024-01-10T08:00:00Z',
        updated_at: '2024-01-12T14:00:00Z',
        listing: {
          id: 'listing_2',
          face_amount: 75000000,
          due_date: '2024-05-15',
          status: 'matched',
          title: 'چک شرکت ب',
        },
      },
    ]
  },

  async updateMatchStatus(id: string, data: UpdateMatchStatusRequest): Promise<Match> {
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const match = {
      id,
      listing_id: 'listing_1',
      investor_id: 'investor_1',
      check_holder_id: 'holder_1',
      status: data.status,
      settlement_type: 'off_platform' as const,
      final_discount_rate: data.final_discount_rate || null,
      terms: data.terms || null,
      message: null,
      created_at: '2024-01-15T10:30:00Z',
      updated_at: new Date().toISOString(),
    }
    
    return match
  },

  async getMatch(id: string): Promise<Match> {
    await new Promise(resolve => setTimeout(resolve, 300))
    
    return {
      id,
      listing_id: 'listing_1',
      investor_id: 'investor_1',
      check_holder_id: 'holder_1',
      status: 'pending',
      settlement_type: 'off_platform',
      final_discount_rate: 8.5,
      terms: null,
      message: 'درخواست خرید چک',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T10:30:00Z',
    }
  },
}