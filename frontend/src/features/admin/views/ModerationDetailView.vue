<template>
  <div class="moderation-detail">
    <div class="moderation-detail__header">
      <h1>{{ $t('admin.listing_detail') }}</h1>
      <AppButton
        variant="secondary"
        size="sm"
        @click="$router.back()"
      >
        {{ $t('common.back') }}
      </AppButton>
    </div>

    <div
      v-if="isLoading"
      class="moderation-detail__loading"
    >
      {{ $t('common.loading') }}
    </div>

    <div
      v-else-if="error"
      class="moderation-detail__error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="listing"
      class="moderation-detail__content"
    >
      <div class="moderation-detail__section">
        <h2>{{ $t('admin.listing_info') }}</h2>
        <div class="moderation-detail__grid">
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.bank_name') }}</span>
            <span class="moderation-detail__value">{{ listing.bank_name }}</span>
          </div>
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.cheque_serial') }}</span>
            <span class="moderation-detail__value">{{ listing.cheque_serial_number }}</span>
          </div>
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.face_amount') }}</span>
            <span class="moderation-detail__value">{{ formatCurrency(listing.face_amount) }} {{ $t('common.rial') }}</span>
          </div>
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.due_date') }}</span>
            <span class="moderation-detail__value">{{ listing.due_date }}</span>
          </div>
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.risk_tier') }}</span>
            <span class="moderation-detail__value">{{ listing.risk_tier || '—' }}</span>
          </div>
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.status') }}</span>
            <span class="moderation-detail__value">{{ listing.status }}</span>
          </div>
        </div>
      </div>

      <div class="moderation-detail__section">
        <h2>{{ $t('admin.issuer_info') }}</h2>
        <IssuerInfo
          :issuer="{
            name: listing.issuer_profile?.name || listing.issuer_name,
            national_or_company_id: listing.issuer_profile?.national_or_company_id || listing.issuer_national_id,
            credit_score: listing.issuer_profile?.credit_score ?? null,
          }"
        />
      </div>

      <div
        v-if="listing.status === 'rejected'"
        class="moderation-detail__section"
      >
        <h2>{{ $t('admin.rejection_info') }}</h2>
        <div class="moderation-detail__grid">
          <div class="moderation-detail__field">
            <span class="moderation-detail__label">{{ $t('admin.rejection_code') }}</span>
            <span class="moderation-detail__value">{{ listing.rejection_code }}</span>
          </div>
          <div class="moderation-detail__field moderation-detail__field--full">
            <span class="moderation-detail__label">{{ $t('admin.rejection_reason') }}</span>
            <span class="moderation-detail__value">{{ listing.rejection_reason }}</span>
          </div>
        </div>
      </div>

      <div
        v-if="listing.status === 'pending_moderation'"
        class="moderation-detail__section moderation-detail__section--actions"
      >
        <AppButton
          variant="teal"
          :loading="isProcessing"
          @click="handleApprove"
        >
          {{ $t('admin.approve') }}
        </AppButton>
        <AppButton
          variant="danger"
          :loading="isProcessing"
          @click="openRejectModal"
        >
          {{ $t('admin.reject') }}
        </AppButton>
      </div>
    </div>
  </div>

  <NModal
    v-model:show="showRejectModal"
    preset="dialog"
    :title="$t('admin.reject_listing')"
  >
    <RejectionForm v-model="rejectionForm" />
    <template #action>
      <AppButton
        :label="$t('common.cancel')"
        variant="secondary"
        @click="showRejectModal = false"
      />
      <AppButton
        :label="$t('admin.confirm_reject')"
        :loading="isProcessing"
        variant="danger"
        @click="confirmReject"
      />
    </template>
  </NModal>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { NModal } from 'naive-ui'
import { ListingService } from '@/features/listings/services/listingService'
import { REJECTION_CODE_LABELS } from '@/features/listings/types/listing'
import IssuerInfo from '../components/IssuerInfo.vue'
import RejectionForm from '../components/RejectionForm.vue'
import AppButton from '@/components/ui/AppButton.vue'
import type { ChequeListing, RejectionCode } from '@/features/listings/types/listing'

const route = useRoute()

const listing = ref<ChequeListing | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)
const isProcessing = ref(false)
const showRejectModal = ref(false)
const rejectionForm = ref<{ code: RejectionCode; note: string }>({
  code: 'MOD_101',
  note: '',
})

function formatCurrency(value: number): string {
  return value.toLocaleString('fa-IR')
}

async function fetchListing(): Promise<void> {
  isLoading.value = true
  error.value = null
  try {
    const id = route.params.id as string
    listing.value = await ListingService.getListing(id)
  } catch (err: unknown) {
    const anyErr = err as { response?: { data?: { error?: { message?: string } } } }
    error.value = anyErr?.response?.data?.error?.message || 'error.unknown'
  } finally {
    isLoading.value = false
  }
}

async function handleApprove(): Promise<void> {
  if (!listing.value) return
  isProcessing.value = true
  try {
    await ListingService.moderateListing(listing.value.id, { decision: 'approve' })
    showRejectModal.value = false
    await fetchListing()
  } catch (err) {
    console.error('Failed to approve:', err)
  } finally {
    isProcessing.value = false
  }
}

function openRejectModal(): void {
  rejectionForm.value = { code: 'MOD_101', note: '' }
  showRejectModal.value = true
}

async function confirmReject(): Promise<void> {
  if (!listing.value || !rejectionForm.value.code || !rejectionForm.value.note) return
  isProcessing.value = true
  try {
    await ListingService.moderateListing(listing.value.id, {
      decision: 'reject',
      rejection_code: rejectionForm.value.code,
      rejection_note: rejectionForm.value.note,
    })
    showRejectModal.value = false
    await fetchListing()
  } catch (err) {
    console.error('Failed to reject:', err)
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  fetchListing()
})
</script>

<style scoped>
.moderation-detail {
  max-width: 900px;
  margin: 0 auto;
}

.moderation-detail__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.moderation-detail__header h1 {
  color: var(--text1);
  font-size: var(--font-size-xl);
  margin: 0;
}

.moderation-detail__loading,
.moderation-detail__error {
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}

.moderation-detail__section {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.moderation-detail__section h2 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text1);
  margin: 0 0 var(--spacing-md);
}

.moderation-detail__section--actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
}

.moderation-detail__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.moderation-detail__field {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.moderation-detail__field--full {
  grid-column: 1 / -1;
}

.moderation-detail__label {
  font-size: var(--font-size-sm);
  color: var(--text2);
}

.moderation-detail__value {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text1);
}

@media (max-width: 768px) {
  .moderation-detail__grid {
    grid-template-columns: 1fr;
  }

  .moderation-detail__header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .moderation-detail__section--actions {
    flex-direction: column;
  }
}
</style>
