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
      <div class="detail-card">
        <div class="detail-header">
          <h2 class="listing-title">
            {{ match.listing?.bank_name || $t('listings.untitled_listing') }}
          </h2>
          <NTag
            :type="statusTagType"
            size="medium"
          >
            {{ statusText }}
          </NTag>
        </div>

        <div class="detail-body">
          <div class="info-grid">
            <div class="info-item">
              <span class="label">{{ $t('listings.face_amount') }}</span>
              <span class="value">{{ formatCurrency(match.listing?.face_amount || 0) }}</span>
            </div>
            <div class="info-item">
              <span class="label">{{ $t('matches.discount_rate') }}</span>
              <span class="value">{{ match.final_discount_rate || match.listing?.suggested_discount_rate || '-' }}%</span>
            </div>
            <div class="info-item">
              <span class="label">{{ $t('matches.settlement_type') }}</span>
              <span class="value">{{ settlementTypeText }}</span>
            </div>
            <div class="info-item">
              <span class="label">{{ $t('matches.counterparty') }}</span>
              <span class="value">{{ counterpartyName }}</span>
            </div>
            <div class="info-item">
              <span class="label">{{ $t('common.created') }}</span>
              <span class="value">{{ formatDateTime(match.created_at) }}</span>
            </div>
          </div>

          <div
            v-if="match.message"
            class="message-box"
          >
            <span class="label">{{ $t('matches.last_message') }}</span>
            <p>{{ match.message }}</p>
          </div>

          <div
            v-if="match.terms"
            class="message-box"
          >
            <span class="label">{{ $t('matches.terms') }}</span>
            <p>{{ match.terms }}</p>
          </div>
        </div>

        <div class="detail-actions">
          <template v-if="isInvestorRole && match.status === 'pending'">
            <NButton
              type="error"
              @click="handleCancel"
            >
              {{ $t('matches.cancel_match') }}
            </NButton>
          </template>

          <template v-if="isCheckHolderRole && match.status === 'pending'">
            <NButton
              type="success"
              @click="handleAccept"
            >
              {{ $t('matches.accept_match') }}
            </NButton>
            <NButton
              type="error"
              @click="handleDecline"
            >
              {{ $t('matches.decline_match') }}
            </NButton>
          </template>

          <template v-if="isCheckHolderRole && match.status === 'accepted'">
            <NButton
              type="success"
              @click="handleConfirmOffPlatform"
            >
              {{ $t('matches.confirm_settlement') }}
            </NButton>
          </template>

          <template v-if="isTerminal">
            <NTag type="default">
              {{ $t('matches.terminal_state') }}
            </NTag>
          </template>
        </div>
      </div>
    </div>

    <div
      v-else
      class="empty-state"
    >
      {{ $t('matches.not_found') }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NTag, NButton, useNotification } from 'naive-ui'
import { useI18n } from 'vue-i18n'
import { useMatchStore } from '../stores/matchStore'
import { useAuthStore } from '@/features/auth/stores/authStore'
import { isInvestor, isCheckHolder } from '@/utils/permissions'
import type { Match } from '../types/match'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()
const notification = useNotification()
const matchStore = useMatchStore()
const authStore = useAuthStore()

const matchId = computed(() => route.params.id as string)
const match = computed(() => matchStore.currentMatch)
const isLoading = computed(() => matchStore.isLoading)
const error = computed(() => matchStore.error)

const user = computed(() => authStore.user)

const isInvestorRole = computed(() => isInvestor(user.value))
const isCheckHolderRole = computed(() => isCheckHolder(user.value))

const isTerminal = computed(() => {
  if (!match.value) return false
  return ['declined', 'cancelled', 'settled', 'off_platform_confirmed'].includes(match.value.status)
})

const statusTagType = computed(() => {
  const map: Record<string, 'info' | 'success' | 'warning' | 'error' | 'default'> = {
    pending: 'info',
    accepted: 'warning',
    declined: 'error',
    cancelled: 'error',
    off_platform_confirmed: 'success',
    settled: 'success',
  }
  return map[match.value?.status || ''] || 'default'
})

const statusText = computed(() => {
  const map: Record<string, string> = {
    pending: t('matches.status_pending'),
    accepted: t('matches.status_accepted'),
    declined: t('matches.status_declined'),
    cancelled: t('matches.status_cancelled'),
    off_platform_confirmed: t('matches.status_off_platform_confirmed'),
    settled: t('matches.status_settled'),
  }
  return map[match.value?.status || ''] || match.value?.status || ''
})

const counterpartyName = computed(() => {
  if (!match.value) return ''
  // For investor, show check_holder; for check_holder, show investor
  return isInvestorRole.value
    ? match.value.check_holder?.full_name || t('common.unknown')
    : match.value.investor?.full_name || t('common.unknown')
})

const settlementTypeText = computed(() => {
  const map: Record<string, string> = {
    off_platform: t('matches.off_platform'),
    escrow: t('matches.escrow'),
    principal_ledger: t('matches.principal_ledger'),
  }
  return map[match.value?.settlement_type || ''] || match.value?.settlement_type || ''
})

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('fa-IR', {
    style: 'currency',
    currency: 'IRR',
    minimumFractionDigits: 0,
  }).format(amount)
}

function formatDateTime(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('fa-IR')
}

async function loadMatch() {
  try {
    await matchStore.fetchMatch(matchId.value)
  } catch {
    notification.error({
      title: t('common.error'),
      description: error.value || t('common.unknown_error'),
    })
  }
}

async function handleAccept() {
  try {
    await matchStore.acceptMatch(matchId.value)
    notification.success({
      title: t('common.success'),
      description: t('matches.accepted_successfully'),
    })
  } catch {
    notification.error({
      title: t('common.error'),
      description: matchStore.error || t('common.unknown_error'),
    })
  }
}

async function handleDecline() {
  try {
    await matchStore.declineMatch(matchId.value)
    notification.success({
      title: t('common.success'),
      description: t('matches.declined_successfully'),
    })
  } catch {
    notification.error({
      title: t('common.error'),
      description: matchStore.error || t('common.unknown_error'),
    })
  }
}

async function handleCancel() {
  try {
    await matchStore.cancelMatch(matchId.value)
    notification.success({
      title: t('common.success'),
      description: t('matches.cancelled_successfully'),
    })
  } catch {
    notification.error({
      title: t('common.error'),
      description: matchStore.error || t('common.unknown_error'),
    })
  }
}

async function handleConfirmOffPlatform() {
  try {
    await matchStore.confirmOffPlatform(matchId.value)
    notification.success({
      title: t('common.success'),
      description: t('matches.confirmed_successfully'),
    })
  } catch {
    notification.error({
      title: t('common.error'),
      description: matchStore.error || t('common.unknown_error'),
    })
  }
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
}

.loading-state,
.error-state,
.empty-state {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}

.detail-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg);
  background: var(--navy);
}

.listing-title {
  color: #fff;
  font-size: var(--font-size-lg);
  margin: 0;
}

.detail-body {
  padding: var(--spacing-lg);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin-bottom: var(--spacing-xs);
}

.value {
  font-size: var(--font-size-base);
  color: var(--text1);
  font-weight: 500;
}

.message-box {
  padding: var(--spacing-md);
  background: var(--surface2);
  border-radius: var(--radius-sm);
  margin-top: var(--spacing-md);
}

.message-box p {
  margin: var(--spacing-xs) 0 0;
  color: var(--text2);
}

.detail-actions {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border);
  background: var(--surface2);
}

@media (max-width: 600px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
