<template>
  <div class="marketplace">
    <div class="market-header">
      <div class="market-header-inner">
        <h2 class="market-header-title">
          آگهی‌های چک
        </h2>
        <p class="market-header-subtitle">
          {{ totalCount.toLocaleString('fa-IR') }} آگهی فعال — به‌روزرسانی لحظه‌ای
        </p>
      </div>
    </div>

    <div class="market-layout">
      <FilterSidebar
        v-model="localFilters"
        @apply="applyFilters"
        @reset="resetFilters"
      />

      <div class="market-main">
        <div class="market-toolbar">
          <span class="market-count">
            نمایش {{ startIndex.toLocaleString('fa-IR') }} تا {{ endIndex.toLocaleString('fa-IR') }} از {{ totalCount.toLocaleString('fa-IR') }} آگهی
          </span>
          <select
            class="sort-select"
            :value="store.sortBy"
            @change="onSortChange"
          >
            <option value="-created_at">
              مرتب‌سازی: جدیدترین
            </option>
            <option value="created_at">
              مرتب‌سازی: قدیمی‌ترین
            </option>
            <option value="-face_amount">
              بیشترین مبلغ
            </option>
            <option value="face_amount">
              کمترین مبلغ
            </option>
            <option value="-suggested_discount_rate">
              بیشترین نرخ تنزیل
            </option>
            <option value="due_date">
              نزدیک‌ترین سررسید
            </option>
          </select>
        </div>

        <div
          v-if="store.isLoading"
          class="listings-grid"
        >
          <div
            v-for="n in 4"
            :key="n"
            class="listing-card listing-card--skeleton"
          >
            <div class="skeleton-header" />
            <div class="skeleton-body">
              <div class="skeleton-amount" />
              <div class="skeleton-meta" />
            </div>
            <div class="skeleton-footer" />
          </div>
        </div>

        <div
          v-else-if="error"
          class="error-state"
        >
          {{ error }}
          <button
            class="btn btn--secondary btn--sm"
            @click="store.fetchListings()"
          >
            تلاش مجدد
          </button>
        </div>

        <div
          v-else-if="store.listings.length === 0"
          class="empty-state"
        >
          آگهی‌ای با فیلترهای انتخابی شما یافت نشد.
        </div>

        <div
          v-else
          class="listings-grid"
        >
          <div
            v-for="item in store.listings"
            :key="item.id"
            class="listing-card-wrapper"
          >
            <MarketplaceListingCard
              :listing="item"
              :hoverable="true"
              @click="openDetail(item)"
            />
          </div>
        </div>

        <div
          v-if="totalPages > 1"
          class="market-pagination"
        >
          <button
            class="btn btn--secondary btn--sm"
            :disabled="store.page <= 1"
            @click="store.setPage(store.page - 1)"
          >
            قبلی
          </button>
          <span class="pagination-info">
            صفحه {{ store.page.toLocaleString('fa-IR') }} از {{ totalPages.toLocaleString('fa-IR') }}
          </span>
          <button
            class="btn btn--secondary btn--sm"
            :disabled="store.page >= totalPages"
            @click="store.setPage(store.page + 1)"
          >
            بعدی
          </button>
        </div>
      </div>
    </div>

    <ListingDetailModal
      v-model="showDetail"
      :listing="selectedListing"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMarketplaceStore, type MarketplaceFilters } from '../stores/marketplaceStore'
import type { ChequeListing } from '@/features/listings/types/listing'
import MarketplaceListingCard from '../components/MarketplaceListingCard.vue'
import FilterSidebar from '../components/FilterSidebar.vue'
import ListingDetailModal from '../components/ListingDetailModal.vue'

const store = useMarketplaceStore()

const localFilters = ref<MarketplaceFilters>({ ...store.filters })
const showDetail = ref(false)
const selectedListing = ref<ChequeListing | null>(null)

const error = computed(() => store.error)
const totalCount = computed(() => store.totalCount)
const totalPages = computed(() => Math.max(1, Math.ceil(store.totalCount / store.pageSize)))
const startIndex = computed(() => (store.page - 1) * store.pageSize + 1)
const endIndex = computed(() => Math.min(store.page * store.pageSize, store.totalCount))

onMounted(() => {
  store.fetchListings()
})

watch(() => ({ ...store.filters }), (newVal) => {
  localFilters.value = { ...newVal }
}, { deep: true })

function applyFilters() {
  store.filters = { ...localFilters.value }
  store.fetchListings()
}

function resetFilters() {
  store.resetFilters()
  localFilters.value = {}
  store.fetchListings()
}

function onSortChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value
  store.setSort(value)
  store.fetchListings()
}

function openDetail(item: ChequeListing) {
  selectedListing.value = item
  showDetail.value = true
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

.listing-card-wrapper {
  display: contents;
}

.error-state {
  text-align: center;
  padding: 2rem;
  color: var(--red);
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text3);
}

.market-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-info {
  font-size: var(--font-size-base);
  color: var(--text2);
}

.listing-card--skeleton {
  pointer-events: none;
}

.skeleton-header {
  height: 52px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-body {
  padding: 1.1rem;
}

.skeleton-amount {
  height: 36px;
  width: 60%;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
  margin-bottom: 0.85rem;
}

.skeleton-meta {
  height: 40px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

.skeleton-footer {
  height: 52px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
