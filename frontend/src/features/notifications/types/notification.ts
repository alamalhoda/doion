// Notification types
export type NotificationType = 'match_created' | 'listing_approved' | 'listing_rejected' | 'match_accepted' | 'match_rejected'
export type NotificationChannel = 'in_app' | 'sms' | 'email'
export type NotificationStatus = 'pending' | 'sent' | 'read'

export interface Notification {
  id: string
  user_id: string
  type: NotificationType
  channel: NotificationChannel
  status: NotificationStatus
  title: string
  message: string
  reference_id?: string
  created_at: string
}