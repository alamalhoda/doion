<!-- DataTable Component -->
<template>
  <div class="data-table-container">
    <!-- Optional toolbar -->
    <div
      v-if="$slots.toolbar"
      class="data-table-toolbar"
    >
      <slot name="toolbar" />
    </div>

    <div class="data-table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th
              v-for="col in columns"
              :key="col.key"
              :style="{ width: col.width, textAlign: col.align || 'right' }"
            >
              {{ col.label }}
            </th>
            <th
              v-if="hasActions"
              style="width: 120px; text-align: center"
            >
              عملیات
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-if="loading"
            class="data-table-loading"
          >
            <td :colspan="columns.length + (hasActions ? 1 : 0)">
              <div class="data-table-loading-indicator">
                <span class="data-table-loading-text">در حال بارگذاری...</span>
              </div>
            </td>
          </tr>
          <tr
            v-else-if="data.length === 0"
            class="data-table-empty"
          >
            <td :colspan="columns.length + (hasActions ? 1 : 0)">
              <div class="data-table-empty-content">
                <svg
                  class="data-table-empty-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.5"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                  />
                </svg>
                <span>داده‌ای برای نمایش وجود ندارد</span>
              </div>
            </td>
          </tr>
          <tr
            v-for="(row, idx) in data"
            :key="getRowKey(row, idx)"
            class="data-table-row"
            :class="{ 'data-table-row--clickable': clickable }"
            @click="onRowClick(row)"
          >
            <td
              v-for="col in columns"
              :key="col.key"
              class="data-table-cell"
              :style="{ textAlign: col.align || 'right' }"
            >
              <!-- Custom slot for cell -->
              <slot
                v-if="$slots[`cell-${col.key}`]"
                :name="`cell-${String(col.key)}`"
                :row="row"
                :value="row[String(col.key)]"
              />
              <!-- Badge slot for status-like columns -->
              <slot
                v-else-if="$slots.badge"
                name="badge"
                :row="row"
                :col="col"
              />
              <!-- Default text -->
              <span
                v-else
                class="data-table-text"
              >{{ row[String(col.key)] }}</span>
            </td>
            <td
              v-if="hasActions"
              class="data-table-cell data-table-actions"
            >
              <slot
                name="actions"
                :row="row"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Optional pagination -->
    <div
      v-if="showPagination"
      class="data-table-pagination"
    >
      <slot name="pagination" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, useSlots } from 'vue'

export interface Column {
  key: string
  label: string
  width?: string
  align?: 'right' | 'left' | 'center'
}

interface Props {
  columns: Column[]
  data: Record<string, unknown>[]
  loading?: boolean
  clickable?: boolean
  showPagination?: boolean
}

defineProps<Props>()

const getRowKey = (row: Record<string, unknown>, idx: number): string | number => {
  const id = row.id
  return typeof id === 'string' || typeof id === 'number' ? id : idx
}

const slots = useSlots()
const hasActions = computed(() => slots.actions !== undefined)

const emit = defineEmits<{
  (e: 'row-click', row: Record<string, unknown>): void
}>()

const onRowClick = (row: Record<string, unknown>) => {
  if (!hasActions.value) {
    emit('row-click', row)
  }
}
</script>

<style>
.data-table-container {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.data-table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-base);
}

/* Header */
.data-table thead {
  background: var(--surface2);
  border-bottom: 2px solid var(--border);
}

.data-table th {
  padding: 0.85rem 1.1rem;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--text2);
  text-align: right;
  letter-spacing: 0.02em;
  white-space: nowrap;
  user-select: none;
}

/* Body */
.data-table tbody tr {
  border-bottom: 1px solid var(--border);
  transition: background-color var(--transition-fast);
}

.data-table tbody tr:last-child {
  border-bottom: none;
}

.data-table tbody tr:hover {
  background-color: var(--surface2);
}

.data-table-row--clickable {
  cursor: pointer;
}

.data-table-row--clickable:hover {
  background-color: var(--surface2);
}

/* Cells */
.data-table-cell {
  padding: 0.85rem 1.1rem;
  color: var(--text1);
  vertical-align: middle;
}

.data-table-text {
  color: var(--text1);
  font-size: var(--font-size-base);
}

/* Actions column */
.data-table-actions {
  text-align: center;
  white-space: nowrap;
}

/* Loading state */
.data-table-loading td,
.data-table-empty td {
  padding: 2.5rem 1rem;
}

.data-table-loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.data-table-loading-text {
  color: var(--text3);
  font-size: var(--font-size-base);
}

/* Empty state */
.data-table-empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.data-table-empty-icon {
  width: 40px;
  height: 40px;
  color: var(--border2);
}

.data-table-empty-content span {
  color: var(--text3);
  font-size: var(--font-size-base);
}

/* Pagination */
.data-table-pagination {
  border-top: 1px solid var(--border);
  padding: 1rem 1.1rem;
}

@media (max-width: 768px) {
  .data-table th,
  .data-table-cell {
    padding: 0.6rem 0.75rem;
  }
}
</style>
