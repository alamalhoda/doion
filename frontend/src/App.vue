<template>
  <div class="framework-root">
    <AppNavbar />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<style>
.framework-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg, #f8f9fa);
}

.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
}
</style>
