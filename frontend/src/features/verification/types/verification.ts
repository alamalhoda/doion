// Verification/KYC types — MASTER_API_CONTRACT.md §4

export const VerificationStatus = {
  PENDING: 'pending',
  APPROVED: 'approved',
  REJECTED: 'rejected',
} as const

export type VerificationStatus = (typeof VerificationStatus)[keyof typeof VerificationStatus]

export interface VerificationDocument {
  id: number
  document_type: string
  file: string
  file_size: number
}

export interface Verification {
  id: number
  full_name: string
  national_id: string
  company_name: string
  status: VerificationStatus
  rejection_reason: string
  rejection_code: string
  documents: VerificationDocument[]
}

export interface CreateVerificationFields {
  full_name: string
  national_id?: string
  company_name?: string
  national_id_front: File
  national_id_back: File
  selfie?: File
}

export interface KycDecisionRequest {
  decision: 'approve' | 'reject'
  rejection_code?: string
  rejection_note?: string
}

export interface KycDecisionResponse {
  status: 'approved' | 'rejected'
}
