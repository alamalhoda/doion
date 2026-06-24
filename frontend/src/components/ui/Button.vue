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
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success'
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
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  border: 1px solid transparent;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--color-primary);
  color: #fff;
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
}

.btn--secondary {
  background: var(--surface2);
  color: var(--color-text-primary);
  border-color: var(--color-border);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--color-gray-100);
}

.btn--ghost {
  background: transparent;
  color: var(--color-text-primary);
}

.btn--ghost:hover:not(:disabled) {
  background: var(--color-gray-100);
}

.btn--danger {
  background: var(--color-error);
  color: #fff;
}

.btn--danger:hover:not(:disabled) {
  background: #ff2c2c;
}

.btn--success {
  background: var(--color-success);
  color: #fff;
}

.btn--success:hover:not(:disabled) {
  opacity: 0.9;
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