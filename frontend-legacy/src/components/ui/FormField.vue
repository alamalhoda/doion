<template>
  <div class="form-field">
    <label
      v-if="label"
      :for="id"
      class="form-label"
    >
      {{ label }}
      <span
        v-if="required"
        class="required"
      >*</span>
    </label>
    <component
      :is="inputComponent"
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :rows="rows"
      class="form-input"
      :class="{ 'has-error': error }"
      @input="handleInput"
    />
    <p
      v-if="error"
      class="error-message"
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
  id?: string
  error?: string
  disabled?: boolean
  required?: boolean
  rows?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  rows: 3,
  label: '',
  placeholder: '',
  id: '',
  error: '',
})

const id = computed(() => props.id || `input-${Math.random().toString(36).substr(2, 9)}`)

const inputComponent = computed(() => props.type === 'textarea' ? 'textarea' : 'input')

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

function handleInput(event: Event): void {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement
  emit('update:modelValue', target.value)
}
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
  color: var(--text2);
  font-size: var(--font-size-sm);
}

.required {
  color: var(--red);
  margin-left: 2px;
}

.form-input {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text1);
  font-size: var(--font-size-sm);
  transition: border-color var(--transition-fast);
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: var(--navy-light);
  box-shadow: 0 0 0 3px rgba(42, 95, 168, 0.08);
}

.form-input.has-error {
  border-color: var(--red);
}

.form-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(192, 57, 43, 0.08);
}

.form-input:disabled {
  background: var(--surface2);
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  margin-top: var(--spacing-sm);
  color: var(--red);
  font-size: var(--font-size-xs);
}
</style>