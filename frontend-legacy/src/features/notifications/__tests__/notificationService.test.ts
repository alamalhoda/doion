import { describe, it, expect, vi, beforeEach } from 'vitest'
import { NotificationService } from '../services/notificationService'
import type { Notification, MarkReadRequest } from '../types/notification'

// Mock apiClient
const mockGet = vi.fn()
const mockPost = vi.fn()
const mockPatch = vi.fn()

vi.mock('@/api/client', () => ({
  apiClient: {
    get: (...args: unknown[]) => mockGet(...args),
    post: (...args: unknown[]) => mockPost(...args),
    patch: (...args: unknown[]) => mockPatch(...args),
  },
}))

vi.mock('@/api/errors', () => ({
  normalizeApiError: (error: unknown) => error,
}))

const basePath = '/api/v1/notifications'

const mockNotification: Notification = {
  id: 'notif-1',
  type: 'match_created',
  channel: 'in_app',
  status: 'pending',
  title: 'درخواست جدید',
  message: 'یک سرمایه‌گذار به آگهی شما علاقه‌مند شده',
  related_object_type: 'listing',
  related_object_id: 'listing-1',
  created_at: '2024-01-15T10:00:00Z',
}

describe('NotificationService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getNotifications', () => {
    it('should fetch notifications list with default params', async () => {
      const mockResponse = {
        data: {
          count: 1,
          next: null,
          previous: null,
          results: [mockNotification],
          unread_count: 1,
        },
      }
      mockGet.mockResolvedValue(mockResponse)

      const result = await NotificationService.getNotifications()

      expect(mockGet).toHaveBeenCalledWith(basePath + '/', { params: undefined })
      expect(result.count).toBe(1)
      expect(result.results[0].id).toBe('notif-1')
    })

    it('should pass query params to request', async () => {
      const mockResponse = {
        data: {
          count: 0,
          next: null,
          previous: null,
          results: [],
          unread_count: 0,
        },
      }
      mockGet.mockResolvedValue(mockResponse)

      await NotificationService.getNotifications({ is_read: false, page: 1 })

      expect(mockGet).toHaveBeenCalledWith(basePath + '/', {
        params: { is_read: false, page: 1 },
      })
    })
  })

  describe('getNotification', () => {
    it('should fetch a single notification by id', async () => {
      const mockResponse = { data: mockNotification }
      mockGet.mockResolvedValue(mockResponse)

      const result = await NotificationService.getNotification('notif-1')

      expect(mockGet).toHaveBeenCalledWith(basePath + '/notif-1/')
      expect(result.id).toBe('notif-1')
    })
  })

  describe('markRead', () => {
    it('should mark notification as read', async () => {
      const updatedNotification = { ...mockNotification, status: 'read' as const }
      const mockResponse = { data: updatedNotification }
      mockPatch.mockResolvedValue(mockResponse)

      const result = await NotificationService.markRead('notif-1', { is_read: true })

      expect(mockPatch).toHaveBeenCalledWith(basePath + '/notif-1/', { is_read: true })
      expect(result.status).toBe('read')
    })

    it('should handle unread request', async () => {
      const mockResponse = { data: { ...mockNotification, status: 'pending' } }
      mockPatch.mockResolvedValue(mockResponse)

      await NotificationService.markRead('notif-1', { is_read: false })

      expect(mockPatch).toHaveBeenCalledWith(basePath + '/notif-1/', { is_read: false })
    })
  })

  describe('markAllRead', () => {
    it('should mark all notifications as read', async () => {
      const mockResponse = { data: { message: '3 notifications marked as read' } }
      mockPost.mockResolvedValue(mockResponse)

      const result = await NotificationService.markAllRead()

      expect(mockPost).toHaveBeenCalledWith(basePath + '/mark-all-read/')
      expect(result.message).toBe('3 notifications marked as read')
    })
  })

  describe('getPreferences', () => {
    it('should fetch notification preferences', async () => {
      const mockResponse = { data: { in_app_enabled: true, sms_enabled: false, email_enabled: true } }
      mockGet.mockResolvedValue(mockResponse)

      const result = await NotificationService.getPreferences()

      expect(mockGet).toHaveBeenCalledWith(basePath + '/preferences/')
      expect(result.in_app_enabled).toBe(true)
      expect(result.email_enabled).toBe(true)
    })
  })

  describe('updatePreferences', () => {
    it('should update notification preferences', async () => {
      const updatedPreferences = {
        in_app_enabled: false,
        sms_enabled: true,
        email_enabled: true,
      }
      const mockResponse = { data: updatedPreferences }
      mockPatch.mockResolvedValue(mockResponse)

      const result = await NotificationService.updatePreferences({
        sms_enabled: true,
      })

      expect(mockPatch).toHaveBeenCalledWith(basePath + '/preferences/', { sms_enabled: true })
      expect(result.sms_enabled).toBe(true)
    })
  })
})
