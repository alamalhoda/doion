<template>
  <div class="landing-view">
    <HeroSection />
    <StatsBar />

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
import HeroSection from '../components/HeroSection.vue'
import StatsBar from '../components/StatsBar.vue'
import StepCard from '../components/StepCard.vue'
import FooterDisclaimer from '../components/FooterDisclaimer.vue'
</script>

<style scoped>
.landing-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.steps-section {
  padding: var(--spacing-2xl) var(--spacing-xl);
  background: var(--bg);
}

.steps__title {
  text-align: center;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--spacing-2xl);
  color: var(--color-text-primary);
}

.steps__grid {
  display: flex;
  gap: var(--spacing-lg);
  max-width: 1200px;
  margin: 0 auto;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .steps__grid {
    flex-direction: column;
  }
}
</style>