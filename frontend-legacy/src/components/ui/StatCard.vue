<template>
  <div
    class="stat-card"
    :class="[`stat-card--${variant}`, { 'stat-card--trend-up': trend === 'up', 'stat-card--trend-down': trend === 'down' }]"
  >
    <div
      v-if="icon || $slots.icon"
      class="stat-card__icon"
    >
      <slot name="icon">
        <span class="stat-card__icon-emoji">{{ icon }}</span>
      </slot>
    </div>
    <div class="stat-card__body">
      <div class="stat-card__value">
        {{ value }}
      </div>
      <div class="stat-card__title">
        {{ title }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon?: string
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  trend?: 'up' | 'down' | 'none'
}

withDefaults(defineProps<Props>(), {
  icon: '',
  variant: 'default',
  trend: 'none',
})
</script>

<style scoped>
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  transition: box-shadow var(--transition-base), transform var(--transition-base);
}

.stat-card:hover {
  box-shadow: var(--shadow);
  transform: translateY(-1px);
}

.stat-card__icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1.2rem;
  background: var(--surface2);
  color: var(--color-text-secondary);
}

.stat-card__icon-emoji {
  font-size: 1.2rem;
  line-height: 1;
}

.stat-card__body {
  min-width: 0;
}

.stat-card__value {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--text1);
  line-height: 1.1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.stat-card__title {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin-top: 0.15rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Variants */
.stat-card--success .stat-card__icon {
  background: var(--color-success-light);
  color: var(--color-success);
}

.stat-card--warning .stat-card__icon {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.stat-card--danger .stat-card__icon {
  background: var(--color-error-light);
  color: var(--color-error);
}

.stat-card--info .stat-card__icon {
  background: #E3F2FD;
  color: #1976D2;
}

.stat-card--success .stat-card__value {
  color: var(--color-success);
}

.stat-card--warning .stat-card__value {
  color: var(--color-warning);
}

.stat-card--danger .stat-card__value {
  color: var(--color-error);
}

.stat-card--info .stat-card__value {
  color: #1976D2;
}

@media (max-width: 768px) {
  .stat-card {
    padding: 0.85rem 1rem;
    gap: 0.65rem;
  }

  .stat-card__icon {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }

  .stat-card__value {
    font-size: 1.25rem;
  }

  .stat-card__title {
    font-size: 0.65rem;
  }
}
</style>
