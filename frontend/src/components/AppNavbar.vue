<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <RouterLink to="/" class="navbar-brand">
        <span class="navbar-brand-text">پلتفرم چک‌بازار</span>
      </RouterLink>

      <div class="navbar-links">
        <RouterLink to="/" class="navbar-link" active-class="active">داشبورد</RouterLink>
        <RouterLink to="/management" class="navbar-link" active-class="active">مدیریت</RouterLink>
      </div>

      <div class="navbar-actions">
        <button class="btn-ghost" @click="handleLogout" v-if="isAuthenticated">
          خروج
        </button>
        <RouterLink v-else to="/login" class="btn-gold">
          ورود
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/features/auth/stores/authStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style>
/* ... existing styles ... */
</style>
