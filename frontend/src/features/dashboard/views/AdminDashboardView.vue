<template>
  <div class="admin-dashboard">
    <!-- Page Header -->
    <div class="page-header">
      <div class="page-header-inner">
        <h1 class="page-header-title">
          {{ $t('dashboard.admin_title') }}
        </h1>
        <p class="page-header-subtitle">
          {{ $t('admin.dashboard_subtitle') }}
        </p>
      </div>
    </div>

    <!-- Stats Bar -->
    <section class="stats-bar">
      <div class="stats-grid">
        <StatCard
          v-for="card in statCards"
          :key="card.title"
          :title="card.title"
          :value="card.value"
          :icon="card.icon"
          :variant="card.variant"
        />
      </div>
    </section>

    <!-- Main Content -->
    <div class="admin-content">
      <div
        v-if="isLoading"
        class="admin-loading"
      >
        <Skeleton :lines="4" />
      </div>

      <div
        v-else-if="error"
        class="admin-error"
      >
        <EmptyState
          :title="$t('admin.error_title')"
          :description="$t('admin.error_description')"
          icon="⚠️"
        >
          <template #actions>
            <Button
              variant="primary"
              @click="retry"
            >
              {{ $t('common.retry') }}
            </Button>
          </template>
        </EmptyState>
      </div>

      <div
        v-else
        class="admin-section"
      >
        <h2 class="admin-section-title">
          {{ $t('admin.pending_section_title') }}
        </h2>
        <p class="admin-section-subtitle">
          {{ $t('admin.pending_section_subtitle') }}
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
import { useI18n } from 'vue-i18n'
import { useAdminStore } from '@/features/admin/stores/adminStore'
import { useListingStore } from '@/features/listings/stores/listingStore'
import StatCard from '@/components/ui/StatCard.vue'
import Skeleton from '@/components/ui/Skeleton.vue'
import EmptyState from '@/components/EmptyState.vue'
import Button from '@/components/ui/Button.vue'

const { t } = useI18n()
const adminStore = useAdminStore()
const listingStore = useListingStore()

const isLoading = computed(() => adminStore.isLoading)
const error = computed(() => adminStore.error)

const statCards = computed(() => {
  const s = adminStore.stats
  if (!s) return []

  return [
    { title: t('admin.stat_total_listings'), value: s.listings.total, icon: '📋', variant: 'default' as const },
    { title: t('admin.stat_published'), value: s.listings.published, icon: '✅', variant: 'success' as const },
    { title: t('admin.stat_pending_moderation'), value: s.listings.pending_moderation, icon: '⏳', variant: 'warning' as const },
    { title: t('admin.stat_rejected'), value: s.listings.rejected, icon: '❌', variant: 'danger' as const },
    { title: t('admin.stat_expired'), value: s.listings.expired, icon: '⏰', variant: 'info' as const },
    { title: t('admin.stat_matched'), value: s.listings.matched, icon: '🤝', variant: 'default' as const },
    { title: t('admin.stat_total_users'), value: s.users.total, icon: '👥', variant: 'default' as const },
    { title: t('admin.stat_kyc_pending'), value: s.users.kyc_pending, icon: '🔍', variant: 'warning' as const },
  ]
})

const listingColumns = [
  { key: 'title', label: 'عنوان آگهی' },
  { key: 'issuer', label: 'صادرکننده' },
  { key: 'amount', label: 'مبلغ' },
  { key: 'dueDate', label: 'سررسید' },
  { key: 'risk', label: 'ریسک' },
  { key: 'status', label: 'وضعیت' },
]

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

function viewListing(id: number): void {
  console.log('View listing:', id)
}

function getRisk(row: { risk: string }): 'low' | 'mid' | 'high' {
  return row.risk as 'low' | 'mid' | 'high'
}

async function retry(): Promise<void> {
  await Promise.all([
    adminStore.fetchStats(),
    listingStore.fetchAllListings(),
  ])
}

onMounted(() => {
  adminStore.fetchStats()
  listingStore.fetchAllListings()
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
