<template>
  <n-space vertical :size="24">
    <n-space align="start" :size="12">
      <n-h2>{{ t('kyc.status.title') }}</n-h2>
    </n-space>

    <n-card v-if="verification" :bordered="false">
      <n-descriptions :column="1" label-placement="left">
        <n-descriptions-item :label="t('kyc.status')">
          <KycStatusBadge :status="verification.status" />
        </n-descriptions-item>
        <n-descriptions-item v-if="verification.rejection_reason" :label="t('kyc.reason')">
          {{ verification.rejection_reason }}
        </n-descriptions-item>
        <n-descriptions-item v-if="verification.rejection_code" :label="t('kyc.rejection_code')">
          <n-tag type="error">{{ verification.rejection_code }}</n-tag>
        </n-descriptions-item>
        <n-descriptions-item :label="t('kyc.submitted_at')">
          {{ formattedDate }}
        </n-descriptions-item>
      </n-descriptions>

      <n-space style="margin-top: 16px" :size="12">
        <n-button v-if="verification.status === 'rejected'" type="primary" @click="resubmit">
          {{ t('kyc.resubmit') }}
        </n-button>
        <n-button v-if="verification.status === 'approved'" @click="goToDashboard">
          {{ t('kyc.go_to_dashboard') }}
        </n-button>
      </n-space>
    </n-card>

    <n-empty v-else :description="t('kyc.no_verification_found')">
      <n-button type="primary" @click="goToStart">
        {{ t('kyc.start_verification') }}
      </n-button>
    </n-empty>
  </n-space>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useVerificationStore } from '@/features/verification/stores/verificationStore'
import KycStatusBadge from '@/features/verification/components/KycStatusBadge.vue'
import { ROUTES } from '@/constants/routes'
import { useToast } from 'vue-toastification'
import dayjs from 'dayjs'

const router = useRouter()
const { t } = useI18n()
const store = useVerificationStore()
const toast = useToast()

const verification = ref<any>(null)

const formattedDate = computed(() => {
  if (!verification.value?.created_at) return '-'
  try {
    return dayjs(verification.value.created_at).format('YYYY/MM/DD HH:mm')
  } catch {
    return verification.value.created_at
  }
})

onMounted(() => {
  loadVerification()
})

async function loadVerification() {
  try {
    verification.value = await store.getMyVerification()
  } catch (error: any) {
    if (error.response?.status !== 404) {
      toast.error(error.message || t('common.error'))
    }
  }
}

function resubmit() {
  router.push(`${ROUTES.VERIFICATION_KYC_START}/step-2`)
}

function goToStart() {
  router.push(ROUTES.VERIFICATION_KYC_START)
}

function goToDashboard() {
  router.push(ROUTES.USER_DASHBOARD)
}
</script>