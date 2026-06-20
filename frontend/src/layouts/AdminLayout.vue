<template>
  <div class="admin-layout">
    <!-- Top Navigation (Admin) -->
    <nav class="navbar navbar--admin">
      <div class="navbar-inner">
        <RouterLink to="/admin" class="navbar-brand">
          <span class="navbar-brand-text">چک‌بازار</span>
        </RouterLink>

        <div class="navbar-links">
          <RouterLink to="/admin" class="navbar-link" active-class="active">داشبورد</RouterLink>
          <RouterLink to="/admin/management" class="navbar-link" active-class="active">مدیریت</RouterLink>
        </div>

        <div class="navbar-actions">
          <button class="btn-ghost" @click="handleLogout">
            خروج
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="admin-main">
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
.admin-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

.admin-main {
  flex: 1;
  padding: 2rem;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
}
</style>
