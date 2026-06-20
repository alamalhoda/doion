<template>
  <div class="marketplace">
    <!-- Marketplace Header -->
    <div class="market-header">
      <div class="market-header-inner">
        <h2 class="market-header-title">آگهی‌های چک</h2>
        <p class="market-header-subtitle">۲۴ آگهی فعال — به‌روزرسانی لحظه‌ای</p>
      </div>
    </div>

    <!-- Marketplace Layout -->
    <div class="market-layout">
      <!-- Filter Panel -->
      <aside class="filter-panel">
        <div class="filter-title">فیلترها</div>

        <div class="filter-group">
          <label class="filter-label">سطح ریسک</label>
          <label v-for="opt in riskOptions" :key="opt.value" class="filter-opt">
            <input type="checkbox" :checked="opt.checked" />
            <span>{{ opt.label }}</span>
          </label>
        </div>

        <div class="filter-group">
          <label class="filter-label">حداکثر روز تا سررسید</label>
          <input type="range" class="filter-range" min="7" max="180" value="120" />
          <div class="filter-range-vals">
            <span>۷ روز</span>
            <span>۱۲۰ روز</span>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">حداقل مبلغ (میلیون ریال)</label>
          <input type="range" class="filter-range" min="50" max="2000" value="50" step="50" />
          <div class="filter-range-vals">
            <span>۵۰م</span>
            <span>۵۰</span>
          </div>
        </div>

        <div class="filter-group">
          <label class="filter-label">نوع صادرکننده</label>
          <label v-for="opt in issuerOptions" :key="opt.value" class="filter-opt">
            <input type="checkbox" :checked="opt.checked" />
            <span>{{ opt.label }}</span>
          </label>
        </div>

        <button class="btn btn--primary btn--block" @click="applyFilters">
          اعمال فیلتر
        </button>
      </aside>

      <!-- Main Content -->
      <div class="market-main">
        <div class="market-toolbar">
          <span class="market-count">نمایش ۲۰ از ۲۴ آگهی</span>
          <select class="sort-select">
            <option>مرتب‌سازی: جدیدترین</option>
            <option>بیشترین نرخ تنزیل</option>
            <option>کمترین ریسک</option>
            <option>نزدیک‌ترین سررسید</option>
          </select>
        </div>

        <div class="listings-grid">
          <div
            v-for="item in listings"
            :key="item.id"
            class="listing-card"
            @click="viewDetail(item.id)"
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
                <div class="meta-item">
                  <div class="meta-key">روز تا سررسید</div>
                  <div class="meta-val">{{ item.days }} روز</div>
                </div>
                <div class="meta-item">
                  <div class="meta-key">نوع صادرکننده</div>
                  <div class="meta-val">{{ item.issuerType }}</div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <div>
                <div class="discount-rate">{{ item.rate }}</div>
                <div class="discount-label">نرخ تنزیل پیشنهادی</div>
              </div>
              <button
                class="btn btn--sm btn--primary"
                @click.stop="expressInterest(item.id)"
              >
                ابراز تمایل
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="market-footer">
      چک‌بازار — اطلاعات این صفحه صرفاً برای آشنایی است. پیش از هرگونه سرمایه‌گذاری، اطلاعات را به‌طور مستقل تأیید کنید.
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Listing {
  id: number
  issuer: string
  issuerType: string
  bank: string
  amount: number
  days: number
  risk: 'low' | 'mid' | 'high'
  rate: string
  dueDate: string
}

const riskOptions = ref([
  { value: 'low', label: 'کم ریسک', checked: true },
  { value: 'mid', label: 'ریسک متوسط', checked: true },
  { value: 'high', label: 'پر ریسک', checked: false },
])

const issuerOptions = ref([
  { value: 'legal', label: 'حقوقی', checked: true },
  { value: 'natural', label: 'حقیقی', checked: true },
])

const listings = ref<Listing[]>([
  { id: 1, issuer: 'شرکت آسان‌پرداخت', issuerType: 'حقوقی', bank: 'بانک ملت', amount: 500000000, days: 45, risk: 'low', rate: '۳.۸٪', dueDate: '۱۴۰۴/۰۳/۲۰' },
  { id: 2, issuer: 'محمدرضا احمدی', issuerType: 'حقیقی', bank: 'بانک صادرات', amount: 120000000, days: 90, risk: 'mid', rate: '۶.۸٪', dueDate: '۱۴۰۴/۰۵/۱۰' },
  { id: 3, issuer: 'شرکت تجارت گستر', issuerType: 'حقوقی', bank: 'بانک تجارت', amount: 250000000, days: 30, risk: 'low', rate: '۲.۵٪', dueDate: '۱۴۰۴/۰۲/۱۵' },
  { id: 4, issuer: 'مهران صادقی', issuerType: 'حقیقی', bank: 'بانک ملی', amount: 80000000, days: 120, risk: 'high', rate: '۱۲٪', dueDate: '۱۴۰۴/۰۷/۰۱' },
  { id: 5, issuer: 'شرکت فناوری ایده‌آل', issuerType: 'حقوقی', bank: 'بانک پارسیان', amount: 1200000000, days: 60, risk: 'low', rate: '۴.۱٪', dueDate: '۱۴۰۴/۰۴/۱۰' },
  { id: 6, issuer: 'علی محمدی تجارت', issuerType: 'حقوقی', bank: 'بانک ملی', amount: 350000000, days: 75, risk: 'mid', rate: '۷.۵٪', dueDate: '۱۴۰۴/۰۴/۲۸' },
])

const formatCurrency = (value: number) => value.toLocaleString('fa-IR')

const applyFilters = () => {
  console.log('Filters applied')
}

const expressInterest = (id: number) => {
  console.log('Express interest:', id)
}

const viewDetail = (id: number) => {
  navigateTo(`/app/listings/${id}`)
}
</script>

<style>
.marketplace {
  min-height: 100vh;
}

/* Marketplace Header */
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

/* Marketplace Layout */
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

/* Filter Panel */
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

.filter-range {
  width: 100%;
  accent-color: var(--navy);
  margin: 0.3rem 0;
}

.filter-range-vals {
  display: flex;
  justify-content: space-between;
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin-top: 0.25rem;
}

/* Toolbar */
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

/* Listings Grid */
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

/* Listing Card */
.card-header {
  background: var(--navy);
  padding: 0.85rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
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

/* Footer */
.market-footer {
  background: var(--navy);
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  padding: 1.5rem;
  font-size: var(--font-size-xs);
  margin-top: 3rem;
}
</style>
