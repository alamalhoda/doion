// Notification Pinia store
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Notification } from '../types/notification'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const unreadCount = ref(0)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const unreadNotifications = computed(() => 
    notifications.value.filter(n => n.status === 'pending')
  )

  async function fetchNotifications(): Promise<void> {
    isLoading.value = true
    error.value = null

    try {
      // Mock API call - replace with real API
      await new Promise(resolve => setTimeout(resolve, 500))
      
      notifications.value = [
        {
          id: 'notif_1',
          user_id: 'user_1',
          type: 'listing_approved',
          channel: 'in_app',
          status: 'pending',
          title: 'آگهی چک تأیید شد',
          message: 'آگهی چک شما پس از بررسی ناظر تأیید و منتشر شد',
          reference_id: 'listing_1',
          created_at: '2024-01-16T10:00:00Z',
        },
        {
          id: 'notif_2',
          user_id: 'user_1',
          type: 'match_created',
          channel: 'in_app',
          status: 'pending',
          title: 'درخواست خرید جدید',
          message: 'سرمایه‌گذار به چک شما علاقه‌مند شده است',
          reference_id: 'match_1',
          created_at: '2024-01-16T09:30:00Z',
        },
        {
          id: 'notif_3',
          user_id: 'user_1',
          type: 'match_accepted',
          channel: 'in_app',
          status: 'sent',
          title: 'درخواست شما پذیرفته شد',
          message: 'سرمایه‌گذار چک شما را پذیرفته است. می‌توانید برای مذاکره با او تماس بگیرید',
          reference_id: 'match_1',
          created_at: '2024-01-15T14:00:00Z',
        },
      ]
      
      unreadCount.value = unreadNotifications.value.length
    } catch (err: any) {
      error.value = err.message || 'error.unknown'
    } finally {
      isLoading.value = false
    }
  }

  async function markAsRead(id: string): Promise<void> {
    const notification = notifications.value.find(n => n.id === id)
    if (notification && notification.status === 'pending') {
      notification.status = 'read'
      unreadCount.value = unreadNotifications.value.length
    }
  }

  async function markAllAsRead(): Promise<void> {
    notifications.value = notifications.value.map(n => ({ ...n, status: 'read' as const }))
    unreadCount.value = 0
  }

  return {
    notifications,
    unreadCount,
    isLoading,
    error,
    unreadNotifications,
    fetchNotifications,
    markAsRead,
    markAllAsRead,
  }
})