<template>
  <div class="user-layout">
    <header class="user-header">
      <div class="header-content">
        <h1>{{ $t('layout.header') }}</h1>
        <div class="header-actions">
          <LanguageSwitcher />
          <button @click="logout">{{ $t('auth.logout') }}</button>
        </div>
      </div>
    </header>
    <main class="user-main">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
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
.user-layout {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.user-header {
  background: var(--color-bg-secondary);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-lg);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
}

.header-actions {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.user-main {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg);
}

@media (max-width: 768px) {
  .user-header {
    padding: var(--spacing-md);
  }

  .user-main {
    padding: var(--spacing-md);
  }
}
</style>
