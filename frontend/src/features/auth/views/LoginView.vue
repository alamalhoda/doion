<template>
  <div class="login-view">
    <form class="login-form" @submit.prevent="handleLogin">
      <h2>{{ $t('auth.login') }}</h2>

      <FormField
        v-model="formData.username"
        type="text"
        :label="$t('auth.username')"
        :error="getFieldError('username')"
        required
      />

      <FormField
        v-model="formData.password"
        type="password"
        :label="$t('auth.password')"
        :error="getFieldError('password')"
        required
      />

      <div v-if="error && !hasFieldErrors" class="form-error">
        {{ error }}
      </div>

      <AppButton
        :label="$t('auth.submit')"
        type="submit"
        :loading="isLoading"
        :disabled="isLoading"
      />
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '../stores/authStore'
import { ROUTES } from '@/constants/routes'
import FormField from '@/components/ui/FormField.vue'
import AppButton from '@/components/ui/AppButton.vue'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

const formData = reactive({
  username: '',
  password: '',
})

const fieldErrors = ref<Record<string, string[]>>({})
const isLoading = ref(false)
const error = ref<string | null>(null)

const hasFieldErrors = computed(() => Object.keys(fieldErrors.value).length > 0)

function getFieldError(field: string): string | undefined {
  const errors = fieldErrors.value[field]
  return errors?.[0]
}

async function handleLogin() {
  fieldErrors.value = {}
  error.value = null
  isLoading.value = true

  try {
    await authStore.login({
      username: formData.username,
      password: formData.password,
    })

    // Redirect based on role
    if (authStore.isAdmin) {
      router.push(ROUTES.ADMIN_DASHBOARD)
    } else {
      router.push(ROUTES.USER_DASHBOARD)
    }
  } catch (err: any) {
    if (err.fieldErrors) {
      fieldErrors.value = err.fieldErrors
    } else {
      error.value = t(err.message || 'error.unknown')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-form {
  width: 100%;
  max-width: 400px;
  padding: var(--spacing-xl);
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.login-form h2 {
  margin-bottom: var(--spacing-xl);
  text-align: center;
  color: var(--color-text-primary);
  font-size: var(--font-size-lg);
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
</style>
