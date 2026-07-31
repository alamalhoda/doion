<template>
  <nav class="nav">
    <div class="nav__inner">
      <RouterLink
        :to="logoLink"
        class="nav__brand"
      >
        <span class="nav__brand-text">{{ appName }}</span>
      </RouterLink>

      <div
        v-if="showLinks"
        class="nav__links"
      >
        <RouterLink
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav__link"
          active-class="nav__link--active"
        >
          {{ link.label }}
        </RouterLink>
      </div>

      <div class="nav__actions">
        <slot name="actions" />

        <RouterLink
          v-if="showNotifications"
          :to="ROUTES.USER_NOTIFICATIONS"
          class="nav__notification"
        >
          <Icon
            name="notifications"
            :size="20"
          />
          <span
            v-if="unreadCount > 0"
            class="nav__notification-badge"
          >{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
        </RouterLink>

        <Button
          v-if="showLanguageSwitcher"
          variant="ghost"
          @click="toggleLocale"
        >
          {{ currentLocale === 'fa' ? 'EN' : 'FA' }}
        </Button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ROUTES } from '@/constants/routes'
import Button from '@/components/ui/Button.vue'
import Icon from '@/components/ui/Icon.vue'
import { useNotificationStore } from '@/features/notifications/stores/notificationStore'

interface NavLink {
  path: string
  label: string
  requiresAuth?: boolean
}

interface Props {
  variant?: 'default' | 'user' | 'admin'
  showLanguageSwitcher?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  showLanguageSwitcher: true,
})

const { locale, t } = useI18n()
const notificationStore = useNotificationStore()

const appName = 'چک‌بازار'
const currentLocale = computed(() => locale.value)

const logoLink = computed(() => {
  if (props.variant === 'admin') return ROUTES.ADMIN_DASHBOARD
  if (props.variant === 'user') return ROUTES.USER_DASHBOARD
  return '/'
})

const navLinks = computed<NavLink[]>(() => {
  if (props.variant === 'admin') {
    return [
      { path: ROUTES.ADMIN_DASHBOARD, label: $t('layout.nav.dashboard') },
      { path: ROUTES.ADMIN_MODERATION_QUEUE, label: $t('admin.moderation_title') },
      { path: ROUTES.ADMIN_FEATURE_FLAGS, label: $t('admin.feature_flags_title') },
    ]
  }
  if (props.variant === 'user') {
    return [
      { path: ROUTES.USER_DASHBOARD, label: 'داشبورد' },
      { path: '/app/profile', label: 'پروفایل' },
      { path: ROUTES.USER_LISTINGS, label: 'آگهی‌های من' },
      { path: ROUTES.MARKETPLACE, label: 'بازارچه' },
    ]
  }
  return []
})

const showLinks = computed(() => props.variant !== 'default')
const showNotifications = computed(() => props.variant === 'user')

const unreadCount = computed(() => notificationStore.unreadCount)

let pollingTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  notificationStore.fetchUnreadCount()
  pollingTimer = setInterval(() => {
    notificationStore.fetchUnreadCount()
  }, 30000)
})

onUnmounted(() => {
  if (pollingTimer) {
    clearInterval(pollingTimer)
  }
})

function toggleLocale() {
  locale.value = currentLocale.value === 'fa' ? 'en' : 'fa'
  document.documentElement.lang = locale.value
  document.documentElement.dir = locale.value === 'fa' ? 'rtl' : 'ltr'
}
</script>

<style scoped>
.nav {
  background: var(--navy);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md) var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.nav__brand {
  text-decoration: none;
}

.nav__brand-text {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--gold-light);
}

.nav__links {
  display: flex;
  gap: var(--spacing-lg);
}

.nav__link {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: color var(--transition-base);
}

.nav__link:hover,
.nav__link--active {
  color: var(--gold-light);
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.nav__notification {
  position: relative;
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xs);
  border-radius: var(--radius-sm);
  transition: color var(--transition-base);
}

.nav__notification:hover {
  color: var(--gold-light);
}

.nav__notification-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--color-warning);
  color: #fff;
  font-size: 10px;
  font-weight: var(--font-weight-bold);
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
}
</style>