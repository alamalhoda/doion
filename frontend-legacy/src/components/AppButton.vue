<template>
  <component
    :is="tag"
    class="btn"
    :class="classes"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'primary' | 'secondary' | 'ghost' | 'gold' | 'danger' | 'teal'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
    block?: boolean
    rounded?: boolean
  }>(),
  {
    variant: 'primary',
    size: 'md',
    disabled: false,
    block: false,
    rounded: false,
  }
)

const tag = computed(() => (props.block ? 'button' : 'button'))

const classes = computed(() => [
  `btn--${props.variant}`,
  `btn--${props.size}`,
  {
    'btn--block': props.block,
    'btn--rounded': props.rounded,
    'btn--disabled': props.disabled,
  },
])
</script>

<style>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  font-family: var(--font-family);
  font-weight: var(--font-weight-semibold);
  line-height: 1.4;
  cursor: pointer;
  transition:
    background-color var(--transition-fast),
    border-color var(--transition-fast),
    color var(--transition-fast),
    box-shadow var(--transition-fast),
    transform var(--transition-fast);
  white-space: nowrap;
  user-select: none;
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
  pointer-events: none;
}

/* Sizes */
.btn--sm {
  padding: 0.35rem 0.9rem;
  font-size: var(--font-size-xs);
  border-radius: var(--radius-sm);
}

.btn--md {
  padding: 0.6rem 1.6rem;
  font-size: var(--font-size-base);
}

.btn--lg {
  padding: 0.75rem 2rem;
  font-size: var(--font-size-md);
  border-radius: var(--radius);
}

/* Block */
.btn--block {
  width: 100%;
}

/* Rounded pill */
.btn--rounded {
  border-radius: 9999px;
}

/* Variants */
.btn--primary {
  background: var(--navy);
  border-color: var(--navy);
  color: #fff;
}
.btn--primary:hover:not(:disabled) {
  background: var(--navy-mid);
  border-color: var(--navy-mid);
}

.btn--secondary {
  background: transparent;
  border-color: var(--border2);
  color: var(--text1);
}
.btn--secondary:hover:not(:disabled) {
  background: var(--surface2);
  border-color: var(--text3);
}

.btn--ghost {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.3);
  color: #fff;
}
.btn--ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.45);
}

.btn--gold {
  background: var(--gold);
  border-color: var(--gold);
  color: #1a1200;
}
.btn--gold:hover:not(:disabled) {
  background: var(--gold-light);
  border-color: var(--gold-light);
}

.btn--danger {
  background: transparent;
  border-color: var(--red);
  color: var(--red);
}
.btn--danger:hover:not(:disabled) {
  background: var(--red-light);
}

.btn--teal {
  background: var(--teal);
  border-color: var(--teal);
  color: #fff;
}
.btn--teal:hover:not(:disabled) {
  background: #0a6560;
}
</style>
