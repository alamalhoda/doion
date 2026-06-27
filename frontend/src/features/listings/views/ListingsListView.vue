<template>
  <div class="listing-list">
    <div class="listings-header">
      <h1 class="listings-title">
        آگهی‌های من
      </h1>
      <button
        class="btn btn--primary"
        @click="goToCreate"
      >
        + ثبت آگهی جدید
      </button>
    </div>

    <div class="stats-grid-user">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="stat-card-user"
      >
        <div class="stat-value-user">
          {{ stat.value }}
        </div>
        <div class="stat-label-user">
          {{ stat.label }}
        </div>
      </div>
    </div>

    <h2 class="dash-section-title">
      آگهی‌های جاری
    </h2>

    <div class="listing-rows">
      <div
        v-for="item in listings"
        :key="item.id"
        class="listing-row"
        @click="goToDetail(item.id)"
      >
        <div class="listing-row-icon">
          <svg
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="var(--gold-light)"
          >
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 4h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S9 13.88 9 12.5 10.12 10 11.5 10c.57 0 1.08.19 1.5.5V7h4v0z" />
          </svg>
        </div>
        <div class="listing-row-info">
          <h4 class="listing-row-title">
            {{ item.title }}
          </h4>
          <p class="listing-row-meta">
            {{ item.meta }}
          </p>
        </div>
        <div class="listing-row-amount">
          {{ formatCurrency(item.amount) }}
          <small>ریال</small>
        </div>
        <StatusPill :variant="item.statusVariant">
          {{ item.status }}
        </StatusPill>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StatusPill from '@/components/StatusPill.vue'
import { useFormat } from '@/composables'

const router = useRouter()
const { formatCurrency } = useFormat()

const stats = ref([
  { label: 'آگهی فعال', value: '۳' },
  { label: 'در انتظار بررسی', value: '۱' },
  { label: 'تطابق یافته', value: '۲' },
  { label: 'مجموع آگهی', value: '۱.۲ میلیارد' },
])

const listings = ref([
  {
    id: 1,
    title: 'چک بانک ملت — شرکت آسان‌پرداخت',
    meta: 'سررسید: ۱۴۰۴/۰۳/۲۰ · ۴۵ روز دیگر · ۳ درخواست سرمایه‌گذار',
    amount: 500000000,
    status: 'منتشر شده',
    statusVariant: 'published',
  },
  {
    id: 2,
    title: 'چک بانک صادرات — محمدرضا احمدی',
    meta: 'سررسید: ۱۴۰۴/۰۵/۱۰ · ۹۵ روز دیگر · ۱ تطابق قطعی',
    amount: 120000000,
    status: 'تطابق‌یافته',
    statusVariant: 'matched',
  },
  {
    id: 3,
    title: 'چک بانک پارسیان — شرکت فناوری ایده‌آل',
    meta: 'ثبت‌شده: دیروز · در انتظار تأیید مدیریت',
    amount: 600000000,
    status: 'در انتظار بررسی',
    statusVariant: 'pending',
  },
])

const goToCreate = () => router.push('/app/listings/create')
const goToDetail = (id: number) => router.push(`/app/listings/${id}`)
</script>

<style>
.listing-list {
  max-width: 1100px;
  margin: 0 auto;
}

.listings-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.listings-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0;
}

.stats-grid-user {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card-user {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
}

.stat-value-user {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  line-height: 1.1;
}

.stat-label-user {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin-top: 0.15rem;
}

.dash-section-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  margin: 0 0 1rem;
}

.listing-rows {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.listing-row {
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

.listing-row:hover {
  border-color: var(--border2);
}

.listing-row-icon {
  width: 40px;
  height: 40px;
  background: var(--navy);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.listing-row-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
  margin: 0 0 0.2rem;
}

.listing-row-meta {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin: 0;
}

.listing-row-amount {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text1);
  text-align: left;
}

.listing-row-amount small {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}

@media (max-width: 768px) {
  .stats-grid-user {
    grid-template-columns: repeat(2, 1fr);
  }

  .listing-row {
    grid-template-columns: 1fr auto;
  }

  .listing-row-icon {
    display: none;
  }

  .listing-row-amount {
    text-align: right;
  }
}
</style>
