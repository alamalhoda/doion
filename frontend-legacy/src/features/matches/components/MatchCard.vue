<template>
  <div
    class="match-card"
    @click="handleClick"
  >
    <div class="card-header">
      <h3 class="listing-title">
        {{ displayTitle }}
      </h3>
      <NTag
        :type="statusTagType"
        size="small"
      >
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
          <span class="value">{{ match.final_discount_rate ? formatNumber(match.final_discount_rate) : '-' }}٪</span>
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

      <div
        v-if="match.message"
        class="message-preview"
      >
        <span class="label">{{ $t('matches.last_message') }}</span>
        <p class="message-text">
          {{ truncateMessage(match.message) }}
        </p>
      </div>
    </div>

    <div class="card-footer">
      <span class="created-at">{{ $t('common.created') }}: {{ formatDateTime(match.created_at) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import dayjs from 'dayjs'
import 'dayjs/locale/fa'
import { useI18n } from 'vue-i18n'
import { NTag } from 'naive-ui'
import { useFormat } from '@/composables'
import type { Match } from '../types/match'

interface Props {
  match: Match
}

const props = defineProps<Props>()
const emit = defineEmits<{
  click: []
}>()

const { t } = useI18n()
const { formatCurrency, formatNumber } = useFormat()

const displayTitle = computed(() => {
  if (!props.match.listing) return t('listings.untitled_listing')
  return `${props.match.listing.bank_name} — ${formatCurrency(props.match.listing.face_amount)}`
})

const statusTagType = computed(() => {
  const statusMap: Record<string, 'info' | 'success' | 'warning' | 'error' | 'default'> = {
    pending: 'info',
    accepted: 'warning',
    declined: 'error',
    cancelled: 'default',
    off_platform_confirmed: 'success',
    settled: 'success',
  }
  return statusMap[props.match.status] || 'default'
})

const statusText = computed(() => {
  const statusMap: Record<string, string> = {
    pending: t('matches.status_pending'),
    accepted: t('matches.status_accepted'),
    declined: t('matches.status_declined'),
    cancelled: t('matches.status_cancelled'),
    off_platform_confirmed: t('matches.status_off_platform_confirmed'),
    settled: t('matches.status_settled'),
  }
  return statusMap[props.match.status] || props.match.status
})

const counterpartyName = computed(() => {
  return props.match.investor?.name || props.match.check_holder?.name || t('common.unknown')
})

const settlementTypeText = computed(() => {
  const map: Record<string, string> = {
    off_platform: t('matches.off_platform'),
    escrow: t('matches.escrow'),
    principal_ledger: t('matches.principal_ledger'),
  }
  return map[props.match.settlement_type] || props.match.settlement_type
})

function handleClick(): void {
  emit('click')
}

function formatDateTime(dateStr: string): string {
  return dayjs(dateStr).locale('fa').format('YYYY/MM/DD')
}

function truncateMessage(message: string): string {
  return message.length > 80 ? message.substring(0, 80) + '...' : message
}
</script>

<style scoped>
.match-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  cursor: pointer;
  transition: all 0.2s;
}

.match-card:hover {
  box-shadow: var(--shadow);
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
  color: var(--text1);
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
  color: var(--text2);
  margin-bottom: var(--spacing-xs);
}

.value {
  font-size: var(--font-size-sm);
  color: var(--text1);
  font-weight: 500;
}

.message-preview {
  padding: var(--spacing-sm);
  background: var(--surface2);
  border-radius: var(--radius-sm);
}

.message-text {
  margin: var(--spacing-xs) 0 0;
  font-size: var(--font-size-sm);
  color: var(--text2);
}

.card-footer {
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border);
}

.created-at {
  font-size: var(--font-size-xs);
  color: var(--text3);
}
</style>