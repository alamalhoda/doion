<template>
  <span class="status-pill" :class="`status-pill--${variant}`">
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'published' | 'pending' | 'matched' | 'reviewing' | 'rejected' | 'approved' | 'kyc-pending'
  }>(),
  {
    variant: 'published',
  }
)

const label = computed(() => {
  switch (props.variant) {
    case 'published':
      return 'منتشر شده'
    case 'pending':
      return 'در انتظار بررسی'
    case 'matched':
      return 'تطابق یافته'
    case 'reviewing':
      return 'در حال بررسی'
    case 'rejected':
      return 'رد شده'
    case 'approved':
      return 'تایید شده'
    case 'kyc-pending':
      return 'در انتظار کایسی'
    default:
      return ''
  }
})
</script>

<style>
.status-pill {
  display: inline-flex;
  align-items: center;
  font-size: 0.72rem;
  font-weight: var(--font-weight-semibold);
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  line-height: 1.4;
  white-space: nowrap;
}

.status-pill--published {
  background: #e6f4f3;
  color: #0a4e49;
}

.status-pill--pending {
  background: #fef3e6;
  color: #7a4000;
}

.status-pill--matched {
  background: #eef0fe;
  color: #3d34a0;
}

.status-pill--reviewing {
  background: var(--surface2);
  color: var(--text2);
}

.status-pill--rejected {
  background: var(--red-light);
  color: #7a1a1a;
}

.status-pill--approved {
  background: #e6f4f3;
  color: #0a4e49;
}

.status-pill--kyc-pending {
  background: #eef0fe;
  color: #3d34a0;
}
</style>
