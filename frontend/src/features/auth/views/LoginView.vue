<template>
  <div class="login-view">
    <form
      class="login-form"
      @submit.prevent="handleLogin"
    >
      <h2>{{ $t('auth.login') }}</h2>

      <FormField
        v-model="formData.identifier"
        type="tel"
        :label="$t('auth.identifier')"
        :error="getFieldError('identifier')"
        required
      />

      <FormField
        v-model="formData.password"
        type="password"
        :label="$t('auth.password')"
        :error="getFieldError('password')"
        required
      />

      <div
        v-if="error && !hasFieldErrors"
        class="form-error"
      >
        {{ error }}
      </div>

      <AppButton
        :label="$t('auth.submit')"
        type="submit"
        :loading="isLoading"
        :disabled="isLoading"
      />

      <div class="register-link">
        <RouterLink :to="ROUTES.REGISTER">
          {{ $t('auth.register_link') }}
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
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
  identifier: '',
  password: '',
})

const fieldErrors = ref<Record<string, string[]>>({})
const isLoading = ref(false)
const error = ref<string | null>(null)

const hasFieldErrors = computed(() => Object.keys(fieldErrors.value).length > 0)

onMounted(async () => {
  if (authStore.isAuthenticated) {
    if (authStore.isAdmin) {
      router.push(ROUTES.ADMIN_DASHBOARD)
    } else {
      router.push(ROUTES.USER_DASHBOARD)
    }
    return
  }
  try {
    await authStore.restoreAuth()
    if (authStore.isAuthenticated) {
      if (authStore.isAdmin) {
        router.push(ROUTES.ADMIN_DASHBOARD)
      } else {
        router.push(ROUTES.USER_DASHBOARD)
      }
    }
  } catch {
    // User not authenticated, stay on login page
  }
})

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
      identifier: formData.identifier,
      password: formData.password,
    })

    // Redirect based on role
    if (authStore.isAdmin) {
      router.push(ROUTES.ADMIN_DASHBOARD)
    } else {
      router.push(ROUTES.USER_DASHBOARD)
    }
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
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
}

.login-form h2 {
  margin-bottom: var(--spacing-xl);
  text-align: center;
  color: var(--navy);
  font-size: var(--font-size-lg);
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

.register-link {
  margin-top: var(--spacing-lg);
  text-align: center;
}

.register-link a {
  color: var(--navy);
  text-decoration: none;
  font-size: var(--font-size-sm);
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
