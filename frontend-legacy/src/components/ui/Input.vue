<template>
  <div class="input-wrapper">
    <label
      v-if="label"
      :for="inputId"
      class="input-label"
    >
      {{ label }}
      <span
        v-if="required"
        class="required"
      >*</span>
    </label>
    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :class="['base-input', { 'has-error': error }]"
      @input="handleInput"
    >
    <p
      v-if="error"
      class="input-error"
    >
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string
  label?: string
  placeholder?: string
  type?: string
  disabled?: boolean
  required?: boolean
  error?: string
  id?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  label: '',
  placeholder: '',
  error: '',
  id: '',
})

const inputId = computed(() => props.id || `input-${Math.random().toString(36).substr(2, 9)}`)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.input-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
}

.required {
  color: var(--red);
  margin-left: 2px;
}

.base-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text1);
  font-size: var(--font-size-sm);
  transition: border-color var(--transition-fast);
}

.base-input:focus {
  outline: none;
  border-color: var(--navy-light);
  box-shadow: 0 0 0 3px rgba(42, 95, 168, 0.08);
}

.base-input.has-error {
  border-color: var(--red);
}

.base-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(192, 57, 43, 0.08);
}

.base-input:disabled {
  background: var(--surface2);
  cursor: not-allowed;
  opacity: 0.6;
}

.input-error {
  margin-top: 2px;
  color: var(--red);
  font-size: var(--font-size-xs);
}
</style>