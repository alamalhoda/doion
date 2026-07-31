export type NotificationType =
  | 'match_created'
  | 'match_accepted'
  | 'match_declined'
  | 'match_cancelled'
  | 'settlement_confirmed'
  | 'listing_published'
  | 'listing_rejected'
  | 'listing_expired'
  | 'kyc_approved'
  | 'kyc_rejected'
  | 'new_moderation_item'

export type NotificationChannel = 'in_app' | 'sms' | 'email'

export type NotificationStatus = 'pending' | 'sent' | 'read' | 'failed'

export interface Notification {
  id: string
  type: NotificationType
  channel: NotificationChannel
  status: NotificationStatus
  title: string
  message: string
  related_object_type?: string
  related_object_id?: string
  read_at?: string | null
  sent_at?: string | null
  created_at: string
}

export interface NotificationPreferences {
  in_app_enabled: boolean
  sms_enabled: boolean
  email_enabled: boolean
}

export interface MarkReadRequest {
  is_read: boolean
}
