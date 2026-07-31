<template>
  <div class="issuer-info">
    <div class="issuer-info__header">
      <span class="issuer-info__label">{{ $t('admin.issuer_info') }}</span>
    </div>
    <div class="issuer-info__rows">
      <div class="issuer-info__row">
        <span class="issuer-info__key">{{ $t('admin.issuer_name') }}</span>
        <span class="issuer-info__value">{{ issuer.name || '—' }}</span>
      </div>
      <div class="issuer-info__row">
        <span class="issuer-info__key">{{ $t('admin.issuer_national_id') }}</span>
        <span class="issuer-info__value">{{ issuer.national_or_company_id || '—' }}</span>
      </div>
      <div class="issuer-info__row">
        <span class="issuer-info__key">{{ $t('admin.credit_score') }}</span>
        <span class="issuer-info__value">{{ issuer.credit_score ?? '—' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  issuer: {
    name: string
    national_or_company_id: string
    credit_score?: number | null
  }
}>()
</script>

<style scoped>
.issuer-info {
  padding: var(--spacing-sm) 0;
}

.issuer-info__header {
  margin-bottom: var(--spacing-sm);
}

.issuer-info__label {
  font-size: var(--font-size-sm);
  color: var(--text3);
  font-weight: var(--font-weight-medium);
}

.issuer-info__rows {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.issuer-info__row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xs) 0;
  border-bottom: 1px solid var(--border-light);
}

.issuer-info__key {
  font-size: var(--font-size-sm);
  color: var(--text2);
}

.issuer-info__value {
  font-size: var(--font-size-sm);
  color: var(--text1);
  font-weight: var(--font-weight-medium);
}

@media (max-width: 768px) {
  .issuer-info__row {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>
