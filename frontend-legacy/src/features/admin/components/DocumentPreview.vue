<template>
  <div class="document-preview">
    <div class="document-preview__header">
      <span class="document-preview__label">{{ $t('admin.document_preview') }}</span>
    </div>
    <div class="document-preview__list">
      <div
        v-for="doc in documents"
        :key="doc.id"
        class="document-preview__item"
      >
        <span class="document-preview__type">{{ doc.document_type }}</span>
        <span class="document-preview__size">{{ formatSize(doc.file_size) }}</span>
      </div>
    </div>
    <p
      v-if="documents.length === 0"
      class="document-preview__empty"
    >
      {{ $t('admin.no_documents') }}
    </p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  documents: Array<{
    id: string
    document_type: string
    file_size: number
  }>
}>()

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}
</script>

<style scoped>
.document-preview {
  padding: var(--spacing-sm) 0;
}

.document-preview__header {
  margin-bottom: var(--spacing-sm);
}

.document-preview__label {
  font-size: var(--font-size-sm);
  color: var(--text3);
  font-weight: var(--font-weight-medium);
}

.document-preview__list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.document-preview__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
}

.document-preview__type {
  color: var(--text1);
}

.document-preview__size {
  color: var(--text2);
}

.document-preview__empty {
  font-size: var(--font-size-sm);
  color: var(--text3);
  text-align: center;
  padding: var(--spacing-md) 0;
}

@media (max-width: 768px) {
  .document-preview__item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>
