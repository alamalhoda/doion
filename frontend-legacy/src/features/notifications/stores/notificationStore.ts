import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { NotificationService } from '../services/notificationService'
import type {
  Notification,
  NotificationPreferences,
  NotificationType,
  NotificationStatus,
} from '../types/notification'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const unreadCount = ref(0)
  const totalCount = ref(0)
  const preferences = ref<NotificationPreferences | null>(null)
  const currentFilter = ref<'all' | NotificationType | null>(null)
  const currentStatusFilter = ref<'all' | NotificationStatus | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const unreadNotifications = computed(() =>
    notifications.value.filter(n => n.status !== 'read'),
  )

  const readNotifications = computed(() =>
    notifications.value.filter(n => n.status === 'read'),
  )

  const matchNotifications = computed(() =>
    notifications.value.filter(n =>
      [
        'match_created',
        'match_accepted',
        'match_declined',
        'match_cancelled',
        'settlement_confirmed',
      ].includes(n.type),
    ),
  )

  const listingNotifications = computed(() =>
    notifications.value.filter(n =>
      [
        'listing_published',
        'listing_rejected',
        'listing_expired',
      ].includes(n.type),
    ),
  )

  const kycNotifications = computed(() =>
    notifications.value.filter(n =>
      ['kyc_approved', 'kyc_rejected'].includes(n.type),
    ),
  )

  const moderationNotifications = computed(() =>
    notifications.value.filter(n => n.type === 'new_moderation_item'),
  )

  async function fetchNotifications(params?: Record<string, unknown>): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      const response = await NotificationService.getNotifications(params)
      notifications.value = response.results
      totalCount.value = response.count
      unreadCount.value = response.unread_count ?? unreadNotifications.value.length
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUnreadCount(): Promise<number> {
    try {
      const response = await NotificationService.getNotifications()
      const count = response.unread_count ?? response.results.filter(n => n.status !== 'read').length
      unreadCount.value = count
      return count
    } catch {
      return unreadCount.value
    }
  }

  async function fetchNotification(id: string | number): Promise<Notification | null> {
    isLoading.value = true
    error.value = null

    try {
      const notification = await NotificationService.getNotification(id)
      return notification
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function markAsRead(id: string | number): Promise<void> {
    const notification = notifications.value.find(n => n.id === String(id))
    if (notification && notification.status !== 'read') {
      // Optimistic update
      notification.status = 'read'
      notification.read_at = new Date().toISOString()
      unreadCount.value = Math.max(0, unreadCount.value - 1)

      try {
        await NotificationService.markRead(id, { is_read: true })
      } catch (err: unknown) {
        // Rollback on error
        notification.status = 'pending'
        notification.read_at = null
        unreadCount.value += 1
        error.value = (err as { message?: string }).message || 'error.unknown'
      }
    }
  }

  async function markAllAsRead(): Promise<void> {
    // Optimistic update
    const previouslyUnread = notifications.value.filter(n => n.status !== 'read')
    notifications.value = notifications.value.map(n => ({
      ...n,
      status: 'read' as NotificationStatus,
      read_at: new Date().toISOString(),
    }))
    unreadCount.value = 0

    try {
      await NotificationService.markAllRead()
    } catch (err: unknown) {
      // Rollback on error
      notifications.value = notifications.value.map((n, index) => {
        const wasUnread = previouslyUnread.find(p => p.id === n.id)
        return wasUnread
          ? { ...n, status: 'pending' as NotificationStatus, read_at: null }
          : n
      })
      unreadCount.value = previouslyUnread.length
      error.value = (err as { message?: string }).message || 'error.unknown'
    }
  }

  async function fetchPreferences(): Promise<NotificationPreferences | null> {
    isLoading.value = true
    error.value = null

    try {
      preferences.value = await NotificationService.getPreferences()
      return preferences.value
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function updatePreferences(
    data: Partial<NotificationPreferences>,
  ): Promise<NotificationPreferences | null> {
    isLoading.value = true
    error.value = null

    try {
      preferences.value = await NotificationService.updatePreferences(data)
      return preferences.value
    } catch (err: unknown) {
      error.value = (err as { message?: string }).message || 'error.unknown'
      return null
    } finally {
      isLoading.value = false
    }
  }

  function setFilter(filter: 'all' | NotificationType | null): void {
    currentFilter.value = filter
  }

  function setStatusFilter(filter: 'all' | NotificationStatus | null): void {
    currentStatusFilter.value = filter
  }

  const filteredNotifications = computed(() => {
    let result = notifications.value

    if (currentFilter.value && currentFilter.value !== 'all') {
      result = result.filter(n => n.type === currentFilter.value)
    }

    if (currentStatusFilter.value && currentStatusFilter.value !== 'all') {
      if (currentStatusFilter.value === 'read') {
        result = result.filter(n => n.status === 'read')
      } else {
        result = result.filter(n => n.status === currentStatusFilter.value)
      }
    }

    return result
  })

  return {
    notifications,
    unreadCount,
    totalCount,
    preferences,
    currentFilter,
    currentStatusFilter,
    isLoading,
    error,
    unreadNotifications,
    readNotifications,
    matchNotifications,
    listingNotifications,
    kycNotifications,
    moderationNotifications,
    filteredNotifications,
    fetchNotifications,
    fetchUnreadCount,
    fetchNotification,
    markAsRead,
    markAllAsRead,
    fetchPreferences,
    updatePreferences,
    setFilter,
    setStatusFilter,
  }
})
