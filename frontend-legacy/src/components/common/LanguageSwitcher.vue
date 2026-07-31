<template>
  <div class="language-switcher">
    <select
      v-model="currentLocale"
      @change="changeLocale"
    >
      <option value="fa">
        {{ $t('language.fa') }}
      </option>
      <option value="en">
        {{ $t('language.en') }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { STORAGE_KEYS } from '@/constants/storage'

const { locale } = useI18n()

const currentLocale = computed({
  get: () => locale.value,
  set: (value) => {
    locale.value = value
    sessionStorage.setItem(STORAGE_KEYS.LOCALE, value)
    document.documentElement.dir = value === 'fa' ? 'rtl' : 'ltr'
  },
})

function changeLocale(event: Event) {
  const target = event.target as HTMLSelectElement
  currentLocale.value = target.value
}
</script>

<style scoped>
.language-switcher select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
  cursor: pointer;
}
</style>
