// Cheque Listing types for the marketplace

export type UserRole = 'CheckHolder' | 'Investor' | 'InstitutionalInvestor' | 'Moderator' | 'Admin'

export type ListingStatus = 'pending_moderation' | 'published' | 'rejected' | 'matched' | 'settled' | 'expired'

export type MatchStatus = 'pending' | 'accepted' | 'rejected' | 'settled_off_platform'

export type VerificationStatus = 'pending' | 'approved' | 'rejected'

export interface IssuerProfile {
  id: string
  national_or_company_id: string
  name: string
  credit_score?: number
}

export interface ChequeListing {
  id: string
  owner_id: string
  issuer_id: string
  face_amount: number
  due_date: string
  status: ListingStatus
  suggested_discount_rate?: number | null
  risk_tier?: 'low' | 'medium' | 'high' | null
  title?: string
  description?: string
  category?: string
  tags?: string[]
  created_at: string
  updated_at: string
  issuer_profile?: IssuerProfile
}

export interface CreateListingRequest {
  face_amount: number
  due_date: string
  issuer_id?: string
  suggested_discount_rate?: number
  title?: string
  description?: string
  category?: string
  tags?: string[]
}

export interface UpdateListingRequest {
  face_amount?: number
  due_date?: string
  suggested_discount_rate?: number
  title?: string
  description?: string
  category?: string
  tags?: string[]
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