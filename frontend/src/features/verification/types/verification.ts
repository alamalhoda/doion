// Verification/KYC types

export type VerificationType = 'individual' | 'corporate'

export type VerificationStatus = 'pending' | 'approved' | 'rejected'

export type KycLevel = 'basic' | 'advanced' | 'full'

export interface Verification {
  id: string
  user_id: string
  verification_type: VerificationType
  status: VerificationStatus
  kyc_level?: KycLevel
  reviewed_at?: string | null
  rejection_reason?: string | null
  created_at: string
}

export interface CreateVerificationRequest {
  verification_type: VerificationType
  full_name: string
  national_id?: string
  company_name?: string
  company_registration_id?: string
  phone_number: string
}

export interface IndividualVerification extends CreateVerificationRequest {
  verification_type: 'individual'
  national_id: string
  birth_date?: string
}

export interface CorporateVerification extends CreateVerificationRequest {
  verification_type: 'corporate'
  company_registration_id: string
  company_representative_name?: string
}

export interface VerificationDocument {
  id: string
  user_id: string
  related_object_type: 'verification' | 'listing'
  related_object_id: string
  document_type: string
  file_url: string
  uploaded_at: string
}