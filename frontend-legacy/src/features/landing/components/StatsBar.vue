<template>
  <div class="stats-bar">
    <div class="stats__inner">
      <div
        v-for="stat in stats"
        :key="stat.key"
        class="stat-item"
      >
        <span class="stat__value">{{ stat.value }}</span>
        <span class="stat__label">{{ stat.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Stat {
  key: string
  value: string
  label: string
}

const stats: Stat[] = [
  { key: 'transactions', value: '۱٬۲۵۰+', label: t('landing.stats.transactions') },
  { key: 'users', value: '۵۰۰+', label: t('landing.stats.users') },
  { key: 'volume', value: '۲.۵ میلیارد ریال', label: t('landing.stats.volume') },
]
</script>

<style scoped>
.stats-bar {
  background: var(--surface);
  padding: var(--spacing-xl) 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.stats__inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  gap: var(--spacing-2xl);
}

.stat-item {
  text-align: center;
}

.stat__value {
  display: block;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.stat__label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}
</style>