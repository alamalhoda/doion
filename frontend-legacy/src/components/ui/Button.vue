<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'btn',
      `btn--${variant}`,
      {
        'btn--loading': loading,
        'btn--icon': iconOnly,
        'btn--block': block,
      }
    ]"
    @click="emit('click', $event)"
  >
    <span
      v-if="loading"
      class="btn__spinner"
    />
    <Icon
      v-if="icon && !loading"
      :name="icon"
      :size="iconSize"
    />
    <span
      v-if="!iconOnly"
      class="btn__text"
    ><slot /></span>
  </button>
</template>

<script setup lang="ts">
import Icon from './Icon.vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success' | 'teal' | 'gold'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  icon?: string
  iconOnly?: boolean
  iconSize?: number
  block?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
  loading: false,
  icon: '',
  iconSize: 16,
  block: false,
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: 0.6rem 1.75rem;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  border: 1px solid transparent;
  line-height: 1.5;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--navy);
  color: #fff;
}

.btn--primary:hover:not(:disabled) {
  background: var(--navy-mid);
}

.btn--secondary {
  background: var(--surface2);
  color: var(--text1);
  border-color: var(--border);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--border);
}

.btn--ghost {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
}

.btn--ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
}

.btn--danger {
  background: var(--red);
  color: #fff;
}

.btn--danger:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--success {
  background: var(--teal);
  color: #fff;
}

.btn--success:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--teal {
  background: var(--teal);
  color: #fff;
}

.btn--teal:hover:not(:disabled) {
  opacity: 0.9;
}

.btn--gold {
  background: var(--gold);
  color: #1A1200;
}

.btn--gold:hover:not(:disabled) {
  background: var(--gold-light);
}

.btn--block {
  width: 100%;
}

.btn__spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.btn--secondary .btn__spinner,
.btn--ghost .btn__spinner {
  border-top-color: var(--color-text-primary);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>