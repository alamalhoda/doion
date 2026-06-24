<template>
  <div 
    class="notification-item" 
    :class="{ unread: notification.status === 'pending' }"
    @click="handleClick"
  >
    <div class="notification-icon">
      <NIcon :component="iconForType" />
    </div>

    <div class="notification-content">
      <div class="notification-header">
        <h4 class="notification-title">
          {{ notification.title }}
        </h4>
        <NButton 
          v-if="notification.status === 'pending'"
          size="tiny" 
          @click.stop="emit('markRead')"
        >
          {{ $t('notifications.mark_read') }}
        </NButton>
      </div>
      <p class="notification-message">
        {{ notification.message }}
      </p>
      <span class="notification-time">{{ formatTime(notification.created_at) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'
import { useI18n } from 'vue-i18n'
import { NIcon, NButton } from 'naive-ui'
import { CheckmarkCircle, AlertCircle, ChatboxEllipses, Cash, DocumentText } from '@vicons/ionicons5'
import type { Notification } from '../types/notification'

const { notification } = defineProps<{ notification: Notification }>()
const emit = defineEmits<{
  markRead: []
  click: []
}>()

const { t } = useI18n()

const iconForType = computed(() => {
  const icons: Record<string, Component> = {
    match_created: ChatboxEllipses,
    listing_approved: CheckmarkCircle,
    listing_rejected: AlertCircle,
    match_accepted: Cash,
    match_rejected: DocumentText,
  }
  return icons[notification.type] || CheckmarkCircle
})

function handleClick(): void {
  emit('click')
}

function formatTime(dateStr: string): string {
  const date = new Date(dateStr)
  const now = new Date()
  const diffHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
  
  if (diffHours < 1) {
    return t('notifications.just_now')
  } else if (diffHours < 24) {
    return `${diffHours} ${t('notifications.hours_ago')}`
  } else {
    return date.toLocaleDateString('fa-IR')
  }
}
</script>

<style scoped>
.notification-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background 0.2s;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background: var(--color-bg-primary);
}

.notification-item.unread {
  background: var(--color-primary-light);
}

.notification-icon {
  padding: var(--spacing-sm);
  background: var(--color-primary-light);
  border-radius: 50%;
  color: var(--color-primary);
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.notification-title {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
}

.notification-message {
  margin: 0 0 var(--spacing-sm);
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.notification-time {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>