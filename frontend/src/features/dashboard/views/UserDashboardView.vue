<template>
  <div class="user-dashboard">
    <div class="user-header">
      <h1>داشبورد من</h1>
      <div class="user-info">
        <p>خوش آمدید، <strong>{{ username }}</strong></p>
        <p>نقش: {{ roleLabel }}</p>
      </div>
    </div>

    <section class="user-info-card">
      <h3>اطلاعات حساب</h3>
      <dl class="info-list">
        <dt>نام کاربری</dt>
        <dd>{{ username }}</dd>
        <dt>ایمیل</dt>
        <dd>{{ email || '—' }}</dd>
        <dt>نام</dt>
        <dd>{{ name || '—' }}</dd>
        <dt>تلفن</dt>
        <dd>{{ phone || '—' }}</dd>
        <dt>نقش</dt>
        <dd>{{ roleLabel }}</dd>
        <dt>وضعیت احراز هویت</dt>
        <dd>{{ isVerified ? 'تأیید شده' : 'در انتظار تأیید' }}</dd>
      </dl>
    </section>

    <section class="actions">
      <h3>دسترسی سریع</h3>
      <div class="action-buttons">
        <AppButton label="مشاهده پروفایل" variant="primary" @click="goToProfile" />
        <AppButton label="ثبت آگهی جدید" variant="secondary" @click="goToCreate" />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AppButton from '@/components/ui/AppButton.vue'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()

const username = computed(() => authStore.user?.username || '—')
const email = computed(() => authStore.user?.email || '')
const name = computed(() => authStore.user?.name || '')
const phone = computed(() => authStore.user?.phone || '')
const isVerified = computed(() => authStore.user?.is_verified || false)

const roleLabel = computed(() => {
  const role = authStore.user?.role
  if (role === 'investor') return t('auth.investor')
  if (role === 'admin') return 'مدیر'
  return t('auth.check_holder')
})

function goToProfile() {
  router.push('/app/profile')
}

function goToCreate() {
  router.push('/app/listings/create')
}
</script>

<style scoped>
.user-dashboard {
  min-height: 100vh;
}

.user-header {
  margin-bottom: 2rem;
}

.user-header h1 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0 0 0.5rem;
}

.user-info p {
  margin: 0;
  color: var(--text2);
}

.user-info-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.user-info-card h3 {
  margin: 0 0 1rem;
  font-size: var(--font-size-md);
  color: var(--text1);
}

.info-list {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.5rem 1.5rem;
  margin: 0;
}

  .info-list dt {
  color: var(--text2);
  font-size: var(--font-size-sm);
}

.info-list dd {
  margin: 0;
  color: var(--text1);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.actions h3 {
  margin: 0 0 1rem;
  font-size: var(--font-size-md);
  color: var(--text1);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
</style>
