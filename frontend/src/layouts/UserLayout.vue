<template>
  <div class="user-layout">
    <Nav variant="user">
      <template #actions>
        <Button
          variant="ghost"
          @click="handleLogout"
        >
          خروج
        </Button>
      </template>
    </Nav>

    <main class="user-main">
      <slot />
    </main>

    <Footer />
  </div>
</template>

<script setup lang="ts">
import Nav from '@/components/layout/Nav.vue'
import Footer from '@/components/layout/Footer.vue'
import Button from '@/components/ui/Button.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/features/auth/stores/authStore'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
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
  padding: var(--spacing-xl);
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .user-main {
    padding: var(--spacing-lg) var(--spacing-md);
  }
}
</style>