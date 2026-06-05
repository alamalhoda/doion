<template>
  <div class="user-dashboard">
    <h1>{{ $t('dashboard.user_title') }}</h1>
    <p class="welcome-text">{{ $t('dashboard.welcome') }}, {{ authStore.user?.username }}!</p>

    <div class="user-content">
      <div class="info-card">
        <h3>حساب کاربری</h3>
        <p>ایمیل: {{ authStore.user?.email }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/features/auth/stores/authStore'

const authStore = useAuthStore()
</script>

<style scoped>
.user-dashboard h1 {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
}

.welcome-text {
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.user-content {
  max-width: 600px;
}

.info-card {
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}

.info-card h3 {
  margin-bottom: var(--spacing-md);
  color: var(--color-primary);
}

.info-card p {
  color: var(--color-text-secondary);
}
</style>
