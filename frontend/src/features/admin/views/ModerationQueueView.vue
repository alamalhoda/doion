<template>
  <div class="admin-moderation-view">
    <div class="view-header">
      <h1>{{ $t('admin.moderation_title') }}</h1>
      <p class="subtitle">
        {{ $t('admin.moderation_subtitle') }}
      </p>
    </div>

    <div
      v-if="isLoading"
      class="loading-state"
    >
      {{ $t('common.loading') }}
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
    </div>

    <div
      v-else
      class="moderation-container"
    >
      <NTabs
        v-model:value="activeTab"
        type="line"
        animated
      >
        <NTabPane
          name="pending"
          :tab="$t('admin.pending_review')"
        >
          <ModerationCard
            v-for="listing in pendingListings"
            :key="listing.id"
            :item="{
              id: listing.id,
              issuer: listing.issuer_profile?.name || '',
              bank: listing.bank_name || '',
              amount: listing.face_amount,
              dueDate: listing.due_date,
              risk: listing.risk_tier || '',
            }"
            @approve="handleApprove(listing.id)"
            @reject="handleReject(listing.id)"
            @view-detail="viewListing(listing.id)"
          />
          <NEmpty
            v-if="pendingListings.length === 0"
            :description="$t('admin.no_pending_listings')"
          />
        </NTabPane>

        <NTabPane
          name="approved"
          :tab="$t('admin.approved')"
        >
          <ModerationCard
            v-for="listing in approvedListings"
            :key="listing.id"
            readonly
            :item="{
              id: listing.id,
              issuer: listing.issuer_profile?.name || '',
              bank: listing.bank_name || '',
              amount: listing.face_amount,
              dueDate: listing.due_date,
              risk: listing.risk_tier || '',
              rejection_code: listing.rejection_code || '',
              rejection_note: listing.rejection_reason || '',
            }"
            @view-detail="viewListing(listing.id)"
          />
          <NEmpty
            v-if="approvedListings.length === 0"
            :description="$t('admin.no_approved_listings')"
          />
        </NTabPane>

        <NTabPane
          name="rejected"
          :tab="$t('admin.rejected')"
        >
          <ModerationCard
            v-for="listing in rejectedListings"
            :key="listing.id"
            readonly
            :item="{
              id: listing.id,
              issuer: listing.issuer_profile?.name || '',
              bank: listing.bank_name || '',
              amount: listing.face_amount,
              dueDate: listing.due_date,
              risk: listing.risk_tier || '',
              rejection_code: listing.rejection_code || '',
              rejection_note: listing.rejection_reason || '',
            }"
            @view-detail="viewListing(listing.id)"
          />
          <NEmpty
            v-if="rejectedListings.length === 0"
            :description="$t('admin.no_rejected_listings')"
          />
        </NTabPane>
      </NTabs>
    </div>

    <!-- Rejection Modal -->
    <NModal
      v-model:show="showRejectModal"
      preset="dialog"
      :title="$t('admin.reject_listing')"
    >
      <div class="reject-form">
        <p>{{ $t('admin.reject_reason_prompt') }}</p>
        <FormField
          v-model="rejectionCode"
          type="select"
          :label="$t('admin.rejection_code')"
          :options="rejectionCodeOptions"
          required
        />
        <FormField
          v-model="rejectionNote"
          type="textarea"
          :label="$t('admin.rejection_reason')"
          :rows="3"
          required
        />
      </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NTabs, NTabPane, NModal, NEmpty } from 'naive-ui'
import { useListingStore } from '@/features/listings/stores/listingStore'
import { ListingService } from '@/features/listings/services/listingService'
import { REJECTION_CODE_LABELS, type RejectionCode } from '@/features/listings/types/listing'
import FormField from '@/components/ui/FormField.vue'
import AppButton from '@/components/ui/AppButton.vue'
import ModerationCard from '../components/ModerationCard.vue'

const router = useRouter()
const listingStore = useListingStore()

const activeTab = ref('pending')
const showRejectModal = ref(false)
const rejectionCode = ref<RejectionCode | ''>('')
const rejectionNote = ref('')
const isProcessing = ref(false)
const listingToReject = ref<number | null>(null)

const rejectionCodeOptions = Object.entries(REJECTION_CODE_LABELS).map(
  ([value, label]) => ({ value, label })
)

const isLoading = computed(() => listingStore.isLoading)
const error = computed(() => listingStore.error)
const pendingListings = computed(() => listingStore.pendingListings)
const approvedListings = computed(() => listingStore.publishedListings)
const rejectedListings = computed(() =>
  listingStore.listings.filter(l => l.status === 'rejected')
)

function viewListing(id: number): void {
  router.push(`/admin/moderation/${id}`)
}

async function handleApprove(id: number): Promise<void> {
  isProcessing.value = true
  try {
    await ListingService.moderateListing(id, { decision: 'approve' })
    await listingStore.fetchModerationQueue()
  } catch (err) {
    console.error('Failed to approve listing:', err)
  } finally {
    isProcessing.value = false
  }
}

function handleReject(id: number): void {
  listingToReject.value = id
  rejectionCode.value = ''
  rejectionNote.value = ''
  showRejectModal.value = true
}

async function confirmReject(): Promise<void> {
  if (!listingToReject.value || !rejectionCode.value || !rejectionNote.value) return

  isProcessing.value = true
  try {
    await ListingService.moderateListing(listingToReject.value, {
      decision: 'reject',
      rejection_code: rejectionCode.value,
      rejection_note: rejectionNote.value,
    })
    showRejectModal.value = false
    await listingStore.fetchModerationQueue()
  } catch (err) {
    console.error('Failed to reject listing:', err)
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  listingStore.fetchModerationQueue()
})
</script>

<style scoped>
.admin-moderation-view {
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
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text2);
}

.reject-form {
  padding: var(--spacing-md) 0;
}

.reject-form p {
  margin-bottom: var(--spacing-md);
  color: var(--text2);
}
</style>