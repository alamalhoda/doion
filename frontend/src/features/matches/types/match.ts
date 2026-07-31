// Match types aligned with MASTER_API_CONTRACT.md §9

export type MatchStatus =
  | 'pending'
  | 'accepted'
  | 'declined'
  | 'cancelled'
  | 'off_platform_confirmed'
  | 'settled'

export type SettlementType = 'off_platform' | 'escrow' | 'principal_ledger'

export interface ListingSummary {
  id: number
  bank_name: string
  face_amount: string
  due_date: string
  status: string
  created_at: string
  updated_at: string
}

export interface UserSummary {
  id: number
  username: string
  name: string
}

export interface Match {
  id: number
  listing: ListingSummary
  investor: UserSummary
  check_holder: UserSummary
  status: MatchStatus
  settlement_type: SettlementType
  final_discount_rate: string | null
  terms: string
  message: string
  created_at: string
  updated_at: string
}

export interface CreateMatchRequest {
  listing_id: number
  message?: string
}

export interface UpdateMatchStatusRequest {
  status: MatchStatus
  final_discount_rate?: string | null
  terms?: string
  note?: string
}
