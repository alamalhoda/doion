<template>
  <div class="review-box">
    <div class="review-title">
      خلاصه آگهی شما
    </div>
    <div class="review-grid">
      <div class="review-item">
        <div class="review-key">
          مبلغ اسمی
        </div>
        <div class="review-value">
          {{ formattedAmount }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          تاریخ سررسید
        </div>
        <div class="review-value">
          {{ formattedDueDate }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          بانک صادرکننده
        </div>
        <div class="review-value">
          {{ listing.bank_name }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          شماره صیاد
        </div>
        <div class="review-value review-value--mono">
          {{ listing.cheque_serial_number }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          نوع صادرکننده
        </div>
        <div class="review-value">
          {{ issuerTypeLabel }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          نام صادرکننده
        </div>
        <div class="review-value">
          {{ listing.issuer_name }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          سطح ریسک
        </div>
        <div class="review-value review-value--teal">
          {{ riskLabel }}
        </div>
      </div>
      <div class="review-item">
        <div class="review-key">
          نرخ تنزیل پیشنهادی
        </div>
        <div class="review-value review-value--teal">
          {{ formattedRate }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFormat } from '@/composables'
import type { ChequeListing } from '../types/listing'

const props = defineProps<{
  listing: ChequeListing
}>()

const { formatCurrency, formatPersianNumber } = useFormat()

const issuerTypeLabel = computed(() => {
  return props.listing.issuer_type === 'legal' ? 'حقوقی (شرکت)' : 'حقیقی (شخص)'
})

const riskLabel = computed(() => {
  switch (props.listing.risk_tier) {
    case 'low':
      return 'کم ریسک'
    case 'medium':
      return 'ریسک متوسط'
    case 'high':
      return 'ریسک بالا'
    default:
      return '-'
  }
})

const formattedAmount = computed(() => {
  return formatPersianNumber(formatCurrency(props.listing.face_amount))
})

const formattedDueDate = computed(() => {
  return formatPersianNumber(props.listing.due_date)
})

const formattedRate = computed(() => {
  if (props.listing.suggested_discount_rate == null) return '-'
  return formatPersianNumber(formatCurrency(Number(props.listing.suggested_discount_rate)))
})
</script>

<style scoped>
.review-box {
  background: var(--surface2);
  border-radius: var(--radius);
  padding: 1.25rem;
  margin-bottom: 1.25rem;
}

.review-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.review-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.review-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.review-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.review-value {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
}

.review-value--teal {
  color: var(--teal);
}

.review-value--mono {
  font-variant-numeric: tabular-nums;
}
</style>
