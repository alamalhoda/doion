<template>
  <aside class="filter-sidebar">
    <div class="filter-sidebar-title">
      فیلترها
    </div>

    <div class="filter-group">
      <label class="filter-label">سطح ریسک</label>
      <label
        v-for="opt in riskOptions"
        :key="opt.value"
        class="filter-opt"
      >
        <input
          type="checkbox"
          :checked="opt.checked"
          @change="toggleRisk(opt.value, $event)"
        >
        <span>{{ opt.label }}</span>
      </label>
    </div>

    <div class="filter-group">
      <label class="filter-label">محدوده مبلغ (ریال)</label>
      <div class="filter-range">
        <input
          type="number"
          class="filter-input"
          placeholder="حداقل"
          :value="model.min_amount ?? ''"
          @input="updateFilter('min_amount', toNumber($event.target.value))"
        >
        <span class="filter-range-sep">—</span>
        <input
          type="number"
          class="filter-input"
          placeholder="حداکثر"
          :value="model.max_amount ?? ''"
          @input="updateFilter('max_amount', toNumber($event.target.value))"
        >
      </div>
    </div>

    <div class="filter-group">
      <label class="filter-label">حداکثر روز تا سررسید</label>
      <input
        type="number"
        class="filter-input"
        placeholder="مثلاً ۳۰"
        :value="model.max_days_to_due ?? ''"
        @input="updateFilter('max_days_to_due', toNumber($event.target.value))"
      >
    </div>

    <div class="filter-group">
      <label class="filter-label">نوع صادرکننده</label>
      <select
        class="filter-select"
        :value="model.issuer_type ?? ''"
        @change="updateFilter('issuer_type', ($event.target as HTMLSelectElement).value || undefined)"
      >
        <option value="">
          همه
        </option>
        <option value="legal">
          حقوقی
        </option>
        <option value="natural">
          حقیقی
        </option>
      </select>
    </div>

    <div class="filter-group">
      <label class="filter-label">نام بانک</label>
      <input
        type="text"
        class="filter-input"
        placeholder="جستجوی بانک..."
        :value="model.bank_name ?? ''"
        @input="updateFilter('bank_name', ($event.target as HTMLInputElement).value || undefined)"
      >
    </div>

    <div class="filter-actions">
      <button
        class="btn btn--primary btn--block"
        @click="$emit('apply')"
      >
        اعمال فیلتر
      </button>
      <button
        class="btn btn--secondary btn--block"
        @click="$emit('reset')"
      >
        پاک‌سازی
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { MarketplaceFilters } from '../stores/marketplaceStore'

const props = defineProps<{
  modelValue: MarketplaceFilters
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: MarketplaceFilters): void
  (e: 'apply'): void
  (e: 'reset'): void
}>()

const model = ref<MarketplaceFilters>({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  model.value = { ...newVal }
}, { deep: true })

const riskOptions = ref([
  { value: 'low', label: 'کم ریسک', checked: false },
  { value: 'medium', label: 'ریسک متوسط', checked: false },
  { value: 'high', label: 'پر ریسک', checked: false },
])

watch(() => model.value.risk_tier, (newVal) => {
  riskOptions.value = riskOptions.value.map(opt => ({
    ...opt,
    checked: newVal === opt.value,
  }))
}, { immediate: true })

function toggleRisk(value: string, event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  riskOptions.value = riskOptions.value.map(opt => ({
    ...opt,
    checked: opt.value === value ? checked : false,
  }))

  const newFilter = checked ? (value as MarketplaceFilters['risk_tier']) : undefined
  model.value = { ...model.value, risk_tier: newFilter }
  emit('update:modelValue', model.value)
}

function updateFilter(key: keyof MarketplaceFilters, value: unknown) {
  model.value = { ...model.value, [key]: value } as MarketplaceFilters
  emit('update:modelValue', model.value)
}

function toNumber(value: string): number | undefined {
  const n = Number(value)
  return value === '' ? undefined : (Number.isNaN(n) ? undefined : n)
}
</script>

<style>
.filter-sidebar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
}

.filter-sidebar-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.filter-group {
  margin-bottom: 1.25rem;
}

.filter-label {
  display: block;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text2);
  margin-bottom: 0.5rem;
}

.filter-opt {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: var(--font-size-base);
  color: var(--text2);
  margin-bottom: 0.35rem;
}

.filter-opt input[type='checkbox'] {
  accent-color: var(--navy);
  width: 15px;
  height: 15px;
}

.filter-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-range-sep {
  color: var(--text3);
}

.filter-input,
.filter-select {
  width: 100%;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.4rem 0.6rem;
  font-size: var(--font-size-base);
  color: var(--text2);
  background: var(--surface);
  box-sizing: border-box;
}

.filter-input::placeholder {
  color: var(--text3);
}

.filter-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}
</style>
