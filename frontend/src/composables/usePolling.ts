import { onUnmounted } from 'vue'
import { useNotificationStore } from '@/features/notifications/stores/notificationStore'

export function usePolling(fn: () => void, intervalMs: number) {
  let timerId: ReturnType<typeof setInterval> | null = null

  function start(): void {
    if (timerId) return
    timerId = setInterval(fn, intervalMs)
  }

  function stop(): void {
    if (timerId) {
      clearInterval(timerId)
      timerId = null
    }
  }

  onUnmounted(() => {
    stop()
  })

  return { start, stop }
}

export function useUnreadCount() {
  const notificationStore = useNotificationStore()

  const { start: startPolling, stop: stopPolling } = usePolling(
    () => {
      notificationStore.fetchUnreadCount()
    },
    30000,
  )

  return {
    unreadCount: notificationStore.unreadCount,
    startPolling,
    stopPolling,
    refresh: () => notificationStore.fetchUnreadCount(),
  }
}
