<template>
  <div class="step-card">
    <div class="step-card__icon">
      {{ stepNumber }}
    </div>
    <h3 class="step-card__title">
      {{ title }}
    </h3>
    <p class="step-card__description">
      {{ description }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  stepNumber: number
  title: string
  description: string
}

defineProps<Props>()
</script>

<style scoped>
.step-card {
  flex: 1;
  min-width: 250px;
  padding: var(--spacing-xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  text-align: center;
}

.step-card__icon {
  width: 40px;
  height: 40px;
  margin: 0 auto var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  color: #fff;
  border-radius: 50%;
  font-weight: var(--font-weight-bold);
}

.step-card__title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
  margin: 0 0 var(--spacing-md);
  color: var(--color-text-primary);
}

.step-card__description {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
  line-height: var(--line-height-base);
}
</style>