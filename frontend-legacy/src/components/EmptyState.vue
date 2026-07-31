<template>
  <div class="empty-state">
    <div class="empty-state-icon">
      <slot name="icon">
        {{ icon }}
      </slot>
    </div>
    <h3 class="empty-state-title">
      {{ title }}
    </h3>
    <p class="empty-state-description">
      {{ description }}
    </p>
    <div
      v-if="$slots.actions"
      class="empty-state-actions"
    >
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  icon?: string
  title: string
  description: string
}>(), {
  icon: '📭',
})
</script>

<style>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3.5rem 1rem;
  text-align: center;
}

.empty-state-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
  margin: 0 0 0.4rem;
}

.empty-state-description {
  font-size: var(--font-size-base);
  color: var(--text3);
  max-width: 280px;
  margin: 0 auto 1.25rem;
  line-height: 1.6;
}

.empty-state-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
