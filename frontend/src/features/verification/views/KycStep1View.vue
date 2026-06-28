<template>
  <n-space
    vertical
    :size="24"
  >
    <n-space
      align="start"
      :size="12"
    >
      <n-h2>{{ t('kyc.step1.title') }}</n-h2>
      <n-p text-color="gray">
        {{ t('kyc.step1.description') }}
      </n-p>
    </n-space>

    <n-card :bordered="false">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
      >
        <n-form-item
          :label="t('kyc.full_name')"
          path="full_name"
        >
          <n-input
            v-model:value="formData.full_name"
            :placeholder="t('kyc.full_name_placeholder')"
            clearable
          />
        </n-form-item>
        <n-form-item
          :label="t('kyc.national_id')"
          path="national_id"
        >
          <n-input
            v-model:value="formData.national_id"
            :placeholder="t('kyc.national_id_placeholder')"
            maxlength="10"
            clearable
          />
        </n-form-item>
        <n-form-item
          :label="t('kyc.company_name')"
          path="company_name"
        >
          <n-input
            v-model:value="formData.company_name"
            :placeholder="t('kyc.company_name_placeholder')"
            clearable
          />
        </n-form-item>
        <n-space justify="end">
          <n-button
            type="primary"
            :loading="store.loading"
            @click="handleSubmit"
          >
            {{ t('kyc.next_step') }}
          </n-button>
        </n-space>
      </n-form>
    </n-card>
  </n-space>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useVerificationStore } from '@/features/verification/stores/verificationStore'
import { ROUTES } from '@/constants/routes'
import { useToast } from 'vue-toastification'

const router = useRouter()
const { t } = useI18n()
const store = useVerificationStore()
const toast = useToast()
const formRef = ref()

const formData = reactive({
  full_name: '',
  national_id: '',
  company_name: '',
})

const rules = {
  full_name: {
    required: true,
    message: t('kyc.full_name_required'),
    trigger: 'blur',
  },
  national_id: {
    required: true,
    len: 10,
    message: t('kyc.national_id_length'),
    trigger: 'blur',
  },
  company_name: {},
}

async function handleSubmit() {
  try {
    await formRef.value?.validate()
    await store.startVerification({
      full_name: formData.full_name,
      national_id: formData.national_id,
      company_name: formData.company_name,
    })
    toast.success(t('kyc.step1_success'))
    router.push(`${ROUTES.VERIFICATION_KYC_START}/step-2`)
  } catch (error: any) {
    toast.error(error.message || t('common.error'))
  }
}
</script>