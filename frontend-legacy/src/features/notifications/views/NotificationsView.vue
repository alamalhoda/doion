<template>
  <div class="notifications-view">
    <div class="view-header">
      <h1>{{ $t('notifications.title') }}</h1>
      <div class="header-actions">
        <NEmpty
          v-if="filteredNotifications.length === 0 && !isLoading"
          :description="$t('notifications.no_notifications')"
          class="empty-state"
        >
          <template #icon>
            <div class="empty-icon">
              <Icon
                name="notifications-off"
                :size="48"
              />
            </div>
          </template>
        </NEmpty>
      </div>
    </div>

    <NotificationSidebar
      v-model:active-tab="activeTab"
      :unread-count="notificationStore.unreadCount"
      @mark-all-read="markAllAsRead"
    />

    <div class="list-actions">
      <span class="unread-summary">
        {{ unreadLabel }}
      </span>
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
      <AppButton
        variant="secondary"
        size="small"
        @click="retryFetch"
      >
        تلاش مجدد
      </AppButton>
    </div>

    <div
      v-else-if="filteredNotifications.length === 0"
      class="empty-list"
    >
      <div class="empty-content">
        <Icon
          name="notifications-off"
          :size="64"
        />
        <p>{{ emptyTitle }}</p>
        <p class="empty-description">
          {{ emptyDescription }}
        </p>
      </div>
    </div>

    <div
      v-else
      class="notifications-list"
    >
      <NotificationItem
        v-for="notification in filteredNotifications"
        :key="notification.id"
        :notification="notification"
        @click="handleNotificationClick(notification)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NEmpty } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import AppButton from '@/components/ui/AppButton.vue'
import Icon from '@/components/ui/Icon.vue'
import { useNotificationStore } from '../stores/notificationStore'
import NotificationItem from '../components/NotificationItem.vue'
import NotificationSidebar from '../components/NotificationSidebar.vue'
import type { Notification, NotificationType } from '../types/notification'

const router = useRouter()
const { t } = useI18n()
const notificationStore = useNotificationStore()

const activeTab = ref<'all' | NotificationType | 'preferences'>('all')

const isLoading = computed(() => notificationStore.isLoading)
const error = computed(() => notificationStore.error)
const filteredNotifications = computed(() => notificationStore.filteredNotifications)

const unreadLabel = computed(() => {
  const count = notificationStore.unreadCount
  if (count === 0) {
    return 'همه اعلان‌ها خوانده شده‌اند'
  }
  return `${count} اعلان خوانده نشده`
})

const emptyTitle = computed(() => {
  switch (activeTab.value) {
    case 'match':
      return 'تطابقی وجود ندارد'
    case 'listing':
      return 'آگهی جدیدی وجود ندارد'
    case 'kyc':
      return 'اعلان KYC وجود ندارد'
    case 'moderation':
      return 'مورد بررسی جدیدی وجود ندارد'
    case 'preferences':
      return 'تنظیمات اعلان‌ها'
    default:
      return 'همه چیز مرتب است'
  }
})

const emptyDescription = computed(() => {
  switch (activeTab.value) {
    case 'match':
      return 'هیچ درخواست تطابق یا به‌روزرسانی تطابقی ندارید'
    case 'listing':
      return 'اعلان جدیدی در مورد آگهی‌های شما وجود ندارد'
    case 'kyc':
      return 'هیچ به‌روزرسانی در مورد احراز هویت شما وجود ندارد'
    case 'moderation':
      return 'تمام موارد بررسی شده‌اند'
    case 'preferences':
      return 'از طریق تنظیمات اعلان‌ها، کانال‌های مورد علاقه خود را مدیریت کنید'
    default:
      return 'اعلان جدیدی ندارید'
  }
})

const storeFilterMap: Record<string, NotificationType> = {
  match: 'match_created',
  listing: 'listing_published',
  kyc: 'kyc_approved',
  moderation: 'new_moderation_item',
}

const storeStatusFilterMap: Record<string, 'all'> = {
  all: 'all',
}

function handleSidebarTabChange(value: string): void {
  activeTab.value = value as 'all' | NotificationType | 'preferences'
  if (value === 'preferences') {
    notificationStore.setFilter('all')
    notificationStore.setStatusFilter('all')
    // Could navigate to preferences view or show inline preferences
    return
  }

  const typeFilter = storeFilterMap[value]
  if (typeFilter) {
    notificationStore.setFilter(typeFilter)
  } else if (value === 'all') {
    notificationStore.setFilter('all')
  }

  notificationStore.setStatusFilter('all')
  notificationStore.fetchNotifications()
}

function markAllAsRead(): void {
  notificationStore.markAllAsRead()
  notificationStore.fetchNotifications()
}

function handleNotificationClick(notification: Notification): void {
  const relatedType = notification.related_object_type
  const relatedId = notification.related_object_id

  if (relatedType === 'listing' && relatedId) {
    router.push(`/app/listings/${relatedId}`)
  } else if (relatedType === 'match' && relatedId) {
    router.push(`/app/matches/${relatedId}`)
  }
}

async function retryFetch(): Promise<void> {
  notificationStore.fetchNotifications()
}

// Watch for tab changes via the sidebar model
import { watch } from 'vue'

watch(
  () => notificationStore.currentFilter,
  () => {
    notificationStore.fetchNotifications()
  },
)

watch(activeTab, (newTab) => {
  handleSidebarTabChange(newTab)
})

function markAsRead(id: string): void {
  notificationStore.markAsRead(id)
}

// Fetch on mount
notificationStore.fetchNotifications()
</script>

<style scoped>
.notifications-view {
  max-width: 900px;
  margin: 0 auto;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.view-header h1 {
  margin: 0;
  font-size: var(--font-size-xl);
  color: var(--text1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.list-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.unread-summary {
  font-size: var(--font-size-sm);
  color: var(--text2);
}

.loading-state,
.error-state {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.empty-icon {
  color: var(--text3);
}

.empty-list {
  text-align: center;
  padding: var(--spacing-2xl);
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  color: var(--text3);
}

.empty-content p {
  margin: 0;
  font-size: var(--font-size-md);
  color: var(--text2);
}

.empty-description {
  font-size: var(--font-size-sm);
  color: var(--text3);
}

.notifications-list {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  overflow: hidden;
}

.loading-state {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}
</style>
