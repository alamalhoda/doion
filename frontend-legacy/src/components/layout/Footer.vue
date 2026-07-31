<template>
  <footer class="footer">
    <div class="footer__inner">
      <p class="footer__copyright">
        {{ copyright }}
      </p>
      <p class="footer__disclaimer">
        {{ disclaimer }}
      </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const copyright = computed(() => `© ${new Date().getFullYear()} چک‌بازار. All rights reserved.`)
const disclaimer = computed(() => t('landing.disclaimer'))
</script>

<style scoped>
.footer {
  background: var(--surface2);
  border-top: 1px solid var(--color-border);
  padding: var(--spacing-lg) var(--spacing-xl);
  margin-top: auto;
}

.footer__inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.footer__copyright,
.footer__disclaimer {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin: 0;
  text-align: center;
}
</style>