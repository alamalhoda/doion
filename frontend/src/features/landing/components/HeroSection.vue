<template>
  <section class="hero-section">
    <div class="hero__content">
      <h1 class="hero__title">
        {{ $t('landing.hero_title') }}
      </h1>
      <p class="hero__subtitle">
        {{ $t('landing.hero_subtitle') }}
      </p>
      <div class="hero__actions">
        <Button
          variant="primary"
          @click="handleGetStarted"
        >
          {{ $t('landing.get_started') }}
        </Button>
        <Button
          variant="ghost"
          @click="handleLearnMore"
        >
          {{ $t('landing.learn_more') }}
        </Button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'
import { ROUTES } from '@/constants/routes'

const router = useRouter()

function handleGetStarted() {
  router.push(ROUTES.LOGIN)
}

function handleLearnMore() {
  // Scroll to stats or steps section
  const statsSection = document.querySelector('.stats-bar')
  statsSection?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
.hero-section {
  width: 100%;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: #fff;
  padding: var(--spacing-2xl);
}

.hero__content {
  text-align: center;
  max-width: 600px;
}

.hero__title {
  font-size: var(--font-size-hero);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--spacing-lg);
}

.hero__subtitle {
  font-size: var(--font-size-lg);
  margin: 0 0 var(--spacing-2xl);
  opacity: 0.9;
}

.hero__actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}
</style>