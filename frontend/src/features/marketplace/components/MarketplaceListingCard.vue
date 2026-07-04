<template>
  <div
    class="listing-card"
    :class="{ 'listing-card--hoverable': hoverable }"
    @click="onClick"
  >
    <div class="card-header">
      <div class="card-issuer">
        <span class="card-issuer-dot" />
        {{ issuerName }}
      </div>
      <RiskBadge :risk="riskTier" />
    </div>
    <div class="card-body">
      <div class="card-amount">
        <span>ریال</span>{{ formattedAmount }}
      </div>
      <div class="card-meta">
        <div class="meta-item">
          <div class="meta-key">
            بانک
          </div>
          <div class="meta-val">
            {{ listing.bank_name }}
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            سررسید
          </div>
          <div class="meta-val">
            {{ formattedDueDate }}
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            روز تا سررسید
          </div>
          <div class="meta-val">
            {{ listing.days_to_due ?? '-' }} روز
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            نوع صادرکننده
          </div>
          <div class="meta-val">
            {{ issuerTypeLabel }}
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <div>
        <div class="discount-rate">
          {{ formattedRate }}
        </div>
        <div class="discount-label">
          نرخ تنزیل پیشنهادی
        </div>
      </div>
      <button
        v-if="hoverable"
        class="btn btn--sm btn--primary"
        @click.stop="onInterest"
      >
        ابراز تمایل
      </button>
      <button
        v-else
        class="btn btn--sm btn--gold"
        disabled
      >
        مشاهده
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDialog, useNotification } from 'naive-ui'
import { useRouter } from 'vue-router'
import RiskBadge from '@/components/RiskBadge.vue'
import type { ChequeListing } from '@/features/listings/types/listing'
import { useFormat } from '@/composables'
import { useMatchStore } from '@/features/matches/stores/matchStore'

const props = withDefaults(
  defineProps<{
    listing: ChequeListing
    hoverable?: boolean
  }>(),
  {
    hoverable: true,
  }
)

const emit = defineEmits<{
  (e: 'click'): void
}>()

const router = useRouter()
const matchStore = useMatchStore()
const dialog = useDialog()
const notification = useNotification()
const { formatCurrency, formatNumber } = useFormat()

const issuerName = computed(() => {
  return props.listing.issuer_profile?.name || props.listing.issuer_name || '-'
})

const riskTier = computed(() => {
  if (!props.listing.risk_tier) return 'low'
  const map: Record<string, 'low' | 'mid' | 'high'> = { low: 'low', medium: 'mid', high: 'high' }
  return map[props.listing.risk_tier] || 'low'
})

const formattedAmount = computed(() => formatCurrency(props.listing.face_amount))

const formattedDueDate = computed(() => props.listing.due_date)

const issuerTypeLabel = computed(() => {
  return props.listing.issuer_type === 'legal' ? 'حقوقی' : 'حقیقی'
})

const formattedRate = computed(() => {
  if (!props.listing.suggested_discount_rate) return '-'
  return `${formatNumber(props.listing.suggested_discount_rate)}٪`
})

function onClick() {
  emit('click')
}

async function onInterest() {
  const confirmed = await showConfirmation()
  if (confirmed) {
    try {
      await matchStore.createMatch({ listing_id: props.listing.id, message: '' })
      notification.success({
        title: 'درخواست تطبیق ثبت شد',
        content: 'درخواست شما با موفقیت ثبت شد. منتظر تایید صاحب چک باشید.',
        duration: 3000,
      })
      router.push('/app/matches')
    } catch (error) {
      notification.error({
        title: 'خطا در ثبت درخواست',
        content: extractErrorMessage(error),
        duration: 3000,
      })
    }
  }
}

function showConfirmation(): Promise<boolean> {
  return new Promise((resolve) => {
    dialog.warning({
      title: 'تایید درخواست تطبیق',
      content: 'آیا مایلید درخواست تطبیق برای این آگهی چک را ثبت کنید؟',
      positiveText: 'تایید',
      negativeText: 'انصراف',
      onPositiveClick: () => resolve(true),
      onNegativeClick: () => resolve(false),
    })
  })
}

function extractErrorMessage(err: unknown): string {
  const anyErr = err as { response?: { data?: { error?: { message?: string } } } }
  return anyErr?.response?.data?.error?.message || (err as Error)?.message || 'خطایی رخ داد'
}
</script>

<style>
.listing-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s;
}

.listing-card--hoverable:hover {
  border-color: var(--navy-light);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.card-header {
  background: var(--navy);
  padding: 0.85rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: repeating-linear-gradient(
    90deg,
    rgba(201, 150, 10, 0.4) 0,
    rgba(201, 150, 10, 0.4) 12px,
    transparent 12px,
    transparent 18px
  );
}

.card-issuer {
  color: rgba(255, 255, 255, 0.85);
  font-size: var(--font-size-xs);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.card-issuer-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--gold-light);
}

.card-body {
  padding: 1.1rem;
}

.card-amount {
  font-size: 1.65rem;
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  font-variant-numeric: tabular-nums;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.4rem 0.75rem;
  display: inline-block;
  margin-bottom: 0.85rem;
  background: var(--surface2);
}

.card-amount span {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-normal);
  color: var(--text3);
  margin-left: 0.3rem;
}

.card-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem 0.5rem;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.meta-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.meta-val {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
}

.card-footer {
  border-top: 1px solid var(--border);
  padding: 0.75rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.discount-rate {
  font-size: 1.15rem;
  font-weight: var(--font-weight-bold);
  color: var(--teal);
}

.discount-label {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}
</style>
