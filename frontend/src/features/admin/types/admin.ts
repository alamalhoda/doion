export interface AdminStats {
  listings: {
    total: number
    published: number
    pending_moderation: number
    rejected: number
    expired: number
    matched: number
  }
  users: {
    total: number
    kyc_pending: number
    kyc_approved: number
  }
  verifications: {
    pending: number
  }
  notifications: {
    unread: number
  }
}

export interface FeatureFlag {
  key: string
  description: string
  is_enabled: boolean
  is_system: boolean
}
