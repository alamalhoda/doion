<template>
  <div
    class="notification-item"
    :class="{ unread: notification.status !== 'read' }"
    @click="handleClick"
  >
    <div class="notification-icon">
      <Icon
        :name="iconName"
        :size="20"
      />
    </div>

    <div class="notification-content">
      <div class="notification-header">
        <h4 class="notification-title">
          {{ notification.title }}
        </h4>
        <span class="notification-type">
          {{ typeLabel }}
        </span>
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
import { useI18n } from 'vue-i18n'
import Icon from '@/components/ui/Icon.vue'
import type { Notification } from '../types/notification'

const { t } = useI18n()

const props = defineProps<{
  notification: Notification
}>()

const emit = defineEmits<{
  click: []
}>()

const typeLabelMap: Record<string, string> = {
  match_created: 'درخواست خرید',
  match_accepted: 'پذیرش درخواست',
  match_declined: 'رد درخواست',
  match_cancelled: 'لغو تطابق',
  settlement_confirmed: 'تأیید تسویه',
  listing_published: 'آگهی منتشر شد',
  listing_rejected: 'آگهی رد شد',
  listing_expired: 'آگهی منقضی شد',
  kyc_approved: 'تأیید هویت',
  kyc_rejected: 'رد هویت',
  new_moderation_item: 'مورد جدید برای بررسی',
}

const iconMap: Record<string, string> = {
  match_created: 'alert',
  match_accepted: 'check',
  match_declined: 'close',
  match_cancelled: 'alert',
  settlement_confirmed: 'check',
  listing_published: 'check',
  listing_rejected: 'alert',
  listing_expired: 'menu',
  kyc_approved: 'check',
  kyc_rejected: 'alert',
  new_moderation_item: 'search',
}

const iconName = computed(() => iconMap[props.notification.type] || 'notifications')
const typeLabel = computed(() => typeLabelMap[props.notification.type] || props.notification.type)

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
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.2s;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background: var(--surface2);
}

.notification-item.unread {
  background: var(--color-primary-light);
}

.notification-item.unread:hover {
  background: var(--color-primary-light);
  opacity: 0.9;
}

.notification-icon {
  padding: var(--spacing-sm);
  background: var(--color-primary-light);
  border-radius: 50%;
  color: var(--color-primary);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-item.unread .notification-icon {
  background: var(--color-primary);
  color: #fff;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
  gap: var(--spacing-sm);
}

.notification-title {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
  line-height: 1.4;
}

.notification-type {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
  flex-shrink: 0;
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
