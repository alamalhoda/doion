<template>
  <div class="match-card" @click="handleClick">
    <div class="card-header">
      <h3 class="listing-title">{{ match.listing?.title || $t('listings.untitled_listing') }}</h3>
      <NTag :type="statusTagType" size="small">
        {{ statusText }}
      </NTag>
    </div>

    <div class="card-body">
      <div class="info-grid">
        <div class="info-item">
          <span class="label">{{ $t('listings.face_amount') }}</span>
          <span class="value">{{ formatCurrency(match.listing?.face_amount || 0) }}</span>
        </div>
        <div class="info-item">
          <span class="label">{{ $t('matches.discount_rate') }}</span>
          <span class="value">{{ match.final_discount_rate || match.proposed_discount_rate || '-' }}%</span>
        </div>
        <div class="info-item">
          <span class="label">{{ $t('matches.counterparty') }}</span>
          <span class="value">{{ counterpartyName }}</span>
        </div>
        <div class="info-item">
          <span class="label">{{ $t('matches.settlement_type') }}</span>
          <span class="value">{{ settlementTypeText }}</span>
        </div>
      </div>

      <div v-if="match.message" class="message-preview">
        <span class="label">{{ $t('matches.last_message') }}</span>
        <p class="message-text">{{ truncateMessage(match.message) }}</p>
      </div>
    </div>

    <div class="card-footer">
      <span class="created-at">{{ $t('common.created') }}: {{ formatDateTime(match.created_at) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { NTag } from 'naive-ui'
import type { Match } from '../types/match'

interface Props {
  match: Match
}

defineProps<Props>()
const emit = defineEmits<{
  click: []
}>()

const { t } = useI18n()

const statusTagType = computed(() => {
  const statusMap: Record<string, 'info' | 'success' | 'warning' | 'error'> = {
    pending: 'info',
    accepted: 'warning',
    rejected: 'error',
    settled_off_platform: 'success',
  }
  return statusMap[match.status] || 'default'
})

const statusText = computed(() => {
  const statusMap: Record<string, string> = {
    pending: t('matches.status_pending'),
    accepted: t('matches.status_accepted'),
    rejected: t('matches.status_rejected'),
    settled_off_platform: t('matches.status_settled'),
  }
  return statusMap[match.status] || match.status
})

const counterpartyName = computed(() => {
  // For check holders, show investor; for investors, show check holder
  return match.investor?.full_name || match.check_holder?.full_name || t('common.unknown')
})

const settlementTypeText = computed(() => {
  const map: Record<string, string> = {
    off_platform: t('matches.off_platform'),
    escrow: t('matches.escrow'),
    principal_ledger: t('matches.principal_ledger'),
  }
  return map[match.settlement_type] || match.settlement_type
})

function handleClick(): void {
  emit('click')
}

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

function truncateMessage(message: string): string {
  return message.length > 80 ? message.substring(0, 80) + '...' : message
}
</script>

<style scoped>
.match-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  cursor: pointer;
  transition: all 0.2s;
}

.match-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.listing-title {
  font-size: var(--font-size-md);
  color: var(--color-text-primary);
  margin: 0;
  flex: 1;
}

.card-body {
  margin-bottom: var(--spacing-md);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.value {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
}

.message-preview {
  padding: var(--spacing-sm);
  background: var(--color-bg-primary);
  border-radius: var(--radius-sm);
}

.message-text {
  margin: var(--spacing-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.card-footer {
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}

.created-at {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
}
</style>