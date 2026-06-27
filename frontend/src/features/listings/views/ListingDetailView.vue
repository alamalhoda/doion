<template>
  <ComingSoonView
    title="جزئیات آگهی"
    description="مشاهده جزئیات آگهی چک"
    phase="فاز ۳"
  >
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

      <div class="detail-header">
        <div class="detail-header-info">
          <h1 class="detail-title">
            {{ listing.title }}
          </h1>
          <p class="detail-subtitle">
            {{ listing.issuer }} · {{ listing.bank }}
          </p>
        </div>
        <RiskBadge :risk="listing.risk" />
      </div>

      <div class="amount-box">
        <div>
          <div class="amount-box-label">
            مبلغ اسمی چک
          </div>
          <div class="amount-box-value">
            <small>ریال</small>{{ formatCurrency(listing.amount) }}
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
              {{ listing.bank }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              تاریخ سررسید
            </div>
            <div class="detail-field-val">
              {{ listing.dueDate }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              روز تا سررسید
            </div>
            <div class="detail-field-val">
              {{ listing.days }} روز
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              نوع صادرکننده
            </div>
            <div class="detail-field-val">
              {{ listing.issuerType }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              نرخ تنزیل پیشنهادی
            </div>
            <div class="detail-field-val detail-field-val--teal">
              {{ listing.rate }}
            </div>
          </div>
          <div class="detail-field">
            <div class="detail-field-key">
              شماره صیاد
            </div>
            <div class="detail-field-val">
              {{ listing.sayad }}
            </div>
          </div>
        </div>
      </div>

      <div class="detail-actions">
        <button
          class="btn btn--gold btn--lg"
          @click="expressInterest"
        >
          ابراز تمایل به خرید
        </button>
      </div>
    </div>
  </ComingSoonView>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ComingSoonView from '@/components/ComingSoonView.vue'

interface Listing {
  id: number
  title: string
  issuer: string
  bank: string
  amount: number
  days: number
  risk: 'low' | 'mid' | 'high'
  rate: string
  dueDate: string
  issuerType: string
  sayad: string
}

const router = useRouter()

const listing = ref<Listing>({
  id: 1,
  title: 'چک ۵۰۰ میلیونی — شرکت آسان‌پرداخت',
  issuer: 'شرکت آسان‌پرداخت',
  bank: 'بانک ملت',
  amount: 500000000,
  days: 45,
  risk: 'low',
  rate: '۳.۸٪',
  dueDate: '۱۴۰۴/۰۳/۲۰',
  issuerType: 'حقوقی',
  sayad: '۱۴۰۲۱۰۳۵۶۸۷۱۲۳',
})

const formatCurrency = (value: number) => value.toLocaleString('fa-IR')

const goBack = () => router.push('/app/listings')

const expressInterest = () => {
  console.log('Express interest:', listing.value.id)
}
</script>

<style>
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

/* Actions */
.detail-actions {
  margin-top: 2rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}
</style>
