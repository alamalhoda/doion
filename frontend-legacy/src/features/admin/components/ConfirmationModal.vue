<template>
  <AppButton
    :label="$t('common.cancel')"
    variant="secondary"
    @click="$emit('cancel')"
  />
  <AppButton
    :label="confirmLabel"
    :variant="confirmVariant"
    :loading="loading"
    @click="$emit('confirm')"
  />
</template>

<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'

withDefaults(
  defineProps<{
    confirmLabel?: string
    confirmVariant?: 'primary' | 'danger' | 'secondary' | 'teal'
    loading?: boolean
  }>(),
  {
    confirmLabel: 'common.confirm',
    confirmVariant: 'primary',
    loading: false,
  }
)

defineEmits<{
  (e: 'cancel'): void
  (e: 'confirm'): void
}>()
</script>
