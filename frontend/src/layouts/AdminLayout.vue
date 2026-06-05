<template>
  <div class="admin-layout">
    <header class="admin-header">
      <div class="header-content">
        <h1>{{ $t('layout.header') }}</h1>
        <div class="header-actions">
          <LanguageSwitcher />
          <button @click="logout">{{ $t('auth.logout') }}</button>
        </div>
      </div>
    </header>
    <main class="admin-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { ROUTES } from '@/constants/routes'
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue'

const router = useRouter()
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  router.push(ROUTES.LOGIN)
}
</script>

<style scoped>
.admin-layout {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.admin-header {
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-lg);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
}

.header-actions {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.admin-main {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-xl);
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
