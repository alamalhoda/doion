<template>
  <footer class="footer-disclaimer">
    <p>{{ disclaimer }}</p>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const disclaimer = computed(() => t('landing.disclaimer'))
</script>

<style scoped>
.footer-disclaimer {
  background: var(--surface2);
  padding: var(--spacing-lg);
  text-align: center;
  border-top: 1px solid var(--color-border);
}

.footer-disclaimer p {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin: 0;
}
</style>