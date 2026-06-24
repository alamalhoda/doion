<template>
  <div class="user-dashboard">
    <!-- Page Header -->
    <div class="user-header">
      <h1 class="user-header-title">
        داشبورد من
      </h1>
      <div class="user-header-actions">
        <button
          class="btn btn--primary"
          @click="goToCreate"
        >
          + ثبت آگهی جدید
        </button>
      </div>
    </div>

    <!-- Stats Grid -->
    <section class="stats-grid-user">
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
    </section>

    <!-- Tabs -->
    <div class="dash-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="dash-tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: My Listings -->
    <div
      v-if="activeTab === 'listings'"
      class="dash-section"
    >
      <h2 class="dash-section-title">
        آگهی‌های جاری
      </h2>

      <div class="listing-rows">
        <div
          v-for="item in myListings"
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

    <!-- Tab: Matches -->
    <div
      v-if="activeTab === 'matches'"
      class="dash-section"
    >
      <h2 class="dash-section-title">
        تطابق‌های اخیر
      </h2>
      <EmptyState
        title="تطابق جدیدی یافت نشده"
        description="هنگام یافتن تطابق، اینجا نمایش داده می‌شود."
      />
    </div>

    <!-- Tab: Activity -->
    <div
      v-if="activeTab === 'activity'"
      class="dash-section"
    >
      <h2 class="dash-section-title">
        فعالیت اخیر
      </h2>
      <div class="activity-list">
        <div
          v-for="activity in activities"
          :key="activity.id"
          class="activity-item"
        >
          <div
            class="activity-dot"
            :style="{ background: activity.dotColor }"
          />
          <div class="activity-content">
            <div class="activity-title">
              {{ activity.title }}
            </div>
            <div class="activity-time">
              {{ activity.time }}
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
import StatusPill from '@/components/StatusPill.vue'
import EmptyState from '@/components/EmptyState.vue'

const router = useRouter()

const activeTab = ref('listings')

const tabs = [
  { key: 'listings', label: 'آگهی‌های من' },
  { key: 'matches', label: 'تطابق‌ها' },
  { key: 'activity', label: 'فعالیت اخیر' },
]

const stats = ref([
  { label: 'آگهی فعال', value: '۳' },
  { label: 'در انتظار بررسی', value: '۱' },
  { label: 'تطابق یافته', value: '۲' },
  { label: 'مجموع آگهی', value: '۱.۲ میلیارد' },
])

const myListings = ref<{
  id: number
  title: string
  meta: string
  amount: number
  status: string
  statusVariant: 'published' | 'pending' | 'matched' | 'reviewing' | 'rejected' | 'approved' | 'kyc-pending'
}[]>([
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
    status: 'تط_matchیافته',
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

const activities = ref([
  { id: 1, title: 'سرمایه‌گذار جدید برای آگهی ۵۰۰M ریالی ابراز تمایل کرد', time: '۲ ساعت پیش', dotColor: 'var(--teal)' },
  { id: 2, title: 'آگهی شما (چک بانک صادرات) تطابق قطعی یافت', time: 'دیروز — ۱۳:۴۵', dotColor: 'var(--gold)' },
  { id: 3, title: 'آگهی جدید (چک بانک پارسیان) ثبت و در صف بررسی قرار گرفت', time: 'دیروز — ۰۹:۱۲', dotColor: 'var(--navy-light)' },
  { id: 4, title: 'احراز هویت KYC شما با موفقیت تأیید شد', time: '۳ روز پیش', dotColor: 'var(--teal)' },
])

const formatCurrency = (value: number) => {
  return value.toLocaleString('fa-IR')
}

const goToCreate = () => {
  router.push('/app/listings/create')
}

const goToDetail = (id: number) => {
  router.push(`/app/listings/${id}`)
}
</script>

<style>
.user-dashboard {
  min-height: 100vh;
}

/* Page Header */
.user-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.user-header-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  margin: 0;
}

/* Stats Grid */
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

/* Tabs */
.dash-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border);
}

.dash-tab {
  background: transparent;
  border: none;
  padding: 0.65rem 1.25rem;
  font-size: var(--font-size-base);
  color: var(--text3);
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-weight: var(--font-weight-medium);
}

.dash-tab:hover {
  color: var(--navy);
}

.dash-tab.active {
  color: var(--navy);
  border-bottom-color: var(--navy);
  font-weight: var(--font-weight-semibold);
}

/* Section */
.dash-section-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  margin: 0 0 1rem;
}

/* Listing Rows */
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

/* Activity */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 0.85rem;
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 0.4rem;
  flex-shrink: 0;
}

.activity-title {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text1);
  margin: 0 0 0.15rem;
}

.activity-time {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin: 0;
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
