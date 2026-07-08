<template>
  <div
    class="skeleton"
    :style="rootStyle"
  >
    <div
      v-for="line in lines"
      :key="line"
      class="skeleton__line"
      :style="[lineStyle, { width: lineWidths[line - 1] || '100%' }]"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  width?: string | number
  height?: string | number
  rounded?: string | number
  lines?: number
}

const props = withDefaults(defineProps<Props>(), {
  width: '100%',
  height: 16,
  rounded: 4,
  lines: 1,
})

const rootStyle = {
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
}

const lineStyle = {
  height: typeof props.height === 'number' ? `${props.height}px` : props.height,
  borderRadius: typeof props.rounded === 'number' ? `${props.rounded}px` : props.rounded,
}

const lineWidths = ['100%', '85%', '70%', '90%', '60%', '80%', '75%', '95%']
</script>

<style scoped>
.skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.skeleton__line {
  background: linear-gradient(90deg, var(--surface2) 25%, var(--border) 50%, var(--surface2) 75%);
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
