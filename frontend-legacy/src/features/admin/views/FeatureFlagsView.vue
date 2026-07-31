<template>
  <div class="feature-flags-view">
    <div class="view-header">
      <h1>{{ $t('admin.feature_flags_title') }}</h1>
      <p class="subtitle">
        {{ $t('admin.feature_flags_subtitle') }}
      </p>
    </div>

    <div
      v-if="isLoading"
      class="loading-state"
    >
      <Skeleton :lines="6" />
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      <EmptyState
        :title="$t('admin.error_title')"
        :description="$t('admin.feature_flags_error_description')"
        icon="⚠️"
      >
        <template #actions>
          <Button
            variant="primary"
            @click="retry"
          >
            {{ $t('common.retry') }}
          </Button>
        </template>
      </EmptyState>
    </div>

    <div
      v-else
      class="flags-container"
    >
      <NDataTable
        :columns="columns"
        :data="flags"
        :bordered="false"
        :single-line="false"
        size="medium"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted } from 'vue'
import { NDataTable, NSwitch } from 'naive-ui'
import { useAdminStore } from '@/features/admin/stores/adminStore'
import { useErrorHandler } from '@/composables/useErrorHandler'
import { useToast } from '@/composables/useToast'
import { useI18n } from 'vue-i18n'
import Skeleton from '@/components/ui/Skeleton.vue'
import EmptyState from '@/components/EmptyState.vue'
import Button from '@/components/ui/Button.vue'

const { t } = useI18n()
const adminStore = useAdminStore()
const errorHandler = useErrorHandler()
const toast = useToast()

const isLoading = computed(() => adminStore.isLoading)
const error = computed(() => adminStore.error)
const flags = computed(() => adminStore.flags)

const columns = computed(() => [
  {
    title: t('admin.feature_flag_key'),
    key: 'key',
    width: 240,
  },
  {
    title: t('admin.feature_flag_description'),
    key: 'description',
    width: 320,
  },
  {
    title: t('admin.feature_flag_status'),
    key: 'is_enabled',
    width: 160,
    render: (row: { key: string; is_enabled: boolean; is_system: boolean }) => {
      return h(NSwitch, {
        value: row.is_enabled,
        disabled: row.is_system,
        'onUpdate:value': (value: boolean) => handleToggle(row.key, value),
      })
    },
  },
])

async function handleToggle(key: string, value: boolean): Promise<void> {
  try {
    await adminStore.updateFlag(key, value)
    toast.showToast(
      value ? 'feature_flags.flag_enabled' : 'feature_flags.flag_disabled',
      'success',
    )
  } catch (err: unknown) {
    errorHandler.handleError(err)
  }
}

async function retry(): Promise<void> {
  await adminStore.fetchFlags()
}

onMounted(() => {
  adminStore.fetchFlags()
})
</script>

<style scoped>
.feature-flags-view {
  max-width: 1200px;
  margin: 0 auto;
}

.view-header {
  margin-bottom: var(--spacing-xl);
}

.view-header h1 {
  color: var(--text1);
  font-size: var(--font-size-xl);
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  color: var(--text2);
  font-size: var(--font-size-md);
}

.loading-state,
.error-state {
  padding: var(--spacing-xl) 0;
}

.flags-container {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  padding: var(--spacing-md);
}
</style>
