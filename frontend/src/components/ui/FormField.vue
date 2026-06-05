<template>
  <div class="form-field">
    <label v-if="label" :for="id" class="form-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      class="form-input"
      :class="{ 'has-error': error }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string
  label?: string
  placeholder?: string
  type?: string
  id?: string
  error?: string
  disabled?: boolean
  required?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
})

const id = computed(() => props.id || `input-${Math.random().toString(36).substr(2, 9)}`)

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped>
.form-field {
  margin-bottom: var(--spacing-lg);
  width: 100%;
}

.form-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 500;
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
}

.required {
  color: var(--color-error);
  margin-left: 2px;
}

.form-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

.form-input.has-error {
  border-color: var(--color-error);
}

.form-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(255, 77, 79, 0.1);
}

.form-input:disabled {
  background: var(--color-gray-100);
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  margin-top: var(--spacing-sm);
  color: var(--color-error);
  font-size: var(--font-size-xs);
}
</style>
