<template>
  <span :class="['badge', `badge--${variant}`, { 'badge--dot': dot }]">
    <span
      v-if="dot"
      class="badge__dot"
    />
    <span
      v-else
      class="badge__text"
    ><slot /></span>
  </span>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger'
  dot?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  dot: false,
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
}

.badge--primary {
  background: var(--color-primary);
  color: #fff;
}

.badge--secondary {
  background: var(--surface2);
  color: var(--color-text-primary);
}

.badge--success {
  background: var(--color-success);
  color: #fff;
}

.badge--warning {
  background: var(--color-warning);
  color: #fff;
}

.badge--danger {
  background: var(--color-error);
  color: #fff;
}

.badge__dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}
</style>