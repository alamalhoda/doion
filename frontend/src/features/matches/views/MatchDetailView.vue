<template>
  <div class="match-detail-view">
    <div class="view-header">
      <h1>{{ $t('matches.detail_title') }}</h1>
    </div>
    <p>Match ID: {{ $route.params.id }}</p>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.match-detail-view {
  max-width: 800px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--spacing-xl);
}

.view-header h1 {
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
}
</style>
