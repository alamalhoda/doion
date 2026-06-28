<template>
  <div class="register-view">
    <form
      v-if="!otpSent"
      class="register-form"
      @submit.prevent="handleRegister"
    >
      <h2>{{ $t('auth.register') }}</h2>

      <FormField
        v-model="formData.username"
        type="text"
        :label="$t('auth.username')"
        :error="getFieldError('username')"
        required
      />

      <FormField
        v-model="formData.email"
        type="email"
        :label="$t('auth.email')"
        :error="getFieldError('email')"
      />

      <FormField
        v-model="formData.name"
        type="text"
        :label="$t('auth.full_name')"
        :error="getFieldError('name')"
      />

      <FormField
        v-model="formData.phone"
        type="tel"
        :label="$t('auth.phone_number')"
        :error="getFieldError('phone')"
      />

      <div class="role-selector">
        <label class="form-label">{{ $t('auth.role') }}</label>
        <NSelect
          v-model:value="formData.role"
          :options="roleOptions"
          :placeholder="$t('auth.select_role')"
        />
      </div>

      <FormField
        v-model="formData.password"
        type="password"
        :label="$t('auth.password')"
        :error="getFieldError('password')"
        required
      />

      <FormField
        v-model="formData.password_confirm"
        type="password"
        :label="$t('auth.confirm_password')"
        :error="getFieldError('password_confirm')"
        required
      />

      <div
        v-if="error && !hasFieldErrors"
        class="form-error"
      >
        {{ error }}
      </div>

      <AppButton
        :label="$t('auth.register')"
        type="submit"
        :loading="isLoading"
        :disabled="isLoading"
      />

      <div class="login-link">
        <RouterLink :to="ROUTES.LOGIN">
          {{ $t('auth.already_have_account') }}
        </RouterLink>
      </div>
    </form>

    <form
      v-else
      class="register-form"
      @submit.prevent="handleOtpVerify"
    >
      <h2>{{ $t('otp_title') }}</h2>
      <p class="otp-description">
        {{ $t('otp_description') }}
      </p>

      <FormField
        v-model="otpCode"
        type="text"
        :label="$t('otp_code')"
        :error="otpError"
        required
      />

      <div
        v-if="otpSuccess"
        class="form-success"
      >
        {{ $t('otp_success') }}
      </div>

      <AppButton
        :label="$t('otp_submit')"
        type="submit"
        :loading="isLoading"
        :disabled="isLoading"
      />

      <div class="login-link">
        <a
          href="#"
          @click.prevent="resendOtp"
        >{{ $t('otp_resend') }}</a>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { NSelect } from 'naive-ui'
import FormField from '@/components/ui/FormField.vue'
import AppButton from '@/components/ui/AppButton.vue'
import { ROUTES } from '@/constants/routes'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'

const router = useRouter()
const { t } = useI18n()

const formData = reactive({
  username: '',
  email: '',
  name: '',
  phone: '',
  role: 'check_holder' as 'check_holder' | 'investor',
  password: '',
  password_confirm: '',
})

const fieldErrors = ref<Record<string, string[]>>({})
const isLoading = ref(false)
const error = ref<string | null>(null)
const otpSent = ref(false)
const otpCode = ref('')
const otpError = ref<string | undefined>(undefined)
const otpSuccess = ref(false)

const hasFieldErrors = computed(() => Object.keys(fieldErrors.value).length > 0)

const roleOptions = computed(() => [
  { label: t('auth.check_holder'), value: 'check_holder' },
  { label: t('auth.investor'), value: 'investor' },
])

function getFieldError(field: string): string | undefined {
  const errors = fieldErrors.value[field]
  return errors?.[0]
}

async function handleRegister() {
  fieldErrors.value = {}
  error.value = null
  isLoading.value = true

  try {
    await apiClient.post('/api/v1/identity/register/', {
      username: formData.username,
      email: formData.email,
      name: formData.name,
      phone: formData.phone,
      role: formData.role,
      password: formData.password,
      password_confirm: formData.password_confirm,
    })

    otpSent.value = true
  } catch (err: unknown) {
    const normalized = normalizeApiError(err)
    if (normalized.fieldErrors) {
      fieldErrors.value = normalized.fieldErrors
    } else {
      error.value = t(normalized.message || 'error.unknown')
    }
  } finally {
    isLoading.value = false
  }
}

async function handleOtpVerify() {
  otpError.value = undefined
  otpSuccess.value = false
  isLoading.value = true

  try {
    await new Promise((resolve) => setTimeout(resolve, 500))
    if (otpCode.value.length === 6) {
      otpSuccess.value = true
      setTimeout(() => router.push(ROUTES.LOGIN), 1000)
    } else {
      otpError.value = t('error.validation_error')
    }
  } finally {
    isLoading.value = false
  }
}

function resendOtp() {
  otpCode.value = ''
  otpError.value = undefined
}
</script>

<style scoped>
.register-view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-form {
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.register-form h2 {
  margin-bottom: var(--spacing-xl);
  text-align: center;
  color: var(--navy);
  font-size: var(--font-size-lg);
}

.otp-description {
  text-align: center;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-sm);
}

.role-selector {
  margin-bottom: var(--spacing-lg);
}

.form-error {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  background: var(--red-light);
  border: 1px solid var(--red);
  border-radius: var(--radius-sm);
  color: var(--red);
  font-size: var(--font-size-sm);
}

.form-success {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  background: var(--green-light, #e8f5e9);
  border: 1px solid var(--green, #4caf50);
  border-radius: var(--radius-sm);
  color: var(--green, #2e7d32);
  font-size: var(--font-size-sm);
}

.login-link {
  margin-top: var(--spacing-lg);
  text-align: center;
}

.login-link a {
  color: var(--navy);
  text-decoration: none;
  font-size: var(--font-size-sm);
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
