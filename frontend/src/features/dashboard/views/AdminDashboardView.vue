<template>
  <div class="admin-dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header-inner">
        <h1 class="page-header-title">
          داشبورد مدیریت
        </h1>
        <p class="page-header-subtitle">
          خلاصه وضعیت پلتفرم
        </p>
      </div>
    </div>

    <!-- Stats Bar -->
    <section class="stats-bar">
      <div class="stats-grid">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="stat-card"
        >
          <div
            class="stat-icon"
            :style="{ background: stat.iconBg }"
          >
            <span
              v-if="stat.icon"
              class="stat-icon-emoji"
            >{{ stat.icon }}</span>
          </div>
          <div>
            <div class="stat-value">
              {{ stat.value }}
            </div>
            <div class="stat-label">
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="admin-content">
      <div
        v-if="isLoading"
        class="admin-loading"
      >
        {{ $t('common.loading') }}
      </div>

      <div
        v-else-if="error"
        class="admin-error"
      >
        {{ error }}
      </div>

      <div
        v-else
        class="admin-section"
      >
        <h2 class="admin-section-title">
          آگهی‌های در انتظار بررسی
        </h2>
        <p class="admin-section-subtitle">
          آگهی‌های ثبت‌شده را بررسی و تأیید یا رد کنید
        </p>

        <DataTable
          :columns="listingColumns"
          :data="pendingListings"
          clickable
        >
          <template #cell-risk="{ row }">
            <RiskBadge :risk="getRisk(row)" />
          </template>
          <template #actions="{ row }">
            <button
              class="btn btn--sm btn--teal"
              @click="viewListing(row)"
            >
              بررسی
            </button>
          </template>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useListingStore }ings/stores/listingStore'
import { ListingService } from '@/features/listings/services/listingService'

const listingStore = useListingStore()

interface Listing {
  id: number
  title: string
  issuer: string
  amount: number
  dueDate: string
  risk: 'low' | 'mid' | 'high'
}

const listingColumns = [
  { key: 'title', label: 'عنوان آگهی' },
  { key: 'issuer', label: 'صادرکننده' },
  { key: 'amount', label: 'مبلغ' },
  { key: 'dueDate', label: 'سررسید' },
  { key: 'risk', label: 'ریسک' },
  { key: 'status', label: 'وضعیت' },
]

const isLoading = ref(false)
const error = ref<string | null>(null)

const pendingListings = computed(() =>
  listingStore.listings
    .filter((l) => l.status === 'pending_moderation')
    .slice(0, 5)
    .map((l) => ({
      id: l.id,
      title: `${l.cheque_serial_number} — ${l.issuer_name}`,
      issuer: l.issuer_profile?.name || l.issuer_name,
      amount: l.face_amount,
      dueDate: l.due_date,
      risk: (l.risk_tier || 'low') as 'low' | 'mid' | 'high',
      status: l.status,
    }))
)

const pendingCount = computed(() =>
  listingStore.listings.filter((l) => l.status === 'pending_moderation').length
)

const publishedCount = computed(() =>
  listingStore.listings.filter((l) => l.status === 'published').length
)

const rejectedCount = computed(() =>
  listingStore.listings.filter((l) => l.status === 'rejected').length
)

const stats = computed(() => [
  { label: 'در انتظار بررسی', value: pendingCount.value.toString(), iconBg: 'var(--orange-light)', icon: '⏳' },
  { label: 'تأیید شده', value: publishedCount.value.toString(), iconBg: 'var(--teal-light)', icon: '✅' },
  { label: 'رد شده', value: rejectedCount.value.toString(), iconBg: 'var(--red-light)', icon: '❌' },
  { label: 'کل آگهی‌ها', value: listingStore.listings.length.toString(), iconBg: 'var(--gold-pale)', icon: '�' },
])

async function loadData(): Promise<void> {
  isLoading.value = true
  error.value = null
  try {
    await listingStore.fetchAllListings()
  } catch (err: unknown) {
    const anyErr = err as { response?: { data?: { error?: { message?: string } } } }
    error.value = anyErr?.response?.data?.error?.message || 'error.unknown'
  } finally {
    isLoading.value = false
  }
}

function viewListing(id: number): void {
  console.log('View listing:', id)
}

function getRisk(row: Listing): 'low' | 'mid' | 'high' {
  return row.risk
}

onMounted(() => {
  loadData()
})
</script>

<style>
.admin-dashboard {
  min-height: 100vh;
}

/* Page Header */
.page-header {
  background: var(--navy);
  padding: 1.5rem 2rem;
  border-radius: var(--radius-lg);
  margin-bottom: 2rem;
}

.page-header-inner {
  max-width: 1100px;
  margin: 0 auto;
}

.page-header-title {
  color: #fff;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 0.25rem;
}

.page-header-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: var(--font-size-base);
  margin: 0;
}

/* Stats Bar */
.stats-bar {
  background: var(--navy);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 1.5rem 2rem;
  border-radius: var(--radius-lg);
  margin-bottom: 2rem;
}

.stats-grid {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 1.2rem;
}

.stat-icon-emoji {
  font-size: 1.2rem;
  line-height: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--gold-light);
  line-height: 1.1;
}

.stat-label {
  font-size: var(--font-size-xs);
  color: rgba(255, 255, 255, 0.6);
  margin-top: 0.15rem;
}

/* Admin Content */
.admin-content {
  max-width: 1100px;
  margin: 0 auto;
}

.admin-section {
  margin-bottom: 2rem;
}

.admin-section-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
  margin: 0 0 0.25rem;
}

.admin-section-subtitle {
  font-size: var(--font-size-base);
  color: var(--text3);
  margin: 0 0 1.25rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .page-header {
    padding: 1.25rem 1rem;
  }

  .stats-bar {
    padding: 1rem;
  }
}

.admin-loading,
.admin-error {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}
</style>
