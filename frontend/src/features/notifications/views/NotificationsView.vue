<template>
  <div class="notifications-view">
    <div class="view-header">
      <h1>{{ $t('notifications.title') }}</h1>
    </div>

    <div
      v-if="isLoading"
      class="loading-state"
    >
      {{ $t('common.loading') }}
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
    </div>

    <div
      v-else
      class="notifications-container"
    >
      <div class="notifications-list">
        <NotificationItem
          v-for="notification in notifications"
          :key="notification.id"
          :notification="notification"
          @mark-read="markAsRead(notification.id)"
          @click="handleNotificationClick(notification)"
        />
      </div>

      <NEmpty
        v-if="notifications.length === 0"
        :description="$t('notifications.no_notifications')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { NEmpty } from 'naive-ui'
import { useNotificationStore } from '../stores/notificationStore'
import NotificationItem from '../components/NotificationItem.vue'

const router = useRouter()
const notificationStore = useNotificationStore()

const isLoading = computed(() => notificationStore.isLoading)
const error = computed(() => notificationStore.error)
const notifications = computed(() => notificationStore.notifications)

function markAsRead(id: string): void {
  notificationStore.markAsRead(id)
}

import type { Notification } from '../types/notification'

function handleNotificationClick(notification: Notification): void {
  // Navigate based on notification type
  if (notification.type === 'match_created') {
    router.push(`/app/matches/${notification.reference_id}`)
  } else if (notification.type === 'listing_approved') {
    router.push(`/app/listings/${notification.reference_id}`)
  }
}
</script>

<style scoped>
.notifications-view {
  max-width: 800px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--spacing-xl);
}

.view-header h1 {
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
}

.loading-state,
.error-state {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--color-text-secondary);
}

.notifications-container {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
}
</style>