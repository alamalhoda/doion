<template>
  <div
    class="listing-card"
    @click="goToDetail"
  >
    <div class="listing-card-icon">
      <svg
        viewBox="0 0 24 24"
        width="20"
        height="20"
        fill="var(--gold-light)"
      >
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 4h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S9 13.88 9 12.5 10.12 10 11.5 10c.57 0 1.08.19 1.5.5V7h4v0z" />
      </svg>
    </div>
    <div class="listing-card-info">
      <h4 class="listing-card-title">
        {{ listing.bank_name }} — {{ listing.issuer_name }}
      </h4>
      <p class="listing-card-meta">
        سررسید: {{ formattedDueDate }} · {{ daysRemaining }} روز دیگر
      </p>
    </div>
    <div class="listing-card-amount">
      {{ formattedAmount }}
      <small>ریال</small>
    </div>
    <StatusPill :variant="statusVariant">
      {{ statusLabel }}
    </StatusPill>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFormat } from '@/composables'
import StatusPill from '@/components/StatusPill.vue'
import type { ChequeListing } from '../types/listing'

const props = defineProps<{
  listing: ChequeListing
}>()

const router = useRouter()
const { formatCurrency, formatPersianNumber } = useFormat()

const statusVariant = computed(() => {
  switch (props.listing.status) {
    case 'published':
      return 'published'
    case 'pending_moderation':
      return 'pending_moderation'
    case 'matched':
      return 'matched'
    case 'rejected':
      return 'rejected'
    case 'expired':
      return 'reviewing'
    default:
      return 'published'
  }
})

const statusLabel = computed(() => {
  switch (props.listing.status) {
    case 'published':
      return 'منتشر شده'
    case 'pending_moderation':
      return 'در انتظار بررسی'
    case 'matched':
      return 'تطابق یافته'
    case 'rejected':
      return 'رد شده'
    case 'expired':
      return 'منقضی شده'
    case 'withdrawn':
      return 'برگشت داده شده'
    case 'settled_off_platform':
      return 'تسویه شده'
    default:
      return props.listing.status
  }
})

const formattedAmount = computed(() => {
  return formatPersianNumber(formatCurrency(props.listing.face_amount))
})

const formattedDueDate = computed(() => {
  return formatPersianNumber(props.listing.due_date)
})

const daysRemaining = computed(() => {
  const due = new Date(props.listing.due_date)
  const now = new Date()
  const diff = Math.ceil((due.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  return formatPersianNumber(String(Math.max(0, diff)))
})

function goToDetail() {
  router.push(`/app/listings/${props.listing.id}`)
}
</script>

<style scoped>
.listing-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 1rem;
  align-items: center;
  transition: border-color var(--transition-fast);
  cursor: pointer;
}

.listing-card:hover {
  border-color: var(--border2);
}

.listing-card-icon {
  width: 40px;
  height: 40px;
  background: var(--navy);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.listing-card-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
  margin: 0 0 0.2rem;
}

.listing-card-meta {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin: 0;
}

.listing-card-amount {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text1);
  text-align: left;
}

.listing-card-amount small {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}

@media (max-width: 768px) {
  .listing-card {
    grid-template-columns: 1fr auto;
  }

  .listing-card-icon {
    display: none;
  }

  .listing-card-amount {
    text-align: right;
  }
}
</style>
