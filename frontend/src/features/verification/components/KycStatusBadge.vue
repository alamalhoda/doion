<template>
  <n-tag :type="statusType" :size="size">
    {{ status }}
  </n-tag>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import type { VerificationStatus } from '@/features/verification/types/verification'

const props = defineProps<{
  status: VerificationStatus
  size?: 'default' | 'small' | 'large'
}>()

const { t } = useI18n()

const size = computed(() => props.size || 'default')

const statusType = computed<'info' | 'success' | 'error' | 'warning'>(() => {
  switch (props.status) {
    case 'pending': return 'warning'
    case 'approved': return 'success'
    case 'rejected': return 'error'
    default: return 'default'
  }
})
</script>