<template>
  <div class="ds-panel" :class="{ 'ds-panel--sticky': sticky }">
    <div v-if="title || $slots.header" class="ds-panel-header">
      <slot name="header">
        <span class="ds-panel-title">{{ title }}</span>
      </slot>
    </div>
    <div class="ds-panel-body">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  sticky?: boolean
}>(), {
  sticky: false,
})
</script>

<style>
.ds-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.ds-panel--sticky {
  position: sticky;
  top: 78px;
}

.ds-panel-header {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--border);
}

.ds-panel-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.ds-panel-body {
  padding: 1rem 1.25rem;
}
</style>
