<template>
  <div class="matches-view">
    <div class="view-header">
      <h1>{{ $t('matches.title') }}</h1>
      <p class="subtitle">{{ $t('matches.subtitle') }}</p>
    </div>

    <div v-if="isLoading" class="loading-state">
      {{ $t('common.loading') }}
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>

    <div v-else class="matches-container">
      <NTabs v-model:value="activeTab" type="line" animated>
        <NTabPane name="pending" :tab="$t('matches.pending')">
          <MatchCard
            v-for="match in pendingMatches"
            :key="match.id"
            :match="match"
            @click="viewMatch(match.id)"
          />
          <NEmpty v-if="pendingMatches.length === 0" :description="$t('matches.no_pending_matches')" />
        </NTabPane>

        <NTabPane name="accepted" :tab="$t('matches.accepted')">
          <MatchCard
            v-for="match in acceptedMatches"
            :key="match.id"
            :match="match"
            @click="viewMatch(match.id)"
          />
          <NEmpty v-if="acceptedMatches.length === 0" :description="$t('matches.no_accepted_matches')" />
        </NTabPane>

        <NTabPane name="completed" :tab="$t('matches.completed')">
          <MatchCard
            v-for="match in completedMatches"
            :key="match.id"
            :match="match"
            @click="viewMatch(match.id)"
          />
          <NEmpty v-if="completedMatches.length === 0" :description="$t('matches.no_completed_matches')" />
        </NTabPane>
      </NTabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NTabs, NTabPane, NEmpty } from 'naive-ui'
import { useMatchStore } from '../stores/matchStore'
import MatchCard from '../components/MatchCard.vue'

const router = useRouter()
const matchStore = useMatchStore()

const activeTab = ref('pending')

const isLoading = computed(() => matchStore.isLoading)
const error = computed(() => matchStore.error)
const pendingMatches = computed(() => matchStore.pendingMatches)
const acceptedMatches = computed(() => matchStore.acceptedMatches)
const completedMatches = computed(() => [...matchStore.rejectedMatches])

function viewMatch(id: string): void {
  router.push(`/app/matches/${id}`)
}

onMounted(() => {
  matchStore.fetchMyMatches()
})
</script>

<style scoped>
.matches-view {
  max-width: 1000px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--spacing-xl);
}

.view-header h1 {
  color: var(--color-text-primary);
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-md);
}

.loading-state,
.error-state {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--color-text-secondary);
}
</style>