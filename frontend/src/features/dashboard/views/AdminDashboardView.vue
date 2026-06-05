<template>
  <div class="admin-dashboard">
    <h1>{{ $t('dashboard.admin_title') }}</h1>
    <p class="welcome-text">{{ $t('dashboard.welcome') }}, {{ authStore.user?.username }}!</p>

    <div class="dashboard-grid">
      <div class="dashboard-card">
        <h3>منابع</h3>
        <p>مدیریت منابع سیستم</p>
      </div>
      <div class="dashboard-card">
        <h3>کاربران</h3>
        <p>مدیریت کاربران</p>
      </div>
      <div class="dashboard-card">
        <h3>تنظیمات</h3>
        <p>تنظیمات سیستم</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/features/auth/stores/authStore'

const authStore = useAuthStore()
</script>

<style scoped>
.admin-dashboard h1 {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text-primary);
}

.welcome-text {
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-secondary);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.dashboard-card {
  padding: var(--spacing-lg);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: box-shadow 0.2s;
}

.dashboard-card:hover {
  box-shadow: var(--shadow-md);
}

.dashboard-card h3 {
  margin-bottom: var(--spacing-md);
  color: var(--color-primary);
}

.dashboard-card p {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}
</style>
