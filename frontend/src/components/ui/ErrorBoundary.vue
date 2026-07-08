<template>
  <slot v-if="!error" />

  <div
    v-else
    class="error-boundary"
  >
    <NResult
      status="error"
      :title="$t('common.something_went_wrong')"
      :description="errorMessage"
    >
      <template #footer>
        <NButton @click="reset">
          {{ $t('common.retry') }}
        </NButton>
      </template>
    </NResult>
  </div>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured, h } from 'vue'
import { NResult, NButton } from 'naive-ui'
import { useI18n } from 'vue-i18n'

const props = withDefaults(defineProps<{
  errorFallback?: string
}>(), {
  errorFallback: '',
})

const { t } = useI18n()
const error = ref<Error | null>(null)

onErrorCaptured((err: unknown) => {
  if (err instanceof Error) {
    error.value = err
  } else if (err && typeof err === 'object' && 'message' in err) {
    error.value = new Error((err as { message: string }).message)
  } else {
    error.value = new Error(String(err))
  }
  return false
})

function reset(): void {
  error.value = null
}

const errorMessage = ref<string>(() => {
  if (props.errorFallback) return props.errorFallback
  return t('error.unknown')
})
</script>

<style scoped>
.error-boundary {
  padding: var(--spacing-xl);
  text-align: center;
}
</style>
