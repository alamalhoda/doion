<template>
  <div class="user-dashboard">
    <div class="user-header">
      <h1>داشبورد من</h1>
      <div class="user-info">
        <p>خوش آمدید، <strong>{{ username }}</strong></p>
        <p>نقش: {{ roleLabel }}</p>
      </div>
    </div>

    <NTabs
      v-model:value="activeTab"
      type="line"
      animated
      class="dashboard-tabs"
    >
      <NTabPane
        name="overview"
        :tab="$t('dashboard.overview')"
      >
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
            <AppButton
              label="مشاهده پروفایل"
              variant="primary"
              @click="goToProfile"
            />
            <AppButton
              v-if="isCheckHolder"
              label="ثبت آگهی جدید"
              variant="secondary"
              @click="goToCreate"
            />
          </div>
        </section>
      </NTabPane>

      <NTabPane
        v-if="isCheckHolder"
        name="matches_holder"
        :tab="$t('dashboard.matches_holder')"
      >
        <div class="stats-grid">
          <div class="stat-card stat-card--info">
            <span class="stat-value">{{ pendingIncomingCount }}</span>
            <span class="stat-label">{{ $t('matches.pending_incoming') }}</span>
          </div>
          <div class="stat-card stat-card--success">
            <span class="stat-value">{{ acceptedCount }}</span>
            <span class="stat-label">{{ $t('matches.accepted') }}</span>
          </div>
          <div class="stat-card stat-card--default">
            <span class="stat-value">{{ terminalCount }}</span>
            <span class="stat-label">{{ $t('matches.terminal') }}</span>
          </div>
        </div>
        <AppButton
          class="mt-4"
          label="مشاهده تطابق‌ها"
          variant="primary"
          @click="goToMatches"
        />
      </NTabPane>

      <NTabPane
        v-if="isInvestor"
        name="matches_investor"
        :tab="$t('dashboard.matches_investor')"
      >
        <div class="stats-grid">
          <div class="stat-card stat-card--info">
            <span class="stat-value">{{ pendingCreatedCount }}</span>
            <span class="stat-label">{{ $t('matches.pending_created') }}</span>
          </div>
          <div class="stat-card stat-card--success">
            <span class="stat-value">{{ acceptedInvestorCount }}</span>
            <span class="stat-label">{{ $t('matches.accepted') }}</span>
          </div>
          <div class="stat-card stat-card--default">
            <span class="stat-value">{{ terminalInvestorCount }}</span>
            <span class="stat-label">{{ $t('matches.terminal') }}</span>
          </div>
        </div>
        <AppButton
          class="mt-4"
          label="مشاهده تطابق‌ها"
          variant="primary"
          @click="goToMatches"
        />
      </NTabPane>
    </NTabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NTabs, NTabPane } from 'naive-ui'
import AppButton from '@/components/ui/AppButton.vue'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { useMatchStore } from '@/features/matches/stores/matchStore'
import { useI18n } from 'vue-i18n'
import { isCheckHolder, isInvestor } from '@/utils/permissions'

const router = useRouter()
const { t } = useI18n()
const authStore = useAuthStore()
const matchStore = useMatchStore()

const activeTab = ref('overview')

const username = computed(() => authStore.user?.username || '—')
const email = computed(() => authStore.user?.email || '')
const name = computed(() => authStore.user?.name || '')
const phone = computed(() => authStore.user?.phone || '')
const isVerified = computed(() => authStore.user?.is_verified || false)

const user = computed(() => authStore.user)
const isCheckHolderRole = computed(() => isCheckHolder(user.value))
const isInvestorRole = computed(() => isInvestor(user.value))

const roleLabel = computed(() => {
  const role = authStore.user?.role
  if (role === 'investor') return t('auth.investor')
  if (role === 'admin') return 'مدیر'
  return t('auth.check_holder')
})

const pendingIncomingCount = computed(() => matchStore.pendingMatches.length)
const acceptedCount = computed(() => matchStore.acceptedMatches.length)
const terminalCount = computed(() => matchStore.terminalMatches.length)

const pendingCreatedCount = computed(() => matchStore.pendingMatches.length)
const acceptedInvestorCount = computed(() => matchStore.acceptedMatches.length)
const terminalInvestorCount = computed(() => matchStore.terminalMatches.length)

onMounted(() => {
  matchStore.fetchMyMatches()
})

function goToProfile() {
  router.push('/app/profile')
}

function goToCreate() {
  router.push('/app/listings/create')
}

function goToMatches() {
  router.push('/app/matches')
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

.dashboard-tabs {
  margin-top: 1rem;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
}

.stat-card--info {
  border-top: 3px solid var(--info-color, #3b82f6);
}

.stat-card--success {
  border-top: 3px solid var(--success-color, #22c55e);
}

.stat-card--default {
  border-top: 3px solid var(--text3);
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--text1);
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--text2);
}

.mt-4 {
  margin-top: 1rem;
}

@media (max-width: 600px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
