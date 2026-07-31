<template>
  <div class="coming-soon-wrapper">
    <div
      v-if="!showPlaceholder"
      class="coming-soon-content"
    >
      <slot />
    </div>
    <div
      v-if="showPlaceholder"
      class="placeholder-overlay"
    >
      <div class="placeholder-card">
        <h2>{{ title }}</h2>
        <p>{{ description }}</p>
        <span class="placeholder-badge">{{ phase }}</span>
        <button
          class="btn btn--secondary btn--sm"
          @click="showPlaceholder = false"
        >
          مشاهده نمونه (Mock)
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  title: string
  description: string
  phase: string
}

defineProps<Props>()

const showPlaceholder = ref(true)
</script>

<style>
.coming-soon-wrapper {
  position: relative;
}

.coming-soon-content {
  position: relative;
  z-index: 1;
}

.placeholder-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  z-index: 10;
}

.placeholder-card {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  max-width: 400px;
  border: 2px solid var(--color-warning);
}

.placeholder-card h2 {
  margin: 0 0 var(--spacing-md);
  color: var(--color-text-primary);
}

.placeholder-card p {
  margin: 0 0 var(--spacing-lg);
  color: var(--color-text-secondary);
}

.placeholder-badge {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-md);
  background: var(--color-warning);
  color: #fff;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--spacing-md);
}
</style>
