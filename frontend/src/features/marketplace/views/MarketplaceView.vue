<template>
  <div class="marketplace">
    <div class="market-header">
      <div class="market-header-inner">
        <h2 class="market-header-title">
          آگهی‌های چک
        </h2>
        <p class="market-header-subtitle">
          ۲۴ آگهی فعال — به‌روزرسانی لحظه‌ای
        </p>
      </div>
    </div>

    <div class="market-layout">
      <aside class="filter-panel">
        <div class="filter-title">
          فیلترها
        </div>
        <div class="filter-group">
          <label class="filter-label">سطح ریسک</label>
          <label
            v-for="opt in riskOptions"
            :key="opt.value"
            class="filter-opt"
          >
            <input
              type="checkbox"
              :checked="opt.checked"
            >
            <span>{{ opt.label }}</span>
          </label>
        </div>
        <button
          class="btn btn--primary btn--block"
          @click="applyFilters"
        >
          اعمال فیلتر
        </button>
      </aside>

      <div class="market-main">
        <div class="market-toolbar">
          <span class="market-count">نمایش ۲۰ از ۲۴ آگهی</span>
          <select class="sort-select">
            <option>مرتب‌سازی: جدیدترین</option>
            <option>بیشترین نرخ تنزیل</option>
            <option>کمترین ریسک</option>
          </select>
        </div>

        <div class="listings-grid">
          <div
            v-for="item in listings"
            :key="item.id"
            class="listing-card"
          >
            <div class="card-header">
              <div class="card-issuer">
                <span class="card-issuer-dot" />
                {{ item.issuer }}
              </div>
              <RiskBadge :risk="item.risk" />
            </div>
            <div class="card-body">
              <div class="card-amount">
                <span>ریال</span>{{ formatCurrency(item.amount) }}
              </div>
              <div class="card-meta">
                <div class="meta-item">
                  <div class="meta-key">بانک</div>
                  <div class="meta-val">{{ item.bank }}</div>
                </div>
                <div class="meta-item">
                  <div class="meta-key">سررسید</div>
                  <div class="meta-val">{{ item.dueDate }}</div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <div>
                <div class="discount-rate">{{ item.rate }}</div>
                <div class="discount-label">نرخ تنزیل پیشنهادی</div>
              </div>
            <button class="btn btn--sm btn--gold">
              ابراز تمایل
            </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RiskBadge from '@/components/RiskBadge.vue'
import { useFormat } from '@/composables'

const router = useRouter()
const { formatCurrency } = useFormat()

interface Listing {
  id: number
  issuer: string
  bank: string
  amount: number
  risk: 'low' | 'mid' | 'high'
  rate: string
  dueDate: string
}

const riskOptions = ref([
  { value: 'low', label: 'کم ریسک', checked: true },
  { value: 'mid', label: 'ریسک متوسط', checked: true },
  { value: 'high', label: 'پر ریسک', checked: false },
])

const listings = ref<Listing[]>([
  { id: 1, issuer: 'شرکت آسان‌پرداخت', bank: 'بانک ملت', amount: 500000000, risk: 'low', rate: '۳.۸٪', dueDate: '۱۴۰۴/۰۳/۲۰' },
  { id: 2, issuer: 'محمدرضا احمدی', bank: 'بانک صادرات', amount: 120000000, risk: 'mid', rate: '۶.۸٪', dueDate: '۱۴۰۴/۰۵/۱۰' },
  { id: 3, issuer: 'شرکت تجارت گستر', bank: 'بانک تجارت', amount: 250000000, risk: 'low', rate: '۲.۵٪', dueDate: '۱۴۰۴/۰۲/۱۵' },
  { id: 4, issuer: 'مهران صادقی', bank: 'بانک ملی', amount: 80000000, risk: 'high', rate: '۱۲٪', dueDate: '۱۴۰۴/۰۷/۰۱' },
])

const applyFilters = () => {
  console.log('Filters applied')
}
</script>

<style>
.marketplace {
  min-height: 100vh;
}

.market-header {
  background: var(--navy);
  padding: 1.5rem 2rem;
}

.market-header-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.market-header-title {
  color: #fff;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 0.25rem;
}

.market-header-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: var(--font-size-base);
  margin: 0;
}

.market-layout {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 768px) {
  .market-layout {
    grid-template-columns: 1fr;
  }
}

.filter-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
}

.filter-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.filter-group {
  margin-bottom: 1.25rem;
}

.filter-label {
  display: block;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
  margin-bottom: 0.5rem;
}

.filter-opt {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: var(--font-size-base);
  color: var(--text2);
  margin-bottom: 0.35rem;
}

.filter-opt input[type='checkbox'] {
  accent-color: var(--navy);
  width: 15px;
  height: 15px;
}

.market-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
}

.market-count {
  font-size: var(--font-size-base);
  color: var(--text3);
}

.sort-select {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.35rem 0.75rem;
  font-size: var(--font-size-base);
  color: var(--text2);
  background: var(--surface);
  cursor: pointer;
}

.listings-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

@media (max-width: 768px) {
  .listings-grid {
    grid-template-columns: 1fr;
  }
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
