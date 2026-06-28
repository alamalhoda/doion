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

    <div v-if="isLoading" class="loading-state">
      در حال بارگذاری...
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
      <button class="btn btn--secondary btn--sm" @click="fetchListings">
        تلاش مجدد
      </button>
    </div>

    <div v-else-if="listings.length === 0" class="empty-state">
      شما تا کنون آگهی ثبت نکرده‌اید.
    </div>

    <div v-else class="listing-rows">
      <ListingCard
        v-for="item in listings"
        :key="item.id"
        :listing="item"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useListingStore } from '../stores/listingStore'
import { useFormat } from '@/composables'
import ListingCard from '../components/ListingCard.vue'

const router = useRouter()
const store = useListingStore()
const { formatPersianNumber } = useFormat()

const isLoading = computed(() => store.isLoading)
const error = computed(() => store.error)
const listings = computed(() => store.listings)

const stats = ref([
  { label: 'آگهی فعال', value: '۰' },
  { label: 'در انتظار بررسی', value: '۰' },
  { label: 'تطابق یافته', value: '۰' },
  { label: 'مجموع آگهی', value: '۰' },
])

onMounted(() => {
  fetchListings()
  updateStats()
})

function fetchListings() {
  store.fetchMyListings().catch(() => {})
}

function updateStats() {
  const list = store.listings
  stats.value = [
    { label: 'آگهی فعال', value: formatPersianNumber(list.filter(l => l.status === 'published').length) },
    { label: 'در انتظار بررسی', value: formatPersianNumber(list.filter(l => l.status === 'pending_moderation').length) },
    { label: 'تطابق یافته', value: formatPersianNumber(list.filter(l => l.status === 'matched').length) },
    { label: 'مجموع آگهی', value: formatPersianNumber(list.length) },
  ]
}

function goToCreate() {
  router.push('/app/listings/create')
}
</script>

<style scoped>
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

.loading-state,
.empty-state,
.error-state {
  text-align: center;
  padding: 2rem;
  color: var(--text3);
}

.error-state {
  color: var(--red);
}

@media (max-width: 768px) {
  .stats-grid-user {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
