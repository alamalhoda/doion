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
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ROUTES } from '@/constants/routes'
import Button from '@/components/ui/Button.vue'

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

const { locale } = useI18n()

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
      { path: ROUTES.ADMIN_DASHBOARD, label: 'داشبورد' },
      { path: ROUTES.ADMIN_MODERATION_QUEUE, label: 'مدیریت' },
    ]
  }
  if (props.variant === 'user') {
    return [
      { path: ROUTES.USER_DASHBOARD, label: 'داشبورد' },
      { path: ROUTES.USER_LISTINGS, label: 'آگهی‌های من' },
      { path: ROUTES.MARKETPLACE, label: 'بازارچه' },
    ]
  }
  return []
})

const showLinks = computed(() => props.variant !== 'default')

function toggleLocale() {
  locale.value = currentLocale.value === 'fa' ? 'en' : 'fa'
  document.documentElement.lang = locale.value
  document.documentElement.dir = locale.value === 'fa' ? 'rtl' : 'ltr'
}
</script>

<style scoped>
.nav {
  background: var(--surface);
  border-bottom: 1px solid var(--color-border);
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
  color: var(--color-primary);
}

.nav__links {
  display: flex;
  gap: var(--spacing-lg);
}

.nav__link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: color var(--transition-base);
}

.nav__link:hover,
.nav__link--active {
  color: var(--color-primary);
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
</style>