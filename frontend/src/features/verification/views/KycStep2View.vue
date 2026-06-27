<template>
  <n-space vertical :size="24">
    <n-space align="start" :size="12">
      <n-h2>{{ t('kyc.step2.title') }}</n-h2>
      <n-p text-color="gray">{{ t('kyc.step2.description') }}</n-p>
    </n-space>

    <n-card :bordered="false">
      <n-space vertical :size="20">
        <UploadArea
          accept=".jpg,.jpeg,.png"
          :maxSize="5 * 1024 * 1024"
          document-type="national_id_front"
          @uploaded="onUploaded('national_id_front', $event)"
        />
        <UploadArea
          accept=".jpg,.jpeg,.png"
          :maxSize="5 * 1024 * 1024"
          document-type="national_id_back"
          @uploaded="onUploaded('national_id_back', $event)"
        />

        <n-space justify="end">
          <n-button
            type="primary"
            :loading="store.loading"
            :disabled="!allUploaded"
            @click="handleSubmit"
          >
            {{ t('kyc.submit_verification') }}
          </n-button>
        </n-space>
      </n-space>
    </n-card>
  </n-space>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useVerificationStore } from '@/features/verification/stores/verificationStore'
import UploadArea from '@/features/verification/components/UploadArea.vue'
import { ROUTES } from '@/constants/routes'
import { useToast } from 'vue-toastification'

const router = useRouter()
const { t } = useI18n()
const store = useVerificationStore()
const toast = useToast()

const files = reactive<Record<string, File>>({})

function onUploaded(type: string, event: { file: File }) {
  files[type] = event.file
}

const allUploaded = computed(() => !!files['national_id_front'] && !!files['national_id_back'])

async function handleSubmit() {
  try {
    const formData = new FormData()
    formData.append('full_name', store.personalInfo.full_name)
    formData.append('national_id', store.personalInfo.national_id)
    if (store.personalInfo.company_name) {
      formData.append('company_name', store.personalInfo.company_name)
    }
    if (files['national_id_front']) {
      formData.append('national_id_front', files['national_id_front'])
    }
    if (files['national_id_back']) {
      formData.append('national_id_back', files['national_id_back'])
    }

    await store.startVerification(formData as any)
    toast.success(t('kyc.submitted_success'))
    router.push(`${ROUTES.VERIFICATION_KYC_START}/status`)
  } catch (error: any) {
    toast.error(error.message || t('common.error'))
  }
}
</script>