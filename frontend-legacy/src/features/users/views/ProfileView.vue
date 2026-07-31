<template>
  <div class="profile-view">
    <div class="profile-header">
      <h1>پروفایل کاربری</h1>
      <AppButton
        v-if="!isEditing"
        label="ویرایش"
        variant="primary"
        @click="startEditing"
      />
      <div
        v-else
        class="edit-actions"
      >
        <AppButton
          label="ذخیره"
          variant="success"
          :loading="isSaving"
          @click="saveProfile"
        />
        <AppButton
          label="انصراف"
          variant="secondary"
          @click="cancelEditing"
        />
      </div>
    </div>

    <div class="profile-card">
      <div class="profile-avatar">
        {{ userInitials }}
      </div>

      <div class="profile-info">
        <div class="info-group">
          <label>نام کاربری</label>
          <span class="info-value">{{ user?.username || '—' }}</span>
        </div>

        <div class="info-group">
          <label>ایمیل</label>
          <input
            v-if="isEditing"
            v-model="editForm.email"
            type="email"
            class="info-input"
          >
          <span
            v-else
            class="info-value"
          >{{ user?.email || '—' }}</span>
        </div>

        <div class="info-group">
          <label>نام کامل</label>
          <input
            v-if="isEditing"
            v-model="editForm.name"
            type="text"
            class="info-input"
          >
          <span
            v-else
            class="info-value"
          >{{ user?.name || '—' }}</span>
        </div>

        <div class="info-group">
          <label>تلفن</label>
          <input
            v-if="isEditing"
            v-model="editForm.phone"
            type="tel"
            class="info-input"
          >
          <span
            v-else
            class="info-value"
          >{{ user?.phone || '—' }}</span>
        </div>

        <div class="info-group">
          <label>نقش</label>
          <Badge :variant="roleVariant">
            {{ roleLabel }}
          </Badge>
        </div>

        <div class="info-group">
          <label>وضعیت احراز هویت</label>
          <Badge :variant="user?.is_verified ? 'success' : 'warning'">
            {{ user?.is_verified ? 'تأیید شده' : 'در انتظار تأیید' }}
          </Badge>
        </div>
      </div>
    </div>

    <div
      v-if="error"
      class="profile-error"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import AppButton from '@/components/ui/AppButton.vue'
import Badge from '@/components/ui/Badge.vue'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { apiClient } from '@/api/client'
import { normalizeApiError } from '@/api/errors'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

const isEditing = ref(false)
const isSaving = ref(false)
const error = ref<string | null>(null)

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  const name = user.value?.name || user.value?.username || ''
  return name.slice(0, 2).toUpperCase()
})

const roleLabel = computed(() => {
  const role = user.value?.role
  if (role === 'investor') return t('auth.investor')
  if (role === 'admin') return 'مدیر'
  if (role === 'moderator') return 'مدیر محتوا'
  return t('auth.check_holder')
})

const roleVariant = computed(() => {
  const role = user.value?.role
  if (role === 'investor') return 'warning'
  if (role === 'admin') return 'danger'
  return 'primary'
})

const editForm = reactive({
  email: '',
  name: '',
  phone: '',
})

onMounted(() => {
  if (user.value) {
    editForm.email = user.value.email || ''
    editForm.name = user.value.name || ''
    editForm.phone = user.value.phone || ''
  }
})

function startEditing() {
  if (user.value) {
    editForm.email = user.value.email || ''
    editForm.name = user.value.name || ''
    editForm.phone = user.value.phone || ''
  }
  isEditing.value = true
  error.value = null
}

function cancelEditing() {
  isEditing.value = false
  error.value = null
}

async function saveProfile() {
  isSaving.value = true
  error.value = null

  try {
    await apiClient.patch('/api/v1/identity/me/', {
      email: editForm.email,
      name: editForm.name,
      phone: editForm.phone,
    })

    const currentUser = await apiClient.get('/api/v1/identity/me/')
    authStore.user = currentUser.data

    isEditing.value = false
  } catch (err: unknown) {
    const normalized = normalizeApiError(err)
    error.value = normalized.message || 'خطا در ذخیره تغییرات'
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped>
.profile-view {
  max-width: 600px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.profile-header h1 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text1);
  margin: 0;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

  .profile-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--navy);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  margin: 0 auto 1.5rem;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.info-group label {
  font-size: var(--font-size-sm);
  color: var(--text2);
  font-weight: var(--font-weight-medium);
}

.info-value {
  font-size: var(--font-size-base);
  color: var(--text1);
}

.info-input {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
  font-size: var(--font-size-base);
  color: var(--text1);
  background: var(--surface);
  transition: border-color var(--transition-fast);
}

.info-input:focus {
  outline: none;
  border-color: var(--navy-light);
  box-shadow: 0 0 0 3px rgba(42, 95, 168, 0.08);
}

.profile-error {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: var(--red-light);
  border: 1px solid var(--red);
  border-radius: var(--radius-sm);
  color: var(--red);
  font-size: var(--font-size-sm);
}

.info-value {
  font-size: var(--font-size-base);
  color: var(--text1);
}

.info-input {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.5rem 0.75rem;
  font-size: var(--font-size-base);
  color: var(--text1);
  background: var(--surface);
  transition: border-color var(--transition-fast);
}

.info-input:focus {
  outline: none;
  border-color: var(--navy-light);
  box-shadow: 0 0 0 3px rgba(42, 95, 168, 0.08);
}

.profile-error {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: var(--red-light);
  border: 1px solid var(--red);
  border-radius: var(--radius-sm);
  color: var(--red);
  font-size: var(--font-size-sm);
}
</style>
