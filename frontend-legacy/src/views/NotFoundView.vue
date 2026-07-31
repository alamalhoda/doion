<template>
  <div class="not-found-view">
    <div class="not-found-content">
      <h1>404</h1>
      <p>{{ $t('error.unknown') }}</p>
      <router-link
        :to="ROUTES.LOGIN"
        class="back-link"
      >
        {{ $t('auth.login') }}
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ROUTES } from '@/constants/routes'
</script>

<style scoped>
.not-found-view {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 4rem;
  color: var(--color-primary);
  margin-bottom: var(--spacing-lg);
}

.not-found-content p {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
}

.back-link {
  display: inline-block;
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: background 0.2s;
}

.back-link:hover {
  background: var(--color-primary-dark);
}
</style>
