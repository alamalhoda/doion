<template>
  <div class="risk-badge" :class="`risk-badge--${variant}`">
    {{ label }}
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    risk: 'low' | 'mid' | 'high'
  }>(),
  {
    risk: 'low',
  }
)

const label = computed(() => {
  switch (props.risk) {
    case 'low':
      return 'کم ریسک'
    case 'mid':
      return 'ریسک متوسط'
    case 'high':
      return 'پر ریسک'
    default:
      return ''
  }
})
</script>

<style>
.risk-badge {
  display: inline-flex;
  align-items: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius-sm);
  line-height: 1.4;
}

.risk-badge--low {
  background: #0d4f2a;
  color: #7ffab0;
}

.risk-badge--mid {
  background: #5c3700;
  color: #ffbe68;
}

.risk-badge--high {
  background: #4d1500;
  color: #ffb0a0;
}
</style>
