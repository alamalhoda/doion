<template>
  <div class="register-view">
    <form
      class="register-form"
      @submit.prevent="handleRegister"
    >
      <h2>{{ $t('auth.register') }}</h2>

      <FormField
        v-model="formData.phoneNumber"
        type="tel"
        :label="$t('auth.phone_number')"
        :error="getFieldError('phoneNumber')"
        required
      />

      <FormField
        v-model="formData.email"
        type="email"
        :label="$t('auth.email')"
        :error="getFieldError('email')"
        required
      />

      <FormField
        v-model="formData.fullName"
        type="text"
        :label="$t('auth.full_name')"
        :error="getFieldError('fullName')"
        required
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
        v-model="formData.confirmPassword"
        type="password"
        :label="$t('auth.confirm_password')"
        :error="getFieldError('confirmPassword')"
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

const router = useRouter()
const { t } = useI18n()

const formData = reactive({
  phoneNumber: '',
  email: '',
  fullName: '',
  role: 'CheckHolder' as 'CheckHolder' | 'Investor',
  password: '',
  confirmPassword: '',
})

const fieldErrors = ref<Record<string, string[]>>({})
const isLoading = ref(false)
const error = ref<string | null>(null)

const hasFieldErrors = computed(() => Object.keys(fieldErrors.value).length > 0)

const roleOptions = computed(() => [
  { label: t('auth.check_holder'), value: 'CheckHolder' },
  { label: t('auth.investor'), value: 'Investor' },
])

function getFieldError(field: string): string | undefined {
  const errors = fieldErrors.value[field]
  return errors?.[0]
}

async function handleRegister() {
  fieldErrors.value = {}
  error.value = null
  isLoading.value = true

  // Validate passwords match
  if (formData.password !== formData.confirmPassword) {
    fieldErrors.value.confirmPassword = [t('auth.passwords_must_match')]
    isLoading.value = false
    return
  }

  try {
    // TODO: Implement registration API call
    console.log('Registration data:', formData)
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Navigate to login after successful registration
    router.push(ROUTES.LOGIN)
  } catch (err: unknown) {
    const errorObj = err as { fieldErrors?: Record<string, string[]>; message?: string }
    if (errorObj.fieldErrors) {
      fieldErrors.value = errorObj.fieldErrors
    } else {
      error.value = t(errorObj.message || 'error.unknown')
    }
  } finally {
    isLoading.value = false
  }
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
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.register-form h2 {
  margin-bottom: var(--spacing-xl);
  text-align: center;
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
}

.role-selector {
  margin-bottom: var(--spacing-lg);
}

.form-error {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  background: #fff2f0;
  border: 1px solid var(--color-error);
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: var(--font-size-sm);
}

.login-link {
  margin-top: var(--spacing-lg);
  text-align: center;
}

.login-link a {
  color: var(--color-primary);
  text-decoration: none;
  font-size: var(--font-size-sm);
}

.login-link a:hover {
  text-decoration: underline;
}
</style>