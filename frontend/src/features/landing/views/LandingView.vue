<template>
  <div class="landing-view">
    <HeroSection />
    <StatsBar />

    <section class="latest-section">
      <h2 class="latest__title">
        آخرین آگهی‌ها
      </h2>
      <div
        v-if="isLoading"
        class="latest-grid"
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
        v-else-if="listings.length === 0"
        class="empty-state"
      >
        آگهی فعالی موجود نیست.
      </div>
      <div
        v-else
        class="latest-grid"
      >
        <MarketplaceListingCard
          v-for="item in listings"
          :key="item.id"
          :listing="item"
          :hoverable="false"
        />
      </div>
    </section>

    <section class="steps-section">
      <h2 class="steps__title">
        {{ $t('landing.steps.how_it_works') }}
      </h2>
      <div class="steps__grid">
        <StepCard
          :step-number="1"
          :title="$t('landing.steps.step_1')"
          :description="$t('landing.steps.step_1_desc')"
        />
        <StepCard
          :step-number="2"
          :title="$t('landing.steps.step_2')"
          :description="$t('landing.steps.step_2_desc')"
        />
        <StepCard
          :step-number="3"
          :title="$t('landing.steps.step_3')"
          :description="$t('landing.steps.step_3_desc')"
        />
      </div>
    </section>

    <FooterDisclaimer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import HeroSection from '../components/HeroSection.vue'
import StatsBar from '../components/StatsBar.vue'
import StepCard from '../components/StepCard.vue'
import FooterDisclaimer from '../components/FooterDisclaimer.vue'
import MarketplaceListingCard from '@/features/marketplace/components/MarketplaceListingCard.vue'
import { ListingService } from '@/features/listings/services/listingService'
import type { MarketplaceLatestListing } from '@/features/listings/types/listing'

const isLoading = ref(false)
const listings = ref<MarketplaceLatestListing[]>([])

onMounted(async () => {
  isLoading.value = true
  try {
    listings.value = await ListingService.getLatestMarketplaceListings()
  } catch {
    listings.value = []
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.latest-section {
  padding: var(--spacing-2xl) var(--spacing-xl);
  background: var(--bg);
}

.latest__title {
  text-align: center;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--spacing-2xl);
  color: var(--color-text-primary);
}

.latest-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1024px) {
  .latest-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .latest-grid {
    grid-template-columns: 1fr;
  }
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--text3);
}

.empty-state .btn {
  margin-top: 1rem;
  text-decoration: none;
  display: inline-block;
}
</style>
