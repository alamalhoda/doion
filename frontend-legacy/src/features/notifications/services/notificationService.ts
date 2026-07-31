// Notification API service
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'
import type {
  Notification,
  NotificationPreferences,
  MarkReadRequest,
} from '../types/notification'
import type { ListResponse } from '@/api/types'

export class NotificationService {
  private static basePath = '/api/v1/notifications'

  static async getNotifications(
    params?: Record<string, unknown>,
  ): Promise<ListResponse<Notification>> {
    try {
      const response = await apiClient.get<ListResponse<Notification>>(
        this.basePath + '/',
        { params },
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getNotification(id: string | number): Promise<Notification> {
    try {
      const response = await apiClient.get<Notification>(
        this.basePath + `/${id}/`,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async markRead(
    id: string | number,
    data: MarkReadRequest,
  ): Promise<Notification> {
    try {
      const response = await apiClient.patch<Notification>(
        this.basePath + `/${id}/`,
        data,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async markAllRead(): Promise<{ message: string }> {
    try {
      const response = await apiClient.post<{ message: string }>(
        this.basePath + '/mark-all-read/',
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async getPreferences(): Promise<NotificationPreferences> {
    try {
      const response = await apiClient.get<NotificationPreferences>(
        this.basePath + '/preferences/',
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }

  static async updatePreferences(
    data: Partial<NotificationPreferences>,
  ): Promise<NotificationPreferences> {
    try {
      const response = await apiClient.patch<NotificationPreferences>(
        this.basePath + '/preferences/',
        data,
      )
      return response.data
    } catch (error) {
      throw normalizeApiError(error)
    }
  }
}
