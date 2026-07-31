<template>
  <span
    class="stat-badge"
    :class="classes"
  >
    <span class="stat-badge-value">{{ displayValue }}</span>
    <span
      v-if="label"
      class="stat-badge-label"
    >{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    value: string | number
    label?: string
    variant?: 'default' | 'gold' | 'teal' | 'orange' | 'red'
    size?: 'sm' | 'md' | 'lg'
  }>(),
  {
    label: '',
    variant: 'default',
    size: 'md',
  }
)

const classes = computed(
  () => `stat-badge--${props.variant} stat-badge--${props.size}`
)

const displayValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString('fa-IR')
  }
  return props.value
})
</script>

<style>
.stat-badge {
  display: inline-flex;
  flex-direction: column;
  gap: 0.15rem;
}

.stat-badge-value {
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
}

.stat-badge-label {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}

/* Sizes */
.stat-badge--sm .stat-badge-value {
  font-size: 1.1rem;
}
.stat-badge--md .stat-badge-value {
  font-size: 1.5rem;
}
.stat-badge--lg .stat-badge-value {
  font-size: 1.75rem;
}

/* Variants */
.stat-badge--gold .stat-badge-value {
  color: var(--gold);
}
.stat-badge--teal .stat-badge-value {
  color: var(--teal);
}
.stat-badge--orange .stat-badge-value {
  color: var(--orange);
}
.stat-badge--red .stat-badge-value {
  color: var(--red);
}
</style>
