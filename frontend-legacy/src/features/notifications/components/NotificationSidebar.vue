<template>
  <div class="notification-sidebar">
    <div class="sidebar-header">
      <h3>اعلان‌ها</h3>
      <AppButton
        v-if="unreadCount > 0"
        variant="secondary"
        size="small"
        block
        @click="$emit('mark-all-read')"
      >
        علامت‌گذاری همه به‌عنوان خوانده‌شده
      </AppButton>
    </div>

    <div class="filter-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        :class="[
          'filter-tab',
          { active: activeTab === tab.value },
          { unread: tab.showBadge && unreadCountByTab(tab.value) > 0 },
        ]"
        @click="activeTab = tab.value"
      >
        <span class="tab-label">{{ tab.label }}</span>
        <NBadge
          v-if="tab.showBadge && unreadCountByTab(tab.value) > 0"
          :value="unreadCountByTab(tab.value)"
          type="success"
          :max="99"
        />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NBadge } from 'naive-ui'
import { useNotificationStore } from '../stores/notificationStore'
import AppButton from '@/components/ui/AppButton.vue'

defineEmits<{
  'update:activeTab': [value: string]
  'mark-all-read': []
}>()

const notificationStore = useNotificationStore()
const activeTab = defineModel<string>('activeTab', { default: 'all' })

const tabs = [
  { value: 'all', label: 'همه', showBadge: true },
  { value: 'match', label: 'تطابق', showBadge: true },
  { value: 'listing', label: 'آگهی', showBadge: true },
  { value: 'kyc', label: 'KYC', showBadge: true },
  { value: 'moderation', label: 'Moderation', showBadge: true },
  { value: 'preferences', label: 'تنظیمات', showBadge: false },
]

const unreadCount = computed(() => notificationStore.unreadCount)

function unreadCountByTab(tabValue: string): number {
  switch (tabValue) {
    case 'match':
      return notificationStore.matchNotifications.filter(n => n.status !== 'read').length
    case 'listing':
      return notificationStore.listingNotifications.filter(n => n.status !== 'read').length
    case 'kyc':
      return notificationStore.kycNotifications.filter(n => n.status !== 'read').length
    case 'moderation':
      return notificationStore.moderationNotifications.filter(n => n.status !== 'read').length
    case 'all':
    default:
      return unreadCount.value
  }
}
</script>

<style scoped>
.notification-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  border-bottom: 1px solid var(--border);
  padding-bottom: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.sidebar-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: var(--text1);
}

.filter-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.filter-tab {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text2);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition: all var(--transition-base);
  white-space: nowrap;
}

.filter-tab:hover {
  background: var(--surface2);
}

.filter-tab.active {
  background: var(--teal-light);
  color: var(--teal);
  border-color: var(--teal);
}

.filter-tab.unread::after {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-warning);
  display: inline-block;
  margin-right: var(--spacing-xs);
}

.tab-label {
  font-weight: 500;
}
</style>
