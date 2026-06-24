<template>
  <div
    class="listing-card-compact"
    :class="{ 'listing-card-compact--clickable': clickable }"
    @click="onClick"
  >
    <div class="row-icon">
      <svg
        viewBox="0 0 24 24"
        width="20"
        height="20"
        fill="var(--gold-light)"
      >
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 4h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S9 13.88 9 12.5 10.12 10 11.5 10c.57 0 1.08.19 1.5.5V7h4v0z" />
      </svg>
    </div>
    <div class="row-info">
      <div class="row-title">
        {{ listing.title }}
      </div>
      <div class="row-meta">
        {{ listing.meta }}
      </div>
    </div>
    <div class="row-amount">
      {{ formatCurrency(listing.face_amount) }}
      <small>ریال</small>
    </div>
    <div class="row-status">
      <StatusPill :variant="statusVariant">
        {{ listing.statusLabel }}
      </StatusPill>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StatusPill from '@/components/StatusPill.vue'
import type { ChequeListing } from '@/features/listings/types/listing'

const props = withDefaults(
  defineProps<{
    listing: ChequeListing & { title: string; meta: string; statusLabel: string; statusVariant: 'published' | 'matched' | 'pending' | 'reviewing' | 'rejected' | 'approved' | 'kyc-pending' }
    clickable?: boolean
  }>(),
  {
    clickable: true,
  }
)

const emit = defineEmits<{
  (e: 'click'): void
}>()

const statusVariant = computed(() => {
  switch (props.listing.status) {
    case 'published':
      return 'published'
    case 'matched':
      return 'matched'
    case 'pending_moderation':
      return 'pending'
    case 'rejected':
      return 'rejected'
    case 'settled':
      return 'matched'
    case 'expired':
      return 'rejected'
    default:
      return 'reviewing'
  }
})

const formatCurrency = (value: number) => value.toLocaleString('fa-IR')

const onClick = () => {
  if (props.clickable) emit('click')
}
</script>

<style>
.listing-card-compact {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 1rem;
  align-items: center;
  transition: border-color 0.2s;
}

.listing-card-compact--clickable {
  cursor: pointer;
}

.listing-card-compact--clickable:hover {
  border-color: var(--border2);
}

.row-icon {
  width: 40px;
  height: 40px;
  background: var(--navy);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.row-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--navy);
  margin: 0 0 0.2rem;
}

.row-meta {
  font-size: var(--font-size-xs);
  color: var(--text3);
  margin: 0;
}

.row-amount {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text1);
  text-align: left;
}

.row-amount small {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}

.row-status {
  text-align: left;
}

@media (max-width: 768px) {
  .listing-card-compact {
    grid-template-columns: 1fr auto;
  }

  .row-icon {
    display: none;
  }

  .row-amount {
    text-align: right;
  }
}
</style>
