<template>
  <Modal
    v-model="isOpen"
    :title="title"
    max-width="640px"
  >
    <div
      v-if="listing"
      class="detail-modal"
    >
      <div class="detail-header">
        <div class="detail-issuer">
          <span class="detail-issuer-dot" />
          {{ issuerName }}
        </div>
        <RiskBadge :risk="riskTier" />
      </div>

      <div class="detail-amount">
        <span>ریال</span>{{ formattedAmount }}
      </div>

      <div class="detail-meta">
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            بانک
          </div>
          <div class="detail-meta-val">
            {{ listing.bank_name }}
          </div>
        </div>
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            سررسید
          </div>
          <div class="detail-meta-val">
            {{ formattedDueDate }}
          </div>
        </div>
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            روز تا سررسید
          </div>
          <div class="detail-meta-val">
            {{ listing.days_to_due ?? '-' }} روز
          </div>
        </div>
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            نوع صادرکننده
          </div>
          <div class="detail-meta-val">
            {{ issuerTypeLabel }}
          </div>
        </div>
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            نرخ تنزیل پیشنهادی
          </div>
          <div class="detail-meta-val">
            {{ formattedRate }}
          </div>
        </div>
        <div class="detail-meta-item">
          <div class="detail-meta-key">
            وضعیت انتشار
          </div>
          <div class="detail-meta-val">
            {{ formattedPublishedAt }}
          </div>
        </div>
      </div>

      <div
        v-if="listing.description"
        class="detail-description"
      >
        {{ listing.description }}
      </div>

      <div class="detail-footer">
        <button
          class="btn btn--primary"
          :disabled="isSubmitting"
          @click="handleInterest"
        >
          {{ isSubmitting ? 'در حال ثبت...' : 'ابراز تمایل' }}
        </button>
      </div>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import 'dayjs/locale/fa'
import Modal from '@/components/Modal.vue'
import RiskBadge from '@/components/RiskBadge.vue'
import { useFormat } from '@/composables'
import { useToast } from '@/composables'
import { useMatchStore } from '@/features/matches/stores/matchStore'
import { useAuthStore } from '@/features/auth/stores/authStore'
import type { ChequeListing } from '@/features/listings/types/listing'

const props = defineProps<{
  modelValue: boolean
  listing: ChequeListing | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const { formatCurrency, formatNumber } = useFormat()
const { showToast } = useToast()
const matchStore = useMatchStore()
const authStore = useAuthStore()
const router = useRouter()

const isOpen = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const title = computed(() => 'جزئیات آگهی')

const issuerName = computed(() => {
  if (!props.listing) return '-'
  return props.listing.issuer_profile?.name || props.listing.issuer_name || '-'
})

const riskTier = computed(() => {
  if (!props.listing?.risk_tier) return 'low'
  const map: Record<string, 'low' | 'mid' | 'high'> = { low: 'low', medium: 'mid', high: 'high' }
  return map[props.listing.risk_tier] || 'low'
})

const formattedAmount = computed(() => {
  if (!props.listing) return '-'
  return formatCurrency(props.listing.face_amount)
})

const formattedDueDate = computed(() => {
  if (!props.listing) return '-'
  return dayjs(props.listing.due_date).locale('fa').format('YYYY/MM/DD')
})

const issuerTypeLabel = computed(() => {
  if (!props.listing) return '-'
  return props.listing.issuer_type === 'legal' ? 'حقوقی' : 'حقیقی'
})

const formattedRate = computed(() => {
  if (!props.listing?.suggested_discount_rate) return '-'
  return `${formatNumber(props.listing.suggested_discount_rate)}٪`
})

const formattedPublishedAt = computed(() => {
  if (!props.listing) return '-'
  const val = props.listing.published_at || props.listing.updated_at || props.listing.created_at
  return dayjs(val).locale('fa').format('YYYY/MM/DD HH:mm')
})

const isSubmitting = ref(false)

async function handleInterest() {
  if (!props.listing) return

  if (authStore.user?.role !== 'investor') {
    showToast('فقط سرمایه‌گذاران می‌توانند ابراز تمایل کنند.', 'error')
    return
  }

  if (!authStore.user?.is_verified) {
    showToast('برای ابراز تمایل، ابتدا احراز هویت خود را تکمیل کنید.', 'warning')
    router.push('/app/verification/kyc')
    return
  }

  isSubmitting.value = true
  try {
    await matchStore.createMatch({ listing_id: String(props.listing.id), message: '' })
    showToast('ابراز تمایل شما ثبت شد.', 'success')
    isOpen.value = false
    router.push('/app/matches')
  } catch (err: unknown) {
    const message = (err as { message?: string }).message || 'خطایی رخ داده است.'
    showToast(message, 'error')
  } finally {
    isSubmitting.value = false
  }
}

</script>

<style>
.detail-modal {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.detail-issuer {
  color: var(--text2);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.detail-issuer-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--gold-light);
}

.detail-amount {
  font-size: 2rem;
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  font-variant-numeric: tabular-nums;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.6rem 1rem;
  display: inline-block;
  background: var(--surface2);
}

.detail-amount span {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-normal);
  color: var(--text3);
  margin-left: 0.4rem;
}

.detail-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.detail-meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.detail-meta-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.detail-meta-val {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
}

.detail-description {
  font-size: var(--font-size-base);
  color: var(--text2);
  line-height: 1.6;
  background: var(--surface2);
  border-radius: var(--radius-sm);
  padding: 0.75rem 1rem;
}

.detail-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
