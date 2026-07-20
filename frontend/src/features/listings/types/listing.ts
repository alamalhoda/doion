// Cheque Listing types for the marketplace

export type UserRole = 'check_holder' | 'investor' | 'institutional_investor' | 'moderator' | 'admin'

export type ListingStatus = 'pending_moderation' | 'published' | 'rejected' | 'matched' | 'expired' | 'withdrawn' | 'settled_off_platform'

export type RejectionCode = 'MOD_101' | 'MOD_102' | 'MOD_103' | 'MOD_104' | 'MOD_105' | 'MOD_106'

export const REJECTION_CODE_LABELS: Record<RejectionCode, string> = {
  MOD_101: 'Incomplete information',
  MOD_102: 'Poor quality image',
  MOD_103: 'Invalid cheque',
  MOD_104: 'Duplicate listing',
  MOD_105: 'Risk too high',
  MOD_106: 'Other',
}

export type MatchStatus = 'pending' | 'accepted' | 'declined' | 'cancelled' | 'off_platform_confirmed' | 'settled'

export type VerificationStatus = 'pending' | 'approved' | 'rejected'

export interface IssuerProfile {
  id: string
  national_or_company_id: string
  name: string
  credit_score?: number
}

export interface ChequeListing {
  id: string
  owner_id: number
  issuer_id: number
  issuer_profile?: IssuerProfile
  bank_name: string
  cheque_serial_number: string
  face_amount: number
  due_date: string
  issuer_type: 'legal' | 'natural'
  issuer_name: string
  issuer_national_id: string
  description: string
  suggested_discount_rate?: number | null
  risk_tier?: 'low' | 'medium' | 'high' | null
  status: ListingStatus
  rejection_reason?: string
  rejection_code?: RejectionCode | null
  resubmit_count?: number
  days_to_due?: number
  interest_count?: number
  published_at?: string
  created_at: string
  updated_at: string
}

export interface CreateListingRequest {
  issuer: number
  bank_name: string
  cheque_serial_number: string
  face_amount: number
  due_date: string
  issuer_type: 'legal' | 'natural'
  issuer_name: string
  issuer_national_id: string
  description?: string
}

export interface UpdateListingRequest {
  bank_name?: string
  cheque_serial_number?: string
  face_amount?: number
  due_date?: string
  issuer_type?: 'legal' | 'natural'
  issuer_name?: string
  issuer_national_id?: string
  description?: string
}

export interface DocumentUpload {
  document_type: string
  file: File
}

export interface ListingFilters {
  min_amount?: number
  max_amount?: number
  min_due_date?: string
  max_due_date?: string
  risk_tier?: 'low' | 'medium' | 'high'
  status?: ListingStatus
  search?: string
}

export interface ModerateDecisionRequest {
  decision: 'approve' | 'reject'
  rejection_code?: RejectionCode
  rejection_note?: string
}

export interface ModerationDecisionResponse {
  id: string
  listing: number
  moderator: number | null
  decision: 'approve' | 'reject'
  rejection_code: RejectionCode | null
  rejection_code_display: string | null
  rejection_note: string
  created_at: string
}