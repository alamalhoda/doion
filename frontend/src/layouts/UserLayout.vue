<template>
  <div class="user-layout">
    <!-- Top Navigation (User) -->
    <nav class="navbar navbar--user">
      <div class="navbar-inner">
        <RouterLink to="/app" class="navbar-brand">
          <span class="navbar-brand-text">چک‌بازار</span>
        </RouterLink>

        <div class="navbar-links">
          <RouterLink to="/app" class="navbar-link" active-class="active">داشبورد</RouterLink>
          <RouterLink to="/app/listings" class="navbar-link" active-class="active">آگهی‌های من</RouterLink>
        </div>

        <div class="navbar-actions">
          <button class="btn-ghost" @click="handleLogout">
            خروج
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="user-main">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
.user-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

.user-main {
  flex: 1;
  padding: 2rem 1rem;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .user-main {
    padding: 1rem 0.75rem;
  }
}
</style>
