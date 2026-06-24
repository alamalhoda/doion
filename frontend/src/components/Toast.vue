<template>
  <Transition name="toast">
    <div
      v-if="visible"
      class="toast"
      :class="`toast--${variant}`"
    >
      <span class="toast-message">{{ message }}</span>
      <button
        class="toast-close"
        aria-label="بستن"
        @click="close"
      >
        <svg
          viewBox="0 0 24 24"
          width="16"
          height="16"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    message: string
    variant?: 'default' | 'success' | 'error' | 'warning'
    duration?: number
  }>(),
  {
    variant: 'default',
    duration: 3000,
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const visible = ref(false)
let timer: ReturnType<typeof setTimeout> | null = null

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      visible.value = true
      if (timer) clearTimeout(timer)
      timer = setTimeout(() => {
        visible.value = false
        emit('update:modelValue', false)
      }, props.duration)
    } else {
      visible.value = false
    }
  },
  { immediate: true }
)

const close = () => {
  visible.value = false
  if (timer) clearTimeout(timer)
  emit('update:modelValue', false)
}
</script>

<style>
.toast {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--navy);
  color: #fff;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: var(--shadow-lg);
  z-index: var(--z-toast);
  pointer-events: auto;
  max-width: calc(100vw - 2rem);
}

.toast--success {
  background: var(--teal);
}

.toast--error {
  background: var(--red);
}

.toast--warning {
  background: var(--orange);
}

.toast-close {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: #fff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background var(--transition-fast);
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

.toast-message {
  line-height: 1.4;
}

/* Transition */
.toast-enter-active,
.toast-leave-active {
  transition: all var(--transition-base);
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
}
</style>
