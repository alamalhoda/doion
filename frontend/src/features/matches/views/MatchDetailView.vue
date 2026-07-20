<template>
  <div class="match-detail-view">
    <div class="view-header">
      <h1>{{ $t('matches.detail_title') }}</h1>
    </div>

    <div
      v-if="isLoading"
      class="loading-state"
    >
      {{ $t('common.loading') }}
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
      <button
        class="btn btn--secondary btn--sm"
        @click="loadMatch"
      >
        {{ $t('common.retry') }}
      </button>
    </div>

    <div
      v-else-if="match"
      class="match-detail"
    >
      <div class="detail-section">
        <h3>{{ $t('matches.listing_info_label') }}</h3>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">بانک</span>
            <span class="detail-value">{{ match.listing?.bank_name || '-' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">{{ $t('listings.face_amount') }}</span>
            <span class="detail-value">{{ formatCurrency(match.listing?.face_amount || 0) }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">سررسید</span>
            <span class="detail-value">{{ formattedDueDate }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">وضعیت</span>
            <span class="detail-value">{{ statusText }}</span>
          </div>
        </div>
      </div>

      <div class="detail-section">
        <h3>{{ $t('matches.detail_title') }}</h3>
        <div class="detail-grid">
          <div class="detail-item">
            <span class="detail-label">{{ $t('matches.settlement_type') }}</span>
            <span class="detail-value">{{ settlementTypeText }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">{{ $t('matches.counterparty') }}</span>
            <span class="detail-value">{{ counterpartyName }}</span>
          </div>
          <div
            v-if="match.message"
            class="detail-item"
          >
            <span class="detail-label">{{ $t('matches.message_label') }}</span>
            <span class="detail-value">{{ match.message }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">{{ $t('common.created') }}</span>
            <span class="detail-value">{{ formattedCreatedAt }}</span>
          </div>
        </div>
      </div>

      <div class="detail-actions">
        <button
          v-if="canAccept"
          class="btn btn--primary"
          :disabled="actionLoading === 'accept'"
          @click="updateStatus('accepted')"
        >
          {{ actionLoading === 'accept' ? 'در حال ثبت...' : $t('matches.actions_accept') }}
        </button>
        <button
          v-if="canDecline"
          class="btn btn--secondary"
          :disabled="actionLoading === 'decline'"
          @click="updateStatus('declined')"
        >
          {{ actionLoading === 'decline' ? 'در حال ثبت...' : $t('matches.actions_decline') }}
        </button>
        <button
          v-if="canConfirm"
          class="btn btn--primary"
          :disabled="actionLoading === 'confirm'"
          @click="updateStatus('off_platform_confirmed')"
        >
          {{ actionLoading === 'confirm' ? 'در حال ثبت...' : $t('matches.actions_confirm') }}
        </button>
        <button
          v-if="canCancel"
          class="btn btn--secondary"
          :disabled="actionLoading === 'cancel'"
          @click="updateStatus('cancelled')"
        >
          {{ actionLoading === 'cancel' ? 'در حال ثبت...' : $t('matches.actions_cancel') }}
        </button>
      </div>
    </div>

    <div
      v-else
      class="empty-state"
    >
      تطابقی یافت نشد.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import dayjs from 'dayjs'
import 'dayjs/locale/fa'
import { useMatchStore } from '../stores/matchStore'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { useToast } from '@/composables'
import { useFormat } from '@/composables'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const matchStore = useMatchStore()
const authStore = useAuthStore()
const { showToast } = useToast()
const { formatCurrency } = useFormat()
const { t } = useI18n()

const isLoading = ref(false)
const error = ref<string | null>(null)
const actionLoading = ref<string | null>(null)

const match = computed(() => matchStore.currentMatch)

const currentUserId = computed(() => authStore.user?.id)
const isHolder = computed(() => currentUserId.value === match.value?.check_holder?.id)
const isInvestor = computed(() => currentUserId.value === match.value?.investor?.id)

const canAccept = computed(() => isHolder.value && match.value?.status === 'pending')
const canDecline = computed(() => isHolder.value && match.value?.status === 'pending')
const canConfirm = computed(() => isHolder.value && match.value?.status === 'accepted')
const canCancel = computed(() => isInvestor.value && (match.value?.status === 'pending' || match.value?.status === 'accepted'))

const statusText = computed(() => {
  const map: Record<string, string> = {
    pending: t('matches.status_pending'),
    accepted: t('matches.status_accepted'),
    declined: t('matches.status_declined'),
    cancelled: t('matches.status_cancelled'),
    off_platform_confirmed: t('matches.status_off_platform_confirmed'),
    settled: t('matches.status_settled'),
  }
  return map[match.value?.status || ''] || match.value?.status || '-'
})

const settlementTypeText = computed(() => {
  const map: Record<string, string> = {
    off_platform: t('matches.off_platform'),
    escrow: t('matches.escrow'),
    principal_ledger: t('matches.principal_ledger'),
  }
  return map[match.value?.settlement_type || ''] || match.value?.settlement_type || '-'
})

const counterpartyName = computed(() => {
  return match.value?.investor?.name || match.value?.check_holder?.name || t('common.unknown')
})

const formattedDueDate = computed(() => {
  if (!match.value?.listing?.due_date) return '-'
  return dayjs(match.value.listing.due_date).locale('fa').format('YYYY/MM/DD')
})

const formattedCreatedAt = computed(() => {
  if (!match.value?.created_at) return '-'
  return dayjs(match.value.created_at).locale('fa').format('YYYY/MM/DD HH:mm')
})

async function loadMatch() {
  isLoading.value = true
  error.value = null
  try {
    await matchStore.fetchMatch(route.params.id as string)
  } catch (err: unknown) {
    error.value = (err as { message?: string }).message || 'خطایی رخ داده است.'
  } finally {
    isLoading.value = false
  }
}

async function updateStatus(status: string) {
  if (!match.value) return
  actionLoading.value = status
  try {
    await matchStore.updateMatchStatus(match.value.id, { status: status as any })
    showToast(getSuccessToast(status), 'success')
    await matchStore.fetchMatch(match.value.id)
  } catch (err: unknown) {
    showToast((err as { message?: string }).message || 'خطایی رخ داده است.', 'error')
  } finally {
    actionLoading.value = null
  }
}

function getSuccessToast(status: string): string {
  const map: Record<string, string> = {
    accepted: 'درخواست تطابق پذیرفته شد.',
    declined: 'درخواست تطابق رد شد.',
    off_platform_confirmed: 'تسویه خارج از پلتفرم تأیید شد.',
    cancelled: 'درخواست تطابق لغو شد.',
  }
  return map[status] || 'عملیات با موفقیت انجام شد.'
}

onMounted(() => {
  loadMatch()
})
</script>

<style scoped>
.match-detail-view {
  max-width: 800px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--spacing-xl);
}

.view-header h1 {
  color: var(--text1);
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-sm);
}

.loading-state,
.error-state {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text3);
}

.match-detail {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-section {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
}

.detail-section h3 {
  color: var(--navy);
  font-size: var(--font-size-md);
  margin: 0 0 1rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.detail-label {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.detail-value {
  font-size: var(--font-size-base);
  color: var(--text2);
  font-weight: var(--font-weight-medium);
}

.detail-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
