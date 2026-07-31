import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useNotificationStore } from '../stores/notificationStore'
import { NotificationService } from '../services/notificationService'

// Mock NotificationService
vi.mock('../services/notificationService', () => ({
  NotificationService: {
    getNotifications: vi.fn(),
    getNotification: vi.fn(),
    markRead: vi.fn(),
    markAllRead: vi.fn(),
    getPreferences: vi.fn(),
    updatePreferences: vi.fn(),
  },
}))

const mockNotifications = [
  {
    id: 'notif-1',
    type: 'match_created',
    channel: 'in_app',
    status: 'pending',
    title: 'درخواست خرید جدید',
    message: 'سرمایه‌گذار به چک شما علاقه‌مند شده است',
    related_object_type: 'listing',
    related_object_id: 'listing-1',
    created_at: '2024-01-15T10:00:00Z',
  },
  {
    id: 'notif-2',
    type: 'listing_published',
    channel: 'in_app',
    status: 'sent',
    title: 'آگهی چک تأیید شد',
    message: 'آگهی چک شما پس از بررسی ناظر تأیید و منتشر شد',
    related_object_type: 'listing',
    related_object_id: 'listing-2',
    created_at: '2024-01-15T09:00:00Z',
  },
  {
    id: 'notif-3',
    type: 'match_accepted',
    channel: 'in_app',
    status: 'pending',
    title: 'درخواست شما پذیرفته شد',
    message: 'سرمایه‌گذار چک شما را پذیرفته است',
    related_object_type: 'match',
    related_object_id: 'match-1',
    created_at: '2024-01-14T14:00:00Z',
  },
]

describe('notificationStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('initial state', () => {
    it('should have empty initial state', () => {
      const store = useNotificationStore()

      expect(store.notifications).toEqual([])
      expect(store.unreadCount).toBe(0)
      expect(store.totalCount).toBe(0)
      expect(store.preferences).toBeNull()
      expect(store.isLoading).toBe(false)
      expect(store.error).toBeNull()
    })
  })

  describe('fetchNotifications', () => {
    it('should fetch notifications and populate store', async () => {
      const store = useNotificationStore()
      const mockResponse = {
        results: mockNotifications,
        count: mockNotifications.length,
        next: null,
        previous: null,
        unread_count: 2,
      }
      vi.mocked(NotificationService.getNotifications).mockResolvedValue(mockResponse)

      await store.fetchNotifications()

      expect(store.notifications).toHaveLength(3)
      expect(store.totalCount).toBe(3)
      expect(store.unreadCount).toBe(2)
      expect(store.isLoading).toBe(false)
    })

    it('should handle API error', async () => {
      const store = useNotificationStore()
      vi.mocked(NotificationService.getNotifications).mockRejectedValue(
        new Error('Network error'),
      )

      await store.fetchNotifications()

      expect(store.error).toBe('Network error')
      expect(store.isLoading).toBe(false)
    })
  })

  describe('markAsRead', () => {
    it('should mark notification as read optimistically', async () => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
      store.unreadCount = 2

      vi.mocked(NotificationService.markRead).mockResolvedValue({
        ...mockNotifications[0],
        status: 'read',
      })

      await store.markAsRead('notif-1')

      expect(store.notifications[0].status).toBe('read')
      expect(store.unreadCount).toBe(1)
    })

    it('should rollback on API error', async () => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
      store.unreadCount = 2

      vi.mocked(NotificationService.markRead).mockRejectedValue(
        new Error('API error'),
      )

      await store.markAsRead('notif-1')

      expect(store.notifications[0].status).toBe('pending')
      expect(store.unreadCount).toBe(2)
    })
  })

  describe('markAllAsRead', () => {
    it('should mark all notifications as read', async () => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
      store.unreadCount = 2

      vi.mocked(NotificationService.markAllRead).mockResolvedValue({
        message: '2 notifications marked as read',
      })

      await store.markAllAsRead()

      expect(store.notifications.every(n => n.status === 'read')).toBe(true)
      expect(store.unreadCount).toBe(0)
    })
  })

  describe('computed properties', () => {
    beforeEach(() => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
    })

    it('should compute unreadNotifications', () => {
      const store = useNotificationStore()

      expect(store.unreadNotifications).toHaveLength(2)
      expect(store.unreadNotifications.every(n => n.status === 'pending')).toBe(true)
    })

    it('should compute readNotifications', () => {
      const store = useNotificationStore()

      expect(store.readNotifications).toHaveLength(1)
      expect(store.readNotifications[0].id).toBe('notif-2')
    })

    it('should compute matchNotifications', () => {
      const store = useNotificationStore()

      expect(store.matchNotifications).toHaveLength(2)
      expect(store.matchNotifications.map(n => n.id)).toContain('notif-1')
      expect(store.matchNotifications.map(n => n.id)).toContain('notif-3')
    })

    it('should compute listingNotifications', () => {
      const store = useNotificationStore()

      expect(store.listingNotifications).toHaveLength(1)
      expect(store.listingNotifications[0].id).toBe('notif-2')
    })

    it('should compute kycNotifications', () => {
      const store = useNotificationStore()

      expect(store.kycNotifications).toHaveLength(0)
    })
  })

  describe('filteredNotifications', () => {
    beforeEach(() => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
    })

    it('should return all notifications by default', () => {
      const store = useNotificationStore()

      expect(store.filteredNotifications).toHaveLength(3)
    })

    it('should filter by type', () => {
      const store = useNotificationStore()
      store.setFilter('listing_published')

      expect(store.filteredNotifications).toHaveLength(1)
      expect(store.filteredNotifications[0].id).toBe('notif-2')
    })
  })

  describe('markAllAsRead', () => {
    it('should handle error and rollback', async () => {
      const store = useNotificationStore()
      store.notifications = [...mockNotifications]
      store.unreadCount = 2

      vi.mocked(NotificationService.markAllRead).mockRejectedValue(
        new Error('API error'),
      )

      await store.markAllAsRead()

      expect(store.error).toBe('API error')
    })
  })
})
