<template>
  <div
    class="app-button"
    :class="[variant, { disabled }]"
  >
    <button
      :disabled="disabled || loading"
      :type="type"
      @click="$emit('click')"
    >
      {{ label }}
      <span
        v-if="loading"
        class="spinner"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  label: string
  variant?: 'primary' | 'secondary' | 'danger'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
  loading: false,
})

defineEmits<{
  click: []
}>()
</script>

<style scoped>
.app-button button {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.primary button {
  background: var(--color-primary);
  color: white;
}

.primary button:hover:not(:disabled) {
  background: var(--color-primary-dark);
}

.secondary button {
  background: var(--color-gray-200);
  color: var(--color-text-primary);
}

.secondary button:hover:not(:disabled) {
  background: var(--color-gray-300);
}

.danger button {
  background: var(--color-error);
  color: white;
}

.danger button:hover:not(:disabled) {
  background: #ff2c2c;
}

.app-button.disabled button,
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
