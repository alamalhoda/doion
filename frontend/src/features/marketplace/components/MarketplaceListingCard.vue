<template>
  <div
    class="listing-card"
    :class="{ 'listing-card--hoverable': hoverable }"
    @click="onClick"
  >
    <div class="card-header">
      <div class="card-issuer">
        <span class="card-issuer-dot" />
        {{ listing.issuer }}
      </div>
      <RiskBadge :risk="listing.risk" />
    </div>
    <div class="card-body">
      <div class="card-amount">
        <span>ریال</span>{{ formatCurrency(listing.amount) }}
      </div>
      <div class="card-meta">
        <div class="meta-item">
          <div class="meta-key">
            بانک
          </div>
          <div class="meta-val">
            {{ listing.bank }}
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            سررسید
          </div>
          <div class="meta-val">
            {{ listing.dueDate }}
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            روز تا سررسید
          </div>
          <div class="meta-val">
            {{ listing.days }} روز
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-key">
            نوع صادرکننده
          </div>
          <div class="meta-val">
            {{ listing.issuerType }}
          </div>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <div>
        <div class="discount-rate">
          {{ listing.rate }}
        </div>
        <div class="discount-label">
          نرخ تنزیل پیشنهادی
        </div>
      </div>
      <button
        class="btn btn--sm btn--primary"
        @click.stop="onInterest"
      >
        ابراز تمایل
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import RiskBadge from '@/components/RiskBadge.vue'
import type { ChequeListing } from '@/features/listings/types/listing'

withDefaults(
  defineProps<{
    listing: ChequeListing & { issuer: string; issuerType: string; bank: string; amount: number; days: number; risk: 'low' | 'mid' | 'high'; rate: string; dueDate: string }
    hoverable?: boolean
  }>(),
  {
    hoverable: true,
  }
)

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'interest'): void
}>()

const formatCurrency = (value: number) => value.toLocaleString('fa-IR')

const onClick = () => emit('click')
const onInterest = () => emit('interest')
</script>

<style>
.listing-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s;
}

.listing-card--hoverable:hover {
  border-color: var(--navy-light);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.card-header {
  background: var(--navy);
  padding: 0.85rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: repeating-linear-gradient(
    90deg,
    rgba(201, 150, 10, 0.4) 0,
    rgba(201, 150, 10, 0.4) 12px,
    transparent 12px,
    transparent 18px
  );
}

.card-issuer {
  color: rgba(255, 255, 255, 0.85);
  font-size: var(--font-size-xs);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.card-issuer-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--gold-light);
}

.card-body {
  padding: 1.1rem;
}

.card-amount {
  font-size: 1.65rem;
  font-weight: var(--font-weight-bold);
  color: var(--navy);
  font-variant-numeric: tabular-nums;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.4rem 0.75rem;
  display: inline-block;
  margin-bottom: 0.85rem;
  background: var(--surface2);
}

.card-amount span {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-normal);
  color: var(--text3);
  margin-left: 0.3rem;
}

.card-meta {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem 0.5rem;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.meta-key {
  font-size: var(--font-size-xs);
  color: var(--text3);
}

.meta-val {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
}

.card-footer {
  border-top: 1px solid var(--border);
  padding: 0.75rem 1.1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.discount-rate {
  font-size: 1.15rem;
  font-weight: var(--font-weight-bold);
  color: var(--teal);
}

.discount-label {
  font-size: var(--font-size-xs);
  color: var(--text3);
  font-weight: var(--font-weight-normal);
}
</style>
