<template>
  <div class="ds-card" :class="[`ds-card--${variant}`, { 'ds-card--hoverable': hoverable, 'ds-card--paddingless': paddingless }]">
    <div v-if="$slots.header || title" class="ds-card-header">
      <slot name="header">
        <h3 class="ds-card-title">{{ title }}</h3>
        <p v-if="subtitle" class="ds-card-subtitle">{{ subtitle }}</p>
      </slot>
    </div>
    <div class="ds-card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="ds-card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  subtitle?: string
  variant?: 'default' | 'navy' | 'surface'
  hoverable?: boolean
  paddingless?: boolean
}>(), {
  variant: 'default',
  hoverable: false,
  paddingless: false,
})
</script>

<style>
.ds-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: box-shadow var(--transition-base), border-color var(--transition-base), transform var(--transition-base);
}

.ds-card--hoverable:hover {
  border-color: var(--navy-light);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.ds-card--navy {
  background: var(--navy);
  border-color: transparent;
}

.ds-card-header {
  padding: 1.1rem;
  border-bottom: 1px solid var(--border);
}

.ds-card--navy .ds-card-header {
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.ds-card-title {
  margin: 0;
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
}

.ds-card--navy .ds-card-title {
  color: #fff;
}

.ds-card-subtitle {
  margin: 0.2rem 0 0;
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.ds-card--navy .ds-card-subtitle {
  color: rgba(255, 255, 255, 0.6);
}

.ds-card-body {
  padding: 1.1rem;
}

.ds-card--paddingless .ds-card-body {
  padding: 0;
}

.ds-card-footer {
  padding: 0.75rem 1.1rem;
  border-top: 1px solid var(--border);
  background: var(--surface2);
}
</style>
