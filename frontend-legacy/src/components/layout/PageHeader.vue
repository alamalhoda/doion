<template>
  <header class="page-header">
    <div class="page-header__inner">
      <h1
        v-if="title"
        class="page-header__title"
      >
        {{ title }}
      </h1>
      <p
        v-if="subtitle"
        class="page-header__subtitle"
      >
        {{ subtitle }}
      </p>
      <div
        v-if="$slots.actions"
        class="page-header__actions"
      >
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  subtitle?: string
}

defineProps<Props>()
</script>

<style scoped>
.page-header {
  background: var(--surface);
  padding: var(--spacing-xl) var(--spacing-xl);
  border-bottom: 1px solid var(--color-border);
}

.page-header__inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.page-header__title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
}

.page-header__subtitle {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
}

.page-header__actions {
  display: flex;
  gap: var(--spacing-sm);
}
</style>