// Match and Notification types for the marketplace

export type MatchStatus = 'pending' | 'accepted' | 'declined' | 'cancelled' | 'off_platform_confirmed' | 'settled'

export interface ListingSummary {
  id: string
  face_amount: number
  due_date: string
  status: string
  title?: string
  suggested_discount_rate?: number | null
}

export interface UserSummary {
  id: string
  username: string
  full_name?: string
}

export interface Match {
  id: string
  listing_id: string
  investor_id: string
  check_holder_id: string
  status: MatchStatus
  settlement_type: 'off_platform' | 'escrow' | 'principal_ledger'
  final_discount_rate?: number | null
  terms?: string | null
  message?: string | null
  created_at: string
  updated_at: string
  listing?: ListingSummary
  investor?: UserSummary
  check_holder?: UserSummary
}

export interface CreateMatchRequest {
  listing_id: string
  message?: string
  proposed_discount_rate?: number
}

export interface UpdateMatchStatusRequest {
  status: MatchStatus
  final_discount_rate?: number
  terms?: string
}

export interface Notification {
  id: string
  user_id: string
  type: 'match_created' | 'listing_approved' | 'listing_rejected' | 'match_accepted' | 'match_rejected'
  channel: 'in_app' | 'sms' | 'email'
  status: 'pending' | 'sent' | 'read'
  title: string
  message: string
  reference_id?: string
  created_at: string
}
