<template>
  <div class="rejection-form">
    <p class="rejection-form__prompt">
      {{ $t('admin.reject_reason_prompt') }}
    </p>
    <FormField
      v-model="selectedCode"
      type="select"
      :label="$t('admin.rejection_code')"
      :options="codeOptions"
      required
    />
    <FormField
      v-model="note"
      type="textarea"
      :label="$t('admin.rejection_reason')"
      :rows="3"
      required
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import FormField from '@/components/ui/FormField.vue'
import { REJECTION_CODE_LABELS, type RejectionCode } from '@/features/listings/types/listing'

const props = defineProps<{
  modelValue?: { code: RejectionCode; note: string }
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: { code: RejectionCode; note: string }): void
}>()

const selectedRejectionCode = ref<RejectionCode>(props.modelValue?.code || '')
const note = ref(props.modelValue?.note || '')

const codeOptions = Object.entries(REJECTION_CODE_LABELS).map(
  ([value, label]) => ({ value, label })
)

const emitValue = computed(() => ({
  code: selectedRejectionCode.value as RejectionCode,
  note: note.value,
}))

defineExpose({ emitValue })
</script>

<style scoped>
.rejection-form {
  padding: var(--spacing-md) 0;
}

.rejection-form__prompt {
  margin-bottom: var(--spacing-md);
  color: var(--text2);
  font-size: var(--font-size-base);
}
</style>
