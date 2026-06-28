<template>
  <div class="listing-detail">
    <button
      class="back-btn"
      @click="goBack"
    >
      <svg
        viewBox="0 0 24 24"
        width="20"
        height="20"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M15 18l-6-6 6-6" />
      </svg>
      بازگشت
    </button>

    <div
      v-if="isLoading"
      class="loading-state"
    >
      در حال بارگذاری...
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
      <button
        class="btn btn--secondary btn--sm"
        @click="fetchListing"
      >
        تلاش مجدد
      </button>
    </div>

    <div
      v-else-if="listing"
      class="detail-content"
    >
      <div class="detail-header">
        <div class="detail-header-info">
          <h1 class="detail-title">
            {{ listing.bank_name }} — {{ listing.issuer_name }}
          </h1>
          <p class="detail-subtitle">
            نوع صادرکننده: {{ issuerTypeLabel }}
          </p>
        </div>
        <StatusPill :variant="statusVariant">
          {{ statusLabel }}
        </StatusPill>
      </div>

      <div class="amount-box">
        <div>
          <div class="amount-box-label">
            مبلغ اسمی چک
          </div>
          <div class="amount-box-value">
            <small>ریال</small> {{ formattedAmount }}
          </div>
        </div>
      </div>

      <div class="detail-section">
        <div class="detail-section-title">
          اطلاعات چک
        </div>
        <div class="detail-grid">
          <div class="detail-field">
            <div class="detail-field-key">
              بانک صادرکننده
            </div>
            <div class="detail-field-val">
              {{ listing.bank_name }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              تاریخ سررسید
            </div>
            <div class="detail-field-val">
              {{ formattedDueDate }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              روز تا سررسید
            </div>
            <div class="detail-field-val">
              {{ daysRemaining }} روز
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              نوع صادرکننده
            </div>
            <div class="detail-field-val">
              {{ issuerTypeLabel }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              نرخ تنزیل پیشنهادی
            </div>
            <div class="detail-field-val detail-field-val--teal">
              {{ formattedRate }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              شماره صیاد
            </div>
            <div class="detail-field-val">
              {{ listing.cheque_serial_number }}
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="listing.description"
        class="detail-section"
      >
        <div class="detail-section-title">
          توضیحات
        </div>
        <p class="detail-description">
          {{ listing.description }}
        </p>
      </div>

      <div class="detail-actions">
        <button
          v-if="listing.status === 'rejected'"
          class="btn btn--secondary btn--lg"
          @click="handleResubmit"
        >
          اصلاح و ارسال مجدد ({{ resubmitRemaining }} بار باقی‌مانده)
        </button>
        <button
          v-else-if="listing.status === 'published'"
          class="btn btn--gold btn--lg"
          @click="expressInterest"
        >
          ابراز تمایل به خرید
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useListingStore } from '../stores/listingStore'
import { useFormat } from '@/composables'
import { useToast } from '@/composables'
import StatusPill from '@/components/StatusPill.vue'

const route = useRoute()
const router = useRouter()
const store = useListingStore()
const { formatCurrency, formatPersianNumber } = useFormat()
const { showToast } = useToast()

const isLoading = computed(() => store.isLoading)
const error = computed(() => store.error)
const listing = computed(() => store.currentListing)

const issuerTypeLabel = computed(() => {
  return listing.value?.issuer_type === 'legal' ? 'حقوقی (شرکت)' : 'حقیقی (شخص)'
})

const statusVariant = computed(() => {
  if (!listing.value) return 'published'
  switch (listing.value.status) {
    case 'published':
      return 'published'
    case 'pending_moderation':
      return 'pending_moderation'
    case 'matched':
      return 'matched'
    case 'rejected':
      return 'rejected'
    default:
      return 'published'
  }
})

const statusLabel = computed(() => {
  if (!listing.value) return ''
  switch (listing.value.status) {
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
      return listing.value.status
  }
})

const formattedAmount = computed(() => {
  if (!listing.value) return '-'
  return formatPersianNumber(formatCurrency(listing.value.face_amount))
})

const formattedDueDate = computed(() => {
  if (!listing.value) return '-'
  return formatPersianNumber(listing.value.due_date)
})

const daysRemaining = computed(() => {
  if (!listing.value) return 0
  const due = new Date(listing.value.due_date)
  const now = new Date()
  const diff = Math.ceil((due.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  return Math.max(0, diff)
})

const formattedRate = computed(() => {
  if (!listing.value || listing.value.suggested_discount_rate == null) return '-'
  return formatPersianNumber(formatCurrency(Number(listing.value.suggested_discount_rate)))
})

const resubmitRemaining = computed(() => {
  if (!listing.value) return 3
  return Math.max(0, 3 - (listing.value.resubmit_count ?? 0))
})

onMounted(() => {
  const id = route.params.id as string
  if (id) {
    fetchListing(id)
  }
})

async function fetchListing(id: string) {
  try {
    await store.fetchListing(id)
  } catch {
    // error handled by store
  }
}

function goBack() {
  window.history.length > 1 ? window.history.back() : router.push('/app/listings')
}

function expressInterest() {
  showToast('درخوا�ت شما ثبت شد', 'success')
}

function handleResubmit() {
  showToast('آگهی برای بررسی مجدد ارسال شد', 'info')
  router.push('/app/listings')
}

</script>

<style scoped>
.listing-detail {
  max-width: 780px;
  margin: 0 auto;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: transparent;
  border: none;
  color: var(--text2);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  padding: 0.5rem 0;
  margin-bottom: 1.5rem;
  transition: color var(--transition-fast);
}

.back-btn:hover {
  color: var(--navy);
}

.loading-state,
.error-state {
  text-align: center;
  padding: 2rem;
  color: var(--text3);
}

.error-state {
  color: var(--red);
}

.detail-content {
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.detail-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0 0 0.2rem;
}

.detail-subtitle {
  font-size: var(--font-size-base);
  color: var(--text3);
  margin: 0;
}

/* Amount Box */
.amount-box {
  background: var(--navy);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.amount-box-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: var(--font-size-xs);
  margin-bottom: 0.25rem;
}

.amount-box-value {
  font-size: 2.25rem;
  font-weight: var(--font-weight-bold);
  color: var(--gold-light);
  font-variant-numeric: tabular-nums;
}

.amount-box-value small {
  font-size: var(--font-size-md);
  color: rgba(255, 255, 255, 0.5);
  font-weight: var(--font-weight-normal);
  margin-left: 0.4rem;
}

/* Detail Section */
.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.detail-field {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.detail-field-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.detail-field-val {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--text1);
}

.detail-field-val--teal {
  color: var(--teal);
}

.detail-description {
  font-size: var(--font-size-base);
  color: var(--text2);
  margin: 0;
  line-height: 1.6;
}

/* Actions */
.detail-actions {
  margin-top: 2rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}
</style>
